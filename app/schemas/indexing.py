from pydantic import BaseModel, Field
from typing import Any

class IndexingResponse(BaseModel):
    """
    Response returned by the indexing endpoint.
    """
    message: str = Field(..., description="Status message of the indexing operation")
    result: Any | None = Field(default=None, description="Result details from the indexing pipeline")
