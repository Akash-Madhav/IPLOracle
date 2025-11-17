from pydantic import BaseModel
from typing import List, Dict

class QueryRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    query: str
    answer: str
    results: List[Dict]