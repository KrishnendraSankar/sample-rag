# app/schemas/query.py

from pydantic import BaseModel, Field
from app.models.retrieved_chunk import RetrievedChunk

class QueryRequest(BaseModel):
    """
    Request body for the RAG query endpoint.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask the RAG system",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of relevant chunks to retrieve",
    )


class QueryResponse(BaseModel):
    """
    Final response returned by the RAG API.
    """

    question: str

    answer: str

    sources: list[RetrievedChunk]