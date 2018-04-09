# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta



class CallFtofTrackReport(models.Model):
    """ Stage track change Analysis """

    _name = "call.ftof.track.report"
    _auto = False
    _description = "Activities track Analysis"
    _rec_name = 'id'

    date = fields.Datetime('Date', readonly=True)
    ftof_div_call = fields.Float('Call to F2F Conversion Rate', group_operator='avg')

    def _select(self):
        return """
       SELECT
        c.id,
        c.start as date,
        (100* (select count(e.id) from calendar_event e
                 where EXTRACT(YEAR FROM e.start)= EXTRACT(YEAR FROM c.start) 
                    AND EXTRACT(MONTH FROM e.start)= EXTRACT(MONTH FROM c.start)   )
                 /
                 (( select count(p.id)
from  call_pitch p
where
 ( EXTRACT(YEAR FROM p.date_pitch)= EXTRACT(YEAR FROM c.start) 
                    AND EXTRACT(MONTH FROM p.date_pitch)= EXTRACT(MONTH FROM c.start) )) 
                    +
                    ( select count(a.id)
from call_attempt a
where
EXTRACT(YEAR FROM a.date_attempt)= EXTRACT(YEAR FROM c.start) 
                    AND EXTRACT(MONTH FROM a.date_attempt)= EXTRACT(MONTH FROM c.start)) ) ) as ftof_div_call  
        """


    def _from(self):
        return """
            from calendar_event AS c
        """


    def _where(self):
        return """
            WHERE
               (( select count(p.id)
from  call_pitch p
where
 ( EXTRACT(YEAR FROM p.date_pitch)= EXTRACT(YEAR FROM c.start) 
                    AND EXTRACT(MONTH FROM p.date_pitch)= EXTRACT(MONTH FROM c.start) )) 
                    +
                    ( select count(a.id)
from call_attempt a
where
EXTRACT(YEAR FROM a.date_attempt)= EXTRACT(YEAR FROM c.start) 
                    AND EXTRACT(MONTH FROM a.date_attempt)= EXTRACT(MONTH FROM c.start)) )!=0
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

