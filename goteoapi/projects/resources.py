# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields

from ..decorators import *
from ..helpers import marshal, image_url, utc_from_local, user_url, get_lang

from ..base_resources import BaseItem, BaseList, Response
from .models import Project, ProjectImage
from ..users.models import User
from ..users.resources import user_resource_fields
from ..location.models import ProjectLocation, UserLocation
from ..models.reward import Reward
from ..models.cost import Cost
from ..models.support import Support

project_resource_fields = {
    "id"                : fields.String,
    "name"              : fields.String,
    "description_short"              : fields.String,
    "node"              : fields.String,
    "date_created"      : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
    "date_published"    : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
    "project_url"       : fields.String,
    "image_url" : fields.String,
    "latitude" : fields.Float,
    "longitude" : fields.Float,
    "owner" : fields.String,
    "status" : fields.String,
}

project_gallery_resource_fields = {
    "image_url" : fields.String,
    "resource_url" : fields.String,
}

project_reward_resource_fields = {
    "reward" : fields.String,
    "description"              : fields.String,
    "license"              : fields.String,
    "type"              : fields.String,
    "icon"              : fields.String,
}

project_cost_resource_fields = {
    "cost" : fields.String,
    "description"              : fields.String,
    "type"              : fields.String,
    "amount"              : fields.Float,
    "required"              : fields.String,
    "date_from"              : fields.DateTime(dt_format='rfc822'),
    "date_to"              : fields.DateTime(dt_format='rfc822'),
}

project_need_resource_fields = {
    "support" : fields.String,
    "description"              : fields.String,
    "type"              : fields.String,
}

project_location_resource_fields = {
    "city"              : fields.String,
    "region"              : fields.String,
    "country"              : fields.String,
    "country_code"              : fields.String,
    "latitude" : fields.Float,
    "longitude" : fields.Float,
}

project_full_resource_fields = {
    "id"                : fields.String,
    "name"              : fields.String,
    "description_short" : fields.String,
    "description" : fields.String,
    "motivation" : fields.String,
    "goal" : fields.String,
    "about" : fields.String,
    "lang" : fields.String,
    "currency" : fields.String,
    "currency_rate" : fields.Float,
    "minimum" : fields.Float,
    "optimum" : fields.Float,
    "amount" : fields.Float,
    "status" : fields.String,
    "node"              : fields.String,
    "date_created"      : fields.DateTime(dt_format='rfc822'),
    "date_published"    : fields.DateTime(dt_format='rfc822'),
    "date_updated"    : fields.DateTime(dt_format='rfc822'),
    "date_succeeded"    : fields.DateTime(dt_format='rfc822'),
    "date_closed"    : fields.DateTime(dt_format='rfc822'),
    "date_passed"    : fields.DateTime(dt_format='rfc822'),
    "location" : fields.List(fields.Nested(project_location_resource_fields)),
    "owner" : fields.String,
    "project_url"       : fields.String,
    "widget_url"       : fields.String,
    "image_url" : fields.String,
    "image_url_big" : fields.String,
    "image_gallery" : fields.List(fields.Nested(project_gallery_resource_fields)),
    "video_url" : fields.String,
    "rewards" : fields.List(fields.Nested(project_reward_resource_fields)),
    "costs" : fields.List(fields.Nested(project_cost_resource_fields)),
    "needs" : fields.List(fields.Nested(project_need_resource_fields))
}

donor_resource_fields = user_resource_fields.copy()
donor_resource_fields['anonymous'] = fields.Boolean

class ProjectsListAPI(BaseList):
    """Project list"""

    @requires_auth
    @ratelimit()
    def get(self):
        """
        Project API
        <a href="http://developers.goteo.org/doc/projects">developers.goteo.org/doc/projects</a>
        This resource returns project information.
        ---
        tags:
            - projects
        definitions:
            - schema:
                id: Project
                properties:
                    id:
                        type: string
                        description: Project unique identifier
                    name:
                        type: string
                        description: Name of the project
                    node:
                        type: string
                        description: Node where the project was created originally
                    description-short:
                        type: string
                        description: Short description of the project
                    project-url:
                        type: string
                        description: URL where for the project
                    image-url:
                        type: string
                        description:  URL with the main image of the project
                    date-created:
                        type: string
                        description: Date when the project was created RFC822 format
                    date-published:
                        type: string
                        description: Date when the project was published RFC822 format
                    latitude:
                        type: number
                        description: Latitude coordinate for the project
                    longitude:
                        type: number
                        description: Longitude coordinate for the project
                    owner:
                        type: string
                        description: Projects owner's user ID
                    status:
                        type: string
                        description: Status of the project
        parameters:
            - in: query
              type: string
              name: node
              description: Filter by individual node(s). Multiple nodes can be specified. Restricts the list to the projects originally created in that node(s)
              collectionFormat: multi
            - in: query
              name: project
              description: Filter by individual project(s). Multiple projects can be specified
              type: string
              collectionFormat: multi
            - in: query
              name: from_date
              description: Filter from date. Ex. "2013-01-01". Restricts the list to the projects created in that range
              type: string
              format: date
            - in: query
              name: to_date
              description: Filter until date.. Ex. "2014-01-01". Restricts the list to the projects created in that range
              type: string
              format: date
            - in: query
              name: category
              description: Filter by project category. Multiple projects can be specified. Restricts the list to the projects that have interests in that category(ies)
              type: integer
            - in: query
              name: location
              description: Filter by project location (Latitude,longitude,Radius in Km). Restricts the list to the projects used in projects geolocated in that area
              type: number
              collectionFormat: csv
            - in: query
              name: page
              description: Page number (starting at 1) if the result can be paginated
              type: integer
            - in: query
              name: limit
              description: Page limit (maximum 50 results, defaults to 10) if the result can be paginated
              type: integer
        responses:
            200:
                description: List of available projects
                schema:
                    type: array
                    id: projects
                    items:
                        $ref: '#/definitions/api_projects_projects_list_get_Project'
            400:
                description: Invalid parameters format
        """
        res = self._get()

        return res.response()

    def _get(self):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args()

        items = []
        for p in Project.list(**args):
            item = marshal(p, project_resource_fields)
            item['project-url'] = project_url(p.id)
            item['description-short'] = p.subtitle
            item['status'] = p.status_string
            item['image-url'] = image_url(p.image, 'medium', False)
            location = ProjectLocation.get(p.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
            items.append( item )

        res = Response(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = Project.total(**args)
        )

        return res



class ProjectAPI(BaseItem):
    """Project Details"""

    @requires_auth
    @ratelimit()
    def get(self, project_id):
        """
        Project API
        <a href="http://developers.goteo.org/projects#project">developers.goteo.org/projects#project</a>
        This resource returns project detailed information.
        ---
        tags:
            - projects
        definitions:
            - schema:
                id: ProjectFull
                properties:
                    id:
                        type: string
                        description: Project unique identifier
                    name:
                        type: string
                        description: Name of the project
                    node:
                        type: string
                        description: Node where the project was created originally
                    description-short:
                        type: string
                        description: Short description of the project
                    description:
                        type: string
                        description: Full description of the project
                    motivation:
                        type: string
                        description: Motivation text writen by the owner of the project
                    goal:
                        type: string
                        description: Goal of the project
                    about:
                        type: string
                        description: About the project or his creators
                    lang:
                        type: string
                        description: Main language of the project
                    currency:
                        type: string
                        description: Currency used in the project (ISO4217 Format)
                    currency-rate:
                        type: number
                        description: Currency rate when the project was created (if was not EUR)
                    minimum:
                        type: number
                        description: Minimum amount to achieve to consider the project succeeded
                    optimum:
                        type: number
                        description: Optimum amount to achieve for the project to achieve all his goals
                    amount:
                        type: number
                        description: Currently achieved amount for the project
                    project-url:
                        type: string
                        description: URL where for the project
                    widget-url:
                        type: string
                        description:  URL with the main widget (embed code) of the project
                    image-url:
                        type: string
                        description:  URL with the main image of the project
                    image-url-big:
                        type: string
                        description:  URL with the main image (big size) of the project
                    video-url:
                        type: string
                        description:  URL with the main video of the project
                    date-created:
                        type: string
                        description: Date when the project was created RFC822 format
                    date-published:
                        type: string
                        description: Date when the project was published RFC822 format
                    date-succeeded:
                        type: string
                        description: Date when the project was succeeded RFC822 format
                    date-closed:
                        type: string
                        description: Date when the project was closed (if was a failed project) RFC822 format
                    date-passed:
                        type: string
                        description: Date when the project passed the first round (reached the minimum) RFC822 format
                    date-updated:
                        type: string
                        description: Date when the project was updated RFC822 format
                    latitude:
                        type: number
                        description: Latitude coordinate for the project
                    longitude:
                        type: number
                        description: Longitude coordinate for the project
                    owner:
                        type: string
                        description: Projects owner's user ID
                    status:
                        type: string
                        description: Status of the project
                    location:
                        type: array
                        description: Location of the project
                        items:
                            $ref: '#/definitions/api_projects_project_get_ProjectLocation'
                    image-gallery:
                        type: array
                        description: List of images for the project
                        items:
                            $ref: '#/definitions/api_projects_project_get_ProjectGallery'
                    rewards:
                        type: array
                        description: List of rewards for the project
                        items:
                            $ref: '#/definitions/api_projects_project_get_ProjectReward'
                    costs:
                        type: array
                        description: Economical detailed list of necessities
                        items:
                            $ref: '#/definitions/api_projects_project_get_ProjectCost'
                    needs:
                        type: array
                        description: Non-economical detailed list of necessities
                        items:
                            $ref: '#/definitions/api_projects_project_get_ProjectNeed'
            - schema:
                id: ProjectLocation
                properties:
                    city:
                        type: string
                    region:
                        type: string
                    country:
                        type: string
                    country-code:
                        type: string
                    latitude:
                        type: number
                    longitude:
                        type: number
            - schema:
                id: ProjectGallery
                properties:
                    image-url:
                        type: string
                    resource-url:
                        type: string
            - schema:
                id: ProjectReward
                properties:
                    reward:
                        type: string
                    description:
                        type: string
                    license:
                        type: string
                    type:
                        type: string
                    icon:
                        type: string
            - schema:
                id: ProjectCost
                properties:
                    cost:
                        type: string
                    description:
                        type: string
                    type:
                        type: string
                    amount:
                        type: float
                    required:
                        type: string
                    date-from:
                        type: string
                    date-to:
                        type: string
            - schema:
                id: ProjectNeed
                properties:
                    support:
                        type: string
                    description:
                        type: string
                    type:
                        type: string
        parameters:
            - in: path
              type: string
              name: project_id
              description: Unique ID for the project
              required: true
        responses:
            200:
                description: Project data
                schema:
                    $ref: '#/definitions/api_projects_project_get_ProjectFull'
            404:
                description: Resource not found
        """
        res = self._get(project_id)

        if res.ret['id'] == None:
            return bad_request('Project not found', 404)

        return res.response()

    def _get(self, project_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        p = Project.get(project_id)

        item = marshal(p, project_full_resource_fields)
        if p != None:
            item['description-short'] = p.subtitle
            item['video-url'] = p.media
            item['image-url'] = image_url(p.image, 'medium', False)
            item['image-url-big'] = image_url(p.image, 'big', False)
            item['project-url'] = project_url(p.id)
            item['widget-url'] = project_widget_url(p.id)
            item['status'] = p.status_string
            location = ProjectLocation.get(p.id)
            if location:
                item['location'] = [marshal(location, project_location_resource_fields)]
            gallery = ProjectImage.get(p.id)
            if gallery:
                item['image-gallery'] = []
                for i in gallery:
                    item['image-gallery'].append({
                        'image-url' : image_url(i.image, 'big', False),
                        'resource-url' : image_resource_url(i.url)
                        })
                #     i['image-url'] = gallery.image
            rewards = Reward.list_by_project(p.id)
            if rewards:
                item['rewards'] = marshal(rewards, project_reward_resource_fields)
            costs = Cost.list_by_project(p.id)
            if costs:
                item['costs'] = marshal(costs, project_cost_resource_fields)
            needs = Support.list_by_project(p.id)
            if needs:
                item['needs'] = marshal(needs, project_need_resource_fields)


        res = Response(
            starttime = time_start,
            attributes = item
        )

        return res


class ProjectDonorsListAPI(BaseList):
    """Donors list"""

    @requires_auth
    @ratelimit()
    def get(self, project_id):
        """
        Project API
        This resource returns user donors information.
        <a href="http://developers.goteo.org/projects#donors">developers.goteo.org/projects#donors</a>
        ---
        tags:
            - projects
        parameters:
            - in: path
              type: string
              name: project_id
              description: Unique ID for the project
              required: true
            - in: query
              type: string
              name: node
              description: Filter by individual node(s). Multiple nodes can be specified. Restricts the list to the users originally created in that node(s)
              collectionFormat: multi
            - in: query
              name: from_date
              description: Filter from date. Ex. "2013-01-01". Restricts the list to the users created in that range
              type: string
              format: date
            - in: query
              name: to_date
              description: Filter until date.. Ex. "2014-01-01". Restricts the list to the users created in that range
              type: string
              format: date
            - in: query
              name: category
              description: Filter by project category. Multiple users can be specified. Restricts the list to the users that have interests in that category(ies)
              type: integer
            - in: query
              name: page
              description: Page number (starting at 1) if the result can be paginated
              type: integer
            - in: query
              name: limit
              description: Page limit (maximum 50 results, defaults to 10) if the result can be paginated
              type: integer
        responses:
            200:
                description: User data
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/api_users_users_list_get_User'
            404:
                description: Resource not found
        """
        res = self._get(project_id)

        return res.response()

    def _get(self, project_id):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args(remove=('location'))

        items = []
        for u in User.donors_by_project(project_id, **args):
            item = marshal(u, donor_resource_fields)
            item['profile-image-url'] = image_url(u['avatar'])
            item['profile-url'] = user_url(u['id'])
            if u['anonymous']:
                item['id'] = None
                item['name'] = 'Anonymous'
                item['profile-image-url'] = None
                item['profile-url'] = None
            else:
                location = UserLocation.get(u['id'])
                if location:
                    item['latitude'] = location.latitude
                    item['longitude'] = location.longitude

            items.append( item )
        res = Response(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = User.donors_by_project_total(project_id, **args)
        )

        return res
