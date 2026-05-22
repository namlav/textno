from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
from app.models.document import DocumentCreate, DocumentResponse, SearchResult
from app.database.mongodb import get_collection
from app.services.embedding import generate_embedding
from app.services.search import add_embedding, search as faiss_search

router = APIRouter()


@router.get("/")
def health_check():
    return {"status": "ok", "message": "Text Document Management System API"}


@router.post("/documents", response_model=DocumentResponse)
def create_document(doc: DocumentCreate):
    embedding = generate_embedding(f"{doc.title} {doc.content}")
    embedding_id = add_embedding(embedding)

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
    docs = collection.find().sort("created_at", -1)
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
    collection = get_collection()
    results = faiss_search(query, top_k)

    if not results:
        return []

    search_results = []
    for embedding_id, score in results:
        doc = collection.find_one({"embedding_id": embedding_id})
        if doc:
            search_results.append(SearchResult(
                id=str(doc["_id"]),
                title=doc["title"],
                content=doc["content"],
                category=doc.get("category"),
                score=score,
            ))
    return search_results
