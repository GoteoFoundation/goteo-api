# -*- coding: utf-8 -*-

from flask.ext.restful import Resource, reqparse, fields, marshal
from model import Project

from flask.ext.restful import Resource


project_fields = {
    'id': fields.String,
    'name': fields.String,
    'category': fields.String,
    'minimum': fields.Integer,
    'optimum': fields.Integer
}

class ProjectListAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('low_minimum', type=str, default="", location='json')
        self.reqparse.add_argument('high_minimum', type=str, default="", location='json')
        super(ProjectListAPI, self).__init__()

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
        return {'projects': map(lambda t: {t.id: marshal(t, project_fields)}, projects)}


class ProjectAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        super(ProjectAPI, self).__init__()

    def get(self, project_id):
        p = Project.query.filter_by(id=project_id).first()
        if p is None:
            abort(404)

        return {'project': marshal(p, project_fields)}
