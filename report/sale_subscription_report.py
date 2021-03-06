# -*- coding: utf-8 -*-
from odoo import fields, models, tools, api

class SaleSubscription (models.Model):
    _inherit = "sale.subscription"

    sub_type = fields.Selection([('full_subscription', 'Full subscription'), ('directory', 'Directory')],
                                'Subscription Type')


class sale_subscription_report(models.Model):
    _inherit = "sale.subscription.report"

    sub_type = fields.Selection([('full_subscription', 'Full subscription'), ('directory', 'Directory')], 'Subscription Type')

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
                sub.sub_type

        '''

        return select_str

    def _group_by(self):
        group_by_str = '''
                    GROUP BY    l.product_id,
                                l.uom_id,
                                t.categ_id,
                                sub.analytic_account_id,
                                sub.date_start,
                                sub.date,
                                sub.partner_id,     
                                sub.user_id,
                                recurring_price,
                                quantity,
                                sub.company_id,
                                sub.state,
                                sub.name,
                                sub.template_id,
                                sub.pricelist_id,
                                p.product_tmpl_id,
                                partner.country_id,
                                partner.commercial_partner_id,
                                partner.industry_id,
                                sub.close_reason_id,
                                sub.sub_type


                                                        

        
        
        
        '''
        return   group_by_str