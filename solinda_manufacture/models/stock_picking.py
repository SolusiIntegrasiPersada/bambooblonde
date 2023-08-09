from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    mrp_prod_id = fields.Many2one('mrp.production', string="Production")

    def button_validate(self):
        """
        Inheriting validate function to altering shrinkage if it does come from workorder PO
        """
        res = super(StockPicking, self).button_validate()
        for record in self:
            for move in record.move_ids_without_package.filtered(lambda l: l.quantity_done):
                workorder = self.env['mrp.workorder'].search([('order_id', '=', move.purchase_line_id.order_id.id)])
                if not workorder or move.quantity_done == move.product_uom_qty:
                    continue

                shrinkage = 1 - (move.quantity_done / move.product_uom_qty)
                workorder.sudo().write({
                    'shrinkage': shrinkage
                })
        return res
