from pathlib import Path
from uuid import uuid4
from datetime import datetime

from app.models.document import Document


def create_document(file_path: str, content: str):

    path = Path(file_path)

    return Document(

        id=uuid4(),

        filename=path.name,

        file_type=path.suffix,

        file_size=path.stat().st_size,

        content=content,

        uploaded_at=datetime.utcnow()
    )