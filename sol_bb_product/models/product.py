from odoo import fields, api, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    order_notes = fields.Html(string="Order Notes")
    collection_product = fields.Many2one("product.collections", string="Collection")
    launch_date = fields.Date(string="Launch Date")
    class_product = fields.Many2one("class.product", string="Class")
    consumption = fields.Float(string="Consumption")
    fabric_width = fields.Float(string="Fabric Width")
    category = fields.Char(related="categ_id.name", string="Category")
    is_print = fields.Boolean(string="Print", default=False)
    main_color = fields.Many2one('product.attribute.value', string="Main Color", domain="[('attribute_id.name', '=', 'COLOR')]")
    # @api.depends("categ_id", "product_template_variant_value_ids")
    # def _compute_barcode(self):
    #     for product in self:
    #         color_value = product.product_template_variant_value_ids.filtered(
    #             lambda x: x.attribute_id.name == "COLOR"
    #         )
    #         size_value = product.product_template_variant_value_ids.filtered(
    #             lambda x: x.attribute_id.name == "SIZE"
    #         )
    #         color_code = color_value.product_attribute_value_id.code
    #         if not color_code:
    #             color_code = "0"
    #         size_code = size_value.product_attribute_value_id.code
    #         if not size_code:
    #             size_code = "0"
    #         model = product.categ_id.parent_id.parent_id.code
    #         if not model:
    #             model = "0"
    #         sub_categ = product.categ_id.code
    #         if not sub_categ:
    #             sub_categ = "0"
    #         product.barcode = model + sub_categ + color_code + size_code
    #         # product.barcode = values


class ProductCollections(models.Model):
    _name = "product.collections"
    _description = "Product Collections"

    name = fields.Char(string="Name")


class ClassProduct(models.Model):
    _name = "class.product"
    _description = "Class"

    name = fields.Char(string="Class")
