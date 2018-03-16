# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta


class ContactActivityReport(models.Model):
    """ CRM Lead Analysis """

    _name = "contact.div.bd.report"
    _auto = False
    _description = "Contact Activity Analysis/BD"
    _rec_name = 'id'

    create_date = fields.Datetime('Created On', readonly=True)
    user_id = fields.Many2one('res.users', 'Contact Created By', readonly=True)
    stage_id = fields.Many2one('crm.stage', 'Stage', readonly=True)
    state_id = fields.Many2one('res.country.state','State')
    business_developer_id = fields.Many2one('res.users', 'Business Developer', readonly=True)
    intern_ids = fields.Many2one('hr.intern', 'Intern')

    count_div_bd = fields.Float("#Nbr/BD")
    count_contact = fields.Float("#Contact")
    tunover_div_bd = fields.Float("Tunover/BD")
    upfront_tunover_contact = fields.Float("Upfront Tunover/BD")
    subscription_commitment = fields.Selection(
        [('monthly', 'Monthly'), ('trimestrial', 'Trimestrial'), ('semestrial', 'Semestrial'), ('yearly', 'Yearly')],
        'Commitment', track_visibility='onchange')
    subscription_upfront_payment = fields.Selection(
        [('no', 'NO'), ('trimestrial', 'Trimestrial'), ('semestrial', 'Semestrial'), ('yearly', 'Yearly')],
        'Upfront Payment', track_visibility='onchange')
    subscription_month = fields.Float('Monthly subscription')
    subscription_upfront_turnover = fields.Float('Upfront turnover')

    def _select(self):
        return """
        with values as ( select id,name, target_month,target_bd from target_report )
            SELECT
                l.id,
                count(l.id)/v.target_bd as count_div_bd , 
                count(l.id) as count_contact,
                l.create_uid as user_id,
                l.stage_id,
                l.create_date ,
                l.state_id,
                l.business_developer_id,
                l.intern_ids,
                l.subscription_month,
                l.subscription_upfront_turnover,
                l.subscription_commitment,
                l.subscription_month/v.target_bd as tunover_div_bd,
                l.subscription_upfront_turnover/v.target_bd as upfront_tunover_contact 
    
                
                
        """


    def _from(self):
        return """
            FROM res_partner AS l, values AS v
        """

    def _where(self):
        return """
            WHERE
                EXTRACT(YEAR FROM l.create_date)= cast(v.name as int) and EXTRACT(MONTH FROM l.create_date)=v.target_month
            
        """
    def _group(self):
        return """
            GROUP BY
                v.target_bd,
                v.target_month,
                l.id,
                l.stage_id,
                l.state_id,
                l.business_developer_id,
                l.intern_ids,
                l.subscription_month,
                l.subscription_commitment,
                l.subscription_upfront_payment,
                l.subscription_upfront_turnover,
                l.subscription_upfront_turnover
             
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
        """ % (self._table, self._select(), self._from(), self._where(), self._group())
        )

