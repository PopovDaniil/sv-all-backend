from decouple import config

import sys
sys.path.append('..')

from common.RedisConnection import RedisConnection
class Redis(RedisConnection):
    def send_data(self, data: str):
        self.client.set('stored_config', data, ex=6000)
        self.client.publish('logger',data)