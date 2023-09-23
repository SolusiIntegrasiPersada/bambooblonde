from odoo import fields, models, api, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_voucher = fields.Boolean(string='Is Voucher', default=False)
    is_price_pos_editable = fields.Boolean(string='Editable Price in Pos', default=False)
    is_shooping_bag = fields.Boolean(string='Is Shopping Bag', default=False)
    is_produk_diskon = fields.Boolean(string='Product Discount', default=False)
    is_produk_promotion = fields.Boolean(string='Product Promotion', default=False)

