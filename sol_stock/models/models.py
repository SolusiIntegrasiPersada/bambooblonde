
from odoo import models, fields, api
import datetime

class StockPickingType(models.Model):
  _inherit = 'stock.picking.type'

  mandatory_source = fields.Boolean('Required Source Documents', default=False)

class StockPicking(models.Model):
  _inherit = 'stock.picking'

  origin_pr = fields.Many2one('purchase.request', 'Source Document', index=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, help="Reference of the document")
  mandatory_source = fields.Boolean(related='picking_type_id.mandatory_source', string='Required Source Documents', readonly=True, related_sudo=False)
  style_name = fields.Char(string="Style Name")
  # analytic_account_id = fields.Many2one('account.analytic.account',string='Analytic Account')
  mrp_id = fields.Many2one('mrp.production', string="MRP")
  count = fields.Integer(string="Count Service")
  location_dest_id_internal = fields.Many2one(
    'stock.location', "Destination Location",
    default=lambda self: self.env['stock.picking.type'].browse(
      self._context.get('default_picking_type_id')).default_location_dest_id,
    domain=[('is_transit', '=', True)],
    check_company=True, readonly=True,
    states={'draft': [('readonly', False)]})
  is_manufacture = fields.Boolean(string="Is Manufacturing", related='company_id.is_manufacturing', readonly=True)

  @api.onchange("location_dest_id_internal")
  def _onchange_location_transfer(self):
    for i in self:
      if i.location_dest_id_internal:
        location = ''
        if i.location_dest_id:
          i.location_dest_id = i.location_dest_id_internal
        return location


class StockMove(models.Model):
  _inherit = 'stock.move'

  fabric_width = fields.Float(string="Fabric Width", related='product_id.fabric_width')
  price = fields.Float(string="Cost", related='product_id.standard_price')
  image = fields.Image(string='Image', related='product_id.image_1920')
  color_ids = fields.Many2many('product.template.attribute.value', string="Size and Color")
  colour = fields.Char('Color', compute="_onchange_color_size")
  size = fields.Char('Size', compute="_onchange_color_size")

  @api.depends('product_id')
  def _onchange_color_size(self):
    for i in self:
      c, s = '', ''
      if i.product_id.product_template_variant_value_ids:
        i.color_ids = i.product_id.product_template_variant_value_ids
        list_size = ['SIZE:', 'SIZES:', 'UKURAN:']
        list_color = ['COLOR:', 'COLOUR:', 'COLOURS:', 'COLORS:', 'WARNA:', 'CORAK:']
        for v in i.product_id.product_template_variant_value_ids:
          if any(v.display_name.upper().startswith(word) for word in list_color):
            c += ' ' + v.name + ' '
          elif any(v.display_name.upper().startswith(word) for word in list_size):
            s += ' ' + v.name + ' '
          else:
            c += ''
            s += ''
      else:
        c = ''
        s = ''
      i.colour = c
      i.size = s

class StockMoveLine(models.Model):
  _inherit = 'stock.move.line'

  color_ids = fields.Many2many('product.template.attribute.value', string="Size and Color")
  colour = fields.Char('Color', compute="_onchange_color_size")
  size = fields.Char('Size', compute="_onchange_color_size")

  @api.depends('product_id')
  def _onchange_color_size(self):
    for i in self:
      c, s = '', ''
      if i.product_id.product_template_variant_value_ids:
        i.color_ids = i.product_id.product_template_variant_value_ids
        list_size = ['SIZE:', 'SIZES:', 'UKURAN:']
        list_color = ['COLOR:', 'COLOUR:', 'COLOURS:', 'COLORS:', 'WARNA:', 'CORAK:']
        for v in i.product_id.product_template_variant_value_ids:
          if any(v.display_name.upper().startswith(word) for word in list_color):
            c += ' ' + v.name + ' '
          elif any(v.display_name.upper().startswith(word) for word in list_size):
            s += ' ' + v.name + ' '
          else:
            c += ''
            s += ''
      else:
        c = ''
        s = ''
      i.colour = c
      i.size = s

