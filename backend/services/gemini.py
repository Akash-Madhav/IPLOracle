# services/gemini.py

import os
import logging, gc, psutil, traceback
from collections import defaultdict
from rapidfuzz import process

if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

logger = logging.getLogger(__name__)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def generate_answer(query: str, context: str) -> str:
    if not GEMINI_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not found; fallback to plain results")
        return f"Top similar records found:\n{context}"

    if not context.strip():
        return "⚠️ No relevant stats found in the dataset."

    prompt = f"""
You are a cricket data analyst. Use the statistics below to answer the user's question precisely.

Question:
{query}

Player Stats:
{context}

Instructions:
- Provide a direct, data-driven answer to the question.
- Use exact numbers from the stats provided.
- If comparing players or years, present the comparison clearly with specific values.
- If asked for "best" or "most", identify the player with the highest value in that category.
- If asked about a specific player or year, focus only on that data.
- Be concise and factual - don't add unnecessary commentary.
- If the answer isn't clearly in the data, state what data is available.
- Format your answer in a clear, readable way.

Answer:
"""

    response = None
    gemini_model = None
    try:
        logger.info(f"🧠 Gemini prompt (first 500 chars):\n{prompt[:500]}...")

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        gemini_model = genai.GenerativeModel("gemini-2.5-flash")

        response = gemini_model.generate_content(prompt)
        logger.info(f"📦 Gemini raw response received")

        gc.collect()

        answer_text = response.text.strip()
        logger.info(f"✅ Gemini answer generated ({len(answer_text)} chars)")

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
    Fallback to heuristic-based classification if Gemini is unavailable.
    """
    if not GEMINI_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not found; using heuristic field classification")
        return _classify_fields_heuristic(query)

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
- Return only the most relevant fields as a Python list of strings.
- Always include "Player_Name" and "Year" first.
- If the query is about batting stats, include batting-related fields.
- If the query is about bowling stats, include bowling-related fields.
- If the query is about fielding stats, include catches/stumpings.
- Limit to the 5-7 most relevant fields.
- Do not invent fields - only use fields from the list above.
- Return ONLY the Python list, nothing else.

Example outputs:
["Player_Name", "Year", "Runs_Scored", "Batting_Strike_Rate"]
["Player_Name", "Year", "Wickets_Taken", "Economy_Rate", "Bowling_Average"]
"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)
        answer_text = response.text.strip()

        # Extract list from response (handle markdown code blocks)
        if "```" in answer_text:
            # Extract from code block
            import re
            match = re.search(r'```(?:python)?\s*(\[.*?\])\s*```', answer_text, re.DOTALL)
            if match:
                answer_text = match.group(1)
        
        # Parse the list
        fields = eval(answer_text) if answer_text.startswith("[") else _classify_fields_heuristic(query)
        logger.info(f"✅ Classified fields via Gemini: {fields}")
        return fields

    except Exception as e:
        logger.error(f"❌ Gemini classification failed: {e}")
        logger.debug(traceback.format_exc())
        return _classify_fields_heuristic(query)

def _classify_fields_heuristic(query: str) -> list[str]:
    """
    Heuristic-based field classification as fallback.
    """
    query_lower = query.lower()
    fields = ["Player_Name", "Year"]
    
    # Batting keywords
    batting_keywords = ["run", "score", "batting", "average", "strike rate", "century", "half century", 
                       "hundred", "fifty", "four", "six", "boundary"]
    # Bowling keywords
    bowling_keywords = ["wicket", "bowl", "economy", "bowling average", "maiden", "haul"]
    # Fielding keywords
    fielding_keywords = ["catch", "stumping", "field"]
    
    has_batting = any(kw in query_lower for kw in batting_keywords)
    has_bowling = any(kw in query_lower for kw in bowling_keywords)
    has_fielding = any(kw in query_lower for kw in fielding_keywords)
    
    if has_batting:
        fields.extend(["Runs_Scored", "Batting_Average", "Batting_Strike_Rate", "Centuries", "Half_Centuries"])
    elif has_bowling:
        fields.extend(["Wickets_Taken", "Economy_Rate", "Bowling_Average", "Bowling_Strike_Rate", "Five_Wicket_Hauls"])
    elif has_fielding:
        fields.extend(["Catches_Taken", "Stumpings"])
    else:
        # Default to batting stats
        fields.extend(["Runs_Scored", "Batting_Average", "Batting_Strike_Rate"])
    
    logger.info(f"✅ Classified fields via heuristic: {fields}")
    return fields

def build_context_by_player(records, relevant_fields, max_per_player=None, target_players=None, threshold=80):
    from collections import defaultdict
    from rapidfuzz import process

    grouped = defaultdict(list)
    for r in records:
        name = r.get("Player_Name")
        if not name:
            continue
        if target_players:
            match = process.extractOne(name, target_players, score_cutoff=threshold)
            if not match:
                continue
            canonical = match[0]
        else:
            canonical = name
        grouped[canonical].append(r)

    context_blocks = []
    for player, recs in grouped.items():
        # Sort records by the primary relevant field for this player
        sort_field = next((f for f in relevant_fields if f not in ["Player_Name", "Year"]), None)
        if sort_field:
            try:
                recs = sorted(recs, key=lambda r: float(r.get(sort_field, "0") or 0), reverse=True)
            except Exception:
                pass

        # Limit records per player if specified
        selected_recs = recs if max_per_player is None else recs[:max_per_player]
        
        for r in selected_recs:
            # Build a clean, readable context line with only relevant fields
            parts = []
            for field in relevant_fields:
                value = r.get(field)
                if value is not None and value != "":
                    # Format field name to be more readable
                    field_name = field.replace("_", " ")
                    parts.append(f"{field_name}: {value}")
            
            if parts:
                context_blocks.append(" | ".join(parts))

    return "\n".join(context_blocks)