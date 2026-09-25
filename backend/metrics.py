import re
import numpy as np
import torch
from sentence_transformers import util
from pydantic import BaseModel
from typing import List
import Levenshtein
from langdetect import detect
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

from synonyms import LEGAL_SYNONYMS

# ─────────────────────────────────────────────────────────────
# PYDANTIC MODELS
# ─────────────────────────────────────────────────────────────
class TestCaseItem(BaseModel):
    test_id: str
    query: str
    expected_article: str

class ManualEvaluationRequest(BaseModel):
    test_cases: List[TestCaseItem]


# ─────────────────────────────────────────────────────────────
# MODULE-LEVEL CONSTANTS  (defined ONCE, not inside any loop)
# ─────────────────────────────────────────────────────────────
CONVERSATIONAL_FILLERS = [
    r"\bano po ba ang\b", r"\bano po ba\b", r"\bano po\b", r"\bano ba ang\b", r"\bano ba\b",
    r"\bpwede po ba akong\b", r"\bpwede po bang\b", r"\bpwede po ba\b", r"\bpwede bang\b",
    r"\bpwede ba akong\b", r"\bpwede ba\b",
    r"\btanong ko lang po\b", r"\btanong ko lang\b",
    r"\bgusto ko lang itanong\b", r"\bgusto ko lang malaman\b",
    r"\blegal po ba na\b", r"\blegal po ba\b", r"\blegal ba na\b", r"\blegal ba\b",
    r"\bmeron po ba akong\b", r"\bmayroon po ba akong\b", r"\bmeron ba akong\b",
    r"\bano ang dapat kong gawin kapag\b", r"\bano dapat gawin kapag\b", r"\bano gagawin kapag\b",
    r"\bkasi naman\b", r"\bbigla na lang\b", r"\bbasta na lang\b", r"\blang po\b", r"\bpo ba\b",
]

TAGALOG_MARKERS = {
    "ang", "ng", "sa", "na", "mga", "ko", "mo", "ako", "ka", "siya", "kami", "tayo", "kayo", "sila",
    "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung",
    "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "naman", "lang", "daw", "din", "rin",
    "may", "wala", "walang", "hindi", "ayaw", "trabaho", "sahod", "sweldo", "suweldo", "kaltas", "tanggal",
    "tinanggal", "tinanggalan", "sinibak", "pinaalis", "nagresign", "overtime", "buntis", "amo", "boss",
}

# FIX: was being recreated on every iteration of the query loop
COMPOUND_ENTITIES = [
    ("government employees",     "government_employees"),
    ("kawani ng gobyerno",       "government_employees"),
    ("empleyado ng gobyerno",    "government_employees"),
    ("civil service",            "civil_service"),
    ("pregnant employees",       "pregnant_employees"),
    ("pregnant workers",         "pregnant_employees"),
    ("probationary employees",   "probationary_employees"),
    ("probationary employment",  "probationary_employment"),
    ("regular employment",       "regular_employment"),
    ("separation pay",           "separation_pay"),
    ("13th month pay",           "13th_month_pay"),
    ("service incentive leave",  "service_incentive_leave"),
    ("night shift differential", "night_shift_differential"),
    ("illegal recruitment",      "illegal_recruitment"),
    ("constructive dismissal",   "constructive_dismissal"),
    ("security of tenure",       "security_of_tenure"),
]

STOPWORDS = {
    "ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila",
    "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po",
    "nga", "yung", "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "naman",
    "lang", "daw", "din", "rin",
    "a", "an", "the", "is", "are", "was", "were", "what", "who", "how", "when", "where",
    "why", "can", "could", "would", "should", "do", "does", "did", "i", "me", "my", "we",
    "you", "your", "it", "about", "and", "or", "of", "in", "on", "to", "for", "with",
    "he", "she", "him", "his", "her", "they", "them", "their", "this", "that", "these",
    "those", "be", "been", "being", "has", "have", "had", "by", "from", "as", "not", "no",
    "any", "all", "such", "shall", "may", "will", "upon", "under", "which", "whom", "other",
    "out", "into", "same", "some", "give", "given", "gave", "take", "took", "get", "got",
    "make", "made", "know", "knew", "ask", "asked", "tell", "told", "say", "said", "just",
    "like", "want", "went", "go", "off", "up", "down",
}


# ─────────────────────────────────────────────────────────────
# MODULE-LEVEL CACHES
# ─────────────────────────────────────────────────────────────

# Translation cache: avoids repeating Google Translate network calls
_translation_cache: dict = {}

# Query embedding cache: once a query is encoded by BGE-M3, the tensor is
# stored here.  Re-running evaluation with the SAME queries is instant.
_query_embedding_cache: dict = {}


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def clean_conversational_noise(text: str) -> str:
    cleaned = text.lower().replace('"', ' ').replace("'", " ")
    for pattern in CONVERSATIONAL_FILLERS:
        cleaned = re.sub(pattern, " ", cleaned)
    cleaned = cleaned.replace("-", " ")
    cleaned = re.sub(r'\b(\w{4,})ng\b', r'\1', cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def strip_filipino_affixes(word: str) -> str:
    w = word.lower()
    if len(w) <= 4:
        return w
    if len(w) > 4 and w[1:3] == 'in' and w[0] not in 'aeiou':
        w = w[0] + w[3:]
    if len(w) > 4 and w[1:3] == 'um' and w[0] not in 'aeiou':
        w = w[0] + w[3:]
    for pre in ['pinag', 'ipag', 'pina', 'nag', 'mag', 'pag']:
        if w.startswith(pre) and len(w) > len(pre) + 2:
            w = w[len(pre):]
            break
    if len(w) >= 6 and w[:2] == w[2:4]:
        w = w[2:]
    for suf in ['han', 'hin', 'an', 'in']:
        if w.endswith(suf) and len(w) > len(suf) + 3:
            w = w[:-len(suf)]
            break
    return w


# lru_cache avoids re-running langdetect on the same text
@lru_cache(maxsize=512)
def is_tagalog_or_taglish(text: str) -> bool:
    tokens = set(re.sub(r'[^\w\s]', '', text.lower()).split())
    if tokens & TAGALOG_MARKERS:
        return True
    try:
        detected = detect(text[:1000])
        return detected in ['tl', 'unknown', 'id', 'ms', 'sk', 'cy', 'hr']
    except Exception:
        return False


def calculate_rrf_scores(raw_scores, k: int = 60):
    ranks = np.empty_like(raw_scores)
    sorted_indices = np.argsort(-raw_scores)
    ranks[sorted_indices] = np.arange(1, len(raw_scores) + 1)
    return np.where(raw_scores > 0, 1.0 / (k + ranks), 0.0)


def build_vocab_index(vocabulary: set) -> dict:
    """Pre-index vocabulary by first letter: O(1) lookup instead of O(n) scan."""
    index: dict = {}
    for word in vocabulary:
        if word:
            index.setdefault(word[0], []).append(word)
    return index


# ── Translation helpers ───────────────────────────────────────

def _translate_one(text: str) -> str:
    """Translate a single text, hitting cache first."""
    if text in _translation_cache:
        return _translation_cache[text]
    try:
        result = GoogleTranslator(source='tl', target='en').translate(text) or ''
        _translation_cache[text] = result
        return result
    except Exception:
        _translation_cache[text] = ''
        return ''


def translate_batch_parallel(texts: List[str], max_workers: int = 8) -> List[str]:
    """
    Translate all texts in parallel using a thread pool.
    Already-cached texts are returned immediately without a network call.
    """
    results = [''] * len(texts)
    uncached_indices = [i for i, t in enumerate(texts) if t not in _translation_cache]

    # Everything is already cached — return instantly
    if not uncached_indices:
        return [_translation_cache.get(t, '') for t in texts]

    # Run uncached translations in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(_translate_one, texts[i]): i
            for i in uncached_indices
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception:
                results[idx] = ''

    # Fill cached results for the rest
    cached_indices = set(range(len(texts))) - set(uncached_indices)
    for i in cached_indices:
        results[i] = _translation_cache.get(texts[i], '')

    return results


# ── Query embedding helpers ───────────────────────────────────

def encode_queries_cached(encoder, queries: List[str], batch_size: int = 16) -> torch.Tensor:
    """
    Encode queries with BGE-M3, using a module-level cache.
    First run: encodes everything (slow — normal for a large model).
    Same queries on re-run: returns cached tensors INSTANTLY.
    """
    uncached = [q for q in queries if q not in _query_embedding_cache]
    if uncached:
        embeddings = encoder.encode(
            uncached,
            batch_size=batch_size,
            convert_to_tensor=True,
            show_progress_bar=False,
        )
        for q, emb in zip(uncached, embeddings):
            _query_embedding_cache[q] = emb

    return torch.stack([_query_embedding_cache[q] for q in queries])


# ─────────────────────────────────────────────────────────────
# MAIN EVALUATION FUNCTION
# ─────────────────────────────────────────────────────────────

def calculate_ir_metrics(search_engine, test_cases: List[TestCaseItem], k: int = 3) -> dict:
    evaluation_rows: list = []
    precision_list:  list = []
    recall_list:     list = []
    rr_list:         list = []

    # Build first-letter vocabulary index ONCE per call
    vocab_by_letter = build_vocab_index(search_engine.vocabulary)

    # ─── PHASE 1: PREPROCESS ALL QUERIES ─────────────────────
    processed_data:            list = []
    valid_queries_for_bge:     list = []
    tagalog_query_indices:     list = []   # indices in processed_data
    tagalog_texts_to_translate: list = []  # texts parallel to above

    for item in test_cases:
        raw_message   = item.query.strip()
        clean_message = clean_conversational_noise(raw_message)
        message_text  = clean_message.lower() if clean_message else raw_message.lower()

        # Direct article-number lookup
        article_num_match = re.search(
            r'\barticle\s+(\d+)\b|\bart\.?\s*(\d+)\b', raw_message.lower()
        )
        direct_article_index = None
        if article_num_match:
            target_num = article_num_match.group(1) or article_num_match.group(2)
            for idx, art_num in enumerate(getattr(search_engine, 'article_numbers', [])):
                m = re.search(r'\d+', art_num)
                if m and m.group() == target_num:
                    direct_article_index = idx
                    break

        # Synonym expansion
        expanded_keywords:  list = []
        clean_text_no_punct = re.sub(r'[^\w\s]', ' ', message_text)
        raw_words           = clean_text_no_punct.split()
        stemmed_words       = [strip_filipino_affixes(w) for w in raw_words]
        all_candidate_words = set(raw_words + stemmed_words)

        for term, english_terms in LEGAL_SYNONYMS.items():
            tl = term.lower()
            if " " in tl:
                if tl in message_text or tl in clean_text_no_punct:
                    expanded_keywords.extend(english_terms)
            else:
                if tl in all_candidate_words:
                    expanded_keywords.extend(english_terms)

        # Flag Tagalog queries for parallel translation later
        needs_translation = is_tagalog_or_taglish(message_text)
        if needs_translation:
            tagalog_query_indices.append(len(processed_data))
            tagalog_texts_to_translate.append(clean_text_no_punct)

        # Full query text (translation will be appended in Phase 1b)
        full_query_text = f"{message_text} {' '.join(expanded_keywords)}"
        lower_query     = full_query_text.lower()

        # Compound entity detection (module-level constant — not rebuilt each loop)
        detected_compounds = [
            bound_token
            for phrase, bound_token in COMPOUND_ENTITIES
            if phrase in lower_query
        ]

        # Token extraction & spell correction
        clean_full_query = re.sub(r'[^\w\s]', '', full_query_text)
        raw_tokens       = [
            w.lower() for w in clean_full_query.split()
            if (len(w) > 2 or w.isdigit()) and w.lower() not in STOPWORDS
        ]
        exact_tokens     = [t for t in raw_tokens if t in search_engine.vocabulary]
        corrected_tokens = list(exact_tokens)
        unmatched        = [t for t in raw_tokens if t not in search_engine.vocabulary]

        for t in unmatched:
            if t in TAGALOG_MARKERS or t in LEGAL_SYNONYMS:
                corrected_tokens.append(t)
                continue
            if len(t) <= 5:
                continue
            # O(V/26) lookup thanks to first-letter index
            candidates = vocab_by_letter.get(t[0], [])
            if not candidates:
                continue
            closest = min(candidates, key=lambda v: Levenshtein.distance(t, v))
            dist    = Levenshtein.distance(t, closest)
            if (len(t) <= 8 and dist == 1) or (len(t) >= 9 and dist <= 2):
                corrected_tokens.append(closest)

        corrected_tokens.extend(detected_compounds)

        if not corrected_tokens and direct_article_index is None:
            processed_data.append({
                "is_valid":           False,
                "item":               item,
                "needs_translation":  needs_translation,
                "clean_text_no_punct":clean_text_no_punct,
            })
        else:
            processed_data.append({
                "is_valid":            True,
                "item":                item,
                "corrected_tokens":    corrected_tokens,
                "direct_article_index":direct_article_index,
                "needs_translation":   needs_translation,
                "clean_text_no_punct": clean_text_no_punct,
                "full_query_text":     full_query_text,
            })

    # ─── PHASE 1b: PARALLEL TRANSLATION ──────────────────────
    if tagalog_texts_to_translate:
        translations = translate_batch_parallel(tagalog_texts_to_translate)
        for list_pos, proc_idx in enumerate(tagalog_query_indices):
            translation = translations[list_pos]
            if not translation:
                continue
            data = processed_data[proc_idx]
            if data.get("is_valid"):
                data["full_query_text"] = f"{data['full_query_text']} {translation}"
            else:
                data["_translation"] = translation

    # Rebuild corrected_tokens for Tagalog queries that received translations
    for proc_idx in tagalog_query_indices:
        data = processed_data[proc_idx]
        if not data.get("is_valid") or not data.get("full_query_text"):
            continue

        fq = data["full_query_text"]
        cq = re.sub(r'[^\w\s]', '', fq)
        rt = [
            w.lower() for w in cq.split()
            if (len(w) > 2 or w.isdigit()) and w.lower() not in STOPWORDS
        ]
        et = [t for t in rt if t in search_engine.vocabulary]
        ct = list(et)
        um = [t for t in rt if t not in search_engine.vocabulary]

        for t in um:
            if t in TAGALOG_MARKERS or t in LEGAL_SYNONYMS:
                ct.append(t)
                continue
            if len(t) <= 5:
                continue
            candidates = vocab_by_letter.get(t[0], [])
            if not candidates:
                continue
            closest = min(candidates, key=lambda v: Levenshtein.distance(t, v))
            dist    = Levenshtein.distance(t, closest)
            if (len(t) <= 8 and dist == 1) or (len(t) >= 9 and dist <= 2):
                ct.append(closest)

        lq = fq.lower()
        for phrase, bound_token in COMPOUND_ENTITIES:
            if phrase in lq:
                ct.append(bound_token)

        data["corrected_tokens"] = ct
        if ct:
            data["is_valid"] = True

    # Build final BGE query texts
    for data in processed_data:
        if data.get("is_valid"):
            valid_queries_for_bge.append(" ".join(data["corrected_tokens"]))

    # ─── PHASE 2: BATCH BGE-M3 ENCODING (CACHED) ─────────────
    # First run: slow (large model inference).
    # Repeat runs with same queries: INSTANT (tensor cache hit).
    all_embeddings = []
    if valid_queries_for_bge:
        encoder        = search_engine.get_bge_model()
        all_embeddings = encode_queries_cached(encoder, valid_queries_for_bge)

    # ─── PHASE 3: SCORING & EVALUATION ───────────────────────
    embedding_idx = 0

    for data in processed_data:
        item = data["item"]

        if not data["is_valid"]:
            evaluation_rows.append({
                "test_id":         item.test_id,
                "query":           item.query,
                "ground_truth":    item.expected_article,
                "retrieved_laws":  ["Query Rejected (No Valid Terms)"],
                "is_relevant":     "0 Found",
                "hit_rank":        "N/A",
                "precision_k":     "0.0%",
                "recall":          "0.0%",
                "reciprocal_rank": 0.0,
            })
            precision_list.append(0.0)
            recall_list.append(0.0)
            rr_list.append(0.0)
            continue

        corrected_tokens     = data["corrected_tokens"]
        direct_article_index = data["direct_article_index"]

        # BGE-M3 dense score (from cache)
        query_embedding = all_embeddings[embedding_idx].unsqueeze(0)
        embedding_idx  += 1
        bge_scores      = util.cos_sim(
            query_embedding, search_engine.bge_embeddings
        )[0].cpu().numpy()

        # BM25 lexical score
        bm25_scores = np.array(search_engine.bm25.get_scores(corrected_tokens))

        # Title boost
        title_boost     = np.zeros(len(search_engine.laws))
        query_token_set = set(corrected_tokens)
        vocab_idf       = getattr(search_engine, 'vocab_idf', {})
        if hasattr(search_engine, 'title_corpus'):
            for idx, title_text in enumerate(search_engine.title_corpus):
                matching = query_token_set & set(title_text.split())
                if matching:
                    title_boost[idx] = sum(vocab_idf.get(w, 1.0) for w in matching)

        # Reciprocal Rank Fusion
        bge_rrf      = calculate_rrf_scores(bge_scores)
        bm25_rrf     = calculate_rrf_scores(bm25_scores)
        title_rrf    = calculate_rrf_scores(title_boost)
        final_scores = bge_rrf + bm25_rrf + title_rrf

        # Build retrieved list
        retrieved_laws: list = []
        if direct_article_index is not None:
            retrieved_laws.append(search_engine.laws[direct_article_index])

        top_indices = np.argsort(final_scores)[::-1]
        for idx in top_indices:
            if len(retrieved_laws) >= k:
                break
            if direct_article_index is not None and idx == direct_article_index:
                continue
            if final_scores[idx] > 0.01 and bge_scores[idx] >= 0.35:
                doc_words = set(search_engine.corpus[idx].split())
                if query_token_set & doc_words:
                    retrieved_laws.append(search_engine.laws[idx])

        # Relevance matching
        targets        = [t.strip().lower() for t in item.expected_article.split(',')]
        total_expected = len(targets)
        relevant_count = 0
        first_match_rank = 0
        retrieved_labels: list = []

        for rank, law in enumerate(retrieved_laws, start=1):
            law_title       = f"{law.get('article', '')} {law.get('title', '')}".strip()
            retrieved_labels.append(law_title)
            law_title_lower   = law_title.lower()
            law_article_lower = (law.get('article') or '').lower()
            clean_article = re.sub(r'[^a-z0-9]', '', law_article_lower)
            clean_title   = re.sub(r'[^a-z0-9]', '', law_title_lower)
            is_match = False
            for target in targets:
                clean_target = re.sub(r'[^a-z0-9]', '', target.lower())
                if clean_target and (
                    clean_target in clean_article or clean_target in clean_title
                ):
                    is_match = True
                    break
                if target in law_title_lower or target in law_article_lower:
                    is_match = True
                    break
            if is_match:
                relevant_count += 1
                if first_match_rank == 0:
                    first_match_rank = rank

        total_k = len(retrieved_laws)
        p_at_k  = relevant_count / total_k  if total_k > 0 else 0.0
        recall  = min(relevant_count / total_expected, 1.0) if total_expected > 0 else 0.0
        rr      = 1.0 / first_match_rank if first_match_rank > 0 else 0.0

        precision_list.append(p_at_k)
        recall_list.append(recall)
        rr_list.append(rr)

        evaluation_rows.append({
            "test_id":         item.test_id,
            "query":           item.query,
            "ground_truth":    item.expected_article,
            "retrieved_laws":  retrieved_labels[:3] if retrieved_labels else ["None Found"],
            "is_relevant":     f"{relevant_count}/{total_expected} Found",
            "hit_rank":        first_match_rank if first_match_rank > 0 else "N/A",
            "precision_k":     f"{round(p_at_k  * 100, 1)}%",
            "recall":          f"{round(recall   * 100, 1)}%",
            "reciprocal_rank": round(rr, 3),
        })

    # ─── SUMMARY METRICS ─────────────────────────────────────
    macro_precision = np.mean(precision_list) if precision_list else 0.0
    macro_recall    = np.mean(recall_list)    if recall_list    else 0.0
    f1  = (
        2 * macro_precision * macro_recall / (macro_precision + macro_recall)
        if (macro_precision + macro_recall) > 0 else 0.0
    )
    mrr = np.mean(rr_list) if rr_list else 0.0

    return {
        "summary": {
            "macro_precision": f"{round(macro_precision * 100, 2)}%",
            "macro_recall":    f"{round(macro_recall    * 100, 2)}%",
            "f1_score":        f"{round(f1              * 100, 2)}%",
            "mrr":             round(mrr, 3),
            "total_tested":    len(test_cases),
        },
        "results_matrix": evaluation_rows,
    }