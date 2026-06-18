import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.database.mongodb import get_collection, close_connection

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Text Document Management System",
    description="Hệ thống quản lý và tìm kiếm tài liệu văn bản phi cấu trúc",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def startup():
    try:
        collection = get_collection()
        existing = collection.index_information()
        if "embedding_id_1" not in existing:
            logger.info("Creating index on embedding_id...")
            collection.create_index("embedding_id", name="embedding_id_1")
            logger.info("Index created.")
        else:
            logger.info("Index on embedding_id already exists.")

        from app.services.tfidf_search import _ensure_index
        logger.info("Pre-building TF-IDF index (first load may take a while)...")
        _ensure_index()
        logger.info("TF-IDF index ready.")
    except Exception:
        logger.exception("Startup initialization error (non-fatal)")


@app.on_event("shutdown")
def shutdown():
    close_connection()
