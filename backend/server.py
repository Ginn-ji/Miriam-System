from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import PyPDF2
import io
from langdetect import detect, DetectorFactory
import Levenshtein
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

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

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "user"
    current_user_role: Optional[str] = None

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
    simplified_text: str
    chunks: List[str]
    tags: List[str]
    language: str = "en"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ==================== HELPER FUNCTIONS ====================

async def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting PDF: {str(e)}")

async def initialize_admin_user():
    count = await db.users.count_documents({})
    if count == 0:
        default_admin = {
            "id": str(uuid.uuid4()), "username": "admin", "password": "adminpassword",
            "role": "admin", "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(default_admin)

async def initialize_legal_knowledge():
    count = await db.legal_knowledge.count_documents({})
    if count > 0: return
    
    mock_law = {
        "id": str(uuid.uuid4()),
        "article": "Art. 211",
        "title": "Declaration of Policy",
        "category": "Labor Law",
        "simplified_text": "The government protects your right to form unions, bargain fairly with employers, and settle disputes peacefully without unfair interference.",
        "chunks": [
            "To promote and emphasize the primacy of free collective bargaining and negotiations, including voluntary arbitration, mediation and conciliation, as modes of settling labor or industrial disputes;",
            "To promote free trade unionism as an instrument for the enhancement of democracy and the promotion of social justice and development;",
            "To foster the free and voluntary organization of a strong and united labor movement;",
            "To promote the enlightenment of workers concerning their rights and obligations as union members and as employees;",
            "To provide an adequate administrative machinery for the expeditious settlement of labor or industrial disputes;",
            "To ensure a stable but dynamic and just industrial peace; and",
            "To ensure the participation of workers in decision and policy-making processes affecting their rights, duties and welfare.",
            "To encourage a truly democratic method of regulating the relations between the employers and employees by means of agreements freely entered into through collective bargaining..."
        ],
        "tags": ["union", "rights", "collective bargaining", "policy", "disputes"],
        "language": "en",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.legal_knowledge.insert_one(mock_law)

# ==================== AUTH ROUTES ====================

@api_router.post("/login")
async def login(request: LoginRequest):
    user = await db.users.find_one({"username": request.username, "password": request.password}, {"_id": 0})
    if not user: raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@api_router.post("/users/register")
async def register_user(request: RegisterRequest):
    if request.role == "admin" and request.current_user_role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create admin accounts")
    existing = await db.users.find_one({"username": request.username})
    if existing: raise HTTPException(status_code=400, detail="Username already exists")
    new_user = {
        "id": str(uuid.uuid4()), "username": request.username, "password": request.password, 
        "role": request.role, "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(new_user)
    return {"message": "User registered successfully", "id": new_user["id"], "username": request.username, "role": request.role}

# ==================== CORE ROUTES ====================

@api_router.get("/")
async def root(): return {"message": "Miriam Legal Assistance API"}

@api_router.post("/chat", response_model=ChatResponse)
async def legal_chat(
    message: str = Form(...),
    session_id: Optional[str] = Form(None),
    context: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        session_id = session_id or str(uuid.uuid4())
        message_text = message

        if file:
            content = await file.read()
            file_text = await extract_text_from_pdf(content) if file.filename.endswith('.pdf') else content.decode('utf-8')
            message_text = f"{message} {file_text}"

        all_laws = await db.legal_knowledge.find({}, {"_id": 0}).to_list(1000)
        
        if not all_laws:
            response = "I could not find any labor laws in the database. Please contact the administrator."
            await db.chat_history.insert_one({"id": str(uuid.uuid4()), "session_id": session_id, "user_id": user_id, "user_message": message, "assistant_response": response, "laws": [], "created_at": datetime.now(timezone.utc).isoformat()})
            return ChatResponse(response=response, session_id=session_id, laws=[])

        corpus = []
        tokenized_corpus = []
        for law in all_laws:
            # Safely grab fields
            article = law.get('article', '')
            title = law.get('title', '')
            category = law.get('category', '') # ADDED CATEGORY
            body_text = " ".join(law.get('chunks', [])) if law.get('chunks') else law.get('content', '')
            tags = " ".join(law.get('tags', []))
            
            # Combine everything into one string, NOW INCLUDING CATEGORY
            doc_text = f"{article} {title} {category} {body_text} {tags}".lower()
            
            corpus.append(doc_text)
            tokenized_corpus.append(doc_text.split())

        vocabulary = set([word for doc in tokenized_corpus for word in doc])
        stopwords = {"ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila", "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung", "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "a", "an", "the", "is", "are", "was", "were", "what", "who", "how", "when", "where", "why", "can", "could", "would", "should", "do", "does", "did", "i", "me", "my", "we", "you", "your", "it", "about", "and", "or", "of", "in", "on", "at", "to", "for", "with"}
        
        # REMOVED the len(w) > 2 restriction so numbers like "1" and "2" are kept!
        raw_tokens = [w.lower() for w in message_text.split() if w.lower() not in stopwords]
        corrected_tokens = []
        
        for token in raw_tokens:
            if token in vocabulary:
                corrected_tokens.append(token)
            else:
                closest_word = min(vocabulary, key=lambda v: Levenshtein.distance(token, v), default=token)
                corrected_tokens.append(closest_word if Levenshtein.distance(token, closest_word) <= 2 else token)
        
        corrected_query = " ".join(corrected_tokens)
        if not corrected_query.strip():
            corrected_query = message_text.lower()
            corrected_tokens = corrected_query.split()

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([corrected_query])
        cosine_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

        bm25 = BM25Okapi(tokenized_corpus)
        bm25_scores = bm25.get_scores(corrected_tokens)

        max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1
        normalized_bm25 = [score / max_bm25 for score in bm25_scores]
        final_scores = (cosine_scores * 0.5) + (np.array(normalized_bm25) * 0.5)

        top_indices = np.argsort(final_scores)[::-1][:3]
        matched_laws = []
        
        for idx in top_indices:
            if final_scores[idx] > 0.05:
                law = all_laws[idx]
                # Find the specific chunk that matches best
                best_chunk = ""
                highest_overlap = -1
                query_set = set(corrected_tokens)
                for chunk in law.get('chunks', []):
                    chunk_tokens = set(chunk.lower().split())
                    overlap = len(query_set.intersection(chunk_tokens))
                    if overlap > highest_overlap:
                        highest_overlap = overlap
                        best_chunk = chunk
                law['best_match_chunk'] = best_chunk if best_chunk else (law.get('chunks', [""])[0] if law.get('chunks') else "")
                matched_laws.append(law)

        if not matched_laws:
            response = "I could not find a specific labor law matching your question in our database. Please note that this system provides legal awareness information only and is not a substitute for professional legal advice."
        else:
            response_parts = ["Based on your query, here are the most relevant Philippine Labor Laws:\n"]
            for law in matched_laws:
                # Safely grab the chunks and format them nicely, or fall back to old content
                body_text = "\n• ".join(law.get('chunks', [])) if law.get('chunks') else law.get('content', '')
                
                response_parts.append(
                    f"📌 {law.get('article', '')} {law.get('title', '')}\nSimplified: {law.get('simplified_text', '')}\n\n• {body_text}\n"
                )
            response_parts.append("\nPlease note that this system provides legal awareness information only and is not a substitute for professional legal advice.")
            response = "\n".join(response_parts)

        chat_record = {
            "id": str(uuid.uuid4()), "session_id": session_id, "user_id": user_id, 
            "user_message": message, "assistant_response": response, "laws": matched_laws,
            "context": context, "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.chat_history.insert_one(chat_record)

        return ChatResponse(response=response, session_id=session_id, laws=matched_laws)

    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"General error: {str(e)}")

@api_router.get("/chat/sessions")
async def get_user_sessions(user_id: str):
    try:
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$sort": {"created_at": -1}},
            {"$group": {"_id": "$session_id", "last_message": {"$first": "$user_message"}, "timestamp": {"$first": "$created_at"}}},
            {"$sort": {"timestamp": -1}}
        ]
        sessions = await db.chat_history.aggregate(pipeline).to_list(100)
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/chat/sessions/{session_id}")
async def get_chat_history(session_id: str):
    try:
        messages = await db.chat_history.find({"session_id": session_id}, {"_id": 0}).sort("created_at", 1).to_list(100)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ADMIN DASHBOARD ROUTES ====================

@api_router.get("/stats")
async def get_stats():
    try:
        chat_sessions = len(await db.chat_history.distinct("session_id"))
        laws_count = await db.legal_knowledge.count_documents({})
        return {"documents": 0, "translations": 0, "chat_sessions": chat_sessions, "legal_articles": laws_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/legal-knowledge")
async def get_all_laws():
    """Fetches all laws to display in the Admin Knowledge Base table."""
    try:
        laws = await db.legal_knowledge.find({}, {"_id": 0}).sort("article", 1).to_list(1000)
        
        # Format the data so the React frontend can read it without crashing
        formatted_laws = []
        for law in laws:
            # Fix the Title to include the Article Number
            if law.get('article'):
                law['title'] = f"{law.get('article')} - {law.get('title', '')}"
                
            # Stitch the chunks back together so the dashboard table has a 'content' field to display
            if law.get('chunks'):
                law['content'] = "\n\n".join(law.get('chunks'))
            elif not law.get('content'):
                law['content'] = law.get('simplified_text', 'No content available.')
                
            formatted_laws.append(law)
            
        return {"laws": formatted_laws}
    except Exception as e:
        logger.error(f"Error fetching legal knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/documents")
async def get_recent_documents(limit: int = 5):
    """Fetches the most recently added laws for the Admin Dashboard widget."""
    try:
        docs = await db.legal_knowledge.find({}, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
        
        # Apply the exact same formatting fix for the recent documents widget
        formatted_docs = []
        for doc in docs:
            if doc.get('article'):
                doc['title'] = f"{doc.get('article')} - {doc.get('title', '')}"
                
            if doc.get('chunks'):
                doc['content'] = "\n\n".join(doc.get('chunks'))
            elif not doc.get('content'):
                doc['content'] = doc.get('simplified_text', 'No content available.')
                
            formatted_docs.append(doc)
            
        return {"documents": formatted_docs}
    except Exception as e:
        logger.error(f"Error fetching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(api_router)
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup_event():
    await initialize_admin_user()
    await initialize_legal_knowledge()
    logger.info("LACBot API Started")

@app.on_event("shutdown")
async def shutdown_db_client(): client.close()