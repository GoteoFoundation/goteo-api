# -*- coding: utf-8 -*-
import time
from api import app
from flask import jsonify

def image_url(img, size='large'):
    """
    @size 'thumb', 'medium', 'large'
    """
    sizes = {'thumb' : '56x56c', 'medium' : '192x192c', 'large' : '512x512c'}

    s = sizes[size] if size in sizes else sizes['thumb']

    i = img if img is not None else 'la_gota.png'

    return 'http://goteo.org/img/' + s + '/' + i

#Error handling
def bad_request(message, code = 400):
    "Error handling json response"
    resp = jsonify(message=str(message))
    resp.status_code = code
    return resp

# Generic percentage
def percent(number, base=None):
    "Porcentaje en base a un total"
    if base is None:
        return 0
    if base == 0:
        return 0
    perc = float(number) / base * 100
    return round(perc, 2)


############################ debug ############################
def debug_time(func):
    def new_f(*args, **kwargs):
        time_start = time.time()
        res = func(*args, **kwargs)
        total_time = time.time() - time_start
        app.logger.debug('Time ' + func.__name__ + ': ' + str(total_time))
        return res
    return new_f
