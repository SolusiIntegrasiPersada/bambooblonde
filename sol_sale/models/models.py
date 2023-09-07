from odoo import models, fields, api


class SalesOrder(models.Model):
    _inherit = "sale.order"

    # def default_warehouse(self):
    #   return self.env['stock.warehouse'].search(['|', ('name', '=', 'FINISH GOODS FROM SEWING SUPPLIER'), ('company_id')], limit=1).id

    po_number = fields.Char("PO No")
    source = fields.Many2one("purchase.order", string="Source Document PO")
    so_number = fields.Char("SO No")
    prepared = fields.Char(string="Prepared By")
    ordered = fields.Many2one("res.users", string="Ordered By")
    approved = fields.Many2one("res.users", string="Approved By")
    style_name = fields.Char(
        string="Style Name", related="order_line.product_id.name", store=True
    )
    total_sale_qty = fields.Integer(
        string="Total Quantity", compute="_compute_total_sale_qty"
    )
    # warehouse_id = fields.Many2one(
    #   'stock.warehouse', string='Warehouse',
    #   required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
    #   default=default_warehouse, check_company=True)

    @api.model
    def create(self, vals):
        res = super(SalesOrder, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("sale.order.seq")
        return res

    def action_confirm(self):
        res = super(SalesOrder, self).action_confirm()
        for order in self:
            order.picking_ids.write(
                {
                    "style_name": order.style_name,
                }
            )
            return res

    def _compute_total_sale_qty(self):
        for rec in self:
            if rec.order_line:
                for line in rec.order_line:
                    rec.total_sale_qty += line.product_uom_qty
            else:
                rec.total_sale_qty = 0

    # @api.depends("partner_id", "date_order")
    # def _compute_analytic_account_id(self):
    #     for order in self:
    #         analytic_account = order.env["account.analytic.account"].search(
    #             [("partner_id", "=", order.partner_id.id)]
    #         )
    #         if analytic_account:
    #             order.analytic_account_id = analytic_account
    #         else:
    #             if not order.analytic_account_id:
    #                 default_analytic_account = (
    #                     order.env["account.analytic.default"]
    #                     .sudo()
    #                     .account_get(
    #                         partner_id=order.partner_id.id,
    #                         user_id=order.env.uid,
    #                         date=order.date_order,
    #                         company_id=order.company_id.id,
    #                     )
    #                 )
    #                 order.analytic_account_id = default_analytic_account.analytic_id


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # color = fields.Many2one('product.product', string="Size and Color")
    colour = fields.Char("Color", compute="_onchange_color_size")
    size = fields.Char("Size", compute="_onchange_color_size")
    color = fields.Char("Color")
    # size = fields.Char('Size')

    @api.depends("product_id")
    def _onchange_color_size(self):
        for i in self:
            c, s = "", ""
            if i.product_id.product_template_variant_value_ids:
                i.color = i.product_id.product_template_variant_value_ids
                list_size = ["SIZE:", "SIZES:", "UKURAN:"]
                list_color = [
                    "COLOR:",
                    "COLOUR:",
                    "COLOURS:",
                    "COLORS:",
                    "WARNA:",
                    "CORAK:",
                ]
                for v in i.product_id.product_template_variant_value_ids:
                    if any(
                        v.display_name.upper().startswith(word) for word in list_color
                    ):
                        c += " " + v.name + " "
                    elif any(
                        v.display_name.upper().startswith(word) for word in list_size
                    ):
                        s += " " + v.name + " "
                    else:
                        c += ""
                        s += ""
            else:
                c = ""
                s = ""
            i.colour = c
            i.size = s
