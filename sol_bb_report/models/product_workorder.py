from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductWorkorder(models.Model):
    _inherit = 'product.workorder'

    date_approve = fields.Datetime(string='Confirmation Date', related='purchase_pw.date_approve')
    po_state = fields.Selection(string='Parent State', related='purchase_pw.state')
