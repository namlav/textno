# textno - Hệ thống Quản lý & Tìm kiếm Văn bản Phi cấu trúc

Bài tập nhóm môn **Khai phá dữ liệu** — Xây dựng hệ thống tìm kiếm ngữ nghĩa (Semantic Search) cho tài liệu văn bản.

## Kiến trúc tổng quan

```
┌─────────────────────────────────────────────────────┐
│  Frontend (Streamlit) ─── port 8501                 │
│  Giao diện quản trị & tìm kiếm                      │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP REST (requests)
┌─────────────────────▼───────────────────────────────-----┐
│  Backend (FastAPI) ──── port 8000                        │
│  API: CRUD documents + Semantic Search                   │
├─────────────────┬──────────────────┬────────────────-----┤
│  MongoDB        │  FAISS           │  SentenceTransformer│
│  (NoSQL storage)│  (Vector index)  │  (Embedding model)  │
└─────────────────┴──────────────────┴────────────────-----┘
```

## Công nghệ sử dụng

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| **Backend API** | FastAPI (Python) | RESTful endpoints cho CRUD & search |
| **Database** | MongoDB | Lưu document gốc (JSON BSON) |
| **Vector Index** | FAISS (CPU) | Tìm kiếm tương tự (similarity search) tốc độ cao |
| **Embedding Model** | SentenceTransformer (`paraphrase-multilingual-MiniLM-L12-v2`) | Chuyển văn bản thành vector 384 chiều |
| **Frontend** | Streamlit | Dashboard trực quan, tìm kiếm & thống kê |

## Cấu trúc thư mục

```
textno/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py           # Entry point FastAPI
│   │   ├── core/config.py    # Cấu hình (MongoDB, model, path)
│   │   ├── database/mongodb.py  # Kết nối MongoDB
│   │   ├── models/document.py   # Pydantic models
│   │   ├── api/routes.py     # REST API endpoints
│   │   ├── services/
│   │   │   ├── embedding.py  # Sinh vector embedding (SentenceTransformer)
│   │   │   └── search.py     # Tìm kiếm vector (FAISS)
│   │   └── utils/preprocessing.py  # Tiền xử lý văn bản tiếng Việt
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                 # Streamlit UI
│   ├── app.py                # Dashboard chính (3 tabs)
│   ├── Dockerfile
│   └── requirements.txt
│
├── scripts/                  # Utility scripts
│   ├── preprocess.py         # Tiền xử lý dataset VnExpress
│   ├── preprocess_books.py   # Tiền xử lý dataset Goodreads Books
│   ├── prepare_kaggle_news_dataset.py  # Tải & chuyển đổi Kaggle dataset
│   ├── import_data.py        # Import CSV -> MongoDB + FAISS
│   ├── generate_embeddings.py  # Sinh embeddings riêng lẻ
│   └── compare_embeddings.py   # So sánh TF-IDF vs BERT
│
├── data/
│   ├── raw/                  # Dữ liệu gốc
│   │   ├── dataset.csv       # Dataset VnExpress gốc
│   │   ├── dataset_kaggle_sample_10000.csv  # Mẫu cân bằng 10K từ Kaggle
│   │   └── news_dataset.json # JSON gốc từ Kaggle
│   └── processed/            # Dữ liệu đã tiền xử lý
│       ├── cleaned.csv       # VnExpress articles đã làm sạch
│       └── books_clean.csv   # Goodreads books đã làm sạch
│
├── faiss_index/              # FAISS vector index (tự động tạo)
│   └── index.faiss
│
├── docker-compose.yml        # Orchestration 3 services
└── README.md
```

## Dataset

### 1. VnExpress News (Nguồn chính)

- **Kaggle**: [Vietnamese Online News Dataset](https://www.kaggle.com/datasets/haitranquangofficial/vietnamese-online-news-dataset) (150K+ bài báo)
- **Schema CSV**: `id, title, updatetime, wordcount, publication, tags, content, author`
- **Mẫu local**: `data/raw/dataset_kaggle_sample_10000.csv` (10,000 articles, stratified sampling theo chủ đề)

### 2. Goodreads Books (Nguồn phụ, metadata)

- Dataset sách với genres, rating, author, description
- Script preprocessing: `scripts/preprocess_books.py`

## Hướng dẫn sử dụng

### Yêu cầu

- Python 3.11+
- MongoDB (local hoặc Atlas)
- Docker (nếu chạy container)

### Cài đặt & Chạy (Local)

```powershell
# 1. Clone repo
git clone <repo-url>
cd textno

# 2. Tạo virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Cài dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 4. Khởi động MongoDB (nếu dùng local)
mongod

# 5. Import dữ liệu lên MongoDB + FAISS
python scripts/import_data.py

# 6. Khởi động Backend
cd backend
uvicorn app.main:app --reload --port 8000

# 7. Khởi động Frontend (terminal khác)
cd frontend
streamlit run app.py --server.port=8501
```

### Chạy với Docker

```powershell
docker compose up -d
```

Sau đó truy cập:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs** (Swagger): http://localhost:8000/docs

### Import dữ liệu

```powershell
# Import cleaned.csv mặc định
python scripts/import_data.py

# Import file đã xử lý cụ thể nếu tên file khác mặc định(cleaned.csv)
python scripts/import_data.py data/processed/name_file.csv

```

> **Lưu ý:** Script tự động dò tìm cột category trong CSV. Thứ tự ưu tiên: `category` → `tags` → `copic` → `topic` → `categories` → `tag`. Nếu không tìm thấy cột nào, trường `category` trong MongoDB sẽ là `null`.

## API Endpoints

| Method | Path | Mô tả |
|--------|------|-------|
| `GET` | `/` | Health check |
| `POST` | `/documents` | Tạo document + sinh embedding |
| `GET` | `/documents` | Danh sách tất cả documents |
| `GET` | `/documents/{id}` | Chi tiết document |
| `DELETE` | `/documents/{id}` | Xoá document |
| `POST` | `/search?query=...&top_k=5` | Tìm kiếm ngữ nghĩa |

## Pipeline xử lý dữ liệu

```
1. Raw Data (CSV/JSON)
       │
       ▼
2. Preprocessing (scripts/preprocess.py)
   - Làm sạch HTML, URL, punctuation
   - Tokenize, remove stopwords
   - Sinh cột text_for_embedding
       │
       ▼
3. Import (scripts/import_data.py)
   - Sinh vector embedding (SentenceTransformer)
   - Lưu vector vào FAISS index
   - Lưu document vào MongoDB
       │
       ▼
4. Search (POST /search)
   - Nhúng query thành vector
   - FAISS tìm top_k vector gần nhất
   - Mapping embedding_id -> document MongoDB
```

## Tác giả

Nhóm 19 môn Khai phá dữ liệu — Đề tài xây dựng hệ thống Quản lý dữ liệu phi cấu trúc.
