from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    coupon_promo = fields.Char(string='Promo char', compute='_compute_promo_coupon', store=True)
    coupon_promo_id = fields.Many2one('coupon.program', string='Promo', compute='_compute_promo_coupon',store=True )
    is_member = fields.Boolean(string='is member',related='coupon_promo_id.is_member', store=True)
    
    def _compute_promo_coupon(self):
        for record in self:
            coupon_program = self.env['coupon.program'].search([('program_type', '=', 'promotion_program'),('is_member','=',True)]).filtered(lambda x: record.id in x.valid_partner_ids.ids)
            if coupon_program:
                persen = coupon_program[0].discount_percentage or 0.0
                record.coupon_promo = str(persen) + ' %'
                record.coupon_promo_id = coupon_program[0].id
            else:
                record.coupon_promo = ""
                record.coupon_promo_id = False