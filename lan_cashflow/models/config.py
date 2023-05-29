from odoo import _, api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cash_bank_cashflow_ids = fields.Many2many('account.account', related='company_id.cash_bank_cashflow_ids', readonly=False)
    sales_income_cashflow_id = fields.Many2one('account.account', string='Sales Account',  related='company_id.sales_income_cashflow_id', readonly=False) 
    sales_deduction_cashflow_ids = fields.Many2many('account.account', related='company_id.sales_deduction_cashflow_ids', readonly=False)


class ResCompany(models.Model):
    _inherit = 'res.company'

    cash_bank_cashflow_ids = fields.Many2many('account.account', 'cash_bank_cashflow_company_rel','company_id','account_id',string='Cash & Bank Account')        
    sales_income_cashflow_id = fields.Many2one('account.account', string='Sales Account') 
    sales_deduction_cashflow_ids = fields.Many2many('account.account', 'sales_deduction_cashflow_company_rel','company_id','account_id',string='Sales Deduction Account')       