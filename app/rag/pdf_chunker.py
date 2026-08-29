from uuid import UUID, uuid4

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from app.models.chunk import Chunk


class PDFChunker:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def chunk(
        self,
        document_id: UUID,
        filename: str,
        pages: list[dict],
    ) -> list[Chunk]:

        chunks = []

        sequence = 1

        for page in pages:

            page_number = page["page_number"]

            page_text = page["text"]

            # Split only the current page.
            #
            # This prevents a chunk from silently
            # mixing text from unrelated pages.
            page_chunks = self.splitter.split_text(page_text)

            for text in page_chunks:

                chunk = Chunk(
                    # Every chunk gets its own
                    # globally unique UUID.
                    id=uuid4(),
                    document_id=document_id,
                    # Maintains global ordering
                    # across the entire PDF.
                    sequence=sequence,
                    text=text,
                    metadata={
                        "page_number": page_number,
                        "source": filename,
                        "file_type": "pdf",
                    },
                )

                chunks.append(chunk)

                sequence += 1

        return chunks
