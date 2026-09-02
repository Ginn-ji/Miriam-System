import re
import numpy as np
from pydantic import BaseModel
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein
from langdetect import detect
from deep_translator import GoogleTranslator

# Import synonyms just like the main server
from synonyms import LEGAL_SYNONYMS

# --- Pydantic Models ---
class TestCaseItem(BaseModel):
    test_id: str
    query: str
    expected_article: str

class ManualEvaluationRequest(BaseModel):
    test_cases: List[TestCaseItem]

# --- Core Logic ---
def calculate_ir_metrics(search_engine, test_cases: List[TestCaseItem]):
    evaluation_rows = []
    precision_list = []
    recall_list = []
    rr_list = []

    # Identical Stopwords from server.py
    stopwords = {
        "ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila", "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung", "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "naman", "lang", "daw", "din", "rin",
        "a", "an", "the", "is", "are", "was", "were", "what", "who", "how", "when", "where", "why", "can", "could", "would", "should", "do", "does", "did", "i", "me", "my", "we", "you", "your", "it", "about", "and", "or", "of", "in", "on", "to", "for", "with", 
        "he", "she", "him", "his", "her", "they", "them", "their", "this", "that", "these", "those", "be", "been", "being", "has", "have", "had", "by", "from", "as", "not", "no", "any", "all", "such", "shall", "may", "will", "upon", "under", "which", "whom", "other", "out", "into", "same", "some",
        "give", "given", "gave", "take", "took", "get", "got", "make", "made", "know", "knew", "ask", "asked", "tell", "told", "say", "said", "just", "like", "want", "went", "go", "off", "up", "down"
    }

    for item in test_cases:
        message_text = item.query.lower()
        
        # 1. EXPAND PHRASES AND SYNONYMS
        expanded_keywords = []
        raw_words = message_text.split()
        
        for term, english_terms in LEGAL_SYNONYMS.items():
            term_lower = term.lower()
            if " " in term_lower:
                if term_lower in message_text:
                    expanded_keywords.extend(english_terms)
            else:
                if term_lower in raw_words:
                    expanded_keywords.extend(english_terms)

        search_text = message_text
        
        # 2. GOOGLE TRANSLATION
        try:
            detected_lang = detect(search_text[:1000])
            if detected_lang in ['tl', 'unknown']:
                english_translation = GoogleTranslator(source='tl', target='en').translate(search_text)
                search_text = f"{search_text} {english_translation}"
        except Exception:
            pass

        full_query_text = f"{search_text} {' '.join(expanded_keywords)}"
        clean_full_query = re.sub(r'[^\w\s]', '', full_query_text)
        
        # 3. TOKENIZATION & STOPWORDS
        raw_tokens = [w.lower() for w in clean_full_query.split() if len(w) > 2 and w.lower() not in stopwords]

        # 4. EXACT MATCHES & LEVENSHTEIN CORRECTION
        exact_tokens = [t for t in raw_tokens if t in search_engine.vocabulary]

        if not exact_tokens:
            # If the chatbot would reject it entirely, metrics must log it as a total miss (0 scores)
            evaluation_rows.append({
                "test_id": item.test_id,
                "query": item.query,
                "ground_truth": item.expected_article,
                "retrieved_laws": ["Query Rejected (No Valid Terms)"],
                "is_relevant": "0 Found",
                "hit_rank": "N/A",
                "precision_k": "0.0%",
                "recall": "0.0%",
                "reciprocal_rank": 0.0
            })
            precision_list.append(0.0)
            recall_list.append(0.0)
            rr_list.append(0.0)
            continue

        corrected_tokens = list(exact_tokens)
        unmatched = [t for t in raw_tokens if t not in search_engine.vocabulary]
        
        for t in unmatched:
            if len(t) >= 6 and search_engine.vocabulary:
                closest = min(search_engine.vocabulary, key=lambda v: Levenshtein.distance(t, v))
                dist = Levenshtein.distance(t, closest)
                if dist == 1 or (dist == 2 and len(t) >= 9):
                    corrected_tokens.append(closest)
        
        query_text_for_math = " ".join(corrected_tokens)

        # 5. VECTOR SEARCH
        query_vec = search_engine.vectorizer.transform([query_text_for_math]) 
        cosine_scores = cosine_similarity(query_vec, search_engine.tfidf_matrix).flatten()
        bm25_scores = search_engine.bm25.get_scores(corrected_tokens) 
        
        bm25_array = np.array(bm25_scores)
        if len(bm25_array) > 0 and np.max(bm25_array) > 0:
            bm25_min = np.min(bm25_array)
            bm25_max = np.max(bm25_array)
            if bm25_max == bm25_min:
                bm25_norm = np.ones_like(bm25_array) 
            else:
                bm25_norm = (bm25_array - bm25_min) / (bm25_max - bm25_min)
        else:
            bm25_norm = np.zeros_like(bm25_array)
            
        final_scores = (cosine_scores * 0.5) + (bm25_norm * 0.5)
        
        # 6. EXACT CHATBOT FILTERING
        top_indices = np.argsort(final_scores)[::-1][:5]
        retrieved_laws = []
        exact_token_set = set(exact_tokens)
        
        for idx in top_indices:
            # Same strict threshold as server_3.py (0.25)
            if final_scores[idx] > 0.25: 
                doc_words = set(search_engine.corpus[idx].split())
                if exact_token_set & doc_words:
                    retrieved_laws.append(search_engine.laws[idx])
        
        # 7. MULTIPLE GROUND TRUTH MATCHING
        targets = [t.strip().lower() for t in item.expected_article.split(',')]
        total_expected = len(targets)
        
        relevant_count = 0
        first_match_rank = 0
        retrieved_labels = []

        for rank, law in enumerate(retrieved_laws, start=1):
            law_title = f"{law.get('article', '')} {law.get('title', '')}".strip()
            retrieved_labels.append(law_title)
            
            law_title_lower = law_title.lower()
            law_article_lower = (law.get('article') or '').lower()
            
            is_match = False
            for target in targets:
                if target in law_title_lower or target in law_article_lower:
                    is_match = True
                    break 
                    
            if is_match:
                relevant_count += 1
                if first_match_rank == 0:
                    first_match_rank = rank

        # 8. COMPUTE FINAL METRICS
        total_k = len(retrieved_laws)
        p_at_k = (relevant_count / total_k) if total_k > 0 else 0.0
        recall = min((relevant_count / total_expected), 1.0) if total_expected > 0 else 0.0
        rr = (1.0 / first_match_rank) if first_match_rank > 0 else 0.0

        precision_list.append(p_at_k)
        recall_list.append(recall)
        rr_list.append(rr)

        evaluation_rows.append({
            "test_id": item.test_id,
            "query": item.query,
            "ground_truth": item.expected_article,
            "retrieved_laws": retrieved_labels[:3] if retrieved_labels else ["None Found"],
            "is_relevant": f"{relevant_count}/{total_expected} Found",
            "hit_rank": first_match_rank if first_match_rank > 0 else "N/A",
            "precision_k": f"{round(p_at_k * 100, 1)}%",
            "recall": f"{round(recall * 100, 1)}%",
            "reciprocal_rank": round(rr, 3)
        })

    # Macro Averages across all test cases
    macro_precision = np.mean(precision_list) if precision_list else 0.0
    macro_recall = np.mean(recall_list) if recall_list else 0.0
    f1 = (2 * macro_precision * macro_recall / (macro_precision + macro_recall)) if (macro_precision + macro_recall) > 0 else 0.0
    mrr = np.mean(rr_list) if rr_list else 0.0

    return {
        "summary": {
            "macro_precision": f"{round(macro_precision * 100, 2)}%",
            "macro_recall": f"{round(macro_recall * 100, 2)}%",
            "f1_score": f"{round(f1 * 100, 2)}%",
            "mrr": round(mrr, 3),
            "total_tested": len(test_cases)
        },
        "results_matrix": evaluation_rows
    }