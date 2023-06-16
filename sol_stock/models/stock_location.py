from odoo import fields, models, api

class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_transit = fields.Boolean(string="Is a Transit Location", default=False)
