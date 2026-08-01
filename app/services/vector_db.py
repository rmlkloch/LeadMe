# Vector DB service stub for future ChromaDB integration
class VectorDBService:
    def __init__(self) -> None:
        pass

    def add_documents(self, documents: list) -> None:
        raise NotImplementedError("Vector DB document insertion will be implemented in a future phase.")

    def query_similar(self, query: str, limit: int = 3) -> list:
        raise NotImplementedError("Vector DB querying will be implemented in a future phase.")
