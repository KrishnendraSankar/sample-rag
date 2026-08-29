# app/ingestion/docx_loader.py

from pathlib import Path

from docx import Document as DocxDocument


class DOCXLoader:
    """
    Extract structured content from a DOCX file.

    Instead of returning one giant string,
    we preserve:

    - headings
    - heading levels
    - normal paragraphs

    This information will later be used by
    DOCXChunker to create section-aware chunks.
    """

    def load(
        self,
        file_path: str,
    ) -> list[dict]:

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                f"DOCX file not found: {file_path}"
            )

        if path.suffix.lower() != ".docx":

            raise ValueError(
                "DOCXLoader only supports .docx files."
            )

        document = DocxDocument(
            str(path)
        )

        elements = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            # Ignore empty paragraphs.
            if not text:
                continue

            style_name = ""

            if paragraph.style:
                style_name = (
                    paragraph.style.name or ""
                )

            # -----------------------------------
            # Detect Word heading styles:
            #
            # Heading 1
            # Heading 2
            # Heading 3
            # ...
            # -----------------------------------

            if style_name.lower().startswith(
                "heading"
            ):

                level = self._get_heading_level(
                    style_name
                )

                elements.append(
                    {
                        "type": "heading",

                        "level": level,

                        "text": text,
                    }
                )

            else:

                elements.append(
                    {
                        "type": "paragraph",

                        "text": text,
                    }
                )

        return elements

    @staticmethod
    def _get_heading_level(
        style_name: str,
    ) -> int:
        """
        Convert:

        Heading 1 → 1
        Heading 2 → 2

        If the heading level cannot be determined,
        default to level 1.
        """

        try:

            return int(
                style_name.split()[-1]
            )

        except (
            ValueError,
            IndexError,
        ):

            return 1