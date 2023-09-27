from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    address = fields.Char(string='Address')
    supervisor = fields.Char(string='Supervisor')
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Analytic Account')
    receipt_design_id = fields.Many2one(
        'pos.receipt',
        string='Receipt Design',
        help='Choose any receipt design',
        required=True
    )
    design_receipt = fields.Text(
        related='receipt_design_id.design_receipt',
        string='Receipt XML',
        help='Helps to get related receipt design'
    )
    is_custom_receipt = fields.Boolean(
        string='Is Custom Receipt',
        help='Boolean field to enable the custom receipt design',
        default=True,
    )
    global_discount_in_line = fields.Boolean(
        string="Add Discount in Line",
        default=True
    )
    include_discount_in_prices = fields.Boolean(
        string="Include Discount in Prices",
        help="If box is unchecked the displayed prices will not include discounts",
    )
    is_order_note = fields.Boolean('Order Note', default=True)
    is_order_note_receipt = fields.Boolean('Order Note on Receipt', default=True)
    is_line_note = fields.Boolean('Order Line Note')
    is_line_note_receipt = fields.Boolean('Order Line Note on Receipt')
    promo_message_ids = fields.Many2many('pos.promotions', string="Promotions")
    show_apply_promotion = fields.Boolean(
        string="Show Apply Promotion Button",
        help="Enable this option to Show Promotions button on POS, or the offers will be applied automatically.",
        default=False
    )
    show_offers_in_orderline = fields.Boolean(
        string="Show Offers in Orderlines",
        help="Enable this option to Show Offers in Orderline.",
        default=True
    )
    
    def use_coupon_code(self, code, creation_date, partner_id, reserved_program_ids):
        coupon_to_check = self.env["coupon.coupon"].search(
            [("code", "=", code), ("program_id", "in", self.program_ids.ids)]
        )
        if not coupon_to_check :
            program_generate_pos = self.env["coupon.program"].search(
            [("is_generate_pos", "=", True)])
            coupon_to_check = self.env["coupon.coupon"].search(
                [("code", "=", code), ("program_id", "in", program_generate_pos.ids)]
            )
           
        # If not unique, we only check the first coupon.
        coupon_to_check = coupon_to_check[:1]
        if not coupon_to_check:
            return {
                "successful": False,
                "payload": {
                    "error_message": _("This coupon is invalid (%s).") % (code)
                },
            }
        message = coupon_to_check._check_coupon_code(
            fields.Date.from_string(creation_date[:11]),
            partner_id,
            reserved_program_ids=reserved_program_ids,
        )
        error_message = message.get("error", False)
        if error_message:
            return {
                "successful": False,
                "payload": {"error_message": error_message},
            }

        coupon_to_check.sudo().write({"state": "used"})
        return {
            "successful": True,
            "payload": {
                "program_id": coupon_to_check.program_id.id,
                "coupon_id": coupon_to_check.id,
            },
        }