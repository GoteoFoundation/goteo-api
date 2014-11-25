#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model import app, db

from api.reports.money import MoneyAPI
from api.reports.rewards import RewardsAPI
from api.reports.community import CommunityAPI
from api.reports.projects import ProjectsAPI
#from api.misc import ProjectListAPI, ProjectAPI

from flask_restful_swagger import swagger
from flask.ext.restful import Api
api = swagger.docs(Api(app), apiVersion='1.0')
#api = Api(app)

@app.route('/')
def index():
    return """
API de Goteo.org.<br><br>
<a href="/reports/">/reports/</a></br>
<br>
Swagger UI: <a href="http://0.0.0.0:5000/api/spec.html">http://0.0.0.0:5000/api/spec.html</a> (<a href="http://0.0.0.0:5000/api/spec.json">json</a>)
"""

@app.route('/reports/')
def reports():
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
curl -i -X GET -d project=hacks-cotidianos-en-pequeno-formato http://0.0.0.0:5000/reports/money<br>
curl -i -X GET -d project=asd -d project=hacks-cotidianos-en-pequeno-formato http://0.0.0.0:5000/reports/money<br>
curl -i -X GET -H "Content-Type: application/jon" -d '{"project":["socialgraph"]}' http://0.0.0.0:5000/reports/money<br>
curl -i -X GET -H "Content-Type: application/jon" -d '{"project":["socialgraph","hacks-cotidianos-en-pequeno-formato"]}' http://0.0.0.0:5000/reports/money<br>

<br><br>
<a href="http://0.0.0.0:5000/reports/money?limit=2">curl -i -X GET -d limit=2 http://0.0.0.0:5000/reports/money</a><br>
<a href="http://0.0.0.0:5000/reports/money?from_date=2014-01-01">curl -i -X GET -d from_date="2014-01-01" http://0.0.0.0:5000/reports/money</a><br>
<a href="http://0.0.0.0:5000/reports/money?project=057ce063ee014dee885b13840774463c">curl -i -X GET -d project="057ce063ee014dee885b13840774463c" http://0.0.0.0:5000/reports/money</a><br>
<a href="http://0.0.0.0:5000/reports/money?project=2a-edicio-in-situ&project=10-anys-de-l-antic-teatre">curl -i -X GET -d project=2a-edicio-in-situ -d project=10-anys-de-l-antic-teatre" http://0.0.0.0:5000/reports/money</a><br>
<br>
Swagger UI: <a href="http://0.0.0.0:5000/api/spec.html">http://0.0.0.0:5000/api/spec.html</a> (<a href="http://0.0.0.0:5000/api/spec.json">json</a>)
"""

#api.add_resource(ProjectListAPI, '/projects/', endpoint='projects1')
#api.add_resource(ProjectAPI, '/projects/<string:project_id>', endpoint='project')
api.add_resource(MoneyAPI, '/reports/money', endpoint='money')
api.add_resource(ProjectsAPI, '/reports/projects', endpoint='projects')
api.add_resource(CommunityAPI, '/reports/community', endpoint='community')
api.add_resource(RewardsAPI, '/reports/rewards', endpoint='rewards')


#This part will not be executed under uWSGI module (nginx)
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
