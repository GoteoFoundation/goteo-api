# -*- coding: utf-8 -*-
from datetime import datetime as dtdatetime
from dateutil.parser import parse
from functools import wraps
from flask.ext.cache import Cache

import pickle
from .helpers import *

from . import app
from .ratelimit import redis

# a long time, when the cars will fly...
INFINITE = 365 * 24 * 3600
if redis:
    redis_prefix = app.config['CACHE']['CACHE_KEY_PREFIX'].encode('utf-8') + b'KEY-ITEM/'

cache = Cache(app, config=app.config['CACHE'])

#
# CACHER BY ARGS FILTERS
#
# ======================
def get_key_list():
    """List all cached keys"""
    if redis:
        try:
            key_list = redis.keys(redis_prefix + b'*')
            keys = {}
            for key in key_list:
                val = redis.get(key)
                decoded = pickle.loads(val)
                keys[key[len(redis_prefix):]] = decoded
        except Exception as e:
            app.logger.debug('Error decoding key {key} [{e}]'.format(key=key, e=e))
    else:
        keys = cache.get('KEY-LIST')

    if not keys:
        return {}
    return keys


def add_key_list(key, timeout, time):
    """Save cache key to a listable set"""
    val = (timeout, time)
    if redis:
        # A more efficient way to touch a single key instead of retrieving the full set
        app.logger.debug('Adding key to REDIS {key} {val}'.format(key=key, val=val))
        v = pickle.dumps(val, pickle.HIGHEST_PROTOCOL)
        return redis.set(redis_prefix + key, v)

    keys = get_key_list()
    keys[key] = val
    return cache.set('KEY-LIST', keys, timeout=INFINITE)

def renew_key_list(key):
    if redis:
        # A more efficient way to touch a single key instead of retrieving the full set
        try:
            (timeout, time) = pickle.loads(redis.get(redis_prefix + key).decode('utf-8'))
            return add_key_list(key, timeout, dtdatetime.now())
        except:
            pass

    keys = get_key_list()
    if key in keys:
        (timeout, time) = keys[key]

    if timeout and time:
        return add_key_list(key, timeout, dtdatetime.now())

    return False

def cacher(f):
    """Caches methods for model classes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not app.config['CACHING']:
            return f(*args, **kwargs)

        key = pickle.dumps((f.__name__, args, kwargs), pickle.HIGHEST_PROTOCOL)
        # TODO: lower the cache time depending on the to_date parameter
        # if present use that date as maxdate (else now)
        # if maxdate is > now() - 2 months (configurable)
        # timeout variable (the closer to now, the lesser the value)
        timeout = app.config['CACHE_MIN_TIMEOUT']
        now = dtdatetime.now()
        if 'to_date' in kwargs and kwargs['to_date'] != None:
            datemax = parse(kwargs['to_date'])
        else:
            datemax = now
        delta = now - datemax
        if delta.days > 60:
            timeout = INFINITE # 1 year time caching
        elif delta.total_seconds() > app.config['CACHE_MIN_TIMEOUT']:
            timeout = int(delta.total_seconds())

        app.logger.debug('CACHER FOR FUNCTION: {0} TIMEOUT: {1}s KEY: {2}'.format(f.__name__, timeout, key))

        cached = cache.get(str(key))
        if cached is not None:
            if 'BYPASS_CACHING' in app.config and app.config['BYPASS_CACHING'] and app.debug:
                app.logger.debug('--Bypassing caching result---')
            else:
                app.logger.debug('--Cached result--')
                return cached

        app.logger.debug('--Real result (not cached)--')

        add_key_list(key, timeout, now)
        result = f(*args, **kwargs)
        cache.set(str(key), result, timeout=timeout)
        return result

    return decorated


def get_key_parts(key):
    """Decodes a cache key"""
    try:
        parts = pickle.loads(key)
        func = parts[0]
        args = ()
        kwargs = {}
        for k in parts:
            if isinstance(k, dict):
                kwargs = k
            elif not isinstance(k, str):
                args = k
        # print (func, kwargs, args)
        clas = None
        if args and hasattr(args[0], func):
            clas = args[0]
            args = args[1:]
            func = getattr(clas, func)
        return (clas, func, args, kwargs)
    except Exception as e:
        app.logger.debug("ERROR DECODING Key '{0}' Exception {1}".format(key, str(e)))

    return False

def get_key_functions(keys, force=False):
    """Returns a list with functions and parameters (ready to execute) associated with the keys in cache"""
    funcs = []
    for key,(timeout,time) in keys.items():
        delta = dtdatetime.now() - time
        # print (key, timeout, time.isoformat(), delta.total_seconds(), timeout / delta.total_seconds(), delta.total_seconds() / timeout)
        # if delta.total_seconds() / timeout < 0.75 and (timeout - delta.total_seconds()) > 60:
        if not force and (timeout - delta.total_seconds()) > 60:
            app.logger.debug("BYPASSING Key '{0}' with timeout {1} still have {2} seconds to expire".format(key, timeout, timeout - delta.total_seconds()))
            continue
        app.logger.debug("PROCESSING Key '{0}' with timeout {1}  about to expire in {2} seconds".format(key, timeout, timeout - delta.total_seconds()))

        key_parts = get_key_parts(key)
        if key_parts is False:
            app.logger.debug("INVALID KEY '{0}' BYPASSING...".format(key))
            continue

        (clas, func, args, kwargs) = key_parts

        if clas:
            funcs.append((key, clas, func, args, kwargs))
        else:

            if func in locals():
                funcs.append((locals()[func], args, dict(kwargs)))
            elif func in globals():
                funcs.append((globals()[func], args, dict(kwargs)))
            else:
                funcs.append((key, None, func, args, dict(kwargs)))

        # # Retrieving content from class
        # if clas:
        #     parts = clas.split('.')
        #     mod = importlib.import_module('.'.join(parts[:-1]))

        #     if inspect.ismodule(mod):
        #         mod = getattr(mod, parts[-1])
        #         instance = getattr(mod, func)
        #         funcs.append((instance, args, dict(kwargs)))

    return funcs
