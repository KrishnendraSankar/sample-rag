# app/rag/docx_chunker.py

from uuid import UUID, uuid4

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from app.models.chunk import Chunk


class DOCXChunker:

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
        elements: list[dict],
    ) -> list[Chunk]:

        chunks = []

        sequence = 1

        # Stores the current heading hierarchy.
        #
        # Example:
        #
        # {
        #     1: "Employee Handbook",
        #     2: "Leave Policy",
        #     3: "Casual Leave"
        # }

        heading_context = {}

        # Text accumulated under the current
        # heading context.
        section_paragraphs = []

        # ---------------------------------------
        # Helper function:
        #
        # Convert accumulated paragraphs into
        # chunks before moving to a new section.
        # ---------------------------------------

        def flush_section():

            nonlocal sequence

            if not section_paragraphs:
                return

            section_text = "\n\n".join(section_paragraphs)

            split_texts = self.splitter.split_text(section_text)

            for text in split_texts:

                metadata = {
                    "source": filename,
                    "file_type": "docx",
                }

                # Add active heading hierarchy
                # into chunk metadata.

                for (
                    level,
                    heading,
                ) in heading_context.items():

                    metadata[f"heading_{level}"] = heading

                chunks.append(
                    Chunk(
                        id=uuid4(),
                        document_id=document_id,
                        sequence=sequence,
                        text=text,
                        metadata=metadata,
                    )
                )

                sequence += 1

            section_paragraphs.clear()

        # ---------------------------------------
        # Process document elements
        # ---------------------------------------

        for element in elements:

            element_type = element["type"]

            # -----------------------------------
            # Heading encountered
            # -----------------------------------

            if element_type == "heading":

                # First save text belonging to
                # the previous section.
                flush_section()

                level = element["level"]

                heading_text = element["text"]

                # Update current heading.
                heading_context[level] = heading_text

                # Remove deeper headings.
                #
                # Example:
                #
                # H1 Company
                # H2 HR
                # H3 Leave
                #
                # Then new H2 Finance appears.
                #
                # H3 Leave must be removed.

                deeper_levels = [
                    existing_level
                    for existing_level in heading_context
                    if existing_level > level
                ]

                for deeper_level in deeper_levels:

                    del heading_context[deeper_level]

            # -----------------------------------
            # Normal paragraph
            # -----------------------------------

            elif element_type == "paragraph":

                section_paragraphs.append(element["text"])

        # ---------------------------------------
        # Flush final section
        # ---------------------------------------

        flush_section()

        return chunks

    def build_embedding_text(self, chunk: Chunk) -> str:

        context_parts = []

        # Preserve heading order:
        #
        # heading_1
        # heading_2
        # heading_3
        # ...

        heading_keys = sorted(
            key for key in chunk.metadata if key.startswith("heading_")
        )

        for key in heading_keys:

            heading = chunk.metadata.get(key)

            if heading:

                context_parts.append(heading)

        context_parts.append(chunk.text)

        return "\n\n".join(context_parts)
