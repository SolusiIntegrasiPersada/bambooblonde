import xlsxwriter
import base64
from odoo import fields, models, api
from io import BytesIO
from datetime import date, datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
from pytz import timezone
import pytz
import io
import itertools
from itertools import groupby

class RlkPlainPrintReport(models.TransientModel):
    _name = "rlk.plain.print.report"
    _description = "Plain & Print Report .xlsx"

    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone(self.env.user.tz or 'UTC'))

    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)
    start_period = fields.Date('Start Period')
    end_period = fields.Date('End Period')

    def print_excel_report(self):
        start_ds = datetime.strptime(str(self.start_period), '%Y-%m-%d')
        end_ds = datetime.strptime(str(self.end_period), '%Y-%m-%d')
        year = start_ds.strftime('%Y')
        start_day = start_ds.strftime('%d')
        start_month = start_ds.strftime('%B')
        end_day = end_ds.strftime('%d')
        end_month = end_ds.strftime('%B')
        
        datetime_string = self.get_default_date_model().strftime("%Y-%m-%d %H:%M:%S")
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        report_name = 'Plain Print Report'
        filename = '%s %s'%(report_name,date_string)
      
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf, workbook = self.add_workbook_format(workbook)

        worksheet = workbook.add_worksheet(report_name)

        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('G:G', 20)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:J', 20)
        worksheet.set_column('K:K', 20)
        worksheet.set_column('L:L', 5)
        worksheet.set_column('M:M', 20)
        worksheet.set_column('N:N', 20)
        worksheet.set_column('O:O', 20)
        worksheet.set_column('P:P', 20)
        worksheet.set_column('Q:Q', 20)
        worksheet.set_column('R:R', 20)
        worksheet.set_column('S:S', 5)
        worksheet.set_column('T:T', 20)
        worksheet.set_column('U:U', 20)
        worksheet.set_column('V:V', 20)
        worksheet.set_column('W:W', 20)
        worksheet.set_column('X:X', 20)
        worksheet.set_column('Y:Y', 20)
        # worksheet.set_column('Z:Z', 20)

        worksheet.merge_range('A1:D1', 'PERIOD OF SALES : ' + str(start_month) + ' ' + str(start_day) + 'th - ' + str(end_month) + ' ' + str(end_day) + 'th, ' +  str(year) , wbf['title_doc_brown'])
        worksheet.merge_range('A2:D2', 'LAST STOCK : ' + str(end_month) + ' ' + str(end_day) + 'th, ' +  str(year), wbf['title_doc_pink'])

        worksheet.write('A5:B5', 'Category', wbf['header_blue'])

        worksheet.merge_range('B4:F4', 'PLAIN', wbf['header_light_green'])
        worksheet.merge_range('G4:K4', 'PRINT', wbf['header_white_orange'])

        worksheet.write('B5:C5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('C5:D5', '%', wbf['header_blue'])
        worksheet.write('D5:E5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('E5:F5', '%', wbf['header_blue'])
        worksheet.write('F5:G5', '% SELL THRU', wbf['header_pink'])
        worksheet.write('G5:H5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('H5:I5', '%', wbf['header_blue'])
        worksheet.write('I5:J5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('J5:K5', '%', wbf['header_blue'])
        worksheet.write('K5:L5', '% SELL THRU', wbf['header_pink'])

        worksheet.merge_range('N4:R4', 'PLAIN', wbf['header_light_green'])

        worksheet.write('M5:N5', 'Color', wbf['header_blue'])
        worksheet.write('N5:O5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('O5:P5', '%', wbf['header_blue'])
        worksheet.write('P5:Q5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('Q5:R5', '%', wbf['header_blue'])
        worksheet.write('R5:S5', '% SELL THRU', wbf['header_pink'])

        worksheet.merge_range('U4:Y4', 'PRINT', wbf['header_white_orange'])

        worksheet.write('T5:U5', 'Color', wbf['header_blue'])
        worksheet.write('U5:V5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('V5:W5', '%', wbf['header_blue'])
        worksheet.write('W5:X5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('X5:Y5', '%', wbf['header_blue'])
        worksheet.write('Y5:Z5', '% SELL THRU', wbf['header_pink'])

        pos_order_lines = self.env['pos.order.line'].search([
            ('order_id.date_order', '>=', self.start_period),
            ('order_id.date_order', '<=', self.end_period),
            ('order_id.state', 'not in', ['draft','cancel']),
            ('product_id.categ_id.parent_id.parent_id.name', 'ilike', 'WOMEN CLOTHES')
        ])


        groups = groupby(pos_order_lines, key=lambda x: (x.product_id.categ_id.parent_id.name, x.product_id.is_print))
        data = {}
        for (category, is_print), lines in groups:
            if is_print:
                data_type = 'qty_print'
            else:
                data_type = 'qty_plain'

            if category not in data:
                data[category] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                    'qty_plain_sold': 0.0,
                    'qty_plain_stock': 0.0,
                }

            qty_sold = sum(line.qty for line in lines)
            data[category][f'{data_type}_sold'] += qty_sold

        quants = self.env['stock.quant'].search([
            ('product_id.categ_id.parent_id.parent_id.name', 'ilike', 'WOMEN CLOTHES'),
            ('location_id.usage', '=', 'internal'),
            # ('quantity', '>', 0),
            ('create_date', '>=', self.start_period),
            ('create_date', '<', self.end_period),
        ])

        for quant in quants:
            category = quant.product_id.categ_id.parent_id.name
            is_print = quant.product_id.is_print
            if is_print:
                data_type = 'qty_print'
            else:
                data_type = 'qty_plain'
            if category not in data:
                data[category] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                    'qty_plain_sold': 0.0,
                    'qty_plain_stock': 0.0,
                }
            # data[category][f'{data_type}_stock'] += quant.quantity
            data[category]['{}_stock'.format(data_type)] += quant.quantity

        # print(data)

        # Menambahkan summary
        total_qty_print_stock = sum(values['qty_print_stock'] for values in data.values())
        total_qty_print_sold = sum(values['qty_print_sold'] for values in data.values())
        total_qty_plain_stock = sum(values['qty_plain_stock'] for values in data.values())
        total_qty_plain_sold = sum(values['qty_plain_sold'] for values in data.values())
        total_percent_plain_sold = 0
        total_percent_plain_stock = 0
        total_percent_print_sold = 0
        total_percent_print_stock = 0
        total_sell_thru_plain = 0
        total_sell_thru_print = 0

        row = 6
        for category, values in data.items():
            percent_plain_sold = 0
            percent_plain_stock = 0
            percent_print_sold = 0
            percent_print_stock = 0
            sell_thru_plain = 0
            sell_thru_print = 0

            if total_qty_plain_sold != 0:
                percent_plain_sold = round(values['qty_plain_sold'] / total_qty_plain_sold, 2) or 0
            if total_qty_plain_stock != 0:
                percent_plain_stock = round(values['qty_plain_stock'] / total_qty_plain_stock, 2) or 0
            if total_qty_print_sold != 0:
                percent_print_sold = round(values['qty_print_sold'] / total_qty_print_sold, 2) or 0
            if total_qty_print_stock != 0:
                percent_print_stock = round(values['qty_print_stock'] / total_qty_print_stock, 2) or 0

            plain_sold_stock = values['qty_plain_sold'] + values['qty_plain_stock']
            print_sold_stock = values['qty_print_sold'] + values['qty_print_stock']
            if plain_sold_stock != 0:
                sell_thru_plain = values['qty_plain_sold']/plain_sold_stock
            if print_sold_stock != 0:
                sell_thru_print = values['qty_print_sold']/print_sold_stock

            sell_thru_plain = round(sell_thru_plain, 2) or 0
            sell_thru_print = round(sell_thru_print, 2) or 0

            worksheet.write('A%s:B%s' %(row, row), category or '', wbf['content'])
            worksheet.write('B%s:C%s' %(row, row), values['qty_plain_sold'] or '', wbf['content_float'])
            worksheet.write('C%s:D%s' %(row, row), str(percent_plain_sold) + '%' or '', wbf['content_float'])
            worksheet.write('D%s:E%s' %(row, row), values['qty_plain_stock'] or '', wbf['content_float'])
            worksheet.write('E%s:F%s' %(row, row), str(percent_plain_stock) + '%' or '', wbf['content_float'])
            worksheet.write('F%s:G%s' %(row, row), str(sell_thru_plain) + '%' or '', wbf['content_float'])
            worksheet.write('G%s:H%s' %(row, row), values['qty_print_sold'] or '', wbf['content_float'])
            worksheet.write('H%s:I%s' %(row, row), str(percent_print_sold) + '%' or '', wbf['content_float'])
            worksheet.write('I%s:J%s' %(row, row), values['qty_print_stock'] or '', wbf['content_float'])
            worksheet.write('J%s:K%s' %(row, row), str(percent_print_stock) + '%' or '', wbf['content_float'])
            worksheet.write('K%s:L%s' %(row, row), str(sell_thru_print) + '%' or '', wbf['content_float'])
            row +=1

            total_percent_plain_sold += percent_plain_sold
            total_percent_plain_stock += percent_plain_stock
            total_percent_print_sold += percent_print_sold
            total_percent_print_stock += percent_print_stock
            total_sell_thru_plain += sell_thru_plain
            total_sell_thru_print += sell_thru_print

        total_percent_plain_sold = round(total_percent_plain_sold, 2) or 0
        total_percent_plain_stock = round(total_percent_plain_stock, 2) or 0
        total_percent_print_sold = round(total_percent_print_sold, 2) or 0
        total_percent_print_stock = round(total_percent_print_stock, 2) or 0
        total_sell_thru_plain = round(total_sell_thru_plain, 2) or 0
        total_sell_thru_print = round(total_sell_thru_print, 2) or 0

        worksheet.write('A%s:B%s' %(row, row), 'Grand Total', wbf['total_content'])
        worksheet.write('B%s:C%s' %(row, row), total_qty_plain_sold or '', wbf['total_content_float'])
        worksheet.write('C%s:D%s' %(row, row), str(total_percent_plain_sold) + '%' or '', wbf['total_content_float'])
        worksheet.write('D%s:E%s' %(row, row), total_qty_plain_stock or '', wbf['total_content_float'])
        worksheet.write('E%s:F%s' %(row, row), str(total_percent_plain_stock) + '%' or '', wbf['total_content_float'])
        worksheet.write('F%s:G%s' %(row, row), str(total_sell_thru_plain) + '%' or '', wbf['total_content_float'])
        worksheet.write('G%s:H%s' %(row, row), total_qty_print_sold or '', wbf['total_content_float'])
        worksheet.write('H%s:I%s' %(row, row), str(total_percent_print_sold) + '%' or '', wbf['total_content_float'])
        worksheet.write('I%s:J%s' %(row, row), total_qty_print_stock or '', wbf['total_content_float'])
        worksheet.write('J%s:K%s' %(row, row), str(total_percent_print_stock) + '%' or '', wbf['total_content_float'])
        worksheet.write('K%s:L%s' %(row, row), str(total_sell_thru_print) + '%' or '', wbf['total_content_float'])

        groups = groupby(pos_order_lines, key=lambda x: (x.product_id.categ_id.parent_id.id, x.product_id.is_print, x.color))

        data_print = {}
        data_plain = {}
        for (category, is_print, color), lines in groups:
            if is_print:
                data = data_print
                data_type = 'qty_print'
            else:
                data = data_plain
                data_type = 'qty_plain'
                
            if color not in data:
                data[color] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                    'qty_plain_sold': 0.0,
                    'qty_plain_stock': 0.0,
                }
            
            qty_sold = sum(line.qty for line in lines)
            data[color][f'{data_type}_sold'] += qty_sold

        quants = self.env['stock.quant'].search([
            ('product_id.categ_id.parent_id.parent_id.name', 'ilike', 'WOMEN CLOTHES'),
            ('location_id.usage', '=', 'internal'),
            # ('quantity', '>', 0),
            ('create_date', '>=', self.start_period),
            ('create_date', '<', self.end_period),
        ])

        for quant in quants:
            color = quant.colour
            is_print = quant.product_id.is_print
            if is_print:
                data = data_print
                data_type = 'qty_print'
            else:
                data = data_plain
                data_type = 'qty_plain'
                
            if color not in data:
                data[color] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                    'qty_plain_sold': 0.0,
                    'qty_plain_stock': 0.0,
                }
            # data[color][f'{data_type}_stock'] += quant.quantity
            data[color]['{}_stock'.format(data_type)] += quant.quantity


        c_total_qty_plain_stock = sum(values['qty_plain_stock'] for values in data_plain.values())
        c_total_qty_plain_sold = sum(values['qty_plain_sold'] for values in data_plain.values())
        c_total_percent_plain_sold = 0
        c_total_percent_plain_stock = 0
        c_total_sell_thru_plain = 0

        row1=6
        for color, values in data_plain.items():
            c_percent_plain_sold = 0
            c_percent_plain_stock = 0
            c_sell_thru_plain = 0

            if c_total_qty_plain_sold != 0:
                c_percent_plain_sold = round(values['qty_plain_sold'] / c_total_qty_plain_sold, 2) or 0
            if c_total_qty_plain_stock != 0:
                c_percent_plain_stock = round(values['qty_plain_stock'] / c_total_qty_plain_stock, 2) or 0

            c_plain_sold_stock = values['qty_plain_sold'] + values['qty_plain_stock']
            if c_plain_sold_stock != 0:
                c_sell_thru_plain = values['qty_plain_sold']/c_plain_sold_stock
            c_sell_thru_plain = round(c_sell_thru_plain, 2) or 0

            worksheet.write('M%s:N%s' %(row1, row1), color or '', wbf['content'])
            worksheet.write('N%s:O%s' %(row1, row1), values['qty_plain_sold'] or '', wbf['content_float'])
            worksheet.write('O%s:P%s' %(row1, row1), str(c_percent_plain_sold) + '%' or '', wbf['content_float'])
            worksheet.write('P%s:Q%s' %(row1, row1), values['qty_plain_stock'] or '', wbf['content_float'])
            worksheet.write('Q%s:R%s' %(row1, row1), str(c_percent_plain_stock) + '%' or '', wbf['content_float'])
            worksheet.write('R%s:S%s' %(row1, row1), str(c_sell_thru_plain) + '%' or '', wbf['content_float'])
            row1 +=1

            c_total_percent_plain_sold += c_percent_plain_sold
            c_total_percent_plain_stock += c_percent_plain_stock
            c_total_sell_thru_plain += c_sell_thru_plain

        c_total_percent_plain_sold = round(c_total_percent_plain_sold, 2) or 0
        c_total_percent_plain_stock = round(c_total_percent_plain_stock, 2) or 0
        c_total_sell_thru_plain = round(c_total_sell_thru_plain, 2) or 0

        worksheet.write('M%s:N%s' %(row1, row1), 'Total', wbf['total_content'])
        worksheet.write('N%s:O%s' %(row1, row1), c_total_qty_plain_sold or '', wbf['total_content_float'])
        worksheet.write('O%s:P%s' %(row1, row1), str(c_total_percent_plain_sold) + '%' or '', wbf['total_content_float'])
        worksheet.write('P%s:Q%s' %(row1, row1), c_total_qty_plain_stock or '', wbf['total_content_float'])
        worksheet.write('Q%s:R%s' %(row1, row1), str(c_total_percent_plain_stock) + '%' or '', wbf['total_content_float'])
        worksheet.write('R%s:S%s' %(row1, row1), str(c_total_sell_thru_plain) + '%' or '', wbf['total_content_float'])

        c_total_qty_print_stock = sum(values['qty_print_stock'] for values in data_print.values())
        c_total_qty_print_sold = sum(values['qty_print_sold'] for values in data_print.values())
        c_total_percent_print_sold = 0
        c_total_percent_print_stock = 0
        c_total_sell_thru_print = 0

        row2 = 6
        for color, values in data_print.items():
            c_percent_print_sold = 0
            c_percent_print_stock = 0
            c_sell_thru_print = 0

            if c_total_qty_print_sold != 0:
                c_percent_print_sold = round(values['qty_print_sold'] / c_total_qty_print_sold, 2) or 0
            if c_total_qty_print_stock != 0:
                c_percent_print_stock = round(values['qty_print_stock'] / c_total_qty_print_stock, 2) or 0

            c_print_sold_stock = values['qty_print_sold'] + values['qty_print_stock']
            if c_print_sold_stock != 0:
                c_sell_thru_print = values['qty_print_sold']/c_print_sold_stock
            c_sell_thru_print = round(c_sell_thru_print, 2) or 0

            worksheet.write('T%s:U%s' %(row2, row2), color or '', wbf['content'])
            worksheet.write('U%s:V%s' %(row2, row2), values['qty_print_sold'] or '', wbf['content_float'])
            worksheet.write('V%s:W%s' %(row2, row2), str(c_percent_print_sold) + '%' or '', wbf['content_float'])
            worksheet.write('W%s:X%s' %(row2, row2), values['qty_print_stock'] or '', wbf['content_float'])
            worksheet.write('X%s:Y%s' %(row2, row2), str(c_percent_print_stock) + '%' or '', wbf['content_float'])
            worksheet.write('Y%s:Z%s' %(row2, row2), str(c_sell_thru_print) + '%' or '', wbf['content_float'])
            row2 +=1

            c_total_percent_print_sold += c_percent_print_sold
            c_total_percent_print_stock += c_percent_print_stock
            c_total_sell_thru_print += c_sell_thru_print

        c_total_percent_print_sold = round(c_total_percent_print_sold, 2) or 0
        c_total_percent_print_stock = round(c_total_percent_print_stock, 2) or 0
        c_total_sell_thru_print = round(c_total_sell_thru_print, 2) or 0

        worksheet.write('T%s:U%s' %(row2, row2), 'Total', wbf['total_content'])
        worksheet.write('U%s:V%s' %(row2, row2), c_total_qty_print_sold or '', wbf['total_content_float'])
        worksheet.write('V%s:W%s' %(row2, row2), str(c_total_percent_print_sold) + '%' or '', wbf['total_content_float'])
        worksheet.write('W%s:X%s' %(row2, row2), c_total_qty_print_stock or '', wbf['total_content_float'])
        worksheet.write('X%s:Y%s' %(row2, row2), str(c_total_percent_print_stock) + '%' or '', wbf['total_content_float'])
        worksheet.write('Y%s:Z%s' %(row2, row2), str(c_total_sell_thru_print) + '%' or '', wbf['total_content_float'])

        workbook.close()
        out=base64.encodestring(fp.getvalue())
        self.write({'datas':out, 'datas_fname':filename})
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
            'pink': '#FFC0CB',
            'violet': '#EE82EE',
            'green': '#00FF7F',
            'light_green': '#90EE90',
            'dark_green': '#8FBC8F',
            'blue': '#B0E0E6',
            'brown': '#FFEFD5',
            'salmon': '#FFA07A',
            'beige': '#F5F5DC',
        }

        wbf = {}
        wbf['header'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': '#FFFFFF','font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header'].set_border()

        wbf['header_brown'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['brown'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_brown'].set_border()

        wbf['header_salmon'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['salmon'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_salmon'].set_border()

        wbf['header_beige'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['beige'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_beige'].set_border()

        wbf['header_blue'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['blue'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_blue'].set_border()

        wbf['header_blue2'] = workbook.add_format({'bold': 1,'align': 'left','bg_color': colors['blue'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_blue2'].set_border()

        wbf['header_green'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['green'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_green'].set_border()

        wbf['header_light_green'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['light_green'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_light_green'].set_border()

        wbf['header_dark_green'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['dark_green'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_dark_green'].set_border()

        wbf['header_pink'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['pink'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_pink'].set_border()

        wbf['header_violet'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['violet'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_violet'].set_border()

        wbf['header_orange'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['orange'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_orange'].set_border()

        wbf['header_white_orange'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['white_orange'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_white_orange'].set_border()

        wbf['header_yellow'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['yellow'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_yellow'].set_border()
        
        wbf['header_no'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': '#FFFFDB','font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_no'].set_border()
        wbf['header_no'].set_align('vcenter')
                
        wbf['footer'] = workbook.add_format({'align':'left', 'font_name': 'Georgia'})
        
        wbf['content_datetime'] = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss', 'font_name': 'Georgia'})
        wbf['content_datetime'].set_left()
        wbf['content_datetime'].set_right()
        
        wbf['content_date'] = workbook.add_format({'num_format': 'yyyy-mm-dd', 'font_name': 'Georgia'})
        wbf['content_date'].set_left()
        wbf['content_date'].set_right() 

        wbf['title_doc_pink'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 16,
            'font_name': 'Georgia',
            'bg_color': '#FFC0CB',
        })

        wbf['title_doc_brown'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 14,
            'font_name': 'Georgia',
            'bg_color': '#FFEFD5',
        })
        
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
        
        wbf['company'] = workbook.add_format({'align': 'left', 'font_name': 'Georgia'})
        wbf['company'].set_font_size(11)
        
        wbf['content'] = workbook.add_format()
        wbf['content'].set_left()
        wbf['content'].set_right() 

        wbf['content2'] = workbook.add_format({'align': 'center', 'font_name': 'Georgia'})
        wbf['content2'].set_left()
        wbf['content2'].set_right()

        wbf['total_content'] = workbook.add_format({'font_size': 9, 'bold': 1,'align': 'left','bg_color': colors['blue'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['total_content'].set_border() 

        wbf['total_content_float'] = workbook.add_format({'font_size': 9,'bold': True, 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia','bg_color': colors['blue'], 'font_color': '#000000'})
        wbf['total_content_float'].set_border() 

        wbf['total_content_float_price'] = workbook.add_format({'font_size': 9,'bold': True, 'align': 'right','num_format': '#,##0.00', 'font_name': 'Georgia','bg_color': colors['blue'], 'font_color': '#000000'})
        wbf['total_content_float_price'].set_border() 
        
        wbf['content_float'] = workbook.add_format({'font_size': 9, 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_float'].set_right() 
        wbf['content_float'].set_left()

        wbf['content_float_price'] = workbook.add_format({'font_size': 9, 'align': 'right','num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['content_float_price'].set_right() 
        wbf['content_float_price'].set_left()

        wbf['content_number'] = workbook.add_format({'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_number'].set_right() 
        wbf['content_number'].set_left() 
        
        wbf['content_percent'] = workbook.add_format({'align': 'right','num_format': '0.00%', 'font_name': 'Georgia'})
        wbf['content_percent'].set_right() 
        wbf['content_percent'].set_left() 
                
        wbf['total_float'] = workbook.add_format({'bold':1, 'bg_color':colors['white_orange'], 'align':'right', 'num_format':'#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float'].set_top()
        wbf['total_float'].set_bottom()            
        wbf['total_float'].set_left()
        wbf['total_float'].set_right()         
        
        wbf['total_number'] = workbook.add_format({'align':'right','bg_color': colors['white_orange'],'bold':1, 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_number'].set_top()
        wbf['total_number'].set_bottom()            
        wbf['total_number'].set_left()
        wbf['total_number'].set_right()
        
        wbf['total'] = workbook.add_format({'bold':1, 'bg_color':colors['white_orange'], 'align':'center', 'font_name': 'Georgia'})
        wbf['total'].set_left()
        wbf['total'].set_right()
        wbf['total'].set_top()
        wbf['total'].set_bottom()

        wbf['total_float_yellow'] = workbook.add_format({'bold':1, 'bg_color':colors['yellow'], 'align':'right', 'num_format':'#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_yellow'].set_top()
        wbf['total_float_yellow'].set_bottom()
        wbf['total_float_yellow'].set_left()
        wbf['total_float_yellow'].set_right()
        
        wbf['total_number_yellow'] = workbook.add_format({'align':'right','bg_color': colors['yellow'],'bold':1, 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_number_yellow'].set_top()
        wbf['total_number_yellow'].set_bottom()
        wbf['total_number_yellow'].set_left()
        wbf['total_number_yellow'].set_right()
        
        wbf['total_yellow'] = workbook.add_format({'bold':1, 'bg_color':colors['yellow'], 'align':'center', 'font_name': 'Georgia'})
        wbf['total_yellow'].set_left()
        wbf['total_yellow'].set_right()
        wbf['total_yellow'].set_top()
        wbf['total_yellow'].set_bottom()

        wbf['total_float_orange'] = workbook.add_format({'bold':1, 'bg_color':colors['orange'], 'align':'right', 'num_format':'#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_orange'].set_top()
        wbf['total_float_orange'].set_bottom()            
        wbf['total_float_orange'].set_left()
        wbf['total_float_orange'].set_right()         
        
        wbf['total_number_orange'] = workbook.add_format({'align':'right','bg_color': colors['orange'],'bold':1, 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_number_orange'].set_top()
        wbf['total_number_orange'].set_bottom()            
        wbf['total_number_orange'].set_left()
        wbf['total_number_orange'].set_right()
        
        wbf['total_orange'] = workbook.add_format({'bold':1, 'bg_color':colors['orange'], 'align':'center', 'font_name': 'Georgia'})
        wbf['total_orange'].set_left()
        wbf['total_orange'].set_right()
        wbf['total_orange'].set_top()
        wbf['total_orange'].set_bottom()

        wbf['total_pink'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align':'right', 'font_name': 'Georgia'})
        wbf['total_pink'].set_left()
        wbf['total_pink'].set_right()
        wbf['total_pink'].set_top()
        wbf['total_pink'].set_bottom()

        wbf['total_float_pink'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align': 'right','num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_pink'].set_left()
        wbf['total_float_pink'].set_right()
        wbf['total_float_pink'].set_top()
        wbf['total_float_pink'].set_bottom()

        wbf['total_float_pink2'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align': 'center','num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_pink2'].set_left()
        wbf['total_float_pink2'].set_right()
        wbf['total_float_pink2'].set_top()
        wbf['total_float_pink2'].set_bottom() 

        wbf['total_violet'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align':'right', 'font_name': 'Georgia'})
        wbf['total_violet'].set_left()
        wbf['total_violet'].set_right()
        wbf['total_violet'].set_top()
        wbf['total_violet'].set_bottom()

        wbf['total_float_violet'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align': 'right','num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_violet'].set_left()
        wbf['total_float_violet'].set_right()
        wbf['total_float_violet'].set_top()
        wbf['total_float_violet'].set_bottom()

        wbf['total_float_violet2'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align': 'center','num_format': '#,##0.00', 'font_name': 'Georgia'})
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

