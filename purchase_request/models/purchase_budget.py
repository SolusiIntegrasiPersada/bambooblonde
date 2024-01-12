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

    @api.model
    def _get_this_year(self):
        return str(datetime.today().year)

    name = fields.Char(string='Name')
    budget_amount = fields.Float(string='Budget', default=0)
    remaining_amount = fields.Float(string='Rem. Balance', compute='_compute_amount')
    usage_amount = fields.Float(string='Used Balance', compute='_compute_amount')
    budget_ids = fields.One2many('category.budget', 'budget_id', string='Category Budget')
    budget_days = fields.Integer(string='Budget Days', default=180, required=True)
    year = fields.Integer(string='Year', default=_get_this_year)
    month = fields.Selection(
        [('1', 'Januari'),
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

    @api.depends('budget_ids')
    def _compute_amount(self):
        for record in self:
            usage_amount = sum(record.budget_ids.mapped('total_value'))
            remaining_amount = record.budget_amount - usage_amount
            record.usage_amount = usage_amount
            record.remaining_amount = remaining_amount


class CategoryBudget(models.Model):
    _name = 'category.budget'
    _description = 'Category Budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    budget_id = fields.Many2one('purchase.budget', string='Purchase Budget', ondelete='cascade')
    category_id = fields.Many2one('product.category', string='Product Category')
    budget_guide = fields.Float(string='Budget Guide', compute='_compute_budget_guide', inverse='_inverse_budget_guide')
    budget_amount = fields.Float(string='Budget', compute='_compute_budget_amount')
    actual_percentage = fields.Float(string='Actual')
    stock_percentage = fields.Float(string='In Stock', compute='_compute_stock_purchase')
    purchase_qty = fields.Integer(string='Order', compute='_compute_stock_purchase')
    total_value = fields.Float(string='Total', compute='_compute_stock_purchase')

    def get_purchase_domain(self, type):
        start_month = datetime(year=datetime.today().year, month=int(self.budget_id.month), day=1)
        end_month = start_month + timedelta(days=self.budget_id.budget_days)
        if type == 'po':
            domain = [('order_id.date_approve', '>=', start_month), ('order_id.date_approve', '<=', end_month)]
        else:
            domain = [('create_date', '>=', start_month), ('create_date', '<=', end_month)]
        return domain

    @api.onchange('category_id')
    def _onchange_category_id(self):
        if not self.category_id:
            domain = self.get_purchase_domain(type='po')
            category_ids = self.env['purchase.order.line'].search(domain).mapped(
                'product_id.product_tmpl_id.categ_id')
            sub_category_ids = category_ids.filtered(
                lambda s: s.parent_id.category_product == 'category'
            ).mapped('parent_id.id')
            return {'domain': {'category_id': [('id', 'in', sub_category_ids)]}} if sub_category_ids else {}

    @api.depends('category_id', 'budget_id.budget_amount')
    def _compute_budget_guide(self):
        for record in self:
            if record.category_id:
                domain = record.get_purchase_domain(type='pos')
                domain += [('product_id.product_tmpl_id.categ_id.id', '=', record.category_id.id)]
                cost_amount = sum(self.env['pos.order.line'].search(domain).mapped('product_id.standard_price'))
                record.budget_guide = ((cost_amount / (record.budget_id.budget_days / 30)) / record.budget_id.budget_amount) if record.budget_id.budget_amount else 0

    def _inverse_budget_guide(self):
        pass

    @api.depends('budget_guide', 'budget_id.budget_amount')
    def _compute_budget_amount(self):
        for record in self:
            record.budget_amount = record.budget_guide * record.budget_id.budget_amount

    @api.depends('category_id')
    def _compute_stock_purchase(self):
        for record in self:
            stock_percentage, purchase_qty, total_value = 0, 0, 0
            if record.category_id:
                product_ids = self.env['product.product'].search(
                    [('product_tmpl_id.categ_id.id', '=', record.category_id.id)]).mapped('id')
                domain = record.get_purchase_domain(type='po')
                domain += [('product_id', 'in', product_ids), ('state', '=', 'purchase')]
                purchase_obj = self.env['purchase.order.line'].search(domain)

                product_cost = self.env['stock.quant'].search(
                    [('product_id', 'in', product_ids)]).mapped('product_id.standard_price')

                stock_percentage = (sum(product_cost) / record.budget_id.budget_amount) if record.budget_id.budget_amount else 0
                purchase_qty = sum(purchase_obj.mapped('product_qty')) or 0
                total_value = sum(purchase_obj.mapped('price_unit')) or 0

            record.update({
                'stock_percentage': stock_percentage,
                'purchase_qty': purchase_qty,
                'total_value': total_value
            })