
from datetime import datetime

from odoo import models
from pytz import timezone
import pytz

header_table = ['Sales ID', 'Sales Date', 'Sales Time', 'Client No', 'Member Name', 'Outlet ID', 'Outlet Name', 'Staff Name', 'Credit Card Amount', 'Bank Name', 'Notes', 'Cash Amount', 'Voucher', 'Void', 'Void Date', 'Void Staff Name', 'Change', 'Shift Code', 'Card Bank', 'Nation ID', 'Nation Desc', 'Void Note', 'Barcode', 'Qty', 'Total Price', 'Total Cost', 'Stock Name', 'Stock ID', 'Color', 'Size Num', 'Model', 'Category', 'Stock Type', 'Stock Class']

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
        ])
        
        # function
        
        def compute_amount_payment(order, payment_method):
            amount = 0
            if payment_method == "bank" :
                amount = sum(order.payment_ids.filtered(lambda x: x.payment_method_id.journal_id.type == 'bank').mapped('amount'))
            if payment_method == "bank_name" :
                bank_name = order.payment_ids.filtered(lambda x: x.payment_method_id.journal_id.type == 'bank')
                if bank_name :
                    return bank_name[0].payment_method_id.name
                else :
                    return ""
            if payment_method == "cash" :
                amount = sum(order.payment_ids.filtered(lambda x: x.payment_method_id.journal_id.type == 'cash' and x.amount > 0).mapped('amount'))
            if payment_method == "change" :
                amount = abs(sum(order.payment_ids.filtered(lambda x: x.amount < 0 ).mapped('amount')))
            if payment_method == "voucher" :
                amount = abs(sum(order.lines.filtered(lambda x: x.product_id.is_produk_promotion).mapped('price_subtotal_incl')))
                
            if payment_method == "void" :
                if order.amount_total > 0 :
                    return "False"
                else :
                    return "True"
                
            if amount > 0 :
                return amount
            else :
                return ""


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
        for pol in pos_order_line.filtered(lambda x: not x.product_id.is_shooping_bag and not x.product_id.is_produk_diskon and not x.product_id.is_produk_promotion):
            sales_id = pol.order_id.pos_reference.replace("Order ","")
            date_orders = pytz.UTC.localize(pol.order_id.date_order).astimezone(
                    timezone(self.env.user.tz or 'UTC'))
            sales_date = date_orders.strftime('%d/%m/%Y') if date_orders else ''
            sales_time = date_orders.strftime('%H:%M:%S') if date_orders else ''
            # client_no = f'HO0{str(int(pol.discount))}' if pol.discount else 'Cash'
            client_no = pol.order_id.partner_id.ref if pol.order_id.partner_id else ''
            member_name = pol.order_id.partner_id.name if pol.order_id.partner_id else ''
            outlet_id = pol.order_id.session_id.config_id.outlet_id or ''
            outlet_name = pol.order_id.session_id.config_id.name or ''
            staff_name = pol.order_id.note if pol.order_id.note else ''
            credit_card_amount = compute_amount_payment(pol.order_id, "bank")
            bank_name = compute_amount_payment(pol.order_id, "bank_name") or ''
            notes = pol.customer_note or ''
            cash_amount = compute_amount_payment(pol.order_id, "cash")
            voucher = compute_amount_payment(pol.order_id, "voucher")
            void = compute_amount_payment(pol.order_id, "void")
            void_date = sales_date if void == "True" else ""
            void_staff_name = staff_name if void == "True" else ""
            change = compute_amount_payment(pol.order_id, "change")
            shift_code = pol.order_id.session_id.shift or ''
            card_bank = bank_name or ''
            nation_id = pol.order_id.region_id.sequence or ''
            nation_desc = pol.order_id.region_id.name or ''
            void_notes = notes if void == "True" else ""
            barcode = pol.product_id.barcode or ''
            qty = pol.qty or 0
            total_price = pol.price_subtotal_incl or ''
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
            
            model = pol.product_id.product_model_categ_id.name or ""
            category = pol.product_id.categ_id.name or ''
            stock_type = pol.product_id.stock_type.name or ''
            stock_class = pol.product_id.class_product.name or ''


            sheet.write(row, 0, sales_id, formatDetailTableReOrder)
            sheet.write(row, 1, sales_date, formatDetailTableReOrder)
            sheet.write(row, 2, sales_time, formatDetailTableReOrder)
            sheet.write(row, 3, client_no, formatDetailTableReOrder)
            sheet.write(row, 4, member_name, formatDetailTableReOrder)
            sheet.write(row, 5, outlet_id, formatDetailTableReOrder)
            sheet.write(row, 6, outlet_name, formatDetailTableReOrder)
            sheet.write(row, 7, staff_name, formatDetailTableReOrder)
            sheet.write(row, 8, credit_card_amount, formatDetailCurrencyTable)
            sheet.write(row, 9, bank_name, formatDetailTableReOrder)
            sheet.write(row, 10, notes, formatDetailTableReOrder)
            sheet.write(row, 11, cash_amount, formatDetailCurrencyTable)
            sheet.write(row, 12, voucher, formatDetailCurrencyTable)
            sheet.write(row, 13, void, formatDetailTableReOrder)
            sheet.write(row, 14, void_date, formatDetailTableReOrder)
            sheet.write(row, 15, void_staff_name, formatDetailTableReOrder)
            sheet.write(row, 16, change, formatDetailCurrencyTable)
            sheet.write(row, 17, shift_code, formatDetailTableReOrder)
            sheet.write(row, 18, card_bank, formatDetailTableReOrder)
            sheet.write(row, 19, nation_id, formatDetailTableReOrder)
            sheet.write(row, 20, nation_desc, formatDetailTableReOrder)
            sheet.write(row, 21, void_notes, formatDetailTableReOrder)
            sheet.write(row, 22, barcode, formatDetailTableReOrder)
            sheet.write(row, 23, qty, formatDetailTableReOrder)
            sheet.write(row, 24, total_price, formatDetailCurrencyTable)
            sheet.write(row, 25, total_cost, formatDetailCurrencyTable)
            sheet.write(row, 26, stock_name, formatDetailTableReOrder)
            sheet.write(row, 27, stock_id, formatDetailTableReOrder)
            sheet.write(row, 28, color, formatDetailTableReOrder)
            sheet.write(row, 29, size_num, formatDetailTableReOrder)
            sheet.write(row, 30, model, formatDetailTableReOrder)
            sheet.write(row, 31, category, formatDetailTableReOrder)
            sheet.write(row, 32, stock_type, formatDetailTableReOrder)
            sheet.write(row, 33, stock_class, formatDetailTableReOrder)




            row += 1
            no += 1
                        