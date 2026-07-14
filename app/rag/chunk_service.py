from app.models.chunk import Chunk

class ChunkService:
    def create_chunk(self, document, chunks: list[str]) -> list[Chunk]:
        """Create a list of Chunk objects from a document and its chunks."""
        result = []
        for index, chunk in enumerate(chunks, start=1):
            result.append(
                Chunk(
                    document_id=document.id,
                    chunk_id=index,
                    text=chunk
                )
            )
        return result