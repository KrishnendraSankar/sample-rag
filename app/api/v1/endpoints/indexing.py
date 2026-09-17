# app/api/v1/endpoints/indexing.py

import os
import shutil
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File

from app.pipeline.indexing_pipeline import IndexingPipeline
from app.schemas.indexing import IndexingResponse

router = APIRouter(
    prefix="/indexing",
    tags=["Indexing"],
)

indexing_pipeline = IndexingPipeline()


@router.post("/upload", response_model=IndexingResponse)
async def upload_and_index(
    file: UploadFile = File(..., description="The document file to be indexed")
) -> IndexingResponse:
    """
    Upload a document and index it.
    """
    upload_dir = Path("app/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
        
    file_path = upload_dir / file.filename
    
    try:
        # Save uploaded file to disk
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Index document
        res = indexing_pipeline.index_document(str(file_path))
        
        return IndexingResponse(
            message="Document Indexed Successfully",
            result=res
        )

    except Exception as exc:
        print(f"Indexing failed: {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to index document: {str(exc)}",
        )
    finally:
        # Clean up the uploaded file after indexing
        if file_path.exists():
            try:
                os.remove(file_path)
            except Exception as cleanup_exc:
                print(f"Failed to delete uploaded file {file_path}: {cleanup_exc}")
