from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    coupon_promo = fields.Char(string='Promo char', compute='_compute_promo_coupon', store=True)
    coupon_promo_id = fields.Many2one('coupon.program', string='Promo', compute='_compute_promo_coupon',store=True )
    
    def _compute_promo_coupon(self):
        for record in self:
            coupon_program = self.env['coupon.program'].search([('program_type', '=', 'promotion_program')]).filtered(lambda x: record.id in x.valid_partner_ids.ids and 'available_in_pos","=",True' in str(x.rule_products_domain))
            if coupon_program:
                persen = coupon_program[0].discount_percentage or 0.0
                record.coupon_promo = str(persen) + ' %'
                record.coupon_promo_id = coupon_program[0].id
            else:
                record.coupon_promo = ""
