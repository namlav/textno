import argparse
import csv
import io
import json
import random
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path


DATASET_URL = (
    "https://www.kaggle.com/api/v1/datasets/download/"
    "haitranquangofficial/vietnamese-online-news-dataset"
)
ZIP_MEMBER = "news_dataset.json"
CSV_FIELDS = [
    "id",
    "title",
    "updatetime",
    "wordcount",
    "publication",
    "tags",
    "content",
    "author",
]

CANONICAL_TOPICS = {
    "Th\u1ebf gi\u1edbi": "Th\u1ebf gi\u1edbi",
    "TH\u1ebe GI\u1edaI": "Th\u1ebf gi\u1edbi",
    "Qu\u1ed1c t\u1ebf": "Th\u1ebf gi\u1edbi",
    "Th\u1ec3 thao": "Th\u1ec3 thao",
    "TH\u1ec2 THAO": "Th\u1ec3 thao",
    "X\u00e3 h\u1ed9i": "X\u00e3 h\u1ed9i",
    "X\u00e3 H\u1ed9i": "X\u00e3 h\u1ed9i",
    "X\u00c3 H\u1ed8I": "X\u00e3 h\u1ed9i",
    "Ph\u00e1p lu\u1eadt": "Ph\u00e1p lu\u1eadt",
    "PH\u00c1P LU\u1eacT": "Ph\u00e1p lu\u1eadt",
    "Th\u1eddi s\u1ef1": "Th\u1eddi s\u1ef1",
    "Trong n\u01b0\u1edbc": "Th\u1eddi s\u1ef1",
    "Kinh doanh": "Kinh doanh",
    "Kinh Doanh": "Kinh doanh",
    "Kinh t\u1ebf": "Kinh t\u1ebf",
    "KINH T\u1ebe": "Kinh t\u1ebf",
    "Gi\u1ea3i tr\u00ed": "Gi\u1ea3i tr\u00ed",
    "S\u1ee9c kh\u1ecfe": "S\u1ee9c kh\u1ecfe",
    "S\u1ee9c Kh\u1ecfe": "S\u1ee9c kh\u1ecfe",
    "\u0110\u1eddi s\u1ed1ng": "\u0110\u1eddi s\u1ed1ng",
    "S\u1ed1ng": "\u0110\u1eddi s\u1ed1ng",
    "Gi\u00e1o d\u1ee5c": "Gi\u00e1o d\u1ee5c",
    "V\u0103n h\u00f3a": "V\u0103n h\u00f3a",
    "V\u0102N H\u00d3A": "V\u0103n h\u00f3a",
    "C\u00f4ng ngh\u1ec7": "C\u00f4ng ngh\u1ec7",
    "S\u1ed1 h\u00f3a": "C\u00f4ng ngh\u1ec7",
    "Du l\u1ecbch": "Du l\u1ecbch",
    "Du L\u1ecbch": "Du l\u1ecbch",
    "B\u1ea5t \u0111\u1ed9ng s\u1ea3n": "B\u1ea5t \u0111\u1ed9ng s\u1ea3n",
    "Khoa h\u1ecdc": "Khoa h\u1ecdc",
    "Ch\u00ednh tr\u1ecb": "Ch\u00ednh tr\u1ecb",
    "CH\u00cdNH TR\u1eca": "Ch\u00ednh tr\u1ecb",
    "Xe": "Xe",
    "\u00d4 t\u00f4": "Xe",
    "\u00d4 t\u00f4 - Xe m\u00e1y": "Xe",
    "B\u1ea1n \u0111\u1ecdc": "B\u1ea1n \u0111\u1ecdc",
    "Gi\u1edbi tr\u1ebb": "Gi\u1edbi tr\u1ebb",
    "B\u1ea1n tr\u1ebb - Cu\u1ed9c s\u1ed1ng": "Gi\u1edbi tr\u1ebb",
}


def compact(value: object) -> str:
    return " ".join(str(value or "").split())


def download_dataset(zip_path: Path) -> None:
    if zip_path.exists():
        return
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(DATASET_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=600) as response:
        zip_path.write_bytes(response.read())


def iter_json_array_from_zip(zip_path: Path, member: str):
    decoder = json.JSONDecoder()
    with zipfile.ZipFile(zip_path) as archive, archive.open(member) as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8")
        buffer = ""
        pos = 0
        while True:
            if pos >= len(buffer):
                chunk = text.read(1024 * 1024)
                if not chunk:
                    return
                buffer = chunk
                pos = 0

            while True:
                while pos < len(buffer) and buffer[pos] in " \r\n\t,":
                    pos += 1
                if pos < len(buffer) and buffer[pos] == "[":
                    pos += 1
                    continue
                if pos < len(buffer) and buffer[pos] == "]":
                    return
                if pos >= len(buffer):
                    break

                try:
                    obj, end = decoder.raw_decode(buffer, pos)
                except json.JSONDecodeError:
                    chunk = text.read(1024 * 1024)
                    if not chunk:
                        raise
                    buffer = buffer[pos:] + chunk
                    pos = 0
                    break

                yield obj
                pos = end


def to_project_row(article: dict, topic: str | None = None) -> dict[str, object] | None:
    title = compact(article.get("title"))
    content = compact(article.get("content"))
    if not title or not content:
        return None

    resolved_topic = topic if topic is not None else compact(article.get("topic")) or "Unknown"
    return {
        "id": compact(article.get("id")),
        "title": title,
        "updatetime": compact(article.get("crawled_at")),
        "wordcount": len(content.split()),
        "publication": compact(article.get("source")),
        "tags": resolved_topic,
        "content": content,
        "author": compact(article.get("author")) or "Unknown",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build_balanced_sample(zip_path: Path, output_path: Path, sample_size: int, seed: int) -> None:
    random.seed(seed)
    topics = sorted(set(CANONICAL_TOPICS.values()))
    per_topic = sample_size // len(topics)
    remainder = sample_size % len(topics)
    target_by_topic = {
        topic: per_topic + (1 if index < remainder else 0)
        for index, topic in enumerate(topics)
    }
    buckets: dict[str, list[dict[str, object]]] = defaultdict(list)
    seen_by_topic: dict[str, int] = defaultdict(int)

    for article in iter_json_array_from_zip(zip_path, ZIP_MEMBER):
        topic = CANONICAL_TOPICS.get(compact(article.get("topic")))
        if topic is None:
            continue
        row = to_project_row(article, topic)
        if row is None:
            continue

        seen_by_topic[topic] += 1
        bucket = buckets[topic]
        target = target_by_topic[topic]
        if len(bucket) < target:
            bucket.append(row)
            continue

        candidate = random.randint(1, seen_by_topic[topic])
        if candidate <= target:
            bucket[candidate - 1] = row

    missing = [
        topic for topic in topics
        if len(buckets[topic]) < target_by_topic[topic]
    ]
    if missing:
        raise RuntimeError(f"Not enough rows for topics: {missing}")

    rows = [row for topic in topics for row in buckets[topic]]
    random.shuffle(rows)
    write_csv(output_path, rows)
    print(f"Sample rows written: {len(rows)} -> {output_path}")


def build_full_dataset(zip_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    written = 0
    skipped_missing = 0
    seen_ids: set[str] = set()

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for article in iter_json_array_from_zip(zip_path, ZIP_MEMBER):
            total += 1
            row = to_project_row(article)
            if row is None:
                skipped_missing += 1
                continue
            article_id = str(row["id"])
            if article_id in seen_ids:
                continue
            seen_ids.add(article_id)
            writer.writerow(row)
            written += 1

    print(f"Source rows: {total}")
    print(f"Rows with title/content written: {written} -> {output_path}")
    print(f"Rows skipped without title/content: {skipped_missing}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and convert the Kaggle Vietnamese Online News Dataset."
    )
    parser.add_argument(
        "--zip-path",
        default="data/raw/kaggle_vietnamese_online_news.zip",
        help="Local cache path for the downloaded Kaggle zip.",
    )
    parser.add_argument(
        "--sample-output",
        default="data/raw/dataset_kaggle_sample_10000.csv",
        help="Output CSV path for the balanced sample.",
    )
    parser.add_argument("--sample-size", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260608)
    parser.add_argument(
        "--full-output",
        default=None,
        help="Optional output CSV path for the full converted dataset.",
    )
    args = parser.parse_args()

    zip_path = Path(args.zip_path)
    download_dataset(zip_path)
    build_balanced_sample(
        zip_path=zip_path,
        output_path=Path(args.sample_output),
        sample_size=args.sample_size,
        seed=args.seed,
    )
    if args.full_output:
        build_full_dataset(zip_path, Path(args.full_output))


if __name__ == "__main__":
    main()
