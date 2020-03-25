from .interfaces import IStore
from datetime import timedelta
from cromlech.marshallers import PickleMarshaller


DEFAULT_VALUE = object()


class RedisStore:

    def __init__(self, redis, prefix='cache:', marshaller=PickleMarshaller):
        self.redis = redis
        self.marshaller = marshaller
        self.prefix = prefix

    def get(self, key, default=DEFAULT_VALUE):
        key = self.prefix + key
        data = self.redis.get(key)
        if data is not None:
            return self.marshaller.loads(data)
        return default

    def set(self, key, value, delta=300):
        key = self.prefix + key
        data = self.marshaller.dumps(value)
        self.redis.setex(key, timedelta(seconds=delta), data)

    def clear(self, key):
        key = self.prefix + key
        self.redis.delete(key)

    delete = clear

    def touch(self, key):
        key = self.prefix + key
        self.redis.expire(key, timedelta(seconds=self.delta))
