from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PosOrder(models.Model):
    _inherit = "pos.order"

    note = fields.Text(string='Internal Notes', required=True)

    def _prepare_invoice_line(self, order_line):
        res = super(PosOrder, self)._prepare_invoice_line(order_line)
        if order_line.order_id.config_id.analytic_account_id:
            res.update({"analytic_account_id": order_line.order_id.config_id.analytic_account_id.id})
        return res

    @api.model
    def _amount_line_tax(self, line, fiscal_position_id):
        if line.absolute_discount:
            taxes = line.tax_ids.filtered(
                lambda t: t.company_id.id == line.order_id.company_id.id
            )
            if fiscal_position_id:
                taxes = fiscal_position_id.map_tax(
                    taxes, line.product_id, line.order_id.partner_id
                )
            price = line.price_unit - line.absolute_discount
            taxes = taxes.compute_all(
                price,
                line.order_id.pricelist_id.currency_id,
                line.qty,
                product=line.product_id,
                partner=line.order_id.partner_id or False,
            )["taxes"]
            return sum(tax.get("amount", 0.0) for tax in taxes)
        else:
            return super(PosOrder, self)._amount_line_tax(line, fiscal_position_id)

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['note'] = ui_order.get('note')
        return order_fields
    
    @api.model
    def create_from_ui(self, orders, draft=False):
        order_ids = super(PosOrder, self).create_from_ui(orders, draft)
        
        for order in self.sudo().browse([o["id"] for o in order_ids]):
            for line in order.lines:
                if line.product_id.is_voucher:
                    coupon_program = self.env['coupon.program']
                    coupon_program.create({
                        'name': 'Voucher Discount ' + str(line.price_unit),
                        'program_type': 'coupon_program',
                        'rule_products_domain': '[["available_in_pos","=",True]]',
                        'reward_type': 'discount',
                        'discount_type': 'fixed_amount',
                        'active': True,
                        'is_generate_pos': True,
                        'qty_generate': line.qty,
                        'discount_fixed_amount': line.price_unit,
                        'sold_in_pos_id': order.id,
                    })
                     
                    # vals = {'program_id': coupon_program.id}
                    # if  line.qty > 0:
                    #     for count in range(0, int(line.qty)):
                    #         coupon = self.env['coupon.coupon'].create(vals)

        return order_ids




class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    absolute_discount = fields.Float(string="Discount per Unit (abs)", default=0.0)
    cost_in_order = fields.Float(string="Cost in Order", default=0.0)
    
    
    @api.model
    def create(self, values):
        result = super(PosOrderLine,self).create(values)
        
        for line in result :
            line.cost_in_order = line.product_id.standard_price
        
        return result

    @api.depends(
        "price_unit", "tax_ids", "qty", "discount", "product_id", "absolute_discount"
    )
    def _compute_amount_line_all(self):
        super(PosOrderLine, self)._compute_amount_line_all()
        for line in self:
            fpos = line.order_id.fiscal_position_id
            tax_ids_after_fiscal_position = (
                fpos.map_tax(line.tax_ids, line.product_id, line.order_id.partner_id)
                if fpos
                else line.tax_ids
            )
            if line.absolute_discount:
                price = line.price_unit - line.absolute_discount
                taxes = tax_ids_after_fiscal_position.compute_all(
                    price,
                    line.order_id.pricelist_id.currency_id,
                    line.qty,
                    product=line.product_id,
                    partner=line.order_id.partner_id,
                )
                line.update(
                    {
                        "price_subtotal_incl": taxes["total_included"],
                        "price_subtotal": taxes["total_excluded"],
                    }
                )

    @api.onchange("qty", "discount", "price_unit", "tax_ids", "absolute_discount")
    def _onchange_qty(self):
        if self.product_id and self.absolute_discount:
            if not self.order_id.pricelist_id:
                raise UserError(_("You have to select a pricelist in the sale form !"))
            price = self.price_unit - self.absolute_discount
            self.price_subtotal = self.price_subtotal_incl = price * self.qty
            if self.product_id.taxes_id:
                taxes = self.product_id.taxes_id.compute_all(
                    price,
                    self.order_id.pricelist_id.currency_id,
                    self.qty,
                    product=self.product_id,
                    partner=False,
                )
                self.price_subtotal = taxes["total_excluded"]
                self.price_subtotal_incl = taxes["total_included"]
        else:
            super(PosOrderLine, self)._onchange_qty()
