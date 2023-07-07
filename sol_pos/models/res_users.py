from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    class ResUsers(models.Model):
        _inherit = 'res.users'

        pos_config_ids = fields.Many2many(
            comodel_name='pos.config',
            string='Allowed POS',
            help="Allowed Points of Sales for the user. "
                 "POS managers can use all POS.",
        )
