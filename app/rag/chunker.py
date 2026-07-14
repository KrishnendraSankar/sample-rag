from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional

class DocumentChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int =100, separators: Optional[List[str]]= ["\n\n", "\n", " ", ""]) -> None:
        """Create a chunker. Reuses a configured splitter for performance."""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators
        )

    def split(self, text: str):
        """Return text split into chunks (list of strings)."""
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        if text == "":
            return []
        return self.splitter.split_text(text)