import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import numpy as np
import pandas as pd
from app.services.embedding import generate_embeddings_batch
from app.services.search import rebuild_index


def generate_and_store_embeddings(
    csv_path: str,
    text_column: str = "content",
    embed_dir: str = "../data/embeddings",
):
    df = pd.read_csv(csv_path)
    texts = df[text_column].astype(str).tolist()
    print(f"Generating embeddings for {len(texts)} documents...")

    embeddings = generate_embeddings_batch(texts)
    os.makedirs(embed_dir, exist_ok=True)

    np.save(os.path.join(embed_dir, "embeddings.npy"), embeddings)
    print(f"Embeddings saved to {embed_dir}/embeddings.npy")
    print(f"Shape: {embeddings.shape}")

    rebuild_index(embeddings)
    print("FAISS index rebuilt and saved.")


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "../data/processed/cleaned.csv"
    text_col = sys.argv[2] if len(sys.argv) > 2 else "content"
    embed_dir = sys.argv[3] if len(sys.argv) > 3 else "../data/embeddings"
    generate_and_store_embeddings(csv_path, text_col, embed_dir)
