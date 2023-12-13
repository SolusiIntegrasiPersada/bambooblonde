import xlsxwriter
import base64
from odoo import fields, models, api
from io import BytesIO
from datetime import datetime, timedelta
from pytz import timezone
import pytz


class SummarySalesReport(models.TransientModel):
    _name = "summary.sales.report"
    _description = "Summary Sales Report .xlsx"

    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone(self.env.user.tz or 'UTC'))

    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)
    start_period = fields.Date('Start Period')
    end_period = fields.Date('End Period')
    config_id = fields.Many2one('pos.config', 'Point of Sale')
    shift = fields.Selection([('ALL', 'ALL'), ('Shift A', 'Shift A'), ('Shift B', 'Shift B')], 'Shift', default='ALL')

    # @api.onchange('start_period')
    # def onchange_end_period(self):
    #     self.end_period = self.start_period

    def print_excel_report(self):
        data = self.read()[0]
        pos_name = self.config_id.name
        address = self.config_id.address
        # shift_id = self.shift_id
        config_id = self.config_id.id
        start_period = data['start_period']
        end_period = data['end_period']

        date = datetime.strptime(str(self.start_period), '%Y-%m-%d')
        d_day = str(date.strftime("%d"))
        d_month = str(date.strftime("%B"))
        d_year = str(date.strftime("%y"))
        
        enddate = datetime.strptime(str(self.end_period), '%Y-%m-%d')
        endd_day = str(enddate.strftime("%d"))
        endd_month = str(enddate.strftime("%B"))
        endd_year = str(enddate.strftime("%y"))

       

        datetime_string = self.get_default_date_model().strftime("%Y-%m-%d %H:%M:%S")
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        report_name = 'Summary Sales Report'
        filename = '%s %s' % (report_name, date_string)

      

        where_date = " and 1=1 "
        if self.shift == 'ALL':
            where_date += " and DATE_TRUNC('day', o.date_order) >= '%s' and DATE_TRUNC('day', o.date_order) <= '%s' and s.shift in ('Shift A','Shift B')" % (
            self.start_period, self.end_period)
        elif self.shift == 'Shift A':
            where_date += " and DATE_TRUNC('day', o.date_order) >= '%s' and DATE_TRUNC('day', o.date_order) <= '%s' and s.shift in ('Shift A')" % (
            self.start_period, self.end_period)
        elif self.shift == 'Shift B':
            where_date += " and DATE_TRUNC('day', o.date_order) >= '%s' and DATE_TRUNC('day', o.date_order) <= '%s' and s.shift in ('Shift B')" % (
            self.start_period, self.end_period)


        
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
        total_qty = 0
        total_receipt = 0
        total_before_diskon = 0
        total_after_diskon = 0
        total_diskon = 0
        total_payment_cash = 0
        total_payment_cc = 0
        total_coupon = 0
        nat_asian = 0
        nat_ina = 0
        nat_west = 0
        nat_japan = 0
        nat_aus = 0
        total = 0
        name = ''
        visitor_count = 0
        for order in orders:
            region = order.region_id
            if region.name in ('Asian') :
                nat_asian += 1
            if region.name in ('Ina','Indonesian') :
                nat_ina += 1
            if region.name in ('West','We','Westerner') :
                nat_west += 1
            if region.name in ('Japan','Japa','Japanese') :
                nat_japan += 1
            if region.name in ('Aus','Australian') :
                nat_aus += 1
                
            
            name = order.session_id.user_id.name
            visitor_count += order.session_id.visitor_count_flt
            lineplus = order.lines.filtered(lambda x: x.price_subtotal_incl > 0)
            qty = sum(lineplus.mapped('qty'))
            # print('order', order,name)
            # print('order', qty)
            pricexqty = sum(plus.price_unit * plus.qty for plus in lineplus)
            total_sales = pricexqty
            price_inc = sum(lineplus.mapped('price_subtotal_incl'))
            discount = pricexqty - price_inc
            total_return = abs(order.amount_total) if order.amount_total < 0 else 0
            cash = order.payment_ids.filtered(
                lambda x: x.payment_method_id.journal_id.type == 'cash')
            bank = order.payment_ids.filtered(
                lambda x: x.payment_method_id.journal_id.type == 'bank' and x.amount > 0)
            payment_cash = sum(cash.mapped('amount'))
            payment_cc = sum(bank.mapped('amount'))
            
            amount_coupon = 0
            coupon = order.lines.filtered(lambda x: x.product_id.is_produk_promotion)
            if coupon :
                amount_coupon = abs(sum(coupon.mapped('price_subtotal_incl')))
            
            discount_member = order.lines.filtered(lambda x: x.product_id.is_produk_diskon)
            if discount_member :
                discount += abs(sum(discount_member.mapped('price_subtotal_incl')))
                
           
                
            total_qty += qty
            total_receipt += 1
            total_before_diskon += total_sales
            total_diskon += discount
            total_payment_cash += payment_cash
            total_payment_cc += payment_cc
            total_coupon += amount_coupon
        
        config_id = config_id
        user_name = name
        print_receipt = total_receipt
        qty_sold = total_qty
        before_discount = total_before_diskon
        discount = total_diskon
        after_discount = before_discount - discount
        payment_cash = total_payment_cash
        payment_cc = total_payment_cc
        coupon = total_coupon
        result.append({'config_id': config_id, 
                       'user_name': user_name, 
                       'print_receipt': print_receipt, 
                       'qty_sold': qty_sold, 
                       'before_discount': before_discount, 
                       'discount': discount, 
                       'after_discount': after_discount, 
                       'payment_cash': payment_cash, 
                       'payment_cc': payment_cc, 
                       'coupon': coupon, 
                       'visitor_count': visitor_count, 
                       })
            
        total = nat_asian + nat_ina + nat_west + nat_japan + nat_aus



        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf, workbook = self.add_workbook_format(workbook)

        shift = str(self.shift)

        worksheet = workbook.add_worksheet(report_name)

        worksheet.set_column('A:A', 8)
        worksheet.set_column('B:B', 8)
        worksheet.set_column('C:C', 2)
        worksheet.set_column('D:D', 8)
        worksheet.set_column('E:E', 8)
        worksheet.set_column('F:F', 8)
        worksheet.set_column('G:G', 8)

        period = self.start_period
        period_end = self.end_period
        start_datetime = datetime(period.year, period.month, period.day, 0, 0, 0) - timedelta(hours=7)
        end_datetime = datetime(period_end.year, period_end.month, period_end.day, 23, 59, 59) - timedelta(hours=7)
        # if self.shift == 'ALL':
        #     pos_session_ids = self.env['pos.session'].sudo().search(
        #         [('state', '=', 'closed'), ('start_at', '>=', start_datetime), ('stop_at', '<=', end_datetime),
        #          ('config_id', '=', self.config_id.id)])
        # else:
        #     pos_session_ids = self.env['pos.session'].sudo().search(
        #         [('state', '=', 'closed'), ('start_at', '>=', start_datetime), ('stop_at', '<=', end_datetime),
        #          ('config_id', '=', self.config_id.id), ('shift', '=', self.shift)])

        # visitor_count = sum(pos_session_ids.mapped('visitor_count'))
        for res in result:

            worksheet.merge_range('A1:G1', str(pos_name), wbf['title_doc'])
            worksheet.merge_range('A2:G2', str(address), wbf['title_doc3'])
            worksheet.merge_range('A3:G3', '', wbf['title_doc3'])
            worksheet.merge_range('A4:G4', 'CLOSING SHIFT', wbf['title_doc3'])

            worksheet.merge_range('A5:B5', '', wbf['content'])
            worksheet.merge_range('A6:B6', 'Cashier No', wbf['content'])
            worksheet.merge_range('A7:B7', 'Cashier Name', wbf['content'])
            worksheet.merge_range('A8:B8', 'Date', wbf['content'])
            worksheet.merge_range('A9:B9', 'Shift', wbf['content'])
            worksheet.merge_range('A10:B10', 'Total Qty Sold', wbf['content_number'])
            worksheet.merge_range('A11:B11', 'Gross Sales Bef/Disc', wbf['content_number'])
            worksheet.merge_range('A12:B12', 'Discount', wbf['content_number'])
            worksheet.merge_range('A13:B13', 'Gross Sales Aft/Disc', wbf['content_number'])
            worksheet.merge_range('A14:B14', 'Total Received Cash', wbf['content_number'])
            worksheet.merge_range('A15:B15', 'Total Received Card', wbf['content_number'])

            worksheet.write('C5:C5', '', wbf['content'])
            worksheet.write('C6:C6', ': ', wbf['content'])
            worksheet.write('C7:C7', ': ', wbf['content'])
            worksheet.write('C8:C8', ': ', wbf['content'])
            worksheet.write('C9:C9', ': ', wbf['content'])
            worksheet.write('C10:C10', ': ', wbf['content_number'])
            worksheet.write('C11:C11', ': ', wbf['content_float'])
            worksheet.write('C12:C12', ': ', wbf['content_float'])
            worksheet.write('C13:C13', ': ', wbf['content_float'])
            worksheet.write('C14:C14', ': ', wbf['content_float'])

            worksheet.merge_range('D5:G5', '', wbf['content'])
            worksheet.merge_range('D6:G6', '-', wbf['content'])
            worksheet.merge_range('D7:G7', pos_name or '', wbf['content'])
            worksheet.merge_range('D8:G8', str(d_day) + ' ' + str(d_month) + ' ' + str(d_year) + ' - ' + str(endd_day) + ' ' + str(endd_month) + ' ' + str(endd_year), wbf['content'])
            worksheet.merge_range('D9:G9', shift or '', wbf['content'])
            worksheet.merge_range('D10:G10', res['qty_sold'] or '', wbf['content_number'])
            worksheet.merge_range('D11:G11', res['before_discount'] or '', wbf['content_float'])
            worksheet.merge_range('D12:G12', res['discount'] or '', wbf['content_float'])
            worksheet.merge_range('D13:G13', res['after_discount'] or '', wbf['content_float'])
            worksheet.merge_range('D14:G14', res['payment_cash'] or '', wbf['content_float'])
            worksheet.merge_range('D15:G15', res['payment_cc'] or '', wbf['content_float'])

            query3 = """
                SELECT pm.name AS payment_method, COALESCE(SUM(p.amount),0) AS amount
                FROM pos_order o
                LEFT JOIN pos_session s ON o.session_id=s.id
                LEFT JOIN pos_payment p ON p.pos_order_id=o.id
                LEFT JOIN pos_payment_method pm ON p.payment_method_id=pm.id
                LEFT JOIN account_journal aj ON pm.journal_id=aj.id
                WHERE aj.type IN ('bank') AND o.state NOT IN ('draft','cancel') AND s.config_id=%s %s
                GROUP BY pm.name
            """
            self._cr.execute(query3 % (config_id, where_date))
            result3 = self._cr.dictfetchall()
            row = 16
            for res3 in result3:
                worksheet.write('A%s:A%s' % (row, row), '>>>', wbf['content_pm'])
                worksheet.merge_range('B%s:C%s' % (row, row), res3['payment_method'] or '', wbf['content_pm_bold'])
                worksheet.merge_range('D%s:G%s' % (row, row), res3['amount'] or '', wbf['content_float_bold'])
                row += 1

            row1 = row
            worksheet.merge_range('A%s:B%s' % (row1, row1), 'Total Received Voucher', wbf['content_number'])
            worksheet.merge_range('A%s:B%s' % (row1 + 1, row1 + 1), 'Total Receipt Print', wbf['content_number'])
            worksheet.merge_range('A%s:B%s' % (row1 + 2, row1 + 2), 'Visitor Statistic:', wbf['content_number'])

            row2 = row
            worksheet.write('C%s: C%s' % (row2, row2), ': ', wbf['content_float'])
            worksheet.write('C%s: C%s' % (row2 + 1, row2 + 1), ': ', wbf['content_float'])
            worksheet.write('C%s: C%s' % (row2 + 2, row2 + 2), ': ', wbf['content'])

            row3 = row
            worksheet.merge_range('D%s:G%s' % (row3, row3), res['coupon'], wbf['content_float'])
            worksheet.merge_range('D%s:G%s' % (row3 + 1, row3 + 1), res['print_receipt'] or '', wbf['content'])
            worksheet.merge_range('D%s:G%s' % (row3 + 2, row3 + 2), res['visitor_count'], wbf['content'])

            row4 = row3 + 3
            worksheet.write(row4, 0, 'Asian', wbf['content2'])
            worksheet.write(row4, 1, 'Ina', wbf['content2'])
            worksheet.write(row4, 2, '', wbf['content2'])
            worksheet.write(row4, 3, 'West', wbf['content2'])
            worksheet.write(row4, 4, 'Japan', wbf['content2'])
            worksheet.write(row4, 5, 'Aus', wbf['content2'])
            worksheet.write(row4, 6, 'Total Buy', wbf['content2'])

            row5 = row4 + 1
            worksheet.write(row5, 0, nat_asian or '', wbf['content2'])
            worksheet.write(row5, 1, nat_ina or '', wbf['content2'])
            worksheet.write(row5, 2, '', wbf['content2'])
            worksheet.write(row5, 3, nat_west or '', wbf['content2'])
            worksheet.write(row5, 4, nat_japan or '', wbf['content2'])
            worksheet.write(row5, 5, nat_aus or '', wbf['content2'])
            worksheet.write(row5, 6, total or '', wbf['content2'])

            row6 = row5 + 1

            worksheet.merge_range('A%s:G%s' % (row6 + 1, row6 + 1), '', wbf['content'])
            worksheet.merge_range('A%s:G%s' % (row6 + 2, row6 + 2), '', wbf['content'])
            worksheet.merge_range('A%s:G%s' % (row6 + 3, row6 + 3), '', wbf['content'])

            row7 = row6 + 1

            worksheet.merge_range('A%s:G%s' % (row7, row7), 'Conversion Ratio:', wbf['content2'])
          
            row8 = row7 + 1
            worksheet.merge_range('A%s:G%s' % (row8, row8), '', wbf['content'])

        workbook.close()
        out = base64.encodestring(fp.getvalue())
        self.write({'datas': out, 'datas_fname': filename})
        fp.close()
        filename += '%2Exlsx'

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model=' + self._name + '&id=' + str(
                self.id) + '&field=datas&download=true&filename=' + filename,
        }

    def add_workbook_format(self, workbook):
        colors = {
            'white_orange': '#FFFFDB',
            'orange': '#FFC300',
            'red': '#FF0000',
            'yellow': '#F6FA03',
            'pink': '#FF69B4',
            'violet': '#EE82EE',
        }

        wbf = {}

        wbf['footer'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['footer'].set_border()

        wbf['header'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': '#FFFFDB', 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header'].set_border()

        wbf['header_pink'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['pink'], 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_pink'].set_border()

        wbf['header_violet'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['violet'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_violet'].set_border()

        wbf['header_orange'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['orange'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_orange'].set_border()

        wbf['header_yellow'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['yellow'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_yellow'].set_border()

        wbf['header_no'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': '#FFFFDB', 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_no'].set_border()
        wbf['header_no'].set_align('vcenter')

        wbf['footer'] = workbook.add_format({'align': 'left', 'font_name': 'Georgia'})

        wbf['content_datetime'] = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss', 'font_name': 'Georgia'})
        wbf['content_datetime'].set_left()
        wbf['content_datetime'].set_right()

        wbf['content_date'] = workbook.add_format({'num_format': 'yyyy-mm-dd', 'font_name': 'Georgia'})
        wbf['content_date'].set_left()
        wbf['content_date'].set_right()

        wbf['title_doc'] = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 20,
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc2'] = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 14,
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc3'] = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })
        # wbf['title_doc3'].set_top()
        # wbf['title_doc3'].set_bottom()            
        # wbf['title_doc3'].set_left()
        # wbf['title_doc3'].set_right()  

        wbf['company'] = workbook.add_format({'align': 'left', 'font_name': 'Georgia'})
        wbf['company'].set_font_size(11)

        wbf['content'] = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })
        # wbf['content'].set_left()
        # wbf['content'].set_right()

        wbf['content_pm'] = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })

        wbf['content_pm_bold'] = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
            'bold': True,
        })

        wbf['content2'] = workbook.add_format({'align': 'center', 'font_name': 'Georgia', 'bg_color': '#FFFFFF', })
        # wbf['content2'].set_left()
        # wbf['content2'].set_right() 

        wbf['content_float_bold'] = workbook.add_format(
            {'align': 'left', 'num_format': '#,##0', 'font_name': 'Georgia', 'bg_color': '#FFFFFF', 'bold': True})
        wbf['content_float'] = workbook.add_format(
            {'align': 'left', 'num_format': '#,##0', 'font_name': 'Georgia', 'bg_color': '#FFFFFF', })
        # wbf['content_float'].set_right() 
        # wbf['content_float'].set_left()

        wbf['content_number'] = workbook.add_format(
            {'align': 'left', 'num_format': '#,##0', 'font_name': 'Georgia', 'bg_color': '#FFFFFF', })
        # wbf['content_number'].set_right() 
        # wbf['content_number'].set_left() 

        wbf['content_percent'] = workbook.add_format({'align': 'right', 'num_format': '0.00%', 'font_name': 'Georgia'})
        wbf['content_percent'].set_right()
        wbf['content_percent'].set_left()

        wbf['total_float'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['white_orange'], 'align': 'right', 'num_format': '#,##0',
             'font_name': 'Georgia'})
        wbf['total_float'].set_top()
        wbf['total_float'].set_bottom()
        wbf['total_float'].set_left()
        wbf['total_float'].set_right()

        wbf['total_number'] = workbook.add_format(
            {'align': 'right', 'bg_color': colors['white_orange'], 'bold': 1, 'num_format': '#,##0',
             'font_name': 'Georgia'})
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

        wbf['header_detail_space'] = workbook.add_format({'font_name': 'Georgia'})
        wbf['header_detail_space'].set_left()
        wbf['header_detail_space'].set_right()
        wbf['header_detail_space'].set_top()
        wbf['header_detail_space'].set_bottom()

        wbf['header_detail'] = workbook.add_format({'bg_color': '#E0FFC2', 'font_name': 'Georgia'})
        wbf['header_detail'].set_left()
        wbf['header_detail'].set_right()
        wbf['header_detail'].set_top()
        wbf['header_detail'].set_bottom()

        return wbf, workbook
