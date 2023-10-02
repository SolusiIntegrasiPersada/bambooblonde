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
        report_name = 'Main Color Sales Stock Report'
        filename = '%s %s'%(report_name,date_string)
      
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf, workbook = self.add_workbook_format(workbook)

        worksheet = workbook.add_worksheet(report_name)

        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 5)
        worksheet.set_column('H:H', 15)
        worksheet.set_column('I:I', 15)
        worksheet.set_column('J:J', 10)
        worksheet.set_column('K:K', 10)
        worksheet.set_column('L:L', 10)
        worksheet.set_column('M:M', 10)
        worksheet.set_column('N:N', 15)
        worksheet.set_column('O:O', 5)
        worksheet.set_column('P:P', 15)
        worksheet.set_column('Q:Q', 15)
        worksheet.set_column('R:R', 10)
        worksheet.set_column('S:S', 10)
        worksheet.set_column('T:T', 10)
        worksheet.set_column('U:U', 10)
        worksheet.set_column('V:V', 15)
        worksheet.set_column('W:W', 20)
        worksheet.set_column('X:X', 20)
        worksheet.set_column('Y:Y', 20)
        # worksheet.set_column('Z:Z', 20)

        worksheet.merge_range('A1:D1', 'PERIOD OF SALES : ' + str(start_month) + ' ' + str(start_day) + 'th - ' + str(end_month) + ' ' + str(end_day) + 'th, ' +  str(year) , wbf['title_doc_brown'])
        worksheet.merge_range('A2:D2', 'LAST STOCK : ' + str(end_month) + ' ' + str(end_day) + 'th, ' +  str(year), wbf['title_doc_pink'])


        worksheet.write('A5:B5', 'Main Color', wbf['header_blue'])
        worksheet.write('B5:C5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('C5:D5', '%', wbf['header_blue'])
        worksheet.write('D5:E5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('E5:F5', '%', wbf['header_blue'])
        worksheet.write('F5:G5', '% SELL THRU', wbf['header_pink'])


        worksheet.write('H5:I5', 'Main Color', wbf['header_blue'])
        worksheet.write('I5:J5', 'Category', wbf['header_blue'])
        worksheet.write('J5:K5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('K5:L5', '%', wbf['header_blue'])
        worksheet.write('L5:M5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('M5:N5', '%', wbf['header_blue'])
        worksheet.write('N5:05', '% SELL THRU', wbf['header_pink'])

        worksheet.write('P5:Q5', 'Main Color', wbf['header_blue'])
        worksheet.write('Q5:R5', 'Sub Color', wbf['header_blue'])
        worksheet.write('R5:S5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('S5:T5', '%', wbf['header_blue'])
        worksheet.write('T5:U5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('U5:V5', '%', wbf['header_blue'])
        worksheet.write('V5:W5', '% SELL THRU', wbf['header_pink'])

        pos_order_lines = self.env['pos.order.line'].search([
            ('order_id.date_order', '>=', self.start_period),
            ('order_id.date_order', '<=', self.end_period),
            ('order_id.state', 'not in', ['draft','cancel']),
            ('product_id.product_model_categ_id.name', '=', 'WOMENS WEAR')
        ])
        
        groups = groupby(pos_order_lines, key=lambda x: (x.product_id.main_color_id.name))
        data = {}
        for (main_color), lines in groups:
            if not main_color :
                main_color = str(main_color)
            if str(main_color) not in data:
                data[main_color] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                }

            qty_sold = sum(line.qty for line in lines)
            data[main_color]['qty_print_sold'] += qty_sold
            
        quants = self.env['stock.quant'].search([
            ('product_id.product_model_categ_id.name', '=', 'WOMENS WEAR'),
            ('location_id.usage', '=', 'internal'),
            # ('quantity', '>', 0),
            # ('create_date', '>=', self.start_period),
            ('create_date', '<', self.end_period),
        ])

        for quant in quants:
            main_color = quant.product_id.main_color_id.name
            if not main_color :
                main_color = str(main_color)
            if str(main_color) not in data:
                data[main_color] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                }
            # data[main_color][f'{data_type}_stock'] += quant.quantity
            data[main_color]['qty_print_stock'] += quant.quantity
            
        total_qty_print_stock = sum(values['qty_print_stock'] for values in data.values())
        total_qty_print_sold = sum(values['qty_print_sold'] for values in data.values())
        
        row = 6
        total_percent_print_sold = 0
        total_percent_print_stock = 0
        total_sell_thru_print  = 0
        for main_color, values in data.items():
           
            percent_print_sold = 0
            percent_print_stock = 0
            sell_thru_print = 0

          
            if total_qty_print_sold != 0:
                percent_print_sold = round((values['qty_print_sold'] / total_qty_print_sold)*100, 2) or 0
            if total_qty_print_stock != 0:
                percent_print_stock = round((values['qty_print_stock'] / total_qty_print_stock)*100, 2) or 0


            print_sold_stock = values['qty_print_sold'] + values['qty_print_stock']

            if print_sold_stock != 0:
                sell_thru_print = values['qty_print_sold']/print_sold_stock
            sell_thru_print = round((sell_thru_print)*100, 2) or 0

            worksheet.write('A%s:B%s' %(row, row), main_color or '', wbf['content'])
            worksheet.write('B%s:C%s' %(row, row), values['qty_print_sold'] or '', wbf['content_float'])
            worksheet.write('C%s:D%s' %(row, row), str(percent_print_sold) + '%' or '', wbf['content_float'])
            worksheet.write('D%s:E%s' %(row, row), values['qty_print_stock'] or '', wbf['content_float'])
            worksheet.write('E%s:F%s' %(row, row), str(percent_print_stock) + '%' or '', wbf['content_float'])
            worksheet.write('F%s:G%s' %(row, row), str(sell_thru_print) + '%' or '', wbf['content_float'])
            row +=1

          
            total_percent_print_sold += percent_print_sold
            total_percent_print_stock += percent_print_stock
            total_sell_thru_print += sell_thru_print


        total_percent_print_sold = min(round(total_percent_print_sold, 2), 100)
        total_percent_print_stock = min(round(total_percent_print_stock, 2), 100)
        total_sell_thru_print = min(round(total_sell_thru_print, 2), 100)

        worksheet.write('A%s:B%s' %(row, row), 'Grand Total', wbf['total_content'])
        worksheet.write('B%s:C%s' %(row, row), total_qty_print_sold or '', wbf['total_content_float'])
        worksheet.write('C%s:D%s' %(row, row), str(total_percent_print_sold) + '%' or '', wbf['total_content_float'])
        worksheet.write('D%s:E%s' %(row, row), total_qty_print_stock or '', wbf['total_content_float'])
        worksheet.write('E%s:F%s' %(row, row), str(total_percent_print_stock) + '%' or '', wbf['total_content_float'])
        worksheet.write('F%s:G%s' %(row, row), str(total_sell_thru_print) + '%' or '', wbf['total_content_float'])
        
        groups = groupby(pos_order_lines, key=lambda x: (x.product_id.main_color_id.name, x.product_id.product_category_categ_id.name))
        data_main_categ = {}
        
        
        for (main_color, category), lines in groups:
            
            main_color_plus_categ = f"{str(main_color)}/{str(category)}"
            if main_color_plus_categ not in data_main_categ:
                data_main_categ[main_color_plus_categ] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                }

            qty_sold = sum(line.qty for line in lines)
            data_main_categ[main_color_plus_categ]['qty_print_sold'] += qty_sold
            

            


        for quant in quants:
            main_color = quant.product_id.main_color_id.name
            category = quant.product_id.product_category_categ_id.name
            main_color_plus_categ = f"{str(main_color)}/{str(category)}"
            if main_color_plus_categ not in data_main_categ:
                data_main_categ[main_color_plus_categ] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                }
                
            data_main_categ[main_color_plus_categ]['qty_print_stock'] += quant.quantity
            
        total_qty_print_stock_b = sum(values['qty_print_stock'] for values in data_main_categ.values())
        total_qty_print_sold_b = sum(values['qty_print_sold'] for values in data_main_categ.values())
        mapping = []
        warna = ""
        categ = ""
        for main_and_categ, values in data_main_categ.items():
            parts = main_and_categ.split('/')  # Membagi string berdasarkan tanda '/'
            if len(parts) == 2:
                warna, categ = parts
                
            mapping.append({'warna': warna, 'categ': categ,'qty_print_sold' : values['qty_print_sold'] , 'qty_print_stock' : values['qty_print_stock']})
            
        mapping_sorted = sorted(mapping, key=lambda x: x['warna'])
        
        row = 6
        total_percent_print_sold = 0
        total_percent_print_stock = 0
        total_sell_thru_print  = 0
        
        
        warna_old = "new"
        total_sold_per_warna = 0
        total_stock_per_warna = 0
        total_percent_print_sold_per_warna = 0 
        total_percent_print_stock_per_warna= 0
        total_sell_thru_print_per_warna = 0
        for colorxcateg in mapping_sorted:
            
            
            percent_print_sold = 0
            percent_print_stock = 0
            sell_thru_print = 0

          
            if total_qty_print_sold_b != 0:
                percent_print_sold = round((colorxcateg['qty_print_sold'] / total_qty_print_sold_b)*100, 2) or 0
            if total_qty_print_stock_b != 0:
                percent_print_stock = round((colorxcateg['qty_print_stock'] / total_qty_print_stock_b)*100, 2) or 0


            print_sold_stock = colorxcateg['qty_print_sold'] + colorxcateg['qty_print_stock']

            if print_sold_stock != 0:
                sell_thru_print = colorxcateg['qty_print_sold']/print_sold_stock
            sell_thru_print = round((sell_thru_print)*100, 2) or 0
            
            
            if warna_old == 'new' :
                warna_old = colorxcateg['warna']
                
            if warna_old != colorxcateg['warna'] :
                
                total_percent_print_sold_per_warna = round(total_percent_print_sold_per_warna, 2) or 0
                total_percent_print_stock_per_warna = round(total_percent_print_stock_per_warna, 2) or 0
                total_sell_thru_print_per_warna = round(total_sell_thru_print_per_warna, 2) or 0
                worksheet.write('H%s:I%s' %(row, row), f'{warna_old} Total', wbf['total_content'])
                worksheet.write('I%s:J%s' %(row, row), '', wbf['total_content'])
                worksheet.write('J%s:K%s' %(row, row), total_sold_per_warna or '0', wbf['total_content_float'])
                worksheet.write('K%s:L%s' %(row, row), str(total_percent_print_sold_per_warna) + '%' or '', wbf['total_content_float'])
                worksheet.write('L%s:M%s' %(row, row), total_stock_per_warna or '0', wbf['total_content_float'])
                worksheet.write('M%s:N%s' %(row, row), str(total_percent_print_stock_per_warna) + '%' or '', wbf['total_content_float'])
                worksheet.write('N%s:O%s' %(row, row), str(total_sell_thru_print_per_warna) + '%' or '', wbf['total_content_float'])
                row +=1
                warna_old = colorxcateg['warna']
                total_sold_per_warna = 0
                total_stock_per_warna = 0
                total_percent_print_sold_per_warna = 0 
                total_percent_print_stock_per_warna= 0
                total_sell_thru_print_per_warna = 0

            worksheet.write('H%s:I%s' %(row, row), colorxcateg['warna'] or '', wbf['content'])
            worksheet.write('I%s:J%s' %(row, row), colorxcateg['categ'] or '', wbf['content'])
            worksheet.write('J%s:K%s' %(row, row), colorxcateg['qty_print_sold'] or '0', wbf['content_float'])
            worksheet.write('K%s:L%s' %(row, row), str(percent_print_sold) + '%' or '', wbf['content_float'])
            worksheet.write('L%s:M%s' %(row, row), colorxcateg['qty_print_stock'] or '0', wbf['content_float'])
            worksheet.write('M%s:N%s' %(row, row), str(percent_print_stock) + '%' or '', wbf['content_float'])
            worksheet.write('N%s:O%s' %(row, row), str(sell_thru_print) + '%' or '', wbf['content_float'])
            row +=1
            

            total_sold_per_warna += colorxcateg['qty_print_sold']
            total_stock_per_warna += colorxcateg['qty_print_stock']
            total_percent_print_sold_per_warna += percent_print_sold
            total_percent_print_stock_per_warna += percent_print_stock
            total_sell_thru_print_per_warna += sell_thru_print
          
            total_percent_print_sold += percent_print_sold
            total_percent_print_stock += percent_print_stock
            total_sell_thru_print += sell_thru_print
            
        

        total_percent_print_sold = min(round(total_percent_print_sold, 2), 100)
        total_percent_print_stock = min(round(total_percent_print_stock, 2), 100)
        total_sell_thru_print = min(round(total_sell_thru_print, 2), 100)
        
        if warna_old == colorxcateg['warna'] :
                
            total_percent_print_sold_per_warna = round(total_percent_print_sold_per_warna, 2) or 0
            total_percent_print_stock_per_warna = round(total_percent_print_stock_per_warna, 2) or 0
            total_sell_thru_print_per_warna = round(total_sell_thru_print_per_warna, 2) or 0
            worksheet.write('H%s:I%s' %(row, row), f'{warna_old} Total', wbf['total_content'])
            worksheet.write('I%s:J%s' %(row, row), '', wbf['total_content'])
            worksheet.write('J%s:K%s' %(row, row), total_sold_per_warna or '0', wbf['total_content_float'])
            worksheet.write('K%s:L%s' %(row, row), str(total_percent_print_sold_per_warna) + '%' or '', wbf['total_content_float'])
            worksheet.write('L%s:M%s' %(row, row), total_stock_per_warna or '0', wbf['total_content_float'])
            worksheet.write('M%s:N%s' %(row, row), str(total_percent_print_stock_per_warna) + '%' or '', wbf['total_content_float'])
            worksheet.write('N%s:O%s' %(row, row), str(total_sell_thru_print_per_warna) + '%' or '', wbf['total_content_float'])
            row +=1


        worksheet.write('H%s:I%s' %(row, row), 'Grand Total', wbf['total_content'])
        worksheet.write('I%s:J%s' %(row, row), '', wbf['total_content'])
        worksheet.write('J%s:K%s' %(row, row), total_qty_print_sold or '', wbf['total_content_float'])
        worksheet.write('K%s:L%s' %(row, row), str(total_percent_print_sold) + '%' or '', wbf['total_content_float'])
        worksheet.write('L%s:M%s' %(row, row), total_qty_print_stock or '', wbf['total_content_float'])
        worksheet.write('M%s:N%s' %(row, row), str(total_percent_print_stock) + '%' or '', wbf['total_content_float'])
        worksheet.write('N%s:O%s' %(row, row), str(total_sell_thru_print) + '%' or '', wbf['total_content_float'])
        

        groups = groupby(pos_order_lines, key=lambda x: (x.product_id.main_color_id.name, x.product_id.product_template_variant_value_ids.filtered(lambda x: x.attribute_id.name.upper() in ['COLOR','COLOUR','COLOURS','COLORS','WARNA','CORAK']).name
))
        data_main_sub_color = {}
        
        
        for (main_color, sub_color), lines in groups:
            
            main_color_plus_sub_color = f"{str(main_color)}/{str(sub_color)}"
            if main_color_plus_sub_color not in data_main_sub_color:
                data_main_sub_color[main_color_plus_sub_color] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                }

            qty_sold = sum(line.qty for line in lines)
            data_main_sub_color[main_color_plus_sub_color]['qty_print_sold'] += qty_sold
            

            


        for quant in quants:
            main_color = quant.product_id.main_color_id.name
            quant.product_id.product_template_variant_value_ids.filtered(lambda x: x.attribute_id.name.upper() in ['COLOR','COLOUR','COLOURS','COLORS','WARNA','CORAK']).name
            main_color_plus_sub_color = f"{str(main_color)}/{str(sub_color)}"
            if main_color_plus_sub_color not in data_main_sub_color:
                data_main_sub_color[main_color_plus_sub_color] = {
                    'qty_print_sold': 0.0,
                    'qty_print_stock': 0.0,
                }
                
            data_main_sub_color[main_color_plus_sub_color]['qty_print_stock'] += quant.quantity
            
        total_qty_print_stock_b = sum(values['qty_print_stock'] for values in data_main_sub_color.values())
        total_qty_print_sold_b = sum(values['qty_print_sold'] for values in data_main_sub_color.values())
        mapping = []
        warna = ""
        categ = ""
        for main_and_categ, values in data_main_sub_color.items():
            parts = main_and_categ.split('/')  # Membagi string berdasarkan tanda '/'
            if len(parts) == 2:
                warna, categ = parts
                
            mapping.append({'warna': warna, 'categ': categ,'qty_print_sold' : values['qty_print_sold'] , 'qty_print_stock' : values['qty_print_stock']})
            
        mapping_sorted = sorted(mapping, key=lambda x: x['warna'])
        
        row = 6
        total_percent_print_sold = 0
        total_percent_print_stock = 0
        total_sell_thru_print  = 0
        
        
        warna_old = "new"
        total_sold_per_warna = 0
        total_stock_per_warna = 0
        total_percent_print_sold_per_warna = 0 
        total_percent_print_stock_per_warna= 0
        total_sell_thru_print_per_warna = 0
        for colorxcateg in mapping_sorted:
            
            
            percent_print_sold = 0
            percent_print_stock = 0
            sell_thru_print = 0

          
            if total_qty_print_sold_b != 0:
                percent_print_sold = round((colorxcateg['qty_print_sold'] / total_qty_print_sold_b)*100, 2) or 0
            if total_qty_print_stock_b != 0:
                percent_print_stock = round((colorxcateg['qty_print_stock'] / total_qty_print_stock_b)*100, 2) or 0


            print_sold_stock = colorxcateg['qty_print_sold'] + colorxcateg['qty_print_stock']

            if print_sold_stock != 0:
                sell_thru_print = colorxcateg['qty_print_sold']/print_sold_stock
            sell_thru_print = round((sell_thru_print)*100, 2) or 0
            
            
            if warna_old == 'new' :
                warna_old = colorxcateg['warna']
                
            if warna_old != colorxcateg['warna'] :
                
                total_percent_print_sold_per_warna = round(total_percent_print_sold_per_warna, 2) or 0
                total_percent_print_stock_per_warna = round(total_percent_print_stock_per_warna, 2) or 0
                total_sell_thru_print_per_warna = round(total_sell_thru_print_per_warna, 2) or 0
                worksheet.write('P%s:Q%s' %(row, row), f'{warna_old} Total', wbf['total_content'])
                worksheet.write('Q%s:R%s' %(row, row), '', wbf['total_content'])
                worksheet.write('R%s:S%s' %(row, row), total_sold_per_warna or '0', wbf['total_content_float'])
                worksheet.write('S%s:T%s' %(row, row), str(total_percent_print_sold_per_warna) + '%' or '', wbf['total_content_float'])
                worksheet.write('T%s:U%s' %(row, row), total_stock_per_warna or '0', wbf['total_content_float'])
                worksheet.write('U%s:V%s' %(row, row), str(total_percent_print_stock_per_warna) + '%' or '', wbf['total_content_float'])
                worksheet.write('V%s:W%s' %(row, row), str(total_sell_thru_print_per_warna) + '%' or '', wbf['total_content_float'])
                row +=1
                warna_old = colorxcateg['warna']
                total_sold_per_warna = 0
                total_stock_per_warna = 0
                total_percent_print_sold_per_warna = 0 
                total_percent_print_stock_per_warna= 0
                total_sell_thru_print_per_warna = 0

            worksheet.write('P%s:Q%s' %(row, row), colorxcateg['warna'] or '', wbf['content'])
            worksheet.write('Q%s:R%s' %(row, row), colorxcateg['categ'] or '', wbf['content'])
            worksheet.write('R%s:S%s' %(row, row), colorxcateg['qty_print_sold'] or '0', wbf['content_float'])
            worksheet.write('S%s:T%s' %(row, row), str(percent_print_sold) + '%' or '', wbf['content_float'])
            worksheet.write('T%s:U%s' %(row, row), colorxcateg['qty_print_stock'] or '0', wbf['content_float'])
            worksheet.write('U%s:V%s' %(row, row), str(percent_print_stock) + '%' or '', wbf['content_float'])
            worksheet.write('V%s:W%s' %(row, row), str(sell_thru_print) + '%' or '', wbf['content_float'])
            row +=1
            

            total_sold_per_warna += colorxcateg['qty_print_sold']
            total_stock_per_warna += colorxcateg['qty_print_stock']
            total_percent_print_sold_per_warna += percent_print_sold
            total_percent_print_stock_per_warna += percent_print_stock
            total_sell_thru_print_per_warna += sell_thru_print
          
            total_percent_print_sold += percent_print_sold
            total_percent_print_stock += percent_print_stock
            total_sell_thru_print += sell_thru_print
            
        

        total_percent_print_sold = min(round(total_percent_print_sold, 2), 100) 
        total_percent_print_stock = min(round(total_percent_print_stock, 2), 100)
        total_sell_thru_print = min(round(total_sell_thru_print, 2), 100)
            
        
        if warna_old == colorxcateg['warna'] :
                
            total_percent_print_sold_per_warna = round(total_percent_print_sold_per_warna, 2) or 0
            total_percent_print_stock_per_warna = round(total_percent_print_stock_per_warna, 2) or 0
            total_sell_thru_print_per_warna = round(total_sell_thru_print_per_warna, 2) or 0
            worksheet.write('P%s:Q%s' %(row, row), f'{warna_old} Total', wbf['total_content'])
            worksheet.write('Q%s:R%s' %(row, row), '', wbf['total_content'])
            worksheet.write('R%s:S%s' %(row, row), total_sold_per_warna or '0', wbf['total_content_float'])
            worksheet.write('S%s:T%s' %(row, row), str(total_percent_print_sold_per_warna) + '%' or '', wbf['total_content_float'])
            worksheet.write('T%s:U%s' %(row, row), total_stock_per_warna or '0', wbf['total_content_float'])
            worksheet.write('U%s:V%s' %(row, row), str(total_percent_print_stock_per_warna) + '%' or '', wbf['total_content_float'])
            worksheet.write('V%s:W%s' %(row, row), str(total_sell_thru_print_per_warna) + '%' or '', wbf['total_content_float'])
            row +=1


        worksheet.write('P%s:Q%s' %(row, row), 'Grand Total', wbf['total_content'])
        worksheet.write('Q%s:R%s' %(row, row), '', wbf['total_content'])
        worksheet.write('R%s:S%s' %(row, row), total_qty_print_sold or '', wbf['total_content_float'])
        worksheet.write('S%s:T%s' %(row, row), str(total_percent_print_sold) + '%' or '', wbf['total_content_float'])
        worksheet.write('T%s:U%s' %(row, row), total_qty_print_stock or '', wbf['total_content_float'])
        worksheet.write('U%s:V%s' %(row, row), str(total_percent_print_stock) + '%' or '', wbf['total_content_float'])
        worksheet.write('V%s:W%s' %(row, row), str(total_sell_thru_print) + '%' or '', wbf['total_content_float'])
        


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

