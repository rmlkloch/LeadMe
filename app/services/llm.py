# LLM service stub for future OpenAI/Gemini RAG pipeline integration
class LLMService:
    def __init__(self) -> None:
        pass

    async def generate_response(self, prompt: str) -> str:
        raise NotImplementedError("LLM response generation will be implemented in a future phase.")
