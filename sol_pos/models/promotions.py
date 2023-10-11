# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_repr
import logging
_logger = logging.getLogger(__name__)
discount_type = {
    'discount_on_products': 'Discount on Products',    
    'buy_x_get_y': 'Buy X Product & Get Y Product Free',
    'buy_x_get_y_qty': 'Buy X Product & Get Y Qty Product Free',
    'buy_x_get_discount_on_y': 'Buy X and Get Discount on Y Product',
    'get_x_discount_on_sale_total': 'Get X % Discount on Sale Total'
}

class PosPromotions(models.Model):
    _name = 'pos.promotions'
    _description = "Promotions"
    _order = "sequence asc, id desc"

    month_list = [('1','January'),
        ('2','February'),
        ('3','March'),
        ('4','April'),
        ('5','May'),
        ('6','June'),
        ('7','July'),
        ('8','August'),
        ('9','Septemper'),
        ('10','Octuber'),
        ('11','November'),
        ('12','December'),]

    name = fields.Char(string='Title', required=True)
    sequence = fields.Integer(default=10)
    criteria_type = fields.Selection([('every_new_customer','For Every New Customers '),
        ('every_x_order','For Every X Order Per POS Session '),
        ('first_x_customer','For First X Customers Per POS Session'),
        ('every_order','For Every Order '),('based_specific_date','Based On Specific Date'),
        ], string="Type of Criteria",required=True, default="every_order")
    
    offer_type = fields.Selection([('discount_on_products','Discount on Products'),    
                                    ('buy_x_get_y','Buy X Product & Get Y Product Free'),
                                    ('buy_x_get_y_qty', 'Buy X Product & Get Y Qty Product Free'),
                                    ('buy_x_get_discount_on_y', 'Buy X and Get Discount on Y Product'),
                                    ('get_x_discount_on_sale_total', 'Get X % Discount on Sale Total'),], required=True)
    discounted_ids = fields.One2many(comodel_name='discount.products', inverse_name='discount_product_id', string='Discounted Products')
    buy_x_get_y_ids = fields.One2many('buy_x.get_y', 'buy_x_get_y_id', string="Buy X Get Y")
    buy_x_get_y_qty_ids = fields.One2many('buy_x.get_y_qty', 'buy_x_get_y_qty_id', string="Buy X Get Y Qty")
    buy_x_get_discount_on_y_ids = fields.One2many('buy_x.get_discount_on_y', 'buy_x_get_discount_on_y_id', string="Buy X Get Discount on Y")
    discount_on_sale_total = fields.Integer("Discount on Sale Total")
    discount_product_id = fields.Many2one('product.product', string='Discount Product',
        domain="[('available_in_pos', '=', True), ('sale_ok', '=', True)]", help='The product used to model the discount.')
    discount_sale_total_ids =  fields.One2many('discount.sale.total', 'discount_sale_total_id', string="Discount Rules")

    active = fields.Boolean(string="Active", default=1)
    pos_ids = fields.Many2many('pos.config',string="Point Of Sale")
    no_of_customers = fields.Integer('Number of Customers')
    order_number = fields.Integer('Order Number (X)')
    wk_day = fields.Char(string="Day")
    wk_month = fields.Selection(month_list, default='1', string="Month")
    pos_categ_ids = fields.Many2many('pos.category' , string="POS Categories")

    @api.constrains('offer_type')
    def validate_offer_type(self):
        promotions_ids = self.env['pos.promotions'].search([('id', '!=', self.id)])
        for promotions_id in promotions_ids:
            if promotions_id.offer_type == self.offer_type:
                if list(set(promotions_id.pos_ids.ids) & set(self.pos_ids.ids)):
                    raise ValidationError("Some of the Point of Sales in this configuration already have a configuration for Offer Type : "+ discount_type[self.offer_type] +".")

    @api.constrains('no_of_customers','order_number')
    def validate_customer_and_order_no(self):
        if (self.criteria_type == 'first_x_customer') and self.no_of_customers <= 0 :
            raise ValidationError("Number of customers must be greater than zero")
        if (self.criteria_type == 'every_x_order') and self.order_number <= 1 :
            raise ValidationError("Order number must be greater than one")

    @api.constrains('wk_day','wk_month', 'discount_sale_total_ids')
    def validate_day_mont(self):
        if(self.criteria_type == 'based_specific_date'):
            if not self.wk_month and not self.wk_day:
                raise ValidationError("Please enter the Day and Month")
            if not self.wk_month:
                raise ValidationError("Please enter the Month")
            elif not self.wk_day:
                raise ValidationError("Please enter the Day")

            if self.wk_month.isdigit() and self.wk_day.isdigit():
                wk_day =  int(self.wk_day)
                wk_month = int(self.wk_month)
                if wk_month >12 or wk_month <1:
                    raise ValidationError("Month can't be less than 0 or greater than 12")
                elif wk_month in [1,3,5,7,8,10,12]:
                    if (wk_day<1 or wk_day>31):
                        raise ValidationError("Please check the day in corresponding month")
                elif wk_month in [4,6,9,11]:
                    if (wk_day<1 or wk_day>30):
                        raise ValidationError("Please check the day in corresponding month")
                elif wk_month ==2 :
                    if (wk_day<1 or wk_day>28):
                        raise ValidationError("Please check the day in corresponding month")
            
            else:
                raise ValidationError("Day and month will be interger type")
        
        if(len(self.discount_sale_total_ids) > 1):
            for line1 in self.discount_sale_total_ids:
                for line2 in self.discount_sale_total_ids:
                    if(line1.id != line2.id):
                        flag = 0
                        if(line2.min_amount < line1.min_amount and line2.min_amount < line1.max_amount and line2.max_amount < line1.max_amount and line2.max_amount < line1.min_amount):
                            flag+=1
                        elif(line2.min_amount > line1.min_amount and line2.min_amount > line1.max_amount and line2.max_amount > line1.max_amount and line2.max_amount > line1.min_amount):
                            flag+=1
                        
                        if(not flag):
                            raise ValidationError('There is some overlapping in the Rule. Please Check and re-assign the Rules.')

class DiscountProducts(models.Model):
    _name = "discount.products"
    _order =  "apply_on, categ_id desc, id desc"

    def _get_default_currency_id(self):
        return self.env.company.currency_id.id

    discount_product_id = fields.Many2one('pos.promotions', string="Discounted Product")
    sequence = fields.Integer(default=16)
    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency_id, required=True)
    apply_on = fields.Selection([
        ('3_all', 'All Products'),
        ('2_categories', 'Categories'),
        ('1_products', 'Products'),
        ('4_class_model', 'Class and Model'),
        ],
        default='3_all', string='Apply On')
    categ_id = fields.Many2one('product.category', 'Product Category')
    product_id = fields.Many2one('product.product', 'Product Variant', domain=[('available_in_pos', '=', True)])
    name = fields.Char(string='Name', compute='_get_discount_line_name')
    percent_discount = fields.Float('Percentage Discount')
    discount = fields.Char('Discount', compute='_get_sale_discount_line_name_discount')

    @api.depends('apply_on', 'categ_id', 'product_id', 'percent_discount','class_product_id','models_id','product_ids')
    def _get_discount_line_name(self):
        for item in self:
            if item.categ_id and item.apply_on == '2_categories':
                item.name = _("Category: %s") % (item.categ_id.display_name)
            elif item.product_id and item.apply_on == '1_products':
                item.name = _("Variant: %s") % (item.product_id.with_context(display_default_code=False).display_name)
            elif item.apply_on == '4_class_model':
                name = _("Class: %s , Model: %s") % (item.class_product_id.name, item.models_id.name)
                if item.product_ids :
                    name += ", Product: %s" % (len(item.product_ids))
                item.name = name
            else:
                item.name = _("All Products")

    @api.depends('percent_discount','discount','currency_id')
    def _get_sale_discount_line_name_discount(self):
        for value in self:
            value.discount = _("%s %%") % (value.percent_discount)
            
    class_product_id = fields.Many2one("class.product", string="Class")
    models_id = fields.Many2one("product.category", string="Model",domain=[('category_product', '=', 'department')])
    product_ids = fields.Many2many(
        comodel_name='product.product', 
        string='Products'
        )
    
    @api.onchange('class_product_id','models_id')
    def ganti_domain_product_ids(self):
        domain = []
    
        # Sesuaikan domain berdasarkan 'class_product_id' dan 'models_id'
        if self.class_product_id and self.models_id:
            domain = [('class_product', '=', self.class_product_id.id),
                    ('product_model_categ_id', '=', self.models_id.id)]
        elif self.class_product_id:
            domain = [('class_product', '=', self.class_product_id.id)]
        elif self.models_id:
            domain = [('product_model_categ_id', '=', self.models_id.id)]
            
        domain += [('available_in_pos', '=', True)]
        
        return {'domain': {'product_ids': domain}}
    
    

class BuyXGetY(models.Model):
    _name = "buy_x.get_y"

    buy_x_get_y_id = fields.Many2one('pos.promotions', string="Buy X Get Y")
    product_x_id = fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string="Product X")
    qty_x = fields.Integer("Minimum Quantity")
    product_y_id =  fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string="Product Y")

    @api.constrains('qty_x')
    def check_constrains(self):
        for data in self:
            if(data.qty_x <= 0):
                raise ValidationError('Quantity of Product should be greater than 0')

class BuyXGetYQty(models.Model):
    _name = "buy_x.get_y_qty"

    buy_x_get_y_qty_id = fields.Many2one('pos.promotions', string="Buy X Get Y Qty")
    product_x_id = fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string="Product X")
    qty_x = fields.Integer("Minimum Quantity")
    product_y_id =  fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string="Product Y")
    qty_y = fields.Integer("Get Quantity")

    @api.constrains('qty_x', 'qty_y')
    def check_constrains(self):
        for data in self:
            if(data.qty_x <= 0):
                raise ValidationError('Quantity of Product should be greater than 0')
            if(data.qty_y <= 0):
                raise ValidationError('Quantity of Product should be greater than 0')

class BuyXGetDiscountOnY(models.Model):
    _name = "buy_x.get_discount_on_y"

    buy_x_get_discount_on_y_id = fields.Many2one('pos.promotions', string="Buy X Get Discount On Y")
    product_x_id = fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string="Product X")
    qty_x = fields.Integer("Minimum Quantity")
    product_y_id =  fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string="Product Y")
    discount = fields.Integer("Discount %")

    @api.constrains('qty_x', 'discount')
    def check_constrains(self):
        for data in self:
            if(data.qty_x <= 0):
                raise ValidationError('Quantity of Product should be greater than 0')
            if(data.discount < 0):
                raise ValidationError('Discount should be greater than 0')

class BuyXGetDiscountOnY(models.Model):
    _name = "discount.sale.total"

    discount_sale_total_id = fields.Many2one('pos.promotions', string="Discount On Sale Total")
    max_amount = fields.Integer("Max Sale")
    min_amount = fields.Integer("Min Sale")
    discount = fields.Integer("Discount %")

    @api.constrains('max_amount', 'min_amount', 'discount')
    def check_constrains(self):
        for data in self:
            if(data.max_amount <= 0):
                raise ValidationError('Max Sale Amount should be greater than 0')
            if(data.max_amount <= data.min_amount):
                raise ValidationError('Max Sale Amount should be greater than Min Sale Amount')
            if(data.discount < 0):
                raise ValidationError('Discount should be greater than 0')
            
            
class CouponProgram(models.Model):
    _inherit = "coupon.program"
    
    qty_generate = fields.Float(string='QTY to generate pos')
    
    sold_in_pos_id = fields.Many2one(
        string='Sold on Order',
        comodel_name='pos.order',
    )
    
    sold_in_pos_confiq_id = fields.Many2one(
        string='Sold on Pos',
        comodel_name='pos.config',
        related='sold_in_pos_id.config_id'
    )
    
    is_add_to_pos = fields.Boolean(string='Add to Pos ?', default=False)
    is_member = fields.Boolean(string='Is Diskon Member ?', default=False)
    
    def add_to_pos(self):
        for doc in self:
            pos_config = self.env["pos.config"].search([("use_coupon_programs", "=", True)])
            for pos in pos_config :
                if doc.program_type == 'coupon_program' :
                    pos.coupon_program_ids = [(4, doc.id)]
                if doc.program_type == 'promotion_program' :
                    pos.promo_program_ids = [(4, doc.id)]
    
            doc.is_add_to_pos = True
    
    def write(self, vals):
        res = super(CouponProgram,self).write(vals)
        
        if vals.get('rule_partners_domain',False) :
            for program in self.filtered(lambda x: x.is_member and x.program_type == 'promotion_program'):
                self.env['res.partner'].search([])._compute_promo_coupon()
            self.validasi_partner_member(self)
                
        
        return res
    
    code_coupon_generate = fields.Char(string='Code Coupon', 
        compute='_compute_coupon_code_and_state' )
    state_coupon_generate = fields.Char(string='State Coupon', 
        compute='_compute_coupon_code_and_state' )
    
    @api.depends('is_generate_pos','coupon_ids','coupon_ids.state')
    def _compute_coupon_code_and_state(self):
        for record in self:
            code_coupon_generate = False
            state_coupon_generate = False
            if record.coupon_ids :
                code_coupon_generate = record.coupon_ids[0].code
                state_coupon_generate = record.coupon_ids[0].state
                
            record.code_coupon_generate = code_coupon_generate
            record.state_coupon_generate = state_coupon_generate
    
    
    
    
    @api.depends("rule_partners_domain")
    def _compute_valid_partner_ids(self):
        
        res = super(CouponProgram, self)._compute_valid_partner_ids()
        
        for program in self.filtered(lambda x:x.is_member and x.program_type == 'promotion_program'):
            self.env['res.partner'].search([])._compute_promo_coupon()
            
        return res
    
    is_generate_pos = fields.Boolean(string='Is Generate Pos', default=False, readonly=True)
    
    
    @api.model
    def create(self, values):
        produk = False
        if values.get('is_generate_pos', False):
            produk = self.env["product.product"].search([("is_produk_promotion", "=", True)])
        elif values.get('program_type', False) == 'coupon_program':
            produk = self.env["product.product"].search([("is_produk_promotion", "=", True), ('is_produk_promotion_free', "=", True)])

        if produk:
            values['discount_line_product_id'] = produk[0].id

        res = super(CouponProgram, self).create(values)
        
        
        
        vals = {'program_id': res.id}
        if res.qty_generate > 0 and res.is_generate_pos:
            for _ in range(int(res.qty_generate)):
                coupon_voucher = self.env['coupon.coupon'].create(vals)
        else :
            if res.program_type == 'coupon_program' :
                coupon_voucher = self.env['coupon.coupon'].create(vals)

        res.add_to_pos()
        res.add_produk_diskon()

        if values.get('rule_partners_domain', False):
            for program in res.filtered(lambda x: x.is_member and x.program_type == 'promotion_program'):
                self.env['res.partner'].search([])._compute_promo_coupon()
                self.validasi_partner_member(res)
        
        return res

    def validasi_partner_member(self, res):
        if res.program_type == 'promotion_program' and res.is_member:
            partner_names = [partner.name for partner in res.valid_partner_ids if partner.id in res.env["coupon.program"].search([("is_member", "=", True), ("id", "!=", res.id)]).mapped('valid_partner_ids').ids]
            if partner_names:
                raise ValidationError(f"Partner {', '.join(partner_names)} sudah ada di Promo Member lain")


    def add_produk_diskon(self):
        if self.discount_line_product_id:
            self.discount_line_product_id.is_produk_promotion = True
            if not self.is_generate_pos:
                self.discount_line_product_id.is_produk_promotion_free = True

        if self.discount_line_product_id and self.program_type == 'promotion_program':
            self.discount_line_product_id.is_produk_diskon = True


from uuid import uuid4

    
class Coupon(models.Model):
    _inherit = "coupon.coupon"
    
    sold_in_pos_id = fields.Many2one(
        string='Sold on Order',
        comodel_name='pos.order',
        related='program_id.sold_in_pos_id'
    )
    
    sold_in_pos_confiq_id = fields.Many2one(
        string='Sold on Pos',
        comodel_name='pos.config',
        related='sold_in_pos_id.config_id'
    )
    
    @api.model
    def create(self, values):
        res = super(Coupon, self).create(values)
        for x in res :
            number = self.env['ir.sequence'].next_by_code('coupon.sequence')
            
            if not number:
                # Jika sequence tidak ada, maka buat sequence baru
                sequence_values = {
                    'name': "Coupon Sequence",
                    'code': "coupon.sequence",
                    'padding': 4,
                    'suffix': "/%(y)s",
                }
                self.env['ir.sequence'].create(sequence_values)
                number = self.env['ir.sequence'].next_by_code('coupon.sequence')
            
            x.code = number
        return res
