from pydantic import BaseModel
from typing import List, Dict

class QueryRequest(BaseModel):
    __slots__ = ("query",)
    query: str

class AskResponse(BaseModel):
    __slots__ = ("query", "answer", "results")
    query: str
    answer: str
    results: List[Dict]