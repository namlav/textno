# textno

Bai tap nhom mon Khai pha du lieu (Python, NoSQL).

## Person B - Data/NLP work

Phan nay xu ly dataset `data/raw/books.csv` cho bai toan quan ly va tim kiem sach.

### Da hoan thanh

- Lam sach dataset goc `books.csv`.
- Tao dataset sach `data/processed/books_clean.csv`.
- Chuan hoa text: xoa HTML, URL, ky tu dac biet, khoang trang thua.
- Tokenize co ban va remove stopwords trong `backend/app/utils/preprocessing.py`.
- Tao cot `embedding_text` de dung cho search/embedding.
- Tao cot `category` tu genre dau tien va chuan hoa cot `genres`.
- Viet script so sanh TF-IDF voi BERT/SentenceTransformer.
- Chuan bi script import dataset sach vao MongoDB va FAISS.
- Tao bao cao data va embedding trong `docs/report/`.

### Files chinh

- `scripts/preprocess_books.py`: tien xu ly rieng cho dataset sach.
- `scripts/compare_embeddings.py`: so sanh TF-IDF va BERT/SentenceTransformer.
- `scripts/generate_embeddings.py`: tao vector embedding va rebuild FAISS index.
- `scripts/import_data.py`: import dataset sach vao MongoDB, dong thoi them embedding vao FAISS.
- `backend/app/utils/preprocessing.py`: cac ham clean text, tokenize, remove stopwords.
- `backend/app/services/embedding.py`: sinh embedding bang SentenceTransformer.
- `docs/report/data_report.md`: bao cao nguon du lieu, cau truc du lieu, quy trinh tien xu ly.
- `docs/report/embedding_report.md`: bao cao so sanh embedding.

### Cach chay lai tu dau

```powershell
pip install -r backend\requirements.txt
python scripts\preprocess_books.py
python scripts\compare_embeddings.py
python scripts\generate_embeddings.py data/processed/books_clean.csv embedding_text data/embeddings
python scripts\import_data.py data/processed/books_clean.csv --batch-size 256
```

Neu chi muon test nhanh TF-IDF va khong tai/chay BERT:

```powershell
python scripts\compare_embeddings.py --skip-bert
```

### Outputs

- `data/processed/books_clean.csv`
- `data/processed/embedding_comparison.csv`
- `docs/report/data_report.md`
- `docs/report/embedding_report.md`
- `data/embeddings/embeddings.npy`
- `faiss_index/index.faiss`

### Ket qua test gan nhat

Dataset sach:

```text
books_clean.csv shape: (52390, 18)
```

So sanh embedding voi sample 1,000 documents:

```text
TF-IDF:
- dimensions: 20000
- build_seconds: 0.1686
- avg_query_latency_ms: 0.0341
- avg_genre_overlap_at_k: 0.5362

BERT/SentenceTransformer:
- dimensions: 384
- build_seconds: 43.2567
- avg_query_latency_ms: 0.0716
- avg_genre_overlap_at_k: 0.5036
```

Check syntax Python:

```powershell
python -m compileall backend scripts
```

### Ghi chu

- BERT dung model mac dinh `all-MiniLM-L6-v2`.
- Lan dau chay BERT se tai model tu Hugging Face nen mat thoi gian hon.
- `scripts/import_data.py` can MongoDB dang chay.
- `scripts/generate_embeddings.py` va `scripts/import_data.py` co the mat nhieu thoi gian neu chay toan bo 52k documents.

### Lenh da dung de verify

```powershell
python scripts\preprocess_books.py
python scripts\compare_embeddings.py
python -m compileall backend scripts
```
