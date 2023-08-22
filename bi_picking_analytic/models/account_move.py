from odoo import fields, api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange("partner_id")
    def _onchange_customer(self):
        analytic_account = self.env["account.analytic.account"].search(
            [("partner_id", "=", self.partner_id.id)]
        )
        for line in self.invoice_line_ids:
            line.analytic_account_id = analytic_account.id
