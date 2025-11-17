from fastapi import APIRouter
from models.query import QueryRequest, AskResponse
import logging, time, psutil, asyncio
import numpy as np

from services.loader import get_resources, clear_resources
from services.embedding import get_embedding
from services.gemini import generate_answer

logger = logging.getLogger(__name__)
ask_router = APIRouter()

index = None
metadata = None

@ask_router.get("/")
async def ask_info():
    return {"message": "POST { 'query': 'Who scored...' }"}

def filter_results(raw_results, query):
    q = query.lower()
    f = []
    for r in raw_results:
        if (
            q in r["Player_Name"].lower()
            or q in r["Year"].lower()
            or q in r["combined_text"].lower()
            or q in r.get("Role", "").lower()
        ):
            f.append(r)
    return f if f else raw_results

async def heartbeat(interval=30):
    try:
        while True:
            print("🔄 Heartbeat: still processing...")
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        print("🛑 Heartbeat stopped")

@ask_router.post("/ask", response_model=AskResponse)
async def ask_query(payload: QueryRequest) -> AskResponse:
    global index, metadata
    start_time = time.time()

    query = payload.query.strip()
    if not query:
        return AskResponse(query=query, answer="⚠️ Provide a question.", results=[])

    logger.info(f"🟢 Query received: {query}")
    heartbeat_task = asyncio.create_task(heartbeat())

    try:
        if index is None or metadata is None:
            print("🔥 Loading FAISS + metadata...")
            index, metadata = get_resources()

        t0 = time.time()
        emb_text = f"Player stats for {query}"
        query_emb = get_embedding(emb_text)
        query_emb = np.array([query_emb], dtype='float32')
        print(f"⏱ Embedding: {time.time() - t0:.2f}s")

        t1 = time.time()
        D, I = index.search(query_emb, k=20)
        print(f"⏱ FAISS search: {time.time() - t1:.2f}s")

        t2 = time.time()
        raw_results = [metadata[i] for i in I[0]]
        results = filter_results(raw_results, query)
        print(f"⏱ Filtering: {time.time() - t2:.2f}s")

        context = "\n".join([r["combined_text"][:500] for r in results[:3]])
        t3 = time.time()
        try:
            answer = generate_answer(query, context)
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

@ask_router.on_event("shutdown")
def shutdown_event():
    clear_resources()
    from services.embedding import clear_model
    clear_model()