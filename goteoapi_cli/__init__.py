# -*- coding: utf-8 -*-
"""
    goteoapi_cli
    ~~~~~~~~
    goteoapi console extension application package

    Adds some command line tools such as:

    clearcache
    renewcache
    crontab install/remove
"""
import os
from flask.ext.script import Manager
from termcolor import colored, cprint
from crontab import CronTab
from goteoapi import app
from goteoapi.cacher import cache, get_key_list, renew_key_list, get_key_functions
from flask.ext.script import Command

manager = Manager(app)

@manager.command
def clearcache():
    """Clears all cache keys"""
    cprint('Clearing cache', 'green')
    cache.clear()
    cprint('Done', 'green')


@manager.command
def renewcache(execute=False, force=False):
    """Renew cached keys by executing the functions with stored params"""
    app.config['BYPASS_CACHING'] = True
    key_list = get_key_functions(get_key_list(), force)
    if key_list:
        for key, clas, f, args, kargs in key_list:
            print '{0} {1} {2} {3} {4} {5}'.format(colored('FUNCTION', 'green'), f.__name__, colored('WITH ARGS', 'green'), args, colored('KARGS', 'green'), kargs)
            if execute:
                cprint("EXECUTING {0}".format(f),'yellow')
                try:
                    renew_key_list(key)
                    f(*args, **kargs)
                except Exception as e:
                    cprint("EXCEPTION {0} EXECUTING {1}".format(str(e), f),'red')
        if not execute:
            cprint("Run with option --execute (-e) to actually renew the cache", 'red')
    else:
        cprint("No keys to be renewed", 'red')
    if not force:
        cprint("Run with option --force (-f) to force renew of non expired keys", 'yellow')

@manager.command
def crontab(install=False, remove=False):
    """Installs/Removes a crontab if is installed"""
    if install:
        cprint('Installing crontab', 'yellow')
    elif remove:
        cprint('Installing crontab', 'yellow')
    else:
        cprint('Please specifiy --install (-i) or --remove (-r) argument', 'red')

    command = os.getcwd() + '/console'
    cron  = CronTab(user=True)

    if install or remove:
        # Removes current crontab
        _iter = cron.find_command(command)
        for job in _iter:
            cron.remove(job)
        # Install job
        if install:
            job  = cron.new(command+  ' renewcache --execute > ' + os.getcwd() + '/crontab.log 2>&1')
        cron.write()

    print "{0}\n{1}".format(colored('CURRENT CRONTAB:', 'green'), cron)

