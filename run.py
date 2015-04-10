#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goteoapi import app

# import sub-modules controllers
# Minimal endpoints:
__import__('goteoapi.controllers')

#This part will not be executed under uWSGI module (nginx)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
