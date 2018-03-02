# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api
from datetime import date, datetime, timedelta



class ContactReport(models.Model):
    """ CRM Lead Analysis """

    _name = "contact.sub.report"
    _auto = False
    _description = "CRM contact Analysis"
    _rec_name = 'id'

    state_id = fields.Many2one('res.country.state', 'Fed. States', readonly=True)
    stage_id = fields.Many2one('crm.stage', 'Actual Stage', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer/Contact', readonly=True)
    business_developer_id = fields.Many2one('res.users', 'Business Developer', readonly=True)
    intern_ids = fields.Many2one('hr.intern', 'Intern')

    subscription_month = fields.Float('Monthly subscription', readonly=True)
    subscription_commitment = fields.Selection(
        [('monthly', 'Monthly'), ('trimestrial', 'Trimestrial'), ('semestrial', 'Semestrial'), ('yearly', 'Yearly')],
        'Commitment', readonly=True)
    subscription_upfront_payment = fields.Selection(
        [('no', 'NO'), ('trimestrial', 'Trimestrial'), ('semestrial', 'Semestrial'), ('yearly', 'Yearly')],
        'Upfront Payment', readonly=True)
    subscription_upfront_turnover = fields.Float('Upfront turnover', readonly=True)

    tsucreate_date = fields.Datetime('Upfront turnover Update Date ', readonly=True)
    tsmcreate_date = fields.Datetime('Monthly subscription Update Date', readonly=True)
    tsufield_name = fields.Char('Upfront turnover', readonly=True)
    tsmfield_name = fields.Char('Monthly subscription', readonly=True)

    # field_name = fields.Selection([('subscription_upfront_turnover','subscription_upfront_turnover'),('subscription_upfront_payment','subscription_upfront_payment'),('subscription_commitment','subscription_commitment'),('subscription_month','subscription_month')],'Value updated')

    def _select(self):
        return """
             SELECT
                l.id as id,
                l.stage_id,
                l.state_id,
                l.business_developer_id,
                l.intern_ids,
                l.subscription_month,
                l.subscription_commitment,
                l.subscription_upfront_payment,
                l.subscription_upfront_turnover,                
                l.id as partner_id,
                tsu.field as tsufield_name,
                tsm.field as tsmfield_name,
                tsu.create_date as tsucreate_date,
                tsm.create_date as tsmcreate_date
                
                
 
                
                
        """


    def _from(self):
        return """
            FROM  res_partner AS l
        """

    def _join(self):
        return """
            Left JOIN (select max(mes.date) as create_date, m.field, mes.res_id as res_id
            from mail_tracking_value m, mail_message mes
            where  field = 'subscription_month' and mes.id = m.mail_message_id and mes.model = 'res.partner' 
            group by field,mes.res_id
            ) as tsm ON l.id = tsm.res_id

            left JOIN (select max(mes.date) as create_date, m.field, mes.res_id as res_id
            from mail_tracking_value m, mail_message mes
            where  field = 'subscription_upfront_turnover' and mes.id = m.mail_message_id and mes.model = 'res.partner' 
            group by field,mes.res_id
            ) as tsu ON l.id = tsu.res_id
        """
    def _where(self):
        return """
            WHERE
                  tsu.field is not null or tsm.field is not null
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

