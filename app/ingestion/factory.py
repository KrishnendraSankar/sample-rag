from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.loaders.docx_loader import DOCXLoader
from app.ingestion.loaders.txt_loader import TXTLoader
from app.ingestion.loaders.markdown_loader import MarkdownLoader


class LoaderFactory:

    loaders = {

        ".pdf": PDFLoader(),

        ".docx": DOCXLoader(),

        ".txt": TXTLoader(),

        ".md": MarkdownLoader()

    }

    @classmethod
    def get_loader(cls, extension):

        if extension not in cls.loaders:

            raise Exception(
                f"Unsupported file type {extension}"
            )

        return cls.loaders[extension]