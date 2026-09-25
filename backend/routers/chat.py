from fastapi import APIRouter, HTTPException, Form
from typing import Optional
import uuid
from datetime import datetime, timezone
import numpy as np
from sentence_transformers import util
import logging

from database import db
from schemas import ChatResponse
from core.engine import search_engine
from core.retrieval import build_query_tokens, score_and_gate, build_vocab_index, THEORETICAL_MAX_RRF

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def legal_chat(
    message:    str           = Form(...),
    session_id: Optional[str] = Form(None),
    user_id:    Optional[str] = Form(None),
):
    try:
        session_id = str(session_id) if (session_id and not hasattr(session_id, 'default')) else str(uuid.uuid4())
        user_id    = str(user_id)    if (user_id    and not hasattr(user_id,    'default')) else None

        if len(message.split()) > 1000:
            return ChatResponse(response="Query too long.", session_id=session_id, laws=[])

        if not search_engine.laws or search_engine.bge_embeddings is None:
            return ChatResponse(response="System initializing.", session_id=session_id, laws=[])

        # ── Query processing (cleaning, direct article lookup, translation cache,
        #    synonym expansion, tokenization, spell correction) — shared logic,
        #    identical to metrics.py ──────────────────────────────────────────
        vocab_by_letter = search_engine.vocab_by_letter or build_vocab_index(search_engine.vocabulary)
        tokens = await build_query_tokens(message, search_engine, db, vocab_by_letter)
        msg_text      = tokens["message_text"]
        dir_idx       = tokens["dir_idx"]
        corr_tokens   = tokens["corrected_tokens"]
        q_set         = set(corr_tokens)

        if not corr_tokens and dir_idx is None:
            if any(t in msg_text for t in ["government employee", "kawani ng gobyerno", "civil service"]):
                return ChatResponse(
                    response="Government employees are governed by CSC, not the Labor Code.",
                    session_id=session_id, laws=[]
                )
            return ChatResponse(
                response="Query not related to Labor Law.",
                session_id=session_id, laws=[]
            )

        # ── BGE-M3 dense scores — encoded here since chat.py handles one query
        #    at a time (metrics.py batches many, for evaluation-time speed) ───
        encoder    = search_engine.get_bge_model()
        bge_scores = util.cos_sim(
            encoder.encode(tokens["query_text"], convert_to_tensor=True),
            search_engine.bge_embeddings
        )[0].cpu().numpy()

        limit = (await db.settings.find_one({"key": "chat_limit"}) or {}).get("value", 5)

        # ── BM25 + title boost + RRF fusion + domain gate + the 3 ranking gates
        #    — shared logic, identical to metrics.py ─────────────────────────
        scored = score_and_gate(search_engine, corr_tokens, dir_idx, bge_scores)
        f_scores = scored["final_scores"]

        if not scored["domain_gate_passed"]:
            return ChatResponse(
                response="Query not related to Labor Law.",
                session_id=session_id, laws=[]
            )

        matched = []

        # ── Direct article-number hit → 100% ─────────────────────────────────
        if dir_idx is not None:
            d_law = search_engine.laws[dir_idx].copy()
            d_law['best_match_chunk'] = max(
                d_law.get('chunks', []),
                key=lambda c: len(q_set.intersection(set(c.lower().split()))) / max(len(c.split()), 1),
                default=""
            ) or d_law.get('simplified_text', '')
            d_law['accuracy'] = "100%"   # exact article request = perfect match
            matched.append(d_law)

        # ── Ranked hybrid retrieval — gates already applied by score_and_gate;
        #    cap against the TRUE running total, since a direct hit may already
        #    occupy one slot ────────────────────────────────────────────────
        for idx in scored["ranked_indices"]:
            if len(matched) >= limit:
                break

            ld = search_engine.laws[idx].copy()
            ld['best_match_chunk'] = max(
                ld.get('chunks', []),
                key=lambda c: len(q_set.intersection(set(c.lower().split()))) / max(len(c.split()), 1),
                default=""
            ) or ld.get('simplified_text', '')

            # ── Accuracy: same formula as original server.py ─────────────────
            # Min-Max normalised against theoretical max RRF = (1/61) × 3
            # Capped at 99% (direct hits get 100%)
            min_max_scaled = (float(f_scores[idx]) / THEORETICAL_MAX_RRF) * 100
            raw_percentage = min(int(min_max_scaled), 99)
            ld['accuracy'] = f"{raw_percentage}%"

            matched.append(ld)

        resp = (
            f"I found {len(matched)} relevant article(s) regarding your query:"
            if matched else "No specific laws found."
        )

        await db.chat_history.insert_one({
            "id": str(uuid.uuid4()), "session_id": session_id, "user_id": user_id,
            "user_message": message, "assistant_response": resp,
            "laws": matched, "created_at": datetime.now(timezone.utc).isoformat()
        })
        return ChatResponse(response=resp, session_id=session_id, laws=matched)

    except Exception as e:
        logger.error(f"CHAT ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# SESSION ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/sessions")
async def get_sessions(user_id: str, skip: int = 0, limit: int = 20):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {
            "_id":          "$session_id",
            "last_message": {"$last": "$user_message"},
            "timestamp":    {"$max":  "$created_at"},
        }},
        {"$sort": {"timestamp": -1}},
        {"$facet": {
            "total":    [{"$count": "count"}],
            "sessions": [{"$skip": skip}, {"$limit": limit}],
            "oldest":   [{"$sort": {"timestamp": 1}}, {"$limit": 1}],
        }},
    ]
    result = await db.chat_history.aggregate(pipeline).to_list(1)
    if not result:
        return {"sessions": [], "total": 0, "oldest_date": None}
    data   = result[0]
    total  = data["total"][0]["count"]      if data["total"]  else 0
    oldest = data["oldest"][0]["timestamp"] if data["oldest"] else None
    return {"sessions": data["sessions"], "total": total, "oldest_date": oldest}


@router.get("/sessions/{session_id}")
async def get_session_messages(session_id: str):
    messages = await db.chat_history.find(
        {"session_id": session_id}, {"_id": 0}
    ).sort("created_at", 1).to_list(1000)
    if not messages:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"messages": messages}


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    result = await db.chat_history.delete_many({"session_id": session_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"message": f"Deleted {result.deleted_count} messages."}