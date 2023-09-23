from odoo import _, api, fields, models





class ResPartnerInherit(models.Model):
  _inherit = 'res.partner'

  analytic_account_id = fields.Many2one("account.analytic.account",string="Analytic Account")
