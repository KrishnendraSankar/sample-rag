from pymongo import MongoClient
from app.config.settings import settings

client = MongoClient(settings.MONGO_URI)
try:
    db = client[settings.MONGO_DB]
    print("Connected to MongoDB")
    print(f"Database: {settings.MONGO_DB}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")