from fastapi import APIRouter
from models.query import QueryRequest
from services.loader import get_resources
from services.gemini import generate_answer
from pydantic import BaseModel
from typing import List, Dict
import logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AskResponse(BaseModel):
    query: str
    answer: str
    results: List[Dict]

ask_router = APIRouter()

@ask_router.post("/", response_model=AskResponse)
async def ask_query(payload: QueryRequest):
    query = payload.query.strip()

    if not query:
        return {"answer": "⚠️ Please provide a question."}

    model, index, metadata = get_resources()
    if not all([model, index, metadata]):
        return {"answer": "⚠️ Backend resources not loaded. Please try again later."}

    logger.info(f"🟢 Query received: {query}")
    try:
        query_emb = model.encode([query])
        D, I = index.search(query_emb.astype("float32"), k=5)
        results = [metadata[i] for i in I[0]]
    except Exception as e:
        logger.error(f"❌ FAISS search failed: {e}")
        return {
            "query": query,
            "answer": "❌ Internal error during semantic search. Please try again later.",
            "results": []
        }
    context = "\n".join([
        f"{r['Player_Name']} - Runs: {r['Runs_Scored']}, Wickets: {r['Wickets_Taken']}, Matches: {r['Matches_Batted']}, Average: {r['Batting_Average']}, Economy: {r.get('Economy_Rate', 'N/A')}"
        for r in results
    ])

    answer = generate_answer(query, context)

    return {"query": query, "answer": answer, "results": results}