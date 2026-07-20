import os
from qdrant_client import QdrantClient
from app.config.settings import settings

# Initialization using explicit environment variables (Recommended for security)
# Or pass strings directly: url="https://your-cluster-url.cloud.qdrant.io:6333"
print("API KEY:", settings.QDRANT_API_KEY)
print("API URL:", settings.QDRANT_URL)
client = QdrantClient(
    url=settings.QDRANT_URL, 
    api_key=settings.QDRANT_API_KEY,
)

# Verify the connection by listing existing collections
try:
    collections = client.get_collections()
    print("Successfully connected to Qdrant Cloud!")
    print(f"Active Collections: {collections}")
except Exception as e:
    print(f"Connection failed: {e}")
