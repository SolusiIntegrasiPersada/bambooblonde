from odoo import _, api, fields, models
from odoo.exceptions import UserError
import base64

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)

    state_bill = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('approve', 'Approved'),
            ('cancel', 'Cancelled'),
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    
    transfer = fields.Many2one('account.journal', string='Transfer to Bank')
    style_name_invc = fields.Char(string='Style Name', related='invoice_line_ids.product_id.name')
    style_name_bill = fields.Char(string='Style Name')
    is_manager_approve = fields.Boolean(compute='_compute_is_manager_approve', string='Is Manager Approve')
    
    @api.depends('name','state_bill')
    def _compute_is_manager_approve(self):
        self = self.sudo()
        for i in self:
            if i.amount_total > 500000000:
                if i.state_bill == 'posted' and self.user_has_groups("sol_account.manager_group_approval_bill"):
                    i.is_manager_approve = True
                else:
                    i.is_manager_approve = False
            else:
                if i.state_bill == 'posted' and self.user_has_groups("sol_account.additional_group_approval_bill"):
                    i.is_manager_approve = True
                else:
                    i.is_manager_approve = False

    ## Signature Naming
    prepared = fields.Many2one('res.users', string='Prepared By', default=_get_default_requested_by)
    ordered = fields.Many2one('hr.employee', string='Ordered By')
    approved = fields.Many2one('hr.employee', string='Approved By')


    def action_post(self):
        res = super(AccountMove,self).action_post()
        self.state_bill = 'posted'
        return res

    def approve_posted_bill(self):
        self.state_bill = 'approve'

    def action_invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        if any(not move.is_invoice(include_receipts=True) for move in self):
            raise UserError(_("Only invoices could be printed."))

        self.filtered(lambda inv: not inv.is_move_sent).write({'is_move_sent': True})
        if self.user_has_groups('account.group_account_invoice'):
            return self.env.ref('sol_account.report_accounting_action').report_action(self)
        
    
    def action_invoice_sent(self):
        self.ensure_one()
        result = super(AccountMove,self).action_invoice_sent()
        report = self.env.ref('sol_account.report_accounting_action')._render_qweb_pdf(self.id)
        pdf_attachment_id = self.env['ir.attachment'].create({
            'name': 'INV - ',
            'datas': base64.b64encode(report[0]),
            # 'datas_fname': self.pdf,
            'res_model': 'mail.compose.message',
            'res_id': self.ids[0],
            'type': 'binary',
            'mimetype': 'application/x-pdf',
        })

        result['context'].update({
            'attachment_ids': [(6,0,[pdf_attachment_id.id])]
        })

        return result


    def button_process_edi_web_services(self):
        print('Example')