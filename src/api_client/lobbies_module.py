from pydantic import ValidationError

from src.api_client.api_handler import ApiHandler
from src.db_client.redis_handler import RedisHandler
from src.models.api_endpoints import LOBBIES_GET, LOBBIES_POST, LOBBIES_JOIN_POST, LOBBIES_START_POST
from src.schemas.api_lobbies_schemas import POSTLobbiesSchema, POSTLobbiesJoinSchema, POSTLobbiesResponseSchema, \
    POSTLobbiesStartSchema
from src.schemas.db_room_schemas import RoomResponse


class LobbyModule:
    def __init__(self, api_handler: ApiHandler, redis_handler: RedisHandler):
        self.api_client = api_handler
        self.redis_client = redis_handler

    def get_open_lobbies(self):
        return self.api_client.send_get(LOBBIES_GET)

    def post_new_lobby(self, payload: POSTLobbiesSchema):
        return self.api_client.send_post(LOBBIES_POST, payload.model_dump())

    def  post_join_lobby(self, payload: POSTLobbiesJoinSchema):
        return self.api_client.send_post(LOBBIES_JOIN_POST, payload.model_dump())

    def post_start_lobby(self, room_id: str, payload: POSTLobbiesStartSchema):
        return self.api_client.send_post(LOBBIES_START_POST.format(room_id), payload.model_dump())

    # def is_room_in_db(self, room_id: str) -> bool:
    #     return self.redis_client.get_room(room_id) is not None

    def validate_room_db_data(self, room_id: str, expected_room: RoomResponse):
        """Validate that the room data in Redis matches the expected room data."""
        room_db_data = RoomResponse(**self.redis_client.get_room(room_id))

        assert room_db_data is not None, f"No room found with room_id = {room_id}"
        assert room_db_data == expected_room, \
            f"Room data mismatch for room_id = {room_id}: expected {expected_room}, got {room_db_data}"

    def validate_schema_match(self, payload, expected_schema):
        """Validate the schema of the payload matches the expected schema."""
        try:
            expected_schema.model_validate(payload)
        except ValidationError as e:
            raise AssertionError(f"Response schema validation failed: {e}") from e

    def validate_response(self, response, expected_response, expected_status_code=200):
        """Validate the response data matches the expected response data"""
        assert response.status_code == expected_status_code

        payload = response.json()

        assert payload == expected_response.model_dump()