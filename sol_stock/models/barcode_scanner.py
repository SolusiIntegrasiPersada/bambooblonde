from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        if barcode:
            for picking in self:
                if picking.picking_type_id.code == 'internal' and picking.state == 'draft':
                    product = self.env['product.product'].search([("barcode", "=", barcode)])

                    if product:
                        if len(product) > 1:
                            raise UserError(f'Product dengan Barcode {barcode} ada {len(product)}')

                        search_move = picking.move_ids_without_package.filtered(lambda x: x.product_id.id == product.id)

                        if search_move:
                            search_move.write({'product_uom_qty': search_move.product_uom_qty + 1})

                        else:
                            picking.move_ids_without_package = [
                                (0, 0, {
                                    'product_id': product.id,
                                    'price': product.standard_price,
                                    'product_uom_qty': 1,
                                    'location_id': picking.location_id.id,
                                    'location_dest_id': picking.location_dest_id.id,
                                    'picking_id': picking.id,
                                })
                            ]
                            
                            search_move = picking.move_ids_without_package.filtered(lambda x: x.product_id.id == product.id)
                            search_move._onchange_product_id()

                    else:
                        raise UserError(f'Product dengan Barcode {barcode} tidak ada')

        return

