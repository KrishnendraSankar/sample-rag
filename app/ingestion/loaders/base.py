from abc import ABC, abstractmethod

class DocumentLoader(ABC):
    @abstractmethod
    def load(self, file_path: str)-> str:
        """Return extracted text from the document."""
        raise NotImplementedError