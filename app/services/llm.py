import google.generativeai as genai
from app.core.config import settings
from app.services.vector_db import vector_db_service

class LLMService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def generate_chat_response(self, query: str, client_id: str) -> dict:
        """
        Generate a response based on ChromaDB context using Gemini.
        Returns: {"answer": str, "needs_fallback": bool}
        """
        if not self.model:
            return {"answer": "Error: Gemini API Key not configured.", "needs_fallback": True}

        # 1. Get Context from Vector DB
        try:
            results = vector_db_service.search_similar(query, client_id=client_id, n_results=3)
            context_docs = results.get('documents', [[]])[0] if results else []
            context_text = "\n\n".join(context_docs)
        except Exception:
            context_text = ""

        if not context_text.strip():
            return {"answer": "", "needs_fallback": True}

        # 2. Construct System Prompt
        prompt = f"""You are a helpful AI assistant for a business.
Your goal is to answer the user's question ONLY using the provided Context.
If the Context does not contain the answer or is completely irrelevant, you MUST output exactly: "FALLBACK_TRIGGERED". Do not output anything else if you cannot answer it.

Context:
{context_text}

User Question: {query}
"""

        # 3. Call Gemini
        try:
            response = self.model.generate_content(prompt)
            answer = response.text.strip()
            
            # 4. Check for fallback
            if "FALLBACK_TRIGGERED" in answer:
                return {"answer": "", "needs_fallback": True}
                
            return {"answer": answer, "needs_fallback": False}
        except Exception as e:
            return {"answer": f"Error generating response: {str(e)}", "needs_fallback": True}

llm_service = LLMService()
