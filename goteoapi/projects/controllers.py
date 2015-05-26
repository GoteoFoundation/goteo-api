# -*- coding: utf-8 -*-
#
# Project resources


from .. import api
from .resources import ProjectsListAPI, ProjectAPI, ProjectDonorsListAPI

api.add_resource(ProjectsListAPI, '/projects/', endpoint='api_projects.projects_list')
api.add_resource(ProjectAPI, '/projects/<string:project_id>/', endpoint='api_projects.project')
api.add_resource(ProjectDonorsListAPI, '/projects/<string:project_id>/donors', endpoint='api_projects_donors.project')
