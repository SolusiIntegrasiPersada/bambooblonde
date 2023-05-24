from odoo import fields, api, models,_
from datetime import datetime, date
from odoo.exceptions import ValidationError

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def show_picking(self):
        if self.move_id.purchase_id:
            return self.move_id.purchase_id.action_view_picking()

    
    