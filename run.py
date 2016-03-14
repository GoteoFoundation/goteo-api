#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goteoapi import app
import config

# import sub-modules controllers
# Minimal endpoints:
__import__('goteoapi.controllers')

# Additional modules from config
if hasattr(config, 'MODULES'):
    for i in config.MODULES:
        __import__(i)

#This part will not be executed under uWSGI module (nginx)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
