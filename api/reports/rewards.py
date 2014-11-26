# -*- coding: utf-8 -*-
from model import app, db
from model import Invest, Reward, InvestReward

from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger

from sqlalchemy import and_, or_


class ModelClass():
    pass


@swagger.model
class RewardsAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('limit', type=int, default=10)
        self.reqparse.add_argument('project', type=str, action='append')
        super(RewardsAPI, self).__init__()

    @swagger.operation(
    notes='Rewards report',
    responseClass=ModelClass.__name__,
    nickname='upload',
    responseMessages=[
        {
          "code": 200,
          "message": "OK"
        },
        {
          "code": 404,
          "message": "Not found"
        }
      ]
    )
    def get(self):
        func = sqlalchemy.func
        args = self.reqparse.parse_args()

        print args
        app.logger.debug('projects')
        app.logger.debug(args['project'])

        filters = []
        # TODO: Qué fechas coger? creacion, finalizacion?
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
        if args['project']:
            filters.append(Invest.project.in_(args['project'][0]))
        limit = args['limit']

        app.logger.debug('start sql')

        # - NÚMERO de cofinanciadores que renuncian a recompensa
        # FIXME: Invest.id not in InvestReWardTable.invest
        f_renuncias = list(filters)
        f_renuncias.append(Invest.resign == 1)
        f_renuncias.append(Invest.status.in_([0, 1, 3, 4]))
        renuncias = db.session.query(func.count(Invest.id)).filter(*f_renuncias).count()

        # (seleccionados por cofinanciador)
        # - Porcentaje de cofinanciadores que renuncian a recompensa
        cofinanciadores = db.session.query(func.distinct(Invest.user)).filter(*filters).count()
        perc_renuncias = float(renuncias) / cofinanciadores * 100

        f_recomp_dinero = list(filters)
        f_recomp_dinero.append(Reward.id != None)
        f_recomp_dinero.append(or_(Invest.resign == None, Invest.resign == 0))

        # - Recompensa elegida de menos de 15 euros
        f_recomp_dinero15 = list(f_recomp_dinero)
        f_recomp_dinero15.append(Reward.amount < 15)
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero15).group_by(Reward.id).subquery()
        recomp_dinero15 = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()

        # - Recompensa elegida de 15 a 30 euros
        f_recomp_dinero30 = list(f_recomp_dinero)
        f_recomp_dinero30.append(Reward.amount.between(15, 30))
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero30).group_by(Reward.id).subquery()
        recomp_dinero30 = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()

        # - Recompensa elegida de 30 a 100 euros
        f_recomp_dinero100 = list(f_recomp_dinero)
        f_recomp_dinero100.append(Reward.amount.between(30, 100))
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero100).group_by(Reward.id).subquery()
        recomp_dinero100 = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()

        # - Recompensa elegida de 100 a 400 euros
        f_recomp_dinero400 = list(f_recomp_dinero)
        f_recomp_dinero400.append(Reward.amount.between(100, 400))
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero400).group_by(Reward.id).subquery()
        recomp_dinero400 = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()

        # - Recompensa elegida de más de 400 euros
        f_recomp_dinero400mas = list(f_recomp_dinero)
        f_recomp_dinero400mas.append(Reward.amount > 400)
        _recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero400).group_by(Reward.id).subquery()
        recomp_dinero400mas = db.session.query(func.sum(_recomp_dinero.c.amourew)).scalar()

        # - Tipo de recompensa más utilizada en proyectos exitosos
        # TODO
        # success_projects. Tipo ? Qué tipos hay?

        app.logger.debug('end check')

        return jsonify({'renuncias': renuncias, 'perc-renuncias': perc_renuncias,
                        'recomp-dinero15': recomp_dinero15, 'recomp-dinero30': recomp_dinero30,
                        'recomp-dinero100': recomp_dinero100, 'recomp-dinero400': recomp_dinero400,
                        'recomp-dinero400mas': recomp_dinero400mas})
