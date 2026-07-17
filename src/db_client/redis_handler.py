import json
import os
import redis
from src.models.redis_keys import ROOM_KEY, OPEN_ROOMS_KEY, ROOM_TTL, ALL_ROOMS_KEY

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

class RedisHandler:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            socket_timeout=2,
            socket_connect_timeout=2)

    def get_value(self, key):
        """Get value from Redis by key"""
        return self.client.get(key)

    def get_room(self, room_id):
        """Get room from Redis by room_id, parsed from JSON. Returns None if missing."""
        raw = self.get_value(key=ROOM_KEY.format(room_id))
        return json.loads(raw) if raw is not None else None

    def get_all_rooms(self):
        """Get all rooms from Redis. Returns an empty list if none are found."""
        rooms = []
        for key in self.client.keys(ROOM_KEY.format("*")):
            raw = self.client.get(key)
            if raw is not None:
                rooms.append(json.loads(raw))
        return rooms

    def get_open_rooms_ids(self):
        """Get all open room ids from Redis. Returns an empty list if none are found."""
        return [item.decode() for item in self.client.smembers(OPEN_ROOMS_KEY)]

    def clear(self):
        """Clear all data from Redis"""
        self.client.flushdb()

    def terminate(self):
        """Clear all data and close Redis"""
        self.clear()
        self.client.close()