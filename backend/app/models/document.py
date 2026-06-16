# document.py - Định nghĩa cấu trúc dữ liệu (Pydantic models)
#
# Kỹ thuật:
# - Dùng Pydantic BaseModel để validate dữ liệu đầu vào/đầu ra API
# - DocumentCreate: model cho request tạo mới document
# - DocumentResponse: model cho response, bao gồm _id (MongoDB ObjectId) thời gian tạo
# - SearchResult: model riêng cho kết quả tìm kiếm kèm điểm số similarity

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DocumentCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    author: Optional[str] = None
    publication: Optional[str] = None
    tags: Optional[str] = None
    updatetime: Optional[str] = None
    wordcount: Optional[int] = None


class DocumentResponse(DocumentCreate):
    id: str = Field(alias="_id")
    embedding_id: Optional[int] = None
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True


class SearchResult(BaseModel):
    id: str
    title: str
    content: str
    category: Optional[str] = None
    author: Optional[str] = None
    publication: Optional[str] = None
    tags: Optional[str] = None
    created_at: Optional[datetime] = None
    wordcount: Optional[int] = None
    score: float
