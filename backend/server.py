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
import re

# NLP and Math libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator
import bcrypt

# Import the external synonyms dictionary
from synonyms import LEGAL_SYNONYMS

# Import the manual IR evaluation metrics module
from metrics import ManualEvaluationRequest, calculate_ir_metrics

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
class SearchEngine:
    laws = []
    corpus = []
    title_corpus = []          # stores ONLY article number + title + tags (no body)
    article_numbers = []       # stores the raw article number string per law (e.g. "article 1")
    tokenized_corpus = []
    vocabulary = set()
    vectorizer = None
    tfidf_matrix = None
    vocab_idf = {}
    bm25 = None
    highest_bm25 = 0.0

class BulkDeleteRequest(BaseModel):
    ids: List[str]

search_engine = SearchEngine()

async def train_search_models():
    """Fetches all laws from the database and pre-trains the TF-IDF and BM25 models in memory."""
    logger.info("Training SHIELD Search Models in memory...")
    all_laws = await db.legal_knowledge.find({}, {"_id": 0}).to_list(None)
    
    if not all_laws:
        logger.warning("No laws found in database to train.")
        search_engine.laws = []
        search_engine.corpus = []
        search_engine.title_corpus = []
        search_engine.article_numbers = []
        search_engine.tokenized_corpus = []
        search_engine.vocabulary = set()
        search_engine.vectorizer = None
        search_engine.tfidf_matrix = None
        search_engine.bm25 = None
        return

    search_engine.laws = all_laws
    corpus = []
    title_corpus = []
    article_numbers = []
    tokenized_corpus = []
    
    stopwords = {
        "ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila", "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung", "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "naman", "lang", "daw", "din", "rin",
        "a", "an", "the", "is", "are", "was", "were", "what", "who", "how", "when", "where", "why", "can", "could", "would", "should", "do", "does", "did", "i", "me", "my", "we", "you", "your", "it", "about", "and", "or", "of", "in", "on", "to", "for", "with",
        "he", "she", "him", "his", "her", "they", "them", "their", "this", "that", "these", "those", "be", "been", "being", "has", "have", "had", "by", "from", "as", "not", "no", "any", "all", "such", "shall", "may", "will", "upon", "under", "which", "whom", "other", "out", "into", "same", "some",
        "give", "given", "gave", "take", "took", "get", "got", "make", "made", "know", "knew", "ask", "asked", "tell", "told", "say", "said", "just", "like", "want", "went", "go", "off", "up", "down"
    }
    
    for law in all_laws:
        body = " ".join(law.get('chunks', [])) if law.get('chunks') else law.get('content', '')
        tags = law.get('tags', [])
        tags_text = " ".join(tags) if isinstance(tags, list) else str(tags)
        article_str = law.get('article', '') or ''
        title_str = law.get('title', '') or ''
        category_str = law.get('category', '') or ''
        
        # --- Full corpus: article + title (3x boosted) + category + tags (2x boosted) + body ---
        # Repeating title/tags gives them higher TF-IDF weight vs body noise
        raw_doc_text = f"{article_str} {title_str} {article_str} {title_str} {category_str} {tags_text} {tags_text} {body}".lower()
        clean_doc_text = re.sub(r'[^\w\s]', '', raw_doc_text)
        corpus.append(clean_doc_text)
        
        # --- Title-only corpus: article number + title + category + tags only (no body) ---
        raw_title_text = f"{article_str} {title_str} {category_str} {tags_text}".lower()
        clean_title_text = re.sub(r'[^\w\s]', '', raw_title_text)
        title_corpus.append(clean_title_text)
        
        # --- Store normalized article number for direct lookup ---
        article_numbers.append(re.sub(r'[^\w\s]', '', article_str.lower()).strip())
        
        # --- BM25 tokenized corpus: include stopword filtering ---
        tokenized_corpus.append([w for w in clean_doc_text.split() if w not in stopwords and len(w) > 1])
        
    search_engine.vocabulary = set([
        word for doc in tokenized_corpus for word in doc
        if word not in stopwords and (len(word) > 2 or word.isdigit())
    ])
    search_engine.corpus = corpus
    search_engine.title_corpus = title_corpus
    search_engine.article_numbers = article_numbers
    search_engine.tokenized_corpus = tokenized_corpus
    
    # Train TF-IDF with bilingual stopwords
    search_engine.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=list(stopwords), min_df=1)
    search_engine.tfidf_matrix = search_engine.vectorizer.fit_transform(corpus)
    search_engine.vocab_idf = dict(zip(search_engine.vectorizer.get_feature_names_out(), search_engine.vectorizer.idf_))
    
    # Train BM25 on stop-word-filtered tokenized corpus
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

class RoleUpdateRequest(BaseModel):
    requester_id: str
    new_role: str

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

class SavedTestCase(BaseModel):
    test_id: str
    query: str
    expected_article: str

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

# --- Conversational noise & filler phrases in Filipino/Taglish ---
CONVERSATIONAL_FILLERS = [
    r"\bano po ba ang\b", r"\bano po ba\b", r"\bano po\b", r"\bano ba ang\b", r"\bano ba\b",
    r"\bpwede po ba akong\b", r"\bpwede po bang\b", r"\bpwede po ba\b", r"\bpwede bang\b", r"\bpwede ba akong\b", r"\bpwede ba\b",
    r"\btanong ko lang po\b", r"\btanong ko lang\b", r"\bgusto ko lang itanong\b", r"\bgusto ko lang malaman\b",
    r"\blegal po ba na\b", r"\blegal po ba\b", r"\blegal ba na\b", r"\blegal ba\b",
    r"\bmeron po ba akong\b", r"\bmayroon po ba akong\b", r"\bmeron ba akong\b",
    r"\bano ang dapat kong gawin kapag\b", r"\bano dapat gawin kapag\b", r"\bano gagawin kapag\b",
    r"\bkasi naman\b", r"\bbigla na lang\b", r"\bbasta na lang\b", r"\blang po\b", r"\bpo ba\b"
]

def clean_conversational_noise(text: str) -> str:
    """Strips polite conversational preambles, expands hyphens, and normalizes Tagalog ligatures."""
    cleaned = text.lower().replace('"', ' ').replace("'", " ")
    for pattern in CONVERSATIONAL_FILLERS:
        cleaned = re.sub(pattern, " ", cleaned)
    # Expand hyphens into spaces so compound verbs/nouns (e.g. "mag-inspect" -> "mag inspect") separate cleanly
    cleaned = cleaned.replace("-", " ")
    # Normalize standard Tagalog enclitic ligatures (e.g. "pwedeng" -> "pwede", "maling" -> "mali")
    cleaned = re.sub(r'\b(\w{4,})ng\b', r'\1', cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()

def strip_filipino_affixes(word: str) -> str:
    """Lightweight rule-based morphological stemmer for Filipino verbs and nouns."""
    w = word.lower()
    if len(w) <= 4:
        return w
    # Infix -in- (e.g. tinanggal -> tanggal, kinakaltas -> kaltas, sinibak -> sibak)
    if len(w) > 4 and w[1:3] == 'in' and w[0] not in 'aeiou':
        w = w[0] + w[3:]
    # Infix -um- (e.g. pumasok -> pasok)
    if len(w) > 4 and w[1:3] == 'um' and w[0] not in 'aeiou':
        w = w[0] + w[3:]
    # Prefixes: pinag-, ipag-, pina-, nag-, mag-, pag-
    for pre in ['pinag', 'ipag', 'pina', 'nag', 'mag', 'pag']:
        if w.startswith(pre) and len(w) > len(pre) + 2:
            w = w[len(pre):]
            break
    # Reduplication (e.g. tatanggal -> tanggal, papasok -> pasok)
    if len(w) >= 6 and w[:2] == w[2:4]:
        w = w[2:]
    # Suffixes: -han, -hin, -an, -in
    for suf in ['han', 'hin', 'an', 'in']:
        if w.endswith(suf) and len(w) > len(suf) + 3:
            w = w[:-len(suf)]
            break
    return w

TAGALOG_MARKERS = {
    "ang", "ng", "sa", "na", "mga", "ko", "mo", "ako", "ka", "siya", "kami", "tayo", "kayo", "sila",
    "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung",
    "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "naman", "lang", "daw", "din", "rin",
    "may", "wala", "walang", "hindi", "ayaw", "trabaho", "sahod", "sweldo", "suweldo", "kaltas", "tanggal",
    "tinanggal", "tinanggalan", "sinibak", "pinaalis", "nagresign", "overtime", "buntis", "amo", "boss"
}

def is_tagalog_or_taglish(text: str) -> bool:
    """Checks if text contains Tagalog grammatical markers or vocabulary."""
    tokens = set(re.sub(r'[^\w\s]', '', text.lower()).split())
    if tokens & TAGALOG_MARKERS:
        return True
    detected = detect_language_simple(text)
    return detected in ['tl', 'unknown', 'id', 'ms', 'sk', 'cy', 'hr']

async def get_or_create_translation(text: str) -> str:
    """Fetches translation with persistent MongoDB cache for 100% determinism and speed."""
    if not text.strip():
        return ""
    try:
        cached = await db.translation_cache.find_one({"query": text})
        if cached:
            return cached.get("translation", "")
    except Exception:
        pass
    
    try:
        translated = GoogleTranslator(source='tl', target='en').translate(text)
        if translated:
            try:
                await db.translation_cache.insert_one({"query": text, "translation": translated})
            except Exception:
                pass
            return translated
    except Exception as e:
        logger.warning(f"Translation module failed: {e}")
    return ""

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
    return {"message": "SHIELD Legal Awareness Chat Bot"}

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
        
        background_tasks.add_task(train_search_models)
        return {"message": "Legal knowledge uploaded successfully", "id": law["id"]}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/legal-knowledge/bulk-delete")
async def bulk_delete_laws(request: BulkDeleteRequest, background_tasks: BackgroundTasks):
    try:
        result = await db.legal_knowledge.delete_many({"id": {"$in": request.ids}})
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

@api_router.delete("/legal-knowledge/{law_id}")
async def delete_legal_knowledge(law_id: str, background_tasks: BackgroundTasks):
    try:
        result = await db.legal_knowledge.delete_one({"id": law_id})
        if result.deleted_count == 0: raise HTTPException(status_code=404, detail="Law not found")
        
        background_tasks.add_task(train_search_models)
        return {"message": "Law deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/legal-knowledge/{law_id}")
async def update_legal_knowledge(law_id: str, law: LegalKnowledge, background_tasks: BackgroundTasks):
    try:
        law_dict = law.model_dump()
        if isinstance(law_dict.get('chunks'), str): 
            law_dict['chunks'] = [c.strip() for c in law_dict['chunks'].split('\n') if c.strip()]
        if isinstance(law_dict.get('tags'), str): 
            law_dict['tags'] = [t.strip() for t in law_dict['tags'].split(',') if t.strip()]
            
        law_dict.pop('_id', None)
        law_dict.pop('id', None)
        
        result = await db.legal_knowledge.update_one(
            {"id": law_id},
            {"$set": law_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Law not found")
            
        background_tasks.add_task(train_search_models)
        return {"message": "Law updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== HYBRID CHATBOT RETRIEVAL (MEMORY-BASED) ====================

@api_router.post("/chat", response_model=ChatResponse)
async def legal_chat(message: str = Form(...), session_id: Optional[str] = Form(None), user_id: Optional[str] = Form(None)):
    try:
        session_id = session_id or str(uuid.uuid4())
        
        # --- NEW: 1,000 Word Limit Check for Chatbot ---
        if len(message.split()) > 1000:
            return ChatResponse(
                response="Your query is too long. Please keep your question under 1,000 words.", 
                session_id=session_id, 
                laws=[]
            )
        # -----------------------------------------------
            
        # --- STEP 1: CONVERSATIONAL NOISE REDUCTION ---
        clean_message = clean_conversational_noise(message)
        message_text = clean_message.lower() if clean_message else message.lower()
            
        if not search_engine.laws or search_engine.vectorizer is None:
            return ChatResponse(response="System is initializing or no laws are available. Please try again in a moment.", session_id=session_id, laws=[])

        # =========================================================
        # STEP 0: DIRECT ARTICLE NUMBER LOOKUP
        # If the query matches "Article N" / "Art. N", find and prepend
        # that exact article BEFORE any scoring pipeline runs.
        # This completely bypasses TF-IDF / BM25 / threshold guards.
        # =========================================================
        article_num_match = re.search(r'\barticle\s+(\d+)\b|\bart\.?\s*(\d+)\b', message.lower())
        direct_article_number = None
        direct_article_index = None
        if article_num_match:
            direct_article_number = article_num_match.group(1) or article_num_match.group(2)
            for idx, art_num in enumerate(search_engine.article_numbers):
                stored_digits = re.search(r'\d+', art_num)
                if stored_digits and stored_digits.group() == direct_article_number:
                    direct_article_index = idx
                    break

        # --- STEP 2: EXPAND PHRASES AND SYNONYMS (Punctuation-free + Affix-aware) ---
        expanded_keywords = []
        clean_text_no_punct = re.sub(r'[^\w\s]', ' ', message_text)
        raw_words = clean_text_no_punct.split()
        stemmed_words = [strip_filipino_affixes(w) for w in raw_words]
        all_candidate_words = set(raw_words + stemmed_words)
        
        for term, english_terms in LEGAL_SYNONYMS.items():
            term_lower = term.lower()
            if " " in term_lower:
                if term_lower in message_text or term_lower in clean_text_no_punct:
                    expanded_keywords.extend(english_terms)
            else:
                if term_lower in all_candidate_words:
                    expanded_keywords.extend(english_terms)

        search_text = message_text
        
        # --- STEP 3: RELIABLE LANGUAGE DETECTION & CACHED TRANSLATION ---
        if is_tagalog_or_taglish(search_text):
            translation = await get_or_create_translation(clean_text_no_punct)
            if translation:
                search_text = f"{search_text} {translation}"

        # Combine translated text with the safely extracted synonyms
        full_query_text = f"{search_text} {' '.join(expanded_keywords)}"
        
        # Strip punctuation from query for accurate matching
        clean_full_query = re.sub(r'[^\w\s]', '', full_query_text)

        # --- STEP 4: TOKENIZATION & STOPWORDS ---
        stopwords = {
            "ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila", "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung", "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "naman", "lang", "daw", "din", "rin",
            "a", "an", "the", "is", "are", "was", "were", "what", "who", "how", "when", "where", "why", "can", "could", "would", "should", "do", "does", "did", "i", "me", "my", "we", "you", "your", "it", "about", "and", "or", "of", "in", "on", "to", "for", "with", 
            "he", "she", "him", "his", "her", "they", "them", "their", "this", "that", "these", "those", "be", "been", "being", "has", "have", "had", "by", "from", "as", "not", "no", "any", "all", "such", "shall", "may", "will", "upon", "under", "which", "whom", "other", "out", "into", "same", "some",
            "give", "given", "gave", "take", "took", "get", "got", "make", "made", "know", "knew", "ask", "asked", "tell", "told", "say", "said", "just", "like", "want", "went", "go", "off", "up", "down"
        }
        
        # Allow short numeric tokens through (e.g. "1", "13") for article number queries
        raw_tokens = [w.lower() for w in clean_full_query.split()
                      if (len(w) > 2 or w.isdigit()) and w.lower() not in stopwords]

        # --- STEP 5: EXACT MATCHES & LEVENSHTEIN FUZZY CORRECTION (Threshold d <= 2) ---
        exact_tokens = [t for t in raw_tokens if t in search_engine.vocabulary]
        corrected_tokens = list(exact_tokens)
        unmatched = [t for t in raw_tokens if t not in search_engine.vocabulary]
        
        for t in unmatched:
            if len(t) >= 4 and search_engine.vocabulary:
                closest = min(search_engine.vocabulary, key=lambda v: Levenshtein.distance(t, v))
                dist = Levenshtein.distance(t, closest)
                if dist == 1 or (dist == 2 and len(t) >= 6):
                    corrected_tokens.append(closest)

        # Only reject if neither exact nor fuzzy match produced any valid legal tokens
        if not corrected_tokens:
            return ChatResponse(
                response="This query does not appear to be related to Philippine Labor Law. Please ask a specific workplace, employment, or labor dispute question.",
                session_id=session_id, laws=[]
            )
        
        query_text_for_math = " ".join(corrected_tokens)
        
        # --- STEP 6: EXPLOIT CACHED MODELS (Instant Speed) ---
        query_vec = search_engine.vectorizer.transform([query_text_for_math]) 
        cosine_scores = cosine_similarity(query_vec, search_engine.tfidf_matrix).flatten()
        bm25_scores = search_engine.bm25.get_scores(corrected_tokens) 
        
        # =========================================================
        # MIN-MAX NORMALIZATION & COMBSUM DATA FUSION
        # =========================================================
        bm25_array = np.array(bm25_scores)
        
        # Normalize BM25 to [0, 1] — use zeros (not ones) when all scores are equal
        if len(bm25_array) > 0 and np.max(bm25_array) > 0:
            bm25_min = np.min(bm25_array)
            bm25_max = np.max(bm25_array)
            if bm25_max == bm25_min:
                bm25_norm = np.zeros_like(bm25_array)   # no signal → no boost
            else:
                bm25_norm = (bm25_array - bm25_min) / (bm25_max - bm25_min)
        else:
            bm25_norm = np.zeros_like(bm25_array)

        # --- TITLE BOOST SCORE (IDF-Weighted) ---
        # Rare, domain-specific words (e.g. "disability", "dismissal", "inspection") give much higher boost
        # than generic ubiquitous words (e.g. "work", "employment").
        title_boost = np.zeros(len(search_engine.laws))
        query_token_set = set(corrected_tokens)
        vocab_idf = getattr(search_engine, 'vocab_idf', {})
        for idx, title_text in enumerate(search_engine.title_corpus):
            title_words = set(title_text.split())
            matching_title_words = query_token_set & title_words
            if matching_title_words:
                title_boost[idx] = sum(vocab_idf.get(w, 1.0) for w in matching_title_words)

        # Normalize title boost to [0, 1]
        tb_max = np.max(title_boost)
        title_boost_norm = title_boost / tb_max if tb_max > 0 else title_boost

        # CombSUM Fusion: 35% TF-IDF + 40% BM25 + 25% Title Boost
        final_scores = (cosine_scores * 0.35) + (bm25_norm * 0.40) + (title_boost_norm * 0.25)
        # =========================================================
        
        try:
            limit_setting = await db.settings.find_one({"key": "chat_limit"})
            chat_limit = int(limit_setting.get("value", 5)) if limit_setting else 5
        except:
            chat_limit = 5
        
        matched_laws = []
        
        # --- DIRECT ARTICLE PRE-FETCH: inject the exact article as result #1 ---
        if direct_article_index is not None:
            direct_law = search_engine.laws[direct_article_index].copy()
            qs = set(corrected_tokens)
            chunks = direct_law.get('chunks') or []
            if chunks:
                direct_law['best_match_chunk'] = max(
                    chunks,
                    key=lambda c: len(qs.intersection(set(c.lower().split()))) / max(len(c.split()), 1),
                    default=""
                ) or direct_law.get('simplified_text', '')
            else:
                direct_law['best_match_chunk'] = direct_law.get('simplified_text') or (direct_law.get('content', '') or '')[:500]
            direct_law['accuracy'] = "100%"
            matched_laws.append(direct_law)

        top_indices = np.argsort(final_scores)[::-1]
        query_match_tokens = set(corrected_tokens)

        for i in top_indices:
            if len(matched_laws) >= chat_limit:
                break
            # Skip the directly-fetched article so it isn't duplicated
            if direct_article_index is not None and i == direct_article_index:
                continue
            if final_scores[i] > 0.25: 
                law_data = search_engine.laws[i].copy()
                doc_words = set(search_engine.corpus[i].split())
                if not (query_match_tokens & doc_words):
                    continue
                    
                raw_percentage = int(final_scores[i] * 100)
                law_data['accuracy'] = f"{raw_percentage}%"
                
                qs = set(corrected_tokens)
                chunks = law_data.get('chunks') or []
                if chunks:
                    law_data['best_match_chunk'] = max(
                        chunks,
                        key=lambda c: len(qs.intersection(set(c.lower().split()))) / max(len(c.split()), 1),
                        default=""
                    ) or law_data.get('simplified_text', '')
                else:
                    law_data['best_match_chunk'] = law_data.get('simplified_text') or (law_data.get('content', '') or '')[:500]
                
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

@api_router.get("/users")
async def get_all_users(requester_id: str):
    """Fetches all users. Only accessible by a super_admin."""
    requester = await db.users.find_one({"id": requester_id})
    
    if not requester or requester.get("role") != "super_admin":
        raise HTTPException(status_code=403, detail="Access Denied: Only Super Admins can view the user list.")
    
    # Return all users but hide their passwords for security
    users = await db.users.find({}, {"_id": 0, "password": 0}).to_list(1000)
    return {"users": users}

@api_router.put("/users/{target_id}/role")
async def update_user_role(target_id: str, request: RoleUpdateRequest):
    """Updates a user's role. Only accessible by a super_admin."""
    requester = await db.users.find_one({"id": request.requester_id})
    
    if not requester or requester.get("role") != "super_admin":
        raise HTTPException(status_code=403, detail="Access Denied: Only Super Admins can modify user roles.")
    
    if request.new_role not in ["user", "admin", "super_admin"]:
        raise HTTPException(status_code=400, detail="Invalid role provided.")
        
    result = await db.users.update_one(
        {"id": target_id},
        {"$set": {"role": request.new_role}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Target user not found.")
        
    return {"message": f"User role successfully updated to {request.new_role}"}

@api_router.get("/stats")
async def get_stats():
    sessions = len(await db.chat_history.distinct("session_id"))
    laws = await db.legal_knowledge.count_documents({})
    return {"chat_sessions": sessions, "legal_articles": laws}

# ==================== TEST CASE DATABASE CLOUD ROUTES ====================
@api_router.get("/admin/metrics/test-cases")
async def get_test_cases():
    """Fetches all saved benchmark test cases from the cloud database."""
    cases = await db.test_cases.find({}, {"_id": 0}).to_list(1000)
    return {"test_cases": cases}

@api_router.post("/admin/metrics/test-cases")
async def add_test_case(test_case: SavedTestCase):
    """Saves a new test case to the cloud database."""
    case_dict = test_case.model_dump()
    
    # Ensure no duplicate test IDs exist
    existing = await db.test_cases.find_one({"test_id": case_dict["test_id"]})
    if existing:
        raise HTTPException(status_code=400, detail="Test ID already exists.")
        
    await db.test_cases.insert_one(case_dict)
    return {"message": "Test case saved to cloud database."}

@api_router.delete("/admin/metrics/test-cases/{test_id}")
async def delete_test_case(test_id: str):
    """Deletes a test case from the cloud database."""
    result = await db.test_cases.delete_one({"test_id": test_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Test case not found.")
    return {"message": "Test case deleted."}


@api_router.post("/admin/metrics/evaluate")
async def evaluate_search_metrics(payload: ManualEvaluationRequest, requester_id: str):
    """Runs manually-entered test cases against the live search engine and returns
    precision/recall/F1/MRR metrics. Only accessible by admins and super_admins."""
    requester = await db.users.find_one({"id": requester_id})

    if not requester or requester.get("role") not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Access Denied: Only Admins can run metric evaluations.")

    if not payload.test_cases:
        raise HTTPException(status_code=400, detail="No test cases provided.")

    if search_engine.vectorizer is None or search_engine.bm25 is None:
        raise HTTPException(status_code=400, detail="Search models are not trained yet. Add legal knowledge first.")

    try:
        limit_setting = await db.settings.find_one({"key": "chat_limit"})
        chat_limit = int(limit_setting.get("value", 3)) if limit_setting else 3
    except:
        chat_limit = 3

    return calculate_ir_metrics(search_engine, payload.test_cases, k=chat_limit)

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

origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:4173", "http://127.0.0.1:4173", "https://lacbot.vercel.app", "https://miriam-system.vercel.app"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup_event():
    # 1. Check if a super_admin exists
    super_admin_exists = await db.users.find_one({"role": "super_admin"})
    
    if not super_admin_exists:
        # If no super_admin exists, see if the default admin is there and upgrade it
        admin_user = await db.users.find_one({"username": "admin"})
        if admin_user:
            await db.users.update_one({"_id": admin_user["_id"]}, {"$set": {"role": "super_admin"}})
            logger.info("Upgraded default admin to super_admin.")
        else:
            # Create a brand new super_admin if the database is completely empty
            await db.users.insert_one({
                "id": str(uuid.uuid4()), 
                "username": "superadmin", 
                "password": "adminpassword", 
                "role": "super_admin", 
                "created_at": datetime.now(timezone.utc).isoformat()
            })
            logger.info("Created new superadmin account.")
    
    # 2. Trigger in-memory search model training
    await train_search_models()
    logger.info("SHIELD API Started and Models Loaded")

@app.on_event("shutdown")
async def shutdown_db_client(): client.close()