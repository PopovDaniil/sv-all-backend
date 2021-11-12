import redis
from decouple import config

class RedisListener(object):
    def __init__(self, connection, channel, handler):
        self.clients = []
        self.connection = connection
        self.channel = channel
        self.handler = handler
        self._connection()
    def _connection(self):
        self.pubsub = self.connection.pubsub(
            ignore_subscribe_messages=False)
        self.pubsub.subscribe(**{self.channel: self.handler})
        self.thread = self.pubsub.run_in_thread(sleep_time=0.001)
    def register_handler(self, client):
        self.clients.append(client)

    def handler(self, message):
        _message = message['data']
        if type(_message) != int:
            self.send(_message)


    def send(self, data):
        for client in self.clients:
            try:
                client.send(data)
            except Exception:
                self.clients.remove(client)