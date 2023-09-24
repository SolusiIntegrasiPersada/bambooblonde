from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta

import io
import base64

header_table = ['No', 'Tanggal','Toko','Shift','Payment', 'Brand', 'Category', 'Barcode', 'Style Code', 'Size', 'Stock Name', 'Last Cost', 'Last Price', 'Qty Sold', 'Total', 'Total Sold', 'Margin']

class XlsxRekapPenjualan(models.Model):
    _name = 'report.sol_bb_report.rekap_penjualan.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        formatHeaderCompany = workbook.add_format({'font_size': 14, 'valign':'vcenter', 'align': 'center', 'bold': True})
        formatHeaderTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bold': True, 'bg_color':'#8db4e2', 'color':'black', 'text_wrap': True, 'border': 1})
        formatNormal = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'left', 'bold': True})
        formatNormalCenter = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'center', 'text_wrap': True, 'bold': True})
        formatNormalCurrencyCenter = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'center', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'bold': True})
        formatDetailTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'text_wrap': True, 'border': 1})
        formatDetailCurrencyTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0.00_-;-"Rp"* #,##0.00_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatImage = workbook.add_format({'text_wrap': True, 'border': 1})

        datas = data.get('form', {})
        
        pos_order_line = self.env['pos.order.line'].sudo().search([
            ('order_id.date_order', '>=', datas.get('from_date')),
            ('order_id.date_order', '<=', datas.get('to_date')),
            ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
        ])

        # datas.get('to_date').strptime('%Y-%m-%d').strftime('%d/%m/%Y')
        from_date = datetime.strptime(datas.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(datas.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')


        sheet = workbook.add_worksheet(f'Rekap Penjualan')
        for x in range(0, len(header_table)):
            sheet.set_column(x, x, 15)
        row = 1
        sheet.merge_range(row, 0, row, 1, 'Rekap Penjualan', formatNormal)
        row += 1
        sheet.merge_range(row, 0, row, 1, f'Dari Tanggal', formatNormal)
        sheet.merge_range(row, 2, row, 3, f': {from_date}', formatNormal)
        row += 1
        sheet.merge_range(row, 0, row, 1, f'Sampe Tanggal', formatNormal)
        sheet.merge_range(row, 2, row, 3, f': {to_date}', formatNormal)
        row += 1
        sheet.merge_range(row, 0, row, 1, f'Brand', formatNormal)
        row += 1
        sheet.merge_range(row, 0, row, 1, f'Category', formatNormal)
        row += 1
        sheet.merge_range(row, 0, row, 1, f'Cashier', formatNormal)
        row += 1
        sheet.merge_range(row, 0, row, 1, f'Shift', formatNormal)

        row += 1
        column = 0
        for header in header_table:
            sheet.write(row, column, header.upper(), formatHeaderTable)
            column += 1

        row += 1
        no = 1
        sum_last_cost= 0
        sum_last_price= 0
        sum_qty_sold= 0
        sum_total= 0
        sum_total_sold= 0
        for pol in pos_order_line:
            list_size = ['SIZE','SIZES','UKURAN']
            tanggal = pol.order_id.date_order.strftime('%d/%m/%Y') if pol.order_id.date_order else ''
            brand = pol.product_id.brand.name or ''
            category = pol.product_id.categ_id.name or ''
            barcode = pol.product_id.barcode or ''
            style_code = pol.product_id.default_code or ''
            size = ''
            for v in pol.product_id.product_template_variant_value_ids:
                if any(v.display_name.upper().startswith(word) for word in list_size):
                    size += v.name
            stock_name = pol.product_id.name or ''
            toko = pol.order_id.session_id.config_id.name or " "
            shift = pol.order_id.session_id.shift or " "
            last_cost = pol.product_id.standard_price
            last_price = pol.price_unit
            qty_sold = pol.qty
            total = last_cost * qty_sold
            total_sold = last_price * qty_sold
            margin = 0
            payment = pol.order_id.payment_ids[0].payment_method_id.name or '' if len(pol.order_id.payment_ids) > 0 else ''

            sum_last_cost += last_cost
            sum_last_price += last_price
            sum_qty_sold += qty_sold
            sum_total += total
            sum_total_sold += total_sold

            sheet.write(row, 0, no, formatDetailTableReOrder)
            sheet.write(row, 1, tanggal, formatDetailTableReOrder)
            sheet.write(row, 2, toko, formatDetailTableReOrder)
            sheet.write(row, 3, shift, formatDetailTableReOrder)
            sheet.write(row, 4, payment, formatDetailTableReOrder)
            sheet.write(row, 5, brand, formatDetailTableReOrder)
            sheet.write(row, 6, category, formatDetailTableReOrder)
            sheet.write(row, 7, barcode, formatDetailTableReOrder)
            sheet.write(row, 8, style_code, formatDetailTableReOrder)
            sheet.write(row, 7, size, formatDetailTableReOrder)
            sheet.write(row, 8, stock_name, formatDetailTableReOrder)
            sheet.write(row, 9, last_cost, formatDetailCurrencyTableReOrder)
            sheet.write(row, 10, last_price, formatDetailCurrencyTableReOrder)
            sheet.write(row, 11, qty_sold, formatDetailTableReOrder)
            sheet.write(row, 12, total, formatDetailCurrencyTableReOrder)
            sheet.write(row, 13, total_sold, formatDetailCurrencyTableReOrder)
            sheet.write(row, 14, margin, formatDetailCurrencyTableReOrder)

            row += 1
            no += 1
        row += 1
        sheet.write(row, 7, 'Grand Total', formatNormalCenter)
        sheet.write(row, 9, sum_last_cost, formatNormalCurrencyCenter)
        sheet.write(row, 10, sum_last_price, formatNormalCurrencyCenter)
        sheet.write(row, 11, sum_qty_sold, formatNormalCenter)
        sheet.write(row, 12, sum_total, formatNormalCurrencyCenter)
        sheet.write(row, 13, sum_total_sold, formatNormalCurrencyCenter)
                        