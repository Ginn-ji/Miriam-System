from __future__ import annotations
from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Form
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

# ==================== MODELS ====================

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    password: str
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LoginRequest(BaseModel):
    username: str
    password: str

class TranslationRequest(BaseModel):
    text: str
    source_language: str = "auto"
    target_language: str

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    detected_language: Optional[str] = None

class DocumentUpload(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    content: str
    document_type: str
    language: str
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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

# Prevent Pydantic TypeAdapter Errors
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
    return {"message": "LACBot Legal Assistance API"}

@api_router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        if file.filename.endswith('.pdf'):
            text_content = await extract_text_from_pdf(content)
            doc_type = "pdf"
        else:
            text_content = content.decode('utf-8')
            doc_type = "text"
            
        language = detect_language_simple(text_content)
        doc = {
            "id": str(uuid.uuid4()), "filename": file.filename, "content": text_content,
            "document_type": doc_type, "language": language, "tags": [],
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.documents.insert_one(doc)
        return {"id": doc["id"], "filename": doc["filename"], "language": language, "message": "Document uploaded successfully"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/documents")
async def get_documents(limit: int = 20):
    try:
        documents = await db.documents.find({}, {"_id": 0, "content": 0}).sort("created_at", -1).limit(limit).to_list(limit)
        return {"documents": documents}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/documents/{document_id}")
async def get_document(document_id: str):
    try:
        document = await db.documents.find_one({"id": document_id}, {"_id": 0})
        if not document: raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# ==================== LEGAL KNOWLEDGE CRUD ====================

@api_router.get("/legal-knowledge")
async def get_all_laws(
    q: Optional[str] = None,
    category: Optional[str] = None,
    language: Optional[str] = None
):
    try:
        db_query = {}
        
        if category and category.lower() != 'all':
            # This regex allows "Labor Law" to match "Labor Law - Book 1", "Labor Law - Book 2", etc.
            db_query['category'] = {"$regex": category, "$options": "i"}
            
        if language and language.lower() != 'all':
            db_query['language'] = language
            
        if q:
            search_regex = {"$regex": q, "$options": "i"}
            db_query["$or"] = [
                {"title": search_regex},
                {"content": search_regex},
                {"tags": search_regex},
                {"chunks": search_regex}
            ]

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
        logger.error(f"Error fetching legal knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")


@api_router.post("/legal-knowledge")
async def add_legal_knowledge(law: LegalKnowledge):
    try:
        law_dict = law.model_dump()
        law_dict['created_at'] = datetime.now(timezone.utc).isoformat()
        
        if isinstance(law_dict.get('chunks'), str): law_dict['chunks'] = [c.strip() for c in law_dict['chunks'].split('\n') if c.strip()]
        if isinstance(law_dict.get('tags'), str): law_dict['tags'] = [t.strip() for t in law_dict['tags'].split(',') if t.strip()]

        law_dict.pop('_id', None)
        await db.legal_knowledge.insert_one(law_dict)
        return {"message": "Law added successfully", "id": law_dict['id']}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/legal-knowledge/upload")
async def upload_legal_knowledge(file: UploadFile = File(...), title: str = Form(...), category: str = Form(...), tags: str = Form(...), language: str = Form(...)):
    try:
        content = await file.read()
        if file.filename.endswith('.pdf'): text_content = await extract_text_from_pdf(content)
        elif file.filename.endswith('.txt'): text_content = content.decode('utf-8')
        else: raise HTTPException(status_code=400, detail="Only PDF and text files are supported")

        if not text_content.strip(): raise HTTPException(status_code=400, detail="Could not extract text from file")

        law = {
            "id": str(uuid.uuid4()), "title": title, "category": category, "content": text_content,
            "simplified_text": "Extracted from uploaded document.",
            "tags": [t.strip() for t in tags.split(',') if t.strip()], "language": language,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.legal_knowledge.insert_one(law)
        return {"message": "Legal knowledge uploaded successfully", "id": law["id"]}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/legal-knowledge/{law_id}")
async def delete_legal_knowledge(law_id: str):
    try:
        result = await db.legal_knowledge.delete_one({"id": law_id})
        if result.deleted_count == 0: raise HTTPException(status_code=404, detail="Law not found")
        return {"message": "Law deleted successfully"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# ==================== HYBRID CHATBOT RETRIEVAL ====================

@api_router.post("/chat", response_model=ChatResponse)
async def legal_chat(message: str = Form(...), session_id: Optional[str] = Form(None), user_id: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    try:
        session_id = session_id or str(uuid.uuid4())
        message_text = message
        if file:
            content = await file.read()
            file_text = await extract_text_from_pdf(content) if file.filename.endswith('.pdf') else content.decode('utf-8')
            message_text = f"{message} {file_text}"
            
        all_laws = await db.legal_knowledge.find({}, {"_id": 0}).to_list(1000)
        if not all_laws: return ChatResponse(response="No laws found in database.", session_id=session_id, laws=[])
        
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
        
        vocabulary = set([word for doc in tokenized_corpus for word in doc if word not in stopwords and len(word) > 2])
        
        # ==========================================
        # 1. PRE-RETRIEVAL TRANSLATION (The Missing Key)
        # ==========================================
        search_text = message_text
        try:
            detected_lang = detect_language_simple(message_text)
            if detected_lang in ['tl', 'unknown']:
                english_translation = GoogleTranslator(source='tl', target='en').translate(message_text)
                # Combine Tagalog and English so the math engine searches BOTH
                search_text = f"{message_text} {english_translation}"
                logger.info(f"Expanded Search: {search_text}")
        except Exception as e:
            logger.warning(f"Pre-translation failed: {e}")

        # Now we tokenize the COMBINED Taglish + English text
        raw_tokens = [w.lower() for w in search_text.split() if len(w) > 2 and w.lower() not in stopwords]
        
        corrected_tokens = []
        for t in raw_tokens:
            if t in vocabulary:
                corrected_tokens.append(t)
            elif vocabulary:
                closest = min(vocabulary, key=lambda v: Levenshtein.distance(t, v))
                dist = Levenshtein.distance(t, closest)
                if dist == 1 or (dist == 2 and len(t) >= 8):
                    corrected_tokens.append(closest)
                    
        if not corrected_tokens:
             return ChatResponse(
                 response="This query does not appear to be related to Philippine Labor Law. Please ask a specific workplace, employment, or labor dispute question.", 
                 session_id=session_id, 
                 laws=[]
             )
        
        legal_synonyms = {
            "sweldo": ["wage", "salary", "pay", "compensation"],
            "sahod": ["wage", "salary", "pay", "compensation"],
            "talsik": ["termination", "dismissal", "severance", "fired"],
            "tanggal": ["termination", "dismissal", "severance", "fired"],
            "buntis": ["maternity", "leave", "pregnancy"],
            "sakit": ["sick", "disease", "health", "hazard", "medical"],
            "pahinga": ["rest", "meal", "break", "holiday"],
            "katapusan": ["month", "payment", "period"],
            "sobra": ["overtime", "excess", "beyond"],
            "gabi": ["night", "shift", "differential"]
        }
        
        expanded_tokens = []
        for token in corrected_tokens:
            expanded_tokens.append(token)
            if token in legal_synonyms:
                expanded_tokens.extend(legal_synonyms[token])
                
        query_text_for_math = " ".join(expanded_tokens)
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([query_text_for_math]) 
        cosine_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
        
        bm25 = BM25Okapi(tokenized_corpus)
        bm25_scores = bm25.get_scores(expanded_tokens) 
        
        highest_bm25 = max(bm25_scores) if len(bm25_scores) > 0 else 0
        baseline_denominator = highest_bm25 if highest_bm25 > 3.0 else 3.0
        
        final_scores = (cosine_scores * 0.5) + ((np.array(bm25_scores) / baseline_denominator) * 0.5)
        
        try:
            limit_setting = await db.settings.find_one({"key": "chat_limit"})
            chat_limit = int(limit_setting.get("value", 5)) if limit_setting else 5
        except Exception as e:
            logger.warning(f"Could not fetch limit setting, using default 5. Error: {e}")
            chat_limit = 5
        
 # 6. STRICTER THRESHOLD (Raised to 0.30)
        top_indices = np.argsort(final_scores)[::-1][:chat_limit]
        matched_laws = [all_laws[i] for i in top_indices if final_scores[i] > 0.30]
        
        for law in matched_laws:
            qs = set(expanded_tokens)
            law['best_match_chunk'] = max(law.get('chunks', []), key=lambda c: len(qs.intersection(set(c.lower().split()))), default="")
            
        if not matched_laws:
            base_response = "I could not find a specific Philippine Labor Law matching your query. Ensure your question is related to employment, wages, or workplace policies."
        else:
            base_response = f"I found {len(matched_laws)} relevant articles regarding your query:"

        # ==========================================
        # 7. POST-RETRIEVAL TRANSLATION (Output Localization)
        # ==========================================
        final_response = base_response
        
        try:
            # Check if the user's original raw message was in Tagalog
            detected_lang = detect_language_simple(message)
            if detected_lang in ['tl', 'unknown']:
                
                # 1. Translate the bot's greeting back to Tagalog
                final_response = GoogleTranslator(source='en', target='tl').translate(base_response)
                
                # 2. Translate the "Relevant Section" chunk so the user understands the law!
                for law in matched_laws:
                    if law['best_match_chunk']:
                        translated_chunk = GoogleTranslator(source='en', target='tl').translate(law['best_match_chunk'])
                        # Overwrite it so the React frontend displays the Tagalog version automatically
                        law['best_match_chunk'] = translated_chunk
                        
        except Exception as e:
            logger.warning(f"Output translation failed: {e}")
            
        # Save to database and return to frontend using the final_response
        await db.chat_history.insert_one({
            "id": str(uuid.uuid4()), 
            "session_id": session_id, 
            "user_id": user_id, 
            "user_message": message, 
            "assistant_response": final_response, 
            "laws": matched_laws, 
            "created_at": datetime.now(timezone.utc).isoformat()
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
    docs_count = await db.documents.count_documents({})
    trans_count = await db.translations.count_documents({})
    return {"documents": docs_count, "translations": trans_count, "chat_sessions": sessions, "legal_articles": laws}

@api_router.post("/login")
async def login(request: LoginRequest):
    user = await db.users.find_one({"username": request.username, "password": request.password}, {"_id": 0})
    if not user: raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

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
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup_event():
    count = await db.users.count_documents({})
    if count == 0:
        await db.users.insert_one({"id": str(uuid.uuid4()), "username": "admin", "password": "adminpassword", "role": "admin", "created_at": datetime.now(timezone.utc).isoformat()})
    logger.info("SHIELD/LACBot API Started")

@app.on_event("shutdown")
async def shutdown_db_client(): client.close()