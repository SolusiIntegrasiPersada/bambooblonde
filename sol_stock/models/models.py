from odoo import models, fields, api
import datetime


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    mandatory_source = fields.Boolean('Required Source Documents', default=False)
    hide_return = fields.Boolean('Hide Return Operations', default=False)
    is_foc_type = fields.Boolean('Is FOC Operation?', default=False)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    origin_pr = fields.Many2one('purchase.request', 'Source Document', index=True,
                                states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
                                help="Reference of the document")
    mandatory_source = fields.Boolean(related='picking_type_id.mandatory_source', string='Required Source Documents',
                                      readonly=True, related_sudo=False)
    style_name = fields.Char(string="Style Name")
    # analytic_account_id = fields.Many2one('account.analytic.account',string='Analytic Account')
    mrp_id = fields.Many2one('mrp.production', string="MRP")
    count = fields.Integer(string="Count Service")
    is_manufacture = fields.Boolean(string="Is Manufacturing", related='company_id.is_manufacturing', readonly=True)
    hide_return = fields.Boolean('Hide Return', related='picking_type_id.hide_return')
    is_foc_type = fields.Boolean('FOC', related='picking_type_id.is_foc_type')
    # source_so = fields.Char(string='SO No')

    # def action_print_quotation_receive(self):
    #     return self.env.ref('sol_stock.action_report_receive_action').report_action(self)
    #
    # def action_print_quotation_internal(self):
    #     return self.env.ref('sol_stock.action_report_internal_action').report_action(self)
    #
    # def action_print_quotation_return(self):
    #     return self.env.ref('sol_stock.action_report_return_action').report_action(self)

    @api.onchange('is_foc_type')
    def _onchange_location(self):
        for rec in self:
            data = {}
            # FOC Location
            if rec.is_foc_type and rec.picking_type_id.code == 'internal':
                data = {'domain': {'location_dest_id': [('is_foc', '=', True)]}}
            # Bamboo Transit
            if rec.picking_type_id.code == 'internal' and not rec.is_manufacture and not rec.is_foc_type:
                data = {'domain': {'location_dest_id': [('is_transit', '=', True)]}}
            return data


class StockMove(models.Model):
    _inherit = 'stock.move'

    fabric_width = fields.Float(string="Fabric Width", related='product_id.fabric_width')
    price = fields.Float(string="Cost")
    price_mo = fields.Float(string="Cost")
    image = fields.Image(string='Image')
    color_ids = fields.Many2many('product.template.attribute.value', string="Size and Color")
    colour = fields.Char('Color', compute="_onchange_color_size")
    size = fields.Char('Size', compute="_onchange_color_size")
    color_mo = fields.Char(string="Color")
    material_ids = fields.Many2many('mrp.bom.line', string='Material')
    qty_available = fields.Float(string='Qty Available', compute='_onchange_product')

    @api.onchange('product_id')
    def _onchange_product(self):
        for record in self:
            if record.product_id:
                record.update({
                    'image': record.product_id.image_1920,
                    'price': record.product_id.standard_price
                })
                if record.picking_id and record.location_id:
                    record.update({
                        'qty_available': sum(self.env['stock.quant'].search(
                            [('product_id', '=', record.product_id.id), ('location_id', '=', record.location_id.id)]
                        ).mapped('available_quantity'))
                    })

    @api.depends('product_id')
    def _onchange_color_size(self):
        for i in self:
            c, s = '', ''
            if i.product_id.product_template_variant_value_ids:
                i.color_ids = i.product_id.product_template_variant_value_ids
                list_size = ['SIZE:', 'SIZES:', 'UKURAN:']
                list_color = ['COLOR:', 'COLOUR:', 'COLOURS:', 'COLORS:', 'WARNA:', 'CORAK:']
                for v in i.product_id.product_template_variant_value_ids:
                    if any(v.display_name.upper().startswith(word) for word in list_color):
                        c += ' ' + v.name + ' '
                    elif any(v.display_name.upper().startswith(word) for word in list_size):
                        s += ' ' + v.name + ' '
                    else:
                        c += ''
                        s += ''
            else:
                c = ''
                s = ''
            i.colour = c
            i.size = s


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    color_ids = fields.Many2many('product.template.attribute.value', string="Size and Color")
    colour = fields.Char('Color', compute="_onchange_color_size")
    size = fields.Char('Size', compute="_onchange_color_size")

    @api.depends('product_id')
    def _onchange_color_size(self):
        for i in self:
            c, s = '', ''
            if i.product_id.product_template_variant_value_ids:
                i.color_ids = i.product_id.product_template_variant_value_ids
                list_size = ['SIZE:', 'SIZES:', 'UKURAN:']
                list_color = ['COLOR:', 'COLOUR:', 'COLOURS:', 'COLORS:', 'WARNA:', 'CORAK:']
                for v in i.product_id.product_template_variant_value_ids:
                    if any(v.display_name.upper().startswith(word) for word in list_color):
                        c += ' ' + v.name + ' '
                    elif any(v.display_name.upper().startswith(word) for word in list_size):
                        s += ' ' + v.name + ' '
                    else:
                        c += ''
                        s += ''
            else:
                c = ''
                s = ''
            i.colour = c
            i.size = s
