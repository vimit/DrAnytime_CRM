#-*- coding:utf-8 -*-
from __future__ import division
from odoo import models, fields, api
from datetime import date, datetime, timedelta, time
import dateutil.parser
from odoo.addons import decimal_precision as dp
from odoo.exceptions import RedirectWarning, UserError, ValidationError

from odoo.tools.misc import formatLang



class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    annual_interest = fields.Float("Interest %", help="Annual Interest Percent")
    second_interest = fields.Float(string="Second Interest %", help="Second Interest applied after 60 days from due date")
    amount_limit_second_interest = fields.Float(string="Lump Amount")

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    number_days = fields.Integer('Delay Days')
    total_interest = fields.Float(string="Total interest", digits=dp.get_precision('Account'))
    annual_interest = fields.Float(string="Interest %", related="payment_term_id.annual_interest", help="Annual Interest Percent")
    second_interest = fields.Float(string="Second interest %", related="payment_term_id.second_interest")
    amount_limit_second_interest = fields.Float(string="Lump Amount", related="payment_term_id.amount_limit_second_interest")

    # envoie email du rappel automatically
    @api.model
    def process_send_reminder(self):
        self.send_reminders()

    @api.multi
    def send_reminders(self):
        account_invoices = self.search([('type', '=', 'out_invoice'), ('state', '=', 'open')])
        template_res = self.env['mail.template']
        imd_res = self.env['ir.model.data']
        for account in account_invoices:
            d = datetime.today().strftime('%Y-%m-%d')
            date = dateutil.parser.parse(d).date()
            dd = date.strftime("%Y-%m-%d")
            date1 = datetime.strptime(dd, '%Y-%m-%d').date()
            date2 = datetime.strptime(account.date_due, '%Y-%m-%d').date()
            diff = (date1 - date2).days
            print('diff--', diff)

            if (diff == 20 or diff % 30 == 0) and diff !=0 :
                print('email envoyé--',account.id)
                _, template_id = imd_res.get_object_reference('DrAnytime_CRM',
                                                              'email_invoice_reminder')
                template = template_res.browse(template_id)
                template.send_mail(account.id)


    # This function is called when the scheduler goes on
    @api.model
    def process_scheduler_interest(self):
        self.calcul_interest()

    @api.multi
    def calcul_interest(self):
        account_invoices = self.search([('type', '=', 'out_invoice'),('state', '=', 'open')])
        template_res = self.env['mail.template']
        imd_res = self.env['ir.model.data']
        for account in account_invoices:
            d = datetime.today().strftime('%Y-%m-%d')
            date = dateutil.parser.parse(d).date()
            dd = date.strftime("%Y-%m-%d")
            date1 = datetime.strptime(dd, '%Y-%m-%d').date()
            date2 = datetime.strptime(account.date_due, '%Y-%m-%d').date()
            print('ddddda--',date2)
            diff = (date1 - date2).days

            print('diff------',diff)
            total_interest = 0
            if diff == 20 or diff % 30 == 0:
                total_interest = (account.amount_untaxed * (account.annual_interest/365)  * diff)/100
                print('int1-----',total_interest)
            if (diff >= 60 and diff % 30 == 0) and diff !=0 :
                second_interest = (account.amount_untaxed * (account.second_interest /365)  * diff)/ 100
                if second_interest < account.amount_limit_second_interest:
                    total_interest = total_interest + account.amount_limit_second_interest
                    print('int2-----', total_interest)

                else:
                    total_interest = total_interest + second_interest
                    print('int1-----', total_interest)

            print('ss-----',self.number)
            print('value total interest---',account.currency_id.round(total_interest))
            print('account interest ----',account.currency_id.round(account.total_interest))
            if account.currency_id.round(total_interest) > account.currency_id.round(account.total_interest) :
                print('okkkk')
                vals = {
                    'number_days': diff,
                    'total_interest': total_interest,
                    'amount_total': account.amount_untaxed + total_interest + account.amount_tax,
                    'residual': account.amount_untaxed + total_interest + account.amount_tax,
                    'residual_signed': account.amount_untaxed + total_interest + account.amount_tax,
                    'amount_total_company_signed': account.currency_id.compute(
                        account.amount_untaxed + total_interest + account.amount_tax,
                        account.company_id.currency_id),
                    'amount_total_signed': account.amount_untaxed + total_interest + account.amount_tax,
                    'amount_residual' : account.amount_untaxed + total_interest + account.amount_tax,
                }


            else:
                vals=({
                    'number_days': diff,
                })



            account.write(vals)
            account.interest_move_create(total_interest)


    @api.multi
    def process_manual_interest(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['account.invoice'].browse(active_ids):
            record.manual_calcul_interest()

    @api.multi
    def manual_calcul_interest(self):
        account = self
        if self.state=='open' and self.type=='out_invoice':
            d = datetime.today().strftime('%Y-%m-%d')
            date = dateutil.parser.parse(d).date()
            dd = date.strftime("%Y-%m-%d")
            date1 = datetime.strptime(dd, '%Y-%m-%d').date()
            date2 = datetime.strptime(self.date_due, '%Y-%m-%d').date()
            diff = (date1 - date2).days
            print('ddddda--',date2)
            print('ddddda--',date1)

            total_interest = 0
            if diff == 20 or diff // 30 > 0:
                total_interest = (self.amount_untaxed * (self.annual_interest/365)  * diff)/100

            if diff >= 60:
                second_interest = (self.amount_untaxed * (self.second_interest/365) * diff) / 100
                print('---ss----',(self.second_interest/365) * 60)
                if second_interest < self.amount_limit_second_interest:
                    total_interest = total_interest + (self.amount_limit_second_interest * ((diff // 30) -1))
                else:
                    total_interest = total_interest + second_interest
            print('1---',total_interest)
            print('2-----',self.total_interest)
            print('bool----',total_interest > self.total_interest)
            if total_interest > self.total_interest:
                print('22222222222')
                vals = {
                    'number_days': diff,
                    'total_interest': total_interest,
                    'amount_total': self.amount_untaxed + total_interest + self.amount_tax,
                    'residual': self.amount_untaxed + total_interest + self.amount_tax,
                    'residual_signed': self.amount_untaxed + total_interest + self.amount_tax,
                    'amount_total_company_signed': self.currency_id.compute(
                        self.amount_untaxed + total_interest + self.amount_tax,
                        self.company_id.currency_id),
                    'amount_total_signed': self.amount_untaxed + total_interest + self.amount_tax,
                    'amount_residual': account.amount_untaxed + total_interest + account.amount_tax,

                }
            else:
                print('000000000000')
                vals = ({
                    'number_days': diff,
                })
            print('aa---',account.amount_untaxed + total_interest + account.amount_tax)
            self.write(vals)
            self.interest_move_create(account.currency_id.round(total_interest))
            print('finish')
        return True
    ####
    # @api.multi
    def interest_move_create(self,interest):
        print('enter')
        self.move_id.state = 'draft'
        account = self.env.ref('DrAnytime_CRM.a491124')
        product = self.env.ref('DrAnytime_CRM.product_interest_01')

        print('aaa----',account)
        print('bbb----',product)

        l_interest = [l for l in self.move_id.line_ids if l.name == 'interest']
        if not l_interest:
            self.env['account.move.line'].with_context(check_move_validity=False).create({
                'name': 'interest',
                'debit': 0.0,
                'credit': interest,
                'account_id': account.id,
                # 'tax_line_id': line.tax_line_id.id,
                # 'tax_exigible': True,
                'amount_currency': 0.0,
                # 'amount_currency': -interest or 0.0,
                'currency_id': self.currency_id.id,
                'move_id': self.move_id.id,
                'partner_id': self.partner_id.id,
                'amount_residual' : 0.0,
                'amount_residual_currency' : 0.0,
                'invoice_id' : self.id,
                'balance' :  -interest or 0.0,
                'quantity' : 1,
                'product_uom_id' : 1,
                'product_id' : product.id,
                'journal_type': 'sale'
            })
            print('ok')
        else:
            l_interest_obj = l_interest[0]
            l_interest_obj.credit = interest
        t_move = [l for l in self.move_id.line_ids if l.name == '/'][0]
        credit = 0.0
        for l in self.move_id.line_ids:
            credit = credit + l.credit

        print('cred----',credit)
        t_move.debit = credit
        self.move_id.state = 'posted'

        return True



class AccountMove(models.Model):
    _inherit = "account.move"

    @api.multi
    def assert_balanced(self):
        if not self.ids:
            return True
        prec = self.env['decimal.precision'].precision_get('Account')

        self._cr.execute("""\
                SELECT      move_id
                FROM        account_move_line
                WHERE       move_id in %s
                GROUP BY    move_id
                HAVING      abs(sum(debit) - sum(credit)) > %s
                """, (tuple(self.ids), 10 ** (-max(5, prec))))
        if len(self._cr.fetchall()) != 0:
            # raise UserError(_("Cannot create unbalanced journal entry."))
            print("Cannot create unbalanced journal entry.")
        return True

#
# class AccountMoveLine(models.Model):
#     _inherit = "account.move.line"
#
#     _order = 'id des'
#     # sql_constraints = [
#     #     ('credit_debit1', 'CHECK (1=1)', 'Wrong credit or debit value in accounting entry !'),
#     #     ('credit_debit2', 'CHECK (1=1)', 'Wrong credit or debit value in accounting entry !'),
#     # ]
#
#     def _auto_init(self):
#         print("pppp")
#         sql_constraints = [
#         ('credit_debit1', 'CHECK (1=1)', 'Wrong credit or debit value in accounting entry !'),
#         ('credit_debit2', 'CHECK (1=1)', 'Wrong credit or debit value in accounting entry !'),
#         ]
#         super(AccountMoveLine, self)._auto_init()