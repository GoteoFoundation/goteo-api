# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields

from goteoapi.decorators import ratelimit, requires_auth
from goteoapi.base_resources import BaseList, Response

money_resource_fields = {
    "average-failed"                : fields.Float,
    "average-donation"              : fields.Float,
    "average-donation-paypal"       : fields.Float,
    "average-minimum"               : fields.Float,
    "average-received"              : fields.Float,
    "average-second-round"          : fields.Float,
    "matchfund-amount"              : fields.Integer,
    "matchfundpledge-amount"        : fields.Integer,
    "cash-amount"                   : fields.Integer,
    "pledged"                       : fields.Integer,
    "percentage-pledged-failed"     : fields.Float,
    "percentage-pledged-successful" : fields.Float,
    "refunded"                      : fields.Integer,
    "fee-amount"                    : fields.Float,
    "paypal-amount"                 : fields.Integer,
    "creditcard-amount"             : fields.Integer
}


class MoneyAPI(BaseList):
    """Money Statistics"""

    @requires_auth
    @ratelimit()
    def get(self):
        """
        Money Stats API
        <a href="http://developers.goteo.org/doc/reports#money">developers.goteo.org/doc/reports#money</a>
        This resource returns statistics about money in Goteo.
        ---
        tags:
            - money_reports
        definitions:
            - schema:
                id: Money
                properties:
                    average-failed:
                        type: number
                    average-donation:
                        type: number
                    average-donation-paypal:
                        type: number
                    average-minimum:
                        type: number
                    average-received:
                        type: number
                    average-second-round:
                        type: number
                    matchfund-amount:
                        type: integer
                    matchfundpledge-amount:
                        type: integer
                    cash-amount:
                        type: integer
                    pledged:
                        type: integer
                    percentage-pledged-failed:
                        type: number
                    percentage-pledged-successful:
                        type: number
                    refunded:
                        type: integer
                    fee-amount:
                        type: number
                    paypal-amount:
                        type: integer
                    creditcard-amount:
                        type: integer

        parameters:
            - in: query
              type: string
              name: node
              description: Filter by individual node(s). Multiple nodes can be specified
              collectionFormat: multi
            - in: query
              name: project
              description: Filter by individual project(s). Multiple projects can be specified
              type: string
              collectionFormat: multi
            - in: query
              name: from_date
              description: Filter from date. Ex. "2013-01-01"
              type: string
              format: date
            - in: query
              name: to_date
              description: Filter until date.. Ex. "2014-01-01"
              type: string
              format: date
            - in: query
              name: category
              description: Filter by project category. Multiple projects can be specified
              type: integer
            - in: query
              name: location
              description: Filter by project location (Latitude,longitude,Radius in Km)
              type: number
              collectionFormat: csv
            - in: query
              name: page
              description: Page number (starting at 1) if the result can be paginated
              type: integer
            - in: query
              name: limit
              description: Page limit (maximum 50 results, defaults to 10) if the result can be paginated
              type: integer
        responses:
            200:
                description: List of available projects
                schema:
                    $ref: '#/definitions/api_reports_money_get_Money'
            400:
                description: Invalid parameters format
        """
        ret = self._get()
        return ret.response()

    def _get(self):
        """Get()'s method dirty work"""
        from goteoapi.calls.models import Call
        from goteoapi.projects.models import Project
        from goteoapi.models.invest import Invest

        time_start = time.time()

        #remove not used arguments
        args = self.parse_args(remove=('page','limit'))

        res = Response(
            starttime = time_start,
            attributes = {
                # Dinero comprometido: Suma recaudada por la plataforma
                "pledged"                 : Invest.pledged_total(**args),
                # "pledged"                 : Project.pledged_total(**args),
                # Perc. medio de recaudación sobre el mínimo recaudado
                # "percentage-pledged-successful"      : Invest.percent_pledged_successful(**args), # <- este metodo filtra por fecha de invest, da numeros negativos
                "percentage-pledged-successful"      : Project.percent_pledged_successful(**args), # <- filtra por fecha de proyecto
                # Perc. dinero compr. medio sobre mínimo',
                # "percentage-pledged-failed"          : Invest.percent_pledged_failed(**args),
                "percentage-pledged-failed"          : Project.percent_pledged_failed(**args),
                # Dinero devuelto (en proyectos archivados)
                "refunded"                : Invest.refunded_total(**args),
                # "refunded"                : Project.refunded_total(**args),
                # Recaudado mediante PayPal
                # TODO: confirmar si hay que quitar devueltos
                "paypal-amount"           : Invest.pledged_total(method=Invest.METHOD_PAYPAL, **args),
                # Recaudado mediante TPV
                "creditcard-amount"       : Invest.pledged_total(method=Invest.METHOD_TPV, **args),
                # # Aportes manuales: recaudado mediante transferencia bancaria directa
                "cash-amount"             : Invest.pledged_total(method=Invest.METHOD_CASH, **args),
                #  Suma recaudada en Convocatorias (Capital riego distribuido + crowd)
                # SOLO CONVOCATORIA:
                "matchfund-amount"        : Invest.pledged_total(method=Invest.METHOD_DROP, **args),
                # CONVOCATORIA y aportes individuales
                # "matchfund-amount"        : Invest.pledged_total(is_call=True, **args),
                # Capital Riego de Goteo (fondos captados de instituciones y empresas destinados a la bolsa de Capital Riego https://goteo.org/service/resources)
                "matchfundpledge-amount"  : Call.pledged_total(**args),
                # Total 8% recaudado por Goteo
                "fee-amount"              : Invest.fee_total(**args),
                # Aporte medio por cofinanciador(micromecenas)
                # OJO: En reporting.php no calcula esto mismo
                "average-donation"        : Invest.average_donation(**args),
                # Aporte medio por cofinanciador(micromecenas) mediante PayPal
                # OJO: En reporting.php no calcula esto mismo
                "average-donation-paypal" : Invest.average_donation(method=Invest.METHOD_PAYPAL, **args),
                # Coste mínimo medio por proyecto exitoso: Presupuesto mínimo medio por proyecto exitoso
                # TODO: ¿parametro location?
                # OJO: En reporting.php no calcula esto mismo
                "average-minimum"         : Project.average_minimum(**args),
                # Recaudación media por proyecto exitoso ( financiado )
                "average-received"        : Project.average_total(status=[Project.STATUS_FUNDED, Project.STATUS_FULFILLED], **args),
                # (Nuevo) Dinero medio solo obtenido en 2a ronda
                "average-second-round"    : Invest.average_second_round(**args),
                # - [Renombrar Dinero compr. medio en proyectos archivados] Dinero recaudado de media en campañas fallidas
                "average-failed"          : Project.average_total(status=[Project.STATUS_UNFUNDED], **args),
                # - [Renombrar]Perc. dinero compr. medio (dinero recaudado de media) sobre mínimo (número del dato anterior)
            },
            filters = args.items()
        )

        return res

