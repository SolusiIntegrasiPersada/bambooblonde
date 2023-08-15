from odoo import fields, models, api, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # @api.constrains('default_code')
    # def _check_code_unique(self):
    #     if self.default_code:
    #         ref_counts = self.search_count(
    #             [('default_code', '=', self.default_code), ('id', '!=', self.id)])
    #         if ref_counts > 0:
    #             raise ValidationError("Internal Reference already exists!")
    #     else:
    #         return

    brand = fields.Many2one('product.brand', string='Brand')
    stock_type = fields.Many2one('stock.type', string='Stock Type')
    fabric_lining = fields.Many2one(comodel_name='data.fabric.lining', string='Fabric/Lining')
    standard_price = fields.Float(store=True)
    from_origin = fields.Boolean(string='From Origin', default=False)
    no_origin = fields.Char(string='Origin Sample No.')
    types = fields.Selection([('staples', 'Staples'),('trend', 'Trend')], string='Type')
    internal_location = fields.One2many('stock.quantity', 'product_id', compute='get_product_qty')

    def get_product_qty(self):
        location_list = []
        product_list = []
        obj_location = self.env['stock.location'].search([('usage', '=', 'internal')])
        for i in obj_location:
            location_list.append(i.id)
        obj_product = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        for i in obj_product:
            obj_quant = self.env['stock.quant'].search([('product_id', '=', i.id),
                                                        ('location_id', 'in', location_list)])
            for obj in obj_quant:
                move_line = {'product_id': obj.product_id.id,
                             'stock_location': obj.location_id.id,
                             'qty_on_hand': obj.available_quantity,
                             }
                product_list.append(move_line)
        for i in product_list:
            if i['qty_on_hand'] > 0:
                self.internal_location |= self.env['stock.quantity'].create(i)

    def _set_standard_price(self):
        for template in self:
            if len(template.product_variant_ids) > 1:
                for p in template.product_variant_ids:
                    p.standard_price = template.standard_price

    @api.depends_context('company')
    @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
    def _compute_standard_price(self):
        # Depends on force_company context because standard_price is company_dependent
        # on the product_product
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.standard_price = template.product_variant_ids.standard_price
        for template in (self - unique_variants):
            template.standard_price = False


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'

    name = fields.Char(string='Name')


class StockType(models.Model):
    _name = 'stock.type'
    _description = 'Stock Type'

    name = fields.Char(string='Name')


class DataFabricLining(models.Model):
    _name = 'data.fabric.lining'
    _description = 'Database Fabric and Lining'

    name = fields.Char(string='Name')


class MainColor(models.Model):
    _name = 'main.color'
    _description = 'Main Color'

    name = fields.Char(string="Name")


class SizeLabel(models.Model):
    _name = 'size.label'
    _description = 'Size Attribute Label'
    _order = 'name'

    name = fields.Char(string='Name')
