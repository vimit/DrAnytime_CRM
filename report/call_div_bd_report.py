# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta


class CallDivBDReport(models.Model):
    """ Stage track change Analysis """

    _name = "call.div.bd.report"
    _auto = False
    _description = "Stage track Analysis"
    _rec_name = 'id'

    date = fields.Selection(
        selection=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'),
                   (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')],
        string='Month')
    year = fields.Char('Year')
    call_bd = fields.Float('#Call/BD', readonly=True)

    def _select(self):
        return """

            SELECT
            v.id,
            v.name as year,
            v.target_month as date,
            (
             ( select count(p.id)
                from  call_pitch p
                where
                 EXTRACT(YEAR FROM p.date_pitch)= cast(v.name as int) 
                    and EXTRACT(MONTH FROM p.date_pitch)=v.target_month ) 
                    
                    
                    +
                    ( select count(a.id)
                    from call_attempt a
                    where
                    EXTRACT(YEAR FROM a.date_attempt)= cast(v.name as int) 
                    and EXTRACT(MONTH FROM a.date_attempt)=v.target_month
                        
                        ) /v.target_bd)as call_bd
        """

    def _from(self):
        return """
           FROM target_report AS v
        """

    def _where(self):
        return """
            Where
            v.target_bd != 0
             """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s

            )
        """ % (self._table, self._select(), self._from(), self._where())
                         )
