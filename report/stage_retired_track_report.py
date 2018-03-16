# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta



class StageTrackReport(models.Model):
    """ Stage track change Analysis """

    _name = "stage.retired.track.report"
    _auto = False
    _description = "Stage Retired track Analysis"
    _rec_name = 'id'

    field = fields.Char('Changed Field', readonly=True)

    date = fields.Datetime('Date', readonly=True)
    author_id = fields.Many2one('res.partner', 'Created By', readonly=True)

    # user_id = fields.Many2one('res.users', 'Assigned a', readonly=True)
    stage_id = fields.Many2one('crm.stage', 'Actual Stage', readonly=True)
    country_id = fields.Many2one('res.country', 'Country', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer/contact', readonly=True)
    stage_retired = fields.Char('Stage Retired')



    def _select(self):
        return """
            SELECT
                m.id,
                m.field,
                m.new_value_char as stage_retired,
                mes.author_id as author_id,
                mes.date,
                l.id as partner_id,
                l.country_id,
                l.company_id,
                l.stage_id
                
                
        """


    def _from(self):
        return """
            FROM mail_tracking_value AS m
        """

    def _join(self):
        return """
            JOIN mail_message AS mes ON mes.id = m.mail_message_id
            JOIN res_partner AS l ON mes.res_id = l.id
        """

    def _where(self):
        return """
            WHERE
                mes.model = 'res.partner' AND m.field ='stage_id' AND new_value_char = 'LOST PAYING' 
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._join(), self._where())
        )

