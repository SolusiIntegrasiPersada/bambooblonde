from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv.expression import AND, NEGATIVE_TERM_OPERATORS
from odoo.tools import float_round

from collections import defaultdict

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