ROOM_KEY = "room:{}"           # room:ABC123
OPEN_ROOMS_KEY = "rooms:open"  # Redis Set of open room IDs
ROOM_TTL = 60 * 60 * 6        # 6 hours — rooms auto-expire from Redis
