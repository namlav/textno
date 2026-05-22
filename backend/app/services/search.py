import os
import numpy as np
import faiss
from typing import Optional
from app.core.config import settings
from app.services.embedding import generate_embedding

_index: Optional[faiss.IndexFlatIP] = None


def get_index() -> faiss.IndexFlatIP:
    global _index
    if _index is None:
        path = settings.FAISS_INDEX_PATH
        if os.path.exists(path):
            _index = faiss.read_index(path)
        else:
            _index = faiss.IndexFlatIP(settings.EMBEDDING_DIM)
    return _index


def save_index():
    index = get_index()
    os.makedirs(os.path.dirname(settings.FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(index, settings.FAISS_INDEX_PATH)


def add_embedding(embedding: np.ndarray) -> int:
    index = get_index()
    vec = embedding.reshape(1, -1).astype(np.float32)
    index.add(vec)
    embedding_id = index.ntotal - 1
    save_index()
    return embedding_id


def add_embeddings_batch(embeddings: np.ndarray) -> list[int]:
    index = get_index()
    vecs = embeddings.astype(np.float32)
    start = index.ntotal
    index.add(vecs)
    embedding_ids = list(range(start, index.ntotal))
    save_index()
    return embedding_ids


def search(query: str, top_k: int = 5) -> list[tuple[int, float]]:
    index = get_index()
    if index.ntotal == 0:
        return []
    query_vec = generate_embedding(query).reshape(1, -1).astype(np.float32)
    scores, indices = index.search(query_vec, top_k)
    results = []
    for i in range(len(indices[0])):
        idx = int(indices[0][i])
        if idx != -1:
            results.append((idx, float(scores[0][i])))
    return results


def rebuild_index(embeddings: np.ndarray):
    global _index
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    _index.add(embeddings.astype(np.float32))
    save_index()
