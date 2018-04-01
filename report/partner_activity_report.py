# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta


class ContactActivityReport(models.Model):
    """ CRM Lead Analysis """

    _name = "partner.activity.report"
    _auto = False
    _description = "Calendar Activity Analysis"
    _rec_name = 'id'

    start = fields.Datetime('Date Start', readonly=True)
    stop = fields.Datetime('Date Stop', readonly=True)
    user_id = fields.Many2one('res.users', 'Created By', readonly=True)
    description = fields.Char('Description', readonly=True)
    event_type_activity = fields.Many2one('mail.activity.type', 'Activity Type', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Contact/Customer')
    business_developer_id = fields.Many2one('res.users', 'Business Developer', readonly=True)
    state = fields.Selection([
        ('needsAction', 'Needs Action'),
        ('tentative', 'Uncertain'),
        ('declined', 'Declined'),
        ('accepted', 'Accepted')], 'State')
    category = fields.Selection([
        ('default', 'Other')], default='default',
        string='Category')

    def _select(self):
        return """
        
            with users as ( 
                select u.id,r.calendar_event_id from calendar_event_res_partner_rel r, res_users u where u.partner_id=r.res_partner_id
                )
            , partners as (
                select r.res_partner_id ,r.calendar_event_id from calendar_event_res_partner_rel r where not exists ( select partner_id from res_users u where u.partner_id=r.res_partner_id)
                )
            SELECT
                distinct m.id,
                m.event_type_activity,
                m.user_id,
                m.start,
                m.stop,
                m.description,
                m.state,
                t.category,
                u.id as business_developer_id,
                p.res_partner_id as partner_id
 
                
                
        """

    def _from(self):
        return """
            FROM calendar_event_res_partner_rel r ,  users u, partners p, calendar_event AS m
        """

    def _join(self):
        return """
            
            JOIN mail_activity_type AS t ON m.event_type_activity = t.id
        """

    def _where(self):
        return """
            WHERE
                m.event_type_activity IS NOT NULL
                AND  u.calendar_event_id=p.calendar_event_id 
                AND  u.calendar_event_id=m.id
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
