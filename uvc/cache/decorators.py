import logging
from functools import wraps
from zope.component import queryUtility
from .interfaces import IStore
from .stores import RedisStore, DEFAULT_VALUE
from datetime import timedelta
from cromlech.marshallers import PickleMarshaller


logger = logging.getLogger('uvc.cache')


def cache_me(marshaller, store_name='redis', lifetime=600):

    def getStore():
        return queryUtility(IStore, name=store_name)

    def cache(func):
        @wraps(func)
        def cache_replacement(*args, **kwargs):
            store = getStore()
            if store is None:
                return func(*args, **kwargs)

            try:
                key = marshaller(func, *args, **kwargs)
                value = store.get(key)
            except Exception as exc:
                # this is very ... unspecific.
                logger.warning(
                    'Store `get` failed with error %s' % exc)
                value = DEFAULT_VALUE

            if value is DEFAULT_VALUE:
                value = func(*args, **kwargs)
                try:
                    store.set(key, value, delta=lifetime)
                    logger.info(
                        'set value %s with key %s' % (value, key))
                except Exception as exc:
                    logger.warning(
                        'Store `set` failed with error %s' % exc)
            else:
                logger.info(
                    'get value %s from cache with key %s' % (value, key))
            return value
        return cache_replacement
    return cache


def remove_from_cache(marshaller, store_name='redis'):

    def invalidate(func):
        @wraps(func)
        def invalidate_replacement(*args, **kwargs):
            store = getUtility(IStore, name=store_name)
            key = marshaller(func, *args, **kwargs)
            deleted = store.delete(key)
            logger.info('remove key %s from store' % key)
            return func(*args, **kwargs)
        return invalidate_replacement
    return invalidate
