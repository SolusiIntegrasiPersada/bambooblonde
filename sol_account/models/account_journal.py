from odoo import _, api, fields, models

class AccountJournal(models.Model):
  _inherit = 'account.journal'

  branch = fields.Char(string="Branch", default="Legian, Bali Indonesia")
  swift_code = fields.Char(string="Swift Code")
  account_no = fields.Char(string="Account No.")