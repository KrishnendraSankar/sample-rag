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

                "chunk_id": str(chunk.id),
                "sequence": chunk.sequence,
                "text": chunk.text

            })

        self.collection.insert_one({

            "document_id": str(document.id),
            "filename": document.filename,
            "content": document.content,
            "chunks": mongo_chunks

        })
        return
    
    def get_chunk(self, chunk_id: str):

        document = self.collection.find_one({
            "chunks.chunk_id": chunk_id
        },
        
        {
            "chunks.$": 1,
            "filename": 1
        })

        if not document:
            return None
        return {"chunks": document["chunks"][0], "filename": document.get("filename", "Unknown")}