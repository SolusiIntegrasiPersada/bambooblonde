from odoo import fields, models, api

class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_transit = fields.Boolean(string="Is a Transit Location?", default=False)
    is_foc = fields.Boolean(string="Is a FOC Location?", default=False)
    address = fields.Char(string="Address")
    phone = fields.Char(string="Phone/Fax")
