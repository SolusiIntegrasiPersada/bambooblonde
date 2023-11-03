# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PosSession(models.Model):
    _inherit = 'pos.session'
    
    visitor_count = fields.Integer(string='Visitor Count')
    customer_count = fields.Integer(compute="_compute_customer_and_order_cont", string='Customer Count')
    order_count = fields.Integer(compute="_compute_customer_and_order_cont", string="Order Count")

    def _compute_customer_and_order_cont(self):
        for pos_obj in self:
            pos_obj.customer_count = pos_obj.env['pos.order'].search_count(
                [('partner_id', '!=', False), ('session_id', '=', pos_obj.id)])
            pos_obj.order_count = pos_obj.env['pos.order'].search_count([('session_id', '=', pos_obj.id)]) + 1

    # def _get_sale_vals(self, key, amount, amount_converted):
    #     account_id, sign, tax_keys, base_tag_ids = key
    #     tax_ids = {tax[0] for tax in tax_keys}
    #     applied_taxes = self.env['account.tax'].browse(tax_ids)
    #     title = 'Sales' if sign == 1 else 'Refund'
    #     name = '%s untaxed' % title
    #     if applied_taxes:
    #         name = '{} with {}'.format(title, ', '.join([tax.name for tax in applied_taxes]))
    #     partial_vals = {
    #         'name': name,
    #         'account_id': account_id,
    #         'analytic_account_id': self.config_id.analytic_account_id.id
    #         if self.config_id.analytic_account_id
    #         else False,
    #         'move_id': self.move_id.id,
    #         'tax_ids': [(6, 0, tax_ids)],
    #         'tax_tag_ids': [(6, 0, base_tag_ids)],
    #     }
    #     return self._credit_amounts(partial_vals, amount, amount_converted)
    
    def _create_combine_account_payment(self, payment_method, amounts, diff_amount):
        outstanding_account = payment_method.outstanding_account_id or self.company_id.account_journal_payment_debit_account_id
        destination_account = self._get_receivable_account(payment_method)

        if float_compare(amounts['amount'], 0, precision_rounding=self.currency_id.rounding) < 0:
            # revert the accounts because account.payment doesn't accept negative amount.
            outstanding_account, destination_account = destination_account, outstanding_account
            
        shift = (' - %s') % (self.shift) if self.shift else  ""

        account_payment = self.env['account.payment'].create({
            'amount': abs(amounts['amount']),
            'journal_id': payment_method.journal_id.id,
            'force_outstanding_account_id': outstanding_account.id,
            'destination_account_id':  destination_account.id,
            'ref': _('Combine %s POS payments from %s (%s%s)') % (payment_method.name, self.name, self.config_id.name,shift),
            'pos_payment_method_id': payment_method.id,
            'pos_session_id': self.id,
        })

        diff_amount_compare_to_zero = self.currency_id.compare_amounts(diff_amount, 0)
        if diff_amount_compare_to_zero != 0:
            self._apply_diff_on_account_payment_move(account_payment, payment_method, diff_amount)

        account_payment.action_post()
        return account_payment.move_id.line_ids.filtered(lambda line: line.account_id == account_payment.destination_account_id)
    
    def _get_combine_statement_line_vals(self, statement, amount, payment_method):
        shift = (' - %s') % (self.shift) if self.shift else  ""
        return {
            'date': fields.Date.context_today(self),
            'amount': amount,
            'payment_ref':  ('%s (%s%s)') % (self.name, self.config_id.name,shift),
            'statement_id': statement.id,
            'journal_id': statement.journal_id.id,
            'counterpart_account_id': self._get_receivable_account(payment_method).id,
        }

    def _get_split_statement_line_vals(self, statement, amount, payment):
        accounting_partner = self.env["res.partner"]._find_accounting_partner(payment.partner_id)
        shift = (' - %s') % (self.shift) if self.shift else  ""
        return {
            'date': fields.Date.context_today(self, timestamp=payment.payment_date),
            'amount': amount,
            'payment_ref':  ('%s (%s%s)') % (self.name, self.config_id.name,shift),
            'statement_id': statement.id,
            'journal_id': statement.journal_id.id,
            'counterpart_account_id': accounting_partner.property_account_receivable_id.id,
            'partner_id': accounting_partner.id,
        }
