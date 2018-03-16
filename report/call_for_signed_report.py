# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta



class CallforSignedTrackReport(models.Model):
    """ Stage track change Analysis """

    _name = "signed.called.track.report"
    _auto = False
    _description = "Stage track Analysis"
    _rec_name = 'id'

    field = fields.Char('Changed Field', readonly=True)

    date = fields.Datetime('Date', readonly=True)
    author_id = fields.Many2one('res.partner', 'Created By', readonly=True)

    # user_id = fields.Many2one('res.users', 'Assigned a', readonly=True)
    stage_id = fields.Many2one('crm.stage', 'Actual Stage', readonly=True)
    country_id = fields.Many2one('res.country', 'Country', readonly=True)
    state_id = fields.Many2one('res.country.state', 'State')
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer/contact', readonly=True)
    stage_signed = fields.Char('Stage SIGNED AGREEMENT')
    called_signed  = fields.Float('Call signed rate')



    def _select(self):
        return """
        with ftof_values as ( select id,create_date from mail_message where mail_activity_type_id=2)
        SELECT
                m.id as id,
                m.field,
                m.new_value_char as stage_signed,
                mes.author_id as author_id,
                mes.date,
                l.id as partner_id,
                l.country_id,
                l.company_id,
                l.state_id,
                l.stage_id,
                100*count(m.id)/count(f.id) as called_signed              
                
        """


    def _from(self):
        return """
            FROM ftof_values AS f, mail_tracking_value AS m
        """

    def _join(self):
        return """
            JOIN mail_message AS mes ON mes.id = m.mail_message_id
            JOIN res_partner AS l ON mes.res_id = l.id
        """

    def _where(self):
        return """
            WHERE
               EXTRACT(YEAR FROM m.create_date)= EXTRACT(YEAR FROM f.create_date) 
               AND EXTRACT(MONTH FROM m.create_date)= EXTRACT(MONTH FROM f.create_date)
               
               and mes.model = 'res.partner' AND m.field ='stage_id' AND new_value_char = 'SIGNED AGREEMENT' 
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
                f.id
            
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
                %s
            )
        """ % (self._table, self._select(), self._from(), self._join(), self._where(), self._group())
        )

