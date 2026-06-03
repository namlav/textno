import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import pandas as pd
from datetime import datetime
from app.database.mongodb import get_collection
from app.services.embedding import generate_embedding
from app.services.search import add_embedding


def import_dataset(
    csv_path: str,
    title_col: str = "title",
    content_col: str = "content",
    category_col: str = "category",
    author_col: str = "author",
):
    df = pd.read_csv(csv_path)
    collection = get_collection()
    imported = 0

    for _, row in df.iterrows():
        title = str(row.get(title_col, ""))
        content = str(row.get(content_col, ""))
        category = str(row.get(category_col, "")) if category_col in row else None
        author = str(row.get(author_col, "")) if author_col in row else None

        text_for_embedding = f"{title} {content}"
        embedding = generate_embedding(text_for_embedding)
        embedding_id = add_embedding(embedding)

        doc = {
            "title": title,
            "content": content,
            "category": category,
            "author": author,
            "embedding_id": embedding_id,
            "created_at": datetime.utcnow(),
        }
        collection.insert_one(doc)
        imported += 1
        if imported % 100 == 0:
            print(f"Imported {imported} documents...")

    print(f"Import completed. Total: {imported} documents.")


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
        csv_path, category_col="tags"
    )  # đọc cột "tags" có trong dataset thay vì "category"
