from odoo import fields, models

_SHIFT = [
    ("Shift A", "Shift A"),
    ("Shift B", "Shift B"),
]


class PosSession(models.Model):
    _inherit = 'pos.session'

    shift = fields.Selection(
        selection=_SHIFT,
        string="Shift",
        index=True,
        tracking=True,
        copy=False,
    )
    visitor_count = fields.Integer(string='Visitor Count')