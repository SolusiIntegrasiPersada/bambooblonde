from odoo import fields, models, api, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_voucher = fields.Boolean(string='Is Voucher', default=False)
