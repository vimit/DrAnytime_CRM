# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta


class BDActivityReport(models.Model):
    """ CRM Lead Analysis """

    _name = "contact.activity.div.bd.report"
    _auto = False
    _description = "CRM Activity Analysis/BD"
    _rec_name = 'id'

    count_div_bd = fields.Float("#Nbr/BD")
    # count_activities = fields.Float("#Activities")
    date = fields.Datetime('Date', readonly=True)

    def _select(self):
        return """
        with values as ( 
                select id,name, target_month,target_bd from target_report 
                )
        SELECT
                    c.id,
                    c.start as date,
                    ((select count(e.id) from calendar_event e, mail_activity_type t 
                         where EXTRACT(YEAR FROM e.start)= EXTRACT(YEAR FROM c.create_date) 
                            AND EXTRACT(MONTH FROM e.start)= EXTRACT(MONTH FROM c.create_date) 
                            AND  t.id=e.event_type_activity and t.category='meeting')/v.target_bd) as count_div_bd
            """

    def _from(self):
        return """
            FROM  values AS v, calendar_event AS c
        """

    def _where(self):
        return """
            WHERE
               v.target_bd !=0 
                AND EXTRACT(YEAR FROM c.start)= cast(v.name as int) 
                and EXTRACT(MONTH FROM c.start)=v.target_month
                and (select count(e.id) from calendar_event e, mail_activity_type t 
                         where EXTRACT(YEAR FROM e.start)= EXTRACT(YEAR FROM c.create_date) 
                            AND EXTRACT(MONTH FROM e.start)= EXTRACT(MONTH FROM c.create_date) 
                            AND  t.id=e.event_type_activity and t.category='meeting') != 0
                
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

