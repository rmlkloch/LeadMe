import json
import logging
import os
import re
from groq import Groq
from app.core.config import settings

logger = logging.getLogger(__name__)


def get_groq_client() -> Groq | None:
    """Initialize the Groq client securely using the API key from settings or environment."""
    api_key = settings.GROQ_API_KEY or os.environ.get("GROQ_API_KEY")
    if api_key:
        return Groq(api_key=api_key)
    return None


SYSTEM_PROMPT = """You are an expert sales development representative (SDR). Your task is to analyze the provided chat transcript and evaluate the lead's buying intent.

Evaluation Rules:
- 🔥 Hot (80-100): High intent, asking about pricing, ready to buy, or urgent.
- ☀️ Warm (40-79): Exploring, asking general product questions, curious but not urgent.
- ❄️ Cold (1-39): Vague questions, outside of scope, or low buying intent.

CRITICAL REQUIREMENT:
You must output your response in JSON format, without any markdown formatting (no ```json code blocks) or conversational text.

JSON Schema:
{
  "conversion_score": <integer between 1 and 100>,
  "lead_temperature": "<Hot | Warm | Cold>"
}
"""


def generate_lead_score(chat_transcript: str) -> dict:
    """
    Analyzes a chat transcript using Groq (llama-3.1-8b-instant) and returns lead score metrics.
    Returns: {"conversion_score": int | None, "lead_temperature": str}
    """
    fallback = {"conversion_score": None, "lead_temperature": "Unknown"}

    if not chat_transcript or not chat_transcript.strip():
        logger.warning("Empty chat transcript provided to generate_lead_score.")
        return fallback

    client = get_groq_client()
    if not client:
        logger.error("Groq API Key is not configured.")
        return fallback

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Chat Transcript:\n{chat_transcript}"}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        raw_text = response.choices[0].message.content
        print(f"RAW GROQ SCORE OUTPUT: {raw_text}")
        data = json.loads(raw_text)

        if "conversion_score" in data and "lead_temperature" in data:
            score = int(data["conversion_score"])
            temp = str(data["lead_temperature"]).strip().capitalize()
            if temp not in ["Hot", "Warm", "Cold"]:
                if score >= 80:
                    temp = "Hot"
                elif score >= 40:
                    temp = "Warm"
                else:
                    temp = "Cold"
            return {"conversion_score": score, "lead_temperature": temp}
        else:
            logger.error(f"LLM output missing required keys. Raw output: {raw_text}")
            return fallback

    except Exception as e:
        import traceback
        print(f"❌ SCORING ERROR: {str(e)}")
        traceback.print_exc()
        logger.error(f"Error generating lead score: {e}", exc_info=True)
        return fallback
