# -*- coding: utf-8 -*-

from flask.ext.restful import Resource

class ProjectsAPI(Resource):

    def __init__(self):
        super(ProjectsAPI, self).__init__()

    def get(self):

        # - Proyectos enviados a revisión (renombrar Proyectos recibidos)
        # - Proyectos publicados
        # - Proyectos exitosos (llegan al mínimo pueden estar en campaña)
        # % exito exitosos
        # -(nuevo) proyectos exitosos con campaña finalizada
        # _(nuevo)% éxito campañas finalizadas
        # - Proyectos archivados Renombrar  por Proyectos Fallidos
        # - Porcentaje media de recaudación conseguida por proyectos exitosos
        # - (NUEVOS)10 Campañas con más cofinanciadores
        # - 10 Campañas con más colaboraciones
        # - 10 Campañas que han recaudado más dinero
        # - Campañas más rápidas en conseguir el mínimo (NUEVO)
        # - Media de posts proyecto exitoso

        pass
