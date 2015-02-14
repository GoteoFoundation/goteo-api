# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from api.users.user import UserAPI

from api import app, api
from api.decorators import *

api_users = Blueprint('api_users', __name__)

# All resources for users
api.add_resource(UserAPI, '/users/<string:id>', endpoint='api_users.user')