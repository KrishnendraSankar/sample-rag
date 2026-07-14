from sqlalchemy import DeclarativeBase
from sqlalchemy import Mapped
from sqlalchemy import mapped_column

from datetime import datetime
from uuid import uuid4

class Base(DeclarativeBase):
    pass

class DocumentMetaData(Base):
    __tablename__ = "documents"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    filename: Mapped[str]
    file_type: Mapped[str]
    file_size: Mapped[int]
    upload_time: Mapped[datetime]
    processing_status: Mapped[str]
    embedding_model: Mapped[str]
    total_chunks: Mapped[int]
