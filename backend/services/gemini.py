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
    gemini_model = None
    try:
        logger.info(f"🧠 Gemini prompt:\n{prompt[:500]}...")

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
        try:
            del response, prompt, context, gemini_model
        except Exception:
            pass
        gc.collect()

def classify_fields(query: str) -> list[str]:
    """
    Use Gemini to decide which fields are most relevant for the given query.
    """
    if not GEMINI_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not found; fallback to default fields")
        return ["Runs_Scored", "Year", "Player_Name"]

    prompt = f"""
You are a cricket query classifier. Given a question, return the most relevant stat fields
from the dataset schema below.

Available fields:
Player_Name, Year, Runs_Scored, Batting_Average, Batting_Strike_Rate, Centuries,
Half_Centuries, Highest_Score, Fours, Sixes, Balls_Faced, Matches_Batted,
Wickets_Taken, Economy_Rate, Bowling_Average, Bowling_Strike_Rate, Best_Bowling_Match,
Five_Wicket_Hauls, Four_Wicket_Hauls, Catches_Taken, Stumpings

Question:
{query}

Instructions:
- Return only the most relevant fields as a Python list.
- Always include "Player_Name" and "Year".
- If the query is about batting, include batting stats.
- If the query is about bowling, include bowling stats.
- If the query is about fielding, include fielding stats.
- Do not invent fields.
- Example output: ["Runs_Scored", "Year", "Player_Name"]
"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)
        answer_text = response.text.strip()

        fields = eval(answer_text) if answer_text.startswith("[") else ["Player_Name", "Year"]
        logger.info(f"✅ Classified fields: {fields}")
        return fields

    except Exception as e:
        logger.error(f"❌ Gemini classification failed: {e}")
        logger.debug(traceback.format_exc())
        return ["Player_Name", "Year", "Runs_Scored"]