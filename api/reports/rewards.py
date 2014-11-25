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

        # (seleccionados por cofinanciador)
        # - Porcentaje de cofinanciadores que renuncian a recompensa
        # TODO

        # - NÚMERO de cofinanciadores que renuncian a recompensa
        # TODO
        #Invest.id not in InvestReWardTable.invest

        # - Recompensa elegida de menos de 15 euros
        # TODO
        #Reward.amount < 15

        # - Recompensa elegida de 15 a 30 euros
        # TODO
        #15 < Reward.amount < 30

        # - Recompensa elegida de 30 a 100 euros
        # TODO
        #30 < Reward.amount < 100

        # - Recompensa elegida de 100 a 400 euros
        # TODO
        #100 < Reward.amount < 400

        # - Recompensa elegida de más de 400 euros
        # TODO
        #Reward.amount > 400

        # - Tipo de recompensa más utilizada en proyectos exitosos
        # TODO
        # success_projects. Tipo ? Qué tipos hay?

        app.logger.debug('end check')

        return jsonify({'rewards': 'yes'})
