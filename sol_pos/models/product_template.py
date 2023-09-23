from odoo import fields, models, api, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_voucher = fields.Boolean(string='Is Voucher', default=False)
    is_price_pos_editable = fields.Boolean(string='Editable Price in Pos', default=False)
    is_shooping_bag = fields.Boolean(string='Is Shopping Bag', default=False)
    is_produk_diskon = fields.Boolean(string='Product Discount', default=False)
    is_produk_promotion = fields.Boolean(string='Product Promotion', default=False)
    
    
    product_model_categ_id = fields.Many2one("product.category", string="Model" , 
        compute='_compute_search_model' , store=True)
    
            
    @api.depends('categ_id')
    def _compute_search_model(self):
        def search_model(categ_id, loop):
            if loop >= 4:
                return False
            if categ_id.category_product == "department":
                return categ_id.id
            return search_model(categ_id.parent_id, loop + 1)

        for record in self:
            product_models_id = False
            if record.categ_id:
                product_models_id = search_model(record.categ_id, 1)
                
            record.product_model_categ_id = product_models_id
            
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    product_model_categ_id = fields.Many2one("product.category", string="Model" , 
        related='product_tmpl_id.product_model_categ_id', store=True)
    

                    
    
    
    
    

