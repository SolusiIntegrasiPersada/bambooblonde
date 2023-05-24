from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_model_id = fields.Many2one('product.model', string='Model')

class ProductModel(models.Model):
    _name = 'product.model'
    _description = 'Product Model'

    name = fields.Char(string='Model Name')

class ProductCategory(models.Model):
    _inherit = 'product.category'

    number_of_best_product = fields.Integer(string='Number of Best Product')
    less_than_one_month = fields.Integer(string='1-2 Minggu')
    more_than_one_month = fields.Integer(string='Sebulan atau Lebih')