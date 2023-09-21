from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    coupon_promo = fields.Char(string='Promo', compute='_compute_promo_coupon', store=True)
    
    @api.depends('name')
    def _compute_promo_coupon(self):
        for record in self:
            print('_compute_promo_coupon')
            coupon_program = self.env['coupon.program'].search([('program_type', '=', 'promotion_program')]).filtered(lambda x: record.id in x.valid_partner_ids.ids and 'available_in_pos","=",True' in str(x.rule_products_domain))
            if coupon_program:
                persen = coupon_program[0].discount_percentage or 0.0
                record.coupon_promo = str(persen) + ' %'
            else:
                record.coupon_promo = ""
