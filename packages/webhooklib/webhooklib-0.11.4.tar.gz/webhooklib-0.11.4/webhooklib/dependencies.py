import contextlib
import os

from redis import Redis


def get_redis_sync():
    redis = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)
    yield redis
    redis.close()


get_redis_cm = contextlib.contextmanager(get_redis_sync)
