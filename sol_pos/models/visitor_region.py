from odoo import fields, models


class VisitorRegion(models.Model):
    _name = 'visitor.region'
    _description = 'Visitor Region'
    
    name = fields.Char('Name')
    sequence = fields.Integer('Sequence')