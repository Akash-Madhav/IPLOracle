# services/gemini.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = None

def configure_gemini():
    global gemini_model
    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
        gemini_model = genai.GenerativeModel("gemini-2.5-flash")
        logger.info("✅ Gemini configured")
    else:
        logger.warning("⚠️ GEMINI_API_KEY not found; fallback to plain FAISS results")

def generate_answer(query: str, context: str) -> str:
    if not gemini_model:
        return f"Top similar records found:\n{context}"

    prompt = f"""
    You are a cricket data analyst. Use the statistics below to answer the user's question.
    Question:
    {query}

    Player Stats:
    {context}

    Answer in the least amount of lines or words. Provide your result or conclusion alone.
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"❌ Gemini generation failed: {e}")
        return f"Top similar records found:\n{context}"