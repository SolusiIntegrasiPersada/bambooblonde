from odoo import fields, models, api, _
from odoo.osv import expression

class StockQuant(models.Model):
  _inherit = 'stock.quant'
  _order = 'location_id, product_id'

  code = fields.Char(string='Stock ID', related='product_id.default_code')
  barcode = fields.Char(string='Barcode', related='product_id.barcode')
  color = fields.Many2many('product.template.attribute.value', string="Size and Color")
  colour = fields.Char(string='Color', compute="_onchange_color_size")
  size = fields.Char(string='Size', compute="_onchange_color_size")
  brand_id = fields.Many2one('product.brand', string='Brand', related='product_id.brand')
  price = fields.Float(string='Price', related='product_id.standard_price')
  cost = fields.Float(string='Cost', related='product_id.lst_price')
  product = fields.Char(string='Product', related='product_id.name')
  quantity = fields.Float(string='Display')
  stock_type_id = fields.Many2one('stock.type', string='Stock Type', related='product_id.stock_type')
  name_warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', related='location_id.warehouse_id', store=True)
  barcode = fields.Char(string="Barcode", related='product_id.barcode')
  notes = fields.Text(string="Note")
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
  

