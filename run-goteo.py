#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Running extra packages for the api.goteo.org
#

from goteoapi import app

# import sub-modules controllers
# Minimal endpoints:
__import__('goteoapi.controllers')

# Additional packages
# reports endpoints
__import__('goteoapi_reports.controllers')

# digests endpoints
# __import__('goteoapi_digests.controllers')


#This part will not be executed under uWSGI module (nginx)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
