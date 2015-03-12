# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy import and_, desc
from sqlalchemy.orm import aliased

from api import db

from api.models.call import Call
from api.models.category import Category, CategoryLang
from api.models.project import Project, ProjectCategory
from api.models.invest import Invest, InvestNode
from api.models.message import Message
from api.models.user import User, UserInterest, UserRole
from api.models.location import Location, LocationItem
from api.decorators import *
from api.helpers import get_lang, image_url, user_url
from api.base_endpoint import BaseList as Base, Response

func = sqlalchemy.func

@swagger.model
class CategoryUsers:
    resource_fields = {
        'id'              : fields.Integer,
        'name'            : fields.String,
        'percentage-users': fields.Float,
        'users'           : fields.Integer
    }
    required = resource_fields.keys()

@swagger.model
class UserDonation:
    resource_fields = {
        'user'         : fields.String,
        'name'              : fields.String,
        'profile-image-url' : fields.String,
        'profile-url' : fields.String,
        'amount'       : fields.Float,
        'contributions': fields.Integer
    }
    required = resource_fields.keys()

@swagger.model
class UserCollaboration:
    resource_fields = {
        'user'              : fields.String,
        'name'              : fields.String,
        'profile-image-url' : fields.String,
        'profile-url' : fields.String,
        'interactions'      : fields.Integer
    }
    required = resource_fields.keys()

@swagger.model
@swagger.nested(**{
                'categories'         :CategoryUsers.__name__,
                'top10-donors'       :UserDonation.__name__,
                'top10-multidonors'  :UserDonation.__name__,
                'top10-collaborators':UserCollaboration.__name__
                }
            )
class CommunityResponse(Response):
    """CommunityResponse"""

    resource_fields = {
        "users"                            : fields.Integer,
        "donors"                           : fields.Integer,
        "percentage-donors-users"          : fields.Float,
        "percentage-unsubscribed-users"    : fields.Float,
        "donors-collaborators"             : fields.Integer,
        "multidonors"                      : fields.Integer,
        "percentage-multidonor-donors"     : fields.Float,
        "percentage-multidonor-users"      : fields.Float,
        "paypal-donors"                    : fields.Integer,
        "creditcard-donors"                : fields.Integer,
        "cash-donors"                      : fields.Integer,
        "collaborators"                    : fields.Integer,
        'average-donors'                   : fields.Integer,
        'average-collaborators'            : fields.Integer,
        'creators-donors'                  : fields.Integer,
        'creators-collaborators'           : fields.Integer,
        'leading-category'                 : fields.Integer,
        'second-category'                  : fields.Integer,
        'users-leading-category'           : fields.Integer,
        'users-second-category'            : fields.Integer,
        'percentage-users-leading-category': fields.Float,
        'percentage-users-second-category' : fields.Float,
        'categories'                       : fields.List(fields.Nested(CategoryUsers.__name__)),
        "top10-donors"                     : fields.List(fields.Nested(UserDonation.__name__)),
        "top10-multidonors"                : fields.List(fields.Nested(UserDonation.__name__)),
        "top10-collaborators"              : fields.List(fields.Nested(UserCollaboration.__name__))
    }

    required = resource_fields.keys()


class CommunityAPI(Base):
    """Get Community Statistics"""

    def __init__(self):
        super(CommunityAPI, self).__init__()

    @swagger.operation(
        notes='Community report',
        responseClass=CommunityResponse.__name__,
        nickname='community',
        parameters=Base.INPUT_FILTERS,
        responseMessages=Base.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the community reports
        <a href="http://developers.goteo.org/doc/reports#community">developers.goteo.org/doc/reports#community</a>
        """
        ret = self._get()
        return ret.response()

    def _get(self):
        """Get()'s method dirty work"""
        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))


        filters = []
        filters_categories = [Category.name != '']  # para categorias
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
            filters_categories.append(Invest.date_invested >= args['from_date'])
            filters_categories.append(Invest.user == UserInterest.user)
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
            filters_categories.append(Invest.date_invested <= args['to_date'])
            filters_categories.append(Invest.user == UserInterest.user)
        if args['project']:
            filters.append(Invest.project.in_(args['project']))
            filters_categories.append(Invest.project.in_(args['project']))
            filters_categories.append(UserInterest.user == Invest.user)
        if args['node']:
            #TODO: project_node o invest_node?
            filters.append(Invest.id == InvestNode.invest_id)
            filters.append(InvestNode.invest_node.in_(args['node']))
            filters_categories.append(UserInterest.user == User.id)
            filters_categories.append(User.node.in_(args['node']))
        if args['category']:

            filters.append(Invest.project == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(args['category']))
        if args['location']:
            # Filtra por la localización del usuario
            locations_ids = Location.location_ids(**args['location'])

            if locations_ids == []:
                return bad_request("No locations in the specified range")

            filters.append(Invest.user == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            filters.append(LocationItem.id.in_(locations_ids))
            filters_categories.append(UserInterest.user == LocationItem.item)
            filters_categories.append(LocationItem.type == 'user')
            filters_categories.append(LocationItem.id.in_(locations_ids))

        users = User.total(**args)
        nargs = args.copy();
        nargs['unsubscribed'] = 1;
        bajas = User.total(**nargs)
        donors = Invest.donors_total(**args)
        multidonors = Invest.multidonors_total(**args)

        paypal_donors = Invest.donors_total(**dict(args, **{'method' : Invest.METHOD_PAYPAL}))
        creditcard_donors = Invest.donors_total(**dict(args, **{'method' : Invest.METHOD_TPV}))
        cash_donors = Invest.donors_total(**dict(args, **{'method' : Invest.METHOD_CASH}))
        # paypal_multidonors = Invest.multidonors_total(**dict(args, **{'method' : Invest.METHOD_PAYPAL}))

        categorias = self._categorias(list(filters_categories), args['lang'])
        users_categoria1 = categorias[0].users if len(categorias) > 0 else None
        users_categoria2 = categorias[1].users if len(categorias) > 1 else None

        # Listado de usuarios que no cuentan para estadisticias (admin, convocatorias)
        admines = db.session.query(UserRole.user_id).filter(UserRole.role_id == 'superadmin').all()
        convocadores = db.session.query(Call.owner).filter(Call.status > Call.STATUS_REVIEWING).all()
        users_exclude = map(lambda c: c[0], admines)
        users_exclude.extend(map(lambda c: c[0], convocadores))
        # convertir en conjunto para evitar repeticiones
        users_exclude = set(users_exclude)

        top10_multidonors = []
        for u in Invest.multidonors_list(**args):
            item = marshal(u, UserDonation.resource_fields)
            item['profile-image-url'] = image_url(u['avatar'])
            item['profile-url'] = user_url(u['id'])
            top10_multidonors.append(item)

        top10_donors = []
        for u in Invest.donors_list(**args):
            item = marshal(u, UserDonation.resource_fields)
            item['profile-image-url'] = image_url(u['avatar'])
            item['profile-url'] = user_url(u['id'])
            top10_donors.append(item)

        top10_collaborations = []
        for u in Message.collaborators_list(**args):
            item = marshal(u, UserCollaboration.resource_fields)
            item['profile-image-url'] = image_url(u['avatar'])
            item['profile-url'] = user_url(u['id'])
            top10_collaborations.append(item)

        res = CommunityResponse(
            starttime = time_start,
            attributes = {
                'users'                             : users,
                'donors'                            : donors,
                'multidonors'                       : multidonors,
                'percentage-donors-users'           : percent(donors, users),
                'percentage-unsubscribed-users'     : percent(bajas, users),
                'percentage-multidonor-donors'      : percent(multidonors, donors),
                'percentage-multidonor-users'       : percent(multidonors, users),
                'collaborators'                     : Message.collaborators_total(**args),
                'paypal-donors'                     : paypal_donors,
                'creditcard-donors'                 : creditcard_donors,
                'cash-donors'                       : cash_donors,
                'donors-collaborators'              : Invest.donors_collaborators_total(**args),
                'average-donors'                    : Invest.average_donors(**args),
                'average-collaborators'             : Message.average_collaborators(**args),
                'creators-donors'                   : Invest.donors_creators_total(**args),
                'creators-collaborators'            : Message.collaborators_creators_total(**args),
                'categories'                        : map(lambda t: {t.id:
                                                                        {'users': t.users,
                                                                         'id': t.id,
                                                                         'name': t.name,
                                                                         'percentage-users': percent(t.users, users)}
                                                                        }, categorias),
                'leading-category'                  : categorias[0].id if len(categorias) > 0 else None,
                'users-leading-category'            : users_categoria1,
                'percentage-users-leading-category' : percent(users_categoria1, users),
                'second-category'                   : categorias[1].id if len(categorias) > 1 else None,
                'users-second-category'             : users_categoria2,
                'percentage-users-second-category'  : percent(users_categoria2, users),
                'top10-multidonors'                 : top10_multidonors,
                'top10-donors'                      : top10_donors,
                'top10-collaborators'               : top10_collaborations,
            },
            filters = args.items()
        )
        return res

    # Lista de categorias
    # TODO: idiomas para los nombres de categorias aqui
    def _categorias(self, f_categorias = [], langs = []):
        # In case of requiring languages, a LEFT JOIN must be generated
        cols = [func.count(UserInterest.user).label('users'), Category.id, Category.name]
        if langs:
            joins = []
            _langs = {}
            for l in langs:
                _langs[l] = aliased(CategoryLang)
                cols.append(_langs[l].name_lang.label('name_' + l))
                joins.append((_langs[l], and_(_langs[l].id == Category.id, _langs[l].lang == l)))
            query = db.session.query(*cols).join(Category, Category.id == UserInterest.interest).outerjoin(*joins)
        else:
            query = db.session.query(*cols).join(Category, Category.id == UserInterest.interest)
        ret = []

        for u in query.filter(*f_categorias).group_by(UserInterest.interest)\
                      .order_by(desc(func.count(UserInterest.user))):
            # u = u._asdict()
            u.name = get_lang(u._asdict(), 'name', langs)
            ret.append(u)
        if ret is None:
            ret = []
        return ret
