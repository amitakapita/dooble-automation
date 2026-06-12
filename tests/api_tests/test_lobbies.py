import pytest

from src.api_client.lobbies_module import LobbyModule

@pytest.mark.api
class TestLobbiesAPI:
    def test_get_lobbies_no_rooms(self, lobby_module):
        """Checks the amount of lobbies available is 0 when no room opened."""
        # Arrange
        lobby_module.redis_client.clear()

        # Act
        response = lobby_module.get_open_lobbies()

        # Assert
        assert response.status_code == 200
        assert response.json() == []
