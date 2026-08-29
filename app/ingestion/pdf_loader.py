from pathlib import Path

from pypdf import PdfReader


class PDFLoader:
    """
    Extract text from a PDF page-by-page.

    We intentionally preserve page boundaries
    because page numbers are valuable metadata
    for RAG citations and debugging.
    """

    def load(
        self,
        file_path: str,
    ) -> list[dict]:

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":

            raise ValueError(
                "PDFLoader only supports PDF files."
            )

        reader = PdfReader(
            str(path)
        )

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):

            text = page.extract_text()

            # Some PDF pages may contain no
            # extractable text.
            if not text:
                continue

            text = text.strip()

            if not text:
                continue

            pages.append(
                {
                    "page_number": page_number,

                    "text": text,
                }
            )

        return pages