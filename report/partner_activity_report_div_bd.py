# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta


class BDActivityReport(models.Model):
    """ CRM Lead Analysis """

    _name = "contact.activity.div.bd.report"
    _auto = False
    _description = "CRM Activity Analysis/BD"
    _rec_name = 'id'

    date_deadline = fields.Date('Date', readonly=True)
    author_id = fields.Many2one('res.partner', 'Created By', readonly=True)
    user_id = fields.Many2one('res.users', 'Contact Created By', readonly=True)
    summary = fields.Char('Summary', readonly=True)
    activity_type_id = fields.Many2one('mail.activity.type', 'Activity Type', readonly=True)
    country_id = fields.Many2one('res.country', 'Country', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    stage_id = fields.Many2one('crm.stage', 'Stage', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer/contact', readonly=True)
    state_id = fields.Many2one('res.country.state', 'State')

    business_developer_id = fields.Many2one('res.users', 'Business Developer', readonly=True)
    intern_ids = fields.Many2one('hr.intern', 'Intern')
    state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned')], 'State')
    category = fields.Selection([
        ('default', 'Other')], default='default',
        string='Category')

    count_div_bd = fields.Float("#Nbr/BD")
    count_activities = fields.Float("#Activities")


    def _select(self):
        return """
        with values as ( select id,name, target_month,target_bd from target_report )
            SELECT
                m.id,
                count(m.id)/v.target_bd as count_div_bd , 
                count(m.id) as count_activities,
                m.activity_type_id,
                m.user_id as author_id,
                m.date_deadline,
                m.summary,
                m.state,
                t.category,
                l.id as partner_id,
                l.create_uid as user_id,
                l.country_id,
                l.company_id,
                l.stage_id,
                l.business_developer_id,
                l.intern_ids,
                l.state_id
 
                
                
        """


    def _from(self):
        return """
            FROM values AS v, mail_activity AS m
        """

    def _join(self):
        return """
            JOIN res_partner AS l ON m.res_id = l.id
            JOIN mail_activity_type AS t ON m.activity_type_id = t.id
        """

    def _where(self):
        return """
            WHERE
                m.res_model = 'res.partner' AND m.activity_type_id IS NOT NULL
                AND EXTRACT(YEAR FROM m.date_deadline)= cast(v.name as int) and EXTRACT(MONTH FROM m.date_deadline)=v.target_month
            
        """
    def _group(self):
        return """
            GROUP BY
             v.target_bd,
             v.target_month,
             m.id,
             m.activity_type_id,
             m.user_id,
             m.date_deadline,
             m.summary,
             m.state,
             t.category,
             l.id,
             l.create_uid,
             l.country_id,
             l.company_id,
             l.stage_id,
             l.business_developer_id,
             l.intern_ids
             
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

