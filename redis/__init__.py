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
            'SOCKET_READ_SIZE':65536,
            'CLIENT_NAME': None,
            'USERNAME': None,
            'HELTH_CHECK_INTERVAL': 0,
            'NEXT_HELTH_CHECK': 0,
        },
        'OVERRIDES': { }
    }
}

def update(d, u):
    for k, v in u.items():
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
    AuthenticationWrongNumberOfArgsError,
    BusyLoadingError,
    ChildDeadlockedError,
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


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


__version__ = '3.4.1'
VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = [
    'AuthenticationError',
    'AuthenticationWrongNumberOfArgsError',
    'BlockingConnectionPool',
    'BusyLoadingError',
    'ChildDeadlockedError',
    'Connection',
    'ConnectionError',
    'ConnectionPool',
    'DataError',
    'from_url',
    'InvalidResponse',
    'PubSubError',
    'ReadOnlyError',
    'Redis',
    'RedisError',
    'ResponseError',
    'SSLConnection',
    'StrictRedis',
    'TimeoutError',
    'UnixDomainSocketConnection',
    'WatchError',
]
