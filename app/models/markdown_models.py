from dataclasses import dataclass, field
from typing import Dict, List, Any
from uuid import UUID


@dataclass
class MarkdownSection:
    """
    Represents one logical section within a Markdown document.

    A section begins at a heading and contains all content until the next
    heading of the same or higher level.
    """

    heading_level: int

    heading: str

    content: str

    hierarchy: Dict[int, str]

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MarkdownDocument:
    """
    Structured representation of an entire Markdown document.
    """

    document_id: UUID

    metadata: Dict

    sections: List[MarkdownSection]

    @property
    def id(self) -> UUID:
        return self.document_id

    @property
    def filename(self) -> str:
        return self.metadata.get("source", "Unknown")

    @property
    def content(self) -> str:
        return "\n\n".join(section.content for section in self.sections)
