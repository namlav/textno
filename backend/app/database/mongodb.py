# mongodb.py - Kết nối và thao tác với MongoDB
#
# Kỹ thuật:
# - Singleton pattern: client được tạo một lần duy nhất, tái sử dụng cho mọi request
# - get_collection() cung cấp interface đơn giản để CRUD collection "documents"
# - close_connection() dọn dẹp tài nguyên khi server shutdown

from pymongo import MongoClient
from pymongo.collection import Collection
from app.core.config import settings

client: MongoClient | None = None


def get_client() -> MongoClient:
    global client
    if client is None:
        client = MongoClient(settings.MONGODB_URI)
    return client


def get_collection() -> Collection:
    db = get_client()[settings.DATABASE_NAME]
    return db[settings.COLLECTION_NAME]


def close_connection():
    global client
    if client:
        client.close()
        client = None
