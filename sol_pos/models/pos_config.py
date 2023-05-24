from odoo import models, fields, api

class PosConfig(models.Model):
  _inherit = 'pos.config'

  address = fields.Char(string='Address')
  supervisor = fields.Char(string='Supervisor')