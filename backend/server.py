from __future__ import annotations
from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union, Any
import uuid
from datetime import datetime, timezone
import PyPDF2
import io
import Levenshtein
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator
import bcrypt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DetectorFactory.seed = 0

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

# ==================== GLOBAL IN-MEMORY SEARCH ENGINE ====================
# This stores the trained models in RAM so the chatbot doesn't have to rebuild them every time
class SearchEngine:
    laws = []
    corpus = []
    tokenized_corpus = []
    vocabulary = set()
    vectorizer = None
    tfidf_matrix = None
    bm25 = None
    highest_bm25 = 0.0

class BulkDeleteRequest(BaseModel):
    ids: List[str]

search_engine = SearchEngine()

async def train_search_models():
    """Fetches all laws from the database and pre-trains the TF-IDF and BM25 models in memory."""
    logger.info("Training LACBot Search Models in memory...")
    all_laws = await db.legal_knowledge.find({}, {"_id": 0}).to_list(None)
    
    if not all_laws:
        logger.warning("No laws found in database to train.")
        search_engine.laws = []
        return

    search_engine.laws = all_laws
    corpus = []
    tokenized_corpus = []
    
    for law in all_laws:
        body = " ".join(law.get('chunks', [])) if law.get('chunks') else law.get('content', '')
        doc_text = f"{law.get('article', '')} {law.get('title', '')} {body}".lower()
        corpus.append(doc_text)
        tokenized_corpus.append(doc_text.split())
        
    stopwords = {
        "ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila", "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung", "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", 
        "a", "an", "the", "is", "are", "was", "were", "what", "who", "how", "when", "where", "why", "can", "could", "would", "should", "do", "does", "did", "i", "me", "my", "we", "you", "your", "it", "about", "and", "or", "of", "in", "on", "to", "for", "with", "law", "article", "code",
        "he", "she", "him", "his", "her", "they", "them", "their", "this", "that", "these", "those", "be", "been", "being", "has", "have", "had", "by", "from", "as", "not", "no", "any", "all", "such", "shall", "may", "will", "upon", "under", "which", "whom", "other", "out", "into", "same", "some"
    }
    
    search_engine.vocabulary = set([word for doc in tokenized_corpus for word in doc if word not in stopwords and len(word) > 2])
    search_engine.corpus = corpus
    search_engine.tokenized_corpus = tokenized_corpus
    
    # Train TF-IDF
    # stop_words='english' strips filler words from the vocabulary itself (not just the query),
    # so common words shared by every document stop inflating cosine similarity for irrelevant queries.
    # min_df=2 drops one-off tokens/typos that would otherwise create accidental exact-match spikes.
    search_engine.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', min_df=2)
    search_engine.tfidf_matrix = search_engine.vectorizer.fit_transform(corpus)
    
    # Train BM25
    search_engine.bm25 = BM25Okapi(tokenized_corpus)
    
    logger.info("Search Models successfully trained and loaded into memory!")

# ==================== MODELS ====================

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    password: str
    role: str = "user"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class LoginRequest(BaseModel):
    username: str
    password: str

class ChatResponse(BaseModel):
    response: str
    session_id: str
    laws: Optional[List[dict]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LegalKnowledge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    article: Optional[str] = None
    title: str
    category: str = "Labor Law"
    simplified_text: Optional[str] = None 
    chunks: Optional[Union[List[str], str]] = None
    content: Optional[str] = None 
    tags: Union[List[str], str]
    language: str = "en"
    created_at: Optional[str] = None

class ChatLimitRequest(BaseModel):
    new_limit: int

LegalKnowledge.model_rebuild()

# ==================== HELPER FUNCTIONS ====================

async def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting PDF: {str(e)}")

def detect_language_simple(text: str) -> str:
    try:
        return detect(text[:1000])
    except:
        return "unknown"

# ==================== SYSTEM SETTINGS ====================

@api_router.get("/settings/chat-limit")
async def get_chat_limit():
    try:
        setting = await db.settings.find_one({"key": "chat_limit"}, {"_id": 0})
        return {"limit": setting["value"] if setting else 5}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/settings/chat-limit")
async def update_chat_limit(request: ChatLimitRequest):
    try:
        if request.new_limit < 1 or request.new_limit > 10:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 10")
            
        await db.settings.update_one(
            {"key": "chat_limit"},
            {"$set": {"value": request.new_limit}},
            upsert=True
        )
        return {"message": "Chat limit updated successfully", "limit": request.new_limit}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== TRANSLATION & GENERAL DOC ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "LACBot Legal Awareness Chat Bot"}

# ==================== LEGAL KNOWLEDGE CRUD ====================

@api_router.get("/legal-knowledge")
async def get_all_laws(q: Optional[str] = None, category: Optional[str] = None, language: Optional[str] = None):
    try:
        db_query = {}
        if category and category.lower() != 'all':
            db_query['category'] = {"$regex": category, "$options": "i"}
        if language and language.lower() != 'all':
            db_query['language'] = language
        if q:
            search_regex = {"$regex": q, "$options": "i"}
            db_query["$or"] = [{"title": search_regex}, {"content": search_regex}, {"tags": search_regex}, {"chunks": search_regex}]

        laws = await db.legal_knowledge.find(db_query, {"_id": 0}).to_list(1000)
        
        for law in laws:
            article = law.get('article') or ""
            title = law.get('title') or "Untitled"
            if article: law['title'] = f"{article} - {title}"
            else: law['title'] = title
            
            if law.get('chunks') and isinstance(law.get('chunks'), list):
                law['content'] = "\n\n".join(law.get('chunks'))
            elif not law.get('content'):
                law['content'] = law.get('simplified_text') or "No content available."
            
            if not isinstance(law.get('tags'), list): law['tags'] = []
            
        return {"laws": laws}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@api_router.post("/legal-knowledge")
async def add_legal_knowledge(law: LegalKnowledge, background_tasks: BackgroundTasks):
    try:
        law_dict = law.model_dump()
        law_dict['created_at'] = datetime.now(timezone.utc).isoformat()
        if isinstance(law_dict.get('chunks'), str): law_dict['chunks'] = [c.strip() for c in law_dict['chunks'].split('\n') if c.strip()]
        if isinstance(law_dict.get('tags'), str): law_dict['tags'] = [t.strip() for t in law_dict['tags'].split(',') if t.strip()]

        law_dict.pop('_id', None)
        await db.legal_knowledge.insert_one(law_dict)
        
        # Retrain the memory models in the background automatically
        background_tasks.add_task(train_search_models)
        
        return {"message": "Law added successfully", "id": law_dict['id']}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/legal-knowledge/upload")
async def upload_legal_knowledge(background_tasks: BackgroundTasks, file: UploadFile = File(...), title: str = Form(...), category: str = Form(...), tags: str = Form(...), language: str = Form(...)):
    try:
        content = await file.read()
        if file.filename.endswith('.pdf'): text_content = await extract_text_from_pdf(content)
        elif file.filename.endswith('.txt'): text_content = content.decode('utf-8')
        else: raise HTTPException(status_code=400, detail="Only PDF and text files are supported")

        law = {
            "id": str(uuid.uuid4()), "title": title, "category": category, "content": text_content,
            "simplified_text": "Extracted from uploaded document.",
            "tags": [t.strip() for t in tags.split(',') if t.strip()], "language": language,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.legal_knowledge.insert_one(law)
        
        # Retrain the memory models in the background automatically
        background_tasks.add_task(train_search_models)
        
        return {"message": "Legal knowledge uploaded successfully", "id": law["id"]}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/legal-knowledge/bulk-delete")
async def bulk_delete_laws(request: BulkDeleteRequest, background_tasks: BackgroundTasks):
    try:
        result = await db.legal_knowledge.delete_many({"id": {"$in": request.ids}})
        # Re-train memory models in the background
        background_tasks.add_task(train_search_models)
        return {"message": f"Successfully deleted {result.deleted_count} laws"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/legal-knowledge/delete-all")
async def delete_all_laws(background_tasks: BackgroundTasks):
    try:
        result = await db.legal_knowledge.delete_many({})
        background_tasks.add_task(train_search_models)
        return {"message": f"All legal articles have been deleted successfully ({result.deleted_count} removed)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# NOTE: this wildcard route MUST come after the two static routes above
# ("/legal-knowledge/bulk-delete" and "/legal-knowledge/delete-all").
# FastAPI matches routes in registration order, and {law_id} matches any
# string, so if this were declared first it would swallow requests meant
# for the routes above (e.g. DELETE .../delete-all would run with
# law_id="delete-all" instead of hitting delete_all_laws()).
@api_router.delete("/legal-knowledge/{law_id}")
async def delete_legal_knowledge(law_id: str, background_tasks: BackgroundTasks):
    try:
        result = await db.legal_knowledge.delete_one({"id": law_id})
        if result.deleted_count == 0: raise HTTPException(status_code=404, detail="Law not found")
        
        # Retrain the memory models in the background automatically
        background_tasks.add_task(train_search_models)
        
        return {"message": "Law deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== HYBRID CHATBOT RETRIEVAL (MEMORY-BASED) ====================

@api_router.post("/chat", response_model=ChatResponse)
async def legal_chat(message: str = Form(...), session_id: Optional[str] = Form(None), user_id: Optional[str] = Form(None)):
    try:
        session_id = session_id or str(uuid.uuid4())
        message_text = message
            
        # FAST CHECK: Ensure models are loaded
        if not search_engine.laws or search_engine.vectorizer is None:
            return ChatResponse(response="System is initializing or no laws are available. Please try again in a moment.", session_id=session_id, laws=[])
        
        search_text = message_text
        try:
            detected_lang = detect_language_simple(message_text)
            if detected_lang in ['tl', 'unknown']:
                english_translation = GoogleTranslator(source='tl', target='en').translate(message_text)
                search_text = f"{message_text} {english_translation}"
        except Exception as e:
            logger.warning(f"Pre-translation failed: {e}")

        stopwords = {
            "ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila", "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung", "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", 
            "a", "an", "the", "is", "are", "was", "were", "what", "who", "how", "when", "where", "why", "can", "could", "would", "should", "do", "does", "did", "i", "me", "my", "we", "you", "your", "it", "about", "and", "or", "of", "in", "on", "to", "for", "with", "law", "article", "code"
        }
        
        raw_tokens = [w.lower() for w in search_text.split() if len(w) > 2 and w.lower() not in stopwords]

        # Pass 1: exact vocabulary hits only. This is the real relevance signal.
        exact_tokens = [t for t in raw_tokens if t in search_engine.vocabulary]

        # Gate on EXACT hits, before any fuzzy correction is allowed to run.
        # Fuzzy correction should only ever fix a typo *within* an already-relevant
        # query, never manufacture relevance for a query with zero real signal.
        if not exact_tokens:
            return ChatResponse(
                response="This query does not appear to be related to Philippine Labor Law. Please ask a specific workplace, employment, or labor dispute question.",
                session_id=session_id, laws=[]
            )

        corrected_tokens = list(exact_tokens)
        unmatched = [t for t in raw_tokens if t not in search_engine.vocabulary]
        for t in unmatched:
            if len(t) >= 6 and search_engine.vocabulary:
                closest = min(search_engine.vocabulary, key=lambda v: Levenshtein.distance(t, v))
                dist = Levenshtein.distance(t, closest)
                # distance relative to word length, not a fixed constant, so short
                # words need a near-exact match and only long words tolerate 2 edits
                if dist == 1 or (dist == 2 and len(t) >= 9):
                    corrected_tokens.append(closest)
        
        legal_synonyms = {
            "sweldo": ["wage", "salary", "pay", "compensation"], "sahod": ["wage", "salary", "pay", "compensation"],
            "talsik": ["termination", "dismissal", "severance", "fired"], "tanggal": ["termination", "dismissal", "severance", "fired"],
            "buntis": ["maternity", "leave", "pregnancy"], "sakit": ["sick", "disease", "health", "hazard", "medical"],
            "pahinga": ["rest", "meal", "break", "holiday"], "katapusan": ["month", "payment", "period"],
            "sobra": ["overtime", "excess", "beyond"], "gabi": ["night", "shift", "differential"]
        }
        
        expanded_tokens = []
        for token in corrected_tokens:
            expanded_tokens.append(token)
            if token in legal_synonyms:
                expanded_tokens.extend(legal_synonyms[token])
                
        query_text_for_math = " ".join(expanded_tokens)
        
        # EXPLOIT CACHED MODELS (Instant Speed)
        query_vec = search_engine.vectorizer.transform([query_text_for_math]) 
        cosine_scores = cosine_similarity(query_vec, search_engine.tfidf_matrix).flatten()
        bm25_scores = search_engine.bm25.get_scores(expanded_tokens) 
        
        highest_bm25 = max(bm25_scores) if len(bm25_scores) > 0 else 0
        baseline_denominator = highest_bm25 if highest_bm25 > 3.0 else 3.0
        
        final_scores = (cosine_scores * 0.5) + ((np.array(bm25_scores) / baseline_denominator) * 0.5)
        
        try:
            limit_setting = await db.settings.find_one({"key": "chat_limit"})
            chat_limit = int(limit_setting.get("value", 5)) if limit_setting else 5
        except:
            chat_limit = 5
        
        top_indices = np.argsort(final_scores)[::-1][:chat_limit]
        matched_laws = []
        
        # INJECTING THE SCALED ACCURACY SCORE
        exact_token_set = set(exact_tokens)
        for i in top_indices:
            if final_scores[i] > 0.45:
                law_data = search_engine.laws[i].copy()
                doc_words = set(search_engine.corpus[i].split())
                if not (exact_token_set & doc_words):
                    continue
                    
                scaled_score = final_scores[i] * 1.5 
                raw_percentage = int(scaled_score * 100)
                
                # Cap the maximum visual score at 98% (never claim 100% perfection)
                law_data['accuracy'] = f"{min(raw_percentage, 98)}%"
                # -------------------------
                
                # Find the specific chunk that matched
                qs = set(expanded_tokens)
                law_data['best_match_chunk'] = max(law_data.get('chunks', []), key=lambda c: len(qs.intersection(set(c.lower().split()))), default="")
                
                matched_laws.append(law_data)
            
        if not matched_laws:
            final_response = "I could not find any specific Philippine Labor Law matching your query. Please ensure your question is related to employment, wages, or workplace policies."
        else:
            base_response = f"I found {len(matched_laws)} relevant articles regarding your query:"
            final_response = base_response
            
            try:
                detected_lang = detect_language_simple(message)
                if detected_lang in ['tl', 'unknown']:
                    final_response = GoogleTranslator(source='en', target='tl').translate(base_response)
                    for law in matched_laws:
                        if law['best_match_chunk']:
                            law['best_match_chunk'] = GoogleTranslator(source='en', target='tl').translate(law['best_match_chunk'])
            except Exception as e:
                logger.warning(f"Output translation failed: {e}")
            
        await db.chat_history.insert_one({
            "id": str(uuid.uuid4()), "session_id": session_id, "user_id": user_id, 
            "user_message": message, "assistant_response": final_response, 
            "laws": matched_laws, "created_at": datetime.now(timezone.utc).isoformat()
        })
        
        return ChatResponse(response=final_response, session_id=session_id, laws=matched_laws)
        
    except Exception as e: 
        logger.error(f"CRITICAL CHAT ERROR: {str(e)}") 
        raise HTTPException(status_code=500, detail=str(e))

# ==================== AUTH & STATS ====================

@api_router.get("/stats")
async def get_stats():
    sessions = len(await db.chat_history.distinct("session_id"))
    laws = await db.legal_knowledge.count_documents({})
    return {"chat_sessions": sessions, "legal_articles": laws}

@api_router.post("/login")
async def login(request: LoginRequest):
    user = await db.users.find_one({"username": request.username, "password": request.password}, {"_id": 0})
    if not user: raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@api_router.post("/users/register")
async def register_user(user: User):
    try:
        existing_user = await db.users.find_one({"username": user.username})
        if existing_user: raise HTTPException(status_code=400, detail="Username already taken")
        new_user_dict = user.model_dump()
        await db.users.insert_one(new_user_dict)
        return {"message": "User registered successfully", "id": new_user_dict["id"], "username": new_user_dict["username"], "role": new_user_dict["role"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/chat/sessions")
async def get_user_sessions(user_id: str):
    pipeline = [{"$match": {"user_id": user_id}}, {"$sort": {"created_at": -1}}, {"$group": {"_id": "$session_id", "last_message": {"$first": "$user_message"}, "timestamp": {"$first": "$created_at"}}}, {"$sort": {"timestamp": -1}}]
    sessions = await db.chat_history.aggregate(pipeline).to_list(100)
    return {"sessions": sessions}

@api_router.get("/chat/sessions/{session_id}")
async def get_chat_history(session_id: str):
    messages = await db.chat_history.find({"session_id": session_id}, {"_id": 0}).sort("created_at", 1).to_list(100)
    return {"messages": messages}

app.include_router(api_router)

origins = ["http://localhost:3000", "http://127.0.0.1:3000", "https://miriam-system.vercel.app"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup_event():
    count = await db.users.count_documents({})
    if count == 0:
        await db.users.insert_one({"id": str(uuid.uuid4()), "username": "admin", "password": "adminpassword", "role": "admin", "created_at": datetime.now(timezone.utc).isoformat()})
    
    # TRIGGERS THE IN-MEMORY TRAINING WHEN SERVER STARTS
    await train_search_models()
    
    logger.info("SHIELD API Started and Models Loaded")

@app.on_event("shutdown")
async def shutdown_db_client(): client.close()