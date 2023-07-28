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
    main_color_id = fields.Many2one('main.color', string="Main Color")
    product_template_variant_value_ids = fields.Many2many('product.template.attribute.value',
                                                          relation='product_variant_combination',
                                                          domain=[('attribute_line_id.value_count', '>', 0)],
                                                          string="Variant Values", ondelete='restrict')


class ProductCollections(models.Model):
    _name = "product.collections"
    _description = "Product Collections"

    name = fields.Char(string="Name")


class ClassProduct(models.Model):
    _name = "class.product"
    _description = "Class"

    name = fields.Char(string="Class")
