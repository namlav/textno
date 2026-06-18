# generate_embeddings.py - Sinh vector embedding riêng lẻ từ CSV và tái tạo FAISS index
#
# Kỹ thuật:
# - Đọc CSV, lấy cột text (mặc định: embedding_text / content)
# - Sinh toàn bộ vector embedding batch bằng SentenceTransformer
# - Lưu file .npy (numpy) và rebuild FAISS index từ đầu
# - Khác với import_data.py: script này KHÔNG ghi MongoDB, chỉ xử lý vector

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import numpy as np
import pandas as pd
from app.services.embedding import generate_embeddings_batch
from app.services.search import rebuild_index


def generate_and_store_embeddings(
    csv_path: str,
    text_column: str = "embedding_text",
    embed_dir: str = "data/embeddings",
):
    df = pd.read_csv(csv_path)

    # Tự động nhận diện cột text: Nếu không thấy 'embedding_text', tự động chuyển sang tìm 'content'
    if text_column not in df.columns:
        if "content" in df.columns:
            text_column = "content"
        else:
            raise ValueError(
                f"Không tìm thấy cột '{text_column}' hoặc 'content' trong file {csv_path}"
            )

    # CHỈNH SỬA QUAN TRỌNG: Ép toàn bộ dữ liệu thành kiểu string và xử lý NaN để tránh lỗi Unsupported input type: float
    texts = df[text_column].fillna("").astype(str).tolist()
    print(f"Generating embeddings for {len(texts)} documents...")

    embeddings = generate_embeddings_batch(texts)
    os.makedirs(embed_dir, exist_ok=True)

    np.save(os.path.join(embed_dir, "embeddings.npy"), embeddings)
    if "source_id" in df.columns:
        df[["source_id"]].to_csv(
            os.path.join(embed_dir, "embedding_ids.csv"), index=False
        )

    print(f"Embeddings saved to {embed_dir}/embeddings.npy")
    print(f"Shape: {embeddings.shape}")

    rebuild_index(embeddings)
    print("FAISS index rebuilt and saved.")


if __name__ == "__main__":
    # Lấy đường dẫn tuyệt đối đến thư mục chứa file script này (thư mục scripts)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Định vị chính xác thư mục gốc của dự án (textno) bằng cách lùi lại 1 cấp
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    csv_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(project_root, "data/processed/cleaned.csv")
    )
    text_col = sys.argv[2] if len(sys.argv) > 2 else "embedding_text"

    # Định vị chính xác thư mục embeddings nằm trong project root
    embed_dir = (
        sys.argv[3]
        if len(sys.argv) > 3
        else os.path.join(project_root, "data/embeddings")
    )

    generate_and_store_embeddings(csv_path, text_col, embed_dir)
