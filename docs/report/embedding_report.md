# Embedding Report

## Muc tieu

So sanh baseline TF-IDF voi BERT/SentenceTransformer cho bai toan tim kiem sach theo noi dung.

## Du lieu test

- File dau vao: `data/processed/books_clean.csv`
- Cot dung de tao vector: `embedding_text`
- Sample mac dinh trong script: 1,000 documents
- Top-k danh gia: 5
- Metric tu dong: trung binh genre overlap giua sach truy van va cac sach duoc tra ve

## Ket qua hien tai

| method | dimensions | documents | build_seconds | avg_query_latency_ms | avg_genre_overlap_at_k |
| --- | ---: | ---: | ---: | ---: | ---: |
| TF-IDF | 20000 | 1000 | 0.2083 | 0.0192 | 0.5362 |

## Nhan xet

- TF-IDF tao vector nhanh, khong can model ngoai, phu hop lam baseline va keyword search.
- BERT/SentenceTransformer phu hop semantic search hon vi bieu dien y nghia cau/description, nhung can cai `sentence-transformers` va model `all-MiniLM-L6-v2`.
- Moi truong Python hien tai chua co package `sentence_transformers`, nen lan verify nay chi chay TF-IDF. Code BERT da co trong `scripts/compare_embeddings.py` va backend `app/services/embedding.py`.

## Lenh chay

```powershell
python scripts\compare_embeddings.py --skip-bert --sample-size 1000 --query-count 100 --top-k 5
```

Sau khi cai dependency:

```powershell
pip install -r backend\requirements.txt
python scripts\compare_embeddings.py --sample-size 1000 --query-count 100 --top-k 5
```
