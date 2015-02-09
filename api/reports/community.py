# -*- coding: utf-8 -*-
from model import app, db
from model import Invest, InvestNode, User, Category, Message, Project, UserInterest, UserRole, ProjectCategory, Call
from model import Location, LocationItem

from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, desc

from decorators import *
from config import config

import time

# DEBUG
if config.debug:
    db.session.query = debug_time(db.session.query)


@swagger.model
class CommunityResponse:
    """CommunityResponse"""

    __name__ = "CommunityResponse"

    resource_fields = {
        "categoria1": fields.String,
        "categoria2": fields.String,
        "categorias": fields.List,
        "cofinanciadores": fields.Integer,
        "colaboradores": fields.Integer,
        "coficolaboradores": fields.Integer,
        "impulcofinanciadores": fields.Integer,
        "impulcolaboradores": fields.Integer,
        "media-cofi": fields.Float,
        "media-colab": fields.Float,
        "multicofi": fields.Integer,
        "paypal": fields.Integer,
        "paypal-multicofi": fields.Integer,
        "perc-bajas": fields.Float,
        "perc-categoria1": fields.Float,
        "perc-categoria2": fields.Float,
        "users": fields.Integer,
        "users-cofi-perc": fields.Float,
        "users-multicofi-perc": fields.Float,
        "top10-investors": fields.List,
        "top10-invests": fields.List,
        "top10-collaborations": fields.List
    }

    required = resource_fields.keys()


class CommunityAPI(Resource):
    """Get Community Statistics"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('node', type=str, action='append')
        self.reqparse.add_argument('project', type=str, action='append')
        self.reqparse.add_argument('category', type=str)
        self.reqparse.add_argument('location', type=str)
        super(CommunityAPI, self).__init__()

    invalid_input = {
        "code": 400,
        "message": "Invalid parameters"
    }

    @swagger.operation(
    summary='Community report',
    notes='Community report',
    responseClass='CommunityResponse',
    nickname='community',
    parameters=[
        {
            "paramType": "query",
            "name": "project",
            "description": "Filter by individual project(s) separated by commas",
            "required": False,
            "dataType": "string",
            "allowMultiple": True
        },
        {
            "paramType": "query",
            "name": "from_date",
            "description": 'Filter from date. Ex. "2013-01-01"',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "to_date",
            "description": 'Filter until date.. Ex. "2014-01-01"',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "node",
            "description": 'Filter by individual node(s) separated by commas',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "category",
            "description": 'Filter by project category',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "location",
            "description": 'Filter by project location (Lat,lon,Km)',
            "required": False,
            "dataType": "string"
        }

    ],
    responseMessages=[invalid_input])
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the community reports
        <a href="http://developers.goteo.org/reports#community">developers.goteo.org/reports#community</a>
        """
        time_start = time.time()
        func = sqlalchemy.func
        args = self.reqparse.parse_args()

        filters = []
        filters2 = []  # para num de usuarios y bajas
        filters3 = []  # para categorias
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

        # - Número total de usuarios
        f_users = list(filters2)
        users = db.session.query(func.count(User.id)).filter(*f_users).scalar()

        # - Porcentaje (antes numero) de usuarios que se han dado de baja
        # Nota: faltarían además de los que se han dado de baja, los que han pedido que borremos datos por LOPD (que son muy pocos)
        f_bajas = list(filters2)
        f_bajas.append(User.active == 0)
        f_bajas.append(User.hide == 1)
        bajas = db.session.query(func.count(User.id)).filter(*f_bajas).scalar()

        # - Número de cofinanciadores
        f_cofinanciadores = list(filters)
        cofinanciadores = db.session.query(func.count(func.distinct(Invest.user))).filter(*f_cofinanciadores).scalar()

        # - Multi-Cofinanciadores (a más de 1 proyecto)
        f_multicofi = list(filters)
        f_multicofi.append(Invest.status.in_([config.INVEST_STATUS_PENDING,
                                              config.INVEST_STATUS_CHARGED,
                                              config.INVEST_STATUS_PAID,
                                              config.INVEST_STATUS_RETURNED]))
        _multicofi = db.session.query(Invest.user).filter(*f_multicofi).group_by(Invest.user).\
                                                    having(func.count(Invest.user) > 1).\
                                                    having(func.count(Invest.project) > 1)
        multicofi = _multicofi.count()

        # - Cofinanciadores usando PayPal
        f_paypal = list(filters)
        f_paypal.append(Invest.method==Invest.METHOD_PAYPAL)
        paypal = db.session.query(func.count(Invest.id)).filter(*f_paypal).scalar()

        # - Multi-Cofinanciadores usando PayPal
        f_paypal_multicofi = list(filters)
        f_paypal_multicofi.append(Invest.method==Invest.METHOD_PAYPAL)
        paypal_multicofi = _multicofi.filter(*f_paypal_multicofi).count()

        # - Número de colaboradores
        f_colaboradores = list(filters4)
        colaboradores = db.session.query(func.count(func.distinct(Message.user))).filter(*f_colaboradores).scalar()

        # - Cofinanciadores que colaboran
        sq_blocked = db.session.query(Message.id).filter(Message.blocked == 1).subquery()
        #
        f_coficolaboradores = list(filters)
        f_coficolaboradores.append(Message.thread > 0)
        f_coficolaboradores.append(Message.thread.in_(sq_blocked))
        f_coficolaboradores.append(Invest.status.in_([config.INVEST_STATUS_PENDING,
                                                      config.INVEST_STATUS_CHARGED,
                                                      config.INVEST_STATUS_PAID,
                                                      config.INVEST_STATUS_RETURNED]))
        coficolaboradores = db.session.query(func.count(func.distinct(Invest.user)))\
                                            .join(Message, Message.user == Invest.user)\
                                            .filter(*f_coficolaboradores).scalar()

        # - Media de cofinanciadores por proyecto exitoso
        f_media_cofi = list(filters)
        f_media_cofi.append(Project.status.in_([config.PROJECT_STATUS_FUNDED,
                                                config.PROJECT_STATUS_FULLFILED]))
        sq = db.session.query(func.count(func.distinct(Invest.user)).label("co"))\
                                    .join(Project, Invest.project == Project.id)\
                                    .filter(*f_media_cofi).group_by(Invest.project).subquery()
        media_cofi = db.session.query(func.avg(sq.c.co)).scalar()
        if media_cofi is None:
            media_cofi = 0

        # - Media de colaboradores por proyecto
        f_media_colab = list(filters4)
        f_media_colab.append(Project.status.in_([config.PROJECT_STATUS_FUNDED,
                                                 config.PROJECT_STATUS_FULLFILED]))
        sq = db.session.query(func.count(func.distinct(Message.user)).label("co"))\
                                    .join(Project, Message.project == Project.id)\
                                    .filter(*f_media_colab).group_by(Message.project).subquery()
        media_colab = db.session.query(func.avg(sq.c.co)).scalar()
        if media_colab is None:
            media_colab = 0

        # - Núm. impulsores que cofinancian a otros
        f_impulcofinanciadores = list(filters)
        f_impulcofinanciadores.append(Invest.status.in_([config.INVEST_STATUS_PAID,
                                                         config.INVEST_STATUS_RETURNED,
                                                         config.INVEST_STATUS_RELOCATED]))
        f_impulcofinanciadores.append(Invest.project != Project.id)
        impulcofinanciadores = db.session.query(func.count(func.distinct(Invest.user)))\
                                    .join(Project, and_(Project.owner == Invest.user, Project.status.in_([
                                        config.PROJECT_STATUS_FUNDED,
                                        config.PROJECT_STATUS_FULLFILED,
                                        config.PROJECT_STATUS_IN_CAMPAIGN,
                                        config.PROJECT_STATUS_UNFUNDED
                                     ])))\
                                    .filter(*f_impulcofinanciadores).scalar()

        # - Núm. impulsores que colaboran con otros
        f_impulcolaboradores = list(filters4)
        f_impulcolaboradores.append(Message.thread > 0)
        f_impulcolaboradores.append(Message.thread.in_(sq_blocked))
        f_impulcolaboradores.append(Message.project != Project.id)
        impulcolaboradores = db.session.query(func.count(func.distinct(Message.user)))\
                                    .join(Project, and_(Project.owner == Message.user, Project.status.in_([
                                        config.PROJECT_STATUS_FUNDED,
                                        config.PROJECT_STATUS_FULLFILED,
                                        config.PROJECT_STATUS_IN_CAMPAIGN,
                                        config.PROJECT_STATUS_UNFUNDED
                                    ])))\
                                    .filter(*f_impulcolaboradores).scalar()

        # - 1ª Categoría con más usuarios interesados
        f_categorias = list(filters3)
        categorias = db.session.query(func.count(UserInterest.user), Category.name)\
                        .join(Category).filter(*f_categorias).group_by(UserInterest.interest)\
                        .order_by(desc(func.count(UserInterest.user))).all()

        if len(categorias) >= 1:
            categoria1 = categorias[0][1]
            # - usuarios en esta 1ª
            users_categoria1 = categorias[0][0]
        else:
            categoria1 = None
            users_categoria1 = 0

        if len(categorias) >= 2:
            # - 2ª Categoría con más usuarios interesados
            categoria2 = categorias[1][1]
            # - usuarios en esta 2ª
            users_categoria2 = categorias[1][0]
        else:
            categoria2 = None
            users_categoria2 = 0

        #Listado de usuarios que no cuentan para estadisticias (admin, convocatorias)
        admines = db.session.query(UserRole.user_id).filter(UserRole.role_id == 'superadmin').all()
        convocadores = db.session.query(Call.owner).filter(Call.status > config.CALL_STATUS_REVIEWING).all()
        users_exclude = map(lambda c: c[0], admines)
        users_exclude.extend(map(lambda c: c[0], convocadores))
        # convertir en conjunto para evitar repeticiones
        users_exclude = set(users_exclude)
        # print('USERS EXCLUDE:', users_exclude)

        # - Top 10 Cofinanciadores (con mayor numero de contribuciones, excepto usuarios convocadores o superadmins)
        f_top10_multidonors = list(filters)
        f_top10_multidonors.append(Invest.status.in_([config.INVEST_STATUS_PENDING,
                                                 config.INVEST_STATUS_CHARGED,
                                                 config.INVEST_STATUS_PAID,
                                                 config.INVEST_STATUS_RETURNED]))
        f_top10_multidonors.append(~Invest.user.in_(users_exclude))
        top10_multidonors = db.session.query(Invest.user, func.count(Invest.id).label('contributions'), func.sum(Invest.amount).label('amount'))\
                                    .filter(*f_top10_multidonors).group_by(Invest.user)\
                                    .order_by(desc('contributions')).limit(10).all()


        # - Top 10 Cofinanciadores con más caudal (más generosos) excluir usuarios convocadores Y ADMINES
        f_top10_donors = list(filters)
        f_top10_donors.append(Invest.status.in_([config.INVEST_STATUS_PENDING,
                                                      config.INVEST_STATUS_CHARGED,
                                                      config.INVEST_STATUS_PAID,
                                                      config.INVEST_STATUS_RETURNED]))
        f_top10_donors.append(~Invest.user.in_(users_exclude))
        top10_donors = db.session.query(Invest.user, func.count(Invest.id).label('contributions'), func.sum(Invest.amount).label('amount'))\
                                    .filter(*f_top10_donors).group_by(Invest.user)\
                                    .order_by(desc('amount')).limit(10).all()

        # - Top 10 colaboradores
        f_top10_collaborations = list(filters4)
        top10_collaborations = db.session.query(Message.user, func.count(Message.id).label('interactions'))\
                            .filter(*f_top10_collaborations).group_by(Message.user)\
                            .order_by(desc('interactions')).limit(10).all()

        def percent(number, base=None):
            "Porcentaje en base a un total (por defecto users)"
            if base is None:
                base = users
            if base == 0:
                return 0
            perc = float(number) / base * 100
            return round(perc, 2)

        def format_categorias(t):
            total = t[0]
            name = t[1]
            perc = float(total) / users * 100
            perc = round(perc, 2)
            return {name: {'interesados': total, 'porcentaje': perc}}

        res = { 'users': users,
                'donors': cofinanciadores,
                'percentage-donors-users': percent(cofinanciadores),
                'percentage-unsubscribed-users': percent(bajas),
                'donors-collaborators': coficolaboradores,
                'multidonors': multicofi,
                'percentage-multidonor-donors': percent(multicofi, cofinanciadores),
                'percentage-multidonor-users': percent(multicofi),
                'paypal-donors': paypal,
                'paypal-multidonors': paypal_multicofi,
                'collaborators': colaboradores,
                'average-donors': media_cofi,
                'average-collaborators': media_colab,
                'creators-donors': impulcofinanciadores,
                'creators-collaborators': impulcolaboradores,
                'leading-category': categoria1,
                'users-leading-category': users_categoria1,
                'percentage-users-leading-category': percent(users_categoria1),
                'second-category': categoria2,
                'users-second-category': users_categoria2,
                'percentage-users-second-category': percent(users_categoria2),
                'categories': map(lambda i: format_categorias(i), categorias),
                'top10-donors': top10_donors,
                'top10-multidonors': top10_multidonors,
                'top10-collaborators': top10_collaborations}

        res['time-elapsed'] = time.time() - time_start
        res['filters'] = {}
        for k, v in args.items():
            if v is not None:
                res['filters'][k] = v

        return jsonify(res)
