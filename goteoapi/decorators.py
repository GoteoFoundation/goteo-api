# -*- coding: utf-8 -*-
import time
from datetime import datetime as dtdatetime

from functools import wraps, update_wrapper
from flask import request, g, jsonify
from flask_redis import Redis
from netaddr import IPSet, AddrFormatError
from sqlalchemy.orm.exc import NoResultFound

from .helpers import *

from . import app, db

#
# REDIS RATE LIMITER
# ==================

redis = False
if app.config['REDIS_URL']:
    redis = Redis(app)

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
    resp = bad_request('Too many requests', 429)
    return resp

def ratelimit(limit=app.config['REQUESTS_LIMIT'], per=app.config['REQUESTS_TIME'], over_limit=on_over_limit):
    def decorator(f):
        def rate_limited(*args, **kwargs):
            if not app.config['REQUESTS_LIMIT'] or not redis:
                return f(*args, **kwargs)

            if app.config['AUTH_ENABLED'] and request.authorization:
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


############################ debug ############################
def debug_time(func):
    def new_f(*args, **kwargs):
        time_start = time.time()
        res = func(*args, **kwargs)
        total_time = time.time() - time_start
        app.logger.debug('Time ' + func.__name__ + ': ' + str(total_time))
        return res
    return new_f
