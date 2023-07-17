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

    @api.onchange('start_period')
    def onchange_end_period(self):
        self.end_period = self.start_period

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

        # where_ids = " and 1=1 "
        # if user_id :
        #     where_ids = " and s.user_id = %s"%(user_id)

        datetime_string = self.get_default_date_model().strftime("%Y-%m-%d %H:%M:%S")
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        report_name = 'Summary Sales Report'
        filename = '%s %s' % (report_name, date_string)

        # where_date = " and 1=1 "
        # if self.shift == 'ALL':
        #     where_date += " and DATE_TRUNC('day', s.start_at) >= '%s' and DATE_TRUNC('day', s.stop_at) <= '%s' and s.shift in ('Shift A','Shift B')"%(self.start_period, self.end_period)
        # elif self.shift == 'Shift A':
        #     where_date += " and DATE_TRUNC('day', s.start_at) >= '%s' and DATE_TRUNC('day', s.stop_at) <= '%s' and s.shift in ('Shift A')"%(self.start_period, self.end_period)
        # elif self.shift == 'Shift B':
        #     where_date += " and DATE_TRUNC('day', s.start_at) >= '%s' and DATE_TRUNC('day', s.stop_at) <= '%s' and s.shift in ('Shift B')"%(self.start_period, self.end_period)

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

        query = """
            SELECT          
                s.config_id AS config_id,
                rp.name AS user_name,
                COUNT(o) AS print_receipt,
                COALESCE(SUM(ol.qty_sold),0) AS qty_sold,
                COALESCE(SUM(ol.before_discount),0) AS before_discount,
                COALESCE(SUM(ol.discount),0) AS discount,
                COALESCE(SUM(o.amount_total),0) AS after_discount,
                COALESCE(SUM(p.payment_cash),0) AS payment_cash,
                COALESCE(SUM(p.payment_cc),0) AS payment_cc
            FROM 
                pos_order o
            LEFT JOIN 
                (SELECT ol.order_id, COALESCE(SUM(ol.qty),0) AS qty_sold, COALESCE(SUM(ol.price_unit * ol.qty),0) AS before_discount, COALESCE(SUM(ol.price_unit * ol.qty),0) - COALESCE(SUM(ol.price_subtotal_incl),0) AS discount FROM pos_order_line ol GROUP BY ol.order_id) ol ON ol.order_id=o.id
            LEFT JOIN 
                (SELECT p.pos_order_id AS pos_order_id,
                        CASE 
                            WHEN aj.type IN ('cash') THEN COALESCE(SUM(p.amount),0)
                        END AS payment_cash,
                        CASE 
                            WHEN aj.type IN ('bank') THEN COALESCE(SUM(p.amount),0)
                        END AS payment_cc
                  FROM pos_payment p 
                  LEFT JOIN 
                     pos_payment_method pm ON p.payment_method_id=pm.id
                  LEFT JOIN 
                     account_journal aj ON pm.journal_id=aj.id
                  GROUP BY p.pos_order_id,aj.type) p ON p.pos_order_id=o.id
            LEFT JOIN 
                pos_session s ON o.session_id=s.id
            LEFT JOIN 
                res_users ru ON s.user_id=ru.id
            LEFT JOIN 
                res_partner rp ON ru.partner_id=rp.id
            WHERE 
                o.state NOT IN ('draft','cancel') AND s.config_id=%s %s
            GROUP BY 
                s.config_id, rp.name
        """
        self._cr.execute(query % (config_id, where_date))
        result = self._cr.dictfetchall()
        # result = self._cr.fetchall()

        nat_asian = 0
        nat_ina = 0
        nat_west = 0
        nat_japan = 0
        nat_aus = 0
        total = 0
        query2 = """
            SELECT 
                CASE 
                    WHEN vr.name IN ('Asian') THEN COUNT(*)
                END AS nat_asian,
                CASE 
                    WHEN vr.name IN ('Ina') THEN COUNT(*)
                END AS nat_ina,
                CASE 
                    WHEN vr.name IN ('West','We') THEN COUNT(*)
                END AS nat_west,
                CASE 
                    WHEN vr.name IN ('Japan','Japa') THEN COUNT(*)
                END AS nat_japan,
                CASE 
                    WHEN vr.name IN ('Aus') THEN COUNT(*)
                END AS nat_aus
            FROM pos_order o
            LEFT JOIN pos_session s ON o.session_id=s.id
            LEFT JOIN visitor_region vr ON o.region_id=vr.id
            WHERE o.state NOT IN ('draft','cancel') AND s.config_id=%s %s
            GROUP BY vr.name, o.partner_id
        """
        self._cr.execute(query2 % (config_id, where_date))
        result2 = self._cr.dictfetchall()
        for res2 in result2:
            if res2['nat_asian']:
                nat_asian += res2['nat_asian']
            if res2['nat_ina']:
                nat_ina += res2['nat_ina']
            if res2['nat_west']:
                nat_west += res2['nat_west']
            if res2['nat_japan']:
                nat_japan += res2['nat_japan']
            if res2['nat_aus']:
                nat_aus += res2['nat_aus']
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
        start_datetime = datetime(period.year, period.month, period.day, 0, 0, 0) - timedelta(hours=7)
        end_datetime = datetime(period.year, period.month, period.day, 23, 59, 59) - timedelta(hours=7)
        if self.shift == 'ALL':
            pos_session_ids = self.env['pos.session'].sudo().search(
                [('state', '=', 'closed'), ('start_at', '>=', start_datetime), ('stop_at', '<=', end_datetime),
                 ('config_id', '=', self.config_id.id)])
        else:
            pos_session_ids = self.env['pos.session'].sudo().search(
                [('state', '=', 'closed'), ('start_at', '>=', start_datetime), ('stop_at', '<=', end_datetime),
                 ('config_id', '=', self.config_id.id), ('shift', '=', self.shift)])

        visitor_count = sum(pos_session_ids.mapped('visitor_count'))
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
            worksheet.merge_range('D8:G8', str(d_day) + ' ' + str(d_month) + ' ' + str(d_year) or '', wbf['content'])
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
            worksheet.merge_range('A%s:B%s' % (row1, row1), 'Total Received US$', wbf['content_number'])
            worksheet.merge_range('A%s:B%s' % (row1 + 1, row1 + 1), 'Total Received AUD', wbf['content_number'])
            worksheet.merge_range('A%s:B%s' % (row1 + 2, row1 + 2), 'Total Received JPY', wbf['content_number'])
            worksheet.merge_range('A%s:B%s' % (row1 + 3, row1 + 3), 'Total Received Euro', wbf['content_number'])
            worksheet.set_row(row1, None, None, {'hidden': True})
            worksheet.set_row(row1 + 1, None, None, {'hidden': True})
            worksheet.set_row(row1 + 2, None, None, {'hidden': True})
            worksheet.set_row(row1 + 3, None, None, {'hidden': True})
            worksheet.merge_range('A%s:B%s' % (row1 + 4, row1 + 4), 'Total Received Vouc', wbf['content_number'])
            worksheet.merge_range('A%s:B%s' % (row1 + 5, row1 + 5), 'Total Receipt Print', wbf['content_number'])
            worksheet.merge_range('A%s:B%s' % (row1 + 6, row1 + 6), 'Visitor Statistic:', wbf['content_number'])

            row2 = row
            worksheet.write('C%s: C%s' % (row2, row2), ': ', wbf['content_float'])
            worksheet.write('C%s: C%s' % (row2 + 1, row2 + 1), ': ', wbf['content_float'])
            worksheet.write('C%s: C%s' % (row2 + 2, row2 + 2), ': ', wbf['content_float'])
            worksheet.write('C%s: C%s' % (row2 + 3, row2 + 3), ': ', wbf['content_float'])
            worksheet.write('C%s: C%s' % (row2 + 4, row2 + 4), ': ', wbf['content_float'])
            worksheet.write('C%s: C%s' % (row2 + 5, row2 + 5), ': ', wbf['content_float'])
            worksheet.write('C%s: C%s' % (row2 + 6, row2 + 6), ': ', wbf['content'])

            row3 = row
            worksheet.merge_range('D%s:G%s' % (row3, row3), '-', wbf['content_float'])
            worksheet.merge_range('D%s:G%s' % (row3 + 1, row3 + 1), '-', wbf['content_float'])
            worksheet.merge_range('D%s:G%s' % (row3 + 2, row3 + 2), '-', wbf['content_float'])
            worksheet.merge_range('D%s:G%s' % (row3 + 3, row3 + 3), '-', wbf['content_float'])
            worksheet.merge_range('D%s:G%s' % (row3 + 4, row3 + 4), '-', wbf['content_float'])
            worksheet.merge_range('D%s:G%s' % (row3 + 5, row3 + 5), res['print_receipt'] or '', wbf['content'])
            worksheet.merge_range('D%s:G%s' % (row3 + 6, row3 + 6), visitor_count, wbf['content'])

            row4 = row3 + 6
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

            row7 = row6 + 3 + 1

            worksheet.merge_range('A%s:G%s' % (row7, row7), 'Conversion Ratio:', wbf['content2'])
            # # # worksheet.merge_range('A28:G28', '', wbf['content'])
            # # # worksheet.merge_range('C29:E29', '', wbf['content'])
            # # # worksheet.merge_range('A29:B29', 'Signature,', wbf['title_doc2'])
            # # # worksheet.merge_range('F29:G29', 'Signature,', wbf['title_doc2'])
            # # # worksheet.merge_range('A30:G30', '', wbf['content'])
            # # # worksheet.merge_range('A31:G31', '', wbf['content'])
            # # # worksheet.merge_range('C32:E32', '', wbf['title_doc2'])
            # # # worksheet.merge_range('A32:B32', '(Supervisor)', wbf['title_doc2'])
            # # # worksheet.merge_range('F32:G32', '(Cashier)', wbf['title_doc2'])
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
