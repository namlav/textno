# preprocess_books.py - Tiền xử lý dataset Goodreads Books (books.csv) hoặc News Dataset
#
# Pipeline:
#   1. Đọc file đầu vào, chỉ lấy các cột cần thiết (RAW_COLUMNS)
#   2. Tự động phát hiện cột dữ liệu nội dung để làm sạch text
#   3. Chuyển genres từ string list -> chuẩn hoá, category = genre đầu tiên
#   4. Sinh embedding_text từ title + author + category + genres + content
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
    "bookId",
    "title",
    "author",
    "description",
    "content",
    "genres",
    "language",
    "rating",
    "numRatings",
    "pages",
    "publisher",
    "publishDate",
    "coverImg",
    "bbeScore",
    "bbeVotes",
    "price",
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
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False), errors="coerce"
    )


def build_embedding_text(row: pd.Series) -> str:
    parts = [
        row.get("title", ""),
        row.get("author", ""),
        row.get("category", ""),
        row.get("genres", ""),
        row.get("content", ""),
    ]
    return preprocess(" ".join(str(part) for part in parts if pd.notna(part)))


def preprocess_books(
    input_path: str, output_path: str, report_path: str
) -> pd.DataFrame:
    df = pd.read_csv(input_path, usecols=lambda col: col in RAW_COLUMNS)
    original_rows = len(df)

    df = df.dropna(subset=["title"]).copy()

    # SỬA ĐỔI: Tự động phát hiện cột chứa nội dung chính (description hoặc content)
    target_content_col = "description" if "description" in df.columns else "content"
    if target_content_col not in df.columns and len(df.columns) > 1:
        target_content_col = df.columns[
            1
        ]  # Lấy cột thứ 2 làm dự phòng nếu không khớp tên

    df[target_content_col] = df[target_content_col].fillna("")

    # Kiểm tra cột định danh duy nhất (bookId), nếu không có thì bỏ qua bước drop_duplicates này
    if "bookId" in df.columns:
        df = df.drop_duplicates(subset=["bookId"], keep="first")
    df = df.drop_duplicates(subset=["title", "author"], keep="first")

    clean_df = pd.DataFrame()
    clean_df["source_id"] = (
        df["bookId"].astype(str) if "bookId" in df.columns else df.index.astype(str)
    )
    clean_df["title"] = df["title"].fillna("").map(lambda value: clean_text(value))
    clean_df["author"] = df["author"].fillna("").map(lambda value: clean_text(value))
    clean_df["content"] = (
        df[target_content_col].fillna("").map(lambda value: clean_text(value))
    )

    # Xử lý an toàn nếu file dữ liệu không có cột phân loại 'genres'
    if "genres" in df.columns:
        clean_df["category"] = df["genres"].map(primary_genre)
        clean_df["genres"] = df["genres"].map(normalize_list_cell)
    else:
        clean_df["category"] = (
            df["category"] if "category" in df.columns else "news_dataset"
        )
        clean_df["genres"] = "Unknown"

    clean_df["language"] = (
        df["language"].fillna("Unknown") if "language" in df.columns else "Unknown"
    )
    clean_df["rating"] = to_numeric(df["rating"]) if "rating" in df.columns else 0.0
    clean_df["num_ratings"] = (
        to_numeric(df["numRatings"]).fillna(0).astype("int64")
        if "numRatings" in df.columns
        else 0
    )
    clean_df["pages"] = to_numeric(df["pages"]) if "pages" in df.columns else 0
    clean_df["publisher"] = (
        df["publisher"]
        .fillna("")
        .map(lambda value: clean_text(value, keep_digits=True))
        if "publisher" in df.columns
        else "Unknown"
    )
    clean_df["publish_date"] = (
        df["publishDate"].fillna("") if "publishDate" in df.columns else ""
    )
    clean_df["cover_img"] = (
        df["coverImg"].fillna("") if "coverImg" in df.columns else ""
    )
    clean_df["bbe_score"] = (
        to_numeric(df["bbeScore"]).fillna(0).astype("int64")
        if "bbeScore" in df.columns
        else 0
    )
    clean_df["bbe_votes"] = (
        to_numeric(df["bbeVotes"]).fillna(0).astype("int64")
        if "bbeVotes" in df.columns
        else 0
    )
    clean_df["price"] = to_numeric(df["price"]) if "price" in df.columns else 0.0

    clean_df["embedding_text"] = clean_df.apply(build_embedding_text, axis=1)
    clean_df["token_count"] = clean_df["embedding_text"].map(
        lambda value: len(tokenize(value))
    )

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
        "# Data Report - Preprocessed Dataset",
        "",
        "## Nguon du lieu",
        f"- File goc: `{input_path}`",
        f"- So dong ban dau: {original_rows}",
        f"- So dong sau tien xu ly: {cleaned_rows}",
        "",
        "## Cau truc du lieu sach",
        "- `source_id`: id tu dataset goc",
        "- `title`: tieu de",
        "- `author`: tac gia",
        "- `content`: noi dung da xoa HTML, URL, ky tu thua",
        "- `category`: category chinh",
        "- `genres`: danh sach genre da chuan hoa bang dau cham phay",
        "- `embedding_text`: text da lowercase, tokenize co ban, remove stopwords de tao vector",
        "",
        "## Quy trinh tien xu ly",
        "1. Doc cac cot can thiet tu file input.",
        "2. Xoa ban ghi thieu title.",
        "3. Lam sach text: HTML unescape, xao HTML tag, URL, ky tu dac biet va khoang trang thua.",
        "4. Tu dong nhan dien cot bieu dien noi dung phu hop.",
        "5. Export file sang CSV UTF-8 de import MongoDB/FAISS.",
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
    parser = argparse.ArgumentParser(description="Preprocess books or news datasets.")
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
