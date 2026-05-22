from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DocumentCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    author: Optional[str] = None


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
    score: float
