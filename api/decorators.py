# -*- coding: utf-8 -*-
import time
from datetime import datetime as dtdatetime
from dateutil.parser import parse

from functools import wraps, update_wrapper
from flask import request, g, jsonify
from flask_redis import Redis
from flask.ext.cache import Cache
from netaddr import IPSet, AddrFormatError
from sqlalchemy.orm.exc import NoResultFound

from config import config

from .helpers import *

from . import app, db

cache = Cache(app)

#
# CACHER BY ARGS FILTERS
#
# ======================
def cacher(f):
    """Caches methods for model classes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        key = f.__name__;
        # if args:
        #     key += '/' + json.dumps(args)
        # if kwargs:
        #     key += '/' + json.dumps(kwargs)
        if args:
            for arg in args:
                key += "|{0}".format(arg)
        if kwargs:
            for k in kwargs:
                key += "|{0}={1}".format(k, kwargs[k])

        #TODO: lower the cache time depending on the to_date parameter
                # if present use that date as maxdate (else now)
                # if maxdate is > now() - 2 months (configurable)
                    # timeout variable (the closer to now, the lesser the value)
        timeout = config.cache_min_timeout
        now = dtdatetime.now()
        if 'to_date' in kwargs and kwargs['to_date'] != None:
            datemax = parse(kwargs['to_date'])
        else:
            datemax = now
        delta = now - datemax
        if delta.days > 60:
            timeout = None # infinite time caching
        elif delta.total_seconds() > config.cache_min_timeout:
            timeout = int(delta.total_seconds())

        if app.debug:
            app.logger.debug('CACHER FOR FUNCTION: {0} TIMEOUT: {1}s KEY: {2}'.format(f.__name__, timeout, key))

        cached = cache.get(key)
        if cached:
            if app.debug:
                app.logger.debug('--Caching--')
            return cached

        if app.debug:
            app.logger.debug('--Not caching--')

        result = f(*args, **kwargs)
        cache.set(key, result, timeout=timeout)

        return result

    return decorated

#
# REDIS RATE LIMITER
# ==================

if app.config['REDIS_URL'] is not False:
    redis = Redis(app)
else:
    redis = False

class RateLimit(object):
    expiration_window = 10

    def __init__(self, key_prefix, limit, per):
        self.reset = (int(time.time()) // per) * per + per
        self.key = key_prefix + str(self.reset)
        self.limit = limit
        self.per = per
        p = redis.pipeline()
        p.incr(self.key)
        p.expireat(self.key, self.reset + self.expiration_window)
        self.current = min(p.execute()[0], limit)

    remaining = property(lambda x: x.limit - x.current)
    over_limit = property(lambda x: x.current >= x.limit)

def get_view_rate_limit():
    return getattr(g, '_view_rate_limit', None)

def on_over_limit(limit):
    resp = bad_request('Too many requests', 400)
    return resp

def ratelimit(limit=config.requests_limit, per=config.requests_time, over_limit=on_over_limit):
    def decorator(f):
        def rate_limited(*args, **kwargs):
            if not config.requests_limit:
                return f(*args, **kwargs)

            if config.auth_enabled:
                key = 'rate-limit/%s/' % request.authorization.username
            else:
                remote_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                key = 'rate-limit/%s' % remote_ip

            rlimit = RateLimit(key, limit, per)
            g._view_rate_limit = rlimit
            if over_limit is not None and rlimit.over_limit:
                return over_limit(rlimit)
            return f(*args, **kwargs)
        return update_wrapper(rate_limited, f)
    return decorator

@app.after_request
def inject_x_rate_headers(response):
    limit = get_view_rate_limit()
    if limit:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response



#
# BASIC AUTH DECORATOR
# ====================
# Based on http://flask.pocoo.org/snippets/8/

def check_auth(username, password):
    """Checks username & password authentication"""

    #try some built-in auth first
    if config.users and username in config.users and 'password' in config.users[username]:
        user = config.users[username]
        if user['password'] == password:
            if 'remotes' in user:
                try:
                    remote_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    if remote_ip in IPSet(user['remotes']):
                        return True
                except AddrFormatError:
                    "continue"

            else:
                return True

    #Try the key-password values in sql
    try:
        from .models.user import UserApi
        user = db.session.query(UserApi).filter(UserApi.user == username, UserApi.key == password).one()
        if user.expiration_date is not None and user.expiration_date <= dtdatetime.today():
            # print user.expiration_date, '<=', dtdatetime.today()
            return 'API Key expired. Please get new valid key! '
        return True
    except NoResultFound:
        return 'Acces denied: Invalid username or password!'

    return False


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not config.auth_enabled:
            return f(*args, **kwargs)

        auth = request.authorization
        msg = 'You need a key in order to use our API. Get one on www.goteo.org!'
        if auth:
            ok = check_auth(auth.username, auth.password)
            if(ok is True):
                return f(*args, **kwargs)
            elif(ok is not False):
                msg = str(ok)

        resp = jsonify(error=401, message=msg)
        resp.status_code = 401
        resp.headers.add('WWW-Authenticate', 'Basic realm="Goteo.org API"')
        return resp

    return decorated


############################ debug ############################
def debug_time(func):
    def new_f(*args, **kwargs):
        time_start = time.time()
        res = func(*args, **kwargs)
        total_time = time.time() - time_start
        app.logger.debug('Time ' + func.__name__ + ': ' + str(total_time))
        return res
    return new_f
