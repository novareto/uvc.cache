import grok

from zope.component import getUtility
from lovely.memcached.utility import MemcachedClient
from lovely.memcached.interfaces import IMemcachedClient


grok.global_utility(MemcachedClient, IMemcachedClient, direct=False)


def get_memcached_client():
    return getUtility(IMemcachedClient)
