from odoo import _, api, fields, models

class VisitorRegion(models.Model):
    _name = 'visitor.region'
    _description = 'Visitor Region'
    
    name = fields.Char('Name')
    sequence = fields.Integer('Sequence')


class PosOrder(models.Model):
    _inherit = 'pos.order'

    region_id = fields.Many2one('visitor.region', string='Nationality')
    
    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['region_id'] = ui_order['region_id']['id'] if ui_order['region_id'] else False
        return order_fields
