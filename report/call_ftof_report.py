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
        (100* (select count(e.id) from calendar_event e, mail_activity_type t 
                 where t.id=e.event_type_activity and t.category='meeting' and EXTRACT(YEAR FROM e.create_date)= EXTRACT(YEAR FROM c.start) 
                    AND EXTRACT(MONTH FROM e.create_date)= EXTRACT(MONTH FROM c.start)  )
                 /
                 (select count(f.id) from calendar_event f, mail_activity_type t 
                 where t.id=f.event_type_activity and t.name ilike '%call%'  and EXTRACT(YEAR FROM f.create_date)= EXTRACT(YEAR FROM c.start) 
                    AND EXTRACT(MONTH FROM f.create_date)= EXTRACT(MONTH FROM c.start)) ) as ftof_div_call  
        """


    def _from(self):
        return """
            from calendar_event AS c
        """

    def _join(self):
        return """
            JOIN mail_message AS mes ON mes.id = m.mail_message_id
            JOIN res_partner AS l ON mes.res_id = l.id
        """

    def _where(self):
        return """
            WHERE
               (select count(f.id) from calendar_event f, mail_activity_type t 
                 where t.id=f.event_type_activity and t.name ilike '%call%'  and EXTRACT(YEAR FROM f.create_date)= EXTRACT(YEAR FROM c.start) 
                    AND EXTRACT(MONTH FROM f.create_date)= EXTRACT(MONTH FROM c.start))!=0
               """
    def _group(self):
        return """
            GROUP BY
                m.id,
                m.field,
                m.new_value_char,
                mes.author_id,
                mes.date,
                l.id ,
                l.country_id,
                l.company_id,
                l.state_id,
                l.stage_id,
                f.id,
                c.id
            
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

