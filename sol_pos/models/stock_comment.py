from odoo import models, fields, api
from datetime import datetime, time

class StockLineComment(models.Model):
  _name = 'stock.line.comment'
  _description = 'Stock Line Comment'

  product_id = fields.Many2one('product.product', string='Stock Name', domain=[('available_in_pos','=','True')])
  color = fields.Many2many('product.template.attribute.value', string="Size and Color")
  colour = fields.Char(string='Color', compute="_onchange_color_size")
  size = fields.Char(string='Color', compute="_onchange_color_size")
  category_id = fields.Many2one('product.category', string='Category')
  stock_comment_id = fields.Many2one(comodel_name='stock.comment', string='stock', ondelete='cascade')
  comment = fields.Text(string='Comment')

  @api.onchange('product_id')
  def _onchange_department(self):
    if self.product_id:
      category_id = ''
      if self.product_id.categ_id:
        self.category_id = self.product_id.categ_id
      # self.qty = 1
      return category_id

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

class StockComment(models.Model):
  _name = 'stock.comment'
  _description = 'Stock Comment'
  _order = "id desc"

  name = fields.Char(string='No Reference')
  shop_name = fields.Many2one('pos.config', string='Shop Name')
  address = fields.Char(string='Address', compute='_onchange_address', store=True, required=True)
  periode = fields.Date(string='Periode', default=fields.Datetime.now)
  last_periode = fields.Date(string='Last Periode')
  stock_comment_ids = fields.One2many(comodel_name='stock.line.comment', inverse_name='stock_comment_id', string='stock')
  category_id = fields.Many2one('product.category', string='Category')

  @api.model
  def create(self, vals):
    res = super(StockComment, self).create(vals)
    res.name = self.env["ir.sequence"].next_by_code('stock.comment.seq')
    return res  

  @api.depends('shop_name')
  def _onchange_address(self):
    if self.shop_name:
      address = ''
      if self.shop_name.address:
        self.address = self.shop_name.address
      return address

  