"""
app/ingestion/markdown_loader.py

Production-ready Markdown Loader using LangChain's
UnstructuredMarkdownLoader.

Features
--------
- YAML Front Matter extraction
- Uses UnstructuredMarkdownLoader for parsing
- Supports paragraphs, headings, tables, lists, links, etc.
- Ignores implementation complexity of markdown parsing
- Returns MarkdownDocument compatible with the existing project

Required Packages
-----------------
pip install langchain-community
pip install unstructured
pip install markdown
pip install pyyaml
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple
from uuid import UUID, uuid4

import yaml
from langchain_community.document_loaders import UnstructuredMarkdownLoader

from app.models.markdown_models import (
    MarkdownDocument,
    MarkdownSection,
)


class MarkdownLoader:
    """Markdown document loader."""

    def load(self, file_path: str | Path) -> MarkdownDocument:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        metadata, markdown_body = self._extract_front_matter(path)

        metadata["source"] = path.name
        metadata["file_type"] = "markdown"

        loader = UnstructuredMarkdownLoader(
            file_path=str(path),
            mode="elements",
        )

        documents = loader.load()

        sections = self._build_sections(
            documents,
            metadata,
        )

        return MarkdownDocument(
            document_id=uuid4(),
            metadata=metadata,
            sections=sections,
        )

    ###########################################################################
    # YAML FRONT MATTER
    ###########################################################################

    def _extract_front_matter(
        self,
        path: Path,
    ) -> Tuple[Dict[str, Any], str]:

        text = path.read_text(encoding="utf-8")

        if not text.startswith("---"):
            return {}, text

        lines = text.splitlines()

        end = None

        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break

        if end is None:
            return {}, text

        yaml_text = "\n".join(lines[1:end])

        markdown_body = "\n".join(lines[end + 1 :])

        metadata = yaml.safe_load(yaml_text) or {}

        return metadata, markdown_body

    ###########################################################################
    # BUILD SECTIONS
    ###########################################################################

    def _build_sections(
        self,
        documents,
        document_metadata: Dict[str, Any],
    ) -> List[MarkdownSection]:

        sections: List[MarkdownSection] = []

        hierarchy: Dict[int, str] = {}

        current_heading = "Document"
        current_heading_level = 0

        current_content: List[str] = []

        for document in documents:

            element_type = document.metadata.get(
                "category",
                "",
            )

            text = (document.page_content or "").strip()

            if not text:
                continue

            ###################################################################
            # TITLE / HEADINGS
            ###################################################################

            if element_type in (
                "Title",
                "Header",
            ):

                if current_content:

                    sections.append(
                        MarkdownSection(
                            heading_level=current_heading_level,
                            heading=current_heading,
                            hierarchy=hierarchy.copy(),
                            content="\n\n".join(current_content),
                            metadata=document_metadata.copy(),
                        )
                    )

                    current_content = []

                depth = document.metadata.get("category_depth")
                if depth is not None:
                    try:
                        level = int(depth) + 1
                    except (ValueError, TypeError):
                        level = self._detect_heading_level(text)
                else:
                    level = self._detect_heading_level(text)

                hierarchy = {k: v for k, v in hierarchy.items() if k < level}

                hierarchy[level] = text

                current_heading = text
                current_heading_level = level

                continue

            ###################################################################
            # TABLE
            ###################################################################

            if element_type == "Table":

                current_content.append(text)

                continue

            ###################################################################
            # LIST
            ###################################################################

            if element_type in (
                "ListItem",
                "BulletedText",
            ):

                current_content.append(f"- {text}")

                continue

            ###################################################################
            # IMAGE
            ###################################################################

            if element_type == "Image":

                current_content.append(f"[Image] {text}")

                continue

            ###################################################################
            # DEFAULT
            ###################################################################

            current_content.append(text)

        if current_content:

            sections.append(
                MarkdownSection(
                    heading=current_heading,
                    heading_level=current_heading_level,
                    hierarchy=hierarchy.copy(),
                    content="\n\n".join(current_content),
                    metadata=document_metadata.copy(),
                )
            )

        return sections

    ###########################################################################
    # HEADING LEVEL
    ###########################################################################

    def _detect_heading_level(
        self,
        heading: str,
    ) -> int:
        """
        Unstructured does not expose markdown heading level.

        If markdown parser preserves '#',
        derive the level.

        Otherwise default to H1.
        """

        stripped = heading.lstrip()

        if stripped.startswith("#"):

            count = 0

            for ch in stripped:
                if ch == "#":
                    count += 1
                else:
                    break

            return min(count, 6)

        return 1
