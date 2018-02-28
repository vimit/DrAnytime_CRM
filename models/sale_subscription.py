# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    sent_by_mail = fields.Boolean('Send by paper mail')

    @api.onchange('partner_id')
    def onchange_send_mail(self):
        self.sent_by_mail = self.partner_id.sent_by_mail