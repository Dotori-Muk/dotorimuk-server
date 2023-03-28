from core.config import settings
from redis import StrictRedis


def get_redis_db():
    conn = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    try:
        yield conn
    finally:
        conn.close()
