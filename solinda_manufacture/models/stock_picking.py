from odoo import _, api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    mrp_prod_id = fields.Many2one('mrp.production', string="Production")
