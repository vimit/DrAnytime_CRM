# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    sent_by_mail = fields.Boolean('Send by paper mail')
    state = fields.Selection([('draft','New'),('open','Active'),('pending','To Renew'),('close','Closed'),('cancel','Cancelled')],string='Status', required=True, track_visibility='onchange',copy=False, default='draft')

    @api.onchange('partner_id')
    def onchange_send_mail(self):
        self.sent_by_mail = self.partner_id.sent_by_mail

    @api.depends('recurring_invoice_line_ids', 'recurring_total')
    def _amount_all(self):
        for account in self:
            account_sudo = account.sudo()
            val = val1 = 0.0
            cur = account_sudo.pricelist_id.currency_id
            for line in account_sudo.recurring_invoice_line_ids:
                val1 += line.price_subtotal
                val += line._amount_line_tax()
            print('------------vv--',val)
            account.recurring_amount_tax = val
            account.recurring_amount_total = account.recurring_amount_tax + account.recurring_total

class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    @api.depends('price_unit', 'quantity', 'discount', 'analytic_account_id.pricelist_id')
    def _compute_price_subtotal(self):
        for line in self:
            line_sudo = line.sudo()
            price = line.env['account.tax']._fix_tax_included_price(line.price_unit, line_sudo.product_id.taxes_id, [])
            line.price_subtotal = line.quantity * price * (100.0 - line.discount) / 100.0
            if line.analytic_account_id.pricelist_id:
                line.price_subtotal = line.price_subtotal