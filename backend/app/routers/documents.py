from fastapi import APIRouter, UploadFile, File
from sqlalchemy import select

from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.database import AsyncSessionLocal

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

    document = Document(
        filename=file.filename,
        file_type=file.content_type,
        content=content.decode("utf-8", errors="ignore"),
    )

    async with AsyncSessionLocal() as session:
        session.add(document)
        await session.commit()
        await session.refresh(document)

    return document


@router.get("/", response_model=list[DocumentResponse])
async def get_documents():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Document))
        documents = result.scalars().all()

    return documents