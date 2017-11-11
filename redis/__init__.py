import collections

config = {
    'CONNECTION':{
        'DEFAULTS':{
            'HOST': 'localhost',
            'PORT': 6379,
            'DB': 0,
            'PASSWORD': None,
            'SOCKET_TIMEOUT': None,
            'SOCKET_CONNECT_TIMEOUT': None,
            'SOCKET_KEEPALIVE_OPTIONS': None,
            'SOCKET_KEEPALIVE': False,
            'SOCKET_TYPE': 0,
            'RETRY_ON_TIMEOUT': False,
            'ENCODING': 'utf-8',
            'ENCODING_ERRORS': 'strict',
            'DECODE_RESPONSES': False,
            'PARSER_CLASS': None,
            'SOCKET_READ_SIZE':65536

        },
        'OVERRIDES': { }
    }

}
def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

config_loaded = False
def load_config():
    try:
        from django.conf import settings
        # if django is installed, use django settings
        global config

        update(config, getattr(settings, 'REDIS_CONFIG', {}))

    except ImportError:
        pass
    global config_loaded
    config_loaded = True

def get_config(section,key,kwargs=None):
    if not config_loaded:
        load_config()
    overrides = config[section].get('OVERRIDES', {})
    defaults = config[section].get('DEFAULTS', {})
    if kwargs is None:
        kwargs={}
    try:
        return overrides.get(key,kwargs.get(key.lower(),defaults[key]))
    except KeyError:
        raise KeyError('Config {}:{} has no default!'.format(section,key))


from redis.client import Redis, StrictRedis
from redis.connection import (
    BlockingConnectionPool,
    ConnectionPool,
    Connection,
    SSLConnection,
    UnixDomainSocketConnection
)
from redis.utils import from_url
from redis.exceptions import (
    AuthenticationError,
    BusyLoadingError,
    ConnectionError,
    DataError,
    InvalidResponse,
    PubSubError,
    ReadOnlyError,
    RedisError,
    ResponseError,
    TimeoutError,
    WatchError
)


__version__ = '2.10.5.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = [
    'Redis', 'StrictRedis', 'ConnectionPool', 'BlockingConnectionPool',
    'Connection', 'SSLConnection', 'UnixDomainSocketConnection', 'from_url',
    'AuthenticationError', 'BusyLoadingError', 'ConnectionError', 'DataError',
    'InvalidResponse', 'PubSubError', 'ReadOnlyError', 'RedisError',
    'ResponseError', 'TimeoutError', 'WatchError'
]


