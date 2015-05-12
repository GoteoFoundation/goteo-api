#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Cron
import re, importlib, inspect
from goteoapi.decorators import cache

def get_parts(key):
    # print key
    args = key.split('|')
    _func = args.pop(0)
    _clas = args.pop(0)
    _clas = re.search("\<class '([a-zA-Z0-9\.\_]+)'\>", _clas)
    kargs = {}
    if args:
        for i in args:
            (k, v) = i.split('=')
            kargs[k] = eval(v)
    # print kargs
    if _clas and _clas.group(1):
        _clas = _clas.group(1)
    else:
        _clas = None
    return (_func, _clas, kargs)

def check_keys(keys):
    if keys:
        for key in keys:
            (func, clas, args) = get_parts(key)
            # Retrieving content from class
            print clas,func,args
            parts = clas.split('.')

            mod = importlib.import_module('.'.join(parts[:-1]))
            if inspect.ismodule(mod):
                mod = getattr(mod, parts[-1])
                instance = getattr(mod, func)
                print instance(**dict(args))


# check_keys(["total|<class 'goteoapi_reports.community.List'>|node=None"])
# check_keys(["total|<class 'goteoapi.users.models.User'>|node=None"])
check_keys(cache.get('KEY-LIST'))
