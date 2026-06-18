import logging
import numpy as np
from bson import ObjectId
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional

from app.database.mongodb import get_collection

logger = logging.getLogger(__name__)

_vectorizer: Optional[TfidfVectorizer] = None
_tfidf_matrix: Optional[csr_matrix] = None
_doc_ids: list[str] = []
_last_doc_count: int = -1


def _rebuild_index():
    global _vectorizer, _tfidf_matrix, _doc_ids, _last_doc_count
    collection = get_collection()
    logger.info("Rebuilding TF-IDF index from MongoDB...")

    total = collection.count_documents({})
    if total == 0:
        _vectorizer = None
        _tfidf_matrix = None
        _doc_ids = []
        _last_doc_count = 0
        logger.info("No documents found, TF-IDF index is empty.")
        return

    texts = []
    _doc_ids = []
    batch_size = 5000
    for i in range(0, total, batch_size):
        batch = list(collection.find({}, {"title": 1, "content": 1}).skip(i).limit(batch_size))
        for doc in batch:
            text = f"{doc.get('title', '')} {doc.get('content', '')}"
            texts.append(text)
            _doc_ids.append(str(doc["_id"]))
        logger.info(f"  Loaded {min(i + batch_size, total)}/{total} documents...")

    logger.info(f"Fitting TfidfVectorizer on {len(texts)} documents...")
    _vectorizer = TfidfVectorizer(max_features=50000, ngram_range=(1, 2))
    _tfidf_matrix = _vectorizer.fit_transform(texts)
    _last_doc_count = len(texts)
    logger.info("TF-IDF index rebuilt successfully.")


def _ensure_index():
    collection = get_collection()
    current_count = collection.count_documents({})
    if (
        _vectorizer is None
        or _tfidf_matrix is None
        or current_count != _last_doc_count
    ):
        _rebuild_index()


def _safe_str(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, list):
        return ",".join(str(v) for v in value)
    if not isinstance(value, str):
        return str(value)
    return value


def _safe_int(value) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def search(query: str, top_k: int = 5) -> list[dict]:
    _ensure_index()
    if _vectorizer is None or _tfidf_matrix is None:
        return []

    query_vec = _vectorizer.transform([query])
    scores = cosine_similarity(query_vec, _tfidf_matrix).ravel()

    top_indices = scores.argsort()[::-1][:top_k]

    doc_ids_to_fetch = [_doc_ids[idx] for idx in top_indices if idx < len(_doc_ids)]
    if not doc_ids_to_fetch:
        return []

    collection = get_collection()
    doc_map = {}
    for doc in collection.find({"_id": {"$in": [ObjectId(did) for did in doc_ids_to_fetch]}}):
        doc_map[str(doc["_id"])] = doc

    results = []
    for idx in top_indices:
        if idx < len(_doc_ids):
            doc = doc_map.get(_doc_ids[idx])
            if doc:
                results.append({
                    "id": str(doc["_id"]),
                    "title": doc.get("title", "") or "",
                    "content": doc.get("content", "") or "",
                    "category": _safe_str(doc.get("category")),
                    "author": _safe_str(doc.get("author")),
                    "publication": _safe_str(doc.get("publication")),
                    "tags": _safe_str(doc.get("tags")),
                    "created_at": doc.get("created_at"),
                    "wordcount": _safe_int(doc.get("wordcount")),
                    "score": float(scores[idx]),
                })
    return results


def get_vocabulary_size() -> int:
    _ensure_index()
    if _vectorizer is None:
        return 0
    return len(_vectorizer.get_feature_names_out())


def get_keyword_overlap(query: str, doc_id: str) -> dict:
    _ensure_index()
    if _vectorizer is None:
        return {"query_terms": 0, "matched_terms": 0, "matched_words": []}

    query_terms = set(_vectorizer.build_tokenizer()(query.lower()))
    query_terms = {t for t in query_terms if t in _vectorizer.get_feature_names_out()}

    collection = get_collection()
    doc = collection.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        return {"query_terms": len(query_terms), "matched_terms": 0, "matched_words": []}

    doc_text = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
    doc_terms = set(_vectorizer.build_tokenizer()(doc_text))
    doc_terms = {t for t in doc_terms if t in _vectorizer.get_feature_names_out()}

    matched = query_terms & doc_terms
    return {
        "query_terms": len(query_terms),
        "matched_terms": len(matched),
        "matched_words": sorted(matched),
    }
