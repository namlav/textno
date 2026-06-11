# preprocessing.py - Tiền xử lý văn bản tiếng Việt cho NLP pipeline
#
# Pipeline xử lý:
#   1. clean_text():   Giải mã HTML, xoá thẻ HTML, URL, ký tự đặc biệt, khoảng trắng thừa
#   2. normalize_text(): lowercased + clean
#   3. tokenize():      Tách từ đơn (word tokenization) từ text đã chuẩn hoá
#   4. remove_stopwords(): Lọc bỏ stopwords (cả tiếng Việt và tiếng Anh)
#   5. preprocess():    Pipeline hoàn chỉnh: clean -> tokenize -> remove stopwords
#
# Kỹ thuật:
# - Regex-based: dùng re.sub cho HTML, URL, punctuation (đủ nhanh cho tiếng Việt)
# - STOPWORDS: kết hợp stopwords tiếng Việt phổ biến + tiếng Anh (phòng trường hợp dữ liệu lai)
# - Tokenization: đơn giản dùng split() thay vì underthesea/VnCoreNLP (giảm dependency)

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
    # HTML unescape: &amp; -> &, &lt; -> <
    if text is None:
        return ""
    text = html.unescape(str(text))
    text = re.sub(r"<[^>]+>", " ", text)       # Xoá thẻ HTML
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)  # Xoá URL
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)  # Xoá punctuation
    text = re.sub(r"\s+", " ", text)            # Chuẩn hoá khoảng trắng
    return text.strip()


def normalize_text(text: str) -> str:
    # lowercase + clean
    return clean_text(text).lower()


def tokenize(text: str) -> list[str]:
    # Tokenization đơn giản bằng split (phù hợp cho tiếng Việt viết liền không dấu cách)
    return [word for word in normalize_text(text).split() if word]


def remove_stopword_tokens(tokens: Iterable[str]) -> list[str]:
    # Lọc token: bỏ stopword và token 1 ký tự (thường là ký tự thừa)
    return [word for word in tokens if word not in STOPWORDS and len(word) > 1]


def remove_stopwords(text: str) -> str:
    # Xoá stopwords từ text đã tokenize
    return " ".join(remove_stopword_tokens(text.split()))


def preprocess(text: str) -> str:
    # Pipeline hoàn chỉnh: làm sạch -> tokenize -> loại stopword
    return " ".join(remove_stopword_tokens(tokenize(text)))
