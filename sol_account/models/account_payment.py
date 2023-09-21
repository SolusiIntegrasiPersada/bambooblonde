from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    need_approval = fields.Boolean("Need Approval", default=False)

    @api.onchange("amount")
    def _onchange_amount(self):
        for payment in self:
            if payment.amount >= 500000000:
                payment.need_approval = True
            else:
                payment.need_approval = False

    def action_post(self):
        """draft -> posted"""
        if self.need_approval and not self.user_has_groups(
            "sol_account.payment_approval_group"
        ):
            raise ValidationError("You're not allowed to confirm this transfer")
        else:
            self.move_id._post(soft=False)

            self.filtered(
                lambda pay: pay.is_internal_transfer
                and not pay.paired_internal_transfer_payment_id
            )._create_paired_internal_transfer_payment()



    def button_cancel_posted_payments(self):
        print('Example')



    def button_abandon_cancel_posted_payments(self):
        print("Example")
