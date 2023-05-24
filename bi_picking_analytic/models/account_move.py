from odoo import fields, api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Analytic Account",
        index=True,
        store=True,
        readonly=False,
        check_company=True,
        copy=True,
    )

    @api.onchange("partner_id")
    def _onchange_customer(self):
        analytic_account = self.env["account.analytic.account"].search(
            [("partner_id", "=", self.partner_id.id)]
        )
        self.analytic_account_id = analytic_account.id


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Analytic Account",
        index=True,
        store=True,
        readonly=False,
        check_company=True,
        copy=True,
        related="move_id.analytic_account_id",
    )
