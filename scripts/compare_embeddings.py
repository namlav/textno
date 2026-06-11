# compare_embeddings.py - So sánh kết quả tìm kiếm giữa TF-IDF và BERT (SBERT)
#
# Kỹ thuật:
# - TF-IDF: vectorizer sklearn với ngram_range=(1,2), max_features=50000
# - BERT: SentenceTransformer với model đa ngôn ngữ
# - Cosine Similarity: dùng sklearn.metrics.pairwise.cosine_similarity
# - So sánh top_k kết quả cho mỗi query, hiển thị title để đánh giá trực quan
#
# Mục đích: chứng minh semantic search (BERT) hiểu ngữ nghĩa hơn keyword search (TF-IDF)

import argparse

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_QUERIES = [
    "du lịch mở cửa sau Covid",
    "giá cổ phiếu và kinh doanh",
    "bóng đá đội tuyển Việt Nam",
    "học sinh đi học trở lại",
    "công nghệ điện thoại mới",
]


def build_bert_texts(df: pd.DataFrame, bert_text_column: str | None) -> list[str]:
    if bert_text_column and bert_text_column in df.columns:
        return df[bert_text_column].astype(str).tolist()
    return (df["title"].astype(str) + ". " + df["content"].astype(str)).tolist()


def top_results(scores: np.ndarray, df: pd.DataFrame, top_k: int) -> list[str]:
    indexes = scores.argsort()[::-1][:top_k]
    return [str(df.iloc[index]["title"]) for index in indexes]


def compare_embeddings(
    csv_path: str,
    tfidf_text_column: str,
    bert_text_column: str | None,
    bert_model_name: str,
    top_k: int,
) -> None:
    df = pd.read_csv(csv_path).fillna("")
    df = df[df[tfidf_text_column].astype(str).str.len() > 0].reset_index(drop=True)

    tfidf_texts = df[tfidf_text_column].astype(str).tolist()
    bert_texts = build_bert_texts(df, bert_text_column)

    vectorizer = TfidfVectorizer(max_features=50000, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(tfidf_texts)

    print(f"Loaded {len(df)} documents")
    print(f"Building BERT/SentenceTransformer embeddings with {bert_model_name}...")
    bert_model = SentenceTransformer(bert_model_name)
    bert_matrix = bert_model.encode(bert_texts, normalize_embeddings=True, show_progress_bar=True)

    for query in DEFAULT_QUERIES:
        tfidf_query = vectorizer.transform([query])
        tfidf_scores = cosine_similarity(tfidf_query, tfidf_matrix).ravel()

        bert_query = bert_model.encode([query], normalize_embeddings=True)
        bert_scores = cosine_similarity(bert_query, bert_matrix).ravel()

        print(f"\nQuery: {query}")
        print("TF-IDF:")
        for title in top_results(tfidf_scores, df, top_k):
            print(f"- {title}")
        print("BERT:")
        for title in top_results(bert_scores, df, top_k):
            print(f"- {title}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare TF-IDF and BERT search results.")
    parser.add_argument("csv_path", nargs="?", default="data/processed/cleaned.csv")
    parser.add_argument("--tfidf-text-column", default="text_for_embedding")
    parser.add_argument("--bert-text-column", default=None)
    parser.add_argument("--bert-model", default="paraphrase-multilingual-MiniLM-L12-v2")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    compare_embeddings(
        args.csv_path,
        args.tfidf_text_column,
        args.bert_text_column,
        args.bert_model,
        args.top_k,
    )
