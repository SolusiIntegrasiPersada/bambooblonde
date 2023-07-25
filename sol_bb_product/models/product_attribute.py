from odoo import _, models, api, fields
from odoo.exceptions import UserError


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    is_size = fields.Boolean('Size Variant', default=False)

    @api.constrains('is_size')
    def check_size_variant(self):
        size_variant = self.env['product.attribute'].search(
            [('id', '!=', self.id), ('is_size', '=', True)]
        )
        if size_variant:
            raise UserError(_('There are already size variant'))


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    code = fields.Char("Code", help="for barcode structure", default="0")
    label_id = fields.Many2one('size.label', string='Size Label')
