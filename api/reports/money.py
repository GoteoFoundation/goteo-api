# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger

from api.models.call import Call
from api.models.project import Project
from api.models.invest import Invest
from api.decorators import ratelimit, requires_auth

from api.base_endpoint import BaseList, Response

func = sqlalchemy.func


@swagger.model
class MoneyResponse(Response):
    """MoneyResponse"""

    resource_fields = {
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

    required = resource_fields.keys()


class MoneyAPI(BaseList):
    """Get Money Statistics"""

    @swagger.operation(
        notes='Money report',
        nickname='money',
        responseClass=MoneyResponse.__name__,
        parameters=BaseList.INPUT_FILTERS,
        responseMessages=BaseList.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the Money Report
        <a href="http://developers.goteo.org/doc/reports#money">developers.goteo.org/doc/reports#money</a>
        """
        ret = self._get()
        return ret.response()

    def _get(self):
        """Get()'s method dirty work"""
        time_start = time.time()

        #remove not used arguments
        args = self.parse_args(remove=('page','limit'))

        res = MoneyResponse(
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
                # "matchfund-amount"        : Invest.pledged_total(method=Invest.METHOD_DROP, **args),
                # CONVOCATORIA y aportes individuales
                "matchfund-amount"        : Invest.pledged_total(is_call=True, **args),
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

