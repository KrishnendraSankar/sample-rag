from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass
class Chunk:
    """
    Represents one searchable piece of a document.
    """

    # Globally unique ID for this chunk.
    id: UUID

    # ID of the parent document.
    document_id: UUID

    # Position of this chunk inside the document.
    sequence: int

    # Actual text stored in MongoDB.
    text: str

    # Format-specific metadata.
    #
    # Examples:
    #
    # PDF:
    # {
    #     "page_number": 12,
    #     "source": "employee_handbook.pdf",
    #     "file_type": "pdf"
    # }
    #
    # Markdown later:
    # {
    #     "heading": "Leave Policy",
    #     "source": "handbook.md",
    #     "file_type": "markdown"
    # }
    metadata: dict[str, Any] = field(default_factory=dict)
