import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import pandas as pd
from app.utils.preprocessing import preprocess


def preprocess_dataset(input_path: str, output_path: str, text_columns: list[str]):
    df = pd.read_csv(input_path)
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(preprocess)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")
    print(f"Total records: {len(df)}")


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "../data/raw/dataset.csv"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "../data/processed/cleaned.csv"
    columns = sys.argv[3].split(",") if len(sys.argv) > 3 else ["title", "content"]
    preprocess_dataset(input_path, output_path, columns)
