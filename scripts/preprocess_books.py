# preprocess_books.py - Tiền xử lý dataset Goodreads Books (books.csv)
#
# Pipeline:
#   1. Đọc books.csv, chỉ lấy các cột cần thiết (RAW_COLUMNS)
#   2. Làm sạch text: HTML unescape, xoá HTML tag, URL, ký tự đặc biệt
#   3. Chuyển genres từ string list -> chuẩn hoá, category = genre đầu tiên
#   4. Sinh embedding_text từ title + author + category + genres + description
#   5. Export cleaned CSV + báo cáo thống kê (docs/report/data_report.md)

import argparse
import ast
import os
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.utils.preprocessing import clean_text, preprocess, tokenize


RAW_COLUMNS = [
    "bookId", "title", "author", "description", "genres", "language", "rating",
    "numRatings", "pages", "publisher", "publishDate", "coverImg", "bbeScore",
    "bbeVotes", "price",
]


def parse_list_cell(value: object) -> list[str]:
    # Chuyển cell dạng list string (vd: "['Fiction', 'Drama']") thành list Python
    if pd.isna(value):
        return []

    text = str(value).strip()
    if not text or text == "[]":
        return []

    try:
        parsed = ast.literal_eval(text)
    except (SyntaxError, ValueError):
        return [clean_text(part) for part in text.split(",") if clean_text(part)]

    if isinstance(parsed, list):
        return [str(item).strip() for item in parsed if str(item).strip()]
    return [str(parsed).strip()]


def normalize_list_cell(value: object) -> str:
    # Chuyển list genres thành string cách nhau bằng dấu chấm phẩy
    return "; ".join(parse_list_cell(value))


def primary_genre(value: object) -> str:
    # Lấy genre đầu tiên làm category chính
    genres = parse_list_cell(value)
    return genres[0] if genres else "Unknown"


def to_numeric(series: pd.Series) -> pd.Series:
    # Chuyển cột string thành số (xoá dấu phẩy trong số)
    return pd.to_numeric(series.astype(str).str.replace(",", "", regex=False), errors="coerce")


def build_embedding_text(row: pd.Series) -> str:
    parts = [
        row.get("title", ""),
        row.get("author", ""),
        row.get("category", ""),
        row.get("genres", ""),
        row.get("content", ""),
    ]
    return preprocess(" ".join(str(part) for part in parts if pd.notna(part)))


def preprocess_books(input_path: str, output_path: str, report_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path, usecols=lambda col: col in RAW_COLUMNS)
    original_rows = len(df)

    df = df.dropna(subset=["title"]).copy()
    df["description"] = df["description"].fillna("")
    df = df.drop_duplicates(subset=["bookId"], keep="first")
    df = df.drop_duplicates(subset=["title", "author"], keep="first")

    clean_df = pd.DataFrame()
    clean_df["source_id"] = df["bookId"].astype(str)
    clean_df["title"] = df["title"].fillna("").map(lambda value: clean_text(value, keep_digits=True))
    clean_df["author"] = df["author"].fillna("").map(lambda value: clean_text(value, keep_digits=True))
    clean_df["content"] = df["description"].fillna("").map(lambda value: clean_text(value, keep_digits=True))
    clean_df["category"] = df["genres"].map(primary_genre)
    clean_df["genres"] = df["genres"].map(normalize_list_cell)
    clean_df["language"] = df["language"].fillna("Unknown")
    clean_df["rating"] = to_numeric(df["rating"])
    clean_df["num_ratings"] = to_numeric(df["numRatings"]).fillna(0).astype("int64")
    clean_df["pages"] = to_numeric(df["pages"])
    clean_df["publisher"] = df["publisher"].fillna("").map(lambda value: clean_text(value, keep_digits=True))
    clean_df["publish_date"] = df["publishDate"].fillna("")
    clean_df["cover_img"] = df["coverImg"].fillna("")
    clean_df["bbe_score"] = to_numeric(df["bbeScore"]).fillna(0).astype("int64")
    clean_df["bbe_votes"] = to_numeric(df["bbeVotes"]).fillna(0).astype("int64")
    clean_df["price"] = to_numeric(df["price"])
    clean_df["embedding_text"] = clean_df.apply(build_embedding_text, axis=1)
    clean_df["token_count"] = clean_df["embedding_text"].map(lambda value: len(tokenize(value)))

    clean_df = clean_df[clean_df["embedding_text"].str.len() > 0].reset_index(drop=True)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(output, index=False, encoding="utf-8")

    write_report(
        report_path=report_path,
        input_path=input_path,
        output_path=output_path,
        original_rows=original_rows,
        cleaned_rows=len(clean_df),
        df=clean_df,
    )
    return clean_df


def write_report(
    report_path: str,
    input_path: str,
    output_path: str,
    original_rows: int,
    cleaned_rows: int,
    df: pd.DataFrame,
) -> None:
    report = Path(report_path)
    report.parent.mkdir(parents=True, exist_ok=True)

    missing = df.isna().sum().sort_values(ascending=False)
    top_categories = df["category"].value_counts().head(10)
    avg_tokens = round(float(df["token_count"].mean()), 2) if cleaned_rows else 0

    content = [
        "# Data Report - Goodreads Books",
        "",
        "## Nguon du lieu",
        "- File goc: `data/raw/books.csv`",
        "- Dataset: Best Books Ever / Goodreads books dataset",
        f"- So dong ban dau: {original_rows}",
        f"- So dong sau tien xu ly: {cleaned_rows}",
        "",
        "## Cau truc du lieu sach",
        "- `source_id`: id sach tu dataset goc",
        "- `title`: ten sach",
        "- `author`: tac gia",
        "- `content`: mo ta sach da xoa HTML, URL, ky tu thua",
        "- `category`: genre dau tien, dung nhu nhan/category chinh",
        "- `genres`: danh sach genre da chuan hoa bang dau cham phay",
        "- `embedding_text`: text da lowercase, tokenize co ban, remove stopwords de tao vector",
        "- `rating`, `num_ratings`, `pages`, `publisher`, `publish_date`, `cover_img`: metadata phuc vu hien thi/loc",
        "",
        "## Quy trinh tien xu ly",
        "1. Doc cac cot can thiet tu `books.csv`.",
        "2. Xoa ban ghi thieu title.",
        "3. Xoa trung lap theo `bookId`, sau do theo cap `title` + `author`.",
        "4. Lam sach text: HTML unescape, xoa HTML tag, URL, ky tu dac biet va khoang trang thua.",
        "5. Chuan hoa `genres` tu chuoi list thanh chuoi phan tach bang dau cham phay.",
        "6. Tao `category` tu genre dau tien.",
        "7. Tao `embedding_text` tu title, author, category, genres va description da remove stopwords.",
        "8. Export file sach sach sang CSV UTF-8 de import MongoDB/FAISS.",
        "",
        "## Thong ke nhanh",
        f"- Token trung binh moi document: {avg_tokens}",
        "",
        "### Missing values sau tien xu ly",
        series_to_markdown(missing),
        "",
        "### Top 10 category",
        series_to_markdown(top_categories),
        "",
        "## File dau ra",
        f"- Dataset sach: `{output_path}`",
        "- San sang import DB bang `scripts/import_data.py`.",
    ]
    report.write_text("\n".join(content), encoding="utf-8")


def series_to_markdown(series: pd.Series) -> str:
    lines = ["| field | value |", "| --- | ---: |"]
    for index, value in series.items():
        lines.append(f"| {index} | {value} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess Goodreads books.csv dataset.")
    parser.add_argument("--input", default="data/raw/books.csv")
    parser.add_argument("--output", default="data/processed/books_clean.csv")
    parser.add_argument("--report", default="docs/report/data_report.md")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = preprocess_books(args.input, args.output, args.report)
    print(f"Saved cleaned dataset to {args.output}")
    print(f"Saved data report to {args.report}")
    print(f"Total cleaned records: {len(result)}")
