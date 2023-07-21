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