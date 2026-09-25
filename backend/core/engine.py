import os
import re
import torch
import logging
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from database import db
from core.retrieval import build_vocab_index

logger = logging.getLogger(__name__)
ROOT_DIR = Path(__file__).parent.parent  # backend/ (this file lives in backend/core/)

class SearchEngine:
    laws = []
    corpus = []
    title_corpus = []          
    article_numbers = []       
    tokenized_corpus = []
    vocabulary = set()
    vocab_by_letter = {}
    vectorizer = None
    tfidf_matrix = None
    vocab_idf = {}
    bm25 = None
    bge_model = None
    bge_embeddings = None

    @classmethod
    def get_bge_model(cls):
        if cls.bge_model is None:
            logger.info("Loading BGE-M3 Dense Model...")
            cls.bge_model = SentenceTransformer('BAAI/bge-m3')
        return cls.bge_model

search_engine = SearchEngine()

async def train_search_models():
    logger.info("Training SHIELD Search Models in memory...")
    all_laws = await db.legal_knowledge.find({}, {"_id": 0}).to_list(None)
    
    if not all_laws:
        logger.warning("No laws found in database to train.")
        search_engine.laws = []
        return

    search_engine.laws = all_laws
    corpus, title_corpus, article_numbers, tokenized_corpus = [], [], [], []
    
    stopwords = {"ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila", "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung", "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "naman", "lang", "daw", "din", "rin", "a", "an", "the", "is", "are", "was", "were", "what", "who", "how", "when", "where", "why", "can", "could", "would", "should", "do", "does", "did", "i", "me", "my", "we", "you", "your", "it", "about", "and", "or", "of", "in", "on", "to", "for", "with", "he", "she", "him", "his", "her", "they", "them", "their", "this", "that", "these", "those", "be", "been", "being", "has", "have", "had", "by", "from", "as", "not", "no", "any", "all", "such", "shall", "may", "will", "upon", "under", "which", "whom", "other", "out", "into", "same", "some", "give", "given", "gave", "take", "took", "get", "got", "make", "made", "know", "knew", "ask", "asked", "tell", "told", "say", "said", "just", "like", "want", "went", "go", "off", "up", "down"}
    
    for law in all_laws:
        body = " ".join(law.get('chunks', [])) if law.get('chunks') else law.get('content', '')
        tags_text = " ".join(law.get('tags', [])) if isinstance(law.get('tags', []), list) else str(law.get('tags', ''))
        intent_text = " ".join(law.get('intent_keywords', [])) if isinstance(law.get('intent_keywords', []), list) else str(law.get('intent_keywords', ''))
        article_str, title_str, category_str = law.get('article', '') or '', law.get('title', '') or '', law.get('category', '') or ''
        
        raw_doc = f"{article_str} {title_str} {article_str} {title_str} {category_str} {tags_text} {tags_text} {intent_text} {intent_text} {intent_text} {body}".lower()
        clean_doc = re.sub(r'[^\w\s]', '', raw_doc)
        corpus.append(clean_doc)
        
        title_corpus.append(re.sub(r'[^\w\s]', '', f"{article_str} {title_str} {category_str} {tags_text} {intent_text}".lower()))
        article_numbers.append(re.sub(r'[^\w\s]', '', article_str.lower()).strip())
        tokenized_corpus.append([w for w in clean_doc.split() if w not in stopwords and len(w) > 1])
        
    search_engine.vocabulary = set([w for doc in tokenized_corpus for w in doc if w not in stopwords and (len(w) > 2 or w.isdigit())])
    search_engine.vocab_by_letter = build_vocab_index(search_engine.vocabulary)
    search_engine.corpus, search_engine.title_corpus = corpus, title_corpus
    search_engine.article_numbers, search_engine.tokenized_corpus = article_numbers, tokenized_corpus
    
    search_engine.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=list(stopwords), min_df=1, sublinear_tf=True)
    search_engine.tfidf_matrix = search_engine.vectorizer.fit_transform(corpus)
    search_engine.vocab_idf = dict(zip(search_engine.vectorizer.get_feature_names_out(), search_engine.vectorizer.idf_))
    search_engine.bm25 = BM25Okapi(tokenized_corpus, k1=1.2, b=0.85)
    
    embeddings_cache_path = os.path.join(ROOT_DIR, "bge_embeddings.pt")
    if os.path.exists(embeddings_cache_path):
        search_engine.bge_embeddings = torch.load(embeddings_cache_path)
    else:
        encoder = SearchEngine.get_bge_model()
        encoder.max_seq_length = 512
        search_engine.bge_embeddings = encoder.encode(corpus, batch_size=4, show_progress_bar=True, convert_to_tensor=True)
        torch.save(search_engine.bge_embeddings, embeddings_cache_path)