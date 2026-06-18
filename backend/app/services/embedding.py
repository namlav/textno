# embedding.py - Sinh vector embedding từ văn bản dùng SentenceTransformer
#
# Kỹ thuật:
# - Dùng SentenceTransformer với model đa ngôn ngữ (mặc định: paraphrase-multilingual-MiniLM-L12-v2)
# - normalize_embeddings=True: chuẩn hoá vector về độ dài 1 đơn vị để dùng Cosine Similarity = Inner Product
# - Lazy loading: model chỉ load một lần (singleton), tránh tốn RAM/VRAM
# - Hỗ trợ batch: generate_embeddings_batch() xử lý hàng loạt với progress bar

import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import settings

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def generate_embedding(text: str) -> np.ndarray:
    # Sinh vector embedding cho một văn bản đơn lẻ
    # normalize_embeddings=True giúp FAISS Inner Product hoạt động như Cosine Similarity
    model = get_model()
    return model.encode(text, normalize_embeddings=True)


def generate_embeddings_batch(texts: list[str], batch_size: int = 256) -> np.ndarray:
    # Sinh vector embedding hàng loạt, hiệu quả hơn gọi từng cái một
    # show_progress_bar=True: hiển thị tiến trình cho dữ liệu lớn
    model = get_model()
    return model.encode(
        texts, batch_size=batch_size, normalize_embeddings=True, show_progress_bar=True
    )
