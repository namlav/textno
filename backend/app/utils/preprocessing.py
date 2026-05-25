import html
import re
from typing import Iterable


ENGLISH_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an",
    "and", "any", "are", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can", "did", "do",
    "does", "doing", "don", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers",
    "herself", "him", "himself", "his", "how", "i", "if", "in", "into",
    "is", "it", "its", "itself", "just", "me", "more", "most", "my",
    "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over",
    "own", "same", "she", "should", "so", "some", "such", "than", "that",
    "the", "their", "theirs", "them", "themselves", "then", "there",
    "these", "they", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "we", "were", "what", "when", "where",
    "which", "while", "who", "whom", "why", "will", "with", "you", "your",
    "yours", "yourself", "yourselves",
}

VIETNAMESE_STOPWORDS = {
    "và", "là", "của", "có", "được", "các", "với", "cho", "trong",
    "một", "người", "những", "khi", "như", "này", "đã", "sẽ", "số",
}

STOPWORDS = ENGLISH_STOPWORDS | VIETNAMESE_STOPWORDS


def clean_text(text: object, keep_digits: bool = False) -> str:
    if text is None:
        return ""

    text = html.unescape(str(text))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    if not keep_digits:
        text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_text(text: object, keep_digits: bool = False) -> str:
    return clean_text(str(text).lower(), keep_digits=keep_digits)


def tokenize(text: object) -> list[str]:
    normalized = normalize_text(text)
    return normalized.split()


def remove_stopwords(text: object, stopwords: Iterable[str] | None = None) -> str:
    words = str(text).split()
    stopword_set = set(stopwords or STOPWORDS)
    return " ".join(word for word in words if word not in stopword_set)


def preprocess(
    text: object,
    remove_stop_words: bool = True,
    keep_digits: bool = False,
) -> str:
    text = normalize_text(text, keep_digits=keep_digits)
    if remove_stop_words:
        text = remove_stopwords(text)
    return text
