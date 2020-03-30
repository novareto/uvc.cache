import pytest
from time import sleep
from uvc.cache.decorators import cache_me
from uvc.cache.stores import RedisStore, IStore, DEFAULT_VALUE
from zope.component import getGlobalSiteManager


def simple_marshaller(func, *args, **kwargs):
    return func.__name__ + '_' + '_'.join(args)


class FaultyStore:

    def get(self, key, default=DEFAULT_VALUE):
        raise KeyError(key)

    def set(self, key, value, delta=300):
        raise NotImplementedError("Store cannot set.")

    def clear(self, key):
        raise NotImplementedError("Store cannot clear.")

    delete = clear

    def touch(self, key):
        raise NotImplementedError("Store cannot touch.")


@pytest.fixture
def store(redisdb):
    storage = RedisStore(redisdb)
    gsm = getGlobalSiteManager()
    gsm.registerUtility(storage, IStore, name='redis')
    yield storage
    gsm.unregisterUtility(storage, IStore, name='redis')


@pytest.fixture
def faulty_store():
    storage = FaultyStore()
    gsm = getGlobalSiteManager()
    gsm.registerUtility(storage, IStore, name='faulty')
    yield storage
    gsm.unregisterUtility(storage, IStore, name='faulty')


def test_caching(store):

    @cache_me(simple_marshaller, lifetime=1)
    def testing(a, b):
        return a + b

    assert testing('a', 'b') == 'ab'
    assert store.get('testing_a_b') == 'ab'

    sleep(1)
    assert store.get('testing_a_b') is DEFAULT_VALUE


def test_caching_no_store():

    @cache_me(simple_marshaller, lifetime=1)
    def testing(a, b):
        return a + b

    assert testing('a', 'b') == 'ab'
    assert testing('a', 'b') == 'ab'


def test_caching_faulty_store(faulty_store):

    @cache_me(simple_marshaller, lifetime=1, store_name='faulty')
    def testing(a, b):
        return a + b

    assert testing('a', 'b') == 'ab'
    assert testing('a', 'b') == 'ab'
