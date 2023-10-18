from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountJournal(models.Model):
    _inherit = 'account.journal'
    
    
    outstanding2_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Outstanding Account",
        store=True,
        compute='_compute_outstanding2_account_id',
        check_company=True)
    
    @api.depends('inbound_payment_method_line_ids.payment_account_id')
    def _compute_outstanding2_account_id(self):
        for pay in self:
            if pay.inbound_payment_method_line_ids :
                pay.outstanding2_account_id = (pay.inbound_payment_method_line_ids[0].payment_account_id.id
                                              or pay.company_id.account_journal_payment_debit_account_id)
            else :
                pay.outstanding2_account_id = pay.company_id.account_journal_payment_debit_account_id
           
    
class AccountMove(models.Model):
    _inherit = 'account.move'


    @api.model
    def create(self, values):
        
        if values.get('journal_id', False) == 44 :
            print('debug')
        result = super(AccountMove, self).create(values)
        
        return result
    
    
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    @api.model
    def create(self, values):
        
        if values.get('account_id', False) == 673 :
            print('debug')
        result = super(AccountMoveLine, self).create(values)
        
        return result
    
    
class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"
    
    
    @api.model
    def _prepare_liquidity_move_line_vals(self):
        ''' Prepare values to create a new account.move.line record corresponding to the
        liquidity line (having the bank/cash account).
        :return:        The values to create a new account.move.line record.
        '''
        self.ensure_one()

        statement = self.statement_id
        journal = statement.journal_id
        company_currency = journal.company_id.currency_id
        journal_currency = journal.currency_id or company_currency

        if self.foreign_currency_id and journal_currency:
            currency_id = journal_currency.id
            if self.foreign_currency_id == company_currency:
                amount_currency = self.amount
                balance = self.amount_currency
            else:
                amount_currency = self.amount
                balance = journal_currency._convert(amount_currency, company_currency, journal.company_id, self.date)
        elif self.foreign_currency_id and not journal_currency:
            amount_currency = self.amount_currency
            balance = self.amount
            currency_id = self.foreign_currency_id.id
        elif not self.foreign_currency_id and journal_currency:
            currency_id = journal_currency.id
            amount_currency = self.amount
            balance = journal_currency._convert(amount_currency, journal.company_id.currency_id, journal.company_id, self.date)
        else:
            currency_id = company_currency.id
            amount_currency = self.amount
            balance = self.amount

        return {
            'name': self.payment_ref,
            'move_id': self.move_id.id,
            'partner_id': self.partner_id.id,
            'currency_id': currency_id,
            'account_id': journal.outstanding2_account_id.id or journal.default_account_id.id,
            'debit': balance > 0 and balance or 0.0,
            'credit': balance < 0 and -balance or 0.0,
            'amount_currency': amount_currency,
        }
        
    def _seek_for_lines(self):
        ''' Helper used to dispatch the journal items between:
        - The lines using the liquidity account.
        - The lines using the transfer account.
        - The lines being not in one of the two previous categories.
        :return: (liquidity_lines, suspense_lines, other_lines)
        '''
        liquidity_lines = self.env['account.move.line']
        suspense_lines = self.env['account.move.line']
        other_lines = self.env['account.move.line']

        for line in self.move_id.line_ids:
            if line.account_id in (self.journal_id.default_account_id, self.journal_id.outstanding2_account_id):
                liquidity_lines += line
            elif line.account_id == self.journal_id.suspense_account_id:
                suspense_lines += line
            else:
                other_lines += line
        return liquidity_lines, suspense_lines, other_lines