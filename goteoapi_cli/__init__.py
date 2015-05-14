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
from goteoapi.cacher import cache, get_key_functions
from flask.ext.script import Command

manager = Manager(app)

@manager.command
def clearcache():
    """Clears all cache keys"""
    cprint('Clearing cache', 'green')
    cache.clear()
    cprint('Done', 'green')


@manager.command
def renewcache():
    """Renew cached keys by executing the functions with stored params"""
    app.config['BYPASS_CACHING'] = True
    keys = cache.get('KEY-LIST')
    key_list = []
    if keys:
        key_list = get_key_functions(keys)
    if key_list:
        for f, args, kargs in key_list:
            print '{0} {1} {2} {3} {4} {5}'.format(colored('EXECUTING FUNCTION', 'green'), colored(f.__name__, 'yellow'), colored('WITH ARGS', 'green'), colored(args, 'yellow'), colored('KARGS', 'green'), colored(kargs, 'yellow'))
            f(*args, **kargs)
    else:
        cprint("No keys to be renewed", 'red')

@manager.command
def crontab(install=False, remove=False):
    """Installs/Removes a crontab if is installed"""
    if install:
        cprint('Installing crontab', 'yellow')
    elif remove:
        cprint('Installing crontab', 'yellow')
    else:
        cprint('Please specifiy --install (-i) or --remove (-r) argument', 'red')
        return
    command = os.getcwd() + '/manage.sh'
    cron  = CronTab(user=True)
    # Removes current crontab
    _iter = cron.find_command(command)
    for job in _iter:
        cron.remove(job)
    # Install job
    if install:
        job  = cron.new(command+  ' renewcache > ' + os.getcwd() + '/crontab.log 2>&1')

    cron.write()
    print "{0}\n{1}".format(colored('CURRENT CRONTAB:', 'green'), cron)

