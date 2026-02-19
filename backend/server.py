from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
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
from emergentintegrations.llm.chat import LlmChat, UserMessage
import PyPDF2
import io
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize Emergent LLM Key
EMERGENT_KEY = os.getenv("EMERGENT_LLM_KEY", "")

# ==================== MODELS ====================

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

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LegalKnowledge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    category: str
    content: str
    tags: List[str]
    language: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ==================== HELPER FUNCTIONS ====================

async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting PDF: {str(e)}")

def detect_language_simple(text: str) -> str:
    """Detect language using langdetect"""
    try:
        lang = detect(text[:1000])  # Use first 1000 chars for detection
        return lang
    except:
        return "unknown"

async def initialize_legal_knowledge():
    """Initialize mock Philippine legal database"""
    count = await db.legal_knowledge.count_documents({})
    if count > 0:
        return
    
    mock_laws = [
        {
            "id": str(uuid.uuid4()),
            "title": "Civil Code of the Philippines - Article 19",
            "category": "Civil Law",
            "content": "Every person must, in the exercise of his rights and in the performance of his duties, act with justice, give everyone his due, and observe honesty and good faith.",
            "tags": ["civil law", "rights", "duties", "good faith"],
            "language": "en",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Labor Code - Article 279",
            "category": "Labor Law",
            "content": "In cases of regular employment, the employer shall not terminate the services of an employee except for a just cause or when authorized by law.",
            "tags": ["labor", "employment", "termination", "just cause"],
            "language": "en",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Republic Act 8353 - Anti-Rape Law",
            "category": "Criminal Law",
            "content": "Rape is committed by a man who shall have carnal knowledge of a woman through force, threat, or intimidation.",
            "tags": ["criminal law", "rape", "sexual crimes"],
            "language": "en",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Family Code - Article 1",
            "category": "Family Law",
            "content": "Marriage is a special contract of permanent union between a man and a woman entered into in accordance with law for the establishment of conjugal and family life.",
            "tags": ["family law", "marriage", "conjugal rights"],
            "language": "en",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Data Privacy Act of 2012",
            "category": "Privacy Law",
            "content": "It is the policy of the State to protect the fundamental human right of privacy while ensuring free flow of information to promote innovation and growth.",
            "tags": ["privacy", "data protection", "personal information"],
            "language": "en",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Batas Sibil ng Pilipinas - Artikulo 19",
            "category": "Batas Sibil",
            "content": "Ang bawat tao ay dapat, sa paggamit ng kanyang mga karapatan at sa pagtupad ng kanyang mga tungkulin, kumilos nang may katarungan, bigyan ang bawat isa ng kanyang karapatdapat, at sundin ang katapatan at mabuting pananampalataya.",
            "tags": ["batas sibil", "karapatan", "tungkulin", "mabuting pananampalataya"],
            "language": "tl",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.legal_knowledge.insert_many(mock_laws)

# ==================== ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "Miriam Legal Assistance API"}

# Language Detection
@api_router.post("/detect-language")
async def detect_language_endpoint(request: dict):
    try:
        text = request.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        detected = detect_language_simple(text)
        return {
            "detected_language": detected,
            "confidence": 0.9 if detected != "unknown" else 0.0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Translation (Placeholder - can be activated with Google API keys)
@api_router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        # Detect source language if auto
        source_lang = request.source_language
        if source_lang == "auto":
            source_lang = detect_language_simple(request.text)
        
        # For now, return placeholder translation
        # When Google API keys are added, this will use actual translation
        translated = f"[Translation from {source_lang} to {request.target_language}]: {request.text}"
        
        # Save translation history
        translation_record = {
            "id": str(uuid.uuid4()),
            "original_text": request.text,
            "translated_text": translated,
            "source_language": source_lang,
            "target_language": request.target_language,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.translations.insert_one(translation_record)
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated,
            source_language=source_lang,
            target_language=request.target_language,
            detected_language=source_lang if request.source_language == "auto" else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Translation History
@api_router.get("/translations")
async def get_translations(limit: int = 20):
    try:
        translations = await db.translations.find({}, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
        return {"translations": translations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Document Upload
@api_router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            text_content = await extract_text_from_pdf(content)
            doc_type = "pdf"
        else:
            text_content = content.decode('utf-8')
            doc_type = "text"
        
        # Detect language
        language = detect_language_simple(text_content)
        
        # Create document record
        doc = {
            "id": str(uuid.uuid4()),
            "filename": file.filename,
            "content": text_content,
            "document_type": doc_type,
            "language": language,
            "tags": [],
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.documents.insert_one(doc)
        
        return {
            "id": doc["id"],
            "filename": doc["filename"],
            "language": language,
            "message": "Document uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Documents
@api_router.get("/documents")
async def get_documents(limit: int = 20):
    try:
        documents = await db.documents.find({}, {"_id": 0, "content": 0}).sort("created_at", -1).limit(limit).to_list(limit)
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Single Document
@api_router.get("/documents/{document_id}")
async def get_document(document_id: str):
    try:
        document = await db.documents.find_one({"id": document_id}, {"_id": 0})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Legal Chat with Claude Sonnet
@api_router.post("/chat", response_model=ChatResponse)
async def legal_chat(request: ChatRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Initialize Claude chat
        chat = LlmChat(
            api_key=EMERGENT_KEY,
            session_id=session_id,
            system_message="You are a knowledgeable Philippine legal assistant. Provide accurate, helpful legal information while clearly stating you are not providing legal advice. Reference relevant Philippine laws when applicable. Be professional and clear."
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        # Add context if provided
        message_text = request.message
        if request.context:
            message_text = f"Context: {request.context}\n\nQuestion: {request.message}"
        
        # Send message
        user_message = UserMessage(text=message_text)
        response = await chat.send_message(user_message)
        
        # Save chat history
        chat_record = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "user_message": request.message,
            "assistant_response": response,
            "context": request.context,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.chat_history.insert_one(chat_record)
        
        return ChatResponse(
            response=response,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Chat History
@api_router.get("/chat/sessions/{session_id}")
async def get_chat_history(session_id: str):
    try:
        messages = await db.chat_history.find(
            {"session_id": session_id},
            {"_id": 0}
        ).sort("created_at", 1).to_list(100)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Search Legal Knowledge
@api_router.get("/legal-knowledge")
async def search_legal_knowledge(q: Optional[str] = None, category: Optional[str] = None, language: Optional[str] = None):
    try:
        query = {}
        if q:
            query["$or"] = [
                {"title": {"$regex": q, "$options": "i"}},
                {"content": {"$regex": q, "$options": "i"}},
                {"tags": {"$regex": q, "$options": "i"}}
            ]
        if category:
            query["category"] = category
        if language:
            query["language"] = language
        
        laws = await db.legal_knowledge.find(query, {"_id": 0}).limit(50).to_list(50)
        return {"laws": laws}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Statistics
@api_router.get("/stats")
async def get_stats():
    try:
        docs_count = await db.documents.count_documents({})
        translations_count = await db.translations.count_documents({})
        chat_sessions = len(await db.chat_history.distinct("session_id"))
        laws_count = await db.legal_knowledge.count_documents({})
        
        return {
            "documents": docs_count,
            "translations": translations_count,
            "chat_sessions": chat_sessions,
            "legal_articles": laws_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await initialize_legal_knowledge()
    logger.info("Miriam API Started")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()