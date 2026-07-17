# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

API, DB, and UI test automation for the Dobble game project (server lives in a separate repo: https://github.com/amitakapita/Dobble). Tests exercise the game server's HTTP API and validate its state in Redis directly.

## Running Tests

Tests require the Dobble server and a Redis instance to be running. Connection details (`BASE_URL`, `REDIS_HOST`, `REDIS_PORT`) are read from `.env` via pytest-env (`env_files` in pytest.ini).

```powershell
.venv/Scripts/python.exe -m pytest                                  # all tests (pytest.ini addopts points at tests/)
.venv/Scripts/python.exe -m pytest -m api                           # API tests only
.venv/Scripts/python.exe -m pytest tests/api_tests/test_lobbies.py::TestLobbiesAPI::test_get_lobbies_rooms  # single test
```

Markers are strict (`--strict-markers`); new markers must be registered in pytest.ini.

## Architecture

Three layers, wired together by session-scoped fixtures in the root `conftest.py`:

1. **Low-level handlers** — `src/api_client/api_handler.py` (thin `requests.Session` wrapper: `send_get`/`send_post` against `BASE_URL`) and `src/db_client/redis_handler.py` (Redis reads keyed by templates in `src/models/redis_keys.py`; `clear()` flushes the DB and is called by tests for isolation, and by `terminate()` at session end).

2. **Domain modules** — `src/api_client/lobbies_module.py` (`LobbyModule`) composes both handlers. It owns endpoint calls (paths in `src/models/api_endpoints.py`) and reusable assertion helpers: `validate_schema_match` (pydantic schema check), `validate_response` (status + body vs expected model), and `validate_room_db_data` (compares a `RoomResponse` built from Redis against an expected one — cross-checks API behavior against DB state).

3. **Schemas** — `src/schemas/api_lobbies_schemas.py` (pydantic models for API request/response payloads, named by method: `POSTLobbiesSchema`, `GETLobbySchema`, ...) and `src/schemas/db_room_schemas.py` (`RoomResponse`/`Player`, mirroring the room JSON stored in Redis).

Tests (`tests/api_tests/`) use only the domain-module layer plus schemas: arrange state via module calls (clearing Redis first), act via the API, then assert both the API response and the Redis contents. New API areas should follow the same pattern: endpoint constants in `src/models/`, schemas in `src/schemas/`, a domain module composing the handlers, and a session-scoped fixture in `conftest.py`.

## Conventions

- Domain knowledge is encoded in tests/schemas rather than fetched from the server repo: new rooms have `state="waiting"`, `max_players=8`, one player (the host) with `score=0` and empty piles.
- Tests follow Arrange / Act / Assert comments and start by clearing Redis.
