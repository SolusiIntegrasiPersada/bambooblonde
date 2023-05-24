import xlsxwriter
import base64
from odoo import fields, models, api
from io import BytesIO
from datetime import date, datetime, timedelta
from pytz import timezone
import pytz
import io
from PIL import Image


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    # def compute_attributes(self):
    #     for line in self:
    #         color = ''
    #         size = ''

    #         if line.product_id.product_template_variant_value_ids:
    #             for a in line.product_id.product_template_variant_value_ids:
    #                 if a.display_type == 'color':
    #                     color = a.name
    #                 elif a.display_type == 'radio':
    #                     size = a.name
    #                 else:
    #                     color = ''
    #                     size = ''
    #         line.color = color
    #         line.size = size

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
          i.color = c
          i.size = s

    color = fields.Char('Color', compute='_onchange_color_size')
    size = fields.Char('Size', compute='_onchange_color_size')