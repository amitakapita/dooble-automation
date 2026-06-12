import os

import pytest

from src.api_client.api_handler import ApiHandler
from src.api_client.lobbies_module import LobbyModule
from src.db_client.redis_handler import RedisHandler


@pytest.fixture(scope="session")
def redis_conn():
    redis_client = RedisHandler(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
    )

    yield redis_client
    redis_client.terminate()

@pytest.fixture(scope="session")
def api_conn():
    api_client = ApiHandler(os.getenv("BASE_URL"))
    yield api_client

@pytest.fixture(scope="session")
def lobby_module(api_conn, redis_conn):
    lobby_module1 = LobbyModule(
        api_handler=api_conn,
        redis_handler=redis_conn
    )
    yield lobby_module1