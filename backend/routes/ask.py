from fastapi import APIRouter
from models.query import QueryRequest
from services.loader import get_resources
from services.gemini import generate_answer
from services.embedding import get_embedding
from pydantic import BaseModel
from typing import List, Dict
import logging
import time
import gc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def filter_results(raw_results, query):
    query_lower = query.lower()
    filtered = []

    for r in raw_results:
        name = r["Player_Name"].lower()
        year = r["Year"].lower()
        combined = r["combined_text"].lower()
        role = r.get("Role", "").lower()

        if query_lower in name or query_lower in year or query_lower in combined or query_lower in role:
            filtered.append(r)

    return filtered if filtered else raw_results

class AskResponse(BaseModel):
    query: str
    answer: str
    results: List[Dict]

ask_router = APIRouter()

@ask_router.get("/")
async def ask_info():
    return {
        "message": "Use POST to send a query like: { \"query\": \"Who scored the most runs in 2024?\" }"
    }

@ask_router.post("/", response_model=AskResponse)
async def ask_query(payload: QueryRequest):
    start_time = time.time()
    query = payload.query.strip()

    if not query:
        return {"query": query, "answer": "⚠️ Please provide a question.", "results": []}

    index, metadata = get_resources()

    if not all([index, metadata]):
        return {"query": query, "answer": "⚠️ Backend resources not loaded. Please try again later.", "results": []}

    logger.info(f"🟢 Query received: {query}")

    try:
        query_for_embedding = f"Player stats for {query}"
        MAX_CHARS = 2000
        if len(query_for_embedding) > MAX_CHARS:
            logger.warning(f"⚠️ Query too long ({len(query_for_embedding)} chars); truncating.")
            query_for_embedding = query_for_embedding[:MAX_CHARS]

        query_emb = [get_embedding(query_for_embedding)]
        gc.collect()

        if not query_emb[0]:
            logger.error("❌ Empty embedding returned")
            return {
                "query": query,
                "answer": "❌ Failed to generate embedding. Please try again later.",
                "results": []
            }

        D, I = index.search(query_emb, k=20)
        raw_results = [metadata[i] for i in I[0]]
        results = filter_results(raw_results, query)
        gc.collect()

        logger.info(f"📊 FAISS distances: {D[0]}")
        logger.info(f"📊 Top results: {[r['Player_Name'] for r in results]}")

        context = "\n".join([r["combined_text"] for r in results])
        answer = generate_answer(query, context)

    except Exception as e:
        logger.error(f"❌ FAISS or Gemini pipeline failed: {e}")
        return {
            "query": query,
            "answer": "❌ Internal error during semantic search. Please try again later.",
            "results": []
        }

    finally:
        # ✅ Explicit cleanup
        try:
            del index, metadata, raw_results, results, D, I, query_emb, context
        except Exception:
            pass
        gc.collect()

    elapsed = time.time() - start_time
    logger.info(f"⏱️ Query processed in {elapsed:.2f} seconds")

    return {"query": query, "answer": answer, "results": results}