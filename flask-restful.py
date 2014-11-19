#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model import app, db

from api.reports.money import MoneyAPI
from api.reports.rewards import RewardsAPI
from api.reports.community import CommunityAPI
from api.reports.projects import ProjectsAPI
#from api.misc import ProjectListAPI, ProjectAPI

from flask.ext.restful import Api
api = Api(app)


@app.route('/')
def hello_world():
    return """
API de Goteo.org.<br><br>
<a href="/reports/money">/reports/money</a></br>
<a href="/reports/projects">/reports/projects</a></br>
<a href="/reports/community">/reports/community</a></br>
<a href="/reports/rewards">/reports/rewards</a></br>
</br>
curl -i http://0.0.0.0:5000/reports/money</br>
<br>
curl -i -X GET -H "Content-Type: application/json" -d '{"from_date_invested":"2014-01-01"}' http://0.0.0.0:5000/reports/money<br>
"""

#api.add_resource(ProjectListAPI, '/projects/', endpoint='projects1')
#api.add_resource(ProjectAPI, '/projects/<string:project_id>', endpoint='project')
api.add_resource(MoneyAPI, '/reports/money', endpoint='money')
api.add_resource(ProjectsAPI, '/reports/projects', endpoint='projects')
api.add_resource(CommunityAPI, '/reports/community', endpoint='community')
api.add_resource(RewardsAPI, '/reports/rewards', endpoint='rewards')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
