from fastapi import APIRouter
from models.query import QueryRequest, AskResponse
import logging, time, psutil, asyncio
from pinecone import Pinecone
import os
from dotenv import load_dotenv

from services.gemini import generate_answer

load_dotenv()
logger = logging.getLogger(__name__)
ask_router = APIRouter()

# 🔐 Load Pinecone credentials
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "ipl-players"

# 🔗 Connect to Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

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
        # 🔎 Query Pinecone directly with frontend-provided vector
        t1 = time.time()
        response = index.query(vector=payload.vector, top_k=20, include_metadata=True)
        print(f"⏱ Pinecone search: {time.time() - t1:.2f}s")

        # 🧹 Filter results
        raw_results = [match.metadata for match in response["matches"]]
        results = [r for r in raw_results if r]
        print("✅ Results filtered")

        # 🧠 Build context for Gemini (optional)
        context = "\n".join([
            " | ".join([f"{k}: {v}" for k, v in r.items() if v])[:500]
            for r in results[:3]
        ])

        # ✨ Generate answer
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