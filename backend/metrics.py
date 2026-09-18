import re
import numpy as np
from pydantic import BaseModel
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein
from langdetect import detect
from deep_translator import GoogleTranslator
import math

# Import synonyms just like the main server
from synonyms import LEGAL_SYNONYMS

# --- Pydantic Models ---
class TestCaseItem(BaseModel):
    test_id: str
    query: str
    expected_article: str

class ManualEvaluationRequest(BaseModel):
    test_cases: List[TestCaseItem]

# Cross-Encoder relevance threshold (synchronized with server.py)
CROSS_ENCODER_THRESHOLD = 0.0

# --- NLP Preprocessing Helpers (Synchronized with server.py) ---
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
    if len(w) > 4 and w[1:3] == "in" and w[0] not in "aeiou":
        w = w[0] + w[3:]
    if len(w) > 4 and w[1:3] == "um" and w[0] not in "aeiou":
        w = w[0] + w[3:]
    for pre in ["pinag", "ipag", "pina", "nag", "mag", "pag"]:
        if w.startswith(pre) and len(w) > len(pre) + 2:
            w = w[len(pre):]
            break
    if len(w) >= 6 and w[:2] == w[2:4]:
        w = w[2:]
    for suf in ["han", "hin", "an", "in"]:
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
    tokens = set(re.sub(r"[^\w\s]", "", text.lower()).split())
    if tokens & TAGALOG_MARKERS:
        return True
    try:
        detected = detect(text[:1000])
        return detected in ["tl", "unknown", "id", "ms", "sk", "cy", "hr"]
    except Exception:
        return False

# --- Core Logic ---
def calculate_ir_metrics(search_engine, test_cases: List[TestCaseItem], k: int = 3):
    precision_list = []
    recall_list = []
    rr_list = []

    stopwords = {
        "ang", "ng", "na", "sa", "at", "ay", "mga", "ko", "mo", "siya", "kami", "kayo", "sila", "ito", "iyan", "iyon", "ano", "sino", "bakit", "paano", "kailan", "saan", "ba", "po", "nga", "yung", "para", "kung", "pero", "kasi", "dahil", "gusto", "pwede", "naman", "lang", "daw", "din", "rin",
        "a", "an", "the", "is", "are", "was", "were", "what", "who", "how", "when", "where", "why", "can", "could", "would", "should", "do", "does", "did", "i", "me", "my", "we", "you", "your", "it", "about", "and", "or", "of", "in", "on", "to", "for", "with",
        "he", "she", "him", "his", "her", "they", "them", "their", "this", "that", "these", "those", "be", "been", "being", "has", "have", "had", "by", "from", "as", "not", "no", "any", "all", "such", "shall", "may", "will", "upon", "under", "which", "whom", "other", "out", "into", "same", "some",
        "give", "given", "gave", "take", "took", "get", "got", "make", "made", "know", "knew", "ask", "asked", "tell", "told", "say", "said", "just", "like", "want", "went", "go", "off", "up", "down"
    }

    # Cap vocabulary for Levenshtein to avoid O(vocab_size) per unmatched token.
    capped_vocab = list(search_engine.vocabulary)[:3000] if search_engine.vocabulary else []

    # -----------------------------------------------------------------------
    # PASS 1: Per-query scoring WITHOUT cross-encoder.
    # Collect candidate pairs from all queries into one flat list.
    # -----------------------------------------------------------------------
    intermediate = []

    for item in test_cases:
        raw_message = item.query.strip()
        clean_message = clean_conversational_noise(raw_message)
        message_text = clean_message.lower() if clean_message else raw_message.lower()

        # Step 0: Direct Article Number Lookup
        article_num_match = re.search(r"\barticle\s+(\d+)\b|\bart\.?\s*(\d+)\b", raw_message.lower())
        direct_article_index = None
        if article_num_match:
            direct_article_number = article_num_match.group(1) or article_num_match.group(2)
            if hasattr(search_engine, "article_numbers"):
                for idx, art_num in enumerate(search_engine.article_numbers):
                    stored_digits = re.search(r"\d+", art_num)
                    if stored_digits and stored_digits.group() == direct_article_number:
                        direct_article_index = idx
                        break

        # Step 1: Synonym & Concept Expansion
        expanded_keywords = []
        clean_text_no_punct = re.sub(r"[^\w\s]", " ", message_text)
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

        # Step 2: Language Detection & Translation
        # PERFORMANCE NOTE: GoogleTranslator makes a blocking HTTP call per query.
        # In the metrics evaluation path this adds seconds of latency per test case.
        # Synonym expansion already provides sufficient English coverage for evaluation,
        # so translation is intentionally skipped here. It still runs in server.py
        # for production chat.

        full_query_text = f"{search_text} {' '.join(expanded_keywords)}"
        clean_full_query = re.sub(r"[^\w\s]", "", full_query_text)

        # Step 3: Tokenization
        raw_tokens = [w.lower() for w in clean_full_query.split()
                      if (len(w) > 2 or w.isdigit()) and w.lower() not in stopwords]

        # Step 4: Vocabulary Matching & Levenshtein Correction (capped vocab)
        exact_tokens = [t for t in raw_tokens if t in search_engine.vocabulary]
        corrected_tokens = list(exact_tokens)
        unmatched = [t for t in raw_tokens if t not in search_engine.vocabulary]

        if exact_tokens and capped_vocab:
            for t in unmatched:
                if len(t) >= 4:
                    closest = min(capped_vocab, key=lambda v: Levenshtein.distance(t, v))
                    dist = Levenshtein.distance(t, closest)
                    if dist == 1 or (dist == 2 and len(t) >= 6):
                        corrected_tokens.append(closest)

        if not corrected_tokens and direct_article_index is None:
            intermediate.append({
                "test_id": item.test_id,
                "query": item.query,
                "ground_truth": item.expected_article,
                "retrieved_laws": ["Query Rejected (No Valid Terms)"],
                "is_relevant": "0 Found",
                "hit_rank": "N/A",
                "precision_k": "0.0%",
                "recall": "0.0%",
                "reciprocal_rank": 0.0,
            })
            precision_list.append(0.0)
            recall_list.append(0.0)
            rr_list.append(0.0)
            continue

        query_text_for_math = " ".join(corrected_tokens)

        # Step 5: Scoring (Cosine + BM25 + IDF-Weighted Title Boost)
        query_vec = search_engine.vectorizer.transform([query_text_for_math])
        cosine_scores = cosine_similarity(query_vec, search_engine.tfidf_matrix).flatten()
        bm25_scores = search_engine.bm25.get_scores(corrected_tokens)

        bm25_array = np.array(bm25_scores)
        if len(bm25_array) > 0 and np.max(bm25_array) > 0:
            bm25_min = np.min(bm25_array)
            bm25_max = np.max(bm25_array)
            if bm25_max == bm25_min:
                bm25_norm = np.zeros_like(bm25_array)
            else:
                bm25_norm = (bm25_array - bm25_min) / (bm25_max - bm25_min)
        else:
            bm25_norm = np.zeros_like(bm25_array)

        title_boost = np.zeros(len(search_engine.laws))
        query_token_set = set(corrected_tokens)
        vocab_idf = getattr(search_engine, "vocab_idf", {})
        if hasattr(search_engine, "title_corpus"):
            for idx, title_text in enumerate(search_engine.title_corpus):
                title_words = set(title_text.split())
                matching_title_words = query_token_set & title_words
                if matching_title_words:
                    title_boost[idx] = sum(vocab_idf.get(w, 1.0) for w in matching_title_words)

        tb_max = np.max(title_boost)
        title_boost_norm = title_boost / tb_max if tb_max > 0 else title_boost

        final_scores = (cosine_scores * 0.35) + (bm25_norm * 0.40) + (title_boost_norm * 0.25)

        # Step 6: Build candidate pairs list (cross-encoder deferred to PASS 2)
        direct_law = search_engine.laws[direct_article_index] if direct_article_index is not None else None

        top_15_indices = np.argsort(final_scores)[::-1][:15]
        candidate_pairs = []
        valid_candidate_indices = []

        for idx in top_15_indices:
            if direct_article_index is not None and idx == direct_article_index:
                continue
            if final_scores[idx] > 0.15:
                doc_words = set(search_engine.corpus[idx].split())
                if query_token_set & doc_words:
                    candidate_pairs.append([full_query_text, search_engine.corpus[idx]])
                    valid_candidate_indices.append(idx)

        intermediate.append({
            "test_id": item.test_id,
            "query": item.query,
            "ground_truth": item.expected_article,
            "_direct_law": direct_law,
            "_candidate_pairs": candidate_pairs,
            "_valid_candidate_indices": valid_candidate_indices,
            "_k": k,
        })

    # -----------------------------------------------------------------------
    # PASS 2: Batched cross-encoder scoring
    # All pairs from all queries are scored in a single encoder.predict() call.
    # This is dramatically faster than calling predict() once per query because:
    #   - The model loads and warms up only once.
    #   - All pairs benefit from batched matrix operations.
    # -----------------------------------------------------------------------
    all_pairs = []
    pair_offsets = []  # (row_dict, start_idx, end_idx)

    for row in intermediate:
        if "_candidate_pairs" not in row:
            continue
        start = len(all_pairs)
        all_pairs.extend(row["_candidate_pairs"])
        end = len(all_pairs)
        pair_offsets.append((row, start, end))

    all_ce_scores = None
    if all_pairs:
        try:
            encoder = search_engine.get_cross_encoder()
            all_ce_scores = encoder.predict(all_pairs)
        except Exception:
            all_ce_scores = None  # Fallback to BM25/cosine order

    # -----------------------------------------------------------------------
    # PASS 3: Resolve results using batched cross-encoder scores
    # -----------------------------------------------------------------------
    for row, start, end in pair_offsets:
        direct_law = row.pop("_direct_law")
        candidate_pairs = row.pop("_candidate_pairs")
        valid_candidate_indices = row.pop("_valid_candidate_indices")
        row_k = row.pop("_k")

        retrieved_laws = []
        if direct_law is not None:
            retrieved_laws.append(direct_law)

        if candidate_pairs:
            if all_ce_scores is not None:
                ce_scores = all_ce_scores[start:end]
                best_ce_indices = np.argsort(ce_scores)[::-1]
                for idx in best_ce_indices:
                    if len(retrieved_laws) >= row_k:
                        break
                    if float(ce_scores[idx]) < CROSS_ENCODER_THRESHOLD:
                        continue
                    original_idx = valid_candidate_indices[idx]
                    retrieved_laws.append(search_engine.laws[original_idx])
            else:
                for idx in valid_candidate_indices:
                    if len(retrieved_laws) >= row_k:
                        break
                    retrieved_laws.append(search_engine.laws[idx])

        # Step 7: Smart Ground Truth Matching
        targets = [t.strip().lower() for t in row["ground_truth"].split(",")]
        total_expected = len(targets)

        relevant_count = 0
        first_match_rank = 0
        retrieved_labels = []

        for rank, law in enumerate(retrieved_laws, start=1):
            law_title = f"{law.get('article', '')} {law.get('title', '')}".strip()
            retrieved_labels.append(law_title)

            law_article_str = law.get("article", "")
            law_article_digit = re.search(r"\d+", law_article_str)
            law_article_num = law_article_digit.group() if law_article_digit else ""

            is_match = False
            for target in targets:
                target_digit = re.search(r"\d+", target)
                target_num = target_digit.group() if target_digit else ""

                if target_num and law_article_num and target_num == law_article_num:
                    is_match = True
                    break

                if target in law_title.lower():
                    is_match = True
                    break

            if is_match:
                relevant_count += 1
                if first_match_rank == 0:
                    first_match_rank = rank

        total_k = len(retrieved_laws)
        p_at_k = (relevant_count / total_k) if total_k > 0 else 0.0
        recall = min((relevant_count / total_expected), 1.0) if total_expected > 0 else 0.0
        rr = (1.0 / first_match_rank) if first_match_rank > 0 else 0.0

        precision_list.append(p_at_k)
        recall_list.append(recall)
        rr_list.append(rr)

        row.update({
            "retrieved_laws": retrieved_labels[:3] if retrieved_labels else ["None Found"],
            "is_relevant": f"{relevant_count}/{total_expected} Found",
            "hit_rank": first_match_rank if first_match_rank > 0 else "N/A",
            "precision_k": f"{round(p_at_k * 100, 1)}%",
            "recall": f"{round(recall * 100, 1)}%",
            "reciprocal_rank": round(rr, 3),
        })

    # Re-order rows to match original test-case order
    row_by_id = {r["test_id"]: r for r in intermediate}
    results_matrix = [row_by_id[item.test_id] for item in test_cases if item.test_id in row_by_id]

    # Macro Averages
    macro_precision = np.mean(precision_list) if precision_list else 0.0
    macro_recall = np.mean(recall_list) if recall_list else 0.0
    f1 = (
        2 * macro_precision * macro_recall / (macro_precision + macro_recall)
        if (macro_precision + macro_recall) > 0 else 0.0
    )
    mrr = np.mean(rr_list) if rr_list else 0.0

    return {
        "summary": {
            "macro_precision": f"{round(macro_precision * 100, 2)}%",
            "macro_recall": f"{round(macro_recall * 100, 2)}%",
            "f1_score": f"{round(f1 * 100, 2)}%",
            "mrr": round(mrr, 3),
            "total_tested": len(test_cases),
        },
        "results_matrix": results_matrix,
    }
