from pymongo import MongoClient

from app.config.settings import settings


class MongoService:

    def __init__(self):

        self.client = MongoClient(settings.MONGO_URI)

        self.db = self.client[settings.MONGO_DB]

        self.collection = self.db.documents

        return
    
    def save_document( self, document, chunks):

        mongo_chunks = []

        for chunk in chunks:

            mongo_chunks.append({

                "chunk_id": chunk.chunk_id,

                "text": chunk.text

            })

        self.collection.insert_one({

            "document_id": str(document.id),

            "filename": document.filename,

            "content": document.content,

            "chunks": mongo_chunks

        })
        return
    
    def get_chunk(self, document_id, chunk_id):

        document = self.collection.find_one({

            "document_id": document_id

        })

        if not document:

            return None

        for chunk in document["chunks"]:

            if chunk["chunk_id"] == chunk_id:

                return chunk["text"]

        return None