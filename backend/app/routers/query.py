from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse
from app.services.vector_store import VectorStore


router = APIRouter(
    prefix="/query",
    tags=["Query"],
)

vector_store = VectorStore()


@router.post(
    "/",
    response_model=QueryResponse,
)
async def ask_question(
    request: QueryRequest,
):
    results = vector_store.search(
        document_id=request.document_id,
        query=request.question,
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    context = "\n".join(documents)

    return QueryResponse(
        question=request.question,
        answer=context,
    )