from odoo import _, api, fields, models
from odoo.tools import float_compare, float_round, float_is_zero, OrderedSet


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    by_product_ids = fields.One2many('by.product.dummy', 'mrp_id', string='By Product')
    purchase_request_id = fields.Many2one('purchase.request', string='Sample Development')
    is_sample = fields.Boolean('Is Sample')
    mrp_bom_variant_ids = fields.One2many('mrp.production.bom.variant', 'production_id', 'Material Variant', copy=True)
    total_qty = fields.Float(string="Total Qty", compute="_compute_total_qty_dummy", store=True)
    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost", store=True)
    retail_price = fields.Float(related='bom_id.retail_price', string='Retail Price', store=True)
    roi = fields.Float(string="ROI", compute="_compute_roi")
    service_ids = fields.One2many('service.return', 'mrp_id', string='Service')
    stock_picking_id = fields.Many2one('stock.picking', string="Stock")
    count_service = fields.Integer(string="Count", compute="_compute_count_service")

    @api.depends('move_finished_ids')
    def _compute_move_byproduct_ids(self):
        for order in self:
            order.move_byproduct_ids = order.move_finished_ids.ids

    @api.depends('retail_price', 'total_cost', 'total_qty')
    def _compute_roi(self):
        for line in self:
            total_wholesale = line.retail_price * line.total_qty
            if total_wholesale:
                line.roi = (total_wholesale - line.total_cost) * 100 / total_wholesale
            else:
                line.roi = 0

    @api.depends('move_raw_ids.total_cost', 'workorder_ids.total_cost')
    def _compute_total_cost(self):
        for line in self:
            total_material = 0
            total_operation = 0
            total = 0
            for move in line.move_raw_ids:
                total_material += move.total_cost
            for op in line.workorder_ids:
                total_operation += op.total_cost
            total = total_operation + total_material
            line.total_cost = total

    @api.depends('by_product_ids.product_uom_qty')
    def _compute_total_qty_dummy(self):
        for by in self:
            if by.by_product_ids:
                total = 0
                for line in by.by_product_ids:
                    total += line.product_uom_qty
                by.total_qty = total
            else:
                by.total_qty = 0

    @api.constrains('move_raw_ids')
    def _constrains_supplier_material(self):
        if self.bom_id and self.move_raw_ids:
            for move in self.move_raw_ids:
                for var in self.mrp_bom_variant_ids:
                    if var.product_id.id == move.product_id.id:
                        var.supplier = move.supplier.id

    @api.onchange('move_raw_ids')
    def _onchange_supplier_material(self):
        if self.bom_id and self.move_raw_ids:
            for move in self.move_raw_ids:
                for var in self.mrp_bom_variant_ids:
                    if var.product_id.id == move.product_id.id:
                        var.supplier = move.supplier.id

    def update_qty_consume_with_variant(self):
        for move in self.move_raw_ids:
            qty_consume = 0
            qty_po = 0
            qty_pr = 0
            po_qty = 0
            # for var in self.mrp_bom_variant_ids:
            #     if move.product_id.id == var.product_id.id:
            #         po_qty += var.po_qty
            move.po_qty = self.purchase_id.total_purchase_qty
            move.product_uom_qty = move.po_qty * move.hk
            # move.quantity_done = move.product_uom_qty
            move.supplier = move.bom_line_id.supplier
            move.color_id = move.bom_line_id.color
            move.cost_material = move.bom_line_id.cost_material

    def update_qty_consume_with_variant_pr(self):
        for move in self.move_raw_ids:
            qty_consume = 0
            qty_po = 0
            qty_pr = 0
            po_qty = 0
            # for var in self.mrp_bom_variant_ids:
            #     if move.product_id.id == var.product_id.id:
            #         po_qty += var.po_qty
            move.po_qty = self.purchase_request_id.total_purchase_qty
            move.product_uom_qty = move.po_qty * move.hk
            # move.quantity_done = move.product_uom_qty
            move.supplier = move.bom_line_id.supplier
            move.color_id = move.bom_line_id.color
            move.cost_material = move.bom_line_id.cost_material

    def update_qty_consume_with_variant_wo(self):
        for move in self.move_raw_ids:
            qty_consume = 0
            po_qty = 0
            for var in self.mrp_bom_variant_ids:
                if move.product_id.id == var.product_id.id:
                    po_qty += var.po_qty
            move.po_qty = po_qty
            move.product_uom_qty = move.po_qty * move.hk
            move.quantity_done = move.product_uom_qty
            # self.qty_po = po_qty

    def update_qty_variant(self):
        if self.mrp_bom_variant_ids:
            self.mrp_bom_variant_ids.unlink()

        variant_ids = []
        for i in self:
            # purchase_obj = self.purchase_id.search([('')])
            for b in i.bom_id.bom_line_variant_ids:
                qty_po = 0
                sizes = b.sizes.strip('()')
                purchase = self.env["purchase.order"].search([('id', '=', self.purchase_id.id)], limit=1)
                order_line_sizes = [(line.size.strip(' '), line.product_qty) for line in purchase.order_line]

                for size, product_qty in order_line_sizes:
                    if size == sizes:
                        qty_po = product_qty
                        break

                variant_ids.append((0, 0, {
                    'product_id': b.product_id.id,
                    'product_qty': b.product_qty,
                    'po_qty': qty_po,
                    'product_uom_id': b.product_uom_id.id,
                    'supplier': b.supplier.id,
                    'ratio': b.ratio,
                    'sizes': b.sizes,
                    'color': b.color,
                    # 'shrinkage' : b.shrinkage,
                    # 'total_qty' : total_qty,
                }))


        i.mrp_bom_variant_ids = variant_ids

    def _create_workorder(self):
        for production in self:
            if not production.bom_id or not production.product_id:
                continue
            workorders_values = []

            product_qty = production.product_uom_id._compute_quantity(
                production.product_qty, production.bom_id.product_uom_id)
            exploded_boms, dummy = production.bom_id.explode(
                production.product_id, product_qty / production.bom_id.product_qty, picking_type=production.bom_id.picking_type_id)

            for bom, bom_data in exploded_boms:
                # If the operations of the parent BoM and phantom BoM are the same, don't recreate work orders.
                if not (bom.operation_ids and (
                        not bom_data['parent_line'] or
                        bom_data['parent_line'].bom_id.operation_ids != bom.operation_ids)):
                    continue
                for operation in bom.operation_ids:
                    accessories_ids = []
                    for accessories in operation.fabric_id:
                        accessories_ids.append((4, accessories.id, None))

                    if operation._skip_operation_line(bom_data['product']):
                        continue
                    workorders_values += [{
                        'name': operation.name,
                        'production_id': production.id,
                        'supplier': operation.supplier.id,
                        'workcenter_id': operation.workcenter_id.id,
                        'product_uom_id': production.product_uom_id.id,
                        'operation_id': operation.id,
                        'state': 'pending',
                        'color_id': operation.color_id.id,
                        'fabric_id': accessories_ids,
                    }]

            production.workorder_ids = [(5, 0)] + [(0, 0, value) for value in workorders_values]
            for workorder in production.workorder_ids:
                workorder.duration_expected = workorder._get_duration_expected()

    @api.depends('stock_picking_id')
    def _compute_count_service(self):
        self = self.sudo()
        for i in self:
            i.count_service = len(i.stock_picking_id)

    def view_action_service(self):
        updt = []
        for i in self:
            i.ensure_one()
            if i.stock_picking_id:
                return {
                    'name': 'Service',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                    'res_model': 'stock.picking',
                    'res_id': i.stock_picking_id.id,
                    'domain': [('mrp_prod_id', '=', self.id)],
                }
            else:
                picking_type = self.env['stock.picking.type'].search([('name', '=', 'Service to Vendor')], limit=1).id
                loc_dest = self.env['stock.location'].search([('complete_name', '=', 'Partner Locations/Vendors')]).id
                for rec in self.by_product_ids:
                    updt.append([0, 0, {
                        'product_id': rec.product_id.id,
                        'name': rec.product_id.name,
                        'product_uom': rec.product_uom_id,
                        'location_id': i.location_dest_id.id,
                        'location_dest_id': loc_dest,
                    }])
                stock = self.env['stock.picking'].create({
                    'mrp_prod_id': self.id,
                    'style_name': self.product_tmpl_id.name,
                    'picking_type_id': picking_type,
                    'location_id': self.location_dest_id.id,
                    'location_dest_id': loc_dest,
                })
                stock.update({
                    'move_ids_without_package': updt,
                })
                if stock:
                    i.stock_picking_id = stock.id
                    return {
                        'name': 'Service',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'stock.picking',
                        'res_id': stock.id,
                        # 'context': {'default_mrp_prod_id':self.id},
                    }


class ServiceReturn(models.Model):
    _name = 'service.return'
    _description = 'Service Return'

    mrp_id = fields.Many2one('mrp.production', string="MRP")


class ByProductDummy(models.Model):
    _name = 'by.product.dummy'
    _description = 'By Product Dummy'

    product_id = fields.Many2one('product.product', string='Product')
    product_uom_id = fields.Many2one('uom.uom', string='UoM')
    product_uom_qty = fields.Float(string='Produce', default=1)
    product_minus = fields.Float(string='Not Produce')
    colour = fields.Char('Color')
    size = fields.Char('Size')
    remarks = fields.Text('Remarks')
    mrp_id = fields.Many2one('mrp.production', string='MRP')
    fabric_por_id = fields.Many2one('product.product', string='Fabric')
    lining_por_id = fields.Many2one('product.product', string='Lining')

    ###
    total_value = fields.Float(string="Total Value")

    @api.onchange('product_minus')
    def _onchange_product_minus(self):
        for i in self:
            if i.product_minus > 0:
                by_prod = self.env["stock.move"].search(
                    [('product_id', '=', self.product_id.id), ('production_id', '=', self._origin.mrp_id.id)], limit=1)
                if by_prod:
                    by_prod.product_uom_qty = self.product_uom_qty - i.product_minus
                else:
                    self.mrp_id.product_qty = self.mrp_id.product_qty - i.product_minus

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        by_prod = self.env["stock.move"].search(
            [('product_id', '=', self.product_id.id), ('production_id', '=', self._origin.mrp_id.id)], limit=1)
        if by_prod:
            by_prod.product_uom_qty = self.product_uom_qty
        else:
            self.mrp_id.product_qty = self.product_uom_qty


class MrpProductionBomVariant(models.Model):
    _name = 'mrp.production.bom.variant'
    _order = "sequence, id"
    _rec_name = "product_id"
    _description = 'Bill of Material MRP (Variant)'

    @api.depends('product_qty', 'cost')
    def _compute_total_material(self):
        for line in self:
            line.total_material = line.cost * line.product_qty

    company_id = fields.Many2one(
        related='production_id.company_id', store=True, index=True, readonly=True)
    product_id = fields.Many2one('product.product', 'Component', required=True)
    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits='Product Unit of Measure', required=True)
    po_qty = fields.Float(
        'Qty PO', default=0.0,
        digits='Product Unit of Measure', required=True)
    total_qty = fields.Float(
        'Total', default=0.0,
        digits='Product Unit of Measure', required=True)
    product_uom_id = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        required=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control")
    sequence = fields.Integer(
        'Sequence', default=1,
        help="Gives the sequence order when displaying.")
    production_id = fields.Many2one(
        'mrp.production', 'MRP Production',
        index=True, ondelete='cascade', required=True)
    supplier = fields.Many2one('res.partner', string='Supplier')
    color = fields.Char('Color')
    sizes = fields.Char('Sizes')
    ratio = fields.Float(string='Ratio', default=1.00)
    cost = fields.Float(string="Cost", related='product_id.standard_price')
    total_material = fields.Float(string="Total Material", compute=_compute_total_material)
    shrinkage = fields.Float(string='Shkg(%)')

