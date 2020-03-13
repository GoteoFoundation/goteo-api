# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flasgger.utils import swag_from

from ..ratelimit import ratelimit
from ..auth.decorators import requires_auth
from ..helpers import DateTime, marshal, bad_request, image_url

from ..base_resources import BaseItem, BaseList, Response, project_status_sanitizer
from .models import Matcher, MatcherLang
from ..users.resources import user_resource_fields
from ..projects.resources import project_resource_fields
from ..projects.models import Project
from ..invests.models import Invest
from ..location.models import MatcherLocation, ProjectLocation
from ..location.models import location_resource_fields

matcher_users_resource_fields = {
    "name": fields.String,
    "url": fields.String,
    "image_url": fields.String,
    # "amount": fields.Float,
    # "order": fields.Integer,
}

matcher_resource_fields = {
    "id": fields.String,
    "name": fields.String,
    "matcher_url": fields.String,
    "logo_url": fields.String,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "radius": fields.Integer,
    "region": fields.String,
    "matcher_location": fields.String,
    "owner": fields.String,
    "owner_name": fields.String,
    "amount_available": fields.Float,
    "amount_peers": fields.Float,
    "amount_committed": fields.Float,
    "amount_remaining": fields.Float,
    "projects_total": fields.Integer,
    "projects_pending": fields.Integer,
    "projects_applied": fields.Integer,
    "projects_active": fields.Integer,
    "projects_rejected": fields.Integer,
    "projects_discarded": fields.Integer,
    "projects_accepted": fields.Integer,
    "projects_succeeded": fields.Integer,
    "date_created": DateTime,
    "active": fields.Boolean
}

matcher_full_resource_fields = matcher_resource_fields.copy()
matcher_full_resource_fields.pop('latitude')
matcher_full_resource_fields.pop('region')
matcher_full_resource_fields.pop('longitude')
matcher_full_resource_fields.pop('radius')
matcher_full_resource_fields["terms"] = fields.String
matcher_full_resource_fields["date_created"] = DateTime
matcher_full_resource_fields["logo_url_big"] = fields.String
matcher_full_resource_fields["user"] = fields.Nested(user_resource_fields)
matcher_full_resource_fields["location"] = fields.List(
    fields.Nested(location_resource_fields))
matcher_full_resource_fields['users'] = fields.List(
    fields.Nested(matcher_users_resource_fields))
matcher_project_resource_fields = project_resource_fields.copy()
matcher_project_resource_fields['amount_matcher'] = fields.Float
# Add radius
location_resource_fields['radius'] = fields.Integer

class MatchersListAPI(BaseList):
    """Matcher list"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/matcher_list.yml')
    def get(self):
        res = self._get()

        return res.response()

    def _get(self):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args()

        items = []
        for m in Matcher.list(**args):
            item = marshal(m, matcher_resource_fields)
            location = MatcherLocation.get(m.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
                item['radius'] = location.radius
                if location.region:
                    item['region'] = location.region
                else:
                    item['region'] = location.country
            item['projects-succeeded'] = m.projects_count(status='active', project_status=Project.SUCCESSFUL_PROJECTS)
            item['projects-pending'] = m.projects_count(status='pending')
            # item['projects-applied'] = m.projects_count(status='active') # Cached in "projects" field
            item['projects-accepted'] = m.projects_count(status='accepted')
            item['projects-rejected'] = m.projects_count(status='rejected')
            item['projects-discarded'] = m.projects_count(status='discarded')
            items.append(item)

        res = Response(
            starttime=time_start,
            attributes={'items': items},
            filters=args.items(),
            total=Matcher.total(**args)
        )

        return res


class MatcherAPI(BaseItem):
    """Matcher Details"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/matcher_item.yml')
    def get(self, matcher_id):
        res = self._get(matcher_id)

        if res.ret['id'] is None:
            return bad_request('Matchfunding matcher not found', 404)

        return res.response()

    def _get(self, matcher_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        m = Matcher.get(matcher_id)

        item = marshal(m, matcher_full_resource_fields)
        if m is not None:
            item['user'] = marshal(m.User, user_resource_fields)
            location = MatcherLocation.get(m.id)
            if location:
                item['location'] = [marshal(location,
                                            location_resource_fields)]
            translations = {}
            translate_keys = {
                k: v for k, v in matcher_full_resource_fields.items()
                if k in MatcherLang.get_translate_keys()
            }
            for k in m.Translations:
                translations[k.lang] = marshal(k, translate_keys)
                translations[k.lang]['terms'] = k.terms
            item['translations'] = translations

            item['projects-pending'] = m.projects_count(status='pending')
            item['projects-active'] = m.projects_count(status='active')
            item['projects-accepted'] = m.projects_count(status='accepted')
            item['projects-rejected'] = m.projects_count(status='rejected')
            item['projects-discarded'] = m.projects_count(status='discarded')

            users = []
            for s in m.users_list():
                users.append(marshal(s, matcher_users_resource_fields))
            item['users'] = users

        res = Response(
            starttime=time_start,
            attributes=item
        )

        return res


class MatcherProjectsListAPI(BaseList):
    """Projects list"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/matcher_projects.yml')
    def get(self, matcher_id):

        self.reqparse.add_argument('status', type=project_status_sanitizer, action='append')

        res = self._get(matcher_id)

        if res.ret['id'] is None:
            return bad_request('Matcher not found', 404)

        return res.response()

    def _get(self, matcher_id):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args()
        args['matcher'] = matcher_id

        items = []
        matcher = Matcher.get(matcher_id)
        if matcher is None:
            return Response(attributes={'id': None})

        for p in Project.list(**args):
            item = marshal(p, matcher_project_resource_fields)
            item['status'] = p.status_string
            item['amount-matcher'] = float(Invest.pledged_total(project=p.id,
                                                             user=matcher.owner,
                                                             method=Invest.METHOD_POOL))
            item['image-url'] = image_url(p.image, 'medium', False)
            location = ProjectLocation.get(p.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
                if location.region:
                    item['region'] = location.region
                else:
                    item['region'] = location.country
            items.append(item)

        res = Response(
            starttime=time_start,
            attributes={'id': matcher_id, 'items': items},
            filters=args.items(),
            total=Project.total(**args)
        )

        return res
