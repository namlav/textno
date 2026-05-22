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
    model = get_model()
    return model.encode(text, normalize_embeddings=True)


def generate_embeddings_batch(texts: list[str]) -> np.ndarray:
    model = get_model()
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
