# -*- coding: utf-8 -*-

import time

from flask.ext.restful import Resource, fields
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, desc

from config import config

from api import db

from api.models import Invest, InvestNode, User, Category, Message, Project, UserInterest, UserRole, ProjectCategory, Call
from api.models import Location, LocationItem
from api.decorators import *

from api.reports.base import Base, Response

# DEBUG
if config.debug:
    db.session.query = debug_time(db.session.query)

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
        'amount'       : fields.Float,
        'contributions': fields.Integer
    }
    required = resource_fields.keys()

@swagger.model
class UserCollaboration:
    resource_fields = {
        'user'        : fields.String,
        'interactions': fields.Integer
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
        "paypal-multidonors"               : fields.Integer,
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
        <a href="http://developers.goteo.org/reports#community">developers.goteo.org/reports#community</a>
        """
        time_start = time.time()
        args = self.reqparse.parse_args()

        filters = []
        filters2 = []  # para num de usuarios y bajas
        filters3 = [Category.name != '']  # para categorias
        filters4 = []  # para las relacionadas con Colaboradores
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
            filters2.append(Invest.date_invested >= args['from_date'])
            filters2.append(Invest.user == User.id)
            filters3.append(Invest.date_invested >= args['from_date'])
            filters3.append(Invest.user == UserInterest.user)
            filters4.append(Message.date >= args['from_date'])
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
            filters2.append(Invest.date_invested <= args['to_date'])
            filters2.append(Invest.user == User.id)
            filters3.append(Invest.date_invested <= args['to_date'])
            filters3.append(Invest.user == UserInterest.user)
            filters4.append(Message.date <= args['to_date'])
        if args['project']:
            filters.append(Invest.project.in_(args['project']))
            filters2.append(Invest.project.in_(args['project']))
            filters2.append(User.id == Invest.user)
            filters3.append(Invest.project.in_(args['project']))
            filters3.append(UserInterest.user == Invest.user)
            filters4.append(Message.project.in_(args['project']))
        if args['node']:
            #TODO: project_node o invest_node?
            filters.append(Invest.id == InvestNode.invest_id)
            filters.append(InvestNode.invest_node.in_(args['node']))
            filters2.append(User.node.in_(args['node']))
            filters3.append(UserInterest.user == User.id)
            filters3.append(User.node.in_(args['node']))
            filters4.append(Message.user == User.id)
            filters4.append(User.node.in_(args['node']))
        if args['category']:
            try:
                category_id = db.session.query(Category.id).filter(Category.name == args['category']).one()
                category_id = category_id[0]
            except NoResultFound:
                return bad_request("Invalid category")

            filters.append(Invest.project == ProjectCategory.project)
            filters.append(ProjectCategory.category == category_id)
            # filters2 y filters3 no hacen uso
            filters4.append(Message.project == ProjectCategory.project)
            filters4.append(ProjectCategory.category == category_id)
        if args['location']:
            # Filtra por la localización del usuario
            location = args['location'].split(",")
            if len(location) != 3:
                return bad_request("Invalid parameter: location")

            from geopy.distance import VincentyDistance
            latitude, longitude, radius = location

            radius = int(radius)
            if radius > 500 or radius < 0:
                return bad_request("Radius must be a value between 0 and 500 Km")

            locations = db.session.query(Location.id, Location.lat, Location.lon).all()
            locations = filter(lambda l: VincentyDistance((latitude, longitude), (l[1], l[2])).km <= radius, locations)
            locations_ids = map(lambda l: int(l[0]), locations)

            if locations_ids == []:
                return bad_request("No locations in the specified range")

            filters.append(Invest.user == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            filters.append(LocationItem.id.in_(locations_ids))
            filters2.append(User.id == LocationItem.item)
            filters2.append(LocationItem.type == 'user')
            filters2.append(LocationItem.id.in_(locations_ids))
            filters3.append(UserInterest.user == LocationItem.item)
            filters3.append(LocationItem.type == 'user')
            filters3.append(LocationItem.id.in_(locations_ids))
            filters4.append(Message.user == LocationItem.item)
            filters4.append(LocationItem.type == 'user')
            filters4.append(LocationItem.id.in_(locations_ids))

        users = self._users(list(filters2))
        bajas = self._bajas(list(filters2))
        donors = self._donors(list(filters))
        multidonors = self._multidonors(list(filters))
        categorias = self._categorias(list(filters3))
        users_categoria1 = categorias[0].users if len(categorias) > 0 else None
        users_categoria2 = categorias[1].users if len(categorias) > 1 else None

        # Listado de usuarios que no cuentan para estadisticias (admin, convocatorias)
        admines = db.session.query(UserRole.user_id).filter(UserRole.role_id == 'superadmin').all()
        convocadores = db.session.query(Call.owner).filter(Call.status > Call.STATUS_REVIEWING).all()
        users_exclude = map(lambda c: c[0], admines)
        users_exclude.extend(map(lambda c: c[0], convocadores))
        # convertir en conjunto para evitar repeticiones
        users_exclude = set(users_exclude)


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
                'collaborators'                     : self._colaboradores(list(filters4)),
                'paypal-donors'                     : self._paypal(list(filters)),
                'paypal-multidonors'                : self._paypal_multidonors(list(filters)),
                'donors-collaborators'              : self._coficolaboradores(list(filters)),
                'average-donors'                    : self._media_cofi(list(filters)),
                'average-collaborators'             : self._media_colab(list(filters4)),
                'creators-donors'                   : self._impulcofinanciadores(list(filters)),
                'creators-collaborators'            : self._impulcolaboradores(list(filters4)),
                'categories'                        : map(lambda t: {t.id: {'users': t.users, 'id': t.id, 'name': t.name, 'percentage-users': percent(t.users, users)}}, categorias),
                'leading-category'                  : categorias[0].id if len(categorias) > 0 else None,
                'users-leading-category'            : users_categoria1,
                'percentage-users-leading-category' : percent(users_categoria1, users),
                'second-category'                   : categorias[1].id if len(categorias) > 1 else None,
                'users-second-category'             : users_categoria2,
                'percentage-users-second-category'  : percent(users_categoria2, users),
                'top10-multidonors'                 : self._top10_multidonors(list(filters), users_exclude),
                'top10-donors'                      : self._top10_donors(list(filters), users_exclude),
                'top10-collaborators'               : self._top10_collaborations(list(filters4)),
            },
            filters = args.items()
        )
        return res.response()

    # Número total de usuarios
    def _users(self, f_users = []):
        res = db.session.query(func.count(User.id)).filter(*f_users).scalar()
        if res is None:
            res = 0
        return res

    # Porcentaje (antes numero) de usuarios que se han dado de baja
    # Nota: faltarían además de los que se han dado de baja, los que han pedido que borremos datos por LOPD (que son muy pocos)
    def _bajas(self, f_bajas = []):
        f_bajas.append(User.active == 0)
        f_bajas.append(User.hide == 1)
        res = db.session.query(func.count(User.id)).filter(*f_bajas).scalar()
        if res is None:
            res = 0
        return res

    # Número de cofinanciadores
    def _donors(self, f_cofinanciadores = []):
        res = db.session.query(func.count(func.distinct(Invest.user))).filter(*f_cofinanciadores).scalar()
        if res is None:
            res = 0
        return res

    # Multi-Cofinanciadores (a más de 1 proyecto)
    def _multidonors(self, f_multidonors = []):
        f_multidonors.append(Invest.status.in_([Invest.STATUS_PENDING,
                                              Invest.STATUS_CHARGED,
                                              Invest.STATUS_PAID,
                                              Invest.STATUS_RETURNED]))
        _multidonors = db.session.query(Invest.user).filter(*f_multidonors).group_by(Invest.user).\
                                                    having(func.count(Invest.user) > 1).\
                                                    having(func.count(Invest.project) > 1)
        res = _multidonors.count()
        if res is None:
            res = 0
        return res

    # Cofinanciadores usando PayPal
    def _paypal(self, f_paypal = []):
        f_paypal.append(Invest.method == Invest.METHOD_PAYPAL)
        res = db.session.query(func.count(Invest.id)).filter(*f_paypal).scalar()


        if res is None:
            res = 0
        return res

    # Multi-Cofinanciadores usando PayPal
    def _paypal_multidonors(self, f_paypal = []):
        f_paypal.append(Invest.method==Invest.METHOD_PAYPAL)
        return self._multidonors(f_paypal)

    # Número de colaboradores
    def _colaboradores(self, f_colaboradores = []):
        res = db.session.query(func.count(func.distinct(Message.user))).filter(*f_colaboradores).scalar()
        if res is None:
            res = 0
        return res

    # Cofinanciadores que colaboran
    def _coficolaboradores(self, f_coficolaboradores = []):
        sq_blocked = db.session.query(Message.id).filter(Message.blocked == 1).subquery()
        f_coficolaboradores.append(Message.thread > 0)
        f_coficolaboradores.append(Message.thread.in_(sq_blocked))
        f_coficolaboradores.append(Invest.status.in_([Invest.STATUS_PENDING,
                                                      Invest.STATUS_CHARGED,
                                                      Invest.STATUS_PAID,
                                                      Invest.STATUS_RETURNED]))
        res = db.session.query(func.count(func.distinct(Invest.user)))\
                                            .join(Message, Message.user == Invest.user)\
                                            .filter(*f_coficolaboradores).scalar()
        if res is None:
            res = 0
        return res

    # Media de cofinanciadores por proyecto exitoso
    def _media_cofi(self, f_media_cofi = []):
        f_media_cofi.append(Project.status.in_([Project.STATUS_FUNDED,
                                                Project.STATUS_FULLFILED]))
        sq = db.session.query(func.count(func.distinct(Invest.user)).label("co"))\
                                    .join(Project, Invest.project == Project.id)\
                                    .filter(*f_media_cofi).group_by(Invest.project).subquery()
        res = db.session.query(func.avg(sq.c.co)).scalar()
        if res is None:
            res = 0
        return res

    # Media de colaboradores por proyecto
    def _media_colab(self, f_media_colab = []):
        f_media_colab.append(Project.status.in_([Project.STATUS_FUNDED,
                                                 Project.STATUS_FULLFILED]))
        sq = db.session.query(func.count(func.distinct(Message.user)).label("co"))\
                                    .join(Project, Message.project == Project.id)\
                                    .filter(*f_media_colab).group_by(Message.project).subquery()
        res = db.session.query(func.avg(sq.c.co)).scalar()
        if res is None:
            res = 0
        return res

    # Núm. impulsores que cofinancian a otros
    def _impulcofinanciadores(self, f_impulcofinanciadores = []):
        f_impulcofinanciadores.append(Invest.status.in_([Invest.STATUS_PAID,
                                                         Invest.STATUS_RETURNED,
                                                         Invest.STATUS_RELOCATED]))
        f_impulcofinanciadores.append(Invest.project != Project.id)
        res = db.session.query(func.count(func.distinct(Invest.user)))\
                                    .join(Project, and_(Project.owner == Invest.user, Project.status.in_([
                                        Project.STATUS_FUNDED,
                                        Project.STATUS_FULLFILED,
                                        Project.STATUS_IN_CAMPAIGN,
                                        Project.STATUS_UNFUNDED
                                     ])))\
                                    .filter(*f_impulcofinanciadores).scalar()
        if res is None:
            res = 0
        return res

    # Núm. impulsores que colaboran con otros
    def _impulcolaboradores(self, f_impulcolaboradores = []):
        sq_blocked = db.session.query(Message.id).filter(Message.blocked == 1).subquery()
        f_impulcolaboradores.append(Message.thread > 0)
        f_impulcolaboradores.append(Message.thread.in_(sq_blocked))
        f_impulcolaboradores.append(Message.project != Project.id)
        res = db.session.query(func.count(func.distinct(Message.user)))\
                                    .join(Project, and_(Project.owner == Message.user, Project.status.in_([
                                        Project.STATUS_FUNDED,
                                        Project.STATUS_FULLFILED,
                                        Project.STATUS_IN_CAMPAIGN,
                                        Project.STATUS_UNFUNDED
                                    ])))\
                                    .filter(*f_impulcolaboradores).scalar()
        if res is None:
            res = 0
        return res

    # Lista de categorias
    # TODO: idiomas para los nombres de categorias aqui
    def _categorias(self, f_categorias = []):
        res = db.session.query(func.count(UserInterest.user).label('users'), Category.id, Category.name)\
                        .join(Category).filter(*f_categorias).group_by(UserInterest.interest)\
                        .order_by(desc(func.count(UserInterest.user))).all()
        if res is None:
            res = []
        return res


    # Top 10 Cofinanciadores (con mayor numero de contribuciones, excepto usuarios convocadores o superadmins)
    def _top10_multidonors(self, f_top10_multidonors = [], users_exclude = []):
        f_top10_multidonors.append(Invest.status.in_([Invest.STATUS_PENDING,
                                                 Invest.STATUS_CHARGED,
                                                 Invest.STATUS_PAID,
                                                 Invest.STATUS_RETURNED]))
        f_top10_multidonors.append(~Invest.user.in_(users_exclude))
        res = db.session.query(Invest.user, func.count(Invest.id).label('contributions'), func.sum(Invest.amount).label('amount'))\
                                    .filter(*f_top10_multidonors).group_by(Invest.user)\
                                    .order_by(desc('contributions'), desc('amount')).limit(10).all()
        if res is None:
            res = []
        return res


    # Top 10 Cofinanciadores con más caudal (más generosos) excluir usuarios convocadores Y ADMINES
    def _top10_donors(self, f_top10_donors = [], users_exclude = []):
        f_top10_donors.append(Invest.status.in_([Invest.STATUS_PENDING,
                                                      Invest.STATUS_CHARGED,
                                                      Invest.STATUS_PAID,
                                                      Invest.STATUS_RETURNED]))
        f_top10_donors.append(~Invest.user.in_(users_exclude))
        res = db.session.query(Invest.user, func.count(Invest.id).label('contributions'), func.sum(Invest.amount).label('amount'))\
                                    .filter(*f_top10_donors).group_by(Invest.user)\
                                    .order_by(desc('amount'), desc('contributions')).limit(10).all()
        if res is None:
            res = []
        return res

    # Top 10 colaboradores
    def _top10_collaborations(self, f_top10_collaborations = []):
        res = db.session.query(Message.user, func.count(Message.id).label('interactions'))\
                            .filter(*f_top10_collaborations).group_by(Message.user)\
                            .order_by(desc('interactions')).limit(10).all()
        if res is None:
            res = []
        return res

