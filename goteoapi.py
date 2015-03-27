#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful_swagger import swagger

from api import app

# import sub-modules controllers
import api.main.controllers
import api.users.controllers
import api.categories.controllers
import api.licenses.controllers
import api.digests.controllers
# reports
import api.reports.controllers


#This part will not be executed under uWSGI module (nginx)
if __name__ == '__main__':
    app.debug = True

    if app.debug:
        import os
        module_path = os.path.dirname(swagger.__file__)
        module_path = os.path.join(module_path, 'static')
        extra_dirs = [module_path, ]
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in os.walk(extra_dir):
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    if os.path.isfile(filename):
                        extra_files.append(filename)
    else:
        extra_files = []

    app.run(host='0.0.0.0', extra_files=extra_files)
