from odoo import _, fields, api, models
from odoo.exceptions import UserError


class BuyerComp(models.Model):
  _name = 'buyer.comp'
  name = fields.Char('buyer')

class AttComp(models.Model):
  _name = 'att.comp'
  name = fields.Char('attention')

class LabelComp(models.Model):
  _name = 'label.comp'
  name = fields.Char('Label')

class ProductWorkorder(models.Model):
  _name = 'product.workorder'

  purchase_pw = fields.Many2one('purchase.order', string='PO')
  name = fields.Many2one('product.product', string='Style Name')
  fabric = fields.Many2one('product.product', string='Fabric')
  lining = fields.Many2one('product.product', string='Lining')
  color = fields.Char(string='Color')
  size = fields.Char(string='Size')
  image = fields.Image(string='Image')
  product_qty = fields.Float(string='Qty')
  price_unit = fields.Float(string='Price Unit')
  sample_comment = fields.Html(string='Sample Comment')


class PurchaseOrder(models.Model):
  _inherit = 'purchase.order'

  attention = fields.Many2one(comodel_name='att.comp', string='Attention')
  sub_suplier = fields.Many2many('res.partner.category', string='Division')
  brand = fields.Many2one('product.brand', string='Brand')
  buyer = fields.Many2one(comodel_name='buyer.comp',string='Buyer')
  sample_order_no = fields.Char(string='Order No')
  supplier_po = fields.Char('Supplier PO')
  po = fields.Char('PO')
  ordering_date = fields.Date(string='Delivery Date', states={'purchase': [('readonly', True)]})
  delivery_date = fields.Date(states={'purchase': [('readonly', True)]})
  pw_ids = fields.One2many(comodel_name='product.workorder', inverse_name='purchase_pw', string='Product from MO')
  product_qty = fields.Float(string='Quantity', default=1)
  product_mo = fields.Char(string='Style Name', store=True)
  is_sample = fields.Boolean(string="Is Sample", default=False)
  total_purchase_qty = fields.Integer(string="Total Quantity", compute="_compute_total_purchase_qty")

  ##SIGNATURE##
  prepared = fields.Many2one('res.users', string='Prepared By')
  ordered = fields.Many2one('res.users', string='Ordered By')
  approved = fields.Many2one('res.users', string='Approved By')

  qty_pax = fields.Integer(string='Pax')
  order_type = fields.Selection([("new_order","New Order"),("re_order","Re Order")], string='Order Type')
  
  def _compute_total_purchase_qty(self):
    for rec in self:
      if rec.order_line:
        for line in rec.order_line:
          rec.total_purchase_qty += line.product_qty
      else:
        rec.total_purchase_qty = 0

  @api.model
  def create(self, vals):
      res = super(PurchaseOrder, self).create(vals)
      # res.name = self.env["ir.sequence"].next_by_code("purchase.order.seq")
      if not vals.get("name") or vals.get("name") == "New":
          vals["name"] = (
              self.env["ir.sequence"].next_by_code("purchase.order.seq") or "New"
          )
      return res
  
  def _compute_product_name(self):
    for order in self:
      order.product_mo = order.order_line.mapped('product_id.name')

  def _prepare_invoice(self):
    """Prepare the dict of values to create the new invoice for a purchase order.
    """
    self.ensure_one()
    move_type = self._context.get('default_move_type', 'in_invoice')
    journal = self.env['account.move'].with_context(default_move_type=move_type)._get_default_journal()
    if not journal:
      raise UserError(_('Please define an accounting purchase journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

    partner_invoice_id = self.partner_id.address_get(['invoice'])['invoice']
    partner_bank_id = self.partner_id.commercial_partner_id.bank_ids.filtered_domain(['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])[:1]
    invoice_vals = {
      'ref': self.partner_ref or '',
      'move_type': move_type,
      'narration': self.notes,
      'currency_id': self.currency_id.id,
      'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
      'partner_id': partner_invoice_id,
      'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(partner_invoice_id)).id,
      'payment_reference': self.partner_ref or '',
      'partner_bank_id': partner_bank_id.id,
      'invoice_origin': self.name,
      'invoice_payment_term_id': self.payment_term_id.id,
      'invoice_line_ids': [],
      'company_id': self.company_id.id,
      'style_name_bill': self.product_mo,
    }
    return invoice_vals

  def _prepare_picking(self):
    res = super()._prepare_picking()
    res.update({'style_name': self.product_mo,})
    return res
 
class PurchaseOrderLine(models.Model):
  _inherit = 'purchase.order.line'

  product_id = fields.Many2one(string='Style Name')
  image = fields.Image(string='Image')
  fabric_por = fields.Many2one('product.product', string='Fabric')
  lining_por = fields.Many2one('product.product', string='Lining')
  color = fields.Many2many('product.template.attribute.value', string="Size and Color")
  colour = fields.Char('Color',compute="_onchange_color_size")
  size = fields.Char('Size',compute="_onchange_color_size")
  label = fields.Many2one(comodel_name='label.comp', string='Label')
  prod_comm = fields.Html(string='Comment')
  comment_bool = fields.Boolean(default=False)



  @api.onchange('product_id')
  def _onchange_image(self):
    if self.product_id:
      image = ''
      if self.product_id.image_1920:
        self.image = self.product_id.image_1920
      return image

  @api.depends('product_id')
  def _onchange_color_size(self):
    for i in self:
      c,s = '',''
      if i.product_id.product_template_variant_value_ids:
        i.color = i.product_id.product_template_variant_value_ids
        list_size = ['SIZE:','SIZES:','UKURAN:']
        list_color = ['COLOR:','COLOUR:','COLOURS:','COLORS:','WARNA:','CORAK:']
        for v in i.product_id.product_template_variant_value_ids:
          if any(v.display_name.upper().startswith(word) for word in list_color):
            c += ' '+v.name+' '
          elif any(v.display_name.upper().startswith(word) for word in list_size):
            s += ' '+v.name+' '
          else:
            c += ''
            s += ''
      else:
        c = ''
        s = ''
      i.colour = c
      i.size = s

            