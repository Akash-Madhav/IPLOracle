from fastapi import APIRouter
from models.query import QueryRequest, AskResponse
import logging, time

from services.loader import get_resources
from services.embedding import get_embedding
from services.gemini import generate_answer

logger = logging.getLogger(__name__)
ask_router = APIRouter()

# Lazy globals
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

@ask_router.post("/", response_model=AskResponse)
async def ask_query(payload: QueryRequest):
    global index, metadata
    start_time = time.time()

    query = payload.query.strip()
    if not query:
        return {"query": query, "answer": "⚠️ Provide a question.", "results": []}

    logger.info(f"🟢 Query received: {query}")

    # Lazy load FAISS + metadata here
    if index is None or metadata is None:
        print("🔥 Loading FAISS + metadata...")
        index, metadata = get_resources()

    emb_text = f"Player stats for {query}"
    query_emb = [get_embedding(emb_text)]

    D, I = index.search(query_emb, k=20)
    raw_results = [metadata[i] for i in I[0]]
    results = filter_results(raw_results, query)

    context = "\n".join([r["combined_text"] for r in results])
    answer = generate_answer(query, context)

    logger.info(f"⏱ Query processed in {time.time() - start_time:.2f}s")

    return {"query": query, "answer": answer, "results": results}
