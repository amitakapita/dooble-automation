from pydantic import BaseModel

class POSTLobbiesSchema(BaseModel):
    host_name: str

class POSTLobbiesJoinSchema(BaseModel):
    room_id: str
    player_name: str

class POSTLobbiesStartSchema(BaseModel):
    room_id: str
    player_id: str

class POSTLobbiesResponseSchema(BaseModel):
    room_id: str
    player_id: str
    message: str