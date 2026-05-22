import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "text_management_db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "documents")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "../faiss_index/index.faiss")
    EMBEDDING_DIM: int = 384


settings = Settings()
