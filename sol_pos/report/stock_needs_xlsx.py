from odoo import fields, models, api, _
from datetime import date


class StockNeedsXlsx(models.AbstractModel):
  _name = 'report.sol_pos.report_stock_needs_xlsx' 
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, obj):
    money_format = workbook.add_format({'font_size': 10, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0.00' })
    border_basic = workbook.add_format({'font_size': 10, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, })
    number_style = workbook.add_format({'font_size': 9, 'font_name': 'arial', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'right','num_format': '#,##0'})
    
    style_basic = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'font': 'arial', })
    style_basic_section = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'font': 'arial' })
    style_basic_note = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font': 'arial' })
    style_basic_center = workbook.add_format({'font_size': 9, 'align': 'center', 'valign': 'vcenter', 'font': 'arial','top': 1, 'left': 1, 'right': 1, 'bottom': 1,'text_wrap': True, })
    style_basic_bold = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'font': 'arial', 'top': 1, 'left': 1, 'right': 1, 'bottom': 1, })
    style_basic_bold_center = workbook.add_format({'font_size': 9, 'align': 'center', 'valign': 'vcenter', 'bold': True, 'font': 'arial' })
    style_title = workbook.add_format({'font_size': 14, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'underline': True, 'font': 'arial' })
    style_address = workbook.add_format({'font_size': 14, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'font': 'arial' })

    format_header = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True, 'size': 12, 'top': 1, 'left': 1, 'right': 1, 'bottom': 1, 'text_wrap': True, 'font': 'arial'})

    worksheet = workbook.add_worksheet('Stock Needs')
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 25)
    worksheet.set_column('E:E', 18)
    worksheet.set_column('F:F', 22)
    worksheet.set_column('G:G', 22)
    worksheet.set_column('H:H', 10)


    get_data = self.env['product.category'].search([('id', 'parent_of', obj.category_id.id)]).mapped('name')
    separator = " / "

    worksheet.merge_range('A1:D1', '%s' % (obj.shop_name.name), style_address)
    worksheet.merge_range('A2:D2', '%s' % (obj.address), style_address)
    worksheet.merge_range('A4:D4', 'STOCK NEEDS', style_title)
    worksheet.merge_range('A5:D5', 'Periode : %s' % (obj.periode.strftime('%d %b, %Y')), style_basic)
    worksheet.merge_range('A6:D6', 'Category : %s' % (separator.join(get_data)), style_basic)
    # worksheet.merge_range('A6:B6', get_data, style_basic)

    worksheet.merge_range('A8:A9', 'NO', format_header)
    worksheet.merge_range('B8:B9', 'STOCK ID', format_header)
    worksheet.merge_range('C8:C9', 'STOCK NAME', format_header)
    worksheet.merge_range('D8:D9', 'COLOR', format_header)
    worksheet.merge_range('E8:E9', 'SIZE', format_header)
    worksheet.merge_range('F8:F9', 'MODEL', format_header)
    worksheet.merge_range('G8:G9', 'CATEGORY', format_header)
    worksheet.merge_range('H8:H9', 'QTY', format_header)

    no = 1
    row = 9
    
    data = obj.stock_ids
    for rec in data:
      model = self.env['product.category'].search([
              '&', ('category_product', '=', 'department'), 
              ('id', 'parent_of', rec.category_id.id)
      ]).mapped('name')
      category = self.env['product.category'].search([
            '&', ('category_product', '=', 'category'), 
            ('id', 'parent_of', rec.category_id.id)
      ]).mapped('name')
      worksheet.write(row, 0, no, style_basic_center)
      worksheet.write(row, 1, rec.product_id.default_code or "", style_basic_center)
      worksheet.write(row, 2, rec.product_id.name, style_basic_center)
      worksheet.write(row, 3, rec.colour, style_basic_center)
      worksheet.write(row, 4, rec.size, style_basic_center)
      worksheet.write(row, 5, '%s' % (''.join(model)) or "", style_basic_center)
      worksheet.write(row, 6, '%s' % (''.join(category)) or "", style_basic_center)
      worksheet.write(row, 7, rec.qty, number_style)
      row += 1
      no += 1
    
    # worksheet.merge_range(row, 1, "TOTAL", style_basic_bold)
    worksheet.merge_range('A' + str(row+1) + ':G' + str(row+1), 'Total', style_basic_bold)
    worksheet.write(row, 7, '=SUM(H10:H' + str(row) + ')', number_style)

    worksheet.write(row+1, 0, 'Print Date : %s' % (str(date.today())), style_basic)

  