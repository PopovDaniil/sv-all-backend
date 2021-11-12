from common.RedisConnection import RedisConnection

class ImageSender(RedisConnection):
    def send_image(self, data: str):
        self.client.publish('image', data)