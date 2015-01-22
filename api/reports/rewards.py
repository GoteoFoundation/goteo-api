# -*- coding: utf-8 -*-
from model import app, db
from model import Category, Invest, Reward, InvestReward, InvestNode, Project, ProjectCategory
from model import Location, LocationItem

from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, or_, desc

from decorators import *

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
class RewardsPerAmount:
    resource_fields = {
        "rewards-between-100-400": fields.Integer,
        "rewards-between-15-30": fields.Integer,
        "rewards-between-30-100": fields.Integer,
        "rewards-less-than-15": fields.Integer,
        "rewards-more-than-400": fields.Integer
    }
    required = resource_fields.keys()

@swagger.model
@swagger.nested(
    rewards_per_amount=RewardsPerAmount.__name__)
    #rewards-per-amount=RewardsPerAmount.__name__)
class RewardsResponse:

    __name__ = "RewardsResponse"

    resource_fields = {
        "favorite-rewards": fields.List,
        "perc-renuncias": fields.Float,
        "renuncias": fields.Integer,
        "rewards_per_amount": fields.Nested(RewardsPerAmount.resource_fields)  # FIXME: parametros con guiones
    }

    required = resource_fields.keys()


@swagger.model
class RewardsAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('node', type=str, action='append')
        self.reqparse.add_argument('project', type=str, action='append')
        self.reqparse.add_argument('category', type=str)
        self.reqparse.add_argument('location', type=str)
        super(RewardsAPI, self).__init__()

    invalid_input = {
        "code": 400,
         "message": "Invalid parameters"
    }

    @swagger.operation(
    summary='Rewards report',
    notes='Rewards report',
    responseClass='RewardsResponse',
    nickname='rewards',
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
            "description": 'Filter by user location related to the reward (Lat,lon,Km)',
            "required": False,
            "dataType": "string"
        }

    ],
    responseMessages=[invalid_input])
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the Rewards Report

        Descripción de los valores devueltos:

        <strong>renuncias</strong>: Número de cofinanciadores que renuncian a recompensa
        <strong>perc-renuncias</strong>: % cofinanciadores que renuncian a recompensa
        <strong>favorite-rewards</strong>: Tipo de recompensa más utilizada en proyectos exitosos. Nota: no le afecta el filtro location.

        <strong>rewards-between-100-400</strong>: Recompensa elegida de 100 a 400 euros
        <strong>rewards-between-15-30</strong>: Recompensa elegida de 15 a 30 euros
        <strong>rewards-between-30-100</strong>: Recompensa elegida de 30 a 100 euros
        <strong>rewards-less-than-15</strong>: Recompensa elegida de menos de 15 euros
        <strong>rewards-more-than-400</strong>: Recompensa elegida de más de 400 euros

        <strong>rewards_per_amount</strong>:

        Además se añade el campo "filters"
        """
        time_start = time.time()
        func = sqlalchemy.func
        args = self.reqparse.parse_args()

        filters = []
        filters2 = []  # para favorite_reward
        # TODO: Qué fechas coger? creacion, finalizacion?
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
            filters2.append(Invest.date_invested >= args['from_date'])
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
            filters2.append(Invest.date_invested <= args['to_date'])
        if args['project']:
            filters.append(Invest.project.in_(args['project'][0]))
            filters2.append(Invest.project.in_(args['project'][0]))
        if args['node']:
            # FIXME: invest_node o project_node ?
            filters.append(Invest.id == InvestNode.invest_id)
            filters2.append(Project.id == InvestNode.project_id)
            filters.append(InvestNode.project_node.in_(args['node']))
            filters2.append(InvestNode.project_node.in_(args['node']))
        if args['category']:
            try:
                category_id = db.session.query(Category.id).filter(Category.name == args['category']).one()
                category_id = category_id[0]
            except NoResultFound:
                return {"error": "Invalid category"}, 400

            filters.append(Invest.project == ProjectCategory.project)
            filters2.append(Project.id == ProjectCategory.project)
            filters.append(ProjectCategory.category == category_id)
            filters2.append(ProjectCategory.category == category_id)
        if args['location']:
            # Filtra por la localización del usuario que elige la recompensa
            # No hace falta filters2, ya que ese filtra por proyecto, no por usuario

            location = args['location'].split(",")
            if len(location) != 3:
                return {"error": "Invalid parameter: location"}, 400

            from geopy.distance import VincentyDistance
            latitude, longitude, radius = location

            radius = int(radius)
            if radius > 500 or radius < 0:
                return {"error": "Radius must be a value between 0 and 500 Km"}, 400

            locations = db.session.query(Location.id, Location.lat, Location.lon).all()
            locations = filter(lambda l: VincentyDistance((latitude, longitude), (l[1], l[2])).km <= radius, locations)
            locations_ids = map(lambda l: int(l[0]), locations)

            if locations_ids == []:
                return {"error": "No locations in the specified range"}, 400

            filters.append(Invest.user == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            filters.append(LocationItem.id.in_(locations_ids))

        #
        cofinanciadores = db.session.query(func.distinct(Invest.user)).filter(*filters).count()

        def perc_invest(number):
            if cofinanciadores == 0:
                return 0
            perc = float(number) / cofinanciadores * 100  # %
            return round(perc, 2)

        # - NÚMERO de cofinanciadores que renuncian a recompensa
        # FIXME: No incluir status=2?
        f_renuncias = list(filters)
        f_renuncias.append(Invest.resign == 1)
        f_renuncias.append(Invest.status.in_([0, 1, 3, 4]))
        renuncias = db.session.query(Invest.id).filter(*f_renuncias).count()

        # (seleccionados por cofinanciador)
        # - Porcentaje de cofinanciadores que renuncian a recompensa
        perc_renuncias = perc_invest(renuncias)

        #
        f_recomp_dinero = list(filters)
        f_recomp_dinero.append(Reward.id != None)
        f_recomp_dinero.append(or_(Invest.resign == None, Invest.resign == 0))

        # OJO: Como en reporting.php, no filtra por proyectos publicados
        # - Recompensa elegida de menos de 15 euros
        f_recomp_dinero15 = list(f_recomp_dinero)
        f_recomp_dinero15.append(Reward.amount < 15)
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero15).group_by(Reward.id).subquery()
        recomp_dinero15 = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()
        if recomp_dinero15 is None:
            recomp_dinero15 = 0

        # - Recompensa elegida de 15 a 30 euros
        f_recomp_dinero30 = list(f_recomp_dinero)
        f_recomp_dinero30.append(Reward.amount.between(15, 30))
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero30).group_by(Reward.id).subquery()
        recomp_dinero30 = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()
        if recomp_dinero30 is None:
            recomp_dinero30 = 0

        # - Recompensa elegida de 30 a 100 euros
        f_recomp_dinero100 = list(f_recomp_dinero)
        f_recomp_dinero100.append(Reward.amount.between(30, 100))
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero100).group_by(Reward.id).subquery()
        recomp_dinero100 = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()
        if recomp_dinero100 is None:
            recomp_dinero100 = 0

        # - Recompensa elegida de 100 a 400 euros
        f_recomp_dinero400 = list(f_recomp_dinero)
        f_recomp_dinero400.append(Reward.amount.between(100, 400))
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero400).group_by(Reward.id).subquery()
        recomp_dinero400 = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()
        if recomp_dinero400 is None:
            recomp_dinero400 = 0

        # - Recompensa elegida de más de 400 euros
        f_recomp_dinero400mas = list(f_recomp_dinero)
        f_recomp_dinero400mas.append(Reward.amount > 400)
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero400).group_by(Reward.id).subquery()
        recomp_dinero400mas = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()
        if recomp_dinero400mas is None:
            recomp_dinero400mas = 0

        # - Tipo de recompensa más utilizada en proyectos exitosos
        # FIXME: Date: Project.published
        f_favorite_reward = list(filters2)
        f_favorite_reward.append(Reward.type == 'individual')
        favorite_reward = db.session.query(Reward.icon, func.count(Reward.project).label('uses'))\
                                .join(Project, and_(Project.id == Reward.project, Project.status.in_([4, 5])))\
                                .filter(*f_favorite_reward).group_by(Reward.icon).order_by(desc('uses')).all()

        res = {'renuncias': renuncias, 'perc-renuncias': perc_renuncias,
                'rewards-per-amount': {'rewards-less-than-15': recomp_dinero15,
                    'rewards-between-15-30': recomp_dinero30, 'rewards-between-30-100': recomp_dinero100,
                    'rewards-between-100-400': recomp_dinero400, 'rewards-more-than-400': recomp_dinero400mas},
                'favorite-rewards': favorite_reward}

        res['time-elapsed'] = time.time() - time_start
        res['filters'] = {}
        for k, v in args.items():
            if v is not None:
                res['filters'][k] = v

        return jsonify(res)
