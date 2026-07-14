from app.ingestion.loaders.base import DocumentLoader


class TXTLoader(DocumentLoader):

    def load(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()