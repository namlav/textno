import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import pandas as pd
from app.utils.preprocessing import preprocess, tokenize


ARTICLE_COLUMNS = [
    "id",
    "title",
    "updatetime",
    "wordcount",
    "publication",
    "tags",
    "content",
    "author",
]


def compact_whitespace(value: object) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def load_json_articles(input_path: Path) -> pd.DataFrame:
    json_files = sorted(input_path.glob("*.json")) if input_path.is_dir() else [input_path]
    rows: list[dict[str, str]] = []

    for json_file in json_files:
        raw_text = json_file.read_text(encoding="utf-8")
        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError:
            if raw_text.startswith("{{") and raw_text.endswith("}}"):
                payload = json.loads(f"[{raw_text[1:-1]}]")
            else:
                raise

        articles = payload if isinstance(payload, list) else payload.get("data", [])
        category = json_file.stem

        for article in articles:
            row = {column: compact_whitespace(article.get(column, "")) for column in ARTICLE_COLUMNS}
            row["category"] = category
            row["source"] = "VnExpress"
            if not row["wordcount"]:
                row["wordcount"] = str(len(tokenize(row["content"])))
            rows.append(row)

    return pd.DataFrame(rows)


def load_articles(input_path: str) -> pd.DataFrame:
    path = Path(input_path)
    if path.is_dir() or path.suffix.lower() == ".json":
        return load_json_articles(path)
    return pd.read_csv(path)


def build_raw_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for column in ARTICLE_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    df["title"] = df["title"].apply(compact_whitespace)
    df["content"] = df["content"].apply(compact_whitespace)
    df["tags"] = df["tags"].apply(compact_whitespace)
    df = df[df["title"].ne("") & df["content"].ne("")]
    df = df.drop_duplicates(subset=["id"], keep="first")
    df = df.drop_duplicates(subset=["title", "content"], keep="first")
    return df[ARTICLE_COLUMNS]


def build_processed_dataset(raw: pd.DataFrame, source_df: pd.DataFrame) -> pd.DataFrame:
    metadata_cols = [column for column in ["id", "category", "source"] if column in source_df.columns]
    processed = raw.merge(source_df[metadata_cols].drop_duplicates("id"), on="id", how="left")
    processed["clean_title"] = processed["title"].apply(preprocess)
    processed["clean_content"] = processed["content"].apply(preprocess)
    processed["tokens"] = processed["clean_content"].apply(lambda text: " ".join(tokenize(text)))
    processed["text_for_embedding"] = (
        processed["clean_title"].fillna("") + " " + processed["clean_content"].fillna("")
    ).str.strip()
    return processed


def preprocess_dataset(input_path: str, raw_output: str, processed_output: str) -> None:
    source_df = load_articles(input_path)
    raw = build_raw_dataset(source_df)
    processed = build_processed_dataset(raw, source_df)

    Path(raw_output).parent.mkdir(parents=True, exist_ok=True)
    Path(processed_output).parent.mkdir(parents=True, exist_ok=True)
    raw.to_csv(raw_output, index=False, encoding="utf-8")
    processed.to_csv(processed_output, index=False, encoding="utf-8")

    print(f"Raw dataset saved to {raw_output}")
    print(f"Processed dataset saved to {processed_output}")
    print(f"Total records: {len(raw)}")
    if "category" in processed.columns:
        print("Records by category:")
        print(processed["category"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build raw and processed VnExpress datasets.")
    parser.add_argument("input_path", help="CSV file, JSON file, or directory containing VnExpress JSON files")
    parser.add_argument("--raw-output", default="data/raw/dataset.csv")
    parser.add_argument("--processed-output", default="data/processed/cleaned.csv")
    args = parser.parse_args()

    preprocess_dataset(args.input_path, args.raw_output, args.processed_output)
