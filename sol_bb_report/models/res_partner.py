from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    customer_initial = fields.Char(string='Initial')