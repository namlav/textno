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
