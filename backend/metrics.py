import re
import numpy as np
import torch
from sentence_transformers import util
from pydantic import BaseModel
from typing import List

from core.retrieval import (
    build_query_tokens,
    build_vocab_index,
    score_and_gate,
)

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
# MODULE-LEVEL STATE  (metrics-specific: batch BGE-M3 caching across
# many test cases at once — chat.py encodes one query at a time, so it
# doesn't need this; everything else is shared via core/retrieval.py)
# ─────────────────────────────────────────────────────────────

# Query embedding cache — same queries are instant on re-run
_query_embedding_cache: dict = {}


def encode_queries_cached(encoder, queries: List[str], batch_size: int = 16) -> torch.Tensor:
    """BGE-M3 with module-level cache — same queries are instant on re-run."""
    uncached = [q for q in queries if q not in _query_embedding_cache]
    if uncached:
        embeddings = encoder.encode(
            uncached, batch_size=batch_size,
            convert_to_tensor=True, show_progress_bar=False,
        )
        for q, emb in zip(uncached, embeddings):
            _query_embedding_cache[q] = emb
    return torch.stack([_query_embedding_cache[q] for q in queries])


# ─────────────────────────────────────────────────────────────
# MAIN EVALUATION FUNCTION
# ─────────────────────────────────────────────────────────────

async def calculate_ir_metrics(search_engine, test_cases: List[TestCaseItem], db, k: int = 3) -> dict:
    evaluation_rows: list = []
    precision_list:  list = []
    recall_list:     list = []
    rr_list:         list = []

    vocab_by_letter = search_engine.vocab_by_letter or build_vocab_index(search_engine.vocabulary)

    # ─── PHASE 1: PREPROCESS ALL QUERIES ─────────────────────
    # Shared logic (core/retrieval.build_query_tokens) — identical to chat.py:
    # conversational-noise cleaning, direct article lookup, Tagalog/Taglish
    # cached-translation lookup, synonym expansion, tokenization, spell correction.
    processed_data:        list = []
    valid_queries_for_bge: list = []

    for item in test_cases:
        raw_message = item.query.strip()
        tokens = await build_query_tokens(raw_message, search_engine, db, vocab_by_letter)
        corrected_tokens     = tokens["corrected_tokens"]
        direct_article_index = tokens["dir_idx"]

        if not corrected_tokens and direct_article_index is None:
            processed_data.append({"is_valid": False, "item": item})
        else:
            processed_data.append({
                "is_valid":            True,
                "item":                item,
                "corrected_tokens":    corrected_tokens,
                "direct_article_index": direct_article_index,
            })
            valid_queries_for_bge.append(tokens["query_text"])

    # ─── PHASE 2: BATCH BGE-M3 ENCODING (CACHED) ─────────────
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

        # BGE-M3 dense scores (already batch-encoded above)
        query_embedding = all_embeddings[embedding_idx].unsqueeze(0)
        embedding_idx  += 1
        bge_scores      = util.cos_sim(
            query_embedding, search_engine.bge_embeddings
        )[0].cpu().numpy()

        # BM25 + title boost + RRF fusion + domain gate + the 3 ranking gates
        # — shared logic (core/retrieval.score_and_gate), identical to chat.py
        scored = score_and_gate(search_engine, corrected_tokens, direct_article_index, bge_scores)

        retrieved_laws: list = []
        if direct_article_index is not None:
            retrieved_laws.append(search_engine.laws[direct_article_index])
        for idx in scored["ranked_indices"]:
            if len(retrieved_laws) >= k:
                break
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

    # ─── SUMMARY ─────────────────────────────────────────────
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