# -*- coding: utf-8 -*-

from flask.ext.restful import Resource

class CommunityAPI(Resource):

    def __init__(self):
        super(CommunityAPI, self).__init__()

    def get(self):

        # - Número total de usuarios formados en Goteo (num de proyectos enviados a revisión + inscrito talleres )
        # - Número total de usuarios
        # - Porcentaje (antes numero) de usuarios que se han dado de baja
        # - Número de cofinanciadores
        # - NEW Porcentaje de usuarios cofinanciadores
        # - Cofinanciadores que colaboran
        # - Multi-Cofinanciadores (a más de 1 proyecto)
        # - NEW Porcentaje de Multi-Cofinanciadores (a más de 1 proyecto)
        # - Cofinanciadores usando PayPal
        # - Multi-Cofinanciadores usando PayPal
        # - Número de colaboradores
        # - Media de cofinanciadores por proyecto exitoso
        # - Media de colaboradores por proyecto
        # - Núm. impulsores que cofinancian a otros
        # - Núm. impulsores que colaboran con otros

        # - 1ª Categoría con más usuarios interesados
        # - Porcentaje de usuarios en esta 1ª
        # - 2ª Categoría con más usuarios interesados
        # - Porcentaje de usuarios en esta 2ª
        # - Top 10 Cofinanciadores (REVISAR como sacamos estos datos, excepto admines)
        # - Top 10 Cofinanciadores con más caudal (más generosos) excluir usuarios convocadores Y ADMINES
        # - Top 10 colaboradores
        pass
