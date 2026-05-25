import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def genre_set(value: object) -> set[str]:
    return {
        item.strip().lower()
        for item in str(value).split(";")
        if item.strip()
    }


def genre_overlap_score(query_genres: set[str], result_genres: set[str]) -> float:
    if not query_genres or not result_genres:
        return 0.0
    return len(query_genres & result_genres) / len(query_genres | result_genres)


def evaluate_neighbors(
    vectors: np.ndarray,
    df: pd.DataFrame,
    query_count: int,
    top_k: int,
) -> tuple[float, float]:
    query_count = min(query_count, len(df))
    query_vectors = vectors[:query_count]

    start = time.perf_counter()
    similarities = cosine_similarity(query_vectors, vectors)
    elapsed = time.perf_counter() - start

    scores: list[float] = []
    for row_idx in range(query_count):
        ranking = np.argsort(similarities[row_idx])[::-1]
        ranking = [idx for idx in ranking if idx != row_idx][:top_k]
        query_genres = genre_set(df.iloc[row_idx]["genres"])
        row_scores = [
            genre_overlap_score(query_genres, genre_set(df.iloc[idx]["genres"]))
            for idx in ranking
        ]
        scores.append(float(np.mean(row_scores)) if row_scores else 0.0)

    avg_latency_ms = (elapsed / query_count) * 1000 if query_count else 0.0
    return float(np.mean(scores)) if scores else 0.0, avg_latency_ms


def run_tfidf(texts: list[str], max_features: int) -> tuple[np.ndarray, float]:
    vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=(1, 2))
    start = time.perf_counter()
    matrix = vectorizer.fit_transform(texts)
    elapsed = time.perf_counter() - start
    return matrix.astype(np.float32), elapsed


def run_bert(texts: list[str]) -> tuple[np.ndarray, float]:
    import os
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
    from app.services.embedding import generate_embeddings_batch

    start = time.perf_counter()
    embeddings = generate_embeddings_batch(texts).astype(np.float32)
    elapsed = time.perf_counter() - start
    return embeddings, elapsed


def compare_embeddings(
    input_path: str,
    output_path: str,
    sample_size: int,
    query_count: int,
    top_k: int,
    max_features: int,
    skip_bert: bool,
) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    df = df.dropna(subset=["embedding_text"]).head(sample_size).reset_index(drop=True)
    texts = df["embedding_text"].astype(str).tolist()

    rows: list[dict[str, object]] = []

    tfidf_vectors, tfidf_build_seconds = run_tfidf(texts, max_features=max_features)
    tfidf_quality, tfidf_latency = evaluate_neighbors(tfidf_vectors, df, query_count, top_k)
    rows.append({
        "method": "TF-IDF",
        "dimensions": tfidf_vectors.shape[1],
        "documents": tfidf_vectors.shape[0],
        "build_seconds": round(tfidf_build_seconds, 4),
        "avg_query_latency_ms": round(tfidf_latency, 4),
        "avg_genre_overlap_at_k": round(tfidf_quality, 4),
        "notes": "Fast, explainable, good keyword baseline",
    })

    if not skip_bert:
        try:
            bert_vectors, bert_build_seconds = run_bert(texts)
            bert_quality, bert_latency = evaluate_neighbors(bert_vectors, df, query_count, top_k)
            rows.append({
                "method": "BERT/SentenceTransformer",
                "dimensions": bert_vectors.shape[1],
                "documents": bert_vectors.shape[0],
                "build_seconds": round(bert_build_seconds, 4),
                "avg_query_latency_ms": round(bert_latency, 4),
                "avg_genre_overlap_at_k": round(bert_quality, 4),
                "notes": "Semantic vectors, better for meaning-based search",
            })
        except Exception as exc:
            rows.append({
                "method": "BERT/SentenceTransformer",
                "dimensions": None,
                "documents": len(df),
                "build_seconds": None,
                "avg_query_latency_ms": None,
                "avg_genre_overlap_at_k": None,
                "notes": f"Skipped because model could not load: {exc}",
            })

    result = pd.DataFrame(rows)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False, encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare TF-IDF and BERT embeddings.")
    parser.add_argument("--input", default="data/processed/books_clean.csv")
    parser.add_argument("--output", default="data/processed/embedding_comparison.csv")
    parser.add_argument("--sample-size", type=int, default=1000)
    parser.add_argument("--query-count", type=int, default=100)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-features", type=int, default=20000)
    parser.add_argument("--skip-bert", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    comparison = compare_embeddings(
        input_path=args.input,
        output_path=args.output,
        sample_size=args.sample_size,
        query_count=args.query_count,
        top_k=args.top_k,
        max_features=args.max_features,
        skip_bert=args.skip_bert,
    )
    print(comparison.to_string(index=False))
    print(f"Saved comparison to {args.output}")
