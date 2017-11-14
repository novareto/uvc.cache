# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import logging
from uvc.cache.util import get_memcached_client


logger = logging.getLogger('uvc.cache')


def cache_me(marshaller, lifetime=None, ns=None, raw=False, dependencies=[]):

    def cache(func):
        def cache_replacement(*args, **kwargs):
            key = marshaller(func, *args, **kwargs)
            client = get_memcached_client()
            value = client.query(key, ns=ns, raw=raw)
            logger.debug('get value %s from cache with key %s' % (value, key))
            if not value:
                value = func(*args, **kwargs)
                client.set(value, key, lifetime=lifetime, ns=ns, raw=raw)
                logger.debug('set value %s with key %s' % (value, key))
            return value
        return cache_replacement
    return cache


def remove_from_cache(marshaller):
    def invalidate(func):
        def invalidate_replacement(*args, **kwargs):
            key = marshaller(func, *args, **kwargs)
            client = get_memcached_client()
            deleted = client.invalidate(key, raw=False)
            logger.debug('remove key %s from store' % key)
            return func(*args, **kwargs)
        return invalidate_replacement
    return invalidate
