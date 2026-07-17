from pydantic import BaseModel

class POSTLobbiesSchema(BaseModel):
    host_name: str

class POSTLobbiesJoinSchema(BaseModel):
    room_id: str
    player_name: str

class POSTLobbiesStartSchema(BaseModel):
    room_id: str
    player_id: str

class GETLobbySchema(BaseModel):
    room_id: str
    host: str
    state: str
    player_count: int
    max_players: int

class POSTLobbiesResponseSchema(BaseModel):
    room_id: str
    player_id: str
    message: str