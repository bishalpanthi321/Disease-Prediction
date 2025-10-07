"""
Redis Cache Configuration
"""

import redis 
from backend.config import REDIS_HOST, REDIS_PORT, REDIS_DB
 
#Initialize Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port =REDIS_PORT,
    db = REDIS_DB, 
    decode_responses=True
)

def get_redis_client():
    """Get Redis Client Instance"""
    return redis_client