import pytest

from src.api_client.lobbies_module import LobbyModule
from src.schemas.api_lobbies_schemas import GETLobbySchema
from src.schemas.db_room_schemas import Player, RoomResponse


@pytest.mark.api
class TestLobbiesAPI:
    def _generate_room(self, lobby_module, host_name):
        room_response = lobby_module.create_new_lobby(host_name=host_name)
        return room_response.json()

    def _build_expected_room(self, create_payload, host_name):
        """Build the RoomResponse a freshly created room is expected to have."""
        host = Player(
            player_id=create_payload["player_id"],
            name=host_name,
            score=0,
            pile=[],
        )
        return RoomResponse(
            room_id=create_payload["room_id"],
            host_name=host_name,
            max_players=8,
            state="waiting",
            center_pile=[],
            players={host.player_id: host},
        )

    def test_get_lobbies_no_rooms(self, lobby_module):
        """Checks the amount of lobbies available is 0 when no room opened."""
        # Arrange
        lobby_module.redis_client.clear()

        # Act
        response = lobby_module.get_open_lobbies()

        # Assert
        assert response.status_code == 200
        assert response.json() == []
        assert lobby_module.redis_client.get_open_rooms_ids() == []
        assert lobby_module.redis_client.get_all_rooms() == []

    def test_get_lobbies_rooms(self, lobby_module, host_names):
        """Checks every opened room is returned by GET lobbies and stored correctly in the DB."""
        # Arrange
        lobby_module.redis_client.clear()
        expected_rooms = {}
        for name in host_names:
            create_payload = self._generate_room(lobby_module, host_name=name)
            expected_rooms[create_payload["room_id"]] = self._build_expected_room(create_payload, host_name=name)

        # Act
        get_response = lobby_module.get_open_lobbies()
        rooms = get_response.json()

        # Assert
        amount_rooms = len(rooms)
        assert get_response.status_code == 200
        assert amount_rooms == len(host_names)
        assert amount_rooms == len(expected_rooms)

        assert amount_rooms == len(lobby_module.redis_client.get_all_rooms())
        assert amount_rooms == len(lobby_module.redis_client.get_open_rooms_ids())

        for room in rooms:
            lobby_module.validate_schema_match(room, GETLobbySchema)

            expected_room = expected_rooms.pop(room["room_id"], None)
            assert expected_room is not None, f"Unexpected room in lobbies list: {room['room_id']}"

            assert room["host"] == expected_room.host_name
            assert room["state"] == expected_room.state
            assert room["player_count"] == len(expected_room.players)
            assert room["max_players"] == expected_room.max_players

            lobby_module.validate_room_db_data(room["room_id"], expected_room)

        assert not expected_rooms, f"Rooms missing from lobbies list: {list(expected_rooms)}"
