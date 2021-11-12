from client.Redis import ClientRedisConnection
from common.RedisListener import RedisListener

import sys
sys.path.append('..')

class ClientRedisListener(RedisListener):
    def __init__(self, connection, handler):
        super().__init__(connection.client, 'image', handler)