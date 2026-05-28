import html
import re
from typing import Iterable


STOPWORDS = {
    "và", "là", "của", "có", "được", "các", "với", "cho", "trong",
    "một", "người", "những", "khi", "như", "này", "đã", "sẽ", "số",
    "về", "từ", "đến", "theo", "tại", "trên", "dưới", "sau", "trước",
    "nhiều", "rằng", "thì", "mà", "để", "do", "vì", "nên", "cũng",
    "ra", "vào", "lại", "hơn", "rất", "bị", "đang", "năm", "ngày",
    "không", "nói", "biết", "hay", "nhưng", "đó", "đây", "nơi",
    "the", "is", "and", "to", "of", "in", "that", "for", "it", "on",
    "this", "with", "are", "was", "were", "been", "being",
}


def clean_text(text: str) -> str:
    if text is None:
        return ""
    text = html.unescape(str(text))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_text(text: str) -> str:
    return clean_text(text).lower()


def tokenize(text: str) -> list[str]:
    return [word for word in normalize_text(text).split() if word]


def remove_stopword_tokens(tokens: Iterable[str]) -> list[str]:
    return [word for word in tokens if word not in STOPWORDS and len(word) > 1]


def remove_stopwords(text: str) -> str:
    return " ".join(remove_stopword_tokens(text.split()))


def preprocess(text: str) -> str:
    return " ".join(remove_stopword_tokens(tokenize(text)))
