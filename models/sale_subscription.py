# -*- coding: utf-8 -*-

import logging
import datetime
import time
import traceback

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import format_date


_logger = logging.getLogger(__name__)

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    sent_by_mail = fields.Boolean('Send by paper mail')
    state = fields.Selection([('draft','New'),('open','Active'),('pending','To Renew'),('close','Closed'),('cancel','Cancelled')],string='Status', required=True, track_visibility='onchange',copy=False, default='draft')
    last_invoice_date = fields.Date('Last Invoice Date')
    payment_token_id = fields.Many2one('payment.token', 'Payment Token',
                                       help='If not set, the default payment token of the partner will be used.',
                                       domain="[('partner_id','=',partner_id)]", oldname='payment_method_id', compute="payment_token", store=True)


    ## set partner saved payment token
    @api.depends('recurring_next_date')
    @api.one
    def payment_token(self):
        print('app too')
        self.payment_token_id = self.env['payment.token'].search([('partner_id', '=', self.partner_id.id)], limit=1, order='id desc').id


    ## send post mail onchange function
    @api.onchange('partner_id')
    def onchange_send_mail(self):
        self.sent_by_mail = self.partner_id.sent_by_mail


    def _prepare_invoice_data(self):
        self.ensure_one()

        if not self.partner_id:
            raise UserError(_("You must first select a Customer for Subscription %s!") % self.name)

        if 'force_company' in self.env.context:
            company = self.env['res.company'].browse(self.env.context['force_company'])
        else:
            company = self.company_id
            self = self.with_context(force_company=company.id, company_id=company.id)

        fpos_id = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id)
        journal = self.template_id.journal_id or self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', company.id)], limit=1)
        if not journal:
            raise UserError(_('Please define a sale journal for the company "%s".') % (company.name or '', ))

        next_date = fields.Date.from_string(self.recurring_next_date)
        if not next_date:
            raise UserError(_('Please define Date of Next Invoice of "%s".') % (self.display_name,))
        periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
        end_date = next_date + relativedelta(**{periods[self.recurring_rule_type]: self.recurring_interval})
        end_date = end_date - relativedelta(days=1)     # remove 1 day as normal people thinks in term of inclusive ranges.
        addr = self.partner_id.address_get(['delivery'])

        return {
            'account_id': self.partner_id.property_account_receivable_id.id,
            'type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'partner_shipping_id': addr['delivery'],
            'currency_id': self.pricelist_id.currency_id.id,
            'journal_id': journal.id,
            'origin': self.code,
            'fiscal_position_id': fpos_id,
            'payment_term_id': self.partner_id.property_payment_term_id.id,
            'company_id': company.id,
            'comment': _("This invoice covers the following period: %s - %s") % (format_date(self.env, next_date), format_date(self.env, end_date)),
            'user_id': self.user_id.id,
            'sent_by_mail': True if self.sent_by_mail else False,
            'subscription_id' : self.id,
        }

    @api.multi
    def _recurring_create_invoice(self, automatic=False):
        auto_commit = self.env.context.get('auto_commit', True)
        cr = self.env.cr
        invoices = self.env['account.invoice']
        current_date = time.strftime('%Y-%m-%d')
        imd_res = self.env['ir.model.data']
        template_res = self.env['mail.template']
        if len(self) > 0:
            subscriptions = self
        else:
            domain = [('recurring_next_date', '<=', current_date),
                      ('state', 'in', ['open', 'pending'])]
            subscriptions = self.search(domain)
        if subscriptions:
            sub_data = subscriptions.read(fields=['id', 'company_id'])
            for company_id in set(data['company_id'][0] for data in sub_data):
                sub_ids = [s['id'] for s in sub_data if s['company_id'][0] == company_id]
                subs = self.with_context(company_id=company_id, force_company=company_id).browse(sub_ids)
                context_company = dict(self.env.context, company_id=company_id, force_company=company_id)
                for subscription in subs:
                    subscription.write({'last_invoice_date': subscription.recurring_next_date})
                    if automatic and auto_commit:
                        cr.commit()
                    payment_token = subscription.payment_token_id
                    # payment + invoice (only by cron)
                    ## add test on payment_token
                    if subscription.template_id.payment_mandatory and subscription.recurring_total and automatic and payment_token:
                        try:
                            # payment_token = subscription.payment_token_id
                            tx = None
                            if payment_token:
                                invoice_values = subscription.with_context(
                                    lang=subscription.partner_id.lang)._prepare_invoice()
                                new_invoice = self.env['account.invoice'].with_context(context_company).create(
                                    invoice_values)
                                new_invoice.message_post_with_view('mail.message_origin_link',
                                                                   values={'self': new_invoice, 'origin': subscription},
                                                                   subtype_id=self.env.ref('mail.mt_note').id)
                                new_invoice.with_context(context_company).compute_taxes()
                                tx = subscription._do_payment(payment_token, new_invoice, two_steps_sec=False)[0]
                                # commit change as soon as we try the payment so we have a trace somewhere
                                if auto_commit:
                                    cr.commit()
                                if tx.state in ['done', 'authorized']:
                                    subscription.send_success_mail(tx, new_invoice)
                                    msg_body = 'Automatic payment succeeded. Payment reference: <a href=# data-oe-model=payment.transaction data-oe-id=%d>%s</a>; Amount: %s. Invoice <a href=# data-oe-model=account.invoice data-oe-id=%d>View Invoice</a>.' % (
                                    tx.id, tx.reference, tx.amount, new_invoice.id)
                                    subscription.message_post(body=msg_body)
                                    if auto_commit:
                                        cr.commit()
                                else:
                                    _logger.error('Fail to create recurring invoice for subscription %s',
                                                  subscription.code)
                                    if auto_commit:
                                        cr.rollback()
                                    new_invoice.unlink()
                            if tx is None or tx.state != 'done':
                                amount = subscription.recurring_total
                                date_close = datetime.datetime.strptime(subscription.recurring_next_date,
                                                                        "%Y-%m-%d") + relativedelta(days=15)
                                close_subscription = current_date >= date_close.strftime('%Y-%m-%d')
                                email_context = self.env.context.copy()
                                email_context.update({
                                    'payment_token': subscription.payment_token_id and subscription.payment_token_id.name,
                                    'renewed': False,
                                    'total_amount': amount,
                                    'email_to': subscription.partner_id.email,
                                    'code': subscription.code,
                                    'currency': subscription.pricelist_id.currency_id.name,
                                    'date_end': subscription.date,
                                    'date_close': date_close.date()
                                })
                                # if close_subscription:
                                #     _, template_id = imd_res.get_object_reference('sale_subscription',
                                #                                                   'email_payment_close')
                                #     template = template_res.browse(template_id)
                                #     template.with_context(email_context).send_mail(subscription.id)
                                #     _logger.debug(
                                #         "Sending Subscription Payment Failure Mail to %s for subscription %s ",
                                #         subscription.partner_id.email, subscription.id)
                                #     msg_body = 'Automatic payment failed after multiple attempts.'
                                #     subscription.message_post(body=msg_body)
                                # else:

                                ## change template to email payment failure template
                                _, template_id = imd_res.get_object_reference('DrAnytime_CRM',
                                                                              'email_payment_failure')
                                msg_body = 'Automatic payment failed.'
                                if (datetime.datetime.today() - datetime.datetime.strptime(
                                        subscription.recurring_next_date, '%Y-%m-%d')).days in [0, 7, 14]:
                                    template = template_res.browse(template_id)
                                    template.with_context(email_context).send_mail(subscription.id)
                                    _logger.debug("Sending Payment Failure Mail to %s for subscription %s",
                                                  subscription.partner_id.email, subscription.id)
                                    msg_body += ' E-mail sent to customer.'
                                subscription.message_post(body=msg_body)
                                # Hide automatic pass subscription to state close
                                # subscription.write({'state': 'close' if close_subscription else 'pending'})
                            if auto_commit:
                                cr.commit()
                        except Exception:
                            if auto_commit:
                                cr.rollback()
                            # we assume that the payment is run only once a day
                            traceback_message = traceback.format_exc()
                            _logger.error(traceback_message)
                            last_tx = self.env['payment.transaction'].search([('reference', 'like',
                                                                               'SUBSCRIPTION-%s-%s' % (subscription.id,
                                                                                                       datetime.date.today().strftime(
                                                                                                           '%y%m%d')))],
                                                                             limit=1)
                            error_message = "Error during renewal of subscription %s (%s)" % (subscription.code,
                                                                                              'Payment recorded: %s' % last_tx.reference if last_tx and last_tx.state == 'done' else 'No payment recorded.')
                            _logger.error(error_message)



                    # invoice only
                    else:
                        try:
                            invoice_values = subscription.with_context(
                                lang=subscription.partner_id.lang)._prepare_invoice()
                            new_invoice = self.env['account.invoice'].with_context(context_company).create(
                                invoice_values)
                            new_invoice.message_post_with_view('mail.message_origin_link',
                                                               values={'self': new_invoice, 'origin': subscription},
                                                               subtype_id=self.env.ref('mail.mt_note').id)
                            new_invoice.with_context(context_company).compute_taxes()
                            invoices += new_invoice
                            next_date = datetime.datetime.strptime(subscription.recurring_next_date or current_date,
                                                                   "%Y-%m-%d")
                            periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
                            invoicing_period = relativedelta(
                                **{periods[subscription.recurring_rule_type]: subscription.recurring_interval})
                            new_date = next_date + invoicing_period
                            subscription.write({'recurring_next_date': new_date.strftime('%Y-%m-%d')})
                            if automatic and auto_commit:
                                cr.commit()
                        except Exception:
                            if automatic and auto_commit:
                                cr.rollback()
                                _logger.exception('Fail to create recurring invoice for subscription %s',
                                                  subscription.code)
                            else:
                                raise

        return invoices

#     @api.depends('recurring_invoice_line_ids', 'recurring_total')
#     def _amount_all(self):
#         for account in self:
#             account_sudo = account.sudo()
#             val = val1 = 0.0
#             cur = account_sudo.pricelist_id.currency_id
#             for line in account_sudo.recurring_invoice_line_ids:
#                 val1 += line.price_subtotal
#                 val += line._amount_line_tax()
#             print('------------vv--',val)
#             account.recurring_amount_tax = val
#             account.recurring_amount_total = account.recurring_amount_tax + account.recurring_total
#
# class SaleSubscriptionLine(models.Model):
#     _inherit = "sale.subscription.line"
#
#     @api.depends('price_unit', 'quantity', 'discount', 'analytic_account_id.pricelist_id')
#     def _compute_price_subtotal(self):
#         for line in self:
#             line_sudo = line.sudo()
#             price = line.env['account.tax']._fix_tax_included_price(line.price_unit, line_sudo.product_id.taxes_id, [])
#             line.price_subtotal = line.quantity * price * (100.0 - line.discount) / 100.0
#             if line.analytic_account_id.pricelist_id:
#                 line.price_subtotal = line.price_subtotal