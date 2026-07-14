from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Document:

    id: UUID

    filename: str

    file_type: str

    file_size: int

    content: str

    uploaded_at: datetime