# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta


class CallforSignedTrackReport(models.Model):
    """ Stage track change Analysis """

    _name = "signed.called.track.report"
    _auto = False
    _description = "Stage track Analysis"
    _rec_name = 'id'

    date = fields.Datetime('Date', readonly=True)
    called_signed = fields.Float('Call signed rate', group_operator='avg')

    def _select(self):
        return """
       
            SELECT
            c.id,
            c.create_date as date,
            (100* (select count(id) 
                   from mail_tracking_value m
                    where field ='stage_id' AND new_value_char = 'SIGNED AGREEMENT' 
                    and EXTRACT(YEAR FROM m.create_date)= EXTRACT(YEAR FROM c.create_date) 
                    AND EXTRACT(MONTH FROM m.create_date)= EXTRACT(MONTH FROM c.create_date) )
                /
               (( select count(p.id)
from  call_pitch p
where
 ( EXTRACT(YEAR FROM p.date_pitch)= EXTRACT(YEAR FROM c.create_date) 
                    AND EXTRACT(MONTH FROM p.date_pitch)= EXTRACT(MONTH FROM c.create_date) )) 
                    +
                    ( select count(a.id)
from call_attempt a
where
EXTRACT(YEAR FROM a.date_attempt)= EXTRACT(YEAR FROM c.create_date) 
                    AND EXTRACT(MONTH FROM a.date_attempt)= EXTRACT(MONTH FROM c.create_date)) ))as called_signed
        """

    def _from(self):
        return """
           FROM mail_tracking_value AS c
        """

    def _where(self):
        return """
            WHERE
              (( select count(p.id)
from  call_pitch p
where
 ( EXTRACT(YEAR FROM p.date_pitch)= EXTRACT(YEAR FROM c.create_date) 
                    AND EXTRACT(MONTH FROM p.date_pitch)= EXTRACT(MONTH FROM c.create_date) )) 
                    +
                    ( select count(a.id)
from call_attempt a
where
EXTRACT(YEAR FROM a.date_attempt)= EXTRACT(YEAR FROM c.create_date) 
                    AND EXTRACT(MONTH FROM a.date_attempt)= EXTRACT(MONTH FROM c.create_date)) ) !=0
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
