import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "text_management_db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "documents")
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2"
    )

    # FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "../faiss_index/index.faiss")
    # Lấy đường dẫn tuyệt đối đến thư mục chứa file config.py này (thư mục core)
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Đi ngược lên 2 cấp để tìm ra thư mục gốc của dự án (thư mục textno)
    # core -> app -> backend -> textno
    PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))

    # Định vị chính xác file index.faiss dựa trên thư mục gốc dự án
    FAISS_INDEX_PATH = os.path.join(PROJECT_ROOT, "faiss_index", "index.faiss")

    EMBEDDING_DIM: int = 384


settings = Settings()
