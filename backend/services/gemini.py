# services/gemini.py

import os
import google.generativeai as genai
import logging,gc

if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

logger = logging.getLogger(__name__)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

gemini_model = None
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.5-flash")
    gc.collect()  # 🔄 Added here
    logger.info("✅ Gemini model loaded")
else:
    logger.warning("⚠️ GEMINI_API_KEY not found; fallback to plain FAISS results")

def generate_answer(query: str, context: str) -> str:
    if not gemini_model:
        return f"Top similar records found:\n{context}"

    if not context.strip():
        return "⚠️ No relevant stats found in the dataset."

    prompt = f"""
You are a cricket data analyst. Use the statistics below to answer the user's question.

Question:
{query}

Player Stats:
{context}

Instructions:
- Extract only the relevant stats from the context.
- If multiple players or years are involved, compare or summarize clearly.
- Do not invent data. If the answer is not in the stats, say so.
- Avoid filler or repetition.
- Use numbers and player names directly in your answer.
- Be concise and stat-rich.

Answer in the least amount of lines or words. Provide your result or conclusion alone.
"""

    try:
        logger.info(f"🧠 Gemini prompt:\n{prompt}")
        response = gemini_model.generate_content(prompt)
        gc.collect()  # 🔄 Added here
        return response.text.strip()
    except Exception as e:
        logger.error(f"❌ Gemini generation failed: {e}")
        return f"Top similar records found:\n{context}"