import argparse
import gc
import os
import sys
from datetime import datetime, timezone

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database.mongodb import get_collection
from app.services.embedding import generate_embeddings_batch
from app.services.search import add_embeddings_batch


METADATA_COLUMNS = [
    "source_id", "author", "genres", "language", "rating", "num_ratings",
    "pages", "publisher", "publish_date", "cover_img", "bbe_score",
    "bbe_votes", "price", "token_count",
]


def clean_value(value: object) -> object:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


CATEGORY_CANDIDATES = ["category", "tags", "copic", "topic", "categories", "tag"]


def _resolve_category_col(df: pd.DataFrame, category_col: str) -> str | None:
    if category_col in df.columns:
        return category_col
    for column in CATEGORY_CANDIDATES:
        if column in df.columns:
            print(f"Category column '{category_col}' not found, using '{column}' instead.")
            return column
    print(f"Warning: No category column found (tried: '{category_col}', {CATEGORY_CANDIDATES}). Category will be null.")
    return None


def import_dataset(
    csv_path: str,
    title_col: str = "title",
    content_col: str = "content",
    category_col: str = "category",
    embedding_col: str = "embedding_text",
    batch_size: int = 256,
    clear_collection: bool = False,
) -> int:
    with pd.option_context("mode.string_storage", "python"):
        df = pd.read_csv(csv_path)
    required = [title_col, content_col]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if embedding_col not in df.columns:
        df[embedding_col] = df[title_col].astype(str) + " " + df[content_col].astype(str)

    category_col = _resolve_category_col(df, category_col)

    collection = get_collection()
    if clear_collection:
        collection.delete_many({})

    imported = 0
    for start in range(0, len(df), batch_size):
        batch = df.iloc[start:start + batch_size].copy()
        texts = batch[embedding_col].fillna("").astype(str).tolist()
        embeddings = generate_embeddings_batch(texts)
        embedding_ids = add_embeddings_batch(embeddings)
        del texts, embeddings
        gc.collect()

        docs = []
        for (_, row), embedding_id in zip(batch.iterrows(), embedding_ids):
            doc = {
                "title": clean_value(row.get(title_col, "")) or "",
                "content": clean_value(row.get(content_col, "")) or "",
                "category": clean_value(row.get(category_col)) if category_col and category_col in row else None,
                "embedding_id": int(embedding_id),
                "created_at": datetime.now(timezone.utc),
            }

            for column in METADATA_COLUMNS:
                if column in row:
                    doc[column] = clean_value(row[column])

            docs.append(doc)

        if docs:
            collection.insert_many(docs)
            imported += len(docs)
            print(f"Imported {imported}/{len(df)} documents...")
        del docs, batch
        gc.collect()

    print(f"Import completed. Total: {imported} documents.")
    return imported


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import cleaned documents into MongoDB and FAISS.")
    parser.add_argument("csv_path", nargs="?", default="data/processed/books_clean.csv")
    parser.add_argument("--title-col", default="title")
    parser.add_argument("--content-col", default="content")
    parser.add_argument("--category-col", default="category")
    parser.add_argument("--embedding-col", default="embedding_text")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--clear-collection", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    csv_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(project_root, "data/processed/cleaned.csv")
    )
    # csv_path = ../data/processed/cleaned.csv"
    import_dataset(
        csv_path, category_col="category"
    )  # tự động dò tìm cột category: category, tags, copic, ...
