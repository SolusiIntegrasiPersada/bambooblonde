from odoo import fields, models, api, _
from datetime import date
from odoo.exceptions import ValidationError

class StockOnHandPerStoreXlsx(models.AbstractModel):
  _name = 'report.sol_stock.report_soh_per_shop_xlsx' 
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, obj):
    money_format = workbook.add_format({'font_size': 9, 'font_name': 'arial', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', })
    border_basic = workbook.add_format({'font_size': 10, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, })
    number_style = workbook.add_format({'font_size': 9, 'font_name': 'arial', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'right', 'text_wrap': True, 'top': 1, 'left': 1, 'right': 1, 'bottom': 1,})
    
    style_basic = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'font': 'arial', })
    style_basic_section = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'font': 'arial' })
    style_basic_note = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font': 'arial' })
    style_basic_center = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'font': 'arial','top': 1, 'left': 1, 'right': 1, 'bottom': 1,'text_wrap': True, })
    style_basic_bold = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'font': 'arial', 'top': 1, 'left': 1, 'right': 1, 'bottom': 1, })
    style_basic_bold_center = workbook.add_format({'font_size': 9, 'align': 'center', 'valign': 'vcenter', 'bold': True, 'font': 'arial' })
    style_title = workbook.add_format({'font_size': 14, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'underline': True, 'font': 'arial' })
    style_address = workbook.add_format({'font_size': 14, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'font': 'arial' })

    format_header = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True, 'size': 10, 'top': 1, 'left': 1, 'right': 1, 'bottom': 1, 'text_wrap': True, 'font': 'arial', 'bg_color': '#8DB4E2'})

    datas = data.get('form', {})
    quant_ids = self.env['stock.quant'].sudo().search([
              ('name_warehouse_id', '=', datas.get('warehouse'))
    ])

    for i in quant_ids['name_warehouse_id']:

      worksheet = workbook.add_worksheet(i.name)

      # worksheet = workbook.add_worksheet('SOH')
      worksheet.set_column('A:A', 23)
      worksheet.set_column('B:B', 13)
      worksheet.set_column('C:C', 14)
      worksheet.set_column('D:D', 23)
      worksheet.set_column('E:E', 23)
      worksheet.set_column('F:F', 45)
      worksheet.set_column('G:G', 20)
      worksheet.set_column('H:H', 14)
      worksheet.set_column('I:I', 23)
      worksheet.set_column('J:J', 5)
      worksheet.set_column('K:K', 10)
      worksheet.set_column('L:L', 12)
      worksheet.set_column('M:M', 12)

      worksheet.merge_range('C1:D1', 'STOCK ON HAND PER STORE', style_title) 
      worksheet.merge_range('A2:B2', 'Print Date : %s' % (str(date.today())), style_basic)

      worksheet.merge_range('A3:A4', 'Store', format_header)
      worksheet.merge_range('B3:B4', 'Stock ID', format_header)
      worksheet.merge_range('C3:C4', 'Barcode', format_header)
      worksheet.merge_range('D3:D4', 'Model', format_header)
      worksheet.merge_range('E3:E4', 'Category', format_header)
      worksheet.merge_range('F3:F4', 'Sub Category', format_header)
      worksheet.merge_range('G3:G4', 'Stock Name', format_header)
      worksheet.merge_range('H3:H4', 'Color', format_header)
      worksheet.merge_range('I3:I4', 'Brand', format_header)
      worksheet.merge_range('J3:J4', 'Size', format_header)
      worksheet.merge_range('K3:K4', 'Stock', format_header)
      worksheet.merge_range('L3:L4', 'Price', format_header)
      worksheet.merge_range('M3:M4', 'Cost', format_header)

      no = 1
      row = 4
      col = 0
      # data = obj.location_id
      
      quant_ids = self.env['stock.quant'].sudo().search([
                ('name_warehouse_id', '=', datas.get('warehouse')),
      ])

      sum_qty = 0
      sum_price = 0
      sum_cost = 0
      
      for i in quant_ids:
        warehouse = i.name_warehouse_id.name or ''
        model_rec = self.env['product.category'].search([
              '&', ('category_product', '=', 'department'), 
              ('id', 'parent_of', i.product_categ_id.id)
        ]).mapped('name')
        category_rec = self.env['product.category'].search([
              '&', ('category_product', '=', 'category'), 
              ('id', 'parent_of', i.product_categ_id.id)
        ]).mapped('name')
        subcategory_rec = self.env['product.category'].search([
              '&', ('category_product', '=', 'subcategory'), 
              ('id', 'parent_of', i.product_categ_id.id)
        ]).mapped('name')
        model = '%s' % (''.join(model_rec)) or ''
        category = '%s' % (''.join(category_rec)) or ''
        subcategory = '%s' % (''.join(subcategory_rec)) or ''
        brand = i.brand_id.name or ''
        qty = i.available_quantity
        price = i.price
        cost = i.cost

        sum_qty += qty
        sum_price += price
        sum_cost += cost

        worksheet.write(row, 0, warehouse, style_basic_center)
        worksheet.write(row, 1, i['code'] or ' ', style_basic_center)
        worksheet.write(row, 2, i['barcode'] or ' ', style_basic_center)
        worksheet.write(row, 3, f'{model}', style_basic_center)
        worksheet.write(row, 4, f'{category}', style_basic_center)
        worksheet.write(row, 5, f'{subcategory}', style_basic_center)
        worksheet.write(row, 6, i['product'], style_basic_center)
        worksheet.write(row, 7, i['colour'], style_basic_center)
        worksheet.write(row, 8, brand, style_basic_center)
        worksheet.write(row, 9, i['size'], style_basic_center)
        worksheet.write(row, 10, qty, number_style)
        worksheet.write(row, 11, cost, money_format)
        worksheet.write(row, 12, price, money_format)
        row += 1
      row += 1  
        
      worksheet.merge_range('A' + str(row+1) + ':J' + str(row+1), 'Total', style_basic_bold)
      worksheet.write(row, 10, sum_qty, number_style)
      worksheet.write(row, 11, sum_price, money_format)
      worksheet.write(row, 12, sum_cost, money_format)