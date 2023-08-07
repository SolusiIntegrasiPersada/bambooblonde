from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import formatLang, get_lang, format_amount

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    order_id = fields.Many2one(comodel_name='purchase.order',string='PO')
    supplier = fields.Many2one(comodel_name='res.partner',related="operation_id.supplier", string='Supplier')
    fabric_id = fields.Many2many(comodel_name='mrp.bom.line',string='Fabric', related='operation_id.fabric_id')
    # accessories_ids = fields.Many2many(comodel_name='product.product', string='Accessories', domain="""[('type', 'in', ['product', 'consu']),'|',('company_id', '=', False),('company_id', '=', company_id)]""", check_company=True)
    hk = fields.Float(string='HK', related='operation_id.hk')
    color_id = fields.Many2one(comodel_name='product.attribute.value', string='Color', domain="[('attribute_id.name','=', 'COLOR')]", store=True)
    shrinkage = fields.Float(string='Shkg(%)', default=0.0)
    duration_expected = fields.Float(
        'Expected Duration',
        digits=(16, 2),
        default=1.0,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Expected duration (in minutes)")
    
    # qty_production = fields.Float(string="Qty", related='production_id.total_qty')
    in_date = fields.Date('In Date')
    out_date = fields.Date('Out Date')
    picking_ids = fields.Many2many('stock.picking', string='Receive',related="order_id.picking_ids")
    total_dyeing = fields.Float(string='Total Dyeing')
    total_mtr = fields.Float(string='Total Mtr', compute="_compute_total_meter")
    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost", store=True)
    cost_service = fields.Float(string='Cost Service', related='operation_id.cost_service', store=True)
    customer = fields.Char(string='Customer', related='production_id.seq_report', store=True)
    po_date = fields.Datetime(string='PO Date', related='order_id.date_approve')
    keterangan = fields.Selection(selection=[('person', 'Individual'), ('company', 'Company')], string='Keterangan', related='production_id.customer.company_type')
    product_tmpl_id = fields.Many2one('product.template', string='Product', related='product_id.product_tmpl_id')
    mrp_payment_id = fields.Many2one('mrp.payment', string="Payment")

    # @api.depends('fabric_id', 'production_id.qty_po', 'hk')
    # def _compute_total_mtr(self):
    #     for line in self:
    #         line.total_mtr = line.production_id.qty_po * line.hk

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
            if line.workcenter_id.name == "CUTTING":
                line.total_cost = line.production_id.total_qty * len(line.fabric_id) * line.cost_service
            if line.workcenter_id.name == "SEWING":
                line.total_cost = line.production_id.total_qty * line.cost_service


    def show_receive_po(self):
        self.order_id.action_view_picking()
        return self.order_id.action_view_picking()

    def show_po(self):
        if not self.order_id:
            raise ValidationError("PO is not defined!\nPlease create PO first")
        return {
                'name': _("Purchase Order"),
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
        self = self.sudo()
        for i in self:
            raw_po_line,updt_variant = [],[]
            total_quant = sum(i.production_id.purchase_id.order_line.mapped('product_qty'))
            i.button_start()
            if not i.supplier:
                raise ValidationError("Please input the supplier first")
            if not i.out_date:
                raise ValidationError("Please input Out Date first")
            if not i.total_dyeing and (i.workcenter_id.name == "DYEING" or i.workcenter_id.name == "WASHING" or i.workcenter_id.name == "PRINTING"):
                raise ValidationError("Please input Total Dyeing in operation Dyeing, Washing, or Printing")
            po = i.env['purchase.order'].create({'partner_id': i.supplier.id,'state': 'draft','date_approve': datetime.now(), 'is_po_service': True})
            if po:
                i.order_id = po.id
            if not i.workcenter_id.product_service_id:
                raise ValidationError("Default product in Workcenter is not defined!\nPlease input product in workcenter as default when create PO from Work Order")
            
            product_qty = total_quant
            if i.workcenter_id.is_dyeing:
                product_qty = i.total_dyeing
            else:
                product_qty = i.production_id.product_qty
            raw_po_line.append((0,0, {
                'product_id': i.workcenter_id.product_service_id.id,
                'name': i.workcenter_id.product_service_id.name,
                'price_unit': i.cost_service,
                # 'fabric': i.fabric_id.product_id.name,
                'product_qty': product_qty,
                'comment_bool': True,
                'color_mo': i.color_id.name,
                'material_ids': i.fabric_id.ids,
                'image': i.product_id.image_1920,
            }))
            for d in i.production_id.by_product_ids:
                updt_variant.append([0,0,{
                'name': d.product_id.id,
                'fabric': d.fabric_por_id.id,
                'lining': d.lining_por_id.id,
                'color': d.colour,
                'size': d.size,
                'product_qty': d.product_uom_qty,
                'price_unit': i.cost_service,
                'image': d.product_id.image_1920,
                }])           
            po.update({
                "order_line": raw_po_line,
                'pw_ids': updt_variant,
                'sub_suplier': i.supplier.category_id.ids,
                'sample_order_no': i.production_id.name,
                'product_mo': i.production_id.product_tmpl_id.name,
                'is_sample': i.production_id.is_sample,
                'hide_field': True,
                })
            for pol in po.order_line:
                product_lang = pol.product_id.with_context(
                    lang=get_lang(pol.env, pol.partner_id.lang).code,
                    partner_id=pol.partner_id.id,
                    company_id=pol.company_id.id,
                )
                pol.name = pol._get_product_purchase_description(product_lang)
            po.button_confirm()
            i.production_id.update_qty_consume_with_variant_wo()
            i.show_po()
            

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
            raise ValidationError("Please Input Supplier first!")

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
            raise ValidationError("Product Service in this Workcenter hasn't been set")
        
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
