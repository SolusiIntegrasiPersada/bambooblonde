from odoo import models, fields

class MrpPayment(models.Model):
    _name = 'mrp.payment'
    _description = 'MRP Payment'

    name = fields.Char(string="Name Payment")