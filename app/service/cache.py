from flask_caching import Cache, CachedResponse

from application import application

cache = Cache(application)

def configure_cache():
    debug = application.config["ENV"] == 'development'
    cacheType = "SimpleCache"
    if debug:
        cacheType = "NullCache"


    config = {
        "DEBUG": debug,          # some Flask specific configs
        "CACHE_TYPE": cacheType,
        "CACHE_DEFAULT_TIMEOUT": 300
    }
    application.config.from_mapping(config)


