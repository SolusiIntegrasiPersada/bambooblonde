from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    address = fields.Char(string='Address')
    supervisor = fields.Char(string='Supervisor')
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Analytic Account")
