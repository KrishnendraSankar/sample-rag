from docx import Document

from app.ingestion.loaders.base import DocumentLoader


class DOCXLoader(DocumentLoader):

    def load(self, file_path: str) -> str:
        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)