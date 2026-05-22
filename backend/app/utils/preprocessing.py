import re
import html


STOPWORDS = {
    "và", "là", "của", "có", "được", "các", "với", "cho", "trong",
    "một", "người", "những", "khi", "như", "này", "đã", "sẽ", "số",
    "the", "is", "and", "to", "of", "in", "that", "for", "it", "on",
    "this", "with", "are", "was", "were", "been", "being",
}


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def normalize_text(text: str) -> str:
    text = text.lower()
    text = clean_text(text)
    return text


def remove_stopwords(text: str) -> str:
    words = text.split()
    words = [w for w in words if w not in STOPWORDS]
    return " ".join(words)


def preprocess(text: str) -> str:
    text = normalize_text(text)
    text = remove_stopwords(text)
    return text
