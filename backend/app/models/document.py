from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)

    language = Column(String, nullable=True)

    content = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)