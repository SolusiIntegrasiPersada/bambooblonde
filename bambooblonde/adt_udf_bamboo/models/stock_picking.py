from odoo import fields, models, api, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta

# ================== stock picking ==================

class StockPicking(models.Model):
    _inherit='stock.picking'

    def kirim_barang (self):
        for record in self :
            if record.sale_id :
                for rec in record.move_line_ids_without_package :
                    mp_obj = self.env['mrp.production'].search([('sales_order_id','=',record.sale_id.id)])
                    po_obj = self.env['purchase.order'].search([('id','=',mp_obj.purchase_id.id)])
                    receipt_obj = self.env['stock.picking'].search([('origin','=',po_obj.name)])
                    move_obj = self.env['stock.move'].search([('picking_id','=',receipt_obj.id)])
                    for move in move_obj :
                        if move.product_id.id == rec.product_id.id:
                            move_line_id = self.env['stock.move.line'].sudo().create({
                                'move_id' : move.id,
                                'picking_id' : move.picking_id.id,
                                'company_id' : move.company_id.id,
                                'date' : rec.date,
                                'location_dest_id' : move.location_dest_id.id,
                                'location_id' : move.location_id.id,
                                'product_uom_id' : move.product_uom.id,
                                'product_uom_qty' : rec.product_uom_qty,
                                'product_id' : move.product_id.id,
                                'qty_done' : rec.qty_done,
                                })
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self.kirim_barang()
        return res


        