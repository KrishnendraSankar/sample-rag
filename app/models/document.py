from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class Document:

    id: UUID

    filename: str

    content: str

    file_type: Optional[str] = None

    file_size: Optional[int] = None

    uploaded_at: Optional[datetime] = None