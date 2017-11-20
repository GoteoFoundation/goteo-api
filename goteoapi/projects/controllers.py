# -*- coding: utf-8 -*-
#
# Project resources


from .. import api, app
from flask import url_for, redirect
from .resources import ProjectsListAPI, ProjectAPI, ProjectDonorsListAPI

api.add_resource(ProjectsListAPI,
                 '/projects/',
                 endpoint='api_projects.projects')
api.add_resource(ProjectAPI,
                 '/projects/<string:project_id>',
                 endpoint='api_projects.project')
api.add_resource(ProjectDonorsListAPI,
                 '/projects/<string:project_id>/donors/',
                 endpoint='api_projects.project_donors')


# redirect end trailing slash
@app.route('/projects/<string:project_id>/', endpoint='redirect.project')
def project_redirect(project_id):
    return redirect(url_for('api_projects.project',
                    project_id=project_id), code=301)
