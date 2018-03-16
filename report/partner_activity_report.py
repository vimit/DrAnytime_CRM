# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned')], 'State',
        compute='_compute_state', store=True)

    @api.depends('date_deadline')
    def _compute_state(self):
        today = date.today()
        for record in self.filtered(lambda activity: activity.date_deadline):
            date_deadline = fields.Date.from_string(record.date_deadline)
            diff = (date_deadline - today)
            if diff.days == 0:
                record.state = 'today'
            elif diff.days < 0:
                record.state = 'overdue'
            else:
                record.state = 'planned'

class ContactActivityReport(models.Model):
    """ CRM Lead Analysis """

    _name = "contact.activity.report"
    _auto = False
    _description = "CRM Activity Analysis"
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


    def _select(self):
        return """
            SELECT
                m.id,
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
            FROM mail_activity AS m
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

