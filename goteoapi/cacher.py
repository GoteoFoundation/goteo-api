# -*- coding: utf-8 -*-
from datetime import datetime as dtdatetime
from dateutil.parser import parse
import re, importlib, inspect
from functools import wraps
from flask.ext.cache import Cache

from .helpers import *

from . import app

cache = Cache(app)

#
# CACHER BY ARGS FILTERS
#
# ======================
def cacher(f):
    """Caches methods for model classes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not app.config['CACHING']:
            return f(*args, **kwargs)

        INFINITE = 365 * 24 * 3600
        key = f.__name__;
        if args:
            for arg in args:
                if inspect.isclass(arg):
                    if not hasattr(arg, '__class__'):
                        arg = "<class '{0}'>".format(arg)
                    # print "ARG:", arg
                key += "|{0}".format(arg)
        if kwargs:
            for k in kwargs:
                val = kwargs[k]
                if val:
                    key += "|{0}={1}".format(k, val)

        #TODO: lower the cache time depending on the to_date parameter
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

        if app.debug:
            app.logger.debug('CACHER FOR FUNCTION: {0} TIMEOUT: {1}s KEY: {2}'.format(f.__name__, timeout, key))

        cached = cache.get(key)
        if cached:
            if 'BYPASS_CACHING' in app.config and app.config['BYPASS_CACHING'] and app.debug:
                app.logger.debug('--Bypassing caching result---')
            else:
                if app.debug:
                    app.logger.debug('--Cached result--')
                return cached

        if app.debug:
            app.logger.debug('--Real result (not cached)--')

        # Save cache key to a listable set
        keys = cache.get('KEY-LIST')
        if not keys:
            keys = {}
        keys[key] = (timeout, now)
        cache.set('KEY-LIST', keys, timeout=INFINITE)
        result = f(*args, **kwargs)
        cache.set(key, result, timeout=timeout)

        return result

    return decorated


def get_key_parts(key):
    """Decodes a cache key"""
    # print key
    args = key.split('|')
    _func = args.pop(0)
    _clas = args[0]
    _clas = re.search("\<class '([a-zA-Z0-9\.\_]+)'\>", _clas)
    if _clas and _clas.group(1):
        _clas = _clas.group(1)
        args.pop(0)
    else:
        _clas = None

    _args = []
    _kargs = {}
    if args:
        for i in args:
            if '=' in i:
                (k, v) = i.split('=')
                _kargs[k] = v
            else:
                _args.append(i)
    print _clas, _func, _args, _kargs
    return (_clas, _func, _args, _kargs)

def get_key_functions(keys):
    """Returns a list with functions and parameters (ready to execute) associated with the keys in cache"""
    funcs = []
    for key,(timeout,time) in keys.iteritems():
        delta = dtdatetime.now() - time
        # print key, timeout, time.isoformat(), delta.total_seconds(), timeout / delta.total_seconds(), delta.total_seconds() / timeout
        # if delta.total_seconds() / timeout < 0.75 and (timeout - delta.total_seconds()) > 60:
        if (timeout - delta.total_seconds()) > 60:
            if app.debug:
                app.logger.debug("BYPASSING Key '{0}' with timeout {1} still have {2} seconds to expire".format(key, timeout, timeout - delta.total_seconds()))
            continue
        if app.debug:
            app.logger.debug("PROCESSING Key '{0}' with timeout {1}  about to expire in {2} seconds".format(key, timeout, timeout - delta.total_seconds()))
        (clas, func, args, kargs) = get_key_parts(key)
        # Retrieving content from class
        if clas:
            parts = clas.split('.')
            mod = importlib.import_module('.'.join(parts[:-1]))

            if inspect.ismodule(mod):
                mod = getattr(mod, parts[-1])
                instance = getattr(mod, func)
                funcs.append((instance, args, dict(kargs)))
        else:

            if func in locals():
                funcs.append((locals()[func], args, dict(kargs)))
            elif func in globals():
                funcs.append((globals()[func], args, dict(kargs)))
            else:
                funcs.append((func, args, dict(kargs)))

    return funcs
