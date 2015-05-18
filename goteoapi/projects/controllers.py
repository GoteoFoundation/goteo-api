# -*- coding: utf-8 -*-
#
# Project resources


from .. import api
from .resources import ProjectsListAPI, ProjectAPI

api.add_resource(ProjectsListAPI, '/projects/', endpoint='api_projects.projects_list')
api.add_resource(ProjectAPI, '/projects/<string:project_id>/', endpoint='api_projects.project')
