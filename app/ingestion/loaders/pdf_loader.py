from pypdf import PdfReader
from app.ingestion.loaders.base import DocumentLoader

class PDFLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        pages = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)
        return "\n".join(pages)
            