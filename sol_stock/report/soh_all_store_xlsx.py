from odoo import fields, models, api, _
from datetime import date

class StockOnHandAllStoreXlsx(models.AbstractModel):
  _name = 'report.sol_stock.report_soh_all_shop_xlsx' 
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, obj):
    money_format = workbook.add_format({'font_size': 9, 'font_name': 'arial', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0.00' })
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

    
    worksheet = workbook.add_worksheet('SOH')
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 14)
    worksheet.set_column('C:C', 41)
    worksheet.set_column('D:D', 16)
    worksheet.set_column('E:E', 13)
    worksheet.set_column('F:F', 9)
    worksheet.set_column('G:G', 7)
    worksheet.set_column('H:H', 21)
    worksheet.set_column('I:I', 21)
    worksheet.set_column('J:J', 21)
    worksheet.set_column('K:K', 14)

    worksheet.merge_range('C1:D1', 'STOCK ON HAND ALL STORE', style_title) 
    worksheet.merge_range('A2:B2', 'Print Date : %s' % (str(date.today())), style_basic)

    worksheet.merge_range('A3:A4', 'Store', format_header)
    worksheet.merge_range('B3:B4', 'Barcode', format_header)
    worksheet.merge_range('C3:C4', 'Stock Name', format_header)
    worksheet.merge_range('D3:D4', 'Stock ID', format_header)
    worksheet.merge_range('E3:E4', 'Color', format_header)
    worksheet.merge_range('F3:F4', 'Sizenum', format_header)
    worksheet.merge_range('G3:G4', 'QTY', format_header)
    worksheet.merge_range('H3:H4', 'Brand', format_header)
    worksheet.merge_range('I3:I4', 'Model', format_header)
    worksheet.merge_range('J3:J4', 'Stock Cat', format_header)
    worksheet.merge_range('K3:K4', 'Stock Type', format_header)

    no = 1
    row = 4
   
    # data = obj.location_id
    
    for rec in obj:
      model_rec = self.env['product.category'].search([
              '&', ('category_product', '=', 'department'), 
              ('id', 'parent_of', rec.product_categ_id.id)
        ]).mapped('name')
      category_rec = self.env['product.category'].search([
              '&', ('category_product', '=', 'category'), 
              ('id', 'parent_of', rec.product_categ_id.id)
        ]).mapped('name')
      subcategory_rec = self.env['product.category'].search([
              '&', ('category_product', '=', 'subcategory'), 
              ('id', 'parent_of', rec.product_categ_id.id)
        ]).mapped('name')

      worksheet.write(row, 0, rec.name_warehouse_id.name or "", style_basic_center)
      worksheet.write(row, 1, rec.barcode or "", style_basic_center)
      worksheet.write(row, 2, rec.product_id.name, style_basic_center)
      worksheet.write(row, 3, rec.code or "", style_basic_center)
      worksheet.write(row, 4, rec.colour, style_basic_center)
      worksheet.write(row, 5, rec.size, style_basic_center)
      worksheet.write(row, 6, rec.available_quantity, number_style)
      worksheet.write(row, 7, rec.brand_id.name or "",  style_basic_center)
      worksheet.write(row, 8, '%s' % (''.join(model_rec)) or "",  style_basic_center)
      worksheet.write(row, 9, '%s' % (''.join(category_rec)) or "",  style_basic_center)
      worksheet.write(row, 10, rec.stock_type_id.name or "",  style_basic_center)
      row += 1

    # @api.depends('ga_project_line_ids.total_price')
    # def _compute_ga_project(self):
    #     for this in self:
    #         this.ga_project = sum(this.ga_project_line_ids.mapped('total_price'))
            
    # worksheet.merge_range('A' + str(row+1) + ':G' + str(row+1), 'Total', style_basic_bold)
    # worksheet.write_formula(row, 7, '', number_style)
    # worksheet.write_formula(row, 8, '', number_style)