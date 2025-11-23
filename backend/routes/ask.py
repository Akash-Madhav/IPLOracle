from fastapi import APIRouter
from models.query import QueryRequest, AskResponse
import logging, time, psutil, asyncio
from pinecone import Pinecone
from config import Config

from services.gemini import generate_answer, classify_fields  # ⬅️ import classifier

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

@ask_router.post("/ask", response_model=AskResponse)
async def ask_query(payload: QueryRequest) -> AskResponse:
    start_time = time.time()
    query = payload.query.strip() if payload.query else ""

    if not payload.vector:
        return AskResponse(query=query, answer="⚠️ Provide a vector embedding.", results=[])

    logger.info(f"🟢 Query received: {query}")
    heartbeat_task = asyncio.create_task(heartbeat())

    try:
        # 🔎 Query Pinecone with a larger top_k for recall
        t1 = time.time()
        response = index.query(vector=payload.vector, top_k=1000, include_metadata=True)
        print(f"⏱ Pinecone search: {time.time() - t1:.2f}s")

        # 🧹 Collect metadata
        raw_results = [match.metadata for match in response["matches"]]
        results = [r for r in raw_results if r]
        print("✅ Results filtered")

        # 🧠 Step 1: Classify query to get relevant fields
        relevant_fields = classify_fields(query)
        logger.info(f"🎯 Relevant fields: {relevant_fields}")

        # 🧠 Step 2: Optional filter by Year if present in query
        if "2023" in query:
            results = [r for r in results if r.get("Year") == "2023"]

        # 🧠 Step 3: Sort results by the primary relevant field if numeric
        sort_field = None
        for f in relevant_fields:
            if f not in ["Player_Name", "Year"]:
                sort_field = f
                break
        if sort_field:
            try:
                results = sorted(results, key=lambda r: float(r.get(sort_field, "0")), reverse=True)
            except Exception:
                pass

        # 🧠 Step 4: Build context dynamically
        context_lines = []
        for r in results[:10]:  # top 10 after sorting
            line_parts = []
            for field in relevant_fields:
                if r.get(field):
                    line_parts.append(f"{field}: {r.get(field)}")
            if line_parts:
                context_lines.append(" | ".join(line_parts))
        context = "\n".join(context_lines)

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

        return AskResponse(query=query, answer=answer, results=results)

    finally:
        heartbeat_task.cancel()
        try:
            await heartbeat_task
        except asyncio.CancelledError:
            pass