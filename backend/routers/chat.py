from fastapi import APIRouter, HTTPException, Form
from typing import Optional, Literal
from pydantic import BaseModel
import uuid
from datetime import datetime, timezone
import numpy as np
from sentence_transformers import util
import logging

from database import db
from schemas import (
    ChatResponse,
    FeedbackRequest,
    LatestFeedbackResponse,
    FeedbackHistoryItem,
)
from core.engine import search_engine
from core.retrieval import (
    build_query_tokens, 
    score_and_gate, 
    build_vocab_index, 
    THEORETICAL_MAX_RRF
)

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
        message_id = str(uuid.uuid4())

        if len(message.split()) > 1000:
            return ChatResponse(
                message_id=message_id,
                response="Query too long.",
                session_id=session_id,
                translated_query="",
                laws=[]
            )

        if not search_engine.laws or search_engine.bge_embeddings is None:
            return ChatResponse(
                message_id=message_id,
                response="System initializing.",
                session_id=session_id,
                translated_query="",
                laws=[]
            )

        # ── Query processing & NLP normalization (Translation, spelling, etc.) ──
        vocab_by_letter = search_engine.vocab_by_letter or build_vocab_index(search_engine.vocabulary)
        tokens = await build_query_tokens(message, search_engine, db, vocab_by_letter)
        
        msg_text         = tokens["message_text"]
        dir_idx          = tokens["dir_idx"]
        corr_tokens      = tokens["corrected_tokens"]
        translated_query = tokens["query_text"]  # Capturing the normalized/translated query
        q_set            = set(corr_tokens)

        if not corr_tokens and dir_idx is None:
            if any(t in msg_text for t in ["government employee", "kawani ng gobyerno", "civil service"]):
                return ChatResponse(
                    message_id=message_id,
                    response="Government employees are governed by CSC, not the Labor Code.",
                    session_id=session_id,
                    translated_query=translated_query,
                    laws=[]
                )
            return ChatResponse(
                message_id=message_id,
                response="Query not related to Labor Law.",
                session_id=session_id,
                translated_query=translated_query,
                laws=[]
            )

        # ── BGE-M3 dense scores ───────────────────────────────────────────────
        encoder    = search_engine.get_bge_model()
        bge_scores = util.cos_sim(
            encoder.encode(translated_query, convert_to_tensor=True),
            search_engine.bge_embeddings
        )[0].cpu().numpy()

        limit = (await db.settings.find_one({"key": "chat_limit"}) or {}).get("value", 5)

        # ── BM25 + title boost + RRF fusion + gating ─────────────────────────
        scored = score_and_gate(search_engine, corr_tokens, dir_idx, bge_scores)
        f_scores = scored["final_scores"]

        if not scored["domain_gate_passed"]:
            return ChatResponse(
                message_id=message_id,
                response="Query not related to Labor Law.",
                session_id=session_id,
                translated_query=translated_query,
                laws=[]
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
            d_law['accuracy'] = "100%"
            matched.append(d_law)

        # ── Ranked hybrid retrieval ────────────────────────────────────────────
        for idx in scored["ranked_indices"]:
            if len(matched) >= limit:
                break

            ld = search_engine.laws[idx].copy()
            ld['best_match_chunk'] = max(
                ld.get('chunks', []),
                key=lambda c: len(q_set.intersection(set(c.lower().split()))) / max(len(c.split()), 1),
                default=""
            ) or ld.get('simplified_text', '')

            # Min-Max normalised against theoretical max RRF
            min_max_scaled = (float(f_scores[idx]) / THEORETICAL_MAX_RRF) * 100
            raw_percentage = min(int(min_max_scaled), 99)
            ld['accuracy'] = f"{raw_percentage}%"

            matched.append(ld)

        resp = (
            f"I found {len(matched)} relevant article(s) regarding your query:"
            if matched else "No specific laws found."
        )

        # ── Save to chat_history with tracked translated query and feedback state ──
        await db.chat_history.insert_one({
            "id": message_id,
            "session_id": session_id,
            "user_id": user_id,
            "user_message": message,
            "translated_query": translated_query,
            "assistant_response": resp,
            "laws": matched,
            "feedback": None,  # Will be updated via the feedback endpoint
            "created_at": datetime.now(timezone.utc).isoformat()
        })

        return ChatResponse(
            message_id=message_id,
            response=resp,
            session_id=session_id,
            translated_query=translated_query,
            laws=matched
        )

    except Exception as e:
        logger.error(f"CHAT ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# FEEDBACK ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/feedback")
async def submit_feedback(payload: FeedbackRequest):
    """
    Submits a like/dislike. If the user clicks the same vote again, it acts as a toggle 
    and removes it. If they switch votes, it updates to the new vote without stacking.
    """
    chat_item = await db.chat_history.find_one({"id": payload.message_id})
    if not chat_item:
        raise HTTPException(status_code=404, detail="Message not found.")

    # Prevent stacking by toggling the vote off if it matches the current feedback state
    new_feedback = None if chat_item.get("feedback") == payload.feedback else payload.feedback

    await db.chat_history.update_one(
        {"id": payload.message_id},
        {"$set": {
            "feedback": new_feedback,
            "feedback_updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )

    return {
        "message_id": payload.message_id,
        "feedback": new_feedback,
        "status": "updated"
    }


@router.get("/feedback/latest", response_model=LatestFeedbackResponse)
async def get_latest_feedback(user_id: Optional[str] = None):
    """
    Retrieves the 3 most recently liked and 3 most recently disliked queries.
    """
    filter_base = {"user_id": user_id} if user_id else {}

    # Query for the latest 3 'liked' messages
    liked_cursor = db.chat_history.find(
        {**filter_base, "feedback": "like"},
        {"_id": 0, "id": 1, "user_message": 1, "translated_query": 1, "feedback": 1, "created_at": 1}
    ).sort("created_at", -1).limit(3)

    # Query for the latest 3 'disliked' messages
    disliked_cursor = db.chat_history.find(
        {**filter_base, "feedback": "dislike"},
        {"_id": 0, "id": 1, "user_message": 1, "translated_query": 1, "feedback": 1, "created_at": 1}
    ).sort("created_at", -1).limit(3)

    liked_records = await liked_cursor.to_list(3)
    disliked_records = await disliked_cursor.to_list(3)

    liked_items = [
        FeedbackHistoryItem(
            message_id=doc["id"],
            user_message=doc.get("user_message", ""),
            translated_query=doc.get("translated_query", ""),
            feedback=doc.get("feedback", "like"),
            created_at=doc.get("created_at", "")
        )
        for doc in liked_records
    ]

    disliked_items = [
        FeedbackHistoryItem(
            message_id=doc["id"],
            user_message=doc.get("user_message", ""),
            translated_query=doc.get("translated_query", ""),
            feedback=doc.get("feedback", "dislike"),
            created_at=doc.get("created_at", "")
        )
        for doc in disliked_records
    ]

    return LatestFeedbackResponse(liked=liked_items, disliked=disliked_items)


# ─────────────────────────────────────────────────────────────────────────────
# PER-ARTICLE FEEDBACK (Supporting LegalChat_2.js)
# ─────────────────────────────────────────────────────────────────────────────

class ArticleFeedbackRequest(BaseModel):
    message_id: str
    law_id: str
    feedback: Literal["like", "dislike"]


def _law_key(law: dict) -> str:
    """Stable identifier for an article inside a stored answer (must match the frontend)."""
    return str(law.get("id") or law.get("article") or "")


@router.post("/feedback/article")
async def submit_article_feedback(payload: ArticleFeedbackRequest):
    chat_item = await db.chat_history.find_one({"id": payload.message_id}, {"_id": 0})
    if not chat_item:
        raise HTTPException(status_code=404, detail="Message not found.")

    # The article must actually be part of that answer
    law = next((l for l in chat_item.get("laws", []) if _law_key(l) == payload.law_id), None)
    if not law:
        raise HTTPException(status_code=404, detail="Article is not part of this answer.")

    key = {"message_id": payload.message_id, "law_id": payload.law_id}
    existing = await db.article_feedback.find_one(key)

    if existing and existing.get("feedback") == payload.feedback:
        # Same vote again -> back to "nothing"
        await db.article_feedback.delete_one(key)
        new_feedback = None
    else:
        await db.article_feedback.update_one(
            key,
            {"$set": {
                "article": law.get("article"),
                "title": law.get("title"),
                # identity comes from the stored chat, never from the client
                "user_id": chat_item.get("user_id"),
                "session_id": chat_item.get("session_id"),
                "query": chat_item.get("user_message", ""),
                "translated_query": chat_item.get("translated_query", ""),
                "feedback": payload.feedback,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }},
            upsert=True,
        )
        new_feedback = payload.feedback

    return {
        "message_id": payload.message_id,
        "law_id": payload.law_id,
        "feedback": new_feedback,
    }


@router.get("/feedback/article")
async def get_article_feedback(
    law_id: str,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
):
    """Latest 3 liked + latest 3 disliked queries for ONE article (the requester's own)."""
    if user_id:
        scope = {"user_id": user_id}
    elif session_id:
        scope = {"session_id": session_id}
    else:
        return {"liked": [], "disliked": []}

    projection = {"_id": 0, "message_id": 1, "query": 1, "translated_query": 1,
                  "feedback": 1, "updated_at": 1}

    async def latest(kind: str):
        cursor = db.article_feedback.find(
            {**scope, "law_id": law_id, "feedback": kind}, projection
        ).sort("updated_at", -1).limit(3)
        return await cursor.to_list(3)

    return {"liked": await latest("like"), "disliked": await latest("dislike")}


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