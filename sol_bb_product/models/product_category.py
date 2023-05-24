from odoo import fields, api, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    category_product = fields.Selection(
        [
            ("department", "Department"),
            ("category", "Category"),
            ("subcategory", "Sub-Category"),
        ],
        string="Category Product",
        required=True,
    )
    code = fields.Char("Code", help="for barcode structure")
