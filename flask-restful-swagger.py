from flask import abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask_restful_swagger import swagger

from model import app, Project

# http://0.0.0.0:5000/api/spec.html
# http://0.0.0.0:5000/api/spec.json

###################################
# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds some swagger smarts
api = swagger.docs(Api(app), apiVersion='1.0')
###################################


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


project_fields = {
    'projectid': fields.String,
    'name': fields.String,
    'category': fields.String,
    'minimum': fields.Integer,
    'optimum': fields.Integer
}


class ModelClass():
    pass


class ModelClass2():
    pass


@swagger.model
class ProjectListAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('low_minimum', type=str, default="", location='json')
        self.reqparse.add_argument('high_minimum', type=str, default="", location='json')
        super(ProjectListAPI, self).__init__()

    @swagger.operation(
    notes='Projects list',
    responseClass=ModelClass.__name__,
    nickname='upload',
    responseMessages=[
        {
          "code": 201,
          "message": "Created. The URL of the created blueprint should be in the Location header"
        },
        {
          "code": 405,
          "message": "Invalid input"
        }
      ]
    )
    def get(self):
        args = self.reqparse.parse_args()
        filters = {}
        for k, v in args.iteritems():
            if v is not None and k in ['low_minimum', 'high_minimum']:
                filters[k] = v

        projects = Project.query  # .all()
        if filters['low_minimum']:
            app.logger.debug('low')
            projects = projects.filter(Project.minimum >= filters['low_minimum'])

        if filters['high_minimum']:
            app.logger.debug('high')
            projects = projects.filter(Project.minimum <= filters['high_minimum'])

        #return {'projects': map(lambda t: marshal(t, project_fields), projects)}
        return {'projects': map(lambda t: {t.projectid: marshal(t, project_fields)}, projects)}


    # Operations not decorated with @swagger.operation do not get added to the swagger docs


@swagger.model
class ProjectAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        super(ProjectAPI, self).__init__()

    @swagger.operation(
    notes='Project details',
    responseClass=ModelClass.__name__,
    nickname='upload',
    parameters=[
        {
          "name": "project_id",
          "description": "blueprint object that needs to be added. YAML.",
          "required": True,
          "allowMultiple": False,
          "dataType": ModelClass2.__name__,
          "paramType": "string"
        }
      ],
    responseMessages=[
        {
          "code": 201,
          "message": "Created. The URL of the created blueprint should be in the Location header"
        },
        {
          "code": 405,
          "message": "Invalid input"
        }
      ]
    )
    def get(self, project_id):
        p = Project.query.filter_by(projectid=project_id).first()
        if p is None:
            abort(404)

        return {'project': marshal(p, project_fields)}


api.add_resource(ProjectListAPI, '/projects/', endpoint='projects')
api.add_resource(ProjectAPI, '/projects/<string:project_id>', endpoint='project')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
