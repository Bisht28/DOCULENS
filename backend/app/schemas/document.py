from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DocumentBase(BaseModel):
    filename: str
    file_type: str
    language: Optional[str] = None


class DocumentCreate(DocumentBase):
    content: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: int
    content: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True