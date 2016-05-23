# -*- coding: utf-8 -*-
#
# Invest resources


from .. import api, app
from flask import url_for, redirect
from .resources import InvestsListAPI, InvestAPI

api.add_resource(InvestsListAPI, '/invests/', endpoint='api_invests.invests')
api.add_resource(InvestAPI, '/invests/<int:invest_id>', endpoint='api_invests.invest')

# redirect end trailing slash
@app.route('/invests/<int:invest_id>/', endpoint='redirect.invest')
def invest_redirect(invest_id):
    return redirect(url_for('api_invests.invest', invest_id=invest_id), code=301)
