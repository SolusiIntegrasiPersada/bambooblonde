from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_STATES = [('draft', 'Draft'), ('order', 'Order'), ('unorder', 'Unorder'), ]


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    state = fields.Selection(selection=_STATES, string='Status', index=True, tracking=True, required=True, copy=False,
                             default='draft', )

    name = fields.Char(required=False, default='New', index=True, readonly=True, string='Trans No.')

    trans_date = fields.Datetime(string='Transaction Date', default=fields.Datetime.now, index=True, required=True, )

    parent_pps = fields.Char(string='Parent PPS')

    @api.model
    def create(self, vals):
        iterate = self.env['ir.sequence'].sudo().next_by_code('mrp.bom')
        if iterate:
            vals['name'] = iterate
        else:
            vals['name'] = 'New'
        return super(MrpBom, self).create(vals)

    @api.depends('over_packaging', 'bom_line_ids.total_material', 'operation_ids.total_services')
    def _compute_total_cost(self):
        for line in self:
            total_material = 0
            total_operation = 0
            for bom in line.bom_line_ids:
                total_material += bom.total_material
            for op in line.operation_ids:
                total_operation += op.total_services
            total = total_operation + total_material + line.over_packaging
            line.total_cost = total

    @api.depends('total_cost', 'margin')
    def _compute_suggest_price(self):
        for line in self:
            line.suggest_price = line.total_cost + (line.total_cost * line.margin)

    @api.depends('total_cost', 'margin_2')
    def _compute_suggest_price_2(self):
        for line in self:
            line.suggest_price_2 = line.total_cost + (line.total_cost * line.margin_2)

    @api.depends('total_cost', 'margin_3')
    def _compute_suggest_price_3(self):
        for line in self:
            line.suggest_price_3 = line.total_cost + (line.total_cost * line.margin_3)

    def order(self):
        return self.write({'state': 'order'})

    def unorder(self):
        return self.write({'state': 'unorder'})

    @api.depends('margin', 'margin_2', 'margin_3', 'total_cost')
    def _compute_nominal(self):
        for record in self:
            record.update({
                'nominal_1': record.total_cost + (record.margin * record.total_cost),
                'nominal_2': record.total_cost + (record.margin_2 * record.total_cost),
                'nominal_3': record.total_cost + (record.margin_3 * record.total_cost),
            })

    code = fields.Char('Child PPS')
    over_packaging = fields.Float(string='Over & Packaging', default=0.00)
    customer = fields.Many2one(comodel_name='res.partner', string='Customer')
    categ_id = fields.Many2one('product.category', related='product_tmpl_id.categ_id', string='Group')
    retail_price = fields.Float(string='Actual Price')
    is_final = fields.Boolean('Final')
    total_cost = fields.Float(string='Total Cost', compute=_compute_total_cost)
    margin = fields.Float(string='Margin 1')
    margin_2 = fields.Float(string='Margin 2')
    margin_3 = fields.Float(string='Margin 3')
    nominal_1 = fields.Float(string='Nominal 1', compute=_compute_nominal)
    nominal_2 = fields.Float(string='Nominal 2', compute=_compute_nominal)
    nominal_3 = fields.Float(string='Nominal 3', compute=_compute_nominal)
    suggest_price = fields.Float(string='Suggest Price', compute=_compute_suggest_price)
    suggest_price_2 = fields.Float(string='Suggest Price 2', compute=_compute_suggest_price_2)
    suggest_price_3 = fields.Float(string='Suggest Price 3', compute=_compute_suggest_price_3)
    bom_line_variant_ids = fields.One2many('mrp.bom.line.variant', 'bom_id', 'Material Variant', copy=True)
    label_hardware_ids = fields.One2many('mrp.bom.label.hardware', 'label_hardware_id', string='Label Hardware')

    # @api.onchange('bom_line_variant_ids')
    # def _onchange_bom_line_qty(self):
    def button_bom_line_qty(self):
        for record in self:
            bom_line_dict = {}
            for variant_line in record.bom_line_variant_ids:
                bom_line = record.bom_line_ids.filtered(lambda x: x.product_id == variant_line.product_id)
                if bom_line:
                    qty_sum = sum(
                        record.bom_line_variant_ids.filtered(lambda x: x.product_id == variant_line.product_id).mapped(
                            'product_qty'))
                    same_product_count = len(
                        record.bom_line_variant_ids.filtered(lambda x: x.product_id == variant_line.product_id))
                    if same_product_count:
                        bom_line_dict[bom_line.id] = qty_sum / same_product_count

            bom_line_list = []
            for bom_line_id, product_qty in bom_line_dict.items():
                # bom_line = record.bom_line_ids.browse(bom_line_id.origin)
                bom_line = record.bom_line_ids.browse(bom_line_id)
                bom_line_list.append((1, bom_line.id, {'total_qty_variant': product_qty}))

            record.bom_line_ids = bom_line_list
            for bl in record.bom_line_ids:
                bl._onchange_product_qty()

    @api.onchange('bom_line_ids')
    def _onchange_bom_line_variant_ids(self):
        for record in self:
            if record.product_tmpl_id:
                record.bom_line_variant_ids = False
                sql = f"""
                    select v.name as size_name
                    from product_attribute_value_product_template_attribute_line_rel m
                    inner join product_attribute_value v on v.id=m.product_attribute_value_id
                    inner join product_attribute a on a.id=v.attribute_id
                    inner join product_template_attribute_line l on l.id=product_template_attribute_line_id
                    inner join product_template p on p.id=l.product_tmpl_id
                    where a.name in ('size', 'Size', 'SIZE', 'SIZES', 'ukuran', 'Ukuran', 'UKURAN')
                    and p.id={record.product_tmpl_id.id}"""

                record.env.cr.execute(sql)
                data = record.env.cr.dictfetchall()
                sizes = []
                for line in record.bom_line_ids:
                    if not line.product_id.attribute_line_ids:
                        bom_product_template_attribute_value_ids = []
                        for t in line.bom_product_template_attribute_value_ids:
                            bom_product_template_attribute_value_ids.append((4, t.id, None))
                        for size in data:
                            sizes.append((0, 0, {
                                'product_id': line.product_id.id,  # 'product_qty' : line.product_qty,
                                'product_uom_id': line.product_uom_id.id, 'supplier': line.supplier.id,
                                'ratio': line.ratio,
                                'sizes': '(' + size['size_name'] + ')',
                                'bom_product_template_attribute_value_ids': bom_product_template_attribute_value_ids,
                                'operation_id': line.operation_id.id
                            }))
                    else:
                        bom_product_template_attribute_value_ids = []
                        for t in line.bom_product_template_attribute_value_ids:
                            bom_product_template_attribute_value_ids.append((4, t.id, None))
                        sizes.append((0, 0, {
                            'product_id': line.product_id.id,  # 'product_qty' : line.product_qty,
                            'product_uom_id': line.product_uom_id.id, 'supplier': line.supplier.id,
                            'ratio': line.ratio, 'sizes': line.sizes, 'color': line.color,
                            'bom_product_template_attribute_value_ids': bom_product_template_attribute_value_ids,
                            'operation_id': line.operation_id.id
                        }))
                record.bom_line_variant_ids = sizes


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.depends('product_qty', 'cost')
    def _compute_total_material(self):
        for line in self:
            line.total_material = line.cost * line.product_qty

    @api.depends('product_id')
    def _onchange_color_size(self):
        for i in self:
            if i.product_id.product_template_variant_value_ids:
                i.color = i.product_id.product_template_variant_value_ids
                list_size = ['SIZE', 'SIZES', 'UKURAN']
                list_color = ['COLOR', 'COLOUR', 'COLOURS', 'COLORS', 'WARNA', 'CORAK']
                for v in i.product_id.product_template_variant_value_ids:
                    if any(v.product_attribute_value_id.attribute_id.name.upper().startswith(word) for word in
                           list_color):
                        i.color = v.product_attribute_value_id.id
                    elif any(v.product_attribute_value_id.attribute_id.name.upper().startswith(word) for word in
                             list_size):
                        i.sizes = v.product_attribute_value_id.id
            else:
                i.color = False
                i.sizes = False

    supplier = fields.Many2one('res.partner', string='Supplier')
    color = fields.Many2one('product.attribute.value', string='Color', domain="[('attribute_id.name', '=', 'COLOR')]")
    sizes = fields.Many2one('product.attribute.value', string='Sizes', domain="[('attribute_id.name', '=', 'SIZE')]")
    ratio = fields.Float(string='Ratio', default=1.00)
    cost = fields.Float(string='Cost', related='product_id.standard_price')
    total_material = fields.Float(string='Total Material', compute=_compute_total_material)
    qty_available = fields.Float(string='Quantity On Hand', related='product_id.qty_available')
    shrinkage = fields.Float(string='Shkg(%)')
    total_qty_variant = fields.Float(string='Quantity')

    @api.onchange('shrinkage', 'total_qty_variant')
    def _onchange_product_qty(self):
        product_qty = self.total_qty_variant * self.shrinkage / 100
        self.product_qty = product_qty + self.total_qty_variant


class MrpBomLineVariant(models.Model):
    _name = 'mrp.bom.line.variant'
    _order = 'sequence, id'
    _rec_name = 'product_id'
    _description = 'Bill of Material Line (Variant)'

    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id

    @api.depends('product_qty', 'cost')
    def _compute_total_material(self):
        for line in self:
            line.total_material = line.cost * line.product_qty

    product_id = fields.Many2one('product.product', 'Component', required=True, check_company=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product Template', related='product_id.product_tmpl_id',
                                      store=True, index=True)
    company_id = fields.Many2one(related='bom_id.company_id', store=True, index=True, readonly=True)
    product_qty = fields.Float('Quantity', default=1.0, digits='Product Unit of Measure', required=True)
    product_uom_id = fields.Many2one(
        'uom.uom',
        'Product Unit of Measure',
        default=_get_default_product_uom_id,
        required=True,
        help='Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control',
        domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying.')
    bom_id = fields.Many2one('mrp.bom', 'Parent BoM', index=True, ondelete='cascade', required=True)
    parent_product_tmpl_id = fields.Many2one('product.template', 'Parent Product Template',
                                             related='bom_id.product_tmpl_id')
    possible_bom_product_template_attribute_value_ids = fields.Many2many(
        related='bom_id.possible_product_template_attribute_value_ids')
    bom_product_template_attribute_value_ids = fields.Many2many(
        'product.template.attribute.value',
        string='Apply on Variants', ondelete='restrict',
        domain="[('id', 'in', possible_bom_product_template_attribute_value_ids)]",
        help='BOM Product Variants needed to apply this line.')
    allowed_operation_ids = fields.One2many('mrp.routing.workcenter', related='bom_id.operation_ids')
    operation_id = fields.Many2one(
        'mrp.routing.workcenter', 'Consumed in Operation', check_company=True,
        domain="[('id', 'in', allowed_operation_ids)]",
        help='The operation where the components are consumed, or the finished products created.'
    )
    child_bom_id = fields.Many2one('mrp.bom', 'Sub BoM', compute='_compute_child_bom_id')
    child_line_ids = fields.One2many('mrp.bom.line', string='BOM lines of the referred bom',
                                     compute='_compute_child_line_ids')
    attachments_count = fields.Integer('Attachments Count', compute='_compute_attachments_count')
    supplier = fields.Many2one('res.partner', string='Supplier')
    color = fields.Char('Color')
    sizes = fields.Char('Sizes')
    ratio = fields.Float(string='Ratio', default=1.00)
    cost = fields.Float(string='Cost', related='product_id.standard_price')
    total_material = fields.Float(string='Total Material', compute=_compute_total_material)

    # shrinkage = fields.Float(string='Shkg(%)')

    @api.depends('product_id', 'bom_id')
    def _compute_child_bom_id(self):
        for line in self:
            if not line.product_id:
                line.child_bom_id = False
            else:
                line.child_bom_id = self.env['mrp.bom']._bom_find(line.product_id)[line.product_id]

    @api.depends('product_id')
    def _compute_attachments_count(self):
        for line in self:
            nbr_attach = self.env['mrp.document'].search_count(
                ['|', '&', ('res_model', '=', 'product.product'), ('res_id', '=', line.product_id.id), '&',
                 ('res_model', '=', 'product.template'), ('res_id', '=', line.product_id.product_tmpl_id.id)])
            line.attachments_count = nbr_attach

    @api.depends('child_bom_id')
    def _compute_child_line_ids(self):
        """ If the BOM line refers to a BOM, return the ids of the child BOM lines """
        for line in self:
            line.child_line_ids = line.child_bom_id.bom_line_ids.ids or False

    @api.onchange('product_uom_id')
    def onchange_product_uom_id(self):
        res = {}
        if not self.product_uom_id or not self.product_id:
            return res
        if self.product_uom_id.category_id != self.product_id.uom_id.category_id:
            self.product_uom_id = self.product_id.uom_id.id
            res['warning'] = {'title': _('Warning'), 'message': _(
                'The Product Unit of Measure you chose has a different category than in the product form.')}
        return res

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if 'product_id' in values and 'product_uom_id' not in values:
                values['product_uom_id'] = self.env['product.product'].browse(values['product_id']).uom_id.id
        return super(MrpBomLineVariant, self).create(vals_list)

    def _skip_bom_line(self, product):
        """
        Control if a BoM line should be produced, can be inherited to add custom control.
        """
        self.ensure_one()
        if product._name == 'product.template':
            return False
        return not product._match_all_variant_values(self.bom_product_template_attribute_value_ids)

    def action_see_attachments(self):
        domain = ['|', '&', ('res_model', '=', 'product.product'), ('res_id', '=', self.product_id.id), '&',
                  ('res_model', '=', 'product.template'), ('res_id', '=', self.product_id.product_tmpl_id.id)]
        attachment_view = self.env.ref('mrp.view_document_file_kanban_mrp')
        return {'name': _('Attachments'), 'domain': domain, 'res_model': 'mrp.document',
                'type': 'ir.actions.act_window', 'view_id': attachment_view.id,
                'views': [(attachment_view.id, 'kanban'), (False, 'form')],
                'view_mode': 'kanban,tree,form', 'help': _(""""
                    <p class='o_view_nocontent_smiling_face'>
                            Upload files to your product
                        </p><p>
                            Use this feature to store any files, like drawings or specifications.
                        </p>
                    """),
                'limit': 80,
                'context': "{'default_res_model': '%s','default_res_id': %d, 'default_company_id': %s}" % (
                    'product.product', self.product_id.id, self.company_id.id)}


class MrpBomLabelHardware(models.Model):
    _name = 'mrp.bom.label.hardware'
    _description = 'Label Hardware'

    label_hardware_id = fields.Many2one('mrp.bom', string='BoM')
    description = fields.Char('Description')
    color = fields.Many2one(comodel_name='print.color', string='Color')
    qty_label = fields.Float('Qty')


class Sizes(models.Model):
    _name = 'sizes'
    _description = 'Sizes'

    name = fields.Char(string='Name')


class DptColor(models.Model):
    _name = 'dpt.color'
    _description = 'DPT Color'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')

    @api.constrains('name')
    def _check_code_unique(self):
        for record in self:
            if record.name:
                ref_counts = record.search_count([('name', '=', record.name), ('id', '!=', record.id)])
                if ref_counts > 0:
                    raise ValidationError('Color already exists!')
            else:
                return

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if record.code:
                ref_counts = record.search_count([('code', '=', record.code), ('id', '!=', record.id)])
                if ref_counts > 0:
                    raise ValidationError('Code already exists!')
            else:
                return
