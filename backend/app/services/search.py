# search.py - Tìm kiếm ngữ nghĩa dùng FAISS (Facebook AI Similarity Search)
#
# Kỹ thuật chính:
# - IndexFlatIP: FAISS index dùng Inner Product (tương đương Cosine Similarity vì vector đã chuẩn hoá)
# - Lazy Loading Singleton: index được load một lần từ file khi có request đầu tiên gọi đến
# - add_embedding / add_embeddings_batch: thêm vector vào index và tự động lưu xuống file
# - search(): nhúng query, tìm top_k vector gần nhất, trả về (id, score)

import os
import numpy as np
import faiss
from typing import Optional, List, Tuple
from app.core.config import settings
from app.services.embedding import generate_embedding

# Sử dụng biến _index làm bộ nhớ đệm tạm thời (Singleton)
_index: Optional[faiss.IndexFlatIP] = None


def get_index() -> faiss.IndexFlatIP:
    """Cơ chế Lazy Loading: Chỉ nạp file FAISS vào RAM khi được gọi đến"""
    global _index
    if _index is None:
        path = settings.FAISS_INDEX_PATH
        if os.path.exists(path):
            # Tải index có sẵn từ file phục vụ truy vấn
            _index = faiss.read_index(path)
        else:
            # Tạo index mới hoàn toàn nếu chưa có file dữ liệu
            _index = faiss.IndexFlatIP(settings.EMBEDDING_DIM)
    return _index


def save_index() -> None:
    """Ghi dữ liệu chỉ mục từ bộ nhớ RAM xuống ổ đĩa"""
    index = get_index()
    os.makedirs(os.path.dirname(settings.FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(index, settings.FAISS_INDEX_PATH)


def add_embedding(embedding: np.ndarray) -> int:
    """Thêm một vector đơn lẻ vào cấu trúc chỉ mục"""
    index = get_index()
    vec = embedding.reshape(1, -1).astype(np.float32)
    index.add(vec)
    embedding_id = index.ntotal - 1
    save_index()
    return embedding_id


def add_embeddings_batch(embeddings: np.ndarray) -> List[int]:
    """Thêm hàng loạt vector (Batch) vào cấu trúc chỉ mục phục vụ import lớn"""
    index = get_index()
    vecs = embeddings.astype(np.float32)
    start = index.ntotal
    index.add(vecs)
    embedding_ids = list(range(start, index.ntotal))
    save_index()
    return embedding_ids


def search(query: str, top_k: int = 5) -> List[Tuple[int, float]]:
    """Tìm kiếm ma trận vector tương đồng, trả về danh sách (embedding_id, score)"""
    index = get_index()
    if index.ntotal == 0:
        return []

    # Biến đổi câu query của người dùng thành vector 384 chiều
    query_vec = generate_embedding(query).reshape(1, -1).astype(np.float32)

    # Thực hiện truy vấn không gian Vector qua thư viện FAISS
    scores, indices = index.search(query_vec, top_k)

    results = []
    for i in range(len(indices[0])):
        idx = int(indices[0][i])
        if idx != -1:
            results.append((idx, float(scores[0][i])))
    return results


def rebuild_index(embeddings: np.ndarray) -> None:
    """Xóa bỏ chỉ mục cũ và thiết lập tái tạo lại toàn bộ ma trận từ đầu"""
    global _index
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    _index.add(embeddings.astype(np.float32))
    save_index()
