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

# DEBUG
import time
def debug_time(func):
    def new_f(*args, **kwargs):
        time_start = time.time()
        res = func(*args, **kwargs)
        total_time = time.time() - time_start
        app.logger.debug('Time ' + func.__name__ + ': ' + str(total_time))
        return res
    return new_f
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
    def get(self):
        """Get the Community Report

        Descripción de los valores devueltos:
        <strong>users</strong>: Número total de usuarios registrados
        <strong>perc-bajas</strong>: Porcentaje de usuarios que se han dado de baja
        <strong>cofinanciadores</strong>: Número de cofinanciadores
        <strong>users-cofi-perc</strong>: % usuarios registrados que son cofinanciadores
        <strong>coficolaboradores</strong>: Número de cofinanciadores que colaboran
        <strong>multicofi</strong>: Número de Multi-Cofinanciadores (a más de 1 proyecto)
        <strong>users-multicofi-perc</strong>: % de Multi-Cofinanciadores (a más de 1 proyecto)
        <strong>paypal</strong>: Número de cofinanciadores que usan PayPal
        <strong>paypal-multicofi</strong>: Número de Multi-Cofinanciadores que usan PayPal
        <strong>colaboradores</strong>: Número de colaboradores
        <strong>media-cofi</strong>: Media de cofinanciadores por proyecto exitoso
        <strong>media-colab</strong>: Media de colaboradores por proyecto
        <strong>impulcofinanciadores</strong>: Número de impulsores que cofinancian a otros
        <strong>impulcolaboradores</strong>: Número de impulsores que colaboran con otros
        <strong>categoria1</strong>: 1ª categoría con más usuarios interesados
        <strong>perc-categoria1</strong>: % usuarios en esta 1ª categoría
        <strong>categoria2</strong>: 2ª categoría con más usuarios interesados
        <strong>perc-categoria2</strong>: % usuarios en esta 2ª categoría
        <strong>top10-investors</strong>: Top 10 cofinanciadores
        <strong>top10-invests</strong>: Top 10 cofinanciadores con más caudal (más generosos) sin incluir usuarios convocadores
        <strong>top10-collaborations</strong>: Top 10 colaboradores

        <strong>categorias</strong>:

        Además se añade el campo "filters"
        """
        time_start = time.time()
        func = sqlalchemy.func
        args = self.reqparse.parse_args()

        filters = []
        filters2 = []
        filters3 = []
        filters4 = []
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
            filters2.append(Invest.date_invested >= args['from_date'])
            filters3.append(Invest.date_invested >= args['from_date'])
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
            filters2.append(Invest.date_invested <= args['to_date'])
            filters3.append(Invest.date_invested <= args['to_date'])
        if args['project']:
            filters.append(Invest.project.in_(args['project']))
            filters2.append(Invest.project.in_(args['project']))
            filters3.append(Invest.project.in_(args['project']))
        if args['node']:
            filters.append(Invest.id == InvestNode.invest_id)
            filters.append(InvestNode.invest_node.in_(args['node']))
            filters2.append(User.node.in_(args['node']))
            filters3.append(UserInterest.user == User.id)
            filters3.append(User.node.in_(args['node']))
        if args['category']:
            try:
                category_id = db.session.query(Category.id).filter(Category.name == args['category']).one()
                category_id = category_id[0]
            except NoResultFound:
                return {"error": "Invalid category"}  # TODO: Return empty, http 400

            filters.append(Invest.project == ProjectCategory.project)
            filters.append(ProjectCategory.category == category_id)
            # filters2 y filters3 no hacen uso
            filters4.append(Message.project == ProjectCategory.project)
            filters4.append(ProjectCategory.category == category_id)
        if args['location']:
            # Filtra por la localización del usuario
            location = args['location'].split(",")
            if len(location) != 3:
                return {"error": "Invalid parameter: location"}  # TODO: Return empty, http 400

            from geopy.distance import VincentyDistance
            latitude, longitude, radius = location

            locations = db.session.query(Location.id, Location.lat, Location.lon).all()
            locations = filter(lambda l: VincentyDistance((latitude, longitude), (l[1], l[2])).km <= int(radius), locations)
            locations_ids = map(lambda l: int(l[0]), locations)

            if locations_ids == []:
                return {"error": "No locations in the specified range"}  # TODO: Return empty, http 400

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
        users = db.session.query(User).filter(*f_users).count()

        def perc_users(number):
            if users == 0:
                return 0
            perc = float(number) / users * 100
            return round(perc, 2)

        # - Porcentaje (antes numero) de usuarios que se han dado de baja
        # Nota: faltarían además de los que se han dado de baja, los que han pedido que borremos datos por LOPD (que son muy pocos)
        f_bajas = list(filters2)
        f_bajas.append(User.active == 0)
        f_bajas.append(User.hide == 1)
        bajas = db.session.query(User).filter(*f_bajas).count()
        p_bajas = perc_users(bajas)

        # - Número de cofinanciadores
        f_cofinanciadores = list(filters)
        _cofinanciadores = db.session.query(func.distinct(Invest.user)).filter(*f_cofinanciadores) # .subquery()
        cofinanciadores = int(_cofinanciadores.count())

        # - NEW Porcentaje de usuarios cofinanciadores
        users_cofi_perc = perc_users(cofinanciadores)
        #users_cofi_perc = float(cofinanciadores) / users * 100  # %
        #users_cofi_perc = _round(users_cofi_perc)

        # - Multi-Cofinanciadores (a más de 1 proyecto)
        f_multicofi = list(filters)
        f_multicofi.append(Invest.status.in_([0, 1, 3, 4]))
        _multicofi = db.session.query(Invest.user).filter(*f_multicofi).group_by(Invest.user).\
                                                    having(func.count(Invest.user) > 1).\
                                                    having(func.count(Invest.project) > 1)
        multicofi = _multicofi.count()

        # - NEW Porcentaje de Multi-Cofinanciadores (a más de 1 proyecto)
        users_multicofi_perc = perc_users(multicofi)

        # - Cofinanciadores usando PayPal
        f_paypal = list(filters)
        f_paypal.append(Invest.method==Invest.METHOD_PAYPAL)
        paypal = db.session.query(Invest).filter(*f_paypal).count()

        # - Multi-Cofinanciadores usando PayPal
        f_paypal_multicofi = list(filters)
        f_paypal_multicofi.append(Invest.method==Invest.METHOD_PAYPAL)
        paypal_multicofi = _multicofi.filter(*f_paypal_multicofi).count()

        # - Número de colaboradores
        f_colaboradores = list(filters)
        if args['node']:
            #FIXME: Revisar
            f_colaboradores.append(Message.user == User.id)
        _colaboradores = db.session.query(func.distinct(Message.user)).filter(*f_colaboradores) # .subquery()
        colaboradores = int(_colaboradores.count())

        # - Cofinanciadores que colaboran
        sq_blocked = db.session.query(Message.id).filter(Message.blocked == 1).subquery()
        #
        f_coficolaboradores = list(filters)
        f_coficolaboradores.append(Message.thread > 0)
        f_coficolaboradores.append(Message.thread.in_(sq_blocked))
        f_coficolaboradores.append(Invest.status.in_([0, 1, 3, 4]))
        coficolaboradores = db.session.query(func.count(func.distinct(Invest.user)))\
                                            .join(Message, Message.user == Invest.user)\
                                            .filter(*f_coficolaboradores).scalar()

        # - Media de cofinanciadores por proyecto exitoso
        f_media_cofi = list(filters)
        f_media_cofi.append(Project.status.in_([4, 5]))
        sq = db.session.query(func.count(func.distinct(Invest.user)).label("co"))\
                                    .join(Project, Invest.project == Project.id)\
                                    .filter(*f_media_cofi).group_by(Invest.project).subquery()
        media_cofi = db.session.query(func.avg(sq.c.co)).scalar()
        if media_cofi is None:
            media_cofi = 0

        # - Media de colaboradores por proyecto
        f_media_colab = list(filters)
        f_media_colab.append(Project.status.in_([4, 5]))
        sq = db.session.query(func.count(func.distinct(Message.user)).label("co"))\
                                    .join(Project, Message.project == Project.id)\
                                    .filter(*f_media_colab).group_by(Message.project).subquery()
        media_colab = db.session.query(func.avg(sq.c.co)).scalar()
        if media_colab is None:
            media_colab = 0

        # - Núm. impulsores que cofinancian a otros
        f_impulcofinanciadores = list(filters)
        f_impulcofinanciadores.append(Invest.status.in_([3, 4, 5, 6]))
        f_impulcofinanciadores.append(Invest.project != Project.id)
        impulcofinanciadores = db.session.query(func.count(func.distinct(Invest.user)))\
                                    .join(Project, and_(Project.owner == Invest.user, Project.status.in_([3, 4, 5, 6])))\
                                    .filter(*f_impulcofinanciadores).scalar()

        # - Núm. impulsores que colaboran con otros
        f_impulcolaboradores = list(filters)
        f_impulcolaboradores.append(Message.thread > 0)
        f_impulcolaboradores.append(Message.thread.in_(sq_blocked))
        f_impulcolaboradores.append(Message.project != Project.id)
        impulcolaboradores = db.session.query(func.count(func.distinct(Message.user)))\
                                    .join(Project, and_(Project.owner == Message.user, Project.status.in_([3, 4, 5, 6])))\
                                    .filter(*f_impulcolaboradores).scalar()

        # - 1ª Categoría con más usuarios interesados
        f_categorias = list(filters3)
        categorias = db.session.query(func.count(UserInterest.user), Category.name)\
                        .join(Category).filter(*f_categorias).group_by(UserInterest.interest)\
                        .order_by(desc(func.count(UserInterest.user))).all()

        if len(categorias) >= 1:
            categoria1 = categorias[0][1]

            # - Porcentaje de usuarios en esta 1ª
            perc_categoria1 = perc_users(categorias[0][0])
        else:
            categoria1 = None
            perc_categoria1 = 0

        if len(categorias) >= 2:
            # - 2ª Categoría con más usuarios interesados
            categoria2 = categorias[1][1]

            # - Porcentaje de usuarios en esta 2ª
            perc_categoria2 = perc_users(categorias[1][0])
        else:
            categoria2 = None
            perc_categoria2 = 0

        # - Top 10 Cofinanciadores (REVISAR como sacamos estos datos, excepto admines)
        f_top10_investors = list(filters)
        f_top10_investors.append(Invest.user == UserRole.user_id)
        f_top10_investors.append(~UserRole.role_id.in_(['admin', 'superadmin']))
        top10_investors = db.session.query(Invest.user, func.count(Invest.id).label('total'))\
                                    .filter(*f_top10_investors).group_by(Invest.user)\
                                    .order_by(desc('total')).limit(10).all()

        # - Top 10 Cofinanciadores con más caudal (más generosos) excluir usuarios convocadores Y ADMINES
        convocadores = db.session.query(Call.owner).filter(Call.status > 2).all()
        convocadores = map(lambda c: c[0], convocadores)

        f_top10_invests = list(filters)
        f_top10_invests.append(Invest.user == UserRole.user_id)
        f_top10_invests.append(~Invest.user.in_(convocadores))
        f_top10_invests.append(~UserRole.role_id.in_(['admin', 'superadmin']))
        top10_invests = db.session.query(Invest.user, func.sum(Invest.amount).label('total'))\
                                    .filter(*f_top10_invests).group_by(Invest.user)\
                                    .order_by(desc('total')).limit(10).all()

        # - Top 10 colaboradores
        f_top10_collaborations = list(filters4)
        top10_collaborations = db.session.query(Message.user, func.count(Message.id).label('total'))\
                            .filter(*f_top10_collaborations).group_by(Message.user)\
                            .order_by(desc('total')).limit(10).all()

        def format_categorias(t):
            total = t[0]
            name = t[1]
            perc = float(total) / users * 100
            perc = round(perc, 2)
            return {name: {'interesados': total, 'porcentaje': perc}}

        res = {'users': users,
                'users-cofi-perc': users_cofi_perc, 'multicofi': multicofi,
                'users-multicofi-perc': users_multicofi_perc, 'paypal': paypal,
                'paypal-multicofi': paypal_multicofi, 'perc-bajas': p_bajas,
                'colaboradores': colaboradores,
                'impulcofinanciadores': impulcofinanciadores,
                'impulcolaboradores': impulcolaboradores,
                'coficolaboradores': coficolaboradores,
                'media-cofi': media_cofi, 'media-colab': media_colab,
                'categorias': map(lambda i: format_categorias(i), categorias),
                'categoria1': categoria1, 'categoria2': categoria2,
                'perc-categoria1': perc_categoria1, 'perc-categoria2': perc_categoria2,
                'top10-investors': top10_investors, 'top10-invests': top10_invests,
                'top10-collaborations': top10_collaborations}
                #'categories': ['a','b']})

        res['time-elapsed'] = time.time() - time_start
        res['filters'] = {}
        for k, v in args.items():
            if v is not None:
                res['filters'][k] = v

        return jsonify(res)
