# -*- coding: utf-8 -*-
from odoo import fields, models, tools, api


class sale_subscription_report(models.Model):
    _inherit = "sale.subscription.report"

    sub_type = fields.Selection([('Full subscription', 'Full subscription'), ('Directory', 'Directory')], 'Subscription Type')

    def _select(self):
        select_str ='''
            SELECT min(l.id) as id,
                sub.name as name,
                l.product_id as product_id,
                l.uom_id as product_uom,
                sub.analytic_account_id as analytic_account_id,
                (l.price_unit * l.quantity) - (0.01 * COALESCE(l.discount, 0.0) * (l.price_unit * l.quantity)) as recurring_price,
                sum(l.quantity) as quantity,
                sub.date_start as date_start,
                sub.date as date_end,
                sub.partner_id as partner_id,
                sub.user_id as user_id,
                sub.company_id as company_id,
                sub.state,
                sub.template_id as template_id,
                t.categ_id as categ_id,
                sub.pricelist_id as pricelist_id,
                p.product_tmpl_id,
                partner.country_id as country_id,
                partner.commercial_partner_id as commercial_partner_id,
                partner.industry_id as industry_id,
                sub.close_reason_id as close_reason_id,
                sub.x_studio_field_q2r2T as sub_type

        '''

        return select_str