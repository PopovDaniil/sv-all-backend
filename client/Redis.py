import sys
sys.path.append('..')

from common.RedisConnection import RedisConnection
class ClientRedisConnection(RedisConnection):
    def log(self, data: str):
        self.client.publish('logger',data)