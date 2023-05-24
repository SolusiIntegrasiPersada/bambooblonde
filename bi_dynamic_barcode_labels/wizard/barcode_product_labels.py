# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class BarcodeProductLabelsWiz(models.TransientModel):
    _name = "barcode.product.labels.wiz"
    _description = 'Barcode Product Labels Wizard'

    product_barcode_ids = fields.One2many('barcode.product.labels.wiz.line', 'label_id', 'Product Barcode')

    @api.model
    def default_get(self, fields):
        res = super(BarcodeProductLabelsWiz, self).default_get(fields)
        active_ids = self._context.get('active_ids')
        product_ids = self.env['product.product'].browse(active_ids)
        barcode_lines = []
        for product in product_ids:
            barcode_lines.append((0,0, {
                'label_id' : self.id,
                'product_id' : product.id, 
                'qty' : 1,
            }))
        res.update({
            'product_barcode_ids': barcode_lines
        })
        return res


    def print_barcode_labels(self):
        self.ensure_one()
        [data] = self.read()
        barcode_config = self.env.ref('bi_dynamic_barcode_labels.barcode_labels_config_data')
        if not barcode_config.barcode_currency_id or not barcode_config.barcode_currency_position:
            raise UserError(_('Barcode Configuration fields are not set in data (Inventory -> Settings -> Barcode Configuration)'))
        data['barcode_labels'] = data['product_barcode_ids']
        barcode_lines = self.env['barcode.product.labels.wiz.line'].browse(data['barcode_labels'])
        datas = {
             'ids': [1],
             'model': 'barcode.product.labels.wiz',
             'form': data
        }
        return self.env.ref('bi_dynamic_barcode_labels.printed_barcode_labels_id').report_action(barcode_lines, data=datas)


class BarcodeProductLabelsLine(models.TransientModel):
    _name = "barcode.product.labels.wiz.line"
    _description = 'Barcode Product Labels Line'
    
    label_id = fields.Many2one('barcode.product.labels.wiz', 'Barcode labels')
    product_id = fields.Many2one('product.product', 'Product')
    product_qty = fields.Float('Product Qty', default=1.0)
    qty = fields.Integer('Barcode Qty', default=1)
    color = fields.Many2many('product.template.attribute.value', 'barcode_product_line_attribute_rel', string="Size and Color")
    colour = fields.Char('Color',compute="_onchange_color_size")
    size = fields.Char('Size',compute="_onchange_color_size")

    @api.depends('product_id')
    def _onchange_color_size(self):
        for i in self:
            c,s = '',''
            if i.product_id.product_template_variant_value_ids:
                i.color = i.product_id.product_template_variant_value_ids
                list_size = ['SIZE:','SIZES:','UKURAN:']
                list_color = ['COLOR:','COLOUR:','COLOURS:','COLORS:','WARNA:','CORAK:']
                for v in i.product_id.product_template_variant_value_ids:
                    if any(v.display_name.upper().startswith(word) for word in list_color):
                        c += ''+v.name+''
                    elif any(v.display_name.upper().startswith(word) for word in list_size):
                        s += ''+v.name+''
                    else:
                        c += ''
                        s += ''
            else:
                c = ''
                s = ''
            i.colour = c
            i.size = s



    