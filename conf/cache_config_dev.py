CACHE_CONFIG = {
    'api_cache' : {
        'enable' : True,
        'type' : 'remote',
        'db': 6,
        'host': 'cache_1',
        'port': 6390
        },
    }

VC_REDIS_CONF = {
    'host': 'cache_1',
    'port': 6390,
    'db': 8
    }
