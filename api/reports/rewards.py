# -*- coding: utf-8 -*-

from flask.ext.restful import Resource

class RewardsAPI(Resource):

    def __init__(self):
        super(RewardsAPI, self).__init__()

    def get(self):

        # (seleccionados por cofinanciador)
        # - Porcentaje de cofinanciadores que renuncian a recompensa
        # - NÚMERO de cofinanciadores que renuncian a recompensa
        # - Recompensa elegida de menos de 15 euros
        # - Recompensa elegida de 15 a 30 euros
        # - Recompensa elegida de 30 a 100 euros
        # - Recompensa elegida de 100 a 400 euros
        # - Recompensa elegida de más de 400 euros
        # - Tipo de recompensa más utilizada en proyectos exitosos
        pass
