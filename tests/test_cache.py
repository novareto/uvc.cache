import pytest
from time import sleep
from uvc.cache.decorators import cache_me
from uvc.cache.stores import RedisStore, IStore, DEFAULT_VALUE
from zope.component import getGlobalSiteManager


def simple_marshaller(func, *args, **kwargs):
    return func.__name__ + '_' + '_'.join(args)


@pytest.fixture
def store(redisdb):
    storage = RedisStore(redisdb)
    gsm = getGlobalSiteManager()
    gsm.registerUtility(storage, IStore, name='redis')
    yield storage
    gsm.unregisterUtility(storage, IStore, name='redis')


def test_caching(store):

    @cache_me(simple_marshaller, lifetime=1)
    def testing(a, b):
        return a + b

    assert testing('a', 'b') == 'ab'
    assert store.get('testing_a_b') == 'ab'

    sleep(1)
    assert store.get('testing_a_b') is DEFAULT_VALUE
