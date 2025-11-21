from pydantic import BaseModel
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    query: Optional[str] = None   
    vector: List[float]           

class AskResponse(BaseModel):
    query: str
    answer: str
    results: List[Dict]