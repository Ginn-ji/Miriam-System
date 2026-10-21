import re
import numpy as np
import Levenshtein
from sklearn.metrics.pairwise import cosine_similarity

from synonyms import LEGAL_SYNONYMS
from core.nlp_utils import clean_conversational_noise, is_tagalog_or_taglish, strip_filipino_affixes

STOPWORDS = {
    "ang","ng","na","sa","at","ay","mga","ko","mo","siya","kami","kayo","sila",
    "ito","iyan","iyon","ano","sino","bakit","paano","kailan","saan","ba","po",
    "nga","yung","para","kung","pero","kasi","dahil","gusto","pwede","naman",
    "lang","daw","din","rin","a","an","the","is","are","was","were","what","who",
    "how","where","why","can","could","would","should","do","does","did",
    "i","me","my","we","you","your","it","about","and","or","of","in","on","to",
    "for","with","he","she","him","his","her","they","them","their","this","that",
    "these","those","be","been","being","has","have","had","by","from","as","not",
    "no","any","all","such","shall","may","will","upon","under","which","whom",
    "other","out","into","same","some","give","given","gave","take","took","get",
    "got","make","made","know","knew","ask","asked","tell","told","say","said",
    "just","like","want","went","go","off","up","down",
}

THEORETICAL_MAX_RRF = (1.0 / 61.0) * 4.0

DOMAIN_GATE_THRESHOLD = 0.45
# BGE-M3 per-document semantic threshold (gate 2)
BGE_GATE_THRESHOLD = 0.35
# Minimum meaningful RRF fusion score (gate 1)
RRF_GATE_THRESHOLD = 0.01
# Stage 1 (raw-query BGE-M3): how many top-scoring documents are kept as candidate pool
RAW_BGE_CANDIDATE_POOL = 30


def rrf(raw: np.ndarray, k: int = 60) -> np.ndarray:
    """Reciprocal Rank Fusion."""
    r = np.empty_like(raw)
    r[np.argsort(-raw)] = np.arange(1, len(raw) + 1)
    return np.where(raw > 0, 1.0 / (k + r), 0.0)


def build_vocab_index(vocabulary: set) -> dict:
    index: dict = {}
    for word in vocabulary:
        if word:
            index.setdefault(word[0], []).append(word)
    return index


def find_direct_article_index(raw_message: str, search_engine):
    """'Article 130' / 'Art. 130' style direct lookups."""
    art_match = re.search(r'\barticle\s+(\d+)\b|\bart\.?\s*(\d+)\b', raw_message.lower())
    if not art_match:
        return None
    target_num = art_match.group(1) or art_match.group(2)
    for i, num in enumerate(search_engine.article_numbers):
        m = re.search(r'\d+', num)
        if m and m.group() == target_num:
            return i
    return None


async def build_query_tokens(raw_message: str, search_engine, db, vocab_by_letter: dict) -> dict:
    clean_message = clean_conversational_noise(raw_message)
    message_text = clean_message.lower() if clean_message else raw_message.lower()

    dir_idx = find_direct_article_index(raw_message, search_engine)

    # Tagalog/Taglish: use DB translation cache only (no external API)
    search_text = message_text
    if is_tagalog_or_taglish(search_text):
        cached = await db.translation_cache.find_one({"query": re.sub(r'[^\w\s]', ' ', message_text)})
        if cached:
            search_text += f" {cached.get('translation', '')}"

    # Synonym expansion (with deduplication)
    expanded_keywords: list = []
    seen_expanded = set()
    clean_text_no_punct = re.sub(r'[^\w\s]', ' ', search_text)
    raw_words = clean_text_no_punct.split()
    stemmed_words = [strip_filipino_affixes(w) for w in raw_words]
    all_candidate_words = set(raw_words + stemmed_words)
    
    for term, english_terms in LEGAL_SYNONYMS.items():
        tl = term.lower()
        matched = False
        if " " in tl:
            if tl in search_text or tl in clean_text_no_punct:
                matched = True
        else:
            if tl in all_candidate_words:
                matched = True
        
        if matched:
            for eng in english_terms:
                if eng not in seen_expanded:
                    seen_expanded.add(eng)
                    expanded_keywords.append(eng)

    # Token extraction & spell correction
    full_query_text = f"{search_text} {' '.join(expanded_keywords)}"
    clean_full_query = re.sub(r'[^\w\s]', '', full_query_text)
    raw_tokens = [
        w.lower() for w in clean_full_query.split()
        if (len(w) > 2 or w.isdigit()) and w.lower() not in STOPWORDS
    ]
    exact_tokens = [t for t in raw_tokens if t in search_engine.vocabulary]
    corrected_tokens = list(exact_tokens)
    unmatched = [t for t in raw_tokens if t not in search_engine.vocabulary]

    for t in unmatched:
        if len(t) <= 5:
            continue
        candidates = vocab_by_letter.get(t[0], [])
        if not candidates:
            continue
        closest = min(candidates, key=lambda v: Levenshtein.distance(t, v))
        dist = Levenshtein.distance(t, closest)
        if (len(t) <= 8 and dist == 1) or (len(t) >= 9 and dist <= 2):
            corrected_tokens.append(closest)

    # Deduplicate corrected tokens while preserving order
    seen_tokens = set()
    unique_corrected_tokens = []
    for t in corrected_tokens:
        if t not in seen_tokens:
            seen_tokens.add(t)
            unique_corrected_tokens.append(t)

    return {
        "message_text": message_text,
        "dir_idx": dir_idx,
        "corrected_tokens": unique_corrected_tokens,
        "query_text": " ".join(unique_corrected_tokens),
    }


def score_and_gate(search_engine, corrected_tokens: list, dir_idx, bge_scores: np.ndarray) -> dict:
    total_laws = len(search_engine.laws)

    # 1. BM25 Lexical Retrieval (using preprocessed tokens)
    if search_engine.bm25 is not None and corrected_tokens:
        bm25_scores = np.array(search_engine.bm25.get_scores(corrected_tokens))
    else:
        bm25_scores = np.zeros(total_laws)

    # 2. TF-IDF Dense Cosine Similarity (using preprocessed query text)
    tfidf_scores = np.zeros(total_laws)
    if search_engine.vectorizer is not None and search_engine.tfidf_matrix is not None and corrected_tokens:
        query_text = " ".join(corrected_tokens)
        query_vec = search_engine.vectorizer.transform([query_text])
        tfidf_scores = cosine_similarity(query_vec, search_engine.tfidf_matrix).flatten()

    # 3. Title IDF Boost (using preprocessed tokens)
    title_boost = np.zeros(total_laws)
    q_set = set(corrected_tokens)
    for i, t_text in enumerate(search_engine.title_corpus):
        matching = q_set & set(t_text.split())
        if matching:
            title_boost[i] = sum(search_engine.vocab_idf.get(w, 1.0) for w in matching)

    # 4. Reciprocal Rank Fusion: BGE-M3 (raw) + BM25 (preprocessed) + TF-IDF (preprocessed) + Title Boost
    final_scores = rrf(bge_scores) + rrf(bm25_scores) + rrf(tfidf_scores) + rrf(title_boost)

    domain_gate_passed = float(np.max(bge_scores)) >= DOMAIN_GATE_THRESHOLD or dir_idx is not None

    ranked_indices: list = []
    if domain_gate_passed:
        top_indices = np.argsort(final_scores)[::-1]
        for idx in top_indices:
            if dir_idx is not None and idx == dir_idx:
                continue
            if final_scores[idx] <= RRF_GATE_THRESHOLD:
                continue
            if bge_scores[idx] < BGE_GATE_THRESHOLD:
                continue
            doc_words = set(search_engine.corpus[idx].split())
            if not (q_set & doc_words):
                continue
            ranked_indices.append(int(idx))

    return {
        "bm25_scores": bm25_scores,
        "tfidf_scores": tfidf_scores,
        "final_scores": final_scores,
        "domain_gate_passed": domain_gate_passed,
        "ranked_indices": ranked_indices,
    }


def raw_bge_stage1(raw_scores: np.ndarray, dir_idx, pool: int = RAW_BGE_CANDIDATE_POOL) -> dict:
    domain_gate_passed = float(np.max(raw_scores)) >= DOMAIN_GATE_THRESHOLD or dir_idx is not None

    candidates: list = []
    if domain_gate_passed:
        for idx in np.argsort(-raw_scores):
            if raw_scores[idx] < BGE_GATE_THRESHOLD:
                break  # sorted descending, so everything after is lower too
            candidates.append(int(idx))
            if len(candidates) >= pool:
                break

    return {
        "domain_gate_passed": domain_gate_passed,
        "candidate_indices": candidates,
    }


def restrict_to_candidates(ranked_indices: list, candidate_indices: list) -> list:
    allowed = set(candidate_indices)
    return [i for i in ranked_indices if i in allowed]