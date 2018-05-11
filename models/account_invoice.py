# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    sent_by_mail = fields.Boolean('Send by paper mail')
    adress_email_to_send = fields.Char('Adress Email of Agent', default='info@winseed.be')



    @api.onchange('partner_id')
    def onchange_send_mail(self):
        self.sent_by_mail = self.partner_id.sent_by_mail

    @api.multi
    def action_send_mail(self):
        self.sent_by_mail = True

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        # round_curr = self.currency_id.round
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum((line.amount_total) for line in self.tax_line_ids)
        self.amount_total = self.amount_untaxed + self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    amount_untaxed = fields.Float(string='Untaxed Amount', digits=dp.get_precision('Account'),
                                     store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    amount_untaxed_signed = fields.Float(string='Untaxed Amount in Company Currency',
                                            currency_field='company_currency_id', digits=dp.get_precision('Account'),
                                            store=True, readonly=True, compute='_compute_amount')
    amount_tax = fields.Float(string='Tax', digits=dp.get_precision('Account'),
                                 store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Float(string='Total', 
                                   store=True, readonly=True, compute='_compute_amount')
    amount_total_signed = fields.Monetary(string='Total in Invoice Currency', currency_field='currency_id',
                                          store=True, readonly=True, compute='_compute_amount', digits=dp.get_precision('Account'),
                                          help="Total amount in the currency of the invoice, negative for credit notes.")
    amount_total_company_signed = fields.Float(string='Total in Company Currency',
                                                  currency_field='company_currency_id', digits=dp.get_precision('Account'),
                                                  store=True, readonly=True, compute='_compute_amount',
                                                  help="Total amount in the currency of the company, negative for credit notes.")

    residual = fields.Float(string='Amount Due',
                               compute='_compute_residual', store=True, help="Remaining amount due.")
    residual_signed = fields.Float(string='Amount Due in Invoice Currency', currency_field='currency_id',
                                      compute='_compute_residual', store=True, digits=dp.get_precision('Account'),
                                      help="Remaining amount due in the currency of the invoice.")
    residual_company_signed = fields.Float(string='Amount Due in Company Currency',
                                              currency_field='company_currency_id',
                                              compute='_compute_residual', store=True,
                                              help="Remaining amount due in the currency of the company.", digits=dp.get_precision('Account'))


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    price_subtotal = fields.Float(string='Amount',
                                     store=True, readonly=True, compute='_compute_price',
                                     help="Total amount without taxes", digits=dp.get_precision('Account'))


class AccountTax(models.Model):
    _inherit = 'account.tax'


    @api.multi
    def compute_all(self, price_unit, currency=None, quantity=1.0, product=None, partner=None):
        """ Returns all information required to apply taxes (in self + their children in case of a tax goup).
            We consider the sequence of the parent for group of taxes.
                Eg. considering letters as taxes and alphabetic order as sequence :
                [G, B([A, D, F]), E, C] will be computed as [A, D, F, C, E, G]

        RETURN: {
            'total_excluded': 0.0,    # Total without taxes
            'total_included': 0.0,    # Total with taxes
            'taxes': [{               # One dict for each tax in self and their children
                'id': int,
                'name': str,
                'amount': float,
                'sequence': int,
                'account_id': int,
                'refund_account_id': int,
                'analytic': boolean,
            }]
        } """
        if len(self) == 0:
            company_id = self.env.user.company_id
        else:
            company_id = self[0].company_id
        if not currency:
            currency = company_id.currency_id
        taxes = []
        # By default, for each tax, tax amount will first be computed
        # and rounded at the 'Account' decimal precision for each
        # PO/SO/invoice line and then these rounded amounts will be
        # summed, leading to the total amount for that tax. But, if the
        # company has tax_calculation_rounding_method = round_globally,
        # we still follow the same method, but we use a much larger
        # precision when we round the tax amount for each line (we use
        # the 'Account' decimal precision + 5), and that way it's like
        # rounding after the sum of the tax amounts of each line
        prec = currency.decimal_places

        # In some cases, it is necessary to force/prevent the rounding of the tax and the total
        # amounts. For example, in SO/PO line, we don't want to round the price unit at the
        # precision of the currency.
        # The context key 'round' allows to force the standard behavior.
        round_tax = False if company_id.tax_calculation_rounding_method == 'round_globally' else True
        round_total = False
        if 'round' in self.env.context:
            round_tax = bool(self.env.context['round'])
            round_total = bool(self.env.context['round'])

        if not round_tax:
            prec += 5

        base_values = self.env.context.get('base_values')
        if not base_values:
            total_excluded = total_included = base = round(price_unit * quantity, prec)
            # total_excluded = total_included = base = (price_unit * quantity, prec)

        else:
            total_excluded, total_included, base = base_values

        # Sorting key is mandatory in this case. When no key is provided, sorted() will perform a
        # search. However, the search method is overridden in account.tax in order to add a domain
        # depending on the context. This domain might filter out some taxes from self, e.g. in the
        # case of group taxes.
        for tax in self.sorted(key=lambda r: r.sequence):
            if tax.amount_type == 'group':
                children = tax.children_tax_ids.with_context(base_values=(total_excluded, total_included, base))
                ret = children.compute_all(price_unit, currency, quantity, product, partner)
                total_excluded = ret['total_excluded']
                base = ret['base'] if tax.include_base_amount else base
                total_included = ret['total_included']
                tax_amount = total_included - total_excluded
                taxes += ret['taxes']
                continue

            tax_amount = tax._compute_amount(base, price_unit, quantity, product, partner)
            if not round_tax:
                tax_amount = round(tax_amount, prec)
            else:
                tax_amount = currency.round(tax_amount)

            if tax.price_include:
                total_excluded -= tax_amount
                base -= tax_amount
            else:
                total_included += tax_amount

            # Keep base amount used for the current tax
            tax_base = base

            if tax.include_base_amount:
                base += tax_amount

            taxes.append({
                'id': tax.id,
                'name': tax.with_context(**{'lang': partner.lang} if partner else {}).name,
                'amount': tax_amount,
                'base': tax_base,
                'sequence': tax.sequence,
                'account_id': tax.account_id.id,
                'refund_account_id': tax.refund_account_id.id,
                'analytic': tax.analytic,
                'price_include': tax.price_include,
            })

        return {
            'taxes': sorted(taxes, key=lambda k: k['sequence']),
            'total_excluded': (total_excluded) if round_total else total_excluded,
            'total_included': (total_included) if round_total else total_included,
            'base': base,
        }

