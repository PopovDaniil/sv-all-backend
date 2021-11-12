import json
import redis
from decouple import config

REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')
REDIS_DB = config('REDIS_DB')
class RedisConnection:
    client = ''
    def __init__(self):
        redis_url = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
        self.client = redis.StrictRedis.from_url(redis_url, decode_responses=True)
    def read_configs(self):
        stored_config = self.client.get('stored_config')
        if stored_config:
            return json.loads(stored_config.decode('utf-8'))