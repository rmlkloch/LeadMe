import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Use the default sentence-transformers model (all-MiniLM-L6-v2) for $0 cost
default_ef = embedding_functions.DefaultEmbeddingFunction()

class VectorDBService:
    def __init__(self):
        # Initialize local ChromaDB client saving to ./data/chromadb
        db_path = os.path.join(os.getcwd(), "data", "chromadb")
        os.makedirs(db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Create or get the main collection for knowledge
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            embedding_function=default_ef
        )

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        """Add documents to the vector store."""
        if not documents:
            return
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search_similar(self, query: str, client_id: str = None, n_results: int = 3):
        """Search for similar documents. Optionally filter by client_id."""
        where = {"client_id": client_id} if client_id else None
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )
        return results

    def delete_knowledge_by_client(self, client_id: str):
        """Delete all knowledge associated with a specific client."""
        self.collection.delete(
            where={"client_id": client_id}
        )

vector_db_service = VectorDBService()
