from datetime import datetime
import uuid
from app.services.vector_db import vector_db_service
from app.services.scraper import scraper_service

class IngestionService:
    def __init__(self):
        self.chunk_size = 500  # Words approximately
        self.chunk_overlap = 50

    def _chunk_text(self, text: str) -> list[str]:
        """Simple chunking by word count."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            chunks.append(chunk)
        return chunks

    def process_website(self, url: str, client_id: str):
        """Scrape website, chunk text, and store in vector DB."""
        raw_text = scraper_service.crawl_website(url)
        if not raw_text:
            raise ValueError("No text extracted from website.")
            
        chunks = self._chunk_text(raw_text)
        
        documents = []
        metadatas = []
        ids = []
        
        timestamp = datetime.utcnow().isoformat()
        
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                "source_url": url,
                "client_id": client_id,
                "timestamp": timestamp,
                "type": "website",
                "chunk_index": i
            })
            ids.append(f"{client_id}-url-{uuid.uuid4().hex[:8]}")
            
        vector_db_service.add_documents(documents, metadatas, ids)
        return {"status": "success", "chunks_processed": len(chunks)}

    def process_faq(self, question: str, answer: str, client_id: str):
        """Process a raw FAQ pair and store in vector DB."""
        content = f"Q: {question}\nA: {answer}"
        
        timestamp = datetime.utcnow().isoformat()
        metadata = {
            "client_id": client_id,
            "timestamp": timestamp,
            "type": "faq"
        }
        doc_id = f"{client_id}-faq-{uuid.uuid4().hex[:8]}"
        
        vector_db_service.add_documents([content], [metadata], [doc_id])
        return {"status": "success", "doc_id": doc_id}

ingestion_service = IngestionService()
