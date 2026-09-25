"""
core/retrieval.py

Single source of truth for the Labor Code retrieval logic.

Both chat.py (live user queries) and metrics.py (offline evaluation) call into
this module for the actual query-processing and scoring math, so the two can
never silently drift apart again. Each file only owns what's specific to its
own job:
  - chat.py:    encodes one query at a time, builds best_match_chunk/accuracy%,
                saves chat history.
  - metrics.py: batches + caches BGE embeddings across many test cases for
                speed, then compares retrieved articles against ground truth
                to compute precision/recall/MRR. None of that changes here —
                it just stops duplicating the retrieval math.
"""
import re
import numpy as np
import Levenshtein

from synonyms import LEGAL_SYNONYMS
from core.nlp_utils import clean_conversational_noise, is_tagalog_or_taglish, strip_filipino_affixes

STOPWORDS = {
    "ang","ng","na","sa","at","ay","mga","ko","mo","siya","kami","kayo","sila",
    "ito","iyan","iyon","ano","sino","bakit","paano","kailan","saan","ba","po",
    "nga","yung","para","kung","pero","kasi","dahil","gusto","pwede","naman",
    "lang","daw","din","rin","a","an","the","is","are","was","were","what","who",
    "how","when","where","why","can","could","would","should","do","does","did",
    "i","me","my","we","you","your","it","about","and","or","of","in","on","to",
    "for","with","he","she","him","his","her","they","them","their","this","that",
    "these","those","be","been","being","has","have","had","by","from","as","not",
    "no","any","all","such","shall","may","will","upon","under","which","whom",
    "other","out","into","same","some","give","given","gave","take","took","get",
    "got","make","made","know","knew","ask","asked","tell","told","say","said",
    "just","like","want","went","go","off","up","down",
}

# Theoretical max RRF: all 3 channels (BGE-M3 + BM25 + Title Boost) ranked #1
# = 3 × (1/61) = 0.04918 — same constant the old server.py used
THEORETICAL_MAX_RRF = (1.0 / 61.0) * 3.0

# BGE-M3 domain-relevance gate: top score must reach this for the query to be
# considered "about Labor Law" at all (unless it's a direct article lookup)
DOMAIN_GATE_THRESHOLD = 0.45
# BGE-M3 per-document semantic threshold (gate 2)
BGE_GATE_THRESHOLD = 0.35
# Minimum meaningful RRF fusion score (gate 1)
RRF_GATE_THRESHOLD = 0.01


def rrf(raw: np.ndarray, k: int = 60) -> np.ndarray:
    """Reciprocal Rank Fusion."""
    r = np.empty_like(raw)
    r[np.argsort(-raw)] = np.arange(1, len(raw) + 1)
    return np.where(raw > 0, 1.0 / (k + r), 0.0)


def build_vocab_index(vocabulary: set) -> dict:
    """First-letter -> [words] index, so spell-correction candidate lookup
    doesn't rescan the whole vocabulary for every unmatched token."""
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
    """
    Full text-processing pipeline: conversational-noise cleaning -> direct
    article lookup -> Tagalog/Taglish cached-translation lookup -> synonym
    expansion -> tokenization -> spell correction.

    Returns:
        {
            "message_text":      cleaned/lowercased query text,
            "dir_idx":           direct article index or None,
            "corrected_tokens":  final token list used for scoring,
            "query_text":        " ".join(corrected_tokens), ready to encode,
        }
    """
    clean_message = clean_conversational_noise(raw_message)
    message_text = clean_message.lower() if clean_message else raw_message.lower()

    dir_idx = find_direct_article_index(raw_message, search_engine)

    # Tagalog/Taglish: use DB translation cache only (no external API)
    search_text = message_text
    if is_tagalog_or_taglish(search_text):
        cached = await db.translation_cache.find_one({"query": re.sub(r'[^\w\s]', ' ', message_text)})
        if cached:
            search_text += f" {cached.get('translation', '')}"

    # Synonym expansion
    expanded_keywords: list = []
    clean_text_no_punct = re.sub(r'[^\w\s]', ' ', search_text)
    raw_words = clean_text_no_punct.split()
    stemmed_words = [strip_filipino_affixes(w) for w in raw_words]
    all_candidate_words = set(raw_words + stemmed_words)
    for term, english_terms in LEGAL_SYNONYMS.items():
        tl = term.lower()
        if " " in tl:
            if tl in search_text or tl in clean_text_no_punct:
                expanded_keywords.extend(english_terms)
        else:
            if tl in all_candidate_words:
                expanded_keywords.extend(english_terms)

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

    return {
        "message_text": message_text,
        "dir_idx": dir_idx,
        "corrected_tokens": corrected_tokens,
        "query_text": " ".join(corrected_tokens),
    }


def score_and_gate(search_engine, corrected_tokens: list, dir_idx, bge_scores: np.ndarray) -> dict:
    """
    Given a precomputed bge_scores array (query vs. search_engine.bge_embeddings),
    runs BM25 + title-boost scoring, RRF fusion, the domain gate, and the 3
    per-document gates. Identical math for both chat.py and metrics.py.

    Deliberately does NOT cap the number of results here: the caller is the
    one who knows whether a direct-article-number hit already occupies a slot
    (chat.py/metrics.py both add that first, separately), so each caller does
    its own `if len(results) >= limit: break` while consuming ranked_indices —
    capping in both places at once would double-count that slot.

    Returns:
        {
            "bm25_scores":         np.ndarray,
            "final_scores":        np.ndarray (RRF-fused),
            "domain_gate_passed":  bool,
            "ranked_indices":      [int, ...] gated + ranked, excludes dir_idx,
        }
    """
    bm25_scores = np.array(search_engine.bm25.get_scores(corrected_tokens))

    title_boost = np.zeros(len(search_engine.laws))
    q_set = set(corrected_tokens)
    for i, t_text in enumerate(search_engine.title_corpus):
        matching = q_set & set(t_text.split())
        if matching:
            title_boost[i] = sum(search_engine.vocab_idf.get(w, 1.0) for w in matching)

    final_scores = rrf(bge_scores) + rrf(bm25_scores) + rrf(title_boost)

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
        "final_scores": final_scores,
        "domain_gate_passed": domain_gate_passed,
        "ranked_indices": ranked_indices,
    }