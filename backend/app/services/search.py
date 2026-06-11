# search.py - Tìm kiếm ngữ nghĩa dùng FAISS (Facebook AI Similarity Search)
#
# Kỹ thuật chính:
# - IndexFlatIP: FAISS index dùng Inner Product (tương đương Cosine Similarity vì vector đã chuẩn hoá)
# - Singleton: index được load một lần từ file (nếu có) hoặc tạo mới
# - add_embedding / add_embeddings_batch: thêm vector vào index và tự động lưu xuống file
# - search(): nhúng query, tìm top_k vector gần nhất, trả về (id, score)
# - rebuild_index(): tạo lại index từ đầu, dùng khi import dữ liệu lớn
#
# Lưu ý:
# - embedding_id là vị trí của vector trong FAISS index (0, 1, 2, ...)
# - Mapping embedding_id <-> document MongoDB thực hiện ở routes.py

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
            # Load index có sẵn từ file (phục hồi sau khi restart)
            _index = faiss.read_index(path)
        else:
            # Tạo index mới với số chiều từ config
            _index = faiss.IndexFlatIP(settings.EMBEDDING_DIM)
    return _index


def save_index():
    # Ghi FAISS index xuống file để dùng lại sau khi restart server
    index = get_index()
    os.makedirs(os.path.dirname(settings.FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(index, settings.FAISS_INDEX_PATH)


def add_embedding(embedding: np.ndarray) -> int:
    # Thêm một vector vào index, trả về embedding_id (vị trí trong index)
    index = get_index()
    vec = embedding.reshape(1, -1).astype(np.float32)
    index.add(vec)
    embedding_id = index.ntotal - 1
    save_index()
    return embedding_id


def add_embeddings_batch(embeddings: np.ndarray) -> list[int]:
    # Thêm batch vector vào index, hiệu quả hơn add từng cái
    index = get_index()
    vecs = embeddings.astype(np.float32)
    start = index.ntotal
    index.add(vecs)
    embedding_ids = list(range(start, index.ntotal))
    save_index()
    return embedding_ids


def search(query: str, top_k: int = 5) -> list[tuple[int, float]]:
    # Tìm kiếm: nhúng câu query, so sánh với toàn bộ vector trong index
    # Trả về list (embedding_id, score) với score cao nhất trước
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
    # Tạo lại index từ đầu, xoá index cũ
    # Dùng khi import dữ liệu lớn (xem generate_embeddings.py)
    global _index
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    _index.add(embeddings.astype(np.float32))
    save_index()
