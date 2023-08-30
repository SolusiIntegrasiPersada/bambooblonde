# -*- coding: utf-8 -*-

from odoo import _, models, fields, api


class PatternAlteration(models.Model):
    _name = 'pattern.alteration'
    _description = 'Link Purchase Request and Pattern Alteration'

    parent_purchase_id = fields.Many2one('purchase.request', string='Request')
    pattern_id = fields.Many2one('purchase.request', string='Pattern Alteration')
    user_id = fields.Many2one('res.users', string='User Pattern Alteration')


class CustomPattern(models.Model):
    _name = 'custom.pattern'
    _description = 'Custom Pattern'

    # name = fields.Char('Print/Color')
    parent_custom_id = fields.Many2one('purchase.request', string='custom')
    print_color_id = fields.Many2one('product.template.attribute.value', string='Print/Color')
    model_ptr = fields.Many2one('product.category', string='Model')
    size = fields.Many2one('product.template.attribute.value', string='Size')

    no_ptr = fields.Char('Pattern No')
    pattern_marker = fields.Char('Pattern Marker')
    size_approve = fields.Char('Size Approve')
    sample_size = fields.Char('Sample Size')
    fabric_width = fields.Char('Fabric Width')
    pattern_time = fields.Float('Pattern Time')
    consumption = fields.Char('Consumption')
    pattern_cost = fields.Float('Costing Order')


class DataLabelHardware(models.Model):
    _name = 'data.label.hardware'
    _description = 'Data Label Hardware'

    name = fields.Char(string="Label")


class LabelHardware(models.Model):
    _name = 'label.hardware'
    _description = 'Label Hardware'

    purchase_id = fields.Many2one('purchase.request', string='Purchase Request')
    label_id = fields.Many2one('data.label.hardware', string='Label')
    description_name = fields.Char(string="Description", tracking=True)
    print_color_id = fields.Many2one(comodel_name='print.color', string='Color')
    color_id = fields.Many2one('product.attribute.value', string='Color',
                               domain="[('attribute_id.name', '=', 'COLOR')]")
    label_qty = fields.Float(string='Qty')

    @api.onchange('label_id')
    def _onchange_description(self):
        for record in self:
            if record.label_id:
                record.update({
                    'description_name': record.label_id.name
                })


class LabelDress(models.Model):
    _name = 'label.dress'
    _description = 'Label Dress'

    label_dress_id = fields.Many2one('purchase.request', string='label dress ids')
    brand = fields.Many2one('product.brand', string='Brand', ondelete='cascade')
    image = fields.Image('Label Pict')
    comment = fields.Html('Comment')


class DataProdSummary(models.Model):
    _name = 'data.prod.summary'
    _description = 'Data Prod Summary'

    name = fields.Char('Production Summary')


class ProductionSummary(models.Model):
    _name = 'production.summary'
    _description = 'Production Summary'

    prod_summ_id = fields.Many2one('purchase.request', string='prod summ ids')
    summary = fields.Many2one('data.prod.summary', string='Prod Summary')
    summary_name = fields.Char(string='Summary', tracking=True)
    description = fields.Char('Description')

    @api.onchange("summary")
    def _onchange_summary(self):
        if self.summary:
            summary = self.summary.name
            self.summary_name = summary


class RequestDetail(models.Model):
    _name = 'request.detail'
    _description = 'Request Detail'

    name = fields.Char(string='Original Sample')
    sample_size = fields.Char(string='Sample Size')
    approved_size = fields.Char(string='Sample In Approved Size')
    sample_in_size = fields.Char(string='Please Make Sample In Size')


class PrintColor(models.Model):
    _name = 'print.color'
    _description = 'Print Color'

    name = fields.Char(string='color')


class DataMasterStory(models.Model):
    _name = 'data.master.story'
    _description = 'Data Master Story'

    name = fields.Char('Story Name')


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    image = fields.Image(string='Fabric Swatch')
    department = fields.Many2one('product.category', string='Department/Category/Sub Category')
    sub_department = fields.Char(string='Sub Department')
    fabric = fields.Many2one('data.fabric.lining', string='Fabric', ondelete='cascade')
    lining = fields.Many2one('data.fabric.lining', string='Lining', ondelete='cascade')
    fabric_smp = fields.Many2one('product.product', string='Fabric', ondelete='cascade')
    lining_smp = fields.Many2one('product.product', string='Lining', ondelete='cascade')
    view_story = fields.Many2one(string='Story', related='request_id.story_id', readonly=True)
    color = fields.Many2many('product.template.attribute.value', string="Size and Color")
    colour = fields.Char('Color', compute="_onchange_color_size")
    size = fields.Char('Size', compute="_onchange_color_size")

    @api.depends('product_id')
    def _onchange_color_size(self):
        for i in self:
            c, s = '', ''
            if i.product_id.product_template_variant_value_ids:
                i.color = i.product_id.product_template_variant_value_ids
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

    @api.onchange('product_id')
    def _onchange_image(self):
        if self.product_id:
            self.image = ''
            if self.product_id.image_1920:
                self.image = self.product_id.image_1920
            self.image = self.image

    @api.onchange('product_id')
    def _onchange_department(self):
        if self.product_id:
            department = ''
            if self.product_id.categ_id:
                self.department = self.product_id.categ_id
            return department


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    @api.model
    def default_get(self, fields):
        res = super(PurchaseRequest, self).default_get(fields)
        updt_label = [(5, 0, 0)]
        updt_summary = [(5, 0, 0)]
        label = self.env["data.label.hardware"].search([])
        summary = self.env["data.prod.summary"].search([])
        for i in label:
            line_i = (0, 0, {
                'label_id': i.id,
                'description_name': i.name
            })
            updt_label.append(line_i)
        for j in summary:
            line_j = (0, 0, {
                'summary': j.id,
                'summary_name': j.name
            })
            updt_summary.append(line_j)
        res.update({
            'label_hardware_ids': updt_label,
            'prod_summ_ids': updt_summary,
        })
        return res

    ### SAMPLE DEVELOPMENT ###
    request_detail_id = fields.Many2one(string='Original Sample', comodel_name='request.detail', ondelete='cascade')
    notes = fields.Html(string='FIT NOTES')
    date_start = fields.Date(string='Transaction Date')
    story_id = fields.Many2one(string='Story', comodel_name='data.master.story')
    alt_cmnt = fields.Html('Alteration Comment')
    spec = fields.Html('Specification')
    count = fields.Integer(string='count')
    source = fields.Char(string='Source Document')
    name_source = fields.Char(string='Source Document')

    ### PATTERN ALTERATION ###
    purchase_custom_ids = fields.One2many('custom.pattern', 'parent_custom_id', string='Custom', copy=True)
    purchase_pattern_ids = fields.One2many('pattern.alteration', 'parent_purchase_id', string='Order History')
    revision_id = fields.Many2one('purchase.request', string='Purchase to Pattern Alteration')
    purchase_revision_id = fields.Many2one('purchase.request', string='Pattern Alteration')
    pattern_count = fields.Integer(string='Pattern', compute='_find_len')
    test = fields.Boolean(string="Test", default=False)
    get_last_costing = fields.Float(string="Get Costing", compute="get_last_costing_pattern")

    ### PENDING ORDER ###
    status_of_sample = fields.Char(string='Status of Sample')
    ordering_date = fields.Date(string='Delivery Date', states={'done': [('readonly', False)]})
    delivery_date = fields.Date(states={'done': [('readonly', False)]})
    thread_type = fields.Many2one('product.attribute.value', domain="[('attribute_id.name', '=', 'SIZE')]",
                                  string='Sample Size')
    thread_color = fields.Many2one('product.attribute.value', domain="[('attribute_id.name', '=', 'SIZE')]",
                                   string='Sample Approve Size')
    hanging_tape = fields.Char(string='Hanging Tape')

    seams = fields.Html(string='Seams')
    grading_intructions = fields.Html(string='Grading Intructions')
    fit_changes = fields.Html(string='Fit Changes')

    # fabric_lining_ids = fields.One2many('fabric.lining', 'fabric_lining_id', string='fabric lining id')
    label_hardware_ids = fields.One2many('label.hardware', 'purchase_id', string='label hardware id')
    label_dress_ids = fields.One2many('label.dress', 'label_dress_id', string='label dress id')
    prod_summ_ids = fields.One2many('production.summary', 'prod_summ_id', string='prod summ id')

    def button_to_pattern(self):
        return self.write({'state': 'rejected'})

    @api.model
    def create(self, vals):
        res = super(PurchaseRequest, self).create(vals)
        if not res.test:
            res.name = self.env["ir.sequence"].next_by_code("purchase.request.sequ")
        return res

    def _find_len(self):
        self.pattern_count = len(self.purchase_pattern_ids.ids)

    def create_pattern_alteration(self):
        custom = self.env['custom.pattern'].create({
            'parent_custom_id': self.ids[0],
        })
        custom.write({
            'no_ptr': 'PTR ' + str(self.count + 1),
        })
        new_name = self.name[0: self.name.index(' - PTR')] if self.test else self.name

        pattern = self.copy({
            # 'count': 1 + len(self.purchase_pattern_ids.ids),
            # 'name': "%s - PTR %s" % (new_name, self.count + 1),
            'revision_id': self.id,
            'count': self.count + 1,
            'test': True,
        })
        pattern.write({
            'name': "%s - PTR %s" % (new_name, self.count + 1),
        })

        uid_id = self.env.user.id
        self.env['pattern.alteration'].create({
            'pattern_id': pattern.id,
            'user_id': uid_id,
            'parent_purchase_id': self.ids[0],
        })
        pattern.recompute()

        return {
            # "name": _("Pattern Alteration"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.request",
            # "views": [
            #     (self.env.ref("purchase_request.view_purchase_request_form").id, "form"),
            # ],
            # "target": "current",
            "view_mode": "form",
            "res_id": pattern.id,
        }

    def view_pattern_alteration(self):
        action = self.env.ref('purchase_request.purchase_request_form_action').read()[0]
        purchase_pattern_ids = self.mapped('purchase_pattern_ids.pattern_id')
        if len(purchase_pattern_ids) > 1:
            action['domain'] = [('id', 'in', purchase_pattern_ids.ids)]
        elif purchase_pattern_ids:
            action['views'] = [
                (self.env.ref('purchase_request.view_purchase_request_form').id, 'form')
            ]
            action['res_id'] = purchase_pattern_ids.id
        return action

    def get_last_record_pattern(self):
        for record in self:
            return record.purchase_custom_ids.sorted(lambda l: l.id, reverse=True)[0]

    @api.depends('test', 'purchase_custom_ids.pattern_cost')
    def get_last_costing_pattern(self):
        for record in self:
            if record.test is True:
                sorted_custom_ids = record.purchase_custom_ids.sorted(key=lambda l: l.id, reverse=True)
                if sorted_custom_ids:
                    last_custom_id = sorted_custom_ids[0]
                    record.get_last_costing = last_custom_id.pattern_cost
            else:
                record.get_last_costing = 0.0