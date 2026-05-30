import chromadb

from sentence_transformers import SentenceTransformer

from app.config import settings


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_DIR
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def add_document(
        self,
        document_id: int,
        text: str,
    ):
        embedding = self.embedding_model.encode(
            text
        ).tolist()

        self.collection.add(
            ids=[str(document_id)],
            embeddings=[embedding],
            documents=[text],
            metadatas=[
                {
                    "document_id": document_id
                }
            ],
        )

    def search(
        self,
        document_id: int,
        query: str,
        n_results: int = 1,
    ):
        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={
                "document_id": document_id
            },
        )

        return results