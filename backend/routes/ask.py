from fastapi import APIRouter
from models.query import QueryRequest
from services.loader import get_resources
from services.gemini import generate_answer
from pydantic import BaseModel
from typing import List, Dict
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔍 Token-based fuzzy filter
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

@ask_router.post("/", response_model=AskResponse)
async def ask_query(payload: QueryRequest):
    query = payload.query.strip()

    if not query:
        return {"query": query, "answer": "⚠️ Please provide a question.", "results": []}

    model, index, metadata = get_resources()
    if not all([model, index, metadata]):
        return {"query": query, "answer": "⚠️ Backend resources not loaded. Please try again later.", "results": []}

    logger.info(f"🟢 Query received: {query}")

    try:
        # 🔁 Rephrase query to match combined_text structure
        query_for_embedding = f"Player stats for {query}"
        query_emb = model.encode([query_for_embedding])

        # 🔍 Search top 20 for broader semantic context
        D, I = index.search(query_emb.astype("float32"), k=20)
        raw_results = [metadata[i] for i in I[0]]

        # 🔍 Apply fuzzy filter
        results = filter_results(raw_results, query)

        logger.info(f"📊 FAISS distances: {D[0]}")
        logger.info(f"📊 Top results: {[r['Player_Name'] for r in results]}")

    except Exception as e:
        logger.error(f"❌ FAISS search failed: {e}")
        return {
            "query": query,
            "answer": "❌ Internal error during semantic search. Please try again later.",
            "results": []
        }

    # 🧠 Build context from combined_text
    context = "\n".join([r["combined_text"] for r in results])

    # 🤖 Generate answer via Gemini
    answer = generate_answer(query, context)

    return {"query": query, "answer": answer, "results": results}