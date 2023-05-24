from odoo import models, api, fields


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    code = fields.Char("Code", help="for barcode structure", default="0")
