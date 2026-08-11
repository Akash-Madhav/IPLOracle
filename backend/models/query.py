from pydantic import BaseModel
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    query: Optional[str] = None   
    vector: Optional[List[float]] = None

class AskResponse(BaseModel):
    query: str
    answer: str
    results: List[Dict]

class PlayerListResponse(BaseModel):
    total_players: int
    players: List[str]

class PlayerDetailResponse(BaseModel):
    player_name: str
    total_records: int
    records: List[Dict]