# services/gemini.py

import os
import logging, gc, psutil, traceback

if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

logger = logging.getLogger(__name__)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def generate_answer(query: str, context: str) -> str:
    if not GEMINI_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not found; fallback to plain FAISS results")
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

    response = None
    try:
        logger.info(f"🧠 Gemini prompt:\n{prompt[:500]}...")  # Truncated for safety

        # 🔄 Lazy-load Gemini model here
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        gemini_model = genai.GenerativeModel("gemini-2.5-flash")

        response = gemini_model.generate_content(prompt)
        logger.info(f"📦 Gemini raw response object: {response}")

        gc.collect()

        answer_text = response.text.strip()
        logger.info(f"✅ Gemini answer:\n{answer_text}")

        mem = psutil.Process().memory_info().rss / 1024**2
        logger.info(f"🧠 Memory after Gemini generation: {mem:.2f} MiB")

        return answer_text

    except Exception as e:
        logger.error(f"❌ Gemini generation failed: {e}")
        logger.debug(traceback.format_exc())
        return f"Top similar records found:\n{context}"

    finally:
        # ✅ Safe cleanup
        for var in ["response", "prompt", "context"]:
            if var in locals():
                del locals()[var]
        gc.collect()