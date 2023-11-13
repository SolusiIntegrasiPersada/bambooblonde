from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.tools import float_round


class StockMove(models.Model):
    _inherit = 'stock.move'

    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost')
    supplier = fields.Many2one(comodel_name='res.partner', string='Supplier')
    color = fields.Many2one(comodel_name='dpt.color', string='Color')
    color_id = fields.Many2one(
        comodel_name='product.attribute.value',
        string='Color',
        domain="[('attribute_id.name','=', 'COLOR')]",
        ondelete='cascade')
    service = fields.Char(string='Fabric', default='FABRIC', readonly=True)
    hk = fields.Float(string='HK', related='bom_line_id.product_qty')
    purchase_id = fields.Many2one('purchase.order', string='Purchase')
    total_buy = fields.Float(string='Total Buy')
    po_qty = fields.Float(string='Qty PO')
    is_sample = fields.Boolean(string='Is Sample', related='raw_material_production_id.is_sample')
    mrp_payment_id = fields.Many2one('mrp.payment', string='Payment')
    cost_material = fields.Float(string='Cost')
    workorder_notes = fields.Char(string='Workorder')

    # Conversion Yard to M
    uom_cost = fields.Many2one('uom.uom', string="UoM", default=lambda self: self.env['uom.uom'].search([('name', '=', 'm')], limit=1))
    uom_total_buy = fields.Many2one('uom.uom', string="UoM", domain="[('category_id', '=', product_uom_category_id)]")
    to_consume_conversion = fields.Float(string="Conversion", compute="_conversion_to_yard")
    to_consume_uom = fields.Many2one('uom.uom', string="UoM", default=lambda self: self.env['uom.uom'].search([('name', '=', 'yard')], limit=1))

    @api.depends('product_uom_qty')
    def _conversion_to_yard(self):
        yard = 0.9144
        for i in self:
            total = i.product_uom_qty / yard
            i.to_consume_conversion = total

    @api.depends('raw_material_production_id.qty_producing', 'product_uom_qty', 'product_uom')
    def _compute_should_consume_qty(self):
        for move in self:
            mo = move.raw_material_production_id
            if not mo or not move.product_uom:
                move.should_consume_qty = 0
                continue
            move.should_consume_qty = float_round(
                (mo.qty_producing - mo.qty_produced) * move.unit_factor, precision_rounding=move.product_uom.rounding)
            if move.product_uom_qty > 0:
                move.should_consume_qty = move.product_uom_qty

    def button_done(self):
        self._action_done()

    def show_receive_po(self):
        self.purchase_id.action_view_picking()
        return self.purchase_id.action_view_picking()

    def show_po(self):
        if not self.purchase_id:
            raise ValidationError('PO is not defined!\nPlease create PO first')
        return {
            'name': _('Purchase Order'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            # 'target': 'new',
            'res_id': self.purchase_id.id,
        }

    def create_po(self):
        for i in self.sudo():
            raw_po_line = []
            # total_quant = i.product_qty
            total_quant = i.total_buy
            yard = 0.9144
            if i.uom_total_buy.name == 'yard':
                total_yard = i.cost_material * yard
            else:
                total_yard = i.cost_material

            if not total_quant:
                raise ValidationError('Total buy cannot be 0')

            if not i.supplier:
                raise ValidationError('Please input the supplier first')

            po = i.env['purchase.order'].create({
                'partner_id': i.supplier.id,
                'state': 'draft',
                'date_approve': datetime.now()
            })
            picking = po._get_picking_type(self.env.context.get('company_id') or self.env.company.id)
            # picking = i.raw_material_production_id.picking_type_id.id
            # picking = i.env['stock.picking.type'].search([('barcode', '=', 'WHFG-RECEIPTS')],limit=1)
            if not picking:
                raise ValidationError('WHFG-RECEIPTS is not defined!')
            if po:
                i.purchase_id = po.id
            raw_po_line.append((0, 0, {
                'product_id': i.product_id.id,
                # 'fabric': i.fabric_id.product_id.name,
                # 'lining':'',
                'color_mo': i.color_id.name,
                'product_qty': total_quant,
                'price_unit': total_yard,
                'image': i.raw_material_production_id.product_tmpl_id.image_1920,
                'product_uom': i.uom_total_buy.id,
                # 'material_ids': i.product_id.id,
            }))
            po.update({
                'order_line': raw_po_line,
                # 'picking_type_id': picking,
                'sample_order_no': i.name,
                'product_mo': i.raw_material_production_id.product_id.name,
                'is_sample': i.raw_material_production_id.is_sample,
                'hide_field': True,
                'picking_type_id': i.raw_material_production_id.picking_type_id.id,
            })
            po.button_confirm()
            for picking in po.picking_ids:
                for move in picking.move_ids_without_package:
                    move.update({
                        'raw_material_production_id': None
                    })
            
            if i.company_id.id == 1 :
                sql_query = """
                    select id from stock_picking where origin = %s and company_id = 1
                    """
                self.env.cr.execute(sql_query, (po.name,))
                id_picking = self.env.cr.dictfetchall()
                id_picking = id_picking[0]['id']

                sql_query = """
                    update stock_picking set location_dest_id = %s where id = %s
                    """
                self.env.cr.execute(sql_query, (8,id_picking,))

                sql_query = """
                    update stock_move set location_dest_id = %s where picking_id = %s
                    """
                self.env.cr.execute(sql_query, (8,id_picking,))

                sql_query = """
                    update stock_move_line set location_dest_id = %s where picking_id = %s
                    """
                self.env.cr.execute(sql_query, (8,id_picking,))
                x=1

            return i.show_po()

    @api.depends('product_id.standard_price', 'product_uom_qty', 'hk', 'total_buy', 'uom_total_buy')
    def _compute_total_cost(self):
        for line in self:
            line.update({
                'total_cost': line.cost_material * (
                    line.total_buy if line.total_buy else line.product_uom_qty)
            })



class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    workorder_ids = fields.Many2many(
        comodel_name='mrp.workorder',
        string='Work Orders',
        compute='compute_mrp_workorders'
    )
    workorder_notes = fields.Char(string='Workorder', related='move_id.workorder_notes')

    def compute_mrp_workorders(self):
        for rec in self:
            workorder_list = []
            if rec.production_id:
                sql = '''SELECT w.id as workorder_id FROM mrp_workorder w WHERE w.production_id=%s''' % (
                    rec.production_id.id)
                self.env.cr.execute(sql)
                workorder_ids = self.env.cr.dictfetchall()
                for w in workorder_ids:
                    workorder_list.append((4, w['workorder_id'], None))
            rec.workorder_ids = workorder_list
