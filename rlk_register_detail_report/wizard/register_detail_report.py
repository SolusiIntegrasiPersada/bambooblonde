import xlsxwriter
import base64
from odoo import fields, models, api
from io import BytesIO
from datetime import datetime
from pytz import timezone
import pytz
import io
from PIL import Image


class RegisterDetailReport(models.TransientModel):
    _name = "register.detail.report"
    _description = "Register Detail Report .xlsx"

    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone(self.env.user.tz or 'UTC'))

    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)
    start_period = fields.Date('Start Period')
    end_period = fields.Date('End Period')
    config_id = fields.Many2one('pos.config', 'Point of Sale')
    shift = fields.Selection(
        [('ALL', 'ALL'), ('Shift A', 'Shift A'), ('Shift B', 'Shift B')], 'Shift', default='ALL')

    # @api.onchange('start_period')
    # def onchange_end_period(self):
    #     self.end_period = self.start_period

    def print_excel_report(self):
        data = self.read()[0]
        pos_name = self.config_id.name
        address = self.config_id.address or ''
        config_id = self.config_id.id
        start_period = data['start_period']
        end_period = data['end_period']

        datetime_string = self.get_default_date_model().strftime("%Y-%m-%d %H:%M:%S")
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        report_name = 'Register Detail Report'
        filename = '%s %s' % (report_name, date_string)

        columns = [
            ('Date', 17, 'datetime', 'char'),
            ('Nationality', 15, 'char', 'char'),
            ('Invoice', 18, 'char', 'char'),
            ('Total Sales', 15, 'float', 'float'),
            ('Cash Rp', 15, 'float', 'float'),
            ('Cash US$', 15, 'float', 'float'),
            ('Cash Euro', 15, 'float', 'float'),
            ('Cash JPY', 15, 'float', 'float'),
            ('Cash AUD', 15, 'float', 'float'),
            ('Cash Other', 15, 'float', 'float'),
            ('Credit Card', 15, 'float', 'float'),
            ('Charge', 15, 'float', 'float'),
            ('Discount', 15, 'float', 'float'),
            ('Return', 15, 'float', 'float'),
            ('Voucher', 15, 'float', 'float'),
            ('Net Sales', 15, 'float', 'float'),
        ]

        domain = [('state', 'not in', ['draft', 'cancel'])]

        if self.shift == 'ALL':
            domain += [('date_order', '>=', self.start_period),
                       ('date_order', '<=', self.end_period)]
        elif self.shift == 'Shift A':
            domain += [('date_order', '>=', self.start_period), ('date_order',
                                                                 '<=', self.end_period), ('session_id.shift', '=', 'Shift A')]
        elif self.shift == 'Shift B':
            domain += [('date_order', '>=', self.start_period), ('date_order',
                                                                 '<=', self.end_period), ('session_id.shift', '=', 'Shift B')]
        if config_id :
            domain += [('config_id', '=', self.config_id.id)]

        
        orders = self.env['pos.order'].search(domain)

        result = []

       
        for order in orders:
           
            shift = order.session_id.shift
            region = order.region_id.name
            region_count = len(self.env['visitor.region'].search([]))
            start_at = self.start_period
            stop_at = self.end_period
            date_order = order.date_order
            invoice = order.pos_reference
            lineplus = order.lines.filtered(lambda x: x.price_subtotal_incl > 0)
            # pricexqty = 0
            # for plus in lineplus :s
            #     pricexqty += plus.price_unit * plus.qty
            pricexqty = sum(plus.price_unit * plus.qty for plus in lineplus)
            total_sales = pricexqty
            price_inc = sum(lineplus.mapped('price_subtotal_incl'))
            discount = pricexqty - price_inc
            total_return = abs(order.amount_total) if order.amount_total < 0 else 0
            payment_cash = sum(order.payment_ids.filtered(
                lambda x: x.payment_method_id.journal_id.type == 'cash' and x.amount > 0).mapped('amount'))
            payment_cc = sum(order.payment_ids.filtered(
                lambda x: x.payment_method_id.journal_id.type == 'bank' and x.amount > 0).mapped('amount'))
            
            amount_coupon = 0
            coupon = order.lines.filtered(lambda x: x.product_id.is_produk_promotion)
            if coupon :
                amount_coupon = abs(sum(coupon.mapped('price_subtotal_incl')))
            
            discount_member = order.lines.filtered(lambda x: x.product_id.is_produk_diskon)
            if discount_member :
                discount += abs(sum(discount_member.mapped('price_subtotal_incl')))

            result.append({'shift': shift, 'region': region, 'region_count': region_count, 'start_at': start_at, 'stop_at': stop_at, 'date_order': date_order, 'invoice': invoice, 'total_sales': total_sales, 'discount': discount, 'total_return': total_return, 'payment_cash': payment_cash, 'payment_cc': payment_cc, 'coupon' : amount_coupon})

        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf, workbook = self.add_workbook_format(workbook)

        cashier = str(self.shift)

        worksheet = workbook.add_worksheet(report_name)
        worksheet.merge_range('A1:N2', str(pos_name), wbf['title_doc'])
        worksheet.merge_range('A3:N3', str(address), wbf['title_doc2'])
        worksheet.merge_range('A4:N4', '', wbf['title_doc2'])
        worksheet.merge_range('A5:N6', 'Register Detail', wbf['title_doc'])
        worksheet.merge_range('A7:N7', 'Period : ' + str(start_period) +
                              ' s/d ' + str(end_period), wbf['title_doc2'])
        worksheet.merge_range('A8:N8', 'Staf/Cashier : ' +
                              str(cashier), wbf['title_doc2'])
        worksheet.merge_range('A9:N9', '', wbf['title_doc2'])
        worksheet.merge_range('O1:P9', '', wbf['title_doc2'])

        def calculate_scale(file_path, bound_size):
            # check the image size without loading it into memory
            im = Image.open(file_path)
            original_width, original_height = im.size

            # calculate the resize factor, keeping original aspect and staying within boundary
            bound_width, bound_height = bound_size
            ratios = (float(bound_width) / original_width,
                      float(bound_height) / original_height)
            return min(ratios)

        if self.env.user.company_id.logo:
            logo_company = io.BytesIO(
                base64.b64decode(self.env.user.company_id.logo))
            bound_width_height = (240, 240)
            resize_scale = calculate_scale(logo_company, bound_width_height)
            worksheet.insert_image('N3:P6', "image.png", {
                                   'image_data': logo_company, 'bg_color': '#FFFFFF', 'x_scale': resize_scale, 'y_scale': resize_scale})

        if self.shift == 'ALL':
            row = 10

            col = 0
            for column in columns:
                column_name = column[0]
                column_width = column[1]
                column_type = column[2]
                worksheet.set_column(col, col, column_width)
                worksheet.write(row-1, col, column_name, wbf['header_smoke'])

                col += 1

            worksheet.merge_range('A11:P11', 'Shift A', wbf['title_doc3'])

            row += 2
            row1 = row
            no = 1

            column_float_number = {}

            total_sales_per_shift1 = total_paymentcash_per_shift1 = total_paymentcc_per_shift1 = total_discount_per_shift1 = total_return_per_shift1 = total_netsales_per_shift1 = total_voucher3_per_shift1 = total_sales_per_shift2 = total_paymentcash_per_shift2 = total_paymentcc_per_shift2 = total_discount_per_shift2 = total_return_per_shift2 = total_netsales_per_shift2 = total_voucher3_per_shift2 = total_sales_per_date = total_paymentcash_per_date = total_paymentcc_per_date = total_discount_per_date = total_return_per_date = total_netsales_per_date = total_voucher3_per_date = grand_total_sales = grand_total_paymentcash = grand_total_paymentcc = grand_total_discount = grand_total_return = grand_total_netsales = grand_total_voucher3 = 0

            shift = ''

            no_shift1 = 0
            no_shift2 = 0
            region_count = ''
            for res in result:
                shift = res['shift']

                region_name = res['region']
                if res['region'] == 'We':
                    region_name = 'Westerner'
                elif res['region'] == 'Ina':
                    region_name = 'Indonesia'
                elif res['region'] == 'Japa':
                    region_name = 'Japan'
                elif res['region'] == 'Aus':
                    region_name = 'Australian'

                date_order = pytz.UTC.localize(res['date_order']).astimezone(
                    timezone(self.env.user.tz or 'UTC'))
                region_count = str(res['region'])
                total_sales = res['total_sales']
                payment_cash = res['payment_cash']
                payment_cc = res['payment_cc']
                if res['total_sales'] < 0:
                    total_sales = abs(res['total_sales'])
                    payment_cash = '-'
                    payment_cc = '-'
                
                net_sales = res['total_sales'] - res['total_return']
                total_return = res['total_return']
                discount = res['discount']
                voucher = res['coupon']

                if shift == 'Shift A':
                    no_shift1 += 1
                    worksheet.write(
                        row-1, 0, date_order.strftime('%Y-%m-%d %H:%M:%S'), wbf['content'])
                    worksheet.write(
                        row-1, 1, region_name or '', wbf['content2'])
                    worksheet.write(row-1, 2, res['invoice'], wbf['content'])
                    worksheet.write(row-1, 3, total_sales,
                                    wbf['content_float'])
                    worksheet.write(row-1, 4, payment_cash,
                                    wbf['content_float'])
                    worksheet.write(row-1, 5, '-', wbf['content2'])
                    worksheet.write(row-1, 6, '-', wbf['content2'])
                    worksheet.write(row-1, 7, '-', wbf['content2'])
                    worksheet.write(row-1, 8, '-', wbf['content2'])
                    worksheet.write(row-1, 9, '-', wbf['content2'])
                    worksheet.write(row-1, 10, payment_cc,
                                    wbf['content_float'])
                    worksheet.write(row-1, 11, '-', wbf['content2'])
                    worksheet.write(row-1, 12, discount, wbf['content_float'])
                    worksheet.write(row-1, 13, total_return,
                                    wbf['content_float'])
                    worksheet.write(row-1, 14, voucher, wbf['content2'])
                    worksheet.write(row-1, 15, net_sales, wbf['content_float'])

                    row += 1
                    no += 1

                    payment_cash = res['payment_cash'] or 0
                    payment_cc = res['payment_cc'] or 0
                    if total_sales:
                        total_sales_per_shift1 += total_sales
                    if payment_cash:
                        total_paymentcash_per_shift1 += payment_cash
                    if payment_cc:
                        total_paymentcc_per_shift1 += payment_cc
                    if discount:
                        total_discount_per_shift1 += discount
                    if total_return:
                        total_return_per_shift1 += total_return
                    if net_sales:
                        total_netsales_per_shift1 += net_sales
                    if voucher:
                        total_voucher3_per_shift1 += voucher

            row1 = row-1
            worksheet.merge_range('A%s:C%s' % (row, row),
                                  'Total Per Shift A', wbf['total_smoke'])
            worksheet.write(row1, 3, total_sales_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 4, total_paymentcash_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 10, total_paymentcc_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 12, total_discount_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 13, total_return_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 14, total_voucher3_per_shift1, wbf['total_float_smoke2'])
            worksheet.write(row1, 15, total_netsales_per_shift1,
                            wbf['total_float_smoke'])
            row1 += 2

            worksheet.merge_range('A%s:P%s' % (
                row1, row1), 'Shift B', wbf['title_doc3'])
            row1 += 1

            for res in result:
                shift = res['shift']
                region_name = res['region']
                if res['region'] == 'We':
                    region_name = 'Westerner'
                elif res['region'] == 'Ina':
                    region_name = 'Indonesia'
                elif res['region'] == 'Japa':
                    region_name = 'Japan'
                elif res['region'] == 'Aus':
                    region_name = 'Australian'
                date_order = pytz.UTC.localize(res['date_order']).astimezone(
                    timezone(self.env.user.tz or 'UTC'))
                region_count = str(res['region_count']) + \
                    ' (' + str(res['region']) + ')'
                total_sales = res['total_sales']
                payment_cash = res['payment_cash']
                payment_cc = res['payment_cc']
                if res['total_sales'] < 0:
                    total_sales = abs(res['total_sales'])
                    payment_cash = '-'
                    payment_cc = '-'
                
                net_sales = res['total_sales'] - res['total_return']
                total_return = res['total_return']
                discount = res['discount']
                voucher = res['coupon']

                if shift == 'Shift B':
                    no_shift2 += 1
                    worksheet.write(
                        row1-1, 0, date_order.strftime('%Y-%m-%d %H:%M:%S'), wbf['content'])
                    worksheet.write(row1-1, 1, region_name, wbf['content2'])
                    worksheet.write(row1-1, 2, res['invoice'], wbf['content'])
                    worksheet.write(row1-1, 3, total_sales,
                                    wbf['content_float'])
                    worksheet.write(row1-1, 4, payment_cash,
                                    wbf['content_float'])
                    worksheet.write(row1-1, 5, '-', wbf['content2'])
                    worksheet.write(row1-1, 6, '-', wbf['content2'])
                    worksheet.write(row1-1, 7, '-', wbf['content2'])
                    worksheet.write(row1-1, 8, '-', wbf['content2'])
                    worksheet.write(row1-1, 9, '-', wbf['content2'])
                    worksheet.write(row1-1, 10, payment_cc,
                                    wbf['content_float'])
                    worksheet.write(row1-1, 11, '-', wbf['content2'])
                    worksheet.write(row1-1, 12, discount, wbf['content_float'])
                    worksheet.write(row1-1, 13, total_return,
                                    wbf['content_float'])
                    worksheet.write(row1-1, 14, voucher, wbf['content2'])
                    worksheet.write(row1-1, 15, net_sales,
                                    wbf['content_float'])

                    row1 += 1
                    no += 1

                    payment_cash = res['payment_cash'] or 0
                    payment_cc = res['payment_cc'] or 0
                    if total_sales:
                        total_sales_per_shift2 += total_sales
                    if payment_cash:
                        total_paymentcash_per_shift2 += payment_cash
                    if payment_cc:
                        total_paymentcc_per_shift2 += payment_cc
                    if discount:
                        total_discount_per_shift2 += discount
                    if total_return:
                        total_return_per_shift2 += total_return
                    if net_sales:
                        total_netsales_per_shift2 += net_sales
                    if voucher:
                        total_voucher3_per_shift2 += voucher

            row2 = row1
            worksheet.merge_range('A%s:C%s' % (
                row2, row2), 'Total Per Shift B', wbf['total_smoke'])
            worksheet.write(row2-1, 3, total_sales_per_shift2,
                            wbf['total_float_smoke'])
            worksheet.write(
                row2-1, 4, total_paymentcash_per_shift2, wbf['total_float_smoke'])
            worksheet.write(row2-1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 10, total_paymentcc_per_shift2,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 12, total_discount_per_shift2,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 13, total_return_per_shift2,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 14, total_voucher3_per_shift2, wbf['total_float_smoke2'])
            worksheet.write(row2-1, 15, total_netsales_per_shift2,
                            wbf['total_float_smoke'])
            row2 += 1

            total_sales_per_date = total_sales_per_shift1 + total_sales_per_shift2
            total_paymentcash_per_date = total_paymentcash_per_shift1 + \
                total_paymentcash_per_shift2
            total_paymentcc_per_date = total_paymentcc_per_shift1 + total_paymentcc_per_shift2
            total_discount_per_date = total_discount_per_shift1 + total_discount_per_shift2
            total_return_per_date = total_return_per_shift1 + total_return_per_shift2
            total_netsales_per_date = total_netsales_per_shift1 + total_netsales_per_shift2
            total_voucher3_per_date = total_voucher3_per_shift1 + total_voucher3_per_shift2

            grand_total_sales = total_sales_per_date
            grand_total_paymentcash = total_paymentcash_per_date
            grand_total_paymentcc = total_paymentcc_per_date
            grand_total_discount = total_discount_per_date
            grand_total_return = total_return_per_date
            grand_total_netsales = total_netsales_per_date
            grand_total_voucher3 = total_voucher3_per_date

            worksheet.merge_range('A%s:C%s' % (row2, row2), 'Total Per ' + str(
                self.start_period) + " s/d " + str(self.end_period), wbf['total_smoke'])
            worksheet.write(row2-1, 3, total_sales_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 4, total_paymentcash_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 10, total_paymentcc_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 12, total_discount_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 13, total_return_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 14, total_voucher3_per_date, wbf['total_float_smoke2'])
            worksheet.write(row2-1, 15, total_netsales_per_date,
                            wbf['total_float_smoke'])
            row2 += 1
            worksheet.merge_range('A%s:C%s' % (
                row2, row2), 'Grand Total', wbf['total_smoke'])
            worksheet.write(row2-1, 3, grand_total_sales,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 4, grand_total_paymentcash,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 10, grand_total_paymentcc,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 12, grand_total_discount,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 13, grand_total_return,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 14, grand_total_voucher3, wbf['total_float_smoke2'])
            worksheet.write(row2-1, 15, grand_total_netsales,
                            wbf['total_float_smoke'])

        if self.shift == 'Shift A':
            row = 10

            col = 0
            for column in columns:
                column_name = column[0]
                column_width = column[1]
                column_type = column[2]
                worksheet.set_column(col, col, column_width)
                worksheet.write(row-1, col, column_name, wbf['header_smoke'])

                col += 1

            worksheet.merge_range('A11:P11', 'Shift A', wbf['title_doc3'])

            row += 2
            row1 = row
            no = 1

            column_float_number = {}

            total_sales_per_shift1 = total_paymentcash_per_shift1 = total_paymentcc_per_shift1 = total_discount_per_shift1 = total_return_per_shift1 = total_netsales_per_shift1 = total_voucher_per_shift1 = total_sales_per_shift2 = total_paymentcash_per_shift2 = total_paymentcc_per_shift2 = total_discount_per_shift2 = total_return_per_shift2 = total_netsales_per_shift2 = total_sales_per_date = total_paymentcash_per_date = total_paymentcc_per_date = total_discount_per_date = total_return_per_date = total_netsales_per_date = total_voucher_per_date = grand_total_sales = grand_total_paymentcash = grand_total_paymentcc = grand_total_discount = grand_total_return = grand_total_netsales = grand_total_voucher = 0

            shift = ''

            no_shift1 = 0
            no_shift2 = 0
            for res in result:
                shift = res['shift']

                date_order = pytz.UTC.localize(res['date_order']).astimezone(
                    timezone(self.env.user.tz or 'UTC'))
                total_sales = res['total_sales']

                region_name = res['region']
                if res['region'] == 'We':
                    region_name = 'Westerner'
                elif res['region'] == 'Ina':
                    region_name = 'Indonesia'
                elif res['region'] == 'Japa':
                    region_name = 'Japan'
                elif res['region'] == 'Aus':
                    region_name = 'Australian'

                payment_cash = res['payment_cash']
                payment_cc = res['payment_cc']
                if res['total_sales'] < 0:
                    total_sales = abs(res['total_sales'])
                    payment_cash = '-'
                    payment_cc = '-'
                
                total_return = res['total_return']
                discount = res['discount']
                net_sales = res['total_sales'] - res['total_return'] - res['discount']
                voucher = res['coupon']

                if shift == 'Shift A':
                    no_shift1 += 1
                    worksheet.write(
                        row-1, 0, date_order.strftime('%Y-%m-%d %H:%M:%S'), wbf['content'])
                    worksheet.write(row-1, 1, region_name, wbf['content2'])
                    worksheet.write(row-1, 2, res['invoice'], wbf['content'])
                    worksheet.write(row-1, 3, total_sales,
                                    wbf['content_float'])
                    worksheet.write(row-1, 4, payment_cash,
                                    wbf['content_float'])
                    worksheet.write(row-1, 5, '-', wbf['content2'])
                    worksheet.write(row-1, 6, '-', wbf['content2'])
                    worksheet.write(row-1, 7, '-', wbf['content2'])
                    worksheet.write(row-1, 8, '-', wbf['content2'])
                    worksheet.write(row-1, 9, '-', wbf['content2'])
                    worksheet.write(row-1, 10, payment_cc,
                                    wbf['content_float'])
                    worksheet.write(row-1, 11, '-', wbf['content2'])
                    worksheet.write(row-1, 12, discount, wbf['content_float'])
                    worksheet.write(row-1, 13, total_return,
                                    wbf['content_float'])
                    worksheet.write(row-1, 14, voucher, wbf['content2'])
                    worksheet.write(row-1, 15, net_sales, wbf['content_float'])

                    row += 1
                    no += 1

                    payment_cash = res['payment_cash'] or 0
                    payment_cc = res['payment_cc'] or 0
                    if total_sales:
                        total_sales_per_shift1 += total_sales
                    if payment_cash:
                        total_paymentcash_per_shift1 += payment_cash
                    if payment_cc:
                        total_paymentcc_per_shift1 += payment_cc
                    if discount:
                        total_discount_per_shift1 += discount
                    if total_return:
                        total_return_per_shift1 += total_return
                    if net_sales:
                        total_netsales_per_shift1 += net_sales
                    if voucher :
                        total_voucher_per_shift1 += voucher

            row1 = row-1
            worksheet.merge_range('A%s:C%s' % (row, row),
                                  'Total Per Shift A', wbf['total_smoke'])
            worksheet.write(row1, 3, total_sales_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 4, total_paymentcash_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 10, total_paymentcc_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row1, 12, total_discount_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 13, total_return_per_shift1,
                            wbf['total_float_smoke'])
            worksheet.write(row1, 14, total_voucher_per_shift1, wbf['total_float_smoke2'])
            worksheet.write(row1, 15, total_netsales_per_shift1,
                            wbf['total_float_smoke'])
            row1 += 2

            total_sales_per_date = total_sales_per_shift1
            total_paymentcash_per_date = total_paymentcash_per_shift1
            total_paymentcc_per_date = total_paymentcc_per_shift1
            total_discount_per_date = total_discount_per_shift1
            total_return_per_date = total_return_per_shift1
            total_netsales_per_date = total_netsales_per_shift1
            total_voucher_per_date = total_voucher_per_shift1

            grand_total_sales = total_sales_per_date
            grand_total_paymentcash = total_paymentcash_per_date
            grand_total_paymentcc = total_paymentcc_per_date
            grand_total_discount = total_discount_per_date
            grand_total_return = total_return_per_date
            grand_total_netsales = total_netsales_per_date
            grand_total_voucher = total_voucher_per_date

            row2 = row1
            worksheet.merge_range('A%s:C%s' % (row2, row2), 'Total Per ' + str(
                self.start_period) + " s/d " + str(self.end_period), wbf['total_smoke'])
            worksheet.write(row2-1, 3, total_sales_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 4, total_paymentcash_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 10, total_paymentcc_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 12, total_discount_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 13, total_return_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 14, total_voucher_per_date, wbf['total_float_smoke2'])
            worksheet.write(row2-1, 15, total_netsales_per_date,
                            wbf['total_float_smoke'])
            row2 += 1
            worksheet.merge_range('A%s:C%s' % (
                row2, row2), 'Grand Total', wbf['total_smoke'])
            worksheet.write(row2-1, 3, grand_total_sales,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 4, grand_total_paymentcash,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 10, grand_total_paymentcc,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 12, grand_total_discount,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 13, grand_total_return,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 14, grand_total_voucher, wbf['total_float_smoke2'])
            worksheet.write(row2-1, 15, grand_total_netsales,
                            wbf['total_float_smoke'])

        if self.shift == 'Shift B':
            row = 10

            col = 0
            for column in columns:
                column_name = column[0]
                column_width = column[1]
                column_type = column[2]
                worksheet.set_column(col, col, column_width)
                worksheet.write(row-1, col, column_name, wbf['header_smoke'])

                col += 1

            worksheet.merge_range('A11:P11', 'Shift B', wbf['title_doc3'])

            row += 2
            row1 = row
            no = 1

            column_float_number = {}

            total_sales_per_shift1 = total_paymentcash_per_shift1 = total_paymentcc_per_shift1 = total_discount_per_shift1 = total_return_per_shift1 = total_netsales_per_shift1 = total_voucher2_per_shift1 = total_sales_per_shift2 = total_paymentcash_per_shift2 = total_paymentcc_per_shift2 = total_discount_per_shift2 = total_return_per_shift2 = total_netsales_per_shift2 = total_voucher2_per_shift2 = total_sales_per_date = total_paymentcash_per_date = total_paymentcc_per_date = total_discount_per_date = total_return_per_date = total_netsales_per_date = total_voucher2_per_date = grand_total_sales = grand_total_paymentcash = grand_total_paymentcc = grand_total_discount = grand_total_return = grand_total_netsales = grand_total_voucher2 = 0

            shift = ''
            start_at_date = ''
            stop_at_date = ''
            start_at_shift1 = ''
            stop_at_shift1 = ''
            start_at_shift2 = ''
            stop_at_shift2 = ''
            no_shift1 = 0
            no_shift2 = 0

            no_shift2 = 0
            no = 0
            for res in result:
                shift = res['shift']

                date_order = pytz.UTC.localize(res['date_order']).astimezone(
                    timezone(self.env.user.tz or 'UTC'))
                total_sales = res['total_sales']

                region_name = res['region']
                if res['region'] == 'We':
                    region_name = 'Westerner'
                elif res['region'] == 'Ina':
                    region_name = 'Indonesia'
                elif res['region'] == 'Japa':
                    region_name = 'Japan'
                elif res['region'] == 'Aus':
                    region_name = 'Australian'

                payment_cash = res['payment_cash']
                payment_cc = res['payment_cc']
                if res['total_sales'] < 0:
                    total_sales = abs(res['total_sales'])
                    payment_cash = '-'
                    payment_cc = '-'
                amount_return = 0
                net_sales = res['total_sales'] - res['total_return']
                total_return = res['total_return']
                discount = res['discount']
                voucher = res['coupon']

                if shift == 'Shift B':
                    no_shift2 += 1
                    worksheet.write(
                        row1-1, 0, date_order.strftime('%Y-%m-%d %H:%M:%S'), wbf['content'])
                    worksheet.write(row1-1, 1, region_name, wbf['content2'])
                    worksheet.write(row1-1, 2, res['invoice'], wbf['content'])
                    worksheet.write(row1-1, 3, total_sales,
                                    wbf['content_float'])
                    worksheet.write(row1-1, 4, payment_cash,
                                    wbf['content_float'])
                    worksheet.write(row1-1, 5, '-', wbf['content2'])
                    worksheet.write(row1-1, 6, '-', wbf['content2'])
                    worksheet.write(row1-1, 7, '-', wbf['content2'])
                    worksheet.write(row1-1, 8, '-', wbf['content2'])
                    worksheet.write(row1-1, 9, '-', wbf['content2'])
                    worksheet.write(row1-1, 10, payment_cc,
                                    wbf['content_float'])
                    worksheet.write(row1-1, 11, '-', wbf['content2'])
                    worksheet.write(row1-1, 12, discount, wbf['content_float'])
                    worksheet.write(row1-1, 13, total_return,
                                    wbf['content_float'])
                    worksheet.write(row1-1, 14, voucher, wbf['content2'])
                    worksheet.write(row1-1, 15, net_sales,
                                    wbf['content_float'])

                    row1 += 1
                    no += 1

                    payment_cash = res['payment_cash'] or 0
                    payment_cc = res['payment_cc'] or 0
                    if total_sales:
                        total_sales_per_shift2 += total_sales
                    if payment_cash:
                        total_paymentcash_per_shift2 += payment_cash
                    if payment_cc:
                        total_paymentcc_per_shift2 += payment_cc
                    if discount:
                        total_discount_per_shift2 += discount
                    if total_return:
                        total_return_per_shift2 += total_return
                    if net_sales:
                        total_netsales_per_shift2 += net_sales
                    if voucher:
                        total_voucher2_per_shift2 += voucher

            row2 = row1
            worksheet.merge_range('A%s:C%s' % (
                row2, row2), 'Total Per Shift B', wbf['total_smoke'])
            worksheet.write(row2-1, 3, total_sales_per_shift2,
                            wbf['total_float_smoke'])
            worksheet.write(
                row2-1, 4, total_paymentcash_per_shift2, wbf['total_float_smoke'])
            worksheet.write(row2-1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 10, total_paymentcc_per_shift2,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 12, total_discount_per_shift2,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 13, total_return_per_shift2,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 14, total_voucher2_per_shift2, wbf['total_float_smoke2'])
            worksheet.write(row2-1, 15, total_netsales_per_shift2,
                            wbf['total_float_smoke'])
            row2 += 1

            total_sales_per_date = total_sales_per_shift2
            total_paymentcash_per_date = total_paymentcash_per_shift2
            total_paymentcc_per_date = total_paymentcc_per_shift2
            total_discount_per_date = total_discount_per_shift2
            total_return_per_date = total_return_per_shift2
            total_netsales_per_date = total_netsales_per_shift2
            total_voucher2_per_date = total_voucher2_per_shift2

            grand_total_sales = total_sales_per_date
            grand_total_paymentcash = total_paymentcash_per_date
            grand_total_paymentcc = total_paymentcc_per_date
            grand_total_discount = total_discount_per_date
            grand_total_return = total_return_per_date
            grand_total_netsales = total_netsales_per_date
            grand_total_voucher2 = total_voucher2_per_date

            worksheet.merge_range('A%s:C%s' % (row2, row2), 'Total Per ' + str(
                self.start_period) + " s/d " + str(self.end_period), wbf['total_smoke'])
            worksheet.write(row2-1, 3, total_sales_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 4, total_paymentcash_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 10, total_paymentcc_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 12, total_discount_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 13, total_return_per_date,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 14, total_voucher2_per_date, wbf['total_float_smoke2'])
            worksheet.write(row2-1, 15, total_netsales_per_date,
                            wbf['total_float_smoke'])
            row2 += 1
            worksheet.merge_range('A%s:C%s' % (
                row2, row2), 'Grand Total', wbf['total_smoke'])
            worksheet.write(row2-1, 3, grand_total_sales,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 4, grand_total_paymentcash,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 5, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 6, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 7, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 8, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 9, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 10, grand_total_paymentcc,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 11, '-', wbf['total_float_smoke2'])
            worksheet.write(row2-1, 12, grand_total_discount,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 13, grand_total_return,
                            wbf['total_float_smoke'])
            worksheet.write(row2-1, 14, grand_total_voucher2, wbf['total_float_smoke2'])
            worksheet.write(row2-1, 15, grand_total_netsales,
                            wbf['total_float_smoke'])

        workbook.close()
        out = base64.encodestring(fp.getvalue())
        self.write({'datas': out, 'datas_fname': filename})
        fp.close()
        filename += '%2Exlsx'

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model='+self._name+'&id='+str(self.id)+'&field=datas&download=true&filename='+filename,
        }

    def add_workbook_format(self, workbook):
        colors = {
            'white_orange': '#FFFFDB',
            'orange': '#FFC300',
            'red': '#FF0000',
            'yellow': '#F6FA03',
            'pink': '#FF69B4',
            'violet': '#EE82EE',
            'smoke': '#F5F5F5',
        }

        wbf = {}
        wbf['header'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': '#FFFFDB', 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header'].set_border()

        wbf['header_smoke'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['smoke'], 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_smoke'].set_border()

        wbf['header_pink'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['pink'], 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_pink'].set_border()

        wbf['header_violet'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['violet'], 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_violet'].set_border()

        wbf['header_orange'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['orange'], 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_orange'].set_border()

        wbf['header_yellow'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['yellow'], 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_yellow'].set_border()

        wbf['header_no'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': '#FFFFDB', 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_no'].set_border()
        wbf['header_no'].set_align('vcenter')

        wbf['footer'] = workbook.add_format(
            {'align': 'left', 'font_name': 'Georgia'})

        wbf['content_datetime'] = workbook.add_format(
            {'num_format': 'yyyy-mm-dd hh:mm:ss', 'font_name': 'Georgia'})
        wbf['content_datetime'].set_left()
        wbf['content_datetime'].set_right()

        wbf['content_date'] = workbook.add_format(
            {'num_format': 'yyyy-mm-dd', 'font_name': 'Georgia'})
        wbf['content_date'].set_left()
        wbf['content_date'].set_right()

        wbf['title_doc'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 20,
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc2'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 14,
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc3'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })
        wbf['title_doc3'].set_top()
        wbf['title_doc3'].set_bottom()
        wbf['title_doc3'].set_left()
        wbf['title_doc3'].set_right()

        wbf['company'] = workbook.add_format(
            {'align': 'left', 'font_name': 'Georgia'})
        wbf['company'].set_font_size(11)

        wbf['content'] = workbook.add_format()
        wbf['content'].set_left()
        wbf['content'].set_right()

        wbf['content2'] = workbook.add_format(
            {'align': 'center', 'font_name': 'Georgia'})
        wbf['content2'].set_left()
        wbf['content2'].set_right()

        wbf['content_float'] = workbook.add_format(
            {'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_float'].set_right()
        wbf['content_float'].set_left()

        wbf['content_number'] = workbook.add_format(
            {'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_number'].set_right()
        wbf['content_number'].set_left()

        wbf['content_percent'] = workbook.add_format(
            {'align': 'right', 'num_format': '0.00%', 'font_name': 'Georgia'})
        wbf['content_percent'].set_right()
        wbf['content_percent'].set_left()

        wbf['total_float'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['white_orange'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float'].set_top()
        wbf['total_float'].set_bottom()
        wbf['total_float'].set_left()
        wbf['total_float'].set_right()

        wbf['total_number'] = workbook.add_format(
            {'align': 'right', 'bg_color': colors['white_orange'], 'bold': 1, 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_number'].set_top()
        wbf['total_number'].set_bottom()
        wbf['total_number'].set_left()
        wbf['total_number'].set_right()

        wbf['total'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['white_orange'], 'align': 'center', 'font_name': 'Georgia'})
        wbf['total'].set_left()
        wbf['total'].set_right()
        wbf['total'].set_top()
        wbf['total'].set_bottom()

        wbf['total_float_yellow'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['yellow'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_yellow'].set_top()
        wbf['total_float_yellow'].set_bottom()
        wbf['total_float_yellow'].set_left()
        wbf['total_float_yellow'].set_right()

        wbf['total_number_yellow'] = workbook.add_format(
            {'align': 'right', 'bg_color': colors['yellow'], 'bold': 1, 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_number_yellow'].set_top()
        wbf['total_number_yellow'].set_bottom()
        wbf['total_number_yellow'].set_left()
        wbf['total_number_yellow'].set_right()

        wbf['total_yellow'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['yellow'], 'align': 'center', 'font_name': 'Georgia'})
        wbf['total_yellow'].set_left()
        wbf['total_yellow'].set_right()
        wbf['total_yellow'].set_top()
        wbf['total_yellow'].set_bottom()

        wbf['total_float_orange'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['orange'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_orange'].set_top()
        wbf['total_float_orange'].set_bottom()
        wbf['total_float_orange'].set_left()
        wbf['total_float_orange'].set_right()

        wbf['total_number_orange'] = workbook.add_format(
            {'align': 'right', 'bg_color': colors['orange'], 'bold': 1, 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_number_orange'].set_top()
        wbf['total_number_orange'].set_bottom()
        wbf['total_number_orange'].set_left()
        wbf['total_number_orange'].set_right()

        wbf['total_orange'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['orange'], 'align': 'center', 'font_name': 'Georgia'})
        wbf['total_orange'].set_left()
        wbf['total_orange'].set_right()
        wbf['total_orange'].set_top()
        wbf['total_orange'].set_bottom()

        wbf['total_pink'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['pink'], 'align': 'right', 'font_name': 'Georgia'})
        wbf['total_pink'].set_left()
        wbf['total_pink'].set_right()
        wbf['total_pink'].set_top()
        wbf['total_pink'].set_bottom()

        wbf['total_float_pink'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['pink'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_pink'].set_left()
        wbf['total_float_pink'].set_right()
        wbf['total_float_pink'].set_top()
        wbf['total_float_pink'].set_bottom()

        wbf['total_float_pink2'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['pink'], 'align': 'center', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_pink2'].set_left()
        wbf['total_float_pink2'].set_right()
        wbf['total_float_pink2'].set_top()
        wbf['total_float_pink2'].set_bottom()

        wbf['total_violet'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['violet'], 'align': 'right', 'font_name': 'Georgia'})
        wbf['total_violet'].set_left()
        wbf['total_violet'].set_right()
        wbf['total_violet'].set_top()
        wbf['total_violet'].set_bottom()

        wbf['total_float_violet'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['violet'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_violet'].set_left()
        wbf['total_float_violet'].set_right()
        wbf['total_float_violet'].set_top()
        wbf['total_float_violet'].set_bottom()

        wbf['total_float_violet2'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['violet'], 'align': 'center', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_violet2'].set_left()
        wbf['total_float_violet2'].set_right()
        wbf['total_float_violet2'].set_top()
        wbf['total_float_violet2'].set_bottom()

        wbf['total_smoke'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['smoke'], 'align': 'right', 'font_name': 'Georgia'})
        wbf['total_smoke'].set_left()
        wbf['total_smoke'].set_right()
        wbf['total_smoke'].set_top()
        wbf['total_smoke'].set_bottom()

        wbf['total_float_smoke'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['smoke'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_smoke'].set_left()
        wbf['total_float_smoke'].set_right()
        wbf['total_float_smoke'].set_top()
        wbf['total_float_smoke'].set_bottom()

        wbf['total_float_smoke2'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['smoke'], 'align': 'center', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_smoke2'].set_left()
        wbf['total_float_smoke2'].set_right()
        wbf['total_float_smoke2'].set_top()
        wbf['total_float_smoke2'].set_bottom()

        wbf['header_detail_space'] = workbook.add_format(
            {'font_name': 'Georgia'})
        wbf['header_detail_space'].set_left()
        wbf['header_detail_space'].set_right()
        wbf['header_detail_space'].set_top()
        wbf['header_detail_space'].set_bottom()

        wbf['header_detail'] = workbook.add_format(
            {'bg_color': '#E0FFC2', 'font_name': 'Georgia'})
        wbf['header_detail'].set_left()
        wbf['header_detail'].set_right()
        wbf['header_detail'].set_top()
        wbf['header_detail'].set_bottom()

        return wbf, workbook
