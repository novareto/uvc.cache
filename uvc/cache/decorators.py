import logging
from functools import wraps
from zope.component import getUtility
from .interfaces import IStore
from .stores import RedisStore, DEFAULT_VALUE
from datetime import timedelta
from cromlech.marshallers import PickleMarshaller


logger = logging.getLogger('uvc.cache')


def cache_me(marshaller, store_name='redis', lifetime=600):
    store = getUtility(IStore, name=store_name)

    def cache(func):
        @wraps(func)
        def cache_replacement(*args, **kwargs):
            key = marshaller(func, *args, **kwargs)
            value = store.get(key)
            if value is DEFAULT_VALUE:
                value = func(*args, **kwargs)
                store.set(key, value, delta=lifetime)
                logger.debug('set value %s with key %s' % (value, key))
            else:
                logger.debug('get value %s from cache with key %s' % (value, key))
            return value
        return cache_replacement
    return cache


def remove_from_cache(marshaller, store_name='redis'):
    store = getUtility(IStore, name=store_name)

    def invalidate(func):
        @wraps(func)
        def invalidate_replacement(*args, **kwargs):
            key = marshaller(func, *args, **kwargs)
            deleted = store.delete(key)
            logger.debug('remove key %s from store' % key)
            return func(*args, **kwargs)
        return invalidate_replacement
    return invalidate
