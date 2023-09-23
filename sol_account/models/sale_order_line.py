from odoo import _, api, fields, models




class SaleOrderLineInherit(models.Model):
  _inherit = 'sale.order.line'
  _description="sale Order Line"






  def _prepare_invoice_line(self, **optional_values):
    res = super(SaleOrderLineInherit, self)._prepare_invoice_line(**optional_values)
    partner = self.order_id.partner_id
    print("Sss")
    res.update({
      'analytic_account_id': partner.analytic_account_id.id,
    })

    return res

