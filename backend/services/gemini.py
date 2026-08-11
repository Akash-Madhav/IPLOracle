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

# Superlative keywords that indicate ranking/comparison queries
# These queries require comprehensive data retrieval for accurate results
SUPERLATIVE_KEYWORDS = [
    "most", "best", "highest", "top", "maximum", "greatest",
    "lowest", "worst", "minimum", "least", "fewest",
    "better", "worse", "higher", "lower", "more", "less",
    "leading", "first", "last", "who scored the", "who took",
    "who has", "who had", "top scorer", "top wicket"
]

def is_superlative_query(query: str) -> bool:
    """
    Detect if a query is asking for superlatives (most, best, highest, etc.).
    These queries require comprehensive data retrieval for accurate ranking.
    
    Uses word boundary matching to avoid false positives from substring matches.
    
    Returns True if the query contains superlative keywords.
    """
    query_lower = query.lower()
    
    # Use word boundary regex for more precise matching
    # This avoids false positives like "remote" matching "more"
    for keyword in SUPERLATIVE_KEYWORDS:
        # For multi-word keywords, check direct substring match
        if " " in keyword:
            if keyword in query_lower:
                return True
        else:
            # For single words, use word boundary matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, query_lower):
                return True
    
    return False

def analyze_query_intent(query: str) -> dict:
    """
    Use Gemini AI as the primary deciding factor (Pre-Fetch Query Intent Router) to analyze
    the user's question before fetching data from the database.
    
    Returns a dict with:
      - query_intent: "player_comparison" | "player_lookup" | "superlative_ranking" | "general_semantic"
      - target_players: list of canonical player names
      - target_years: list of integer years
      - primary_stat_focus: str (e.g. "Runs_Scored")
      - recommended_strategy: "direct_player_store" | "superlative_store" | "vector_search"
      - ai_decided: bool
    """
    from services.player_store import player_store

    # Local fallback routing
    fallback_players = player_store.extract_players_from_query(query) if player_store.is_loaded else []
    fallback_years = extract_years_from_query(query)
    fallback_superlative = is_superlative_query(query)

    if fallback_players:
        fallback_strategy = "direct_player_store"
        fallback_intent = "player_comparison" if len(fallback_players) > 1 else "player_lookup"
    elif fallback_superlative:
        fallback_strategy = "superlative_store"
        fallback_intent = "superlative_ranking"
    else:
        fallback_strategy = "vector_search"
        fallback_intent = "general_semantic"

    fallback_dict = {
        "query_intent": fallback_intent,
        "target_players": fallback_players,
        "target_years": fallback_years,
        "primary_stat_focus": "Runs_Scored",
        "recommended_strategy": fallback_strategy,
        "ai_decided": False
    }

    if not GEMINI_KEY:
        logger.info(f"🧠 Gemini Router (local fallback): {fallback_dict}")
        return fallback_dict

    prompt = f"""You are a Cricket Query Intent Analyzer and Router for the IPL Oracle Database.
Analyze the user's question and decide the exact retrieval strategy before querying the database.

Question:
{query}

Output ONLY a raw JSON object (with NO markdown backticks or extra text) following this exact schema:
{{
  "query_intent": "player_comparison" | "player_lookup" | "superlative_ranking" | "general_semantic",
  "target_players": ["Player Name 1", "Player Name 2"],
  "target_years": [2023],
  "primary_stat_focus": "Runs_Scored" | "Wickets_Taken" | "Batting_Strike_Rate" | "Economy_Rate" | "Batting_Average",
  "recommended_strategy": "direct_player_store" | "superlative_store" | "vector_search"
}}

Rules:
- "target_players": List full names of any specific players mentioned (e.g. "Virat Kohli", "Rohit Sharma", "Jasprit Bumrah"). If no specific player, return [].
- "target_years": List any 4-digit IPL years mentioned (2008-2024). If no year, return [].
- "recommended_strategy":
    - Use "direct_player_store" if 1 or more specific players are mentioned.
    - Use "superlative_store" if asking for top/most/best performers (e.g. most runs, highest strike rate).
    - Use "vector_search" for general semantic questions without specific players or superlatives.

JSON Output:"""

    try:
        import google.generativeai as genai
        import json, time

        genai.configure(api_key=GEMINI_KEY)
        models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]

        for model_name in models_to_try:
            try:
                gemini_model = genai.GenerativeModel(model_name)
                response = gemini_model.generate_content(prompt)
                if response and hasattr(response, "text") and response.text:
                    txt = response.text.strip()
                    if "```json" in txt:
                        txt = txt.split("```json")[1].split("```")[0].strip()
                    elif "```" in txt:
                        txt = txt.split("```")[1].split("```")[0].strip()

                    parsed = json.loads(txt)
                    if isinstance(parsed, dict) and "recommended_strategy" in parsed:
                        # Normalize target players against PlayerStore if loaded
                        if player_store.is_loaded and parsed.get("target_players"):
                            norm_players = []
                            for p in parsed["target_players"]:
                                canon = player_store.get_canonical_name(p)
                                if canon:
                                    norm_players.append(canon)
                                else:
                                    norm_players.append(p)
                            parsed["target_players"] = list(dict.fromkeys(norm_players))

                        parsed["ai_decided"] = True
                        logger.info(f"🧠 Gemini AI Router Decision ({model_name}): strategy={parsed.get('recommended_strategy')}, players={parsed.get('target_players')}, years={parsed.get('target_years')}")
                        return parsed
            except Exception as e:
                err_str = str(e).lower()
                if "429" in err_str or "rate limit" in err_str:
                    time.sleep(1.0)
                    continue
                else:
                    logger.warning(f"⚠️ Gemini Router model {model_name} failed: {e}")
                    break

    except Exception as e:
        logger.error(f"❌ Gemini AI Router analysis failed: {e}")

    logger.info(f"🧠 Gemini Router falling back to RapidFuzz/Regex router: {fallback_dict}")
    return fallback_dict


def extract_years_from_query(query: str) -> list:
    """
    Extract all year mentions from the query (2008-2024 IPL years)
    Returns a list of years found in the query
    """
    years = []
    year_pattern = r'\b(20(?:0[8-9]|1[0-9]|2[0-4]))\b'
    matches = re.findall(year_pattern, query)
    years.extend([int(year) for year in matches])
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

    prompt = f"""You are a Lead IPL Cricket Analyst & Senior Commentator. Your goal is to deliver an insightful, expert POINT OF VIEW (POV) and narrative evaluation answering the user's question based strictly on the provided IPL statistics.

Question:
{query}

Available IPL Player Statistics:
{context}

CRITICAL DIRECTIVES:
1. Deliver a compelling, expert narrative Point of View (POV). Write in engaging, analytical prose.
2. DO NOT output raw markdown data tables or list out raw season-by-season record tables. Focus on narrative synthesis, tactical insights, and critical evaluation.
3. Seamlessly weave key statistical milestones (such as peak run tallies, strike rates, career averages, or centuries) into your narrative paragraphs rather than presenting raw list dumps.
4. Structure your response into clear, engaging sections:
   - 💡 **Analyst's Point of View (POV)**: The core thesis, narrative overview, and expert perspective on the query.
   - ⚡ **Playstyle, Impact & Dominance Synthesis**: Deep tactical evaluation comparing scoring tempo, consistency vs. peak power, adaptability across eras, and match-winning capabilities.
   - 🎯 **The Analyst's Verdict**: Your definitive expert conclusion and analytical takeaway answering the user's intent.
5. Ground all facts and numbers strictly in the provided data. Do NOT hallucinate figures.

Analyst POV & Evaluation:"""

    import google.generativeai as genai
    import time

    genai.configure(api_key=GEMINI_KEY)
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]
    answer_text = None

    logger.info(f"🧠 Gemini prompt context length: {len(context)} chars")

    for model_name in models_to_try:
        for attempt in range(2):
            try:
                gemini_model = genai.GenerativeModel(model_name)
                response = gemini_model.generate_content(prompt)
                if response and hasattr(response, "text") and response.text:
                    answer_text = response.text.strip()
                    logger.info(f"✅ Gemini response generated via {model_name} (length: {len(answer_text)} chars)")
                    break
            except Exception as e:
                err_str = str(e).lower()
                if "429" in err_str or "quota" in err_str or "rate limit" in err_str:
                    logger.warning(f"⚠️ Rate limit 429 hit on model {model_name} (attempt {attempt+1}), retrying in 1.5s...")
                    time.sleep(1.5)
                else:
                    logger.warning(f"⚠️ Model {model_name} failed: {e}")
                    break
        if answer_text:
            break

    if answer_text:
        gc.collect()
        mem = psutil.Process().memory_info().rss / 1024**2
        logger.info(f"🧠 Memory after Gemini generation: {mem:.2f} MiB")
        return answer_text

    # Smart local analyst POV fallback if AI model rate-limited
    logger.warning("⚠️ All Gemini AI model attempts failed or rate-limited; generating local rule-based Analyst POV narrative.")
    return generate_local_analyst_pov(query, context)


def generate_local_analyst_pov(query: str, context: str) -> str:
    """
    Generate an expert Analyst Point of View (POV) narrative fallback directly in Python 
    when Gemini API is rate-limited or offline.
    Never outputs raw pipe lists or data dumps.
    """
    if not context or not context.strip():
        return "⚠️ No dataset statistics available for analysis."

    from collections import defaultdict
    player_data = defaultdict(list)

    for line in context.splitlines():
        line = line.strip()
        if not line or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        header = parts[0]  # e.g. "Virat Kohli (2016)"
        
        player_name = header
        year = ""
        if "(" in header and ")" in header:
            player_name = header[:header.index("(")].strip()
            year = header[header.index("(")+1:header.index(")")].strip()

        stats = {}
        for part in parts[1:]:
            if ":" in part:
                k, v = part.split(":", 1)
                stats[k.strip()] = v.strip()
        
        if year:
            stats["Year"] = year
        player_data[player_name].append(stats)

    players = list(player_data.keys())

    pov_lines = []
    pov_lines.append("💡 **Analyst's Point of View (POV)**\n")

    if len(players) >= 2:
        p1, p2 = players[0], players[1]
        recs1, recs2 = player_data[p1], player_data[p2]
        
        def safe_num(val):
            try:
                return float(str(val).replace("*", "").replace(",", "").strip())
            except (ValueError, TypeError):
                return 0.0

        def get_totals(recs):
            total_runs = sum(safe_num(r.get("Runs_Scored")) for r in recs)
            total_100s = sum(int(safe_num(r.get("Centuries"))) for r in recs)
            total_50s = sum(int(safe_num(r.get("Half_Centuries"))) for r in recs)
            total_wkts = sum(int(safe_num(r.get("Wickets_Taken"))) for r in recs)
            peak_season = max(recs, key=lambda r: safe_num(r.get("Runs_Scored")), default={})
            return total_runs, total_100s, total_50s, total_wkts, peak_season

        r1_runs, r1_100s, r1_50s, r1_wkts, r1_peak = get_totals(recs1)
        r2_runs, r2_100s, r2_50s, r2_wkts, r2_peak = get_totals(recs2)

        pov_lines.append(f"When evaluating **{p1}** and **{p2}**, we are analyzing two defining icons of IPL history spanning {len(recs1)} recorded seasons.")
        pov_lines.append(f"**{p1}** operates as an elite volume run-accumulator with massive single-season peaks, whereas **{p2}** offers consistent top-order adaptability paired with strategic versatility.\n")
        
        pov_lines.append("---\n")
        pov_lines.append("⚡ **Playstyle, Impact & Dominance Synthesis**\n")
        
        pov_lines.append(f"* **Peak Dominance & Volume Ceiling:**")
        if r1_peak:
            pov_lines.append(f"  * **{p1}’s peak season ({r1_peak.get('Year', '')})** stands out with **{r1_peak.get('Runs_Scored', 'N/A')} runs** (Avg: {r1_peak.get('Batting_Average', 'N/A')}, SR: {r1_peak.get('Batting_Strike_Rate', 'N/A')}). Across recorded seasons, {p1} has logged **{r1_100s} centuries** and **{r1_50s} half-centuries**.")
        if r2_peak:
            pov_lines.append(f"  * **{p2}’s peak season ({r2_peak.get('Year', '')})** produced **{r2_peak.get('Runs_Scored', 'N/A')} runs** (Avg: {r2_peak.get('Batting_Average', 'N/A')}, SR: {r2_peak.get('Batting_Strike_Rate', 'N/A')}). Across recorded seasons, {p2} has registered **{r2_100s} centuries** and **{r2_50s} half-centuries**.\n")
        
        if r1_wkts > 0 or r2_wkts > 0:
            pov_lines.append(f"* **All-Round & Versatility Contributions:**")
            if r2_wkts > 0:
                pov_lines.append(f"  * **{p2}** provided notable bowling utility, accumulating **{r2_wkts} career wickets**.")
            if r1_wkts > 0:
                pov_lines.append(f"  * **{p1}** chipped in with **{r1_wkts} wickets** in key seasons.\n")

        pov_lines.append("---\n")
        pov_lines.append("🎯 **The Analyst's Verdict**\n")
        if r1_runs >= r2_runs:
            pov_lines.append(f"1. **Volume & Consistency Verdict:** **{p1}** holds the edge for overall run volume and peak season scoring power.")
            pov_lines.append(f"2. **Impact Verdict:** **{p2}** offers exceptional top-order longevity and tactical versatility.")
        else:
            pov_lines.append(f"1. **Volume & Consistency Verdict:** **{p2}** holds the edge for overall run accumulation across seasons.")
            pov_lines.append(f"2. **Impact Verdict:** **{p1}** provides explosive peak scoring and game-changing individual campaigns.")

    elif len(players) == 1:
        p = players[0]
        recs = player_data[p]
        def safe_num(val):
            try:
                return float(str(val).replace("*", "").replace(",", "").strip())
            except (ValueError, TypeError):
                return 0.0

        peak_season = max(recs, key=lambda r: safe_num(r.get("Runs_Scored")), default={})
        
        pov_lines.append(f"Analyzing the IPL performance profile of **{p}** across {len(recs)} recorded seasons in the dataset.\n")
        pov_lines.append("---\n")
        pov_lines.append("⚡ **Playstyle & Dominance Synthesis**\n")
        if peak_season:
            pov_lines.append(f"* **Career Peak ({peak_season.get('Year', '')}):** **{p}** recorded a career-defining season with **{peak_season.get('Runs_Scored', 'N/A')} runs** at an average of **{peak_season.get('Batting_Average', 'N/A')}** and a strike rate of **{peak_season.get('Batting_Strike_Rate', 'N/A')}**.")
        
        tot_100s = sum(int(safe_num(r.get("Centuries"))) for r in recs)
        tot_50s = sum(int(safe_num(r.get("Half_Centuries"))) for r in recs)
        pov_lines.append(f"* **Milestone Consistency:** Registered **{tot_100s} centuries** and **{tot_50s} half-centuries** across recorded IPL campaigns.\n")
        
        pov_lines.append("---\n")
        pov_lines.append("🎯 **The Analyst's Verdict**\n")
        pov_lines.append(f"**{p}** demonstrates elite IPL longevity, combining high peak scoring output with sustained top-order impact.")

    else:
        top_rec = player_data[players[0]][0] if players and player_data[players[0]] else {}
        pov_lines.append(f"Statistical analysis of top IPL performers matching the query intent.\n")
        pov_lines.append("---\n")
        pov_lines.append("⚡ **Dominance Synthesis**\n")
        if top_rec:
            pov_lines.append(f"* **Top Performer:** **{players[0]}** leads the benchmark with **{top_rec.get('Runs_Scored', top_rec.get('Wickets_Taken', 'N/A'))}** in {top_rec.get('Year', '')}.\n")
        pov_lines.append("🎯 **The Analyst's Verdict**\n")
        pov_lines.append("The dataset highlights top-tier individual performances with high efficiency across IPL seasons.")

    return "\n".join(pov_lines)

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
    comparison_keywords = ["compare", "comparison", "vs", "versus", "between", "better", "performance", "career", "stats", "overall"]
    
    query_lower = query.lower()
    
    # Default fields
    base_fields = ["Player_Name", "Year"]
    relevant_fields = []
    
    # Check for comparison / general stats
    if any(keyword in query_lower for keyword in comparison_keywords):
        relevant_fields.extend(["Runs_Scored", "Batting_Average", "Batting_Strike_Rate", 
                               "Centuries", "Half_Centuries", "Wickets_Taken", "Economy_Rate"])

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
            year = r.get("Year", "")
            # Skip Player_Name and Year from individual key-value pairs to avoid redundancy
            parts = []
            for field in relevant_fields:
                if field in ("Player_Name", "Year"):
                    continue
                value = r.get(field)
                # Skip if value is None, empty, or 0 for numeric stats
                if value is not None and value != "" and value != "0" and value != 0 and value != "0.0":
                    parts.append(f"{field}: {value}")
            
            if parts:
                header = f"{player} ({year})" if year else player
                context_blocks.append(f"{header} | " + " | ".join(parts))

    return "\n".join(context_blocks)