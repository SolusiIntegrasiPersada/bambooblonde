# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseBudget(models.Model):

    _name = 'purchase.budget'
    _description = 'Purchase Budget'
    _order = 'id desc'

    name = fields.Char(string='Name')
    remaining_amount = fields.Integer(string='Rem. Balance', default=0)
    usage_amount = fields.Integer(string='Used Balance', default=0)
    budget_ids = fields.One2many('category.budget', 'budget_id', string='Category Budget')
    
    
class CategoryBudget(models.Model):
    _name = 'category.budget'
    _description = 'Purchase Budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    budget_id = fields.Many2one('purchase.budget', string='Purchase Budget', ondelete='cascade')
    category_id = fields.Many2one('product.category', string='Product Category')
    budget_guide = fields.Float(string='Budget Guide')
    budget_amount = fields.Float(string='Budget')
    actual_percentage = fields.Float(string='Actual')
    stock_percentage = fields.Float(string='In Stock')
    purchase_qty = fields.Integer(string='Order')
    total_value = fields.Float(string='Total')
