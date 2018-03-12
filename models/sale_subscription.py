# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    sent_by_mail = fields.Boolean('Send by paper mail')
    state = fields.Selection([('draft','New'),('open','Active'),('pending','To Renew'),('close','Closed'),('cancel','Cancelled')],string='Status', required=True, track_visibility='onchange',copy=False, default='draft')

    @api.onchange('partner_id')
    def onchange_send_mail(self):
        self.sent_by_mail = self.partner_id.sent_by_mail