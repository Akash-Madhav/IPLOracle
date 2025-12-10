# services/gemini.py

import os
import re
import logging, gc, psutil, traceback
from collections import defaultdict
from rapidfuzz import process

if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

logger = logging.getLogger(__name__)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def is_superlative_query(query: str) -> bool:
    """
    Detect if a query is asking for superlatives (most, best, highest, etc.).
    These queries require comprehensive data retrieval for accurate ranking.
    
    Returns True if the query contains superlative keywords.
    """
    query_lower = query.lower()
    
    # Superlative keywords that indicate ranking/comparison needs
    superlative_keywords = [
        "most", "best", "highest", "top", "maximum", "greatest",
        "lowest", "worst", "minimum", "least", "fewest",
        "better", "worse", "higher", "lower", "more", "less",
        "leading", "first", "last", "who scored the", "who took",
        "who has", "who had", "top scorer", "top wicket"
    ]
    
    return any(keyword in query_lower for keyword in superlative_keywords)

def extract_years_from_query(query: str) -> list:
    """
    Extract all year mentions from the query (2008-2024 IPL years)
    Returns a list of years found in the query
    """
    years = []
    # Match 4-digit years between 2008 and 2024 (IPL started in 2008)
    year_pattern = r'\b(20(?:0[8-9]|1[0-9]|2[0-4]))\b'
    matches = re.findall(year_pattern, query)
    years.extend([int(year) for year in matches])
    
    # Also check for phrases like "last year", "this year", "previous season"
    # For now, return the explicitly mentioned years
    return sorted(list(set(years)))

def identify_primary_stat(query: str, relevant_fields: list) -> str:
    """
    Identify the primary statistic field for sorting based on query intent.
    Returns the most relevant field for ranking results.
    """
    query_lower = query.lower()
    
    # Stat-specific keywords mapping
    stat_keywords = {
        "Runs_Scored": ["runs", "run", "runs scored", "most runs", "total runs"],
        "Batting_Strike_Rate": ["strike rate", "striking", "fastest", "quickest"],
        "Batting_Average": ["average", "batting average", "consistency"],
        "Wickets_Taken": ["wickets", "wicket", "most wickets", "bowling", "taken"],
        "Economy_Rate": ["economy", "economical", "cheap", "best economy"],
        "Bowling_Average": ["bowling average"],
        "Centuries": ["century", "centuries", "hundred"],
        "Half_Centuries": ["half century", "fifty", "fifties"],
        "Sixes": ["sixes", "six", "most sixes"],
        "Fours": ["fours", "four", "most fours"],
        "Catches_Taken": ["catches", "catch", "fielding"],
        "Highest_Score": ["highest score", "best score", "top score"],
    }
    
    # Find the first matching stat in query
    for field, keywords in stat_keywords.items():
        if field in relevant_fields:
            if any(keyword in query_lower for keyword in keywords):
                return field
    
    # Default: return first non-name/year field
    for field in relevant_fields:
        if field not in ["Player_Name", "Year"]:
            return field
    
    return "Runs_Scored"  # Ultimate fallback

def generate_answer(query: str, context: str) -> str:
    if not GEMINI_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not found; fallback to plain results")
        return f"Top similar records found:\n{context}"

    if not context.strip():
        return "⚠️ No relevant stats found in the dataset for this query."

    prompt = f"""
You are a precise cricket statistics analyst. Answer the question using ONLY the data provided below.

Question:
{query}

Available Player Statistics:
{context}

Critical Instructions:
1. Extract and use ONLY the relevant statistics from the data above
2. Be direct and specific - state the answer with exact numbers immediately
3. If comparing players, list them with their stats clearly
4. If the question asks for "most" or "best", identify the top performer(s) with exact values
5. NEVER invent or estimate data - use only what's provided
6. If data is insufficient, clearly state what's missing
7. Keep response concise (2-4 sentences maximum)
8. Always mention the player name(s) and year when relevant

Answer format:
[Direct answer with player name(s) and exact stat(s)]"""

    response = None
    gemini_model = None
    try:
        logger.info(f"🧠 Gemini prompt context length: {len(context)} chars")

        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        gemini_model = genai.GenerativeModel("gemini-2.5-flash")

        response = gemini_model.generate_content(prompt)
        logger.info(f"📦 Gemini raw response received")

        gc.collect()

        answer_text = response.text.strip()
        logger.info(f"✅ Gemini answer length: {len(answer_text)} chars")

        mem = psutil.Process().memory_info().rss / 1024**2
        logger.info(f"🧠 Memory after Gemini generation: {mem:.2f} MiB")

        return answer_text

    except Exception as e:
        logger.error(f"❌ Gemini generation failed: {e}")
        logger.debug(traceback.format_exc())
        # Fallback to structured context display
        return f"Based on the available data:\n{context[:1000]}"

    finally:
        # ✅ Safe cleanup
        try:
            del response, prompt, gemini_model
        except Exception:
            pass
        gc.collect()

def classify_fields(query: str) -> list[str]:
    """
    Use Gemini to decide which fields are most relevant for the given query.
    Falls back to keyword-based classification if Gemini is unavailable.
    """
    # Keywords for different stat categories
    batting_keywords = ["run", "score", "batting", "strike rate", "century", "half century", 
                        "four", "six", "average", "highest", "total runs", "most runs"]
    bowling_keywords = ["wicket", "bowling", "economy", "bowl", "five wicket", "four wicket",
                        "best bowling", "taken", "maiden"]
    fielding_keywords = ["catch", "field", "stumping", "caught"]
    
    query_lower = query.lower()
    
    # Default fields
    base_fields = ["Player_Name", "Year"]
    relevant_fields = []
    
    # Check for batting stats
    if any(keyword in query_lower for keyword in batting_keywords):
        relevant_fields.extend(["Runs_Scored", "Batting_Average", "Batting_Strike_Rate", 
                               "Centuries", "Half_Centuries", "Highest_Score", "Fours", "Sixes"])
    
    # Check for bowling stats
    if any(keyword in query_lower for keyword in bowling_keywords):
        relevant_fields.extend(["Wickets_Taken", "Bowling_Average", "Economy_Rate", 
                               "Bowling_Strike_Rate", "Best_Bowling_Match", 
                               "Five_Wicket_Hauls", "Four_Wicket_Hauls"])
    
    # Check for fielding stats
    if any(keyword in query_lower for keyword in fielding_keywords):
        relevant_fields.extend(["Catches_Taken", "Stumpings"])
    
    # If no specific category, include common stats
    if not relevant_fields:
        relevant_fields = ["Runs_Scored", "Wickets_Taken", "Batting_Strike_Rate"]
    
    # Remove duplicates and add base fields
    final_fields = base_fields + list(dict.fromkeys(relevant_fields))
    
    # If Gemini is available, use it for refinement
    if not GEMINI_KEY:
        logger.info(f"✅ Keyword-based classification: {final_fields}")
        return final_fields
    
    prompt = f"""
You are a cricket query classifier. Given a question, return ONLY the most relevant stat fields
from the dataset schema below. Return a Python list with NO extra text.

Available fields:
Player_Name, Year, Runs_Scored, Batting_Average, Batting_Strike_Rate, Centuries,
Half_Centuries, Highest_Score, Fours, Sixes, Balls_Faced, Matches_Batted,
Wickets_Taken, Economy_Rate, Bowling_Average, Bowling_Strike_Rate, Best_Bowling_Match,
Five_Wicket_Hauls, Four_Wicket_Hauls, Catches_Taken, Stumpings

Question:
{query}

Rules:
- ALWAYS include "Player_Name" and "Year"
- Include 3-7 most relevant fields for this specific question
- For batting questions: include batting stats
- For bowling questions: include bowling stats  
- For fielding questions: include fielding stats
- Return ONLY a Python list like: ["Field1", "Field2", "Field3"]

Output (list only):"""
    
    try:
        import google.generativeai as genai
        import ast
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)
        answer_text = response.text.strip()
        
        # Extract list from response safely
        if "[" in answer_text and "]" in answer_text:
            start = answer_text.index("[")
            end = answer_text.rindex("]") + 1
            list_text = answer_text[start:end]
            try:
                # Use ast.literal_eval for safe evaluation
                fields = ast.literal_eval(list_text)
                if isinstance(fields, list):
                    logger.info(f"✅ Gemini classified fields: {fields}")
                    return fields
                else:
                    logger.warning(f"⚠️ Gemini response not a list, using keyword fallback")
                    return final_fields
            except (ValueError, SyntaxError) as e:
                logger.warning(f"⚠️ Failed to parse Gemini response: {e}, using keyword fallback")
                return final_fields
        else:
            logger.warning(f"⚠️ Gemini response not a list, using keyword fallback: {answer_text}")
            return final_fields

    except Exception as e:
        logger.error(f"❌ Gemini classification failed: {e}")
        logger.info(f"✅ Using keyword fallback: {final_fields}")
        return final_fields

def build_context_by_player(records, relevant_fields, max_per_player=None, target_players=None, threshold=80):
    """
    Build context by grouping records by player and including relevant fields.
    
    Args:
        records: List of player records
        relevant_fields: List of field names to include
        max_per_player: Maximum records per player (None = all)
        target_players: List of target player names (None = all)
        threshold: Fuzzy matching threshold (0-100)
    
    Returns:
        Formatted context string with player stats
    """
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
    
    # Determine the primary sort field (first non-name/year field)
    sort_field = next((f for f in relevant_fields if f not in ["Player_Name", "Year"]), None)
    
    for player, recs in grouped.items():
        # Sort records by the primary relevant field (highest first)
        if sort_field:
            try:
                # Filter out records where the sort field has no value or is 0
                valid_recs = [r for r in recs if r.get(sort_field) and float(r.get(sort_field, "0")) > 0]
                if valid_recs:
                    recs = sorted(valid_recs, key=lambda r: float(r.get(sort_field, "0")), reverse=True)
                else:
                    recs = sorted(recs, key=lambda r: float(r.get(sort_field, "0")), reverse=True)
            except (ValueError, TypeError):
                # If sorting fails, sort by Year descending
                recs = sorted(recs, key=lambda r: int(r.get("Year", "0")), reverse=True)
        else:
            # Default: sort by Year descending
            recs = sorted(recs, key=lambda r: int(r.get("Year", "0")), reverse=True)

        # Limit records per player if specified
        selected_recs = recs if max_per_player is None else recs[:max_per_player]
        
        # Build context for each record
        for r in selected_recs:
            # Only include fields that have meaningful values
            parts = []
            for field in relevant_fields:
                value = r.get(field)
                # Skip if value is None, empty, or 0 for numeric stats
                if value is not None and value != "" and value != "0" and value != 0:
                    parts.append(f"{field}: {value}")
            
            if parts:
                context_blocks.append(f"{player} | " + " | ".join(parts))

    return "\n".join(context_blocks)