from odoo import fields, api, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    order_notes = fields.Html(string="Order Notes")
    collection_product = fields.Many2one("product.collections", string="Collection")
    launch_date = fields.Date(string="Launch Date")
    class_product = fields.Many2one("class.product", string="Class")
    default_code = fields.Char(
        string="Internal Reference", related="product_tmpl_id.default_code", store=True
    )
    consumption = fields.Float(string="Consumption")
    fabric_width = fields.Float(string="Fabric Width")
    category = fields.Char(related="categ_id.name", string="Category")
    standard_price = fields.Float(related="product_tmpl_id.standard_price")
    product_template_variant_value_ids = fields.Many2many(
        "product.template.attribute.value",
        relation="product_variant_combination",
        domain=[("attribute_line_id.value_count", ">=", 1)],
        string="Variant Values",
        ondelete="restrict",
    )
    is_print = fields.Boolean(string="Print", default=False)
    barcode = fields.Char(
        "Barcode",
        copy=False,
        help="International Article Number used for product identification.",
        compute="_compute_barcode",
    )

    @api.depends("categ_id", "product_template_variant_value_ids")
    def _compute_barcode(self):
        for product in self:
            color_value = product.product_template_variant_value_ids.filtered(
                lambda x: x.attribute_id.name == "COLOR"
            )
            size_value = product.product_template_variant_value_ids.filtered(
                lambda x: x.attribute_id.name == "SIZE"
            )
            color_code = color_value.product_attribute_value_id.code
            if not color_code:
                color_code = "0"
            size_code = size_value.product_attribute_value_id.code
            if not size_code:
                size_code = "0"
            model = product.categ_id.parent_id.parent_id.code
            if not model:
                model = "0"
            sub_categ = product.categ_id.code
            if not sub_categ:
                sub_categ = "0"
            product.barcode = model + sub_categ + color_code + size_code
            # product.barcode = values


class ProductCollections(models.Model):
    _name = "product.collections"
    _description = "Product Collections"

    name = fields.Char(string="Name")


class ClassProduct(models.Model):
    _name = "class.product"
    _description = "Class"

    name = fields.Char(string="Class")
