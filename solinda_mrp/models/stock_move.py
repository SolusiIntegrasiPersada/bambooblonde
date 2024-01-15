from odoo import models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def show_picking(self):
        if self.move_id.purchase_id:
            return self.move_id.purchase_id.action_view_picking()
