import xlsxwriter
import base64
from odoo import fields, models, api, _
from io import BytesIO
from datetime import date, datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
from pytz import timezone
import pytz
import io
import itertools
import pandas as pd
from itertools import groupby
from odoo.exceptions import UserError
from PIL import Image
from dateutil.rrule import rrule, MONTHLY
from math import ceil

class SlowSellingSalestockReport(models.TransientModel):
    _name = "slow.selling.salestock.report"
    _description = "Slow Selling Sale Stock .xlsx"
    
    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone(self.env.user.tz or 'UTC'))
    
    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)
    start_period = fields.Date('Start Period')
    end_period = fields.Date('End Period')
    categ_id = fields.Many2one('product.category', 'Category')
    parent_categ_id = fields.Many2one('product.category', 'Model')
    class_id = fields.Many2one('class.product', 'Class')
    types = fields.Selection([('staples','Staples'),('trend','Trend')], string='Type')
    start_aging = fields.Integer('Start Aging')
    end_aging = fields.Integer('End Aging')

    def print_excel_report(self):

        def calculate_scale(file_path, bound_size):
            # check the image size without loading it into memory
            im = Image.open(file_path)
            original_width, original_height = im.size

            # calculate the resize factor, keeping original aspect and staying within boundary
            bound_width, bound_height = bound_size
            ratios = (float(bound_width) / original_width, float(bound_height) / original_height)
            return min(ratios)

        datetime_string = self.get_default_date_model().strftime("%Y-%m-%d %H:%M:%S")
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        report_name = 'Slow Selling Sale Stock Report'
        filename = '%s %s'%(report_name,date_string)
      
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf, workbook = self.add_workbook_format(workbook)

        worksheet = workbook.add_worksheet(report_name)

        start_ds = datetime.strptime(str(self.start_period), '%Y-%m-%d')
        end_ds = datetime.strptime(str(self.end_period), '%Y-%m-%d')
        year_start = start_ds.strftime('%Y')
        year_end = end_ds.strftime('%Y')
        start_month = start_ds.strftime('%B')
        start_day = start_ds.strftime('%d')
        end_month = end_ds.strftime('%B')
        end_day = end_ds.strftime('%d')

        month_list = pd.period_range(start=self.start_period, end=self.end_period, freq='M')
        months = [month.strftime("%b-%Y") for month in month_list]
        # total_months = len(months)
        # if total_months > 4:
        #   raise UserError(_("Cannot generate more than 4 months!"))
        # elif total_months < 4:
        #   raise UserError(_("Cannot generate less than 4 months!"))

        # index = 0
        # col = 0
        # for month in month_list:
        #     index += 1
        #     month_list = month.strftime("%b-%Y")
        #     tahun = month.strftime("%Y")
        #     bulan = month.strftime("%m")
        #     if index == 1:
        #         col = 13
        #     elif index == 2:
        #         col = 14
        #     elif index == 3:
        #         col = 15
        #     elif index == 4:
        #         col = 16

        #     worksheet.write(2,col, str(month_list), wbf['header_green'])

        start_date = fields.Date.from_string(self.start_period)
        end_date = fields.Date.from_string(self.end_period)
        months = list(rrule(MONTHLY, dtstart=start_date, until=end_date))

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
        worksheet.set_column('L:L', 20)
        worksheet.set_column('M:M', 20)
        # worksheet.set_column('N:N', 20)
        # worksheet.set_column('O:O', 20)
        # worksheet.set_column('P:P', 20)
        # worksheet.set_column('Q:Q', 20)
        # worksheet.set_column('R:R', 20)

        worksheet.merge_range('A1:E1', 'PERIOD OF SALES : ' + str(start_month) + ' ' + str(start_day) + 'th, ' + str(year_start) + ' - '+ str(end_month) + ' ' + str(end_day) + 'th, ' + str(year_end) , wbf['title_doc_brown'])
        worksheet.merge_range('A2:E2', 'LAST STOCK : ' + str(end_month) + ' ' + str(end_day) + 'th, ' + str(year_end), wbf['title_doc_pink'])
        worksheet.merge_range('F1:M1', '', wbf['title_doc'])
        worksheet.merge_range('F2:M2', '', wbf['title_doc'])
        worksheet.merge_range('A3:K3', '', wbf['header'])

        worksheet.merge_range('L3:M3', 'SUMMARY TOTAL', wbf['header_orange'])

        columns = [
            ('Category', 20, 'char', 'char'),
            ('Style', 30, 'char', 'char'),
            ('Stock Name', 30, 'char', 'char'),
            ('Stock ID', 20, 'char', 'char'),
            ('Color', 20, 'char', 'char'),
            ('Photo', 20, 'char', 'char'),
            ('Aging', 20, 'char', 'char'),
            ('Barcode', 20, 'char', 'char'),
            ('Size', 20, 'char', 'char'),
            ('Cost Price', 20, 'char', 'char'),
            ('Retail Price', 20, 'char', 'char'),
            ('Qty Sold', 20, 'float', 'float'),
            ('In Stock', 20, 'float2', 'float2'),
            # ('Qty Sold', 20, 'float', 'float'),
            # ('Qty Sold', 20, 'float', 'float'),
            # ('Qty Sold', 20, 'float', 'float'),
            # ('Qty Sold', 20, 'float', 'float'),
        ]

        row = 4
        col = 0
        for column in columns :
            column_name = column[0]
            column_width = column[1]
            column_type = column[2]
            bg_column = wbf['header_purple']
            if column_type == 'float':
                bg_column = wbf['header_yellow']
            elif column_type == 'float2':
                bg_column = wbf['header_violet']
            worksheet.set_column(col,col,column_width)
            worksheet.write(row-1, col, column_name, bg_column)

            col += 1

        row += 1
        no = 1

        domain = [
            ('order_id.state', 'not in', ['draft','cancel']),
            ('order_id.date_order', '>=', self.start_period),
            ('order_id.date_order', '<=', self.end_period)
        ]

        if self.categ_id:
            domain += [('product_id.categ_id.parent_id', '=', self.categ_id.id)]
        if self.parent_categ_id:
            domain += [('product_id.categ_id.parent_id.parent_id', '=', self.parent_categ_id.id)]
        if self.class_id:
            domain += [('product_id.class_product', '=', self.class_id.id)]
        if self.types:
            domain += [('product_id.types', '=', self.types)]

        pos_orders = self.env['pos.order.line'].search(domain)

        report_data = {}
        for line in pos_orders:
            prod = line.product_id
            category = prod.product_tmpl_id.categ_id.name
            style = '<' + str(prod.name) + '>-' + str(line.color)
            stockname = '<' + str(prod.name) + '>'
            stockid = prod.default_code
            color = line.color
            barcode = prod.barcode
            size = line.size
            cost_price = line.cost_in_order  or 0
            retail_price = prod.lst_price
            sold_qty = sum(line.mapped('qty'))
            photo = prod.image_1920
            # qty_stock = sum(line.product_id.stock_quant_ids.filtered(lambda x: x.location_id.usage == 'internal' and x.location_id.warehouse_id.code in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Onlne') and x.in_date.date() >= self.start_period and x.in_date.date() <= self.end_period).mapped('quantity'))

            if prod.id not in report_data:
                report_data[prod.id] = {f'month_{i}': 0 for i in range(1, len(months)+1)}
                report_data[prod.id].update({
                                'category': category,
                                'style': style,
                                'stockname': stockname,
                                'stockid': stockid,
                                'color': color,
                                'photo': '',
                                'aging': '',
                                'barcode': barcode,
                                'size': size,
                                'cost_price': cost_price,
                                'retail_price': retail_price,
                                'total_qty_sold': sold_qty,
                                'total_stock_in': prod.qty_available,
                })

            else:
                report_data[prod.id]['total_qty_sold'] += sold_qty
                report_data[prod.id]['total_stock_in'] += prod.qty_available

            # qty_stock = sum(line.product_id.qty_available for line in lines)
            # qty_stock = sum(line.product_id.product_tmpl_id.qty_available for line in lines)
            # calculate sold qty per month
            date_order = fields.Date.from_string(line.order_id.date_order)
            month_diff = relativedelta(date_order, self.start_period).months
            if month_diff < len(months):
                report_data[line.product_id.id][f'month_{month_diff+1}'] += sold_qty


            # calculate aging
            # now = fields.Date.today()
            today = datetime.now()

            # age_in_weeks = (now - date_order).days // 7
            # report_data[prod.id]['aging'] = str(age_in_weeks) + ' weeks'

            moves = sorted(line.product_id.stock_move_ids.filtered(lambda x: x.picking_type_id.code == 'incoming' and x.state == 'done' and x.product_id == line.product_id), key=lambda x: x.date)
            # age_in_weeks = ((today - moves[0].date).days) // 7 if moves else 0
            age_in_weeks = ceil(((today - moves[0].date).days) / 7) if moves else 0


            report_data[prod.id]['aging'] = int(age_in_weeks)
            report_data[prod.id]['photo'] = photo

        # Format report data into rows
        rows = []
        for data in report_data.values():
            if data.get('aging', 0) >= self.start_aging and data.get('aging', 0) <= self.end_aging:
                row = [
                    data.get('category', ''),
                    data.get('style', ''),
                    data.get('stockname', ''),
                    data.get('stockid', ''),
                    data.get('color', ''),
                    data.get('barcode', ''),
                    data.get('size', ''),
                    data.get('cost_price', ''),
                    data.get('retail_price', ''),
                    data.get('total_qty_sold', 0),
                    data.get('total_stock_in', 0),
                ]
                # for i in range(1, len(months)+1):
                    # row.append(data.get(f'month_{i}', 0))
                row.append(data.get('aging', 0))
                row.append(data.get('photo', ''))
                rows.append(row)

            # else:
            #     row = [
            #         data.get('category', ''),
            #         data.get('style', ''),
            #         data.get('stockname', ''),
            #         data.get('stockid', ''),
            #         data.get('color', ''),
            #         data.get('barcode', ''),
            #         data.get('size', ''),
            #         data.get('cost_price', ''),
            #         data.get('retail_price', ''),
            #         data.get('total_qty_sold', 0),
            #         data.get('total_stock_in', 0),
            #     ]
            #     # for i in range(1, len(months)+1):
            #         # row.append(data.get(f'month_{i}', 0))
            #     row.append(data.get('aging', 0))
            #     row.append(data.get('photo', ''))
            #     rows.append(row)

            # if self.type_aging == 'A':
            #     if data.get('aging', 0) >= 3 and data.get('aging', 0) <= 8:
            #         row = [
            #             data.get('category', ''),
            #             data.get('style', ''),
            #             data.get('stockname', ''),
            #             data.get('stockid', ''),
            #             data.get('color', ''),
            #             data.get('barcode', ''),
            #             data.get('size', ''),
            #             data.get('cost_price', ''),
            #             data.get('retail_price', ''),
            #             data.get('total_qty_sold', 0),
            #             data.get('total_stock_in', 0),
            #         ]
            #         for i in range(1, len(months)+1):
            #             row.append(data.get(f'month_{i}', 0))
            #         row.append(data.get('aging', 0))
            #         row.append(data.get('photo', ''))
            #         rows.append(row)
            # elif self.type_aging == 'B':        
            #     if data.get('aging', 0) >= 28:
            #         row = [
            #             data.get('category', ''),
            #             data.get('style', ''),
            #             data.get('stockname', ''),
            #             data.get('stockid', ''),
            #             data.get('color', ''),
            #             data.get('barcode', ''),
            #             data.get('size', ''),
            #             data.get('cost_price', ''),
            #             data.get('retail_price', ''),
            #             data.get('total_qty_sold', 0),
            #             data.get('total_stock_in', 0),
            #         ]
            #         for i in range(1, len(months)+1):
            #             row.append(data.get(f'month_{i}', 0))
            #         row.append(data.get('aging', 0))
            #         row.append(data.get('photo', ''))
            #         rows.append(row)
            # else:
            #     row = [
            #         data.get('category', ''),
            #         data.get('style', ''),
            #         data.get('stockname', ''),
            #         data.get('stockid', ''),
            #         data.get('color', ''),
            #         data.get('barcode', ''),
            #         data.get('size', ''),
            #         data.get('cost_price', ''),
            #         data.get('retail_price', ''),
            #         data.get('total_qty_sold', 0),
            #         data.get('total_stock_in', 0),
            #     ]
            #     for i in range(1, len(months)+1):
            #         row.append(data.get(f'month_{i}', 0))
            #     row.append(data.get('aging', 0))
            #     row.append(data.get('photo', ''))
            #     rows.append(row)

        grouped_colors = {}
        for row in rows:
            # category, style, stockname, stockid, color, barcode, size, cost_price, retail_price, qty_sold, stock_in, month_1, month_2, month_3, month_4, aging, photo = row
            category, style, stockname, stockid, color, barcode, size, cost_price, retail_price, qty_sold, stock_in, aging, photo = row
            key = (category, style, stockname, color)
            if key not in grouped_colors:
                grouped_colors[key] = {
                    'photo': photo,
                    'stockid': stockid,
                    'qty_sold': qty_sold,
                    'stock_in': stock_in,
                    # 'month_1': month_1,
                    # 'month_2': month_2,
                    # 'month_3': month_3,
                    # 'month_4': month_4,
                    'children': {}
                }
            else:
                grouped_colors[key]['qty_sold'] += qty_sold
                grouped_colors[key]['stock_in'] += stock_in
                # grouped_colors[key]['month_1'] += month_1
                # grouped_colors[key]['month_2'] += month_2
                # grouped_colors[key]['month_3'] += month_3
                # grouped_colors[key]['month_4'] += month_4

            if size not in grouped_colors[key]['children']:
                grouped_colors[key]['children'][size] = {
                    'photo': photo,
                    'barcode': barcode,
                    'cost_price': cost_price,
                    'retail_price': retail_price,
                    'qty_sold': qty_sold,
                    'stock_in': stock_in,
                    # 'month_1': month_1,
                    # 'month_2': month_2,
                    # 'month_3': month_3,
                    # 'month_4': month_4,
                    'aging': aging
                }
            else:
                grouped_colors[key]['children'][size]['qty_sold'] += qty_sold
                grouped_colors[key]['children'][size]['stock_in'] += stock_in
                # grouped_colors[key]['children'][size]['month_1'] += month_1
                # grouped_colors[key]['children'][size]['month_2'] += month_2
                # grouped_colors[key]['children'][size]['month_3'] += month_3
                # grouped_colors[key]['children'][size]['month_4'] += month_4

        # Print the result
        row = 4
        gt_qty_sold = 0
        gt_stock_in = 0
        # gt_month_1 = 0
        # gt_month_2 = 0
        # gt_month_3 = 0
        # gt_month_4 = 0
        sorted_colors = sorted(grouped_colors.items(), key=lambda x: x[1]['qty_sold'], reverse=True)
        for key, value in sorted_colors:
        # for key, value in grouped_colors.items():
            category, style, stockname, color = key
            # qty_sold, stock_in, month_1, month_2, month_3, month_4 = value['qty_sold'], value['stock_in'], value['month_1'], value['month_2'], value['month_3'], value['month_4']
            qty_sold, stock_in = value['qty_sold'], value['stock_in']
            dt_style = str(style) + ' Total'
            dt_qty_sold = qty_sold
            dt_stock_in = stock_in
            # dt_month_1 = month_1
            # dt_month_2 = month_2
            # dt_month_3 = month_3
            # dt_month_4 = month_4
            dt_photo = ''
            if value['photo']:
                dt_photo = io.BytesIO(base64.b64decode(value['photo']))
            bound_width_height = (80, 80)
            dt_resize_scale = 0
            if dt_photo:
                dt_resize_scale = calculate_scale(dt_photo, bound_width_height)

            children = value['children']
            for size, size_value in children.items():
                d_category = category
                d_style = style
                d_stockname = stockname
                d_stockid = value['stockid']
                d_color = color
                d_aging = size_value['aging']
                d_barcode = size_value['barcode']
                d_photo = ''
                if size_value['photo']:
                    d_photo = io.BytesIO(base64.b64decode(size_value['photo']))
                bound_width_height = (80, 80)
                resize_scale = 0
                if d_photo:
                    resize_scale = calculate_scale(d_photo, bound_width_height)
                d_size = size
                d_cost_price = size_value['cost_price']
                d_retail_price = size_value['retail_price']
                d_qty_sold = size_value['qty_sold']
                d_stock_in = size_value['stock_in']
                # d_month_1 = size_value['month_1']
                # d_month_2 = size_value['month_2']
                # d_month_3 = size_value['month_3']
                # d_month_4 = size_value['month_4']

                worksheet.write(row, 0, d_category or ' ', wbf['content'])
                worksheet.write(row, 1, d_style or ' ', wbf['content'])
                worksheet.write(row, 2, d_stockname or ' ', wbf['content'])
                worksheet.write(row, 3, d_stockid or ' ', wbf['content'])
                worksheet.write(row, 4, d_color or ' ', wbf['content'])

                # if len(children) == 1:
                # Mengatur ukuran kolom
                worksheet.set_column(row, 5, 15)
                worksheet.set_row(row, 75)
                worksheet.insert_image(row, 5, "image.png", {'image_data': d_photo, 'bg_color': '#FFFFFF', 'x_scale': resize_scale, 'y_scale': resize_scale, 'x_offset': 10, 'y_offset': 10})
                
                worksheet.write(row, 6, d_aging or ' ', wbf['content2'])
                worksheet.write(row, 7, d_barcode or ' ', wbf['content'])
                worksheet.write(row, 8, d_size or ' ', wbf['content2'])
                worksheet.write(row, 9, d_cost_price or ' ', wbf['content_float'])
                worksheet.write(row, 10, d_retail_price or ' ', wbf['content_float'])
                worksheet.write(row, 11, d_qty_sold or ' ', wbf['content_float1'])
                worksheet.write(row, 12, d_stock_in or ' ', wbf['content_float2'])
                # worksheet.write(row, 13, d_month_1 or ' ', wbf['content_float1'])
                # worksheet.write(row, 14, d_month_2 or ' ', wbf['content_float1'])
                # worksheet.write(row, 15, d_month_3 or ' ', wbf['content_float1'])
                # worksheet.write(row, 16, d_month_4 or ' ', wbf['content_float1'])
                row += 1

            if len(children) > 1:
                worksheet.write(row, 0, ' ', wbf['total_content'])
                worksheet.write(row, 1, ' ', wbf['total_content'])
                worksheet.write(row, 2, dt_style, wbf['total_content'])
                worksheet.write(row, 3, ' ', wbf['total_content'])
                worksheet.write(row, 4, ' ', wbf['total_content'])
                worksheet.write(row, 5, ' ', wbf['total_content'])
                # worksheet.insert_image(row, 5, "image.png", {'image_data': dt_photo, 'bg_color': '#FFFFFF', 'x_scale': dt_resize_scale, 'y_scale': dt_resize_scale, 'x_offset': 10, 'y_offset': -40})
                worksheet.write(row, 6, ' ', wbf['total_content2'])
                worksheet.write(row, 7, ' ', wbf['total_content'])
                worksheet.write(row, 8, ' ', wbf['total_content2'])
                worksheet.write(row, 9, ' ', wbf['total_content_float'])
                worksheet.write(row, 10, ' ', wbf['total_content_float'])
                worksheet.write(row, 11, dt_qty_sold or ' ', wbf['total_content_float1'])
                worksheet.write(row, 12, dt_stock_in or ' ', wbf['total_content_float2'])
                # worksheet.write(row, 13, dt_month_1 or ' ', wbf['total_content_float1'])
                # worksheet.write(row, 14, dt_month_2 or ' ', wbf['total_content_float1'])
                # worksheet.write(row, 15, dt_month_3 or ' ', wbf['total_content_float1'])
                # worksheet.write(row, 16, dt_month_4 or ' ', wbf['total_content_float1'])
                row += 1

                gt_qty_sold += dt_qty_sold
                gt_stock_in += dt_stock_in
                # gt_month_1 += dt_month_1
                # gt_month_2 += dt_month_2
                # gt_month_3 += dt_month_3
                # gt_month_4 += dt_month_4

            else:
                gt_qty_sold += d_qty_sold
                gt_stock_in += d_stock_in
                # gt_month_1 += d_month_1
                # gt_month_2 += d_month_2
                # gt_month_3 += d_month_3
                # gt_month_4 += d_month_4

        worksheet.write(row, 0, 'Grand Total', wbf['header_blue'])
        worksheet.write(row, 1, ' ', wbf['header_blue'])
        worksheet.write(row, 2, ' ', wbf['header_blue'])
        worksheet.write(row, 3, ' ', wbf['header_blue'])
        worksheet.write(row, 4, ' ', wbf['header_blue'])
        worksheet.write(row, 5, ' ', wbf['header_blue'])
        worksheet.write(row, 6, ' ', wbf['header_blue'])
        worksheet.write(row, 7, ' ', wbf['header_blue'])
        worksheet.write(row, 8, ' ', wbf['header_blue'])
        worksheet.write(row, 9, ' ', wbf['header_blue'])
        worksheet.write(row, 10, ' ', wbf['header_blue'])
        worksheet.write(row, 11, gt_qty_sold or ' ', wbf['header_blue2'])
        worksheet.write(row, 12, gt_stock_in or ' ', wbf['header_blue2'])
        # worksheet.write(row, 13, gt_month_1 or ' ', wbf['header_blue2'])
        # worksheet.write(row, 14, gt_month_2 or ' ', wbf['header_blue2'])
        # worksheet.write(row, 15, gt_month_3 or ' ', wbf['header_blue2'])
        # worksheet.write(row, 16, gt_month_4 or ' ', wbf['header_blue2'])


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
            'white_orange': '#FFE4BD',
            'orange': '#FFDDAC',
            'red': '#FFBDBD',
            'yellow': '#FFFFBD',
            'pink': '#FFD5D5',
            'violet': '#CACAFF',
            'purple': '#E9CAFF',
            'green': '#CAFFCA',
            'light_green': '#D5FFD5',
            'dark_green': '#BDFFBD',
            'blue': '#CACAFF',
            'brown': '#E4DDCA',
            'salmon': '#F4F4F4',
            'beige': '#F6F6F6',
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

        wbf['header_blue'] = workbook.add_format({'bold': 1,'align': 'left','bg_color': colors['blue'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_blue'].set_border()

        wbf['header_blue2'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['blue'],'font_color': '#000000', 'font_name': 'Georgia'})
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

        wbf['header_purple'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['purple'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_purple'].set_border()

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
        wbf['content'].set_border()

        wbf['content2'] = workbook.add_format({'align': 'center', 'font_name': 'Georgia'})
        wbf['content2'].set_border()


        wbf['grandtotal_content'] = workbook.add_format({'align': 'center', 'font_name': 'Georgia', 'bg_color': colors['purple']})
        wbf['grandtotal_content'].set_border() 

        wbf['grandtotal_content_float'] = workbook.add_format({'bold': True, 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia', 'font_color': '#000000', 'bg_color': colors['purple']})
        wbf['grandtotal_content_float'].set_border() 

        wbf['total_content'] = workbook.add_format({ 'bold': 1,'align': 'left','font_color': '#000000', 'font_name': 'Georgia'})
        wbf['total_content'].set_border() 

        wbf['total_content2'] = workbook.add_format({ 'bold': 1,'align': 'center','font_color': '#000000', 'font_name': 'Georgia'})
        wbf['total_content2'].set_border() 

        wbf['total_content_float'] = workbook.add_format({'bold': True, 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia', 'font_color': '#000000'})
        wbf['total_content_float'].set_border() 

        wbf['total_content_float1'] = workbook.add_format({'bold': True, 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia', 'font_color': '#000000'})
        wbf['total_content_float1'].set_border() 

        wbf['total_content_float2'] = workbook.add_format({'bold': True, 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia', 'font_color': '#000000'})
        wbf['total_content_float2'].set_border() 

        wbf['total_content_float_price'] = workbook.add_format({'bold': True, 'align': 'right','num_format': '#,##0', 'font_name': 'Georgia','bg_color': colors['blue'], 'font_color': '#000000'})
        wbf['total_content_float_price'].set_border()

        wbf['content_float'] = workbook.add_format({'align': 'right','num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_float'].set_border()
 
        
        wbf['content_float1'] = workbook.add_format({'align': 'center','num_format': '#,##0', 'font_name': 'Georgia', 'bg_color': colors['yellow']})
        wbf['content_float1'].set_border()

        wbf['content_float2'] = workbook.add_format({'align': 'center','num_format': '#,##0', 'font_name': 'Georgia', 'bg_color': colors['violet']})
        wbf['content_float2'].set_border()

        wbf['content_float_price'] = workbook.add_format({'align': 'right','num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_float_price'].set_right() 
        wbf['content_float_price'].set_left()

        wbf['content_number'] = workbook.add_format({'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_number'].set_right() 
        wbf['content_number'].set_left() 
        
        wbf['content_percent'] = workbook.add_format({'align': 'right','num_format': '0.00%', 'font_name': 'Georgia'})
        wbf['content_percent'].set_right() 
        wbf['content_percent'].set_left() 
                
        wbf['total_float'] = workbook.add_format({'bold':1, 'bg_color':colors['white_orange'], 'align':'right', 'num_format':'#,##0', 'font_name': 'Georgia'})
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

        wbf['total_float_yellow'] = workbook.add_format({'bold':1, 'bg_color':colors['yellow'], 'align':'right', 'num_format':'#,##0', 'font_name': 'Georgia'})
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

        wbf['total_float_orange'] = workbook.add_format({'bold':1, 'bg_color':colors['orange'], 'align':'right', 'num_format':'#,##0', 'font_name': 'Georgia'})
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

        wbf['total_float_pink'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align': 'right','num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_pink'].set_left()
        wbf['total_float_pink'].set_right()
        wbf['total_float_pink'].set_top()
        wbf['total_float_pink'].set_bottom()

        wbf['total_float_pink2'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_pink2'].set_left()
        wbf['total_float_pink2'].set_right()
        wbf['total_float_pink2'].set_top()
        wbf['total_float_pink2'].set_bottom() 

        wbf['total_violet'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align':'right', 'font_name': 'Georgia'})
        wbf['total_violet'].set_left()
        wbf['total_violet'].set_right()
        wbf['total_violet'].set_top()
        wbf['total_violet'].set_bottom()

        wbf['total_float_violet'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align': 'right','num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_float_violet'].set_left()
        wbf['total_float_violet'].set_right()
        wbf['total_float_violet'].set_top()
        wbf['total_float_violet'].set_bottom()

        wbf['total_float_violet2'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia'})
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


