# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields, marshal

from ..decorators import *
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
    "description-short"              : fields.String,
    "node"              : fields.String,
    "date-created"      : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
    "date-published"    : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
    "project-url"       : fields.String,
    "image-url" : fields.String,
    "latitude" : fields.Float,
    "longitude" : fields.Float,
    "owner" : fields.String,
    "status" : fields.String,
}

project_gallery_resource_fields = {
    "image-url" : fields.String,
    "resource-url"              : fields.String,
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
    "from-date"              : fields.DateTime(dt_format='rfc822'),
    "to-date"              : fields.DateTime(dt_format='rfc822'),
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
    "country-code"              : fields.String,
    "latitude" : fields.Float,
    "longitude" : fields.Float,
}

project_full_resource_fields = {
    "id"                : fields.String,
    "name"              : fields.String,
    "description-short" : fields.String,
    "description" : fields.String,
    "motivation" : fields.String,
    "goal" : fields.String,
    "about" : fields.String,
    "lang" : fields.String,
    "currency" : fields.String,
    "currency-rate" : fields.Float,
    "minimum" : fields.Float,
    "optimum" : fields.Float,
    "amount" : fields.Float,
    "status" : fields.String,
    "node"              : fields.String,
    "date-created"      : fields.DateTime(dt_format='rfc822'),
    "date-published"    : fields.DateTime(dt_format='rfc822'),
    "date-updated"    : fields.DateTime(dt_format='rfc822'),
    "date-succeeded"    : fields.DateTime(dt_format='rfc822'),
    "date-closed"    : fields.DateTime(dt_format='rfc822'),
    "date-passed"    : fields.DateTime(dt_format='rfc822'),
    "location" : fields.List(fields.Nested(project_location_resource_fields)),
    "owner" : fields.String,
    "project-url"       : fields.String,
    "widget-url"       : fields.String,
    "image-url" : fields.String,
    "image-url-big" : fields.String,
    "image-gallery" : fields.List(fields.Nested(project_gallery_resource_fields)),
    "video-url" : fields.String,
    "rewards" : fields.List(fields.Nested(project_reward_resource_fields)),
    "costs" : fields.List(fields.Nested(project_cost_resource_fields)),
    "needs" : fields.List(fields.Nested(project_need_resource_fields)),
}

class ProjectsListAPI(BaseList):
    """Get Project list"""

    @requires_auth
    @ratelimit()
    def get(self):
        """Get the projects list
        <a href="http://developers.goteo.org/doc/projects">developers.goteo.org/doc/projects</a>
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
            item['date-created'] =p.date_created
            item['date-published'] = p.date_published
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
    """Get Project Details"""

    @requires_auth
    @ratelimit()
    def get(self, project_id):
        """Get a project details
        <a href="http://developers.goteo.org/projects#project">developers.goteo.org/projects#project</a>
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
            item['date-created'] = p.date_created
            item['date-published'] = p.date_published
            item['date-updated'] = p.date_updated
            item['date-succeeded'] = p.date_success
            item['date-closed'] = p.date_closed
            item['date-passed'] = p.date_passed
            item['description-short'] = p.subtitle
            item['video-url'] = p.media
            item['image-url'] = image_url(p.image, 'medium', False)
            item['image-url-big'] = image_url(p.image, 'big', False)
            item['project-url'] = project_url(p.id)
            item['widget-url'] = project_widget_url(p.id)
            item['currency-rate'] = p.currency_rate
            item['status'] = p.status_string
            location = ProjectLocation.get(p.id)
            if location:
                item['location'] = [marshal(location, project_location_resource_fields)]
                item['location'][0]['country-code'] = location.country_code
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
                item['costs'] = []
                for i in costs:
                    it = marshal(i, project_cost_resource_fields)
                    it['from-date'] = i.date_from
                    it['to-date'] = i.date_to
                    item['costs'].append(it)
            needs = Support.list_by_project(p.id)
            if needs:
                item['needs'] = marshal(needs, project_need_resource_fields)


        res = Response(
            starttime = time_start,
            attributes = item
        )

        return res


class ProjectDonorsListAPI(BaseItem):
    """Get donors list"""

    @requires_auth
    @ratelimit()
    def get(self, project_id):
        """Get the donors list
        <a href="http://developers.goteo.org/doc/users">developers.goteo.org/doc/users</a>
        """
        res = self._get(project_id)

        if res.ret['items'] == []:
            return bad_request('No users to list', 404)

        return res.response()

    def _get(self, project_id):
        """Get()'s method dirty work"""

        time_start = time.time()

        items = []
        for u in User.donors_by_project(project_id):
            item = marshal(u, user_resource_fields)
            item['date-created'] = u.date_created
            item['profile-url'] = u.profile_url
            item['profile-image-url'] = u.profile_image_url
            location = UserLocation.get(u.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
            items.append( item )

        res = Response(
            starttime = time_start,
            attributes = {'items' : items},
            # filters = args.items(),
            # total = User.total(**args)
        )

        return res
