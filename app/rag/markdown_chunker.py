from __future__ import annotations

from uuid import uuid4
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.chunk import Chunk
from app.models.markdown_models import MarkdownDocument, MarkdownSection


class MarkdownChunker:
    """
    Splits a MarkdownDocument into embedding-ready chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:

        self.text_splitter = RecursiveCharacterTextSplitter(
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
        document: MarkdownDocument,
    ) -> List[Chunk]:

        chunks: List[Chunk] = []

        sequence = 1

        for section in document.sections:

            embedding_text = self._build_embedding_text(
                document,
                section,
            )

            split_texts = self.text_splitter.split_text(embedding_text)

            for text in split_texts:

                metadata = document.metadata.copy()
                metadata.update(section.metadata)

                for level, heading in section.hierarchy.items():
                    metadata[f"heading_{level}"] = heading

                chunks.append(
                    Chunk(
                        id=uuid4(),
                        document_id=document.document_id,
                        sequence=sequence,
                        text=text,
                        metadata=metadata,
                    )
                )

                sequence += 1

        return chunks

    def build_embedding_text(self, chunk: Chunk) -> str:
        context_parts = []
        heading_keys = sorted(
            key for key in chunk.metadata if key.startswith("heading_")
        )
        for key in heading_keys:
            heading = chunk.metadata.get(key)
            if heading:
                context_parts.append(heading)
        context_parts.append(chunk.text)
        return "\n\n".join(context_parts)

    def _build_embedding_text(
        self,
        document: MarkdownDocument,
        section: MarkdownSection,
    ) -> str:

        lines = []

        title = document.metadata.get("title")
        if title:
            lines.append(f"Title: {title}")

        for level in sorted(section.hierarchy.keys()):
            lines.append(f"Heading {level}: {section.hierarchy[level]}")

        lines.append("")
        lines.append(section.content)

        return "\n".join(lines).strip()
