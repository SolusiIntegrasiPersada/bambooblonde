from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta

import io
import base64

header_table = ['Sales ID', 'Sales Date', 'Sales Time', 'Client No', 'Member Name', 'Outlet ID', 'Outlet Name', 'Staff', 'Staff Name', 'Credit Card Type', 'Credit Card No', 'Credit Card Name', 'Credit Card Expired Date', 'Credit Card Charge', 'Credit Card Authorisation', 'Credit Card Amount', 'Bank Name', 'Notes', 'Cash Amount', 'Voucher', 'Void', 'Void Date', 'Void Staff', 'Void Staff Name', 'Change', 'Shift Code', 'Card Bank', 'Nation ID', 'Nation Desc', 'Sale SP', 'Sales Person', 'Void Note', 'Barcode', 'Qty', 'Total Price', 'Total Cost', 'Stock Name', 'Stock ID', 'Color', 'Size Num', 'Model', 'Category', 'Stock Type', 'Stock Class']

class XlsxSalesReportDetail(models.Model):
    _name = 'report.sol_bb_report.sales_report_detail.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        formatHeaderCompany = workbook.add_format({'font_size': 16, 'valign':'vcenter', 'align': 'center', 'bold': True})
        formatHeaderTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bold': True, 'bg_color':'#8db4e2', 'color':'black', 'text_wrap': True, 'border': 1})
        formatDetailTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True, 'border': 1})
        formatDetailCurrencyTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatImage = workbook.add_format({'text_wrap': True, 'border': 1})

        datas = data.get('form', {})
        from_date = datetime.strptime(datas.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(datas.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        
        pos_order_line = self.env['pos.order.line'].sudo().search([
            ('order_id.date_order', '>=', datas.get('from_date')),
            ('order_id.date_order', '<=', datas.get('to_date')),
            ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
            ('price_subtotal_incl', '>', 0),
        ])


        sheet = workbook.add_worksheet(f'Sales DetailS')
        for x in range(0, len(header_table)):
            sheet.set_column(x, x, 15)
        row = 1

        sheet.merge_range(row, 0, row, len(header_table)-1, f'Sales Report Detail {from_date} - {to_date}', formatHeaderCompany)
        row += 2
        column = 0
        for header in header_table:
            sheet.write(row, column, header.upper(), formatHeaderTable)
            column += 1

        row += 1
        no = 1
        for pol in pos_order_line:
            sales_id = pol.order_id.pos_reference
            sales_date = pol.order_id.date_order.strftime('%d/%m/%Y') if pol.order_id.date_order else ''
            sales_time = pol.order_id.date_order.strftime('%H:%M:%S') if pol.order_id.date_order else ''
            client_no = f'HO0{str(int(pol.discount))}' if pol.discount else 'Cash'
            member_name = f'HO0{str(int(pol.discount))}' if pol.discount else 'Cash'
            outlet_id = pol.order_id.session_id.config_id.id
            outlet_name = pol.order_id.session_id.config_id.name or ''
            staff_id = pol.order_id.session_id.id
            staff_name = pol.order_id.session_id.name or ''
            credit_card_type = ''
            credit_card_no = ''
            credit_card_name = ''
            credit_card_exp_date = ''
            credit_card_charge = 0
            credit_card_authorisation = ''
            credit_card_amount = 0
            bank_name = ''
            notes = pol.order_id.note or ''
            cash_amount = 0
            voucher = ''
            void = ''
            void_date = ''
            void_staff = ''
            void_staff_name = ''
            change = 0
            shift_code = ''
            card_bank = ''
            nation_id = ''
            nation_desc = ''
            sale_sp = ''
            sales_person = ''
            void_notes = ''
            barcode = pol.product_id.barcode or ''
            qty = pol.qty or 0
            total_price = pol.price_subtotal_incl
            total_cost = pol.product_id.standard_price * qty
            stock_name = pol.product_id.name or ''
            stock_id = pol.product_id.default_code or ''

            list_size = ['SIZE','SIZES','UKURAN']
            list_color = ['COLOR:','COLOUR:','COLOURS:','COLORS:','WARNA:','CORAK:']
            color = ''
            size_num = ''
            for v in pol.product_id.product_template_variant_value_ids:
                if any(v.display_name.upper().startswith(word) for word in list_size):
                    size_num += v.name
                if any(v.display_name.upper().startswith(word) for word in list_color):
                    color += v.name
            
            model = ''
            category = pol.product_id.categ_id.name or ''
            stock_type = pol.product_id.stock_type.name or ''
            stock_class = pol.product_id.class_product.name or ''

            # brand = pol.company_id.name or ''
            # category = pol.product_id.categ_id.name or ''
            # barcode = pol.product_id.barcode or ''
            # style_code = pol.product_id.default_code or ''
            # stock_class = pol.product_id.class_product.name or ''

            # stock_name = pol.product_id.name or ''
            # last_cost = pol.product_id.standard_price
            # last_price = pol.price_unit
            # qty_sold = pol.qty
            # total = last_cost * qty_sold
            # total_sold = last_price * qty_sold
            # margin = 0
            # payment = pol.order_id.payment_ids[0].payment_method_id.name or '' if len(pol.order_id.payment_ids) > 0 else ''

            sheet.write(row, 0, sales_id, formatDetailTableReOrder)
            sheet.write(row, 1, sales_date, formatDetailTableReOrder)
            sheet.write(row, 2, sales_time, formatDetailTableReOrder)
            sheet.write(row, 3, client_no, formatDetailTableReOrder)
            sheet.write(row, 4, member_name, formatDetailTableReOrder)
            sheet.write(row, 5, outlet_id, formatDetailTableReOrder)
            sheet.write(row, 6, outlet_name, formatDetailTableReOrder)
            sheet.write(row, 7, staff_id, formatDetailTableReOrder)
            sheet.write(row, 8, staff_name, formatDetailTableReOrder)
            sheet.write(row, 9, credit_card_type, formatDetailTableReOrder)
            sheet.write(row, 10, credit_card_no, formatDetailTableReOrder)
            sheet.write(row, 11, credit_card_name, formatDetailTableReOrder)
            sheet.write(row, 12, credit_card_exp_date, formatDetailTableReOrder)
            sheet.write(row, 13, credit_card_charge, formatDetailTableReOrder)
            sheet.write(row, 14, credit_card_authorisation, formatDetailTableReOrder)
            sheet.write(row, 15, credit_card_amount, formatDetailTableReOrder)
            sheet.write(row, 16, bank_name, formatDetailTableReOrder)
            sheet.write(row, 17, notes, formatDetailTableReOrder)
            sheet.write(row, 18, cash_amount, formatDetailTableReOrder)
            sheet.write(row, 19, voucher, formatDetailTableReOrder)
            sheet.write(row, 20, void, formatDetailTableReOrder)
            sheet.write(row, 21, void_date, formatDetailTableReOrder)
            sheet.write(row, 22, void_staff, formatDetailTableReOrder)
            sheet.write(row, 23, void_staff_name, formatDetailTableReOrder)
            sheet.write(row, 24, change, formatDetailTableReOrder)
            sheet.write(row, 25, shift_code, formatDetailTableReOrder)
            sheet.write(row, 26, card_bank, formatDetailTableReOrder)
            sheet.write(row, 27, nation_id, formatDetailTableReOrder)
            sheet.write(row, 28, nation_desc, formatDetailTableReOrder)
            sheet.write(row, 29, sale_sp, formatDetailTableReOrder)
            sheet.write(row, 30, sales_person, formatDetailTableReOrder)
            sheet.write(row, 31, void_notes, formatDetailTableReOrder)
            sheet.write(row, 32, barcode, formatDetailTableReOrder)
            sheet.write(row, 33, qty, formatDetailTableReOrder)
            sheet.write(row, 34, total_price, formatDetailCurrencyTable)
            sheet.write(row, 35, total_cost, formatDetailCurrencyTable)
            sheet.write(row, 36, stock_name, formatDetailTableReOrder)
            sheet.write(row, 37, stock_id, formatDetailTableReOrder)
            sheet.write(row, 38, color, formatDetailTableReOrder)
            sheet.write(row, 39, size_num, formatDetailTableReOrder)
            sheet.write(row, 40, model, formatDetailTableReOrder)
            sheet.write(row, 41, category, formatDetailTableReOrder)
            sheet.write(row, 42, stock_type, formatDetailTableReOrder)
            sheet.write(row, 43, stock_class, formatDetailTableReOrder)

            row += 1
            no += 1
                        