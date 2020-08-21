import redis

client = redis.Redis(host='localhost', port='6379', db=0)


class RedisPublish:
    def __init__(self, channel):
        self.channel = channel

    def publish(self, message):
        client.publish(self.channel, message)
