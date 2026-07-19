from dataclasses import dataclass
from uuid import UUID

@dataclass
class RetrievedChunk:
    chunk_id: UUID
    sequence: int
    text: str
    document_name: str
    score: float