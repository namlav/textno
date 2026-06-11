# HỆ THỐNG QUẢN LÝ DỮ LIỆU PHI CẤU TRÚC – TEXT DOCUMENT MANAGEMENT SYSTEM

## 1. Tổng quan dự án

### 1.1 Tên đề tài

Xây dựng hệ thống quản lý và tìm kiếm dữ liệu văn bản phi cấu trúc sử dụng MongoDB, FAISS và Sentence Transformers.

---

### 1.2 Mục tiêu dự án

Xây dựng một hệ thống có khả năng:

* Quản lý tài liệu văn bản phi cấu trúc.
* Tìm kiếm tài liệu theo ngữ nghĩa.
* Lưu trữ dữ liệu bằng hệ quản trị cơ sở dữ liệu NoSQL.
* Triển khai backend API và giao diện người dùng.
* Hỗ trợ mở rộng thành hệ thống semantic search hoặc chatbot RAG trong tương lai.

---

### 1.3 Bài toán thực tế

Trong thực tế, phần lớn dữ liệu tồn tại dưới dạng phi cấu trúc như:

* Tin tức
* Tài liệu
* Bài viết
* Bình luận
* Báo cáo
* Nội dung mạng xã hội

Các hệ quản trị CSDL truyền thống gặp khó khăn trong:

* Tìm kiếm ngữ nghĩa
* Khả năng mở rộng
* Xử lý dữ liệu text lớn
* Tìm kiếm theo nội dung thay vì keyword

Do đó hệ thống sẽ sử dụng:

* MongoDB để lưu trữ document
* FAISS để vector search
* Sentence Transformer để embedding

---

# 2. Công nghệ sử dụng

## 2.1 Backend

* Python 3.11+
* FastAPI
* Uvicorn

---

## 2.2 Database

### MongoDB

Dùng để:

* Lưu document
* Metadata
* Nội dung text
* Thông tin category
* Timestamp

---

### FAISS

Dùng để:

* Vector similarity search
* Semantic search
* Cosine similarity

---

## 2.3 NLP

### sentence-transformers

Model đề xuất:

```python
all-MiniLM-L6-v2
```

Dùng để:

* Chuyển văn bản thành vector embedding
* Semantic search

---

## 2.4 Frontend

### Streamlit

Dùng để:

* Tạo giao diện nhanh
* Search documents
* Hiển thị kết quả

---

## 2.5 Công cụ phát triển

* VSCode
* Git
* GitHub
* Postman
* Docker (optional)

---

# 3. Kiến trúc hệ thống

## 3.1 Tổng quan kiến trúc

```text
Dataset
   ↓
Preprocessing
   ↓
Embedding Generation
   ↓
MongoDB + FAISS
   ↓
FastAPI Backend
   ↓
Streamlit Frontend
```

---

## 3.2 Luồng hoạt động

### Bước 1

Thu thập dữ liệu.

### Bước 2

Tiền xử lý dữ liệu text.

### Bước 3

Sinh vector embedding.

### Bước 4

Lưu:

* Document → MongoDB
* Embedding → FAISS

### Bước 5

Người dùng nhập query.

### Bước 6

Query được embedding.

### Bước 7

FAISS tìm vector gần nhất.

### Bước 8

Trả kết quả về frontend.

---

# 4. Cấu trúc thư mục dự án

```text
project-root/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   ├── database/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── embeddings/
│
├── notebooks/
│
├── scripts/
│   ├── preprocess.py
│   ├── generate_embeddings.py
│   └── import_data.py
│
├── faiss_index/
│
├── docs/
│   ├── report/
│   └── presentation/
│
├── README.md
├── .gitignore
└── docker-compose.yml
```

---

# 5. Dataset

## 5.1 Dataset sử dụng

Vietnamese Online News Dataset

---

## 5.2 Nguồn dataset

* Kaggle

---

## 5.3 Cấu trúc dữ liệu

Ví dụ document:

```json
{
  "title": "AI đang thay đổi thế giới",
  "content": "Nội dung bài viết...",
  "category": "technology",
  "author": "abc",
  "created_at": "2026-05-22"
}
```

---

# 6. Tiền xử lý dữ liệu

## 6.1 Các bước preprocessing

### Lowercase

```python
text = text.lower()
```

---

### Remove Special Characters

Loại bỏ:

* ký tự đặc biệt
* URL
* emoji
* HTML tags

---

### Tokenization

Tách từ.

---

### Remove Stopwords

Ví dụ:

* và
* là
* của
* the
* is

---

### Remove Duplicates

Xóa dữ liệu trùng lặp.

---

# 7. Embedding và Semantic Search

## 7.1 Embedding

Embedding là quá trình chuyển text thành vector số.

Ví dụ:

```text
"machine learning"
↓
[0.12, 0.98, 0.44, ...]
```

---

## 7.2 Model embedding

### Sentence Transformer

Model:

```python
all-MiniLM-L6-v2
```

---

## 7.3 Semantic Search

Thay vì:

```text
keyword matching
```

Hệ thống dùng:

```text
meaning matching
```

Ví dụ:

Query:

```text
AI trong giáo dục
```

Vẫn có thể tìm:

```text
Ứng dụng trí tuệ nhân tạo trong học tập
```

---

# 8. MongoDB Design

## 8.1 Collection

### documents

---

## 8.2 Schema

```json
{
  "_id": "ObjectId",
  "title": "string",
  "content": "string",
  "category": "string",
  "embedding_id": "int",
  "created_at": "datetime"
}
```

---

# 9. FAISS Design

## 9.1 Chức năng

* Vector indexing
* Similarity search
* Fast nearest neighbor search

---

## 9.2 Quy trình

```text
Document
   ↓
Embedding
   ↓
FAISS Index
```

---

# 10. Backend API

## 10.1 Framework

FastAPI

---

## 10.2 API endpoints

### GET /

Health check.

---

### POST /documents

Thêm document.

Request:

```json
{
  "title": "sample",
  "content": "sample content"
}
```

---

### GET /documents

Lấy danh sách document.

---

### POST /search

Search semantic.

Request:

```json
{
  "query": "machine learning"
}
```

Response:

```json
[
  {
    "title": "AI article",
    "score": 0.91
  }
]
```

---

# 11. Frontend

## 11.1 Chức năng

* Search documents
* Hiển thị kết quả
* Hiển thị similarity score

---

## 11.2 UI components

### Search Box

Người dùng nhập query.

---

### Search Results

Hiển thị:

* Title
* Content preview
* Similarity score

---

### Filters

Optional:

* category
* date

---

# 12. Quy trình phát triển phần mềm

## 12.1 Git Workflow

### Branches

```text
main
```

Production-ready.

```text
dev
```

Development branch.

```text
feature/*
```

Feature branches.

```text
feature/backend-core
Caotiendev (frontend)
feature/data-nlp-books
```

---

## 12.2 Quy tắc commit

Format:

```text
feat: add semantic search API
fix: resolve mongodb connection bug
refactor: clean preprocessing module
```

---

## 12.3 Pull Request Rules

* Không push trực tiếp vào main.
* Merge qua dev.
* Code review trước khi merge.

---

# 13. Cài đặt môi trường

## 13.1 Clone project

```bash
git clone https://github.com/namlav/textno.git
```

---

## 13.2 Backend setup

```bash
cd backend
pip install -r requirements.txt
```

---

## 13.3 Frontend setup

```bash
cd frontend
pip install -r requirements.txt
```

---

## 13.4 Run backend

```bash
cd backend
uvicorn app.main:app --reload
```

---

## 13.5 Run frontend

```bash
streamlit run app.py
```

---

# 14. Dependencies đề xuất

## Backend requirements.txt

```text
fastapi
uvicorn
pymongo
sentence-transformers
faiss-cpu
numpy
pandas
python-dotenv
scikit-learn
```

---

## Frontend requirements.txt

```text
streamlit
requests
pandas
```

---

# 15. Environment Variables

## .env

```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=text_management_db
COLLECTION_NAME=documents
```

---

# 16. Core Modules

## 16.1 Preprocessing Module

Chức năng:

* clean text
* normalize text
* remove stopwords

---

## 16.2 Embedding Module

Chức năng:

* load transformer model
* generate embeddings

---

## 16.3 Search Module

Chức năng:

* query embedding
* vector search
* similarity ranking

---

## 16.4 MongoDB Module

Chức năng:

* insert documents
* fetch documents
* update documents

---

# 17. Pipeline chi tiết

## Data Ingestion Pipeline

```text
Dataset
   ↓
Load Data
   ↓
Clean Data
   ↓
Generate Embeddings
   ↓
Store MongoDB
   ↓
Store FAISS Index
```

---

## Search Pipeline

```text
User Query
   ↓
Preprocess Query
   ↓
Generate Query Embedding
   ↓
FAISS Similarity Search
   ↓
Retrieve Documents
   ↓
Return Results
```

---

# 18. Testing

## 18.1 Backend Testing

Test:

* API endpoints
* MongoDB connection
* Search accuracy

---

## 18.2 Frontend Testing

Test:

* Search flow
* UI rendering
* Error handling

---

## 18.3 Performance Testing

Test:

* Search latency
* Number of documents
* Response time

---

# 19. Hướng phát triển

## Future Improvements

### Chatbot RAG

Tích hợp:

* LLM
* Retrieval Augmented Generation

---

### Elasticsearch

Thay thế hoặc kết hợp FAISS.

---

### Cloud Deployment

Deploy:

* Render
* Railway
* AWS
* Docker

---

### Authentication

Thêm:

* login
* JWT auth
* role management

---

### Multi-language Support

Hỗ trợ:

* Vietnamese
* English
* multilingual embedding

---

# 20. Phân công nhóm

## Thành viên 1 – Backend + Search

### Công việc

* FastAPI
* MongoDB integration
* FAISS search
* API development

---

## Thành viên 2 – Data + NLP

### Công việc

* Dataset
* Preprocessing
* Embeddings
* Testing search quality

---

## Thành viên 3 – Frontend + Documentation

### Công việc

* Streamlit UI
* PPT
* Report
* Demo

---

# 21. Timeline

## Week 1

* Chọn dataset
* Setup project
* Thiết kế database
* Setup MongoDB

---

## Week 2

* Preprocessing
* Embedding generation
* Build search engine

---

## Week 3

* API development
* Frontend UI
* Integration

---

## Week 4

* Testing
* Fix bugs
* PPT
* Final demo

---

# 22. Coding Standards

## Python Style

* PEP8
* Type hints
* Docstrings

---

## Naming Convention

### Variables

```python
snake_case
```

### Classes

```python
PascalCase
```

### Constants

```python
UPPER_CASE
```

---

# 23. README Requirements

README phải có:

* Project overview
* Features
* Installation guide
* Run instructions
* API docs
* Tech stack
* Demo screenshots

---

# 24. Demo Scenario

## Demo Flow

### Step 1

Import dataset.

### Step 2

Generate embeddings.

### Step 3

Search query.

### Step 4

Hiển thị semantic results.

### Step 5

So sánh keyword search vs semantic search.

---

# 25. Tiêu chí hoàn thành project

## Functional Requirements

* CRUD documents
* Semantic search
* MongoDB storage
* Frontend interface

---

## Non-functional Requirements

* Fast search
* Clean architecture
* Readable code
* Easy scalability

---

# 26. Mục tiêu nâng cao

## Optional Features

* User authentication
* Admin dashboard
* Search analytics
* Recommendation system
* Document summarization

---

# 27. Kết luận

Dự án tập trung vào:

* Quản lý dữ liệu phi cấu trúc
* Semantic search
* NoSQL database
* NLP applications
* Information retrieval

Hệ thống có thể mở rộng thành:

* Enterprise search engine
* AI assistant
* Knowledge management system
* RAG chatbot platform
