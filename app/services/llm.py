from groq import Groq
from app.core.config import settings
from app.services.vector_db import vector_db_service

class LLMService:
    def __init__(self):
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        else:
            self.client = None

    def generate_chat_response(self, query: str, client_id: str) -> dict:
        """
        Generate a response based on ChromaDB context using Groq.
        Returns: {"answer": str, "needs_fallback": bool}
        """
        if not self.client:
            return {"answer": "Error: Groq API Key not configured.", "needs_fallback": True}

        # 1. Get Context from Vector DB
        try:
            context_docs = vector_db_service.search_similar(query, client_id=client_id, n_results=3)
            context_text = "\n\n".join(context_docs)
        except Exception:
            context_text = ""

        print(f"--- DEBUG CONTEXT --- \n{context_text}\n---------------------")

        if not context_text.strip():
            return {"answer": "", "needs_fallback": True}

        # 2. Construct System Prompt
        prompt = f"""You are a helpful customer support AI. Use the following Context to answer the user's question. Context: {context_text}. If the exact answer is in the Context, answer it naturally and concisely. If the Context is empty or does not contain the answer, you MUST reply with exactly and only: FALLBACK_TRIGGERED.

User Question: {query}
"""

        # 3. Call Groq API
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    }
                ]
            )
            answer = response.choices[0].message.content.strip()
            
            # 4. Check for fallback
            if "FALLBACK_TRIGGERED" in answer:
                return {"answer": "", "needs_fallback": True}
                
            return {"answer": answer, "needs_fallback": False}
        except Exception as e:
            return {"answer": f"Error generating response: {str(e)}", "needs_fallback": True}

llm_service = LLMService()
