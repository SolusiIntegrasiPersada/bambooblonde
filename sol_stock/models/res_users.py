from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    default_warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='Default Warehouse')

