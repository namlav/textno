# routes.py - Các API endpoints cho hệ thống
#
# RESTful API:
#   POST /documents     - Tạo document mới, tự động sinh embedding vector và lưu vào FAISS
#   GET  /documents     - Lấy danh sách tất cả documents từ MongoDB
#   GET  /documents/:id - Lấy chi tiết một document theo ObjectId
#   DELETE /documents/:id - Xoá document
#   POST /search        - Tìm kiếm ngữ nghĩa (semantic search) dùng vector similarity
#
# Kỹ thuật:
# - Mỗi document khi tạo đều chạy pipeline: nhúng văn bản -> vector -> FAISS index
# - Tìm kiếm dùng FAISS (Inner Product ~ Cosine Similarity) thay vì MongoDB text search
# - Kết quả tìm được từ FAISS mapping ngược về MongoDB qua embedding_id

import logging
import time as time_module

from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
from app.models.document import DocumentCreate, DocumentResponse, SearchResult, SearchComparisonResult
from app.database.mongodb import get_collection
from app.services.embedding import generate_embedding
from app.services.search import add_embedding, search as faiss_search
from app.services import tfidf_search

logger = logging.getLogger(__name__)


def _safe_str(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, list):
        return ",".join(str(v) for v in value)
    if not isinstance(value, str):
        return str(value)
    return value


def _safe_int(value) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

router = APIRouter()


@router.get("/")
def health_check():
    return {"status": "ok", "message": "Text Document Management System API"}


@router.post("/documents", response_model=DocumentResponse)
def create_document(doc: DocumentCreate):
    # Bước 1: Tạo vector embedding cho nội dung document
    embedding = generate_embedding(f"{doc.title} {doc.content}")
    # Bước 2: Lưu vector vào FAISS index và lấy embedding_id
    embedding_id = add_embedding(embedding)

    # Bước 3: Lưu document vào MongoDB kèm embedding_id để mapping sau này
    doc_dict = doc.model_dump()
    doc_dict["embedding_id"] = embedding_id
    doc_dict["created_at"] = datetime.utcnow()

    collection = get_collection()
    result = collection.insert_one(doc_dict)
    doc_dict["_id"] = str(result.inserted_id)
    return doc_dict


@router.get("/documents", response_model=list[DocumentResponse])
def list_documents():
    collection = get_collection()
    docs = list(collection.find())
    docs.sort(key=lambda d: d.get("created_at") or "", reverse=True)
    results = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results


@router.get("/documents/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: str):
    collection = get_collection()
    try:
        doc = collection.find_one({"_id": ObjectId(doc_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid document ID")
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc["_id"] = str(doc["_id"])
    return doc


@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str):
    collection = get_collection()
    try:
        result = collection.delete_one({"_id": ObjectId(doc_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid document ID")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted"}


@router.post("/search", response_model=list[SearchResult])
def search_documents(query: str, top_k: int = 5):
    try:
        collection = get_collection()
        results = faiss_search(query, top_k)
        if not results:
            return []

        embedding_ids = [eid for eid, _ in results]
        doc_map = {}
        for doc in collection.find({"embedding_id": {"$in": embedding_ids}}):
            doc_map[doc.get("embedding_id")] = doc

        search_results = []
        for embedding_id, score in results:
            doc = doc_map.get(embedding_id)
            if doc:
                search_results.append(SearchResult(
                    id=str(doc["_id"]),
                    title=doc.get("title", "") or "",
                    content=doc.get("content", "") or "",
                    category=_safe_str(doc.get("category")),
                    author=_safe_str(doc.get("author")),
                    publication=_safe_str(doc.get("publication")),
                    tags=_safe_str(doc.get("tags")),
                    created_at=doc.get("created_at"),
                    wordcount=_safe_int(doc.get("wordcount")),
                    score=score,
                ))
        return search_results
    except Exception:
        logger.exception("Search failed")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/search/tfidf", response_model=list[SearchResult])
def search_documents_tfidf(query: str, top_k: int = 5):
    return tfidf_search.search(query, top_k)


@router.post("/search/compare", response_model=SearchComparisonResult)
def search_documents_compare(query: str, top_k: int = 5):
    try:
        t0 = time_module.time()
        semantic_results = faiss_search(query, top_k)
        semantic_time = round(time_module.time() - t0, 4)

        collection = get_collection()
        embedding_ids = [eid for eid, _ in semantic_results]
        doc_map = {}
        for doc in collection.find({"embedding_id": {"$in": embedding_ids}}):
            doc_map[doc.get("embedding_id")] = doc

        semantic_rich = []
        for embedding_id, score in semantic_results:
            doc = doc_map.get(embedding_id)
            if doc:
                semantic_rich.append(SearchResult(
                    id=str(doc["_id"]),
                    title=doc.get("title", "") or "",
                    content=doc.get("content", "") or "",
                    category=_safe_str(doc.get("category")),
                    author=_safe_str(doc.get("author")),
                    publication=_safe_str(doc.get("publication")),
                    tags=_safe_str(doc.get("tags")),
                    created_at=doc.get("created_at"),
                    wordcount=_safe_int(doc.get("wordcount")),
                    score=score,
                ))

        t1 = time_module.time()
        tfidf_raw = tfidf_search.search(query, top_k)
        tfidf_time = round(time_module.time() - t1, 4)

        tfidf_rich = [SearchResult(
            id=r.get("id", ""),
            title=r.get("title", "") or "",
            content=r.get("content", "") or "",
            category=_safe_str(r.get("category")),
            author=_safe_str(r.get("author")),
            publication=_safe_str(r.get("publication")),
            tags=_safe_str(r.get("tags")),
            created_at=r.get("created_at"),
            wordcount=_safe_int(r.get("wordcount")),
            score=float(r.get("score", 0.0)),
        ) for r in tfidf_raw]

        return SearchComparisonResult(
            semantic=semantic_rich,
            tfidf=tfidf_rich,
            semantic_time=semantic_time,
            tfidf_time=tfidf_time,
            query=query,
        )
    except Exception:
        logger.exception("Search compare failed")
        raise HTTPException(status_code=500, detail="Internal server error")
