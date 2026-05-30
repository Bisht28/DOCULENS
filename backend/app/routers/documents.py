import os
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile
from sqlalchemy import select

from app.config import settings
from app.database import AsyncSessionLocal
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStore


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

processor = DocumentProcessor()
vector_store = VectorStore()


@router.post(
    "/upload",
    response_model=DocumentResponse,
)
async def upload_document(
    file: UploadFile = File(...),
):
    extension = os.path.splitext(file.filename)[1]

    unique_filename = f"{uuid4()}{extension}"

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        unique_filename,
    )

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    extracted_text = await processor.extract_text(file_path)

    language = processor.detect_language(
        extracted_text[:2000]
    )

    document = Document(
        filename=file.filename,
        file_type=file.content_type,
        language=language,
        content=extracted_text,
    )

    async with AsyncSessionLocal() as session:
        session.add(document)

        await session.commit()

        await session.refresh(document)

    if extracted_text.strip():
        vector_store.add_document(
            document_id=document.id,
            text=extracted_text,
        )

    return document


@router.get(
    "/",
    response_model=list[DocumentResponse],
)
async def get_documents():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Document)
        )

        documents = result.scalars().all()

    return documents