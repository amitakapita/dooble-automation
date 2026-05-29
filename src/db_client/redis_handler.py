import os
import redis
from src.models.redis_keys import ROOM_KEY, OPEN_ROOMS_KEY, ROOM_TTL

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

class RedisHandler:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db)

    def get_value(self, key):
        """Get value from Redis by key"""
        return self.client.get(key)

    def get_room(self, room_id):
        """Get room from Redis by room_id"""
        return self.get_value(key=ROOM_KEY.format(room_id))

    def get_open_rooms_ids(self):
        """Get all open room ids"""
        return self.get_value(key=OPEN_ROOMS_KEY)

    def clear(self):
        """Clear all data from Redis"""
        self.client.flushdb()

    def terminate(self):
        """Clear all data and close Redis"""
        self.clear()
        self.client.close()