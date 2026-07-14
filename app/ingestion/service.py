from pathlib import Path

from app.ingestion.factory import LoaderFactory
from app.ingestion.metadata import create_document

class IngestionService:
    
    def ingest(self, file_path: str):
        extension = Path(file_path).suffix.lower()
        loader = LoaderFactory.get_loader(extension)
        content = loader.load(file_path)
        document = create_document(file_path=file_path, content=content)
        return document