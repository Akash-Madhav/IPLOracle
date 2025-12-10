from fastapi import APIRouter
from models.query import QueryRequest, AskResponse
import logging, time, psutil, asyncio
from pinecone import Pinecone
from config import Config

from services.gemini import generate_answer, classify_fields, build_context_by_player, extract_years_from_query
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

# 🧠 Helper: fuzzy player extraction
def extract_players_from_query(query: str, player_names: list, threshold: int = 80) -> list:
    found = set()
    q_tokens = query.lower().split()
    for token in q_tokens:
        match = process.extractOne(token, player_names, score_cutoff=threshold)
        if match:
            found.add(match[0])  # canonical name
    return list(found)

@ask_router.post("/ask", response_model=AskResponse)
async def ask_query(payload: QueryRequest) -> AskResponse:
    start_time = time.time()
    query = payload.query.strip() if payload.query else ""

    if not payload.vector:
        return AskResponse(query=query, answer="⚠️ Provide a vector embedding.", results=[])

    logger.info(f"🟢 Query received: {query}")
    heartbeat_task = asyncio.create_task(heartbeat())

    try:
        # 🔎 Step 1: Extract years from query
        years = extract_years_from_query(query)
        logger.info(f"📅 Extracted years from query: {years}")
        
        # 🔎 Step 2: Query Pinecone with semantic search
        # Use reasonable top_k for semantic search (not all records)
        t1 = time.time()
        
        # Build metadata filter if years are specified
        filter_dict = None
        if years:
            if len(years) == 1:
                filter_dict = {"Year": {"$eq": str(years[0])}}
            else:
                filter_dict = {"Year": {"$in": [str(y) for y in years]}}
            logger.info(f"🔍 Using Pinecone filter: {filter_dict}")
        
        # Query with appropriate top_k
        # If filtering by year, use smaller top_k; otherwise use larger for broader search
        top_k = 50 if filter_dict else 100
        
        response = index.query(
            vector=payload.vector, 
            top_k=top_k, 
            include_metadata=True,
            filter=filter_dict
        )
        print(f"⏱ Pinecone search: {time.time() - t1:.2f}s")

        # 🧹 Collect metadata
        raw_results = [match.metadata for match in response["matches"]]
        results = [r for r in raw_results if r]
        logger.info(f"📊 Retrieved {len(results)} records from Pinecone")

        # 🧠 Step 3: Classify query to get relevant fields
        relevant_fields = classify_fields(query)
        logger.info(f"🎯 Relevant fields: {relevant_fields}")

        # 🧠 Step 4: Sort results by the primary relevant field if numeric
        sort_field = next((f for f in relevant_fields if f not in ["Player_Name", "Year"]), None)
        if sort_field and results:
            try:
                # Filter and sort by the primary stat field
                valid_results = [r for r in results if r.get(sort_field) and float(r.get(sort_field, "0")) > 0]
                if valid_results:
                    results = sorted(valid_results, key=lambda r: float(r.get(sort_field, "0")), reverse=True)
                    logger.info(f"✅ Sorted {len(results)} results by {sort_field}")
            except Exception as e:
                logger.warning(f"⚠️ Sorting by {sort_field} failed: {e}")

        # 🧠 Step 5: Fuzzy player extraction from query
        all_players = get_all_players(results)
        players = extract_players_from_query(query, all_players, threshold=75)
        logger.info(f"🧠 Fuzzy-matched players from query: {players}")

        # 🧠 Step 6: Build focused context
        # If specific players are mentioned, limit to top records per player
        # If no specific players, use top overall records
        max_records_per_player = 5 if players else None
        
        context = build_context_by_player(
            records=results,
            relevant_fields=relevant_fields,
            max_per_player=max_records_per_player,
            target_players=players if players else None,
            threshold=75
        )
        
        logger.info(f"📝 Context length: {len(context)} chars, {len(context.split(chr(10)))} lines")

        # ✨ Step 7: Generate Gemini answer
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

        return AskResponse(query=query, answer=answer, results=results[:20])  # Return top 20 results

    finally:
        heartbeat_task.cancel()
        try:
            await heartbeat_task
        except asyncio.CancelledError:
            pass