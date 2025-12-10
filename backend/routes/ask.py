from fastapi import APIRouter
from models.query import QueryRequest, AskResponse
import logging, time, psutil, asyncio
from pinecone import Pinecone
from config import Config

from services.gemini import generate_answer, classify_fields, build_context_by_player
from rapidfuzz import process  # ⬅️ fuzzy matching

logger = logging.getLogger(__name__)
ask_router = APIRouter()

# 🔗 Connect to Pinecone
pc = Pinecone(api_key=Config.PINECONE_API_KEY)
index = pc.Index(Config.INDEX_NAME)

@ask_router.get("/ask")
async def ask_info():
    return {"message": "POST { 'query': '...', 'vector': [...] }"}

async def heartbeat(interval=30):
    try:
        while True:
            print("🔄 Heartbeat: still processing...")
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        print("🛑 Heartbeat stopped")

# 🧠 Helper: build player list dynamically from Pinecone results
def get_all_players(results) -> list:
    return list({r.get("Player_Name") for r in results if r.get("Player_Name")})

# 🧠 Helper: fuzzy player extraction with better multi-word name matching
def extract_players_from_query(query: str, player_names: list, threshold: int = 80) -> list:
    found = set()
    query_lower = query.lower()
    
    # First, try to match full player names directly
    for player in player_names:
        if player.lower() in query_lower:
            found.add(player)
    
    # If no full matches, try token-based fuzzy matching
    if not found:
        q_tokens = query_lower.split()
        for token in q_tokens:
            if len(token) > 2:  # Skip very short tokens
                match = process.extractOne(token, player_names, score_cutoff=threshold)
                if match:
                    found.add(match[0])
    
    return list(found)

# 🧠 Helper: extract years from query
def extract_years_from_query(query: str) -> list:
    import re
    # Match 4-digit years (2008-2024 range for IPL)
    years = re.findall(r'\b(20[0-2][0-9])\b', query)
    return [year for year in years if 2008 <= int(year) <= 2024]

@ask_router.post("/ask", response_model=AskResponse)
async def ask_query(payload: QueryRequest) -> AskResponse:
    start_time = time.time()
    query = payload.query.strip() if payload.query else ""

    if not payload.vector:
        return AskResponse(query=query, answer="⚠️ Provide a vector embedding.", results=[])

    logger.info(f"🟢 Query received: {query}")
    heartbeat_task = asyncio.create_task(heartbeat())

    try:
        # 🔎 Query Pinecone with optimized top_k for better performance
        t1 = time.time()
        response = index.query(vector=payload.vector, top_k=100, include_metadata=True)
        print(f"⏱ Pinecone search: {time.time() - t1:.2f}s")

        # 🧹 Collect metadata with similarity scores
        raw_results = [(match.metadata, match.score) for match in response["matches"]]
        results_with_scores = [(r, score) for r, score in raw_results if r]
        results = [r for r, score in results_with_scores]
        print(f"✅ Retrieved {len(results)} results from Pinecone")

        # 🧠 Step 1: Classify query to get relevant fields
        relevant_fields = classify_fields(query)
        logger.info(f"🎯 Relevant fields: {relevant_fields}")

        # 🧠 Step 2: Extract years from query dynamically
        years = extract_years_from_query(query)
        if years:
            logger.info(f"📅 Filtering by years: {years}")
            results = [r for r in results if str(r.get("Year")) in years]
            print(f"✅ After year filter: {len(results)} results")

        # 🧠 Step 3: Extract and filter by players mentioned in query
        all_players = get_all_players(results)
        players = extract_players_from_query(query, all_players)
        logger.info(f"🧠 Fuzzy-matched players: {players}")
        
        # If specific players are mentioned, filter to only those players
        if players:
            results = [r for r in results if r.get("Player_Name") in players]
            print(f"✅ After player filter: {len(results)} results")

        # 🧠 Step 4: Sort results by the primary relevant field if numeric
        sort_field = next((f for f in relevant_fields if f not in ["Player_Name", "Year"]), None)
        if sort_field:
            try:
                results = sorted(results, key=lambda r: float(r.get(sort_field, "0") or 0), reverse=True)
                print(f"✅ Sorted by {sort_field}")
            except Exception as e:
                logger.warning(f"Could not sort by {sort_field}: {e}")

        # 🧠 Step 5: Limit results to top most relevant records for context
        # Keep top 20 records for context to avoid overwhelming Gemini
        top_results = results[:20]
        logger.info(f"📊 Using top {len(top_results)} records for context generation")

        # Build context with filtered records
        context = build_context_by_player(
            records=top_results,
            relevant_fields=relevant_fields,
            max_per_player=5,  # Limit to 5 records per player for concise context
            target_players=players if players else None,
            threshold=80
        )

        # ✨ Generate Gemini answer
        t3 = time.time()
        try:
            answer = generate_answer(query, context) if query else "Vector-only query"
        except Exception as e:
            answer = "⚠️ Answer generation failed. Please try again."
            logger.error(f"Gemini error: {e}")
        print(f"⏱ Gemini: {time.time() - t3:.2f}s")

        mem_used = psutil.Process().memory_info().rss / 1024**2
        print(f"🧠 Memory after query: {mem_used:.2f} MiB")
        print(f"⏱ Total query time: {time.time() - start_time:.2f}s")

        # Return top_results (limited) instead of all results for efficiency
        return AskResponse(query=query, answer=answer, results=top_results)

    finally:
        heartbeat_task.cancel()
        try:
            await heartbeat_task
        except asyncio.CancelledError:
            pass