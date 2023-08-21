# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from datetime import datetime, timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseBudget(models.Model):

    _name = 'purchase.budget'
    _description = 'Purchase Budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    @api.model
    def _get_this_month(self):
        return str(datetime.today().month)

    name = fields.Char(string='Name')
    remaining_amount = fields.Integer(string='Rem. Balance', default=0)
    usage_amount = fields.Integer(string='Used Balance', default=0)
    budget_ids = fields.One2many('category.budget', 'budget_id', string='Category Budget')
    month = fields.Selection([('1', 'Januari'),
                              ('2', 'Februari'),
                              ('3', 'Maret'),
                              ('4', 'April'),
                              ('5', 'Mei'),
                              ('6', 'Juni'),
                              ('7', 'Juli'),
                              ('8', 'Agustus'),
                              ('9', 'September'),
                              ('10', 'Oktober'),
                              ('11', 'November'),
                              ('12', 'Desember')], string='Month', default=_get_this_month)

    @api.model
    def create(self, vals):
        month_name = dict(self._fields['month'].selection).get(vals['month'])
        vals["name"] = f"""Budget {month_name} {datetime.today().year}"""
        return super(PurchaseBudget, self).create(vals)
    
    
class CategoryBudget(models.Model):
    _name = 'category.budget'
    _description = 'Category Budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    budget_id = fields.Many2one('purchase.budget', string='Purchase Budget', ondelete='cascade')
    category_id = fields.Many2one('product.category', string='Product Category')
    budget_guide = fields.Float(string='Budget Guide')
    budget_amount = fields.Float(string='Budget')
    actual_percentage = fields.Float(string='Actual')
    stock_percentage = fields.Float(string='In Stock')
    purchase_qty = fields.Integer(string='Order')
    total_value = fields.Float(string='Total')

    @api.depends('budget_id.month')
    def _get_category_domain(self):
        current_month = datetime(year=datetime.today().year, month=int(self.budget_id.month), day=1)
        start_month = current_month - timedelta(days=180)
        category_ids = self.env['purchase.order.line'].search(
            [('date_planned', '<=', current_month),
             ('date_planned', '>=', start_month)]).mapped('product_id.product_tmpl_id.categ_id.id')
        return {'domain': {'product_category_id': [('id', 'in', category_ids)]}} if category_ids else {}

