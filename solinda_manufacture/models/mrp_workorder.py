from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import get_lang


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    order_id = fields.Many2one(comodel_name='purchase.order', string='PO', copy=False)
    supplier = fields.Many2one(comodel_name='res.partner', string='Supplier')
    fabric_id = fields.Many2many(comodel_name='mrp.bom.line', string='Fabric', related='operation_id.fabric_id')
    hk = fields.Float(string='HK', related='operation_id.hk')
    color_id = fields.Many2one(comodel_name='product.attribute.value', string='Color',
                               domain="[('attribute_id.name','=', 'COLOR')]", store=True)
    shrinkage = fields.Float(string='Shkg(%)', default=0.0)
    duration_expected = fields.Float(
        'Expected Duration',
        digits=(16, 2),
        default=1.0,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help='Expected duration (in minutes)')

    # qty_production = fields.Float(string='Qty', related='production_id.total_qty')
    in_date = fields.Date('In Date')
    out_date = fields.Date('Out Date')
    picking_ids = fields.Many2many('stock.picking', string='Receive', related='order_id.picking_ids')
    total_dyeing = fields.Float(string='Total Dyeing')
    total_mtr = fields.Float(string='Total Mtr', compute='_compute_total_meter')
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)
    cost_service = fields.Float(string='Cost Service', related='operation_id.cost_service', store=True)
    customer = fields.Char(string='Customer', related='production_id.seq_report', store=True)
    po_date = fields.Datetime(string='PO Date', related='order_id.date_approve')
    keterangan = fields.Selection(selection=[('person', 'Individual'), ('company', 'Company')], string='Keterangan',
                                  related='production_id.customer.company_type')
    product_tmpl_id = fields.Many2one('product.template', string='Product', related='product_id.product_tmpl_id')
    mrp_payment_id = fields.Many2one('mrp.payment', string='Payment')
    total_receipt = fields.Float(string='Total Receipt',)

    @api.depends('production_id', 'fabric_id')
    def _compute_total_meter(self):
        for record in self:
            product_ids = record.fabric_id.mapped('product_id.id')
            product_meter = record.production_id.move_raw_ids.filtered(lambda l: l.product_id.id in product_ids)
            total_meter = sum(product_meter.mapped('product_uom_qty'))
            if record.workcenter_id.is_dyeing:
                record.update({
                    'total_mtr': total_meter if total_meter else 0
                })
            else:
                record.update({
                    'total_mtr': 0
                })

    @api.depends('total_dyeing', 'hk', 'qty_production', 'cost_service', 'fabric_id', 'production_id.total_qty')
    def _compute_total_cost(self):
        for line in self:
            if line.total_dyeing:
                line.total_cost = line.total_dyeing * line.cost_service
            else:
                line.total_cost = line.production_id.total_qty * line.hk * line.cost_service
            if line.workcenter_id.name == 'CUTTING':
                line.total_cost = line.production_id.total_qty * len(line.fabric_id) * line.cost_service
            if line.workcenter_id.name == 'SEWING':
                line.total_cost = line.production_id.total_qty * line.cost_service

    def show_receive_po(self):
        self.order_id.action_view_picking()
        return self.order_id.action_view_picking()

    def show_po(self):
        if not self.order_id:
            raise ValidationError('PO is not defined!\nPlease create PO first')
        return {
            'name': _('Purchase Order'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            # 'target': 'new',
            'res_id': self.order_id.id,
        }

    def button_start(self):
        self.ensure_one()
        if any(not time.date_end for time in self.time_ids.filtered(lambda t: t.user_id.id == self.env.user.id)):
            return True
        # As button_start is automatically called in the new view
        if self.state in ('done', 'cancel'):
            return True

        if self.product_tracking == 'serial':
            self.qty_producing = 1.0
        else:
            self.qty_producing = self.qty_remaining

        self.env['mrp.workcenter.productivity'].create(
            self._prepare_timeline_vals(self.duration, datetime.now())
        )
        if self.production_id.state != 'progress':
            self.production_id.write({
                'date_start': datetime.now(),
            })
        if self.state == 'progress':
            return True
        start_date = datetime.now()
        vals = {
            'state': 'progress',
            'date_start': start_date,
        }
        if not self.leave_id:
            leave = self.env['resource.calendar.leaves'].create({
                'name': self.display_name,
                'calendar_id': self.workcenter_id.resource_calendar_id.id,
                'date_from': start_date,
                'date_to': start_date + relativedelta(minutes=self.duration_expected),
                'resource_id': self.workcenter_id.resource_id.id,
                'time_type': 'other'
            })
            vals['leave_id'] = leave.id
            return self.write(vals)
        else:
            if self.date_planned_start > start_date:
                vals['date_planned_start'] = start_date
            if self.date_planned_finished and self.date_planned_finished < start_date:
                vals['date_planned_finished'] = start_date
            return self.with_context(bypass_duration_calculation=True).write(vals)

    def create_po(self):
        for record in self.sudo():
            workorder_name = ['DYEING', 'WASHING', 'PRINTING']
            if not record.supplier:
                raise ValidationError('Please input the supplier first')
            if not record.out_date:
                raise ValidationError('Please input Out Date first')
            if not record.total_dyeing and (record.workcenter_id.name.upper() in workorder_name):
                raise ValidationError('Please input Total Dyeing in operation Dyeing, Washing, or Printing')

            raw_po_line, updt_variant = [], []
            total_quant = sum(record.production_id.purchase_id.order_line.mapped('product_qty'))
            record.button_start()

            po = record.env['purchase.order'].create({
                'partner_id': record.supplier.id,
                'state': 'draft',
                'date_approve': datetime.now(),
                'is_po_service': True
            })
            if po:
                record.order_id = po.id
            if not record.workcenter_id.product_service_id:
                raise ValidationError(
                    'Default product in Workcenter is not defined!\nPlease input product in workcenter as default when create PO from Work Order')

            product_qty = record.total_dyeing if record.workcenter_id.is_dyeing else record.production_id.move_raw_ids[0].po_qty
            raw_po_line.append((0, 0, {
                'product_id': record.workcenter_id.product_service_id.id,
                'name': record.workcenter_id.product_service_id.name,
                'price_unit': record.cost_service,
                # 'fabric': record.fabric_id.product_id.name,
                'product_qty': product_qty,
                'comment_bool': True,
                'color_mo': record.color_id.name,
                'material_ids': record.fabric_id.ids,
                'image': record.product_id.image_1920,
            }))
            for d in record.production_id.by_product_ids:
                updt_variant.append([0, 0, {
                    'name': d.product_id.id,
                    'fabric': d.fabric_por_id.id,
                    'lining': d.lining_por_id.id,
                    'color': d.colour,
                    'size': d.size,
                    'product_qty': d.product_uom_qty,
                    'price_unit': record.cost_service,
                    'image': d.product_id.image_1920,
                }])
            po.update({
                'order_line': raw_po_line,
                'pw_ids': updt_variant,
                'sub_suplier': record.supplier.category_id.ids,
                'sample_order_no': record.production_id.name,
                'product_mo': record.production_id.product_tmpl_id.name,
                'is_sample': record.production_id.is_sample,
                'hide_field': True,
                'picking_type_id': record.production_id.picking_type_id.id,
            })
            for pol in po.order_line:
                product_lang = pol.product_id.with_context(
                    lang=get_lang(pol.env, pol.partner_id.lang).code,
                    partner_id=pol.partner_id.id,
                    company_id=pol.company_id.id,
                )
                pol.name = pol._get_product_purchase_description(product_lang)

            record.create_workorder_moves(finish=False)
            po.button_confirm()
            record.production_id.update_qty_consume_with_variant_wo()
            record.show_po()

    def create_po_action(self):
        self.ensure_one()
        if any(not time.date_end for time in self.time_ids.filtered(lambda t: t.user_id.id == self.env.user.id)):
            return True

        # As button_start is automatically called in the new view
        if self.state in ('done', 'cancel'):
            return True

        if self.product_tracking == 'serial':
            self.qty_producing = 1.0
        else:
            self.qty_producing = self.qty_remaining
        self.env['mrp.workcenter.productivity'].create(
            self._prepare_timeline_vals(self.duration, datetime.now())
        )
        if self.production_id.state != 'progress':
            self.production_id.write({
                'date_start': datetime.now(),
            })
        if self.state == 'progress':
            return True

        start_date = datetime.now()

        if not self.supplier:
            raise ValidationError('Please Input Supplier first!')

        vals = {
            'state': 'progress',
            'date_start': start_date,
        }
        po = self.env['purchase.order'].create({
            'partner_id': self.supplier.id,
            'state': 'purchase',
            'date_approve': start_date,
        })

        if not self.workcenter_id.product_service_id:
            raise ValidationError("""Product Service in this Workcenter hasn't been set""")

        self.env['purchase.order.line'].create({
            'product_id': self.workcenter_id.product_service_id.id,
            'product_qty': self.qty_producing,
            'order_id': po.id,
        })
        vals['order_id'] = po.id
        if not self.leave_id:
            leave = self.env['resource.calendar.leaves'].create({
                'name': self.display_name,
                'calendar_id': self.workcenter_id.resource_calendar_id.id,
                'date_from': start_date,
                'date_to': start_date + relativedelta(minutes=self.duration_expected),
                'resource_id': self.workcenter_id.resource_id.id,
                'time_type': 'other'
            })
            vals['leave_id'] = leave.id
            return self.write(vals)
        else:
            if self.date_planned_start > start_date:
                vals['date_planned_start'] = start_date
            if self.date_planned_finished and self.date_planned_finished < start_date:
                vals['date_planned_finished'] = start_date
            return self.with_context(bypass_duration_calculation=True).write(vals)

    def create_workorder_moves(self, finish):
        """
        Sub function to create moves based on status of the workorder
        If it triggered from create PO, then finish = false
        """
        for record in self:
            virtual_location = self.env['stock.location'].search(
                [('usage', '=', 'production'), ('company_id', '=', record.company_id.id)])
            location_id = virtual_location.id if finish else record.production_id.location_src_id.id
            location_dest_id = record.production_id.location_src_id.id if finish else virtual_location.id
            date = record.in_date if finish else record.out_date
            qty_receive = sum(record.order_id.picking_ids.move_ids_without_package.mapped('quantity_done'))
            qty = qty_receive if finish else record.total_dyeing
            for material in record.fabric_id:
                move_raw = record.production_id.move_raw_ids.filtered(
                    lambda l: l.product_id.id == material.product_id.id)

                move = self.env['stock.move'].create({
                    'name': record.production_id.name,
                    'date': date if date else datetime.now(),
                    'location_id': location_id,
                    'location_dest_id': location_dest_id,
                    'product_id': move_raw.product_id.id,
                    'product_uom': move_raw.product_uom.id,
                    'product_uom_qty': qty,
                    'production_id': record.production_id.id,
                    'workorder_notes': f'{record.name} - {record.production_id.name}'
                })
                move._action_confirm(merge=False)
                move._action_assign()
                move.move_line_ids.write({'qty_done': move_raw.product_uom_qty})
                move._action_done()

    def button_finish(self):
        """
        Function to inherit button finish and automatically creates stock_move based on pair with
        MRP Workorder create_po function
        """
        res = super(MrpWorkorder, self).button_finish()
        self.create_workorder_moves(finish=True)
        return res
