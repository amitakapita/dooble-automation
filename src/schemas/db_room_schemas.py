from pydantic import BaseModel
from typing import List, Dict

class Player(BaseModel):
    player_id: str
    name: str
    score: int
    pile: List[dict]

class RoomResponse(BaseModel):
    room_id: str
    host_name: str
    max_players: int
    state: str
    center_pile: List[dict]
    players: Dict[str, Player]
