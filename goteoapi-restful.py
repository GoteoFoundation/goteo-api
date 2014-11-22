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
API de Goteo.org. <a href="/projects/">/projects/</a></br>
</br>
curl -i http://0.0.0.0:5000/projects/057ce063ee014dee885b13840774463c</br>
</br>
curl -i http://0.0.0.0:5000/projects/</br>
curl -i -X GET -H "Content-Type: application/json" -d '{"low_minimum":10000}' http://0.0.0.0:5000/projects/</br>
curl -i -X GET -H "Content-Type: application/json" -d '{"high_minimum":20000}' http://0.0.0.0:5000/projects/</br>
curl -i -X GET -H "Content-Type: application/json" -d '{"low_minimum":10000,"high_minimum":20000}' http://0.0.0.0:5000/projects/</br>
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
