from gettext import find

import pytest

from src.api_client.lobbies_module import LobbyModule
from src.schemas.db_room_schemas import Player


@pytest.mark.api
class TestLobbiesAPI:
    def _generate_room(self, lobby_module, host_name):
        room_response = lobby_module.create_new_lobby(host_name=host_name)
        return room_response.json()

    def test_get_lobbies_no_rooms(self, lobby_module):
        """Checks the amount of lobbies available is 0 when no room opened."""
        # Arrange
        lobby_module.redis_client.clear()

        # Act
        response = lobby_module.get_open_lobbies()

        # Assert
        assert response.status_code == 200
        assert response.json() == []

    def test_get_lobbies_rooms(self, lobby_module, host_names):
        """Checks the amount of lobbies available is 1 when a room is opened."""
        """I need to make the test to create rooms like in "RoomResponse", 
        and then for api response test just equalize them in lobbies_module.validate_response(),
        and validate the db by sending the RoomResponse in lobbies_module.validate_room_db_data() and compare it with the get response room for each room"""
        pass
        # # Arrange
        # lobby_module.redis_client.clear()
        # expected_rooms = []
        # for name in host_names:
        #     expected_rooms.append(self._generate_room(lobby_module, host_name=name))
        #
        # # Act
        # get_response = lobby_module.get_open_lobbies()
        # rooms = get_response.json()
        #
        # # Assert
        # assert get_response.status_code == 200
        # assert len(get_response.json()) == len(host_names)
        # for room in rooms:
        #     # get expected room by room_id
        #     expected_room = dict(filter(lambda r: r["room_id"] == room["room_id"], expected_rooms))
        #     expected_rooms.remove(expected_room)
        #
        #     assert expected_room is not None
        #     assert room["host"] == expected_room["host"]
        #     assert room["state"] == "waiting"
        #     assert room["player_count"] == 1
        #     assert room["max_players"] == 8
        #
        #     player = Player(player_id=expected_room["player_id"], )