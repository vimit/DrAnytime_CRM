# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, datetime, timedelta, time
import dateutil.parser

from dateutil.relativedelta import relativedelta

class SubscriptionForecast(models.Model):
    """ Subscription Forecast Report Analysis """

    _name = "subscription.forecast"
    _description = "Subscription Forecast Report Analysis "

    subscription_id = fields.Many2one('sale.subscription', 'Subscription')
    name = fields.Char('Name', related="subscription_id.name", store=True)

    recurring_amount_total = fields.Float('Total',related="subscription_id.recurring_amount_total", store=True)
    date = fields.Date('Date Invoice')


    @api.constrains('subscription_id')
    def _check_subscrition(self):
        for sub in self:
            if not sub.subscription_id:
                sub.unlink()

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    subscription_forecast_ids = fields.One2many('subscription.forecast','subscription_id','Subscription Forecast'
                                                , compute='subscription_forecast_report',store=True)
    @api.multi
    @api.depends('recurring_next_date')
    def subscription_forecast_report(self):
        if self.state == 'open':
            sub_forecast = []
            today = datetime.today().strftime('%Y-%m-%d')
            today_year = datetime.strptime(today, '%Y-%m-%d').strftime('%y')

            date_subscription = self.recurring_next_date
            date_subscription = str(date_subscription)
            months = datetime.strptime(date_subscription, '%Y-%m-%d').strftime('%m')
            years = datetime.strptime(date_subscription, '%Y-%m-%d').strftime('%y')
            n = self.template_id.recurring_interval
            if years == today_year:
                sub_forecast.append((0, 0, {
                    'subscription_id': self.id,
                    'date': date_subscription,

                }))

            while int(months) < 12 and years == today_year :
                date_subscription = (datetime.strptime(date_subscription, '%Y-%m-%d') + relativedelta(months=n)).strftime('%Y-%m-%d')
                months = datetime.strptime(date_subscription, '%Y-%m-%d').strftime('%m')
                years =  datetime.strptime(date_subscription, '%Y-%m-%d').strftime('%y')
                print('date_subscription-----',date_subscription)
                if years == today_year :
                    sub_forecast.append((0, 0, {
                        'subscription_id': self.id,
                        'date': date_subscription,

                    }))
            self.subscription_forecast_ids = sub_forecast

    @api.multi
    def process_forecast(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['sale.subscription'].browse(active_ids):
            record.subscription_forecast_report()