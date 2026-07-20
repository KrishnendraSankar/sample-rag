# app/api/query.py

from fastapi import APIRouter, HTTPException

from app.pipeline.rag_pipeline import RAGPipeline
from app.schemas.query import (
    QueryRequest,
    QueryResponse,
)


router = APIRouter(
    prefix="/query",
    tags=["RAG Query"],
)


# Create the pipeline once.
#
# We do NOT want to recreate:
# - OpenAI client
# - MongoDB client
# - Qdrant client
#
# for every incoming request.
rag_pipeline = RAGPipeline()


@router.post(
    "",
    response_model=QueryResponse,
)
def query_rag(
    request: QueryRequest,
) -> QueryResponse:
    """
    Ask a question against indexed documents.
    """

    try:

        result = rag_pipeline.ask(
            question=request.question,
            top_k=request.top_k,
            score_threshold= request.score_threshold

        )

        return QueryResponse(
            **result
        )

    except Exception as exc:

        print(
            f"RAG query failed: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to process the RAG query.",
        )