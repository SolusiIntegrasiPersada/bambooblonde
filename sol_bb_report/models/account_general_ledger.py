from odoo import models, fields, api, _
from odoo.tools.misc import format_date, DEFAULT_SERVER_DATE_FORMAT
from datetime import timedelta


class AccountGeneralLedgerReport(models.AbstractModel):
    _inherit = "account.general.ledger"

    @api.model
    def _get_account_title_line(self, options, account, amount_currency, debit, credit, balance, has_lines):

        expanded_account = self.env['account.account'].browse(account.id)
        amls_query, amls_params = self._get_query_amls(options, expanded_account)
        self.env.cr.execute(amls_query, amls_params)
        amls = self._cr.dictfetchall()
        
        cumulated_debit = 0
        cumulated_credit = 0
        for aml in amls:
            cumulated_debit += aml['debit']
            cumulated_credit += aml['credit']

        has_foreign_currency = account.currency_id and account.currency_id != account.company_id.currency_id or False
        unfold_all = self._context.get('print_mode') and not options.get('unfolded_lines')

        name = '%s %s' % (account.code, account.name)
        columns = [
            {'name': self.format_value(cumulated_debit), 'class': 'number'},
            {'name': self.format_value(cumulated_credit), 'class': 'number'},
            {'name': self.format_value(balance), 'class': 'number'},
        ]
        if self.user_has_groups('base.group_multi_currency'):
            columns.insert(0, {'name': has_foreign_currency and self.format_value(amount_currency, currency=account.currency_id, blank_if_zero=True) or '', 'class': 'number'})
        return {
            'id': 'account_%d' % account.id,
            'name': name,
            'columns': columns,
            'level': 1,
            'unfoldable': has_lines,
            'unfolded': has_lines and 'account_%d' % account.id in options.get('unfolded_lines') or unfold_all,
            'colspan': 4,
            'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
        }

    @api.model
    def _get_initial_balance_line(self, options, account, amount_currency, debit, credit, balance):
        columns = [
            {'name': self.format_value(0), 'class': 'number'},
            {'name': self.format_value(0), 'class': 'number'},
            {'name': self.format_value(balance), 'class': 'number'},
        ]

        has_foreign_currency = account.currency_id and account.currency_id != account.company_id.currency_id or False
        if self.user_has_groups('base.group_multi_currency'):
            columns.insert(0, {'name': has_foreign_currency and self.format_value(amount_currency, currency=account.currency_id, blank_if_zero=True) or '', 'class': 'number'})
        return {
            'id': 'initial_%d' % account.id,
            'class': 'o_account_reports_initial_balance',
            'name': _('Initial Balance'),
            'parent_id': 'account_%d' % account.id,
            'columns': columns,
            'colspan': 4,
        }