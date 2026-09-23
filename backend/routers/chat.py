from fastapi import APIRouter, HTTPException, Form
from typing import Optional
import uuid
from datetime import datetime, timezone
import re
import numpy as np
from sentence_transformers import util
import logging

from database import db
from schemas import ChatResponse
from core.engine import search_engine
from synonyms import LEGAL_SYNONYMS
from core.nlp_utils import clean_conversational_noise, is_tagalog_or_taglish, strip_filipino_affixes, detect_language_simple
import Levenshtein
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
async def legal_chat(message: str = Form(...), session_id: Optional[str] = Form(None), user_id: Optional[str] = Form(None)):
    try:
        session_id = str(session_id) if (session_id and not hasattr(session_id, 'default')) else str(uuid.uuid4())
        user_id = str(user_id) if (user_id and not hasattr(user_id, 'default')) else None
        
        if len(message.split()) > 1000: return ChatResponse(response="Query too long.", session_id=session_id, laws=[])
        clean_msg = clean_conversational_noise(message)
        msg_text = clean_msg.lower() if clean_msg else message.lower()
            
        if not search_engine.laws or search_engine.bge_embeddings is None:
            return ChatResponse(response="System initializing.", session_id=session_id, laws=[])

        art_match = re.search(r'\barticle\s+(\d+)\b|\bart\.?\s*(\d+)\b', message.lower())
        dir_idx = next((i for i, num in enumerate(search_engine.article_numbers) if re.search(r'\d+', num) and re.search(r'\d+', num).group() == (art_match.group(1) or art_match.group(2))), None) if art_match else None

        exp_kw = []
        raw_w = re.sub(r'[^\w\s]', ' ', msg_text).split()
        cand_w = set(raw_w + [strip_filipino_affixes(w) for w in raw_w])
        for t, eng in LEGAL_SYNONYMS.items():
            if (" " in t.lower() and t.lower() in msg_text) or (" " not in t.lower() and t.lower() in cand_w): exp_kw.extend(eng)

        search_text = msg_text
        if is_tagalog_or_taglish(search_text):
            cached = await db.translation_cache.find_one({"query": re.sub(r'[^\w\s]', ' ', msg_text)})
            if cached: search_text += f" {cached.get('translation', '')}"

        full_q = f"{search_text} {' '.join(exp_kw)}"
        clean_q = re.sub(r'[^\w\s]', '', full_q)
        stopwords = {"ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila"} # truncated for brevity
        
        raw_tokens = [w for w in clean_q.split() if (len(w) > 2 or w.isdigit()) and w not in stopwords]
        corr_tokens = [t for t in raw_tokens if t in search_engine.vocabulary]
        
        for t in [x for x in raw_tokens if x not in search_engine.vocabulary and len(x) > 5]:
            cands = [v for v in search_engine.vocabulary if v.startswith(t[0])]
            if cands:
                closest = min(cands, key=lambda v: Levenshtein.distance(t, v))
                if (len(t) <= 8 and Levenshtein.distance(t, closest) == 1) or (len(t) >= 9 and Levenshtein.distance(t, closest) <= 2):
                    corr_tokens.append(closest)

        if not corr_tokens and dir_idx is None:
            if any(t in msg_text for t in ["government employee", "kawani ng gobyerno", "civil service"]):
                return ChatResponse(response="Government employees are governed by CSC, not the Labor Code.", session_id=session_id, laws=[])
            return ChatResponse(response="Query not related to Labor Law.", session_id=session_id, laws=[])
        
        q_math = " ".join(corr_tokens)
        
        encoder = search_engine.get_bge_model()
        bge_scores = util.cos_sim(encoder.encode(q_math, convert_to_tensor=True), search_engine.bge_embeddings)[0].cpu().numpy()
        bm25_scores = np.array(search_engine.bm25.get_scores(corr_tokens))
        
        t_boost = np.zeros(len(search_engine.laws))
        q_set = set(corr_tokens)
        for i, t_text in enumerate(search_engine.title_corpus):
            m_words = q_set & set(t_text.split())
            if m_words: t_boost[i] = sum(search_engine.vocab_idf.get(w, 1.0) for w in m_words)

        def rrf(raw, k=60):
            r = np.empty_like(raw)
            r[np.argsort(-raw)] = np.arange(1, len(raw) + 1)
            return np.where(raw > 0, 1.0 / (k + r), 0.0)

        f_scores = rrf(bge_scores) + rrf(bm25_scores) + rrf(t_boost)
        
        if float(np.max(bge_scores)) < 0.45 and dir_idx is None:
            return ChatResponse(response="Query not related to Labor Law.", session_id=session_id, laws=[])

        limit = (await db.settings.find_one({"key": "chat_limit"}) or {}).get("value", 5)
        matched = []
        if dir_idx is not None:
            d_law = search_engine.laws[dir_idx].copy()
            d_law['best_match_chunk'] = max(d_law.get('chunks', []), key=lambda c: len(q_set.intersection(set(c.lower().split()))) / max(len(c.split()), 1), default="") or d_law.get('simplified_text', '')
            matched.append(d_law)

        for i in np.argsort(f_scores)[::-1]:
            if len(matched) >= limit: break
            if dir_idx is not None and i == dir_idx: continue
            if f_scores[i] > 0.01 and bge_scores[i] >= 0.35 and (q_set & set(search_engine.corpus[i].split())):
                ld = search_engine.laws[i].copy()
                ld['best_match_chunk'] = max(ld.get('chunks', []), key=lambda c: len(q_set.intersection(set(c.lower().split()))) / max(len(c.split()), 1), default="") or ld.get('simplified_text', '')
                matched.append(ld)

        resp = f"I found {len(matched)} relevant articles regarding your query:" if matched else "No specific laws found."
        
        await db.chat_history.insert_one({"id": str(uuid.uuid4()), "session_id": session_id, "user_id": user_id, "user_message": message, "assistant_response": resp, "laws": matched, "created_at": datetime.now(timezone.utc).isoformat()})
        return ChatResponse(response=resp, session_id=session_id, laws=matched)
    except Exception as e:
        logger.error(f"CHAT ERROR: {str(e)}") 
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}")
async def get_session_messages(session_id: str):
    messages = await db.chat_history.find(
        {"session_id": session_id},
        {"_id": 0}
    ).sort("created_at", 1).to_list(1000)
    if not messages:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"messages": messages}

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
    
@router.get("/sessions")
async def get_sessions(user_id: str):
    return {"sessions": await db.chat_history.aggregate([{"$match": {"user_id": user_id}}, {"$sort": {"created_at": -1}}, {"$group": {"_id": "$session_id", "last_message": {"$first": "$user_message"}, "timestamp": {"$first": "$created_at"}}}, {"$sort": {"timestamp": -1}}]).to_list(100)}