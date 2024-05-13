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
from math import ceil
from PIL import Image

class WhatsStockinSoldReport(models.TransientModel):
    _name = "whats.stockin.sold.report"
    _description = "What in Stock vs What is Sold .xlsx"
    _inherit = 'report.report_xlsx.abstract'
    
    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone(self.env.user.tz or 'UTC'))
    
    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)
    start_period = fields.Date('Start Period')
    end_period = fields.Date('End Period')
    class_product_id = fields.Many2one('class.product', string='Class')
    product_category_id = fields.Many2one('product.category', string='Category', domain=[('category_product', '=', 'category')])
    picture = fields.Boolean(string="Export With Photo")

    def print_excel_report(self):
        start_ds = datetime.strptime(str(self.start_period), '%Y-%m-%d')
        end_ds = datetime.strptime(str(self.end_period), '%Y-%m-%d')
        year = start_ds.strftime('%Y')
        start_month = start_ds.strftime('%B')
        start_day = start_ds.strftime('%d')
        end_month = end_ds.strftime('%B')
        end_day = end_ds.strftime('%d')

        datetime_string = self.get_default_date_model().strftime("%Y-%m-%d %H:%M:%S")
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        report_name = 'What in Stock vs What is Sold Report'
        filename = '%s %s'%(report_name,date_string)
      
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf, workbook = self.add_workbook_format(workbook)

        worksheet = workbook.add_worksheet(report_name)

        if self.picture is False:
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
            worksheet.set_column('N:N', 20)
            worksheet.set_column('O:O', 20)
            worksheet.set_column('P:P', 20)
            worksheet.set_column('Q:Q', 20)
            worksheet.set_column('R:R', 20)
            worksheet.set_column('S:S', 20)
            worksheet.set_column('T:T', 20)
            worksheet.set_column('U:U', 20)
            worksheet.set_column('V:V', 20)
            worksheet.set_column('W:W', 20)
            worksheet.set_column('X:X', 20)
            worksheet.set_column('Y:Y', 20)
            worksheet.set_column('Z:Z', 20)

            worksheet.set_column('AA:AA', 20)
            worksheet.set_column('AB:AB', 20)
            worksheet.set_column('AC:AC', 20)
            worksheet.set_column('AD:AD', 20)
            worksheet.set_column('AE:AE', 20)
            worksheet.set_column('AF:AF', 20)
            worksheet.set_column('AG:AG', 20)
            worksheet.set_column('AH:AH', 20)
            worksheet.set_column('AI:AI', 20)
            worksheet.set_column('AJ:AJ', 20)
            worksheet.set_column('AK:AK', 20)
            worksheet.set_column('AL:AL', 20)
            worksheet.set_column('AM:AM', 20)
            worksheet.set_column('AN:AN', 20)

            worksheet.merge_range('A1:E1', 'PERIOD OF SALES : ' + str(start_month) + ' ' + str(start_day) + 'th - '+ str(end_month) + ' ' + str(end_day) + 'th, ' + str(year), wbf['title_doc_brown'])
            worksheet.merge_range('A2:E2', 'DATA LAST STOCK : ' + str(end_month) + ' ' + str(end_day) + 'th, ' + str(year), wbf['title_doc_pink'])
            worksheet.merge_range('F1:AN1', '', wbf['title_doc'])
            worksheet.merge_range('F2:AN2', '', wbf['title_doc'])
            worksheet.merge_range('A3:M3', '', wbf['header'])

            worksheet.merge_range('N3:O3', 'SUMMARY TOTAL', wbf['header_orange'])
            worksheet.write(2,15, "WH", wbf['header_green'])
            worksheet.merge_range('Q3:R3', "FLAGSHIP", wbf['header_no'])
            worksheet.merge_range('S3:T3', "BATU BOLONG", wbf['header_no'])
            worksheet.merge_range('U3:V3', "BEACHWALK", wbf['header_no'])
            worksheet.merge_range('W3:X3', "BRAWA", wbf['header_no'])
            worksheet.merge_range('Y3:Z3', "PADANG", wbf['header_no'])
            worksheet.merge_range('AA3:AB3', "VILAGE", wbf['header_no'])
            worksheet.merge_range('AC3:AD3', "GALERIA", wbf['header_no'])
            worksheet.merge_range('AE3:AF3', "BATU BELIG", wbf['header_no'])
            worksheet.merge_range('AG3:AH3', "SANUR", wbf['header_no'])
            worksheet.merge_range('AI3:AJ3', "PETITENGET", wbf['header_no'])
            worksheet.merge_range('AK3:AL3', "KUTA", wbf['header_no'])
            worksheet.merge_range('AM3:AN3', "ONLINE STORE", wbf['header_no'])

            columns = [
                ('Class', 8, 'char', 'char'),
                ('Model', 20, 'char', 'char'),
                ('Category', 20, 'char', 'char'),
                ('Style', 60, 'char', 'char'),
                ('Stock Name', 38, 'char', 'char'),
                ('Stock ID', 8, 'char', 'char'),
                ('Color', 20, 'char', 'char'),
                ('Aging', 11, 'char', 'char'),
                ('Barcode', 15, 'char', 'char'),
                ('Size', 7, 'char', 'char'),
                ('Notes Order', 20, 'char', 'char'),
                ('Cost Price', 9, 'char', 'char'),
                ('Retail Price', 9, 'char', 'char'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
            ]

            row = 4
            col = 0
            for column in columns :
                column_name = column[0]
                column_width = column[1]
                column_type = column[2]
                bg_column = wbf['header_blue']
                if column_type == 'float':
                    bg_column = wbf['header_brown']
                elif column_type == 'float2':
                    bg_column = wbf['header_pink']
                worksheet.set_column(col,col,column_width)
                worksheet.write(row-1, col, column_name, bg_column)

                col += 1

            row += 1
            no = 1

            # domain_product = self.env['pos.order.line'].search(domain)



            domain = [
                ('type', '=', 'product'),
                # ('id', '=', 45263),
            ]

            if self.class_product_id and self.product_category_id:
                domain += [
                    ('class_product', '=', self.class_product_id.id),
                    ('product_category_categ_id', '=', self.product_category_id.id),
                ]
            elif self.class_product_id:
                domain += [('class_product', '=', self.class_product_id.id)]
            elif self.product_category_id:
                domain += [('product_category_categ_id', '=', self.product_category_id.id)]

            product_product = self.env['product.product'].with_context(to_date=self.end_period).search(domain)

            report_data = {}

            data_pos_orders = product_product.filtered(lambda x: not x.is_produk_diskon and not x.is_produk_promotion and not x.is_produk_promotion_free)

            for line in data_pos_orders:
                notes = ''
                # pickings = self.env['stock.picking'].browse(line.order_id.picking_ids.filtered(lambda x: x.state == 'done').ids)
                # for picking in pickings:
                #     notes = picking.date_done.strftime('%Y-%m-%d')
                incoming_qty = 0
                qty_received = 0
                purchase_count = 0
                purchase_list = []
                for move in self.env['stock.move'].search([
                        ('product_id', '=', line.id),
                        ('state', 'in', ['assigned','done']),
                        ('location_dest_id.usage', '=', 'internal'),
                        ('picking_id.purchase_id.date_planned', '>=', self.start_period),
                        ('picking_id.purchase_id.date_planned', '<=', self.end_period)]):
                    qty_received += move.product_uom_qty
                    purchase_list.append(move.picking_id.purchase_id.id)

                purchase_ids = self.env['purchase.order'].search([
                    ('id','in',purchase_list),
                    ('state','=','purchase'),
                    ],limit=10)
                purchase_count = len(purchase_ids)
                if qty_received > 0 and purchase_count > 1:
                    notes = self.end_period.strftime('%B') + ', ' + str(qty_received) + 'pcs'
                else:
                    for move in self.env['stock.move'].search([
                            ('product_id', '=', line.id),
                            ('state', '=', 'assigned'),
                            ('location_dest_id.usage', '=', 'internal'),
                            ('picking_id.purchase_id.date_planned', '<=', self.end_period)]):
                        incoming_qty += move.product_uom_qty

                    if incoming_qty > 0:
                        notes = 'just comming last week'

                list_color = ['COLOR', 'COLOUR', 'COLOURS', 'COLORS', 'WARNA', 'CORAK']
                list_size = ['SIZE', 'UKURAN']

                prod = line
                class_id = prod.class_product
                category = prod.product_model_categ_id
                parent_category = prod.product_category_categ_id
                stockname = prod.name
                stockid = prod.default_code
                color_size_ids = prod.product_template_variant_value_ids.mapped('display_name') or ''
                get_color = [c.split(': ')[1] for c in color_size_ids if any(attr in c for attr in list_color)]
                get_size = [s.split(': ')[1] for s in color_size_ids if any(attr in s for attr in list_size)]
                color = get_color[0] if get_color else ''
                size = get_size[0] if get_size else ''
                barcode = prod.barcode
                style = str(stockname) + '-' + str(color)
                cost_price = prod.standard_price
                retail_price = prod.lst_price
                # qty_sold = line.qty
                # qty_stock = prod.qty_available

                qty_sold_quantities = self.env['pos.order'].search([
                    ('picking_ids.move_lines.product_id', '=', prod.id),
                    ('date_order', '>=', self.start_period),
                    ('date_order', '<=', self.end_period),
                    ('picking_ids.state', 'in', ['assigned', 'done']),
                    ('picking_ids.location_id.warehouse_id.code', 'in', ('WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW',
                        'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG', 'BBSNR', 'BBPTG', 'BBKTA', 'Onlne'))
                ])

                qty_sold_per_warehouse = {
                    wh.code: sum(move.product_uom_qty for move in move_lines)
                                  for wh in self.env['stock.warehouse'].search([])
                                  for move_lines in qty_sold_quantities.picking_ids.move_lines
                                  if move_lines.location_id.warehouse_id.code == wh.code
                }

                total_qty_sold = sum(qty_sold_per_warehouse.values())

                # stock_quant = self.env['stock.quant'].sudo().search([
                #             ('location_id.usage', '=', 'internal'),
                #             ('name_warehouse_id.code', 'in', ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Online')),
                #             ('product_id.categ_id', '=', category.id),
                #         ])
                # qty_stock = 0
                # for quant in stock_quant:
                #     qty_stock += quant.quantity

                # qty_stock = sum(line.product_id.stock_quant_ids.filtered(lambda x: x.location_id.usage == 'internal' and x.location_id.warehouse_id.code in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Online') and x.in_date.date() >= self.start_period and x.in_date.date() <= self.end_period).mapped('quantity'))
                # qty_stock = sum(line.product_id.qty_available for line in lines)
                # qty_stock = sum(line.product_id.product_tmpl_id.qty_available for line in lines)

                warehouse_quantities = line.stock_quant_ids.filtered(
                    lambda x: x.location_id.usage == 'internal' and
                              x.location_id.warehouse_id.code in (
                              'WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW', 'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG', 'BBSNR',
                              'BBPTG', 'BBKTA', 'Onlne')
                )

                # qty_stock = sum(warehouse_quantities.mapped('quantity'))
                # warehouse = set(warehouse_quantities.mapped('location_id.warehouse_id'))
                # warehouse_list = list(warehouse)
                qty_stock_per_warehouse = {wh.code: sum(
                    quant.quantity for quant in warehouse_quantities if quant.location_id.warehouse_id.code == wh.code)
                                     for wh in set(warehouse_quantities.mapped('location_id.warehouse_id'))}

                total_qty_stock = sum(qty_stock_per_warehouse.values())
                if total_qty_stock == 0 and total_qty_sold == 0:
                    continue
                # total_qty_sold += qty_sold

                # warehouse = line.order_id.picking_type_id.warehouse_id
                # age = int((fields.Date.today() - line.order_id.date_order.date()).days / 7)
                today = datetime.now()
                moves = sorted(line.stock_move_ids.filtered(lambda x: x.picking_type_id.code == 'incoming' and x.state == 'done' and x.product_id == prod), key=lambda x: x.date)
                # age_in_weeks = ((today - moves[0].date).days) // 7 if moves else 0
                age_in_weeks = ceil(((today - moves[0].date).days) / 7) if moves else 0
                age = int(age_in_weeks)

                # create keys for the report_data dictionary
                key = (class_id.id, parent_category.id, category.id, prod.id, color, size)

                # create dictionary entry for product if it does not exist
                if key not in report_data:
                    report_data[key] = {
                        'class_name': class_id.name,
                        'parent_category': parent_category.name,
                        'category': category.name,
                        'style': style,
                        'stockname': stockname,
                        'stockid': stockid,
                        'color': color,
                        'barcode': barcode,
                        'size': size,
                        'notes': notes,
                        'cost_price': cost_price,
                        'retail_price': retail_price,
                        'total_qty_sold': 0,
                        'total_qty_stock': 0,
                        'qty_sold': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                        'qty_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                        'age': age,
                    }

                # warehouse_key = warehouse.code
                for warehouse_key, quantity_stock in qty_stock_per_warehouse.items():
                    if warehouse_key in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Onlne'):
                        report_data[key]['total_qty_stock'] = total_qty_stock
                        report_data[key]['qty_stock'][warehouse_key] = quantity_stock

                for warehouse_key, quantity_sold in qty_sold_per_warehouse.items():
                    if warehouse_key in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Onlne'):
                        report_data[key]['total_qty_sold'] = total_qty_sold
                        report_data[key]['qty_sold'][warehouse_key] = quantity_sold


            rows = []
            for data in report_data.values():
                row = [data['class_name'],
                       data['parent_category'],
                       data['category'],
                       data['style'],
                       data['stockname'],
                       data['stockid'],
                       data['color'],
                       data['barcode'],
                       data['size'],
                       data['notes'],
                       data['cost_price'],
                       data['retail_price'],
                       data['total_qty_sold'],
                       data['total_qty_stock'],
                       data['qty_sold']['WHBB'],
                       data['qty_sold']['BBFLG'],
                       data['qty_sold']['BBBBG'],
                       data['qty_sold']['BBBWK'],
                       data['qty_sold']['BBBRW'],
                       data['qty_sold']['BBPDG'],
                       data['qty_sold']['BBSYV'],
                       data['qty_sold']['BBGLR'],
                       data['qty_sold']['BBBLG'],
                       data['qty_sold']['BBSNR'],
                       data['qty_sold']['BBPTG'],
                       data['qty_sold']['BBKTA'],
                       data['qty_sold']['Online'],
                       data['qty_stock']['WHBB'],
                       data['qty_stock']['BBFLG'],
                       data['qty_stock']['BBBBG'],
                       data['qty_stock']['BBBWK'],
                       data['qty_stock']['BBBRW'],
                       data['qty_stock']['BBPDG'],
                       data['qty_stock']['BBSYV'],
                       data['qty_stock']['BBGLR'],
                       data['qty_stock']['BBBLG'],
                       data['qty_stock']['BBSNR'],
                       data['qty_stock']['BBPTG'],
                       data['qty_stock']['BBKTA'],
                       data['qty_stock']['Online'],
                       data['age']]
                rows.append(row)

            grouped_colors = {}

            for data in report_data.values():
                class_name = data['class_name']
                parent_category = data['parent_category']
                category = data['category']
                style = data['style']
                stockname = data['stockname']
                stockid = data['stockid']
                color = data['color']
                barcode = data['barcode']
                size = data['size']
                notes = data['notes']
                cost_price = data['cost_price']
                retail_price = data['retail_price']
                total_qty_sold = data['total_qty_sold']
                total_qty_stock = data['total_qty_stock']
                whbb_qty_sold = data['qty_sold']['WHBB']
                bbflg_qty_sold = data['qty_sold']['BBFLG']
                bbbbg_qty_sold = data['qty_sold']['BBBBG']
                bbbwk_qty_sold = data['qty_sold']['BBBWK']
                bbbrw_qty_sold = data['qty_sold']['BBBRW']
                bbpdg_qty_sold = data['qty_sold']['BBPDG']
                bbsyv_qty_sold = data['qty_sold']['BBSYV']
                bbglr_qty_sold = data['qty_sold']['BBGLR']
                bbblg_qty_sold = data['qty_sold']['BBBLG']
                bbsnr_qty_sold = data['qty_sold']['BBSNR']
                bbptg_qty_sold = data['qty_sold']['BBPTG']
                bbkta_qty_sold = data['qty_sold']['BBKTA']
                online_qty_sold = data['qty_sold']['Online']
                whbb_qty_stock = data['qty_stock']['WHBB']
                bbflg_qty_stock = data['qty_stock']['BBFLG']
                bbbbg_qty_stock = data['qty_stock']['BBBBG']
                bbbwk_qty_stock = data['qty_stock']['BBBWK']
                bbbrw_qty_stock = data['qty_stock']['BBBRW']
                bbpdg_qty_stock = data['qty_stock']['BBPDG']
                bbsyv_qty_stock = data['qty_stock']['BBSYV']
                bbglr_qty_stock = data['qty_stock']['BBGLR']
                bbblg_qty_stock = data['qty_stock']['BBBLG']
                bbsnr_qty_stock = data['qty_stock']['BBSNR']
                bbptg_qty_stock = data['qty_stock']['BBPTG']
                bbkta_qty_stock = data['qty_stock']['BBKTA']
                online_qty_stock = data['qty_stock']['Online']
                age = data['age']

                key = (class_name, parent_category, category, style, stockname, color)

                if key not in grouped_colors:
                    grouped_colors[key] = {
                        'class_name': class_name,
                        'parent_category': parent_category,
                        'category': category,
                        'style': style,
                        'stockname': stockname,
                        'color': color,
                        'stockid': stockid,
                        'total_qty_sold': total_qty_sold,
                        'total_qty_stock': total_qty_stock,
                        'whbb_qty_sold': whbb_qty_sold,
                        'bbflg_qty_sold': bbflg_qty_sold,
                        'bbbbg_qty_sold': bbbbg_qty_sold,
                        'bbbwk_qty_sold': bbbwk_qty_sold,
                        'bbbrw_qty_sold': bbbrw_qty_sold,
                        'bbpdg_qty_sold': bbpdg_qty_sold,
                        'bbsyv_qty_sold': bbsyv_qty_sold,
                        'bbglr_qty_sold': bbglr_qty_sold,
                        'bbblg_qty_sold': bbblg_qty_sold,
                        'bbsnr_qty_sold': bbsnr_qty_sold,
                        'bbptg_qty_sold': bbptg_qty_sold,
                        'bbkta_qty_sold': bbkta_qty_sold,
                        'online_qty_sold': online_qty_sold,
                        'whbb_qty_stock': whbb_qty_stock,
                        'bbflg_qty_stock': bbflg_qty_stock,
                        'bbbbg_qty_stock': bbbbg_qty_stock,
                        'bbbwk_qty_stock': bbbwk_qty_stock,
                        'bbbrw_qty_stock': bbbrw_qty_stock,
                        'bbpdg_qty_stock': bbpdg_qty_stock,
                        'bbsyv_qty_stock': bbsyv_qty_stock,
                        'bbglr_qty_stock': bbglr_qty_stock,
                        'bbblg_qty_stock': bbblg_qty_stock,
                        'bbsnr_qty_stock': bbsnr_qty_stock,
                        'bbptg_qty_stock': bbptg_qty_stock,
                        'bbkta_qty_stock': bbkta_qty_stock,
                        'online_qty_stock': online_qty_stock,
                        'children': {}
                    }

                else:
                    grouped_colors[key]['total_qty_sold'] += total_qty_sold
                    grouped_colors[key]['total_qty_stock'] += total_qty_stock
                    grouped_colors[key]['whbb_qty_sold'] += whbb_qty_sold
                    grouped_colors[key]['bbflg_qty_sold'] += bbflg_qty_sold
                    grouped_colors[key]['bbbbg_qty_sold'] += bbbbg_qty_sold
                    grouped_colors[key]['bbbwk_qty_sold'] += bbbwk_qty_sold
                    grouped_colors[key]['bbbrw_qty_sold'] += bbbrw_qty_sold
                    grouped_colors[key]['bbpdg_qty_sold'] += bbpdg_qty_sold
                    grouped_colors[key]['bbsyv_qty_sold'] += bbsyv_qty_sold
                    grouped_colors[key]['bbglr_qty_sold'] += bbglr_qty_sold
                    grouped_colors[key]['bbblg_qty_sold'] += bbblg_qty_sold
                    grouped_colors[key]['bbsnr_qty_sold'] += bbsnr_qty_sold
                    grouped_colors[key]['bbptg_qty_sold'] += bbptg_qty_sold
                    grouped_colors[key]['bbkta_qty_sold'] += bbkta_qty_sold
                    grouped_colors[key]['online_qty_sold'] += online_qty_sold
                    grouped_colors[key]['whbb_qty_stock'] += whbb_qty_stock
                    grouped_colors[key]['bbflg_qty_stock'] += bbflg_qty_stock
                    grouped_colors[key]['bbbbg_qty_stock'] += bbbbg_qty_stock
                    grouped_colors[key]['bbbwk_qty_stock'] += bbbwk_qty_stock
                    grouped_colors[key]['bbbrw_qty_stock'] += bbbrw_qty_stock
                    grouped_colors[key]['bbpdg_qty_stock'] += bbpdg_qty_stock
                    grouped_colors[key]['bbsyv_qty_stock'] += bbsyv_qty_stock
                    grouped_colors[key]['bbglr_qty_stock'] += bbglr_qty_stock
                    grouped_colors[key]['bbblg_qty_stock'] += bbblg_qty_stock
                    grouped_colors[key]['bbsnr_qty_stock'] += bbsnr_qty_stock
                    grouped_colors[key]['bbptg_qty_stock'] += bbptg_qty_stock
                    grouped_colors[key]['bbkta_qty_stock'] += bbkta_qty_stock
                    grouped_colors[key]['online_qty_stock'] += online_qty_stock


                category_data = grouped_colors[key]

                if size not in grouped_colors[key]['children']:
                    grouped_colors[key]['children'][size] = {
                        'notes': notes,
                        'barcode': barcode,
                        'cost_price': cost_price,
                        'retail_price': retail_price,
                        'total_qty_sold': total_qty_sold,
                        'total_qty_stock': total_qty_stock,
                        'whbb_qty_sold': whbb_qty_sold,
                        'bbflg_qty_sold': bbflg_qty_sold,
                        'bbbbg_qty_sold': bbbbg_qty_sold,
                        'bbbwk_qty_sold': bbbwk_qty_sold,
                        'bbbrw_qty_sold': bbbrw_qty_sold,
                        'bbpdg_qty_sold': bbpdg_qty_sold,
                        'bbsyv_qty_sold': bbsyv_qty_sold,
                        'bbglr_qty_sold': bbglr_qty_sold,
                        'bbblg_qty_sold': bbblg_qty_sold,
                        'bbsnr_qty_sold': bbsnr_qty_sold,
                        'bbptg_qty_sold': bbptg_qty_sold,
                        'bbkta_qty_sold': bbkta_qty_sold,
                        'online_qty_sold': online_qty_sold,
                        'whbb_qty_stock': whbb_qty_stock,
                        'bbflg_qty_stock': bbflg_qty_stock,
                        'bbbbg_qty_stock': bbbbg_qty_stock,
                        'bbbwk_qty_stock': bbbwk_qty_stock,
                        'bbbrw_qty_stock': bbbrw_qty_stock,
                        'bbpdg_qty_stock': bbpdg_qty_stock,
                        'bbsyv_qty_stock': bbsyv_qty_stock,
                        'bbglr_qty_stock': bbglr_qty_stock,
                        'bbblg_qty_stock': bbblg_qty_stock,
                        'bbsnr_qty_stock': bbsnr_qty_stock,
                        'bbptg_qty_stock': bbptg_qty_stock,
                        'bbkta_qty_stock': bbkta_qty_stock,
                        'online_qty_stock': online_qty_stock,
                        'age': age,
                    }
                else:
                    grouped_colors[key]['total_qty_sold'] += total_qty_sold
                    grouped_colors[key]['total_qty_stock'] += total_qty_stock
                    grouped_colors[key]['whbb_qty_sold'] += whbb_qty_sold
                    grouped_colors[key]['bbflg_qty_sold'] += bbflg_qty_sold
                    grouped_colors[key]['bbbbg_qty_sold'] += bbbbg_qty_sold
                    grouped_colors[key]['bbbwk_qty_sold'] += bbbwk_qty_sold
                    grouped_colors[key]['bbbrw_qty_sold'] += bbbrw_qty_sold
                    grouped_colors[key]['bbpdg_qty_sold'] += bbpdg_qty_sold
                    grouped_colors[key]['bbsyv_qty_sold'] += bbsyv_qty_sold
                    grouped_colors[key]['bbglr_qty_sold'] += bbglr_qty_sold
                    grouped_colors[key]['bbblg_qty_sold'] += bbblg_qty_sold
                    grouped_colors[key]['bbsnr_qty_sold'] += bbsnr_qty_sold
                    grouped_colors[key]['bbptg_qty_sold'] += bbptg_qty_sold
                    grouped_colors[key]['bbkta_qty_sold'] += bbkta_qty_sold
                    grouped_colors[key]['online_qty_sold'] += online_qty_sold
                    grouped_colors[key]['whbb_qty_stock'] += whbb_qty_stock
                    grouped_colors[key]['bbflg_qty_stock'] += bbflg_qty_stock
                    grouped_colors[key]['bbbbg_qty_stock'] += bbbbg_qty_stock
                    grouped_colors[key]['bbbwk_qty_stock'] += bbbwk_qty_stock
                    grouped_colors[key]['bbbrw_qty_stock'] += bbbrw_qty_stock
                    grouped_colors[key]['bbpdg_qty_stock'] += bbpdg_qty_stock
                    grouped_colors[key]['bbsyv_qty_stock'] += bbsyv_qty_stock
                    grouped_colors[key]['bbglr_qty_stock'] += bbglr_qty_stock
                    grouped_colors[key]['bbblg_qty_stock'] += bbblg_qty_stock
                    grouped_colors[key]['bbsnr_qty_stock'] += bbsnr_qty_stock
                    grouped_colors[key]['bbptg_qty_stock'] += bbptg_qty_stock
                    grouped_colors[key]['bbkta_qty_stock'] += bbkta_qty_stock
                    grouped_colors[key]['online_qty_stock'] += online_qty_stock


            grouped_class = {}
            for data_class in grouped_colors.values():
                cl_class_name = data_class['class_name']
                cl_parent_category = data_class['parent_category']
                cl_category = data_class['category']
                cl_style = data_class['style']
                cl_stockname = data_class['stockname']
                cl_color = data_class['color']
                cl_stockid = data_class['stockid']
                cl_total_qty_sold = data_class['total_qty_sold']
                cl_total_qty_stock = data_class['total_qty_stock']
                cl_whbb_qty_sold = data_class['whbb_qty_sold']
                cl_bbflg_qty_sold = data_class['bbflg_qty_sold']
                cl_bbbbg_qty_sold = data_class['bbbbg_qty_sold']
                cl_bbbwk_qty_sold = data_class['bbbwk_qty_sold']
                cl_bbbrw_qty_sold = data_class['bbbrw_qty_sold']
                cl_bbpdg_qty_sold = data_class['bbpdg_qty_sold']
                cl_bbsyv_qty_sold = data_class['bbsyv_qty_sold']
                cl_bbglr_qty_sold = data_class['bbglr_qty_sold']
                cl_bbblg_qty_sold = data_class['bbblg_qty_sold']
                cl_bbsnr_qty_sold = data_class['bbsnr_qty_sold']
                cl_bbptg_qty_sold = data_class['bbptg_qty_sold']
                cl_bbkta_qty_sold = data_class['bbkta_qty_sold']
                cl_online_qty_sold = data_class['online_qty_sold']
                cl_whbb_qty_stock = data_class['whbb_qty_stock']
                cl_bbflg_qty_stock = data_class['bbflg_qty_stock']
                cl_bbbbg_qty_stock = data_class['bbbbg_qty_stock']
                cl_bbbwk_qty_stock = data_class['bbbwk_qty_stock']
                cl_bbbrw_qty_stock = data_class['bbbrw_qty_stock']
                cl_bbpdg_qty_stock = data_class['bbpdg_qty_stock']
                cl_bbsyv_qty_stock = data_class['bbsyv_qty_stock']
                cl_bbglr_qty_stock = data_class['bbglr_qty_stock']
                cl_bbblg_qty_stock = data_class['bbblg_qty_stock']
                cl_bbsnr_qty_stock = data_class['bbsnr_qty_stock']
                cl_bbptg_qty_stock = data_class['bbptg_qty_stock']
                cl_bbkta_qty_stock = data_class['bbkta_qty_stock']
                cl_online_qty_stock = data_class['online_qty_stock']
                cl_children = data_class['children']

                key = cl_class_name

                if key not in grouped_class:
                    grouped_class[key] = {
                        'class_name': cl_class_name,
                        'total_qty_sold': cl_total_qty_sold,
                        'total_qty_stock': cl_total_qty_stock,
                        'whbb_qty_sold': cl_whbb_qty_sold,
                        'bbflg_qty_sold': cl_bbflg_qty_sold,
                        'bbbbg_qty_sold': cl_bbbbg_qty_sold,
                        'bbbwk_qty_sold': cl_bbbwk_qty_sold,
                        'bbbrw_qty_sold': cl_bbbrw_qty_sold,
                        'bbpdg_qty_sold': cl_bbpdg_qty_sold,
                        'bbsyv_qty_sold': cl_bbsyv_qty_sold,
                        'bbglr_qty_sold': cl_bbglr_qty_sold,
                        'bbblg_qty_sold': cl_bbblg_qty_sold,
                        'bbsnr_qty_sold': cl_bbsnr_qty_sold,
                        'bbptg_qty_sold': cl_bbptg_qty_sold,
                        'bbkta_qty_sold': cl_bbkta_qty_sold,
                        'online_qty_sold': cl_online_qty_sold,
                        'whbb_qty_stock': cl_whbb_qty_stock,
                        'bbflg_qty_stock': cl_bbflg_qty_stock,
                        'bbbbg_qty_stock': cl_bbbbg_qty_stock,
                        'bbbwk_qty_stock': cl_bbbwk_qty_stock,
                        'bbbrw_qty_stock': cl_bbbrw_qty_stock,
                        'bbpdg_qty_stock': cl_bbpdg_qty_stock,
                        'bbsyv_qty_stock': cl_bbsyv_qty_stock,
                        'bbglr_qty_stock': cl_bbglr_qty_stock,
                        'bbblg_qty_stock': cl_bbblg_qty_stock,
                        'bbsnr_qty_stock': cl_bbsnr_qty_stock,
                        'bbptg_qty_stock': cl_bbptg_qty_stock,
                        'bbkta_qty_stock': cl_bbkta_qty_stock,
                        'online_qty_stock': cl_online_qty_stock,
                        'children_category': {},
                    }
                else:
                    grouped_class[key]['total_qty_sold'] += cl_total_qty_sold
                    grouped_class[key]['total_qty_stock'] += cl_total_qty_stock
                    grouped_class[key]['whbb_qty_sold'] += cl_whbb_qty_sold
                    grouped_class[key]['bbflg_qty_sold'] += cl_bbflg_qty_sold
                    grouped_class[key]['bbbbg_qty_sold'] += cl_bbbbg_qty_sold
                    grouped_class[key]['bbbwk_qty_sold'] += cl_bbbwk_qty_sold
                    grouped_class[key]['bbbrw_qty_sold'] += cl_bbbrw_qty_sold
                    grouped_class[key]['bbpdg_qty_sold'] += cl_bbpdg_qty_sold
                    grouped_class[key]['bbsyv_qty_sold'] += cl_bbsyv_qty_sold
                    grouped_class[key]['bbglr_qty_sold'] += cl_bbglr_qty_sold
                    grouped_class[key]['bbblg_qty_sold'] += cl_bbblg_qty_sold
                    grouped_class[key]['bbsnr_qty_sold'] += cl_bbsnr_qty_sold
                    grouped_class[key]['bbptg_qty_sold'] += cl_bbptg_qty_sold
                    grouped_class[key]['bbkta_qty_sold'] += cl_bbkta_qty_sold
                    grouped_class[key]['online_qty_sold'] += cl_online_qty_sold
                    grouped_class[key]['whbb_qty_stock'] += cl_whbb_qty_stock
                    grouped_class[key]['bbflg_qty_stock'] += cl_bbflg_qty_stock
                    grouped_class[key]['bbbbg_qty_stock'] += cl_bbbbg_qty_stock
                    grouped_class[key]['bbbwk_qty_stock'] += cl_bbbwk_qty_stock
                    grouped_class[key]['bbbrw_qty_stock'] += cl_bbbrw_qty_stock
                    grouped_class[key]['bbpdg_qty_stock'] += cl_bbpdg_qty_stock
                    grouped_class[key]['bbsyv_qty_stock'] += cl_bbsyv_qty_stock
                    grouped_class[key]['bbglr_qty_stock'] += cl_bbglr_qty_stock
                    grouped_class[key]['bbblg_qty_stock'] += cl_bbblg_qty_stock
                    grouped_class[key]['bbsnr_qty_stock'] += cl_bbsnr_qty_stock
                    grouped_class[key]['bbptg_qty_stock'] += cl_bbptg_qty_stock
                    grouped_class[key]['bbkta_qty_stock'] += cl_bbkta_qty_stock
                    grouped_class[key]['online_qty_stock'] += cl_online_qty_stock

                category_data = grouped_class[key]
                subkey = (cl_parent_category, cl_category, cl_style, cl_stockname, cl_color)

                if subkey not in grouped_class[key]['children_category']:
                    grouped_class[key]['children_category'][subkey] = {
                        'class_name': cl_class_name,
                        'parent_category': cl_parent_category,
                        'category': cl_category,
                        'style': cl_style,
                        'stockname': cl_stockname,
                        'color': cl_color,
                        'stockid': cl_stockid,
                        # 'notes': cl_notes,
                        # 'barcode': cl_barcode,
                        # 'cost_price': cl_cost_price,
                        # 'retail_price': cl_retail_price,
                        'total_qty_sold': cl_total_qty_sold,
                        'total_qty_stock': cl_total_qty_stock,
                        'whbb_qty_sold': cl_whbb_qty_sold,
                        'bbflg_qty_sold': cl_bbflg_qty_sold,
                        'bbbbg_qty_sold': cl_bbbbg_qty_sold,
                        'bbbwk_qty_sold': cl_bbbwk_qty_sold,
                        'bbbrw_qty_sold': cl_bbbrw_qty_sold,
                        'bbpdg_qty_sold': cl_bbpdg_qty_sold,
                        'bbsyv_qty_sold': cl_bbsyv_qty_sold,
                        'bbglr_qty_sold': cl_bbglr_qty_sold,
                        'bbblg_qty_sold': cl_bbblg_qty_sold,
                        'bbsnr_qty_sold': cl_bbsnr_qty_sold,
                        'bbptg_qty_sold': cl_bbptg_qty_sold,
                        'bbkta_qty_sold': cl_bbkta_qty_sold,
                        'online_qty_sold': cl_online_qty_sold,
                        'whbb_qty_stock': cl_whbb_qty_stock,
                        'bbflg_qty_stock': cl_bbflg_qty_stock,
                        'bbbbg_qty_stock': cl_bbbbg_qty_stock,
                        'bbbwk_qty_stock': cl_bbbwk_qty_stock,
                        'bbbrw_qty_stock': cl_bbbrw_qty_stock,
                        'bbpdg_qty_stock': cl_bbpdg_qty_stock,
                        'bbsyv_qty_stock': cl_bbsyv_qty_stock,
                        'bbglr_qty_stock': cl_bbglr_qty_stock,
                        'bbblg_qty_stock': cl_bbblg_qty_stock,
                        'bbsnr_qty_stock': cl_bbsnr_qty_stock,
                        'bbptg_qty_stock': cl_bbptg_qty_stock,
                        'bbkta_qty_stock': cl_bbkta_qty_stock,
                        'online_qty_stock': cl_online_qty_stock,
                        # 'age': cl_age,
                        'children': cl_children,
                    }

            # Print the result
            row = 4
            gt_total_qty_sold = 0
            gt_total_qty_stock = 0
            gt_whbb_qty_sold = 0
            gt_bbflg_qty_sold = 0
            gt_bbbbg_qty_sold = 0
            gt_bbbwk_qty_sold = 0
            gt_bbbrw_qty_sold = 0
            gt_bbpdg_qty_sold = 0
            gt_bbsyv_qty_sold = 0
            gt_bbglr_qty_sold = 0
            gt_bbblg_qty_sold = 0
            gt_bbsnr_qty_sold = 0
            gt_bbptg_qty_sold = 0
            gt_bbkta_qty_sold = 0
            gt_online_qty_sold = 0
            gt_whbb_qty_stock = 0
            gt_bbflg_qty_stock = 0
            gt_bbbbg_qty_stock = 0
            gt_bbbwk_qty_stock = 0
            gt_bbbrw_qty_stock = 0
            gt_bbpdg_qty_stock = 0
            gt_bbsyv_qty_stock = 0
            gt_bbglr_qty_stock = 0
            gt_bbblg_qty_stock = 0
            gt_bbsnr_qty_stock = 0
            gt_bbptg_qty_stock = 0
            gt_bbkta_qty_stock = 0
            gt_online_qty_stock = 0

            for key, value in grouped_class.items():
                children_category = value['children_category']

                cl_class_name = value['class_name']
                cl_total_qty_sold = value['total_qty_sold']
                cl_total_qty_stock = value['total_qty_stock']
                cl_whbb_qty_sold = value['whbb_qty_sold']
                cl_bbflg_qty_sold = value['bbflg_qty_sold']
                cl_bbbbg_qty_sold = value['bbbbg_qty_sold']
                cl_bbbwk_qty_sold = value['bbbwk_qty_sold']
                cl_bbbrw_qty_sold = value['bbbrw_qty_sold']
                cl_bbpdg_qty_sold = value['bbpdg_qty_sold']
                cl_bbsyv_qty_sold = value['bbsyv_qty_sold']
                cl_bbglr_qty_sold = value['bbglr_qty_sold']
                cl_bbblg_qty_sold = value['bbblg_qty_sold']
                cl_bbsnr_qty_sold = value['bbsnr_qty_sold']
                cl_bbptg_qty_sold = value['bbptg_qty_sold']
                cl_bbkta_qty_sold = value['bbkta_qty_sold']
                cl_online_qty_sold = value['online_qty_sold']
                cl_whbb_qty_stock = value['whbb_qty_stock']
                cl_bbflg_qty_stock = value['bbflg_qty_stock']
                cl_bbbbg_qty_stock = value['bbbbg_qty_stock']
                cl_bbbwk_qty_stock = value['bbbwk_qty_stock']
                cl_bbbrw_qty_stock = value['bbbrw_qty_stock']
                cl_bbpdg_qty_stock = value['bbpdg_qty_stock']
                cl_bbsyv_qty_stock = value['bbsyv_qty_stock']
                cl_bbglr_qty_stock = value['bbglr_qty_stock']
                cl_bbblg_qty_stock = value['bbblg_qty_stock']
                cl_bbsnr_qty_stock = value['bbsnr_qty_stock']
                cl_bbptg_qty_stock = value['bbptg_qty_stock']
                cl_bbkta_qty_stock = value['bbkta_qty_stock']
                cl_online_qty_stock = value['online_qty_stock']
                
                for subkey, categ_value in children_category.items():

                    parent_category, category, style, stockname, color = subkey
                    # class_name, parent_category, category = key

                    total_qty_sold, total_qty_stock, whbb_qty_sold, bbflg_qty_sold, bbbbg_qty_sold, bbbwk_qty_sold, bbbrw_qty_sold, bbpdg_qty_sold, bbsyv_qty_sold, bbglr_qty_sold, bbblg_qty_sold, bbsnr_qty_sold, bbptg_qty_sold, bbkta_qty_sold, online_qty_sold, whbb_qty_stock, bbflg_qty_stock, bbbbg_qty_stock, bbbwk_qty_stock, bbbrw_qty_stock, bbpdg_qty_stock, bbsyv_qty_stock, bbglr_qty_stock, bbblg_qty_stock, bbsnr_qty_stock, bbptg_qty_stock, bbkta_qty_stock, online_qty_stock = \
                    categ_value['total_qty_sold'], categ_value['total_qty_stock'], categ_value['whbb_qty_sold'], categ_value['bbflg_qty_sold'], \
                    categ_value['bbbbg_qty_sold'], categ_value['bbbwk_qty_sold'], categ_value['bbbrw_qty_sold'], categ_value['bbpdg_qty_sold'], \
                    categ_value['bbsyv_qty_sold'], categ_value['bbglr_qty_sold'], categ_value['bbblg_qty_sold'], categ_value['bbsnr_qty_sold'], \
                    categ_value['bbptg_qty_sold'], categ_value['bbkta_qty_sold'], categ_value['online_qty_sold'], categ_value['whbb_qty_stock'], \
                    categ_value['bbflg_qty_stock'], categ_value['bbbbg_qty_stock'], categ_value['bbbwk_qty_stock'], categ_value[
                        'bbbrw_qty_stock'], categ_value['bbpdg_qty_stock'], categ_value['bbsyv_qty_stock'], categ_value[
                        'bbglr_qty_stock'], categ_value['bbblg_qty_stock'], categ_value['bbsnr_qty_stock'], categ_value[
                        'bbptg_qty_stock'], categ_value['bbkta_qty_stock'], categ_value['online_qty_stock']
                    qty_sold_total = whbb_qty_sold + bbflg_qty_sold + bbbbg_qty_sold + bbbwk_qty_sold + bbbrw_qty_sold + bbpdg_qty_sold + bbsyv_qty_sold + bbglr_qty_sold + bbblg_qty_sold + bbsnr_qty_sold + bbptg_qty_sold + bbkta_qty_sold + online_qty_sold
                    qty_stock_total = whbb_qty_stock + bbflg_qty_stock + bbbbg_qty_stock + bbbwk_qty_stock + bbbrw_qty_stock + bbpdg_qty_stock + bbsyv_qty_stock + bbglr_qty_stock + bbblg_qty_stock + bbsnr_qty_stock + bbptg_qty_stock + bbkta_qty_stock + online_qty_stock

                    dt_class_name = categ_value['class_name']
                    dt_parent_category = parent_category
                    dt_category = category
                    dt_style = str(style) + ' Total'
                    dt_total_qty_sold = total_qty_sold
                    dt_total_qty_stock = total_qty_stock
                    dt_whbb_qty_sold = whbb_qty_sold
                    dt_bbflg_qty_sold = bbflg_qty_sold
                    dt_bbbbg_qty_sold = bbbbg_qty_sold
                    dt_bbbwk_qty_sold = bbbwk_qty_sold
                    dt_bbbrw_qty_sold = bbbrw_qty_sold
                    dt_bbpdg_qty_sold = bbpdg_qty_sold
                    dt_bbsyv_qty_sold = bbsyv_qty_sold
                    dt_bbglr_qty_sold = bbglr_qty_sold
                    dt_bbblg_qty_sold = bbblg_qty_sold
                    dt_bbsnr_qty_sold = bbsnr_qty_sold
                    dt_bbptg_qty_sold = bbptg_qty_sold
                    dt_bbkta_qty_sold = bbkta_qty_sold
                    dt_online_qty_sold = online_qty_sold
                    dt_whbb_qty_stock = whbb_qty_stock
                    dt_bbflg_qty_stock = bbflg_qty_stock
                    dt_bbbbg_qty_stock = bbbbg_qty_stock
                    dt_bbbwk_qty_stock = bbbwk_qty_stock
                    dt_bbbrw_qty_stock = bbbrw_qty_stock
                    dt_bbpdg_qty_stock = bbpdg_qty_stock
                    dt_bbsyv_qty_stock = bbsyv_qty_stock
                    dt_bbglr_qty_stock = bbglr_qty_stock
                    dt_bbblg_qty_stock = bbblg_qty_stock
                    dt_bbsnr_qty_stock = bbsnr_qty_stock
                    dt_bbptg_qty_stock = bbptg_qty_stock
                    dt_bbkta_qty_stock = bbkta_qty_stock
                    dt_online_qty_stock = online_qty_stock
                    children = categ_value['children']

                    for size, size_value in children.items():
                        d_class_name = categ_value['class_name']
                        d_parent_category = categ_value['parent_category']
                        d_category = categ_value['category']
                        d_style = categ_value['style']
                        d_stockname = categ_value['stockname']
                        d_stockid = categ_value['stockid']
                        d_color = categ_value['color']
                        d_age = size_value['age']
                        d_barcode = size_value['barcode']
                        d_size = size
                        d_notes = size_value['notes']
                        d_cost_price = size_value['cost_price']
                        d_retail_price = size_value['retail_price']
                        d_total_qty_sold = size_value['total_qty_sold']
                        d_total_qty_stock = size_value['total_qty_stock']
                        d_whbb_qty_sold = size_value['whbb_qty_sold']
                        d_bbflg_qty_sold = size_value['bbflg_qty_sold']
                        d_bbbbg_qty_sold = size_value['bbbbg_qty_sold']
                        d_bbbwk_qty_sold = size_value['bbbwk_qty_sold']
                        d_bbbrw_qty_sold = size_value['bbbrw_qty_sold']
                        d_bbpdg_qty_sold = size_value['bbpdg_qty_sold']
                        d_bbsyv_qty_sold = size_value['bbsyv_qty_sold']
                        d_bbglr_qty_sold = size_value['bbglr_qty_sold']
                        d_bbblg_qty_sold = size_value['bbblg_qty_sold']
                        d_bbsnr_qty_sold = size_value['bbsnr_qty_sold']
                        d_bbptg_qty_sold = size_value['bbptg_qty_sold']
                        d_bbkta_qty_sold = size_value['bbkta_qty_sold']
                        d_online_qty_sold = size_value['online_qty_sold']
                        d_whbb_qty_stock = size_value['whbb_qty_stock']
                        d_bbflg_qty_stock = size_value['bbflg_qty_stock']
                        d_bbbbg_qty_stock = size_value['bbbbg_qty_stock']
                        d_bbbwk_qty_stock = size_value['bbbwk_qty_stock']
                        d_bbbrw_qty_stock = size_value['bbbrw_qty_stock']
                        d_bbpdg_qty_stock = size_value['bbpdg_qty_stock']
                        d_bbsyv_qty_stock = size_value['bbsyv_qty_stock']
                        d_bbglr_qty_stock = size_value['bbglr_qty_stock']
                        d_bbblg_qty_stock = size_value['bbblg_qty_stock']
                        d_bbsnr_qty_stock = size_value['bbsnr_qty_stock']
                        d_bbptg_qty_stock = size_value['bbptg_qty_stock']
                        d_bbkta_qty_stock = size_value['bbkta_qty_stock']
                        d_online_qty_stock = size_value['online_qty_stock']

                        worksheet.write(row, 0, d_class_name or ' ', wbf['content'])
                        worksheet.write(row, 1, d_category or ' ', wbf['content'])
                        worksheet.write(row, 2, d_parent_category or ' ', wbf['content'])
                        worksheet.write(row, 3, d_style or ' ', wbf['content'])
                        worksheet.write(row, 4, d_stockname or ' ', wbf['content'])
                        worksheet.write(row, 5, d_stockid or ' ', wbf['content'])
                        worksheet.write(row, 6, d_color or ' ', wbf['content'])
                        worksheet.write(row, 7, d_age or ' ', wbf['content2'])
                        worksheet.write(row, 8, d_barcode or ' ', wbf['content'])
                        worksheet.write(row, 9, d_size or ' ', wbf['content2'])
                        worksheet.write(row, 10, d_notes or ' ', wbf['content'])
                        worksheet.write(row, 11, d_cost_price or ' ', wbf['content_float_price'])
                        worksheet.write(row, 12, d_retail_price or ' ', wbf['content_float_price'])
                        worksheet.write(row, 13, d_total_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 14, d_total_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 15, d_whbb_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 16, d_bbflg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 17, d_bbflg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 18, d_bbbbg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 19, d_bbbbg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 20, d_bbbwk_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 21, d_bbbwk_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 22, d_bbbrw_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 23, d_bbbrw_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 24, d_bbpdg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 25, d_bbpdg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 26, d_bbsyv_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 27, d_bbsyv_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 28, d_bbglr_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 29, d_bbglr_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 30, d_bbblg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 31, d_bbblg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 32, d_bbsnr_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 33, d_bbsnr_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 34, d_bbptg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 35, d_bbptg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 36, d_bbkta_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 37, d_bbkta_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 38, d_online_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 39, d_online_qty_stock or ' ', wbf['content_float'])
                        row += 1

                    worksheet.write(row, 0, dt_class_name or ' ', wbf['total_content'])
                    worksheet.write(row, 1, dt_category  or ' ', wbf['total_content'])
                    worksheet.write(row, 2, dt_parent_category or ' ', wbf['total_content'])
                    worksheet.write(row, 3, ' ', wbf['total_content'])
                    worksheet.write(row, 4, style + ' Total' or ' ', wbf['total_content'])
                    worksheet.write(row, 5, ' ', wbf['total_content'])
                    worksheet.write(row, 6, ' ', wbf['total_content'])
                    worksheet.write(row, 7, ' ', wbf['total_content'])
                    worksheet.write(row, 8, ' ', wbf['total_content'])
                    worksheet.write(row, 9, ' ', wbf['total_content'])
                    worksheet.write(row, 10, ' ', wbf['total_content'])
                    worksheet.write(row, 11, ' ', wbf['total_content_float_price'])
                    worksheet.write(row, 12, ' ', wbf['total_content_float_price'])
                    worksheet.write(row, 13, dt_total_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 14, dt_total_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 15, dt_whbb_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 16, dt_bbflg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 17, dt_bbflg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 18, dt_bbbbg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 19, dt_bbbbg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 20, dt_bbbwk_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 21, dt_bbbwk_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 22, dt_bbbrw_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 23, dt_bbbrw_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 24, dt_bbpdg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 25, dt_bbpdg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 26, dt_bbsyv_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 27, dt_bbsyv_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 28, dt_bbglr_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 29, dt_bbglr_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 30, dt_bbblg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 31, dt_bbblg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 32, dt_bbsnr_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 33, dt_bbsnr_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 34, dt_bbptg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 35, dt_bbptg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 36, dt_bbkta_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 37, dt_bbkta_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 38, dt_online_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 39, dt_online_qty_stock or ' ', wbf['total_content_float'])
                    row += 1

                worksheet.write(row, 0, cl_class_name + ' Total' or ' ', wbf['total_content'])
                worksheet.write(row, 1, ' ', wbf['total_content'])
                worksheet.write(row, 2, ' ', wbf['total_content'])
                worksheet.write(row, 3, ' ', wbf['total_content'])
                worksheet.write(row, 4, ' ', wbf['total_content'])
                worksheet.write(row, 5, ' ', wbf['total_content'])
                worksheet.write(row, 6, ' ', wbf['total_content'])
                worksheet.write(row, 7, ' ', wbf['total_content'])
                worksheet.write(row, 8, ' ', wbf['total_content'])
                worksheet.write(row, 9, ' ', wbf['total_content'])
                worksheet.write(row, 10, ' ', wbf['total_content'])
                worksheet.write(row, 11, ' ', wbf['total_content_float_price'])
                worksheet.write(row, 12, ' ', wbf['total_content_float_price'])
                worksheet.write(row, 13, cl_total_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 14, cl_total_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 15, cl_whbb_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 16, cl_bbflg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 17, cl_bbflg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 18, cl_bbbbg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 19, cl_bbbbg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 20, cl_bbbwk_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 21, cl_bbbwk_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 22, cl_bbbrw_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 23, cl_bbbrw_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 24, cl_bbpdg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 25, cl_bbpdg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 26, cl_bbsyv_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 27, cl_bbsyv_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 28, cl_bbglr_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 29, cl_bbglr_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 30, cl_bbblg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 31, cl_bbblg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 32, cl_bbsnr_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 33, cl_bbsnr_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 34, cl_bbptg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 35, cl_bbptg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 36, cl_bbkta_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 37, cl_bbkta_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 38, cl_online_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 39, cl_online_qty_stock or ' ', wbf['total_content_float'])
                row += 1
                
                
                gt_total_qty_sold += cl_total_qty_sold
                gt_total_qty_stock += cl_total_qty_stock
                gt_whbb_qty_sold += cl_whbb_qty_sold
                gt_bbflg_qty_sold += cl_bbflg_qty_sold
                gt_bbbbg_qty_sold += cl_bbbbg_qty_sold
                gt_bbbwk_qty_sold += cl_bbbwk_qty_sold
                gt_bbbrw_qty_sold += cl_bbbrw_qty_sold
                gt_bbpdg_qty_sold += cl_bbpdg_qty_sold
                gt_bbsyv_qty_sold += cl_bbsyv_qty_sold
                gt_bbglr_qty_sold += cl_bbglr_qty_sold
                gt_bbblg_qty_sold += cl_bbblg_qty_sold
                gt_bbsnr_qty_sold += cl_bbsnr_qty_sold
                gt_bbptg_qty_sold += cl_bbptg_qty_sold
                gt_bbkta_qty_sold += cl_bbkta_qty_sold
                gt_online_qty_sold += cl_online_qty_sold
                gt_whbb_qty_stock += cl_whbb_qty_stock
                gt_bbflg_qty_stock += cl_bbflg_qty_stock
                gt_bbbbg_qty_stock += cl_bbbbg_qty_stock
                gt_bbbwk_qty_stock += cl_bbbwk_qty_stock
                gt_bbbrw_qty_stock += cl_bbbrw_qty_stock
                gt_bbpdg_qty_stock += cl_bbpdg_qty_stock
                gt_bbsyv_qty_stock += cl_bbsyv_qty_stock
                gt_bbglr_qty_stock += cl_bbglr_qty_stock
                gt_bbblg_qty_stock += cl_bbblg_qty_stock
                gt_bbsnr_qty_stock += cl_bbsnr_qty_stock
                gt_bbptg_qty_stock += cl_bbptg_qty_stock
                gt_bbkta_qty_stock += cl_bbkta_qty_stock
                gt_online_qty_stock += cl_online_qty_stock

            worksheet.write(row, 0, 'GRAND TOTAL', wbf['total_content'])
            worksheet.write(row, 1, ' ', wbf['total_content'])
            worksheet.write(row, 2, ' ', wbf['total_content'])
            worksheet.write(row, 3, ' ', wbf['total_content'])
            worksheet.write(row, 4, ' ', wbf['total_content'])
            worksheet.write(row, 5, ' ', wbf['total_content'])
            worksheet.write(row, 6, ' ', wbf['total_content'])
            worksheet.write(row, 7, ' ', wbf['total_content'])
            worksheet.write(row, 8, ' ', wbf['total_content'])
            worksheet.write(row, 9, ' ', wbf['total_content'])
            worksheet.write(row, 10, ' ', wbf['total_content'])
            worksheet.write(row, 11, ' ', wbf['total_content_float_price'])
            worksheet.write(row, 12, ' ', wbf['total_content_float_price'])
            worksheet.write(row, 13, gt_total_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 14, gt_total_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 15, gt_whbb_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 16, gt_bbflg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 17, gt_bbflg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 18, gt_bbbbg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 19, gt_bbbbg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 20, gt_bbbwk_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 21, gt_bbbwk_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 22, gt_bbbrw_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 23, gt_bbbrw_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 24, gt_bbpdg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 25, gt_bbpdg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 26, gt_bbsyv_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 27, gt_bbsyv_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 28, gt_bbglr_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 29, gt_bbglr_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 30, gt_bbblg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 31, gt_bbblg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 32, gt_bbsnr_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 33, gt_bbsnr_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 34, gt_bbptg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 35, gt_bbptg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 36, gt_bbkta_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 37, gt_bbkta_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 38, gt_online_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 39, gt_online_qty_stock or ' ', wbf['total_content_float'])


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






        else:

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
            worksheet.set_column('N:N', 20)
            worksheet.set_column('O:O', 20)
            worksheet.set_column('P:P', 20)
            worksheet.set_column('Q:Q', 20)
            worksheet.set_column('R:R', 20)
            worksheet.set_column('S:S', 20)
            worksheet.set_column('T:T', 20)
            worksheet.set_column('U:U', 20)
            worksheet.set_column('V:V', 20)
            worksheet.set_column('W:W', 20)
            worksheet.set_column('X:X', 20)
            worksheet.set_column('Y:Y', 20)
            worksheet.set_column('Z:Z', 20)

            worksheet.set_column('AA:AA', 20)
            worksheet.set_column('AB:AB', 20)
            worksheet.set_column('AC:AC', 20)
            worksheet.set_column('AD:AD', 20)
            worksheet.set_column('AE:AE', 20)
            worksheet.set_column('AF:AF', 20)
            worksheet.set_column('AG:AG', 20)
            worksheet.set_column('AH:AH', 20)
            worksheet.set_column('AI:AI', 20)
            worksheet.set_column('AJ:AJ', 20)
            worksheet.set_column('AK:AK', 20)
            worksheet.set_column('AL:AL', 20)
            worksheet.set_column('AM:AM', 20)
            worksheet.set_column('AN:AN', 20)
            worksheet.set_column('AO:AO', 20)

            worksheet.merge_range('A1:E1', 'PERIOD OF SALES : ' + str(start_month) + ' ' + str(start_day) + 'th - ' + str(
                end_month) + ' ' + str(end_day) + 'th, ' + str(year), wbf['title_doc_brown'])
            worksheet.merge_range('A2:E2', 'DATA LAST STOCK : ' + str(end_month) + ' ' + str(end_day) + 'th, ' + str(year),
                                  wbf['title_doc_pink'])
            worksheet.merge_range('F1:AO1', '', wbf['title_doc'])
            worksheet.merge_range('F2:AO2', '', wbf['title_doc'])
            worksheet.merge_range('A3:N3', '', wbf['header'])

            worksheet.merge_range('O3:P3', 'SUMMARY TOTAL', wbf['header_orange'])
            worksheet.write(2, 16, "WH", wbf['header_green'])
            worksheet.merge_range('R3:S3', "FLAGSHIP", wbf['header_no'])
            worksheet.merge_range('T3:U3', "BATU BOLONG", wbf['header_no'])
            worksheet.merge_range('V3:W3', "BEACHWALK", wbf['header_no'])
            worksheet.merge_range('X3:Y3', "BRAWA", wbf['header_no'])
            worksheet.merge_range('Z3:AA3', "PADANG", wbf['header_no'])
            worksheet.merge_range('AB3:AC3', "VILAGE", wbf['header_no'])
            worksheet.merge_range('AD3:AE3', "GALERIA", wbf['header_no'])
            worksheet.merge_range('AF3:AG3', "BATU BELIG", wbf['header_no'])
            worksheet.merge_range('AH3:AI3', "SANUR", wbf['header_no'])
            worksheet.merge_range('AJ3:AK3', "PETITENGET", wbf['header_no'])
            worksheet.merge_range('AL3:AM3', "KUTA", wbf['header_no'])
            worksheet.merge_range('AN3:AO3', "ONLINE STORE", wbf['header_no'])

            columns = [
                ('Class', 8, 'char', 'char'),
                ('Model', 20, 'char', 'char'),
                ('Category', 20, 'char', 'char'),
                ('Style', 60, 'char', 'char'),
                ('Stock Name', 38, 'char', 'char'),
                ('Stock ID', 8, 'char', 'char'),
                ('Color', 20, 'char', 'char'),
                ('Aging', 11, 'char', 'char'),
                ('Barcode', 15, 'char', 'char'),
                ('Size', 7, 'char', 'char'),
                ('Photo', 25, 'char', 'char'),
                ('Notes Order', 20, 'char', 'char'),
                ('Cost Price', 9, 'char', 'char'),
                ('Retail Price', 9, 'char', 'char'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
                ('QTY SOLD', 8, 'float', 'float'),
                ('IN STOCK', 8, 'float2', 'float2'),
            ]

            row = 4
            col = 0
            for column in columns:
                column_name = column[0]
                column_width = column[1]
                column_type = column[2]
                bg_column = wbf['header_blue']
                if column_type == 'float':
                    bg_column = wbf['header_brown']
                elif column_type == 'float2':
                    bg_column = wbf['header_pink']
                worksheet.set_column(col, col, column_width)
                worksheet.write(row - 1, col, column_name, bg_column)

                col += 1

            row += 1
            no = 1

            domain = [
                ('type', '=', 'product'),
            ]

            if self.class_product_id and self.product_category_id:
                domain += [
                    ('class_product', '=', self.class_product_id.id),
                    ('product_category_categ_id', '=', self.product_category_id.id),
                ]
            elif self.class_product_id:
                domain += [('class_product', '=', self.class_product_id.id)]
            elif self.product_category_id:
                domain += [('product_category_categ_id', '=', self.product_category_id.id)]

            product_product = self.env['product.product'].with_context(to_date=self.end_period).search(domain)

            report_data = {}

            data_pos_orders = product_product.filtered(
                lambda x: not x.is_produk_diskon and not x.is_produk_promotion and not x.is_produk_promotion_free)

            for line in data_pos_orders:
                notes = ''
                # pickings = self.env['stock.picking'].browse(line.order_id.picking_ids.filtered(lambda x: x.state == 'done').ids)
                # for picking in pickings:
                #     notes = picking.date_done.strftime('%Y-%m-%d')
                incoming_qty = 0
                qty_received = 0
                purchase_count = 0
                purchase_list = []
                for move in self.env['stock.move'].search([
                    ('product_id', '=', line.id),
                    ('state', 'in', ['assigned', 'done']),
                    ('location_dest_id.usage', '=', 'internal'),
                    ('picking_id.purchase_id.date_planned', '>=', self.start_period),
                    ('picking_id.purchase_id.date_planned', '<=', self.end_period)]):
                    qty_received += move.product_uom_qty
                    purchase_list.append(move.picking_id.purchase_id.id)

                purchase_ids = self.env['purchase.order'].search([
                    ('id', 'in', purchase_list),
                    ('state', '=', 'purchase'),
                ], limit=10)
                purchase_count = len(purchase_ids)
                if qty_received > 0 and purchase_count > 1:
                    notes = self.end_period.strftime('%B') + ', ' + str(qty_received) + 'pcs'
                else:
                    for move in self.env['stock.move'].search([
                        ('product_id', '=', line.id),
                        ('state', '=', 'assigned'),
                        ('location_dest_id.usage', '=', 'internal'),
                        ('picking_id.purchase_id.date_planned', '<=', self.end_period)]):
                        incoming_qty += move.product_uom_qty

                    if incoming_qty > 0:
                        notes = 'just comming last week'

                list_color = ['COLOR', 'COLOUR', 'COLOURS', 'COLORS', 'WARNA', 'CORAK']
                list_size = ['SIZE', 'UKURAN']

                prod = line
                class_id = prod.class_product
                category = prod.product_model_categ_id
                parent_category = prod.product_category_categ_id
                stockname = prod.name
                stockid = prod.default_code
                color_size_ids = prod.product_template_variant_value_ids.mapped('display_name') or ''
                get_color = [c.split(': ')[1] for c in color_size_ids if any(attr in c for attr in list_color)]
                get_size = [s.split(': ')[1] for s in color_size_ids if any(attr in s for attr in list_size)]
                color = get_color[0] if get_color else ''
                size = get_size[0] if get_size else ''
                barcode = prod.barcode
                style = str(stockname) + '-' + str(color)
                cost_price = prod.standard_price
                retail_price = prod.lst_price
                picture = io.BytesIO(base64.b64decode(prod.image_1920)) if prod.image_1920 else ''
                # qty_sold = line.qty
                # qty_stock = prod.qty_available

                qty_sold_quantities = self.env['pos.order'].search([
                    ('picking_ids.move_lines.product_id', '=', prod.id),
                    ('date_order', '>=', self.start_period),
                    ('date_order', '<=', self.end_period),
                    ('picking_ids.state', 'in', ['assigned', 'done']),
                    ('picking_ids.location_id.warehouse_id.code', 'in', ('WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW',
                                                                         'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG', 'BBSNR',
                                                                         'BBPTG', 'BBKTA', 'Onlne'))
                ])

                qty_sold_per_warehouse = {wh.code: sum(move.product_uom_qty for move in move_lines)
                                          for wh in self.env['stock.warehouse'].search([])
                                          for move_lines in qty_sold_quantities.picking_ids.move_lines
                                          if move_lines.location_id.warehouse_id.code == wh.code}

                total_qty_sold = sum(qty_sold_per_warehouse.values())

                # stock_quant = self.env['stock.quant'].sudo().search([
                #             ('location_id.usage', '=', 'internal'),
                #             ('name_warehouse_id.code', 'in', ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Online')),
                #             ('product_id.categ_id', '=', category.id),
                #         ])
                # qty_stock = 0
                # for quant in stock_quant:
                #     qty_stock += quant.quantity

                # qty_stock = sum(line.product_id.stock_quant_ids.filtered(lambda x: x.location_id.usage == 'internal' and x.location_id.warehouse_id.code in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Online') and x.in_date.date() >= self.start_period and x.in_date.date() <= self.end_period).mapped('quantity'))
                # qty_stock = sum(line.product_id.qty_available for line in lines)
                # qty_stock = sum(line.product_id.product_tmpl_id.qty_available for line in lines)

                warehouse_quantities = line.stock_quant_ids.filtered(
                    lambda x: x.location_id.usage == 'internal' and
                              x.location_id.warehouse_id.code in (
                                  'WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW', 'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG',
                                  'BBSNR',
                                  'BBPTG', 'BBKTA', 'Onlne')
                )

                # qty_stock = sum(warehouse_quantities.mapped('quantity'))
                # warehouse = set(warehouse_quantities.mapped('location_id.warehouse_id'))
                # warehouse_list = list(warehouse)
                qty_stock_per_warehouse = {wh.code: sum(
                    quant.quantity for quant in warehouse_quantities if quant.location_id.warehouse_id.code == wh.code)
                    for wh in set(warehouse_quantities.mapped('location_id.warehouse_id'))}

                total_qty_stock = sum(qty_stock_per_warehouse.values())
                # total_qty_sold += qty_sold
                if total_qty_stock == 0 and total_qty_sold == 0:
                    continue

                # warehouse = line.order_id.picking_type_id.warehouse_id
                # age = int((fields.Date.today() - line.order_id.date_order.date()).days / 7)
                today = datetime.now()
                moves = sorted(line.stock_move_ids.filtered(
                    lambda x: x.picking_type_id.code == 'incoming' and x.state == 'done' and x.product_id == prod),
                               key=lambda x: x.date)
                # age_in_weeks = ((today - moves[0].date).days) // 7 if moves else 0
                age_in_weeks = ceil(((today - moves[0].date).days) / 7) if moves else 0
                age = int(age_in_weeks)

                # create keys for the report_data dictionary
                key = (class_id.id, parent_category.id, category.id, prod.id, color, size)

                # create dictionary entry for product if it does not exist
                if key not in report_data:
                    report_data[key] = {
                        'class_name': class_id.name,
                        'parent_category': parent_category.name,
                        'category': category.name,
                        'style': style,
                        'picture': picture,
                        'stockname': stockname,
                        'stockid': stockid,
                        'color': color,
                        'barcode': barcode,
                        'size': size,
                        'notes': notes,
                        'cost_price': cost_price,
                        'retail_price': retail_price,
                        'total_qty_sold': 0,
                        'total_qty_stock': 0,
                        'qty_sold': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0,
                                     'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                        'qty_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0,
                                      'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                        'age': age,
                    }

                for warehouse_key, quantity_stock in qty_stock_per_warehouse.items():
                    if warehouse_key in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Onlne'):
                        report_data[key]['total_qty_stock'] = total_qty_stock
                        report_data[key]['qty_stock'][warehouse_key] = quantity_stock

                for warehouse_key, quantity_sold in qty_sold_per_warehouse.items():
                    if warehouse_key in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Onlne'):
                        report_data[key]['total_qty_sold'] = total_qty_sold
                        report_data[key]['qty_sold'][warehouse_key] = quantity_sold

            rows = []
            for data in report_data.values():
                row = [data['class_name'],
                       data['parent_category'],
                       data['category'],
                       data['style'],
                       data['picture'],
                       data['stockname'],
                       data['stockid'],
                       data['color'],
                       data['barcode'],
                       data['size'],
                       data['notes'],
                       data['cost_price'],
                       data['retail_price'],
                       data['total_qty_sold'],
                       data['total_qty_stock'],
                       data['qty_sold']['WHBB'],
                       data['qty_sold']['BBFLG'],
                       data['qty_sold']['BBBBG'],
                       data['qty_sold']['BBBWK'],
                       data['qty_sold']['BBBRW'],
                       data['qty_sold']['BBPDG'],
                       data['qty_sold']['BBSYV'],
                       data['qty_sold']['BBGLR'],
                       data['qty_sold']['BBBLG'],
                       data['qty_sold']['BBSNR'],
                       data['qty_sold']['BBPTG'],
                       data['qty_sold']['BBKTA'],
                       data['qty_sold']['Online'],
                       data['qty_stock']['WHBB'],
                       data['qty_stock']['BBFLG'],
                       data['qty_stock']['BBBBG'],
                       data['qty_stock']['BBBWK'],
                       data['qty_stock']['BBBRW'],
                       data['qty_stock']['BBPDG'],
                       data['qty_stock']['BBSYV'],
                       data['qty_stock']['BBGLR'],
                       data['qty_stock']['BBBLG'],
                       data['qty_stock']['BBSNR'],
                       data['qty_stock']['BBPTG'],
                       data['qty_stock']['BBKTA'],
                       data['qty_stock']['Online'],
                       data['age']]
                rows.append(row)

            grouped_colors = {}

            for data in report_data.values():
                class_name = data['class_name']
                parent_category = data['parent_category']
                category = data['category']
                style = data['style']
                picture = data['picture']
                stockname = data['stockname']
                stockid = data['stockid']
                color = data['color']
                barcode = data['barcode']
                size = data['size']
                notes = data['notes']
                cost_price = data['cost_price']
                retail_price = data['retail_price']
                total_qty_sold = data['total_qty_sold']
                total_qty_stock = data['total_qty_stock']
                whbb_qty_sold = data['qty_sold']['WHBB']
                bbflg_qty_sold = data['qty_sold']['BBFLG']
                bbbbg_qty_sold = data['qty_sold']['BBBBG']
                bbbwk_qty_sold = data['qty_sold']['BBBWK']
                bbbrw_qty_sold = data['qty_sold']['BBBRW']
                bbpdg_qty_sold = data['qty_sold']['BBPDG']
                bbsyv_qty_sold = data['qty_sold']['BBSYV']
                bbglr_qty_sold = data['qty_sold']['BBGLR']
                bbblg_qty_sold = data['qty_sold']['BBBLG']
                bbsnr_qty_sold = data['qty_sold']['BBSNR']
                bbptg_qty_sold = data['qty_sold']['BBPTG']
                bbkta_qty_sold = data['qty_sold']['BBKTA']
                online_qty_sold = data['qty_sold']['Online']
                whbb_qty_stock = data['qty_stock']['WHBB']
                bbflg_qty_stock = data['qty_stock']['BBFLG']
                bbbbg_qty_stock = data['qty_stock']['BBBBG']
                bbbwk_qty_stock = data['qty_stock']['BBBWK']
                bbbrw_qty_stock = data['qty_stock']['BBBRW']
                bbpdg_qty_stock = data['qty_stock']['BBPDG']
                bbsyv_qty_stock = data['qty_stock']['BBSYV']
                bbglr_qty_stock = data['qty_stock']['BBGLR']
                bbblg_qty_stock = data['qty_stock']['BBBLG']
                bbsnr_qty_stock = data['qty_stock']['BBSNR']
                bbptg_qty_stock = data['qty_stock']['BBPTG']
                bbkta_qty_stock = data['qty_stock']['BBKTA']
                online_qty_stock = data['qty_stock']['Online']
                age = data['age']

                key = (class_name, parent_category, category, style, stockname, color)

                if key not in grouped_colors:
                    grouped_colors[key] = {
                        'class_name': class_name,
                        'parent_category': parent_category,
                        'category': category,
                        'style': style,
                        'stockname': stockname,
                        'color': color,
                        'stockid': stockid,
                        'total_qty_sold': total_qty_sold,
                        'total_qty_stock': total_qty_stock,
                        'whbb_qty_sold': whbb_qty_sold,
                        'bbflg_qty_sold': bbflg_qty_sold,
                        'bbbbg_qty_sold': bbbbg_qty_sold,
                        'bbbwk_qty_sold': bbbwk_qty_sold,
                        'bbbrw_qty_sold': bbbrw_qty_sold,
                        'bbpdg_qty_sold': bbpdg_qty_sold,
                        'bbsyv_qty_sold': bbsyv_qty_sold,
                        'bbglr_qty_sold': bbglr_qty_sold,
                        'bbblg_qty_sold': bbblg_qty_sold,
                        'bbsnr_qty_sold': bbsnr_qty_sold,
                        'bbptg_qty_sold': bbptg_qty_sold,
                        'bbkta_qty_sold': bbkta_qty_sold,
                        'online_qty_sold': online_qty_sold,
                        'whbb_qty_stock': whbb_qty_stock,
                        'bbflg_qty_stock': bbflg_qty_stock,
                        'bbbbg_qty_stock': bbbbg_qty_stock,
                        'bbbwk_qty_stock': bbbwk_qty_stock,
                        'bbbrw_qty_stock': bbbrw_qty_stock,
                        'bbpdg_qty_stock': bbpdg_qty_stock,
                        'bbsyv_qty_stock': bbsyv_qty_stock,
                        'bbglr_qty_stock': bbglr_qty_stock,
                        'bbblg_qty_stock': bbblg_qty_stock,
                        'bbsnr_qty_stock': bbsnr_qty_stock,
                        'bbptg_qty_stock': bbptg_qty_stock,
                        'bbkta_qty_stock': bbkta_qty_stock,
                        'online_qty_stock': online_qty_stock,
                        'children': {}
                    }

                else:
                    grouped_colors[key]['total_qty_sold'] += total_qty_sold
                    grouped_colors[key]['total_qty_stock'] += total_qty_stock
                    grouped_colors[key]['whbb_qty_sold'] += whbb_qty_sold
                    grouped_colors[key]['bbflg_qty_sold'] += bbflg_qty_sold
                    grouped_colors[key]['bbbbg_qty_sold'] += bbbbg_qty_sold
                    grouped_colors[key]['bbbwk_qty_sold'] += bbbwk_qty_sold
                    grouped_colors[key]['bbbrw_qty_sold'] += bbbrw_qty_sold
                    grouped_colors[key]['bbpdg_qty_sold'] += bbpdg_qty_sold
                    grouped_colors[key]['bbsyv_qty_sold'] += bbsyv_qty_sold
                    grouped_colors[key]['bbglr_qty_sold'] += bbglr_qty_sold
                    grouped_colors[key]['bbblg_qty_sold'] += bbblg_qty_sold
                    grouped_colors[key]['bbsnr_qty_sold'] += bbsnr_qty_sold
                    grouped_colors[key]['bbptg_qty_sold'] += bbptg_qty_sold
                    grouped_colors[key]['bbkta_qty_sold'] += bbkta_qty_sold
                    grouped_colors[key]['online_qty_sold'] += online_qty_sold
                    grouped_colors[key]['whbb_qty_stock'] += whbb_qty_stock
                    grouped_colors[key]['bbflg_qty_stock'] += bbflg_qty_stock
                    grouped_colors[key]['bbbbg_qty_stock'] += bbbbg_qty_stock
                    grouped_colors[key]['bbbwk_qty_stock'] += bbbwk_qty_stock
                    grouped_colors[key]['bbbrw_qty_stock'] += bbbrw_qty_stock
                    grouped_colors[key]['bbpdg_qty_stock'] += bbpdg_qty_stock
                    grouped_colors[key]['bbsyv_qty_stock'] += bbsyv_qty_stock
                    grouped_colors[key]['bbglr_qty_stock'] += bbglr_qty_stock
                    grouped_colors[key]['bbblg_qty_stock'] += bbblg_qty_stock
                    grouped_colors[key]['bbsnr_qty_stock'] += bbsnr_qty_stock
                    grouped_colors[key]['bbptg_qty_stock'] += bbptg_qty_stock
                    grouped_colors[key]['bbkta_qty_stock'] += bbkta_qty_stock
                    grouped_colors[key]['online_qty_stock'] += online_qty_stock

                category_data = grouped_colors[key]

                if size not in grouped_colors[key]['children']:
                    grouped_colors[key]['children'][size] = {
                        'notes': notes,
                        'barcode': barcode,
                        'picture': picture,
                        'cost_price': cost_price,
                        'retail_price': retail_price,
                        'total_qty_sold': total_qty_sold,
                        'total_qty_stock': total_qty_stock,
                        'whbb_qty_sold': whbb_qty_sold,
                        'bbflg_qty_sold': bbflg_qty_sold,
                        'bbbbg_qty_sold': bbbbg_qty_sold,
                        'bbbwk_qty_sold': bbbwk_qty_sold,
                        'bbbrw_qty_sold': bbbrw_qty_sold,
                        'bbpdg_qty_sold': bbpdg_qty_sold,
                        'bbsyv_qty_sold': bbsyv_qty_sold,
                        'bbglr_qty_sold': bbglr_qty_sold,
                        'bbblg_qty_sold': bbblg_qty_sold,
                        'bbsnr_qty_sold': bbsnr_qty_sold,
                        'bbptg_qty_sold': bbptg_qty_sold,
                        'bbkta_qty_sold': bbkta_qty_sold,
                        'online_qty_sold': online_qty_sold,
                        'whbb_qty_stock': whbb_qty_stock,
                        'bbflg_qty_stock': bbflg_qty_stock,
                        'bbbbg_qty_stock': bbbbg_qty_stock,
                        'bbbwk_qty_stock': bbbwk_qty_stock,
                        'bbbrw_qty_stock': bbbrw_qty_stock,
                        'bbpdg_qty_stock': bbpdg_qty_stock,
                        'bbsyv_qty_stock': bbsyv_qty_stock,
                        'bbglr_qty_stock': bbglr_qty_stock,
                        'bbblg_qty_stock': bbblg_qty_stock,
                        'bbsnr_qty_stock': bbsnr_qty_stock,
                        'bbptg_qty_stock': bbptg_qty_stock,
                        'bbkta_qty_stock': bbkta_qty_stock,
                        'online_qty_stock': online_qty_stock,
                        'age': age,
                    }
                else:
                    grouped_colors[key]['total_qty_sold'] += total_qty_sold
                    grouped_colors[key]['total_qty_stock'] += total_qty_stock
                    grouped_colors[key]['whbb_qty_sold'] += whbb_qty_sold
                    grouped_colors[key]['bbflg_qty_sold'] += bbflg_qty_sold
                    grouped_colors[key]['bbbbg_qty_sold'] += bbbbg_qty_sold
                    grouped_colors[key]['bbbwk_qty_sold'] += bbbwk_qty_sold
                    grouped_colors[key]['bbbrw_qty_sold'] += bbbrw_qty_sold
                    grouped_colors[key]['bbpdg_qty_sold'] += bbpdg_qty_sold
                    grouped_colors[key]['bbsyv_qty_sold'] += bbsyv_qty_sold
                    grouped_colors[key]['bbglr_qty_sold'] += bbglr_qty_sold
                    grouped_colors[key]['bbblg_qty_sold'] += bbblg_qty_sold
                    grouped_colors[key]['bbsnr_qty_sold'] += bbsnr_qty_sold
                    grouped_colors[key]['bbptg_qty_sold'] += bbptg_qty_sold
                    grouped_colors[key]['bbkta_qty_sold'] += bbkta_qty_sold
                    grouped_colors[key]['online_qty_sold'] += online_qty_sold
                    grouped_colors[key]['whbb_qty_stock'] += whbb_qty_stock
                    grouped_colors[key]['bbflg_qty_stock'] += bbflg_qty_stock
                    grouped_colors[key]['bbbbg_qty_stock'] += bbbbg_qty_stock
                    grouped_colors[key]['bbbwk_qty_stock'] += bbbwk_qty_stock
                    grouped_colors[key]['bbbrw_qty_stock'] += bbbrw_qty_stock
                    grouped_colors[key]['bbpdg_qty_stock'] += bbpdg_qty_stock
                    grouped_colors[key]['bbsyv_qty_stock'] += bbsyv_qty_stock
                    grouped_colors[key]['bbglr_qty_stock'] += bbglr_qty_stock
                    grouped_colors[key]['bbblg_qty_stock'] += bbblg_qty_stock
                    grouped_colors[key]['bbsnr_qty_stock'] += bbsnr_qty_stock
                    grouped_colors[key]['bbptg_qty_stock'] += bbptg_qty_stock
                    grouped_colors[key]['bbkta_qty_stock'] += bbkta_qty_stock
                    grouped_colors[key]['online_qty_stock'] += online_qty_stock


            grouped_class = {}
            for data_class in grouped_colors.values():
                cl_class_name = data_class['class_name']
                cl_parent_category = data_class['parent_category']
                cl_category = data_class['category']
                cl_style = data_class['style']
                cl_stockname = data_class['stockname']
                cl_color = data_class['color']
                cl_stockid = data_class['stockid']
                cl_total_qty_sold = data_class['total_qty_sold']
                cl_total_qty_stock = data_class['total_qty_stock']
                cl_whbb_qty_sold = data_class['whbb_qty_sold']
                cl_bbflg_qty_sold = data_class['bbflg_qty_sold']
                cl_bbbbg_qty_sold = data_class['bbbbg_qty_sold']
                cl_bbbwk_qty_sold = data_class['bbbwk_qty_sold']
                cl_bbbrw_qty_sold = data_class['bbbrw_qty_sold']
                cl_bbpdg_qty_sold = data_class['bbpdg_qty_sold']
                cl_bbsyv_qty_sold = data_class['bbsyv_qty_sold']
                cl_bbglr_qty_sold = data_class['bbglr_qty_sold']
                cl_bbblg_qty_sold = data_class['bbblg_qty_sold']
                cl_bbsnr_qty_sold = data_class['bbsnr_qty_sold']
                cl_bbptg_qty_sold = data_class['bbptg_qty_sold']
                cl_bbkta_qty_sold = data_class['bbkta_qty_sold']
                cl_online_qty_sold = data_class['online_qty_sold']
                cl_whbb_qty_stock = data_class['whbb_qty_stock']
                cl_bbflg_qty_stock = data_class['bbflg_qty_stock']
                cl_bbbbg_qty_stock = data_class['bbbbg_qty_stock']
                cl_bbbwk_qty_stock = data_class['bbbwk_qty_stock']
                cl_bbbrw_qty_stock = data_class['bbbrw_qty_stock']
                cl_bbpdg_qty_stock = data_class['bbpdg_qty_stock']
                cl_bbsyv_qty_stock = data_class['bbsyv_qty_stock']
                cl_bbglr_qty_stock = data_class['bbglr_qty_stock']
                cl_bbblg_qty_stock = data_class['bbblg_qty_stock']
                cl_bbsnr_qty_stock = data_class['bbsnr_qty_stock']
                cl_bbptg_qty_stock = data_class['bbptg_qty_stock']
                cl_bbkta_qty_stock = data_class['bbkta_qty_stock']
                cl_online_qty_stock = data_class['online_qty_stock']
                cl_children = data_class['children']

                key = cl_class_name

                if key not in grouped_class:
                    grouped_class[key] = {
                        'class_name': cl_class_name,
                        'total_qty_sold': cl_total_qty_sold,
                        'total_qty_stock': cl_total_qty_stock,
                        'whbb_qty_sold': cl_whbb_qty_sold,
                        'bbflg_qty_sold': cl_bbflg_qty_sold,
                        'bbbbg_qty_sold': cl_bbbbg_qty_sold,
                        'bbbwk_qty_sold': cl_bbbwk_qty_sold,
                        'bbbrw_qty_sold': cl_bbbrw_qty_sold,
                        'bbpdg_qty_sold': cl_bbpdg_qty_sold,
                        'bbsyv_qty_sold': cl_bbsyv_qty_sold,
                        'bbglr_qty_sold': cl_bbglr_qty_sold,
                        'bbblg_qty_sold': cl_bbblg_qty_sold,
                        'bbsnr_qty_sold': cl_bbsnr_qty_sold,
                        'bbptg_qty_sold': cl_bbptg_qty_sold,
                        'bbkta_qty_sold': cl_bbkta_qty_sold,
                        'online_qty_sold': cl_online_qty_sold,
                        'whbb_qty_stock': cl_whbb_qty_stock,
                        'bbflg_qty_stock': cl_bbflg_qty_stock,
                        'bbbbg_qty_stock': cl_bbbbg_qty_stock,
                        'bbbwk_qty_stock': cl_bbbwk_qty_stock,
                        'bbbrw_qty_stock': cl_bbbrw_qty_stock,
                        'bbpdg_qty_stock': cl_bbpdg_qty_stock,
                        'bbsyv_qty_stock': cl_bbsyv_qty_stock,
                        'bbglr_qty_stock': cl_bbglr_qty_stock,
                        'bbblg_qty_stock': cl_bbblg_qty_stock,
                        'bbsnr_qty_stock': cl_bbsnr_qty_stock,
                        'bbptg_qty_stock': cl_bbptg_qty_stock,
                        'bbkta_qty_stock': cl_bbkta_qty_stock,
                        'online_qty_stock': cl_online_qty_stock,
                        'children_category': {},
                    }
                else:
                    grouped_class[key]['total_qty_sold'] += cl_total_qty_sold
                    grouped_class[key]['total_qty_stock'] += cl_total_qty_stock
                    grouped_class[key]['whbb_qty_sold'] += cl_whbb_qty_sold
                    grouped_class[key]['bbflg_qty_sold'] += cl_bbflg_qty_sold
                    grouped_class[key]['bbbbg_qty_sold'] += cl_bbbbg_qty_sold
                    grouped_class[key]['bbbwk_qty_sold'] += cl_bbbwk_qty_sold
                    grouped_class[key]['bbbrw_qty_sold'] += cl_bbbrw_qty_sold
                    grouped_class[key]['bbpdg_qty_sold'] += cl_bbpdg_qty_sold
                    grouped_class[key]['bbsyv_qty_sold'] += cl_bbsyv_qty_sold
                    grouped_class[key]['bbglr_qty_sold'] += cl_bbglr_qty_sold
                    grouped_class[key]['bbblg_qty_sold'] += cl_bbblg_qty_sold
                    grouped_class[key]['bbsnr_qty_sold'] += cl_bbsnr_qty_sold
                    grouped_class[key]['bbptg_qty_sold'] += cl_bbptg_qty_sold
                    grouped_class[key]['bbkta_qty_sold'] += cl_bbkta_qty_sold
                    grouped_class[key]['online_qty_sold'] += cl_online_qty_sold
                    grouped_class[key]['whbb_qty_stock'] += cl_whbb_qty_stock
                    grouped_class[key]['bbflg_qty_stock'] += cl_bbflg_qty_stock
                    grouped_class[key]['bbbbg_qty_stock'] += cl_bbbbg_qty_stock
                    grouped_class[key]['bbbwk_qty_stock'] += cl_bbbwk_qty_stock
                    grouped_class[key]['bbbrw_qty_stock'] += cl_bbbrw_qty_stock
                    grouped_class[key]['bbpdg_qty_stock'] += cl_bbpdg_qty_stock
                    grouped_class[key]['bbsyv_qty_stock'] += cl_bbsyv_qty_stock
                    grouped_class[key]['bbglr_qty_stock'] += cl_bbglr_qty_stock
                    grouped_class[key]['bbblg_qty_stock'] += cl_bbblg_qty_stock
                    grouped_class[key]['bbsnr_qty_stock'] += cl_bbsnr_qty_stock
                    grouped_class[key]['bbptg_qty_stock'] += cl_bbptg_qty_stock
                    grouped_class[key]['bbkta_qty_stock'] += cl_bbkta_qty_stock
                    grouped_class[key]['online_qty_stock'] += cl_online_qty_stock

                category_data = grouped_class[key]
                subkey = (cl_parent_category, cl_category, cl_style, cl_stockname, cl_color)

                if subkey not in grouped_class[key]['children_category']:
                    grouped_class[key]['children_category'][subkey] = {
                        'class_name': cl_class_name,
                        'parent_category': cl_parent_category,
                        'category': cl_category,
                        'style': cl_style,
                        'stockname': cl_stockname,
                        # 'picture': cl_picture,
                        'color': cl_color,
                        'stockid': cl_stockid,
                        # 'notes': cl_notes,
                        # 'barcode': cl_barcode,
                        # 'cost_price': cl_cost_price,
                        # 'retail_price': cl_retail_price,
                        'total_qty_sold': cl_total_qty_sold,
                        'total_qty_stock': cl_total_qty_stock,
                        'whbb_qty_sold': cl_whbb_qty_sold,
                        'bbflg_qty_sold': cl_bbflg_qty_sold,
                        'bbbbg_qty_sold': cl_bbbbg_qty_sold,
                        'bbbwk_qty_sold': cl_bbbwk_qty_sold,
                        'bbbrw_qty_sold': cl_bbbrw_qty_sold,
                        'bbpdg_qty_sold': cl_bbpdg_qty_sold,
                        'bbsyv_qty_sold': cl_bbsyv_qty_sold,
                        'bbglr_qty_sold': cl_bbglr_qty_sold,
                        'bbblg_qty_sold': cl_bbblg_qty_sold,
                        'bbsnr_qty_sold': cl_bbsnr_qty_sold,
                        'bbptg_qty_sold': cl_bbptg_qty_sold,
                        'bbkta_qty_sold': cl_bbkta_qty_sold,
                        'online_qty_sold': cl_online_qty_sold,
                        'whbb_qty_stock': cl_whbb_qty_stock,
                        'bbflg_qty_stock': cl_bbflg_qty_stock,
                        'bbbbg_qty_stock': cl_bbbbg_qty_stock,
                        'bbbwk_qty_stock': cl_bbbwk_qty_stock,
                        'bbbrw_qty_stock': cl_bbbrw_qty_stock,
                        'bbpdg_qty_stock': cl_bbpdg_qty_stock,
                        'bbsyv_qty_stock': cl_bbsyv_qty_stock,
                        'bbglr_qty_stock': cl_bbglr_qty_stock,
                        'bbblg_qty_stock': cl_bbblg_qty_stock,
                        'bbsnr_qty_stock': cl_bbsnr_qty_stock,
                        'bbptg_qty_stock': cl_bbptg_qty_stock,
                        'bbkta_qty_stock': cl_bbkta_qty_stock,
                        'online_qty_stock': cl_online_qty_stock,
                        # 'age': cl_age,
                        'children': cl_children,
                    }




            # Print the result
            row = 4
            gt_total_qty_sold = 0
            gt_total_qty_stock = 0
            gt_whbb_qty_sold = 0
            gt_bbflg_qty_sold = 0
            gt_bbbbg_qty_sold = 0
            gt_bbbwk_qty_sold = 0
            gt_bbbrw_qty_sold = 0
            gt_bbpdg_qty_sold = 0
            gt_bbsyv_qty_sold = 0
            gt_bbglr_qty_sold = 0
            gt_bbblg_qty_sold = 0
            gt_bbsnr_qty_sold = 0
            gt_bbptg_qty_sold = 0
            gt_bbkta_qty_sold = 0
            gt_online_qty_sold = 0
            gt_whbb_qty_stock = 0
            gt_bbflg_qty_stock = 0
            gt_bbbbg_qty_stock = 0
            gt_bbbwk_qty_stock = 0
            gt_bbbrw_qty_stock = 0
            gt_bbpdg_qty_stock = 0
            gt_bbsyv_qty_stock = 0
            gt_bbglr_qty_stock = 0
            gt_bbblg_qty_stock = 0
            gt_bbsnr_qty_stock = 0
            gt_bbptg_qty_stock = 0
            gt_bbkta_qty_stock = 0
            gt_online_qty_stock = 0

            for key, value in grouped_class.items():
                children_category = value['children_category']

                cl_class_name = value['class_name']
                cl_total_qty_sold = value['total_qty_sold']
                cl_total_qty_stock = value['total_qty_stock']
                cl_whbb_qty_sold = value['whbb_qty_sold']
                cl_bbflg_qty_sold = value['bbflg_qty_sold']
                cl_bbbbg_qty_sold = value['bbbbg_qty_sold']
                cl_bbbwk_qty_sold = value['bbbwk_qty_sold']
                cl_bbbrw_qty_sold = value['bbbrw_qty_sold']
                cl_bbpdg_qty_sold = value['bbpdg_qty_sold']
                cl_bbsyv_qty_sold = value['bbsyv_qty_sold']
                cl_bbglr_qty_sold = value['bbglr_qty_sold']
                cl_bbblg_qty_sold = value['bbblg_qty_sold']
                cl_bbsnr_qty_sold = value['bbsnr_qty_sold']
                cl_bbptg_qty_sold = value['bbptg_qty_sold']
                cl_bbkta_qty_sold = value['bbkta_qty_sold']
                cl_online_qty_sold = value['online_qty_sold']
                cl_whbb_qty_stock = value['whbb_qty_stock']
                cl_bbflg_qty_stock = value['bbflg_qty_stock']
                cl_bbbbg_qty_stock = value['bbbbg_qty_stock']
                cl_bbbwk_qty_stock = value['bbbwk_qty_stock']
                cl_bbbrw_qty_stock = value['bbbrw_qty_stock']
                cl_bbpdg_qty_stock = value['bbpdg_qty_stock']
                cl_bbsyv_qty_stock = value['bbsyv_qty_stock']
                cl_bbglr_qty_stock = value['bbglr_qty_stock']
                cl_bbblg_qty_stock = value['bbblg_qty_stock']
                cl_bbsnr_qty_stock = value['bbsnr_qty_stock']
                cl_bbptg_qty_stock = value['bbptg_qty_stock']
                cl_bbkta_qty_stock = value['bbkta_qty_stock']
                cl_online_qty_stock = value['online_qty_stock']

                for subkey, categ_value in children_category.items():

                    parent_category, category, style, stockname, color = subkey
                    # class_name, parent_category, category = key

                    total_qty_sold, total_qty_stock, whbb_qty_sold, bbflg_qty_sold, bbbbg_qty_sold, bbbwk_qty_sold, bbbrw_qty_sold, bbpdg_qty_sold, bbsyv_qty_sold, bbglr_qty_sold, bbblg_qty_sold, bbsnr_qty_sold, bbptg_qty_sold, bbkta_qty_sold, online_qty_sold, whbb_qty_stock, bbflg_qty_stock, bbbbg_qty_stock, bbbwk_qty_stock, bbbrw_qty_stock, bbpdg_qty_stock, bbsyv_qty_stock, bbglr_qty_stock, bbblg_qty_stock, bbsnr_qty_stock, bbptg_qty_stock, bbkta_qty_stock, online_qty_stock = \
                        categ_value['total_qty_sold'], categ_value['total_qty_stock'], categ_value['whbb_qty_sold'], \
                        categ_value['bbflg_qty_sold'], \
                            categ_value['bbbbg_qty_sold'], categ_value['bbbwk_qty_sold'], categ_value['bbbrw_qty_sold'], \
                        categ_value['bbpdg_qty_sold'], \
                            categ_value['bbsyv_qty_sold'], categ_value['bbglr_qty_sold'], categ_value['bbblg_qty_sold'], \
                        categ_value['bbsnr_qty_sold'], \
                            categ_value['bbptg_qty_sold'], categ_value['bbkta_qty_sold'], categ_value[
                            'online_qty_sold'], categ_value['whbb_qty_stock'], \
                            categ_value['bbflg_qty_stock'], categ_value['bbbbg_qty_stock'], categ_value[
                            'bbbwk_qty_stock'], categ_value[
                            'bbbrw_qty_stock'], categ_value['bbpdg_qty_stock'], categ_value['bbsyv_qty_stock'], \
                        categ_value[
                            'bbglr_qty_stock'], categ_value['bbblg_qty_stock'], categ_value['bbsnr_qty_stock'], \
                        categ_value[
                            'bbptg_qty_stock'], categ_value['bbkta_qty_stock'], categ_value['online_qty_stock']
                    qty_sold_total = whbb_qty_sold + bbflg_qty_sold + bbbbg_qty_sold + bbbwk_qty_sold + bbbrw_qty_sold + bbpdg_qty_sold + bbsyv_qty_sold + bbglr_qty_sold + bbblg_qty_sold + bbsnr_qty_sold + bbptg_qty_sold + bbkta_qty_sold + online_qty_sold
                    qty_stock_total = whbb_qty_stock + bbflg_qty_stock + bbbbg_qty_stock + bbbwk_qty_stock + bbbrw_qty_stock + bbpdg_qty_stock + bbsyv_qty_stock + bbglr_qty_stock + bbblg_qty_stock + bbsnr_qty_stock + bbptg_qty_stock + bbkta_qty_stock + online_qty_stock

                    dt_class_name = categ_value['class_name']
                    dt_parent_category = parent_category
                    dt_category = category
                    dt_style = str(style) + ' Total'
                    dt_total_qty_sold = total_qty_sold
                    dt_total_qty_stock = total_qty_stock
                    dt_whbb_qty_sold = whbb_qty_sold
                    dt_bbflg_qty_sold = bbflg_qty_sold
                    dt_bbbbg_qty_sold = bbbbg_qty_sold
                    dt_bbbwk_qty_sold = bbbwk_qty_sold
                    dt_bbbrw_qty_sold = bbbrw_qty_sold
                    dt_bbpdg_qty_sold = bbpdg_qty_sold
                    dt_bbsyv_qty_sold = bbsyv_qty_sold
                    dt_bbglr_qty_sold = bbglr_qty_sold
                    dt_bbblg_qty_sold = bbblg_qty_sold
                    dt_bbsnr_qty_sold = bbsnr_qty_sold
                    dt_bbptg_qty_sold = bbptg_qty_sold
                    dt_bbkta_qty_sold = bbkta_qty_sold
                    dt_online_qty_sold = online_qty_sold
                    dt_whbb_qty_stock = whbb_qty_stock
                    dt_bbflg_qty_stock = bbflg_qty_stock
                    dt_bbbbg_qty_stock = bbbbg_qty_stock
                    dt_bbbwk_qty_stock = bbbwk_qty_stock
                    dt_bbbrw_qty_stock = bbbrw_qty_stock
                    dt_bbpdg_qty_stock = bbpdg_qty_stock
                    dt_bbsyv_qty_stock = bbsyv_qty_stock
                    dt_bbglr_qty_stock = bbglr_qty_stock
                    dt_bbblg_qty_stock = bbblg_qty_stock
                    dt_bbsnr_qty_stock = bbsnr_qty_stock
                    dt_bbptg_qty_stock = bbptg_qty_stock
                    dt_bbkta_qty_stock = bbkta_qty_stock
                    dt_online_qty_stock = online_qty_stock
                    children = categ_value['children']

                    for size, size_value in children.items():
                        d_class_name = categ_value['class_name']
                        d_parent_category = categ_value['parent_category']
                        d_category = categ_value['category']
                        d_style = categ_value['style']
                        d_stockname = categ_value['stockname']
                        d_stockid = categ_value['stockid']
                        d_color = categ_value['color']
                        d_age = size_value['age']
                        d_picture = size_value['picture']
                        d_barcode = size_value['barcode']
                        d_size = size
                        d_notes = size_value['notes']
                        d_cost_price = size_value['cost_price']
                        d_retail_price = size_value['retail_price']
                        d_total_qty_sold = size_value['total_qty_sold']
                        d_total_qty_stock = size_value['total_qty_stock']
                        d_whbb_qty_sold = size_value['whbb_qty_sold']
                        d_bbflg_qty_sold = size_value['bbflg_qty_sold']
                        d_bbbbg_qty_sold = size_value['bbbbg_qty_sold']
                        d_bbbwk_qty_sold = size_value['bbbwk_qty_sold']
                        d_bbbrw_qty_sold = size_value['bbbrw_qty_sold']
                        d_bbpdg_qty_sold = size_value['bbpdg_qty_sold']
                        d_bbsyv_qty_sold = size_value['bbsyv_qty_sold']
                        d_bbglr_qty_sold = size_value['bbglr_qty_sold']
                        d_bbblg_qty_sold = size_value['bbblg_qty_sold']
                        d_bbsnr_qty_sold = size_value['bbsnr_qty_sold']
                        d_bbptg_qty_sold = size_value['bbptg_qty_sold']
                        d_bbkta_qty_sold = size_value['bbkta_qty_sold']
                        d_online_qty_sold = size_value['online_qty_sold']
                        d_whbb_qty_stock = size_value['whbb_qty_stock']
                        d_bbflg_qty_stock = size_value['bbflg_qty_stock']
                        d_bbbbg_qty_stock = size_value['bbbbg_qty_stock']
                        d_bbbwk_qty_stock = size_value['bbbwk_qty_stock']
                        d_bbbrw_qty_stock = size_value['bbbrw_qty_stock']
                        d_bbpdg_qty_stock = size_value['bbpdg_qty_stock']
                        d_bbsyv_qty_stock = size_value['bbsyv_qty_stock']
                        d_bbglr_qty_stock = size_value['bbglr_qty_stock']
                        d_bbblg_qty_stock = size_value['bbblg_qty_stock']
                        d_bbsnr_qty_stock = size_value['bbsnr_qty_stock']
                        d_bbptg_qty_stock = size_value['bbptg_qty_stock']
                        d_bbkta_qty_stock = size_value['bbkta_qty_stock']
                        d_online_qty_stock = size_value['online_qty_stock']

                        worksheet.write(row, 0, d_class_name or ' ', wbf['content'])
                        worksheet.write(row, 1, d_category or ' ', wbf['content'])
                        worksheet.write(row, 2, d_parent_category or ' ', wbf['content'])
                        worksheet.write(row, 3, d_style or ' ', wbf['content'])
                        worksheet.write(row, 4, d_stockname or ' ', wbf['content'])
                        worksheet.write(row, 5, d_stockid or ' ', wbf['content'])
                        worksheet.write(row, 6, d_color or ' ', wbf['content'])
                        worksheet.write(row, 7, d_age or ' ', wbf['content2'])
                        worksheet.write(row, 8, d_barcode or ' ', wbf['content'])
                        worksheet.write(row, 9, d_size or ' ', wbf['content2'])
                        if d_picture:
                            worksheet.write(row, 10, '', wbf['content'])
                            worksheet.insert_image(row, 10, 'image.png', {'image_data': d_picture, 'x_scale': 0.21,
                                                                          'y_scale': 0.15, 'object_position': 1,
                                                                          'x_offset': 30, 'y_offset': 5})
                        else:
                            worksheet.write(row, 10, '', wbf['content'])
                        worksheet.write(row, 11, d_notes or ' ', wbf['content'])
                        worksheet.write(row, 12, d_cost_price or ' ', wbf['content_float_price'])
                        worksheet.write(row, 13, d_retail_price or ' ', wbf['content_float_price'])
                        worksheet.write(row, 14, d_total_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 15, d_total_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 16, d_whbb_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 17, d_bbflg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 18, d_bbflg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 19, d_bbbbg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 20, d_bbbbg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 21, d_bbbwk_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 22, d_bbbwk_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 23, d_bbbrw_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 24, d_bbbrw_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 25, d_bbpdg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 26, d_bbpdg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 27, d_bbsyv_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 28, d_bbsyv_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 29, d_bbglr_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 30, d_bbglr_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 31, d_bbblg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 32, d_bbblg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 33, d_bbsnr_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 34, d_bbsnr_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 35, d_bbptg_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 36, d_bbptg_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 37, d_bbkta_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 38, d_bbkta_qty_stock or ' ', wbf['content_float'])
                        worksheet.write(row, 39, d_online_qty_sold or ' ', wbf['total_content_float_brown'])
                        worksheet.write(row, 40, d_online_qty_stock or ' ', wbf['content_float'])

                        worksheet.set_row(row, 70)
                        row += 1

                    worksheet.write(row, 0, dt_class_name or ' ', wbf['total_content'])
                    worksheet.write(row, 1, dt_category or ' ', wbf['total_content'])
                    worksheet.write(row, 2, dt_parent_category or ' ', wbf['total_content'])
                    worksheet.write(row, 3, ' ', wbf['total_content'])
                    worksheet.write(row, 4, style + ' Total' or ' ', wbf['total_content'])
                    worksheet.write(row, 5, ' ', wbf['total_content'])
                    worksheet.write(row, 6, ' ', wbf['total_content'])
                    worksheet.write(row, 7, ' ', wbf['total_content'])
                    worksheet.write(row, 8, ' ', wbf['total_content'])
                    worksheet.write(row, 9, ' ', wbf['total_content'])
                    worksheet.write(row, 10, ' ', wbf['total_content'])
                    worksheet.write(row, 11, ' ', wbf['total_content'])
                    worksheet.write(row, 12, ' ', wbf['total_content_float_price'])
                    worksheet.write(row, 13, ' ', wbf['total_content_float_price'])
                    worksheet.write(row, 14, dt_total_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 15, dt_total_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 16, dt_whbb_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 17, dt_bbflg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 18, dt_bbflg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 19, dt_bbbbg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 20, dt_bbbbg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 21, dt_bbbwk_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 22, dt_bbbwk_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 23, dt_bbbrw_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 24, dt_bbbrw_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 25, dt_bbpdg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 26, dt_bbpdg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 27, dt_bbsyv_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 28, dt_bbsyv_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 29, dt_bbglr_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 30, dt_bbglr_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 31, dt_bbblg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 32, dt_bbblg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 33, dt_bbsnr_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 34, dt_bbsnr_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 35, dt_bbptg_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 36, dt_bbptg_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 37, dt_bbkta_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 38, dt_bbkta_qty_stock or ' ', wbf['total_content_float'])
                    worksheet.write(row, 39, dt_online_qty_sold or ' ', wbf['total_content_float'])
                    worksheet.write(row, 40, dt_online_qty_stock or ' ', wbf['total_content_float'])
                    row += 1

                worksheet.write(row, 0, cl_class_name + ' Total' or ' ', wbf['total_content'])
                worksheet.write(row, 1, ' ', wbf['total_content'])
                worksheet.write(row, 2, ' ', wbf['total_content'])
                worksheet.write(row, 3, ' ', wbf['total_content'])
                worksheet.write(row, 4, ' ', wbf['total_content'])
                worksheet.write(row, 5, ' ', wbf['total_content'])
                worksheet.write(row, 6, ' ', wbf['total_content'])
                worksheet.write(row, 7, ' ', wbf['total_content'])
                worksheet.write(row, 8, ' ', wbf['total_content'])
                worksheet.write(row, 9, ' ', wbf['total_content'])
                worksheet.write(row, 10, ' ', wbf['total_content'])
                worksheet.write(row, 11, ' ', wbf['total_content'])
                worksheet.write(row, 12, ' ', wbf['total_content_float_price'])
                worksheet.write(row, 13, ' ', wbf['total_content_float_price'])
                worksheet.write(row, 14, cl_total_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 15, cl_total_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 16, cl_whbb_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 17, cl_bbflg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 18, cl_bbflg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 19, cl_bbbbg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 20, cl_bbbbg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 21, cl_bbbwk_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 22, cl_bbbwk_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 23, cl_bbbrw_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 24, cl_bbbrw_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 25, cl_bbpdg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 26, cl_bbpdg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 27, cl_bbsyv_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 28, cl_bbsyv_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 29, cl_bbglr_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 30, cl_bbglr_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 31, cl_bbblg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 32, cl_bbblg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 33, cl_bbsnr_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 34, cl_bbsnr_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 35, cl_bbptg_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 36, cl_bbptg_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 37, cl_bbkta_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 38, cl_bbkta_qty_stock or ' ', wbf['total_content_float'])
                worksheet.write(row, 39, cl_online_qty_sold or ' ', wbf['total_content_float'])
                worksheet.write(row, 40, cl_online_qty_stock or ' ', wbf['total_content_float'])

                gt_total_qty_sold += cl_total_qty_sold
                gt_total_qty_stock += cl_total_qty_stock
                gt_whbb_qty_sold += cl_whbb_qty_sold
                gt_bbflg_qty_sold += cl_bbflg_qty_sold
                gt_bbbbg_qty_sold += cl_bbbbg_qty_sold
                gt_bbbwk_qty_sold += cl_bbbwk_qty_sold
                gt_bbbrw_qty_sold += cl_bbbrw_qty_sold
                gt_bbpdg_qty_sold += cl_bbpdg_qty_sold
                gt_bbsyv_qty_sold += cl_bbsyv_qty_sold
                gt_bbglr_qty_sold += cl_bbglr_qty_sold
                gt_bbblg_qty_sold += cl_bbblg_qty_sold
                gt_bbsnr_qty_sold += cl_bbsnr_qty_sold
                gt_bbptg_qty_sold += cl_bbptg_qty_sold
                gt_bbkta_qty_sold += cl_bbkta_qty_sold
                gt_online_qty_sold += cl_online_qty_sold
                gt_whbb_qty_stock += cl_whbb_qty_stock
                gt_bbflg_qty_stock += cl_bbflg_qty_stock
                gt_bbbbg_qty_stock += cl_bbbbg_qty_stock
                gt_bbbwk_qty_stock += cl_bbbwk_qty_stock
                gt_bbbrw_qty_stock += cl_bbbrw_qty_stock
                gt_bbpdg_qty_stock += cl_bbpdg_qty_stock
                gt_bbsyv_qty_stock += cl_bbsyv_qty_stock
                gt_bbglr_qty_stock += cl_bbglr_qty_stock
                gt_bbblg_qty_stock += cl_bbblg_qty_stock
                gt_bbsnr_qty_stock += cl_bbsnr_qty_stock
                gt_bbptg_qty_stock += cl_bbptg_qty_stock
                gt_bbkta_qty_stock += cl_bbkta_qty_stock
                gt_online_qty_stock += cl_online_qty_stock


            worksheet.write(row, 0, 'GRAND TOTAL', wbf['total_content'])
            worksheet.write(row, 1, ' ', wbf['total_content'])
            worksheet.write(row, 2, ' ', wbf['total_content'])
            worksheet.write(row, 3, ' ', wbf['total_content'])
            worksheet.write(row, 4, ' ', wbf['total_content'])
            worksheet.write(row, 5, ' ', wbf['total_content'])
            worksheet.write(row, 6, ' ', wbf['total_content'])
            worksheet.write(row, 7, ' ', wbf['total_content'])
            worksheet.write(row, 8, ' ', wbf['total_content'])
            worksheet.write(row, 9, ' ', wbf['total_content'])
            worksheet.write(row, 10, ' ', wbf['total_content'])
            worksheet.write(row, 11, ' ', wbf['total_content'])
            worksheet.write(row, 12, ' ', wbf['total_content_float_price'])
            worksheet.write(row, 13, ' ', wbf['total_content_float_price'])
            worksheet.write(row, 14, gt_total_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 15, gt_total_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 16, gt_whbb_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 17, gt_bbflg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 18, gt_bbflg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 19, gt_bbbbg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 20, gt_bbbbg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 21, gt_bbbwk_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 22, gt_bbbwk_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 23, gt_bbbrw_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 24, gt_bbbrw_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 25, gt_bbpdg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 26, gt_bbpdg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 27, gt_bbsyv_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 28, gt_bbsyv_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 29, gt_bbglr_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 30, gt_bbglr_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 31, gt_bbblg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 32, gt_bbblg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 33, gt_bbsnr_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 34, gt_bbsnr_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 35, gt_bbptg_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 36, gt_bbptg_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 37, gt_bbkta_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 38, gt_bbkta_qty_stock or ' ', wbf['total_content_float'])
            worksheet.write(row, 39, gt_online_qty_sold or ' ', wbf['total_content_float'])
            worksheet.write(row, 40, gt_online_qty_stock or ' ', wbf['total_content_float'])

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
            'pink': '#FFC0CB',
            'violet': '#EE82EE',
            'green': '#00FF7F',
            'light_green': '#90EE90',
            'dark_green': '#8FBC8F',
            'blue': '#DCE6F1',
            'brown': '#DDD9C4',
            'salmon': '#FFA07A',
            'beige': '#F5F5DC',
        }

        wbf = {}
        wbf['header'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': '#FFFFFF', 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header'].set_border()

        wbf['header_brown'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['brown'], 'font_color': '#000000'})
        wbf['header_brown'].set_border()

        wbf['header_salmon'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['salmon'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_salmon'].set_border()

        wbf['header_beige'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['beige'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_beige'].set_border()

        wbf['header_blue'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['blue'], 'font_color': '#000000'})
        wbf['header_blue'].set_border()

        wbf['header_blue2'] = workbook.add_format(
            {'bold': 1, 'align': 'left', 'bg_color': colors['blue'], 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_blue2'].set_border()

        wbf['header_green'] = workbook.add_format(
            {'font_size': 11, 'italic': 1, 'bold': 1, 'align': 'center', 'bg_color': colors['green'], 'font_color': '#000000'})
        wbf['header_green'].set_border()

        wbf['header_light_green'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['light_green'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_light_green'].set_border()

        wbf['header_dark_green'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['dark_green'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_dark_green'].set_border()

        wbf['header_pink'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['pink'], 'font_color': '#000000'})
        wbf['header_pink'].set_border()

        wbf['header_violet'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['violet'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_violet'].set_border()

        wbf['header_orange'] = workbook.add_format(
            {'font_size': 11, 'italic': 1, 'bold': 1, 'align': 'center', 'bg_color': colors['orange'], 'font_color': '#000000'})
        wbf['header_orange'].set_border()

        wbf['header_white_orange'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['white_orange'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_white_orange'].set_border()

        wbf['header_yellow'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['yellow'], 'font_color': '#000000'})
        # wbf['header_yellow'] = self.format
        wbf['header_yellow'].set_border()

        wbf['header_no'] = workbook.add_format(
            {'font_size': 11, 'italic': 1, 'bold': 1, 'align': 'center', 'bg_color': '#D8E4BC', 'font_color': '#000000'})
        wbf['header_no'].set_border()
        wbf['header_no'].set_align('vcenter')

        wbf['footer'] = workbook.add_format({'align': 'left', 'font_name': 'Georgia'})

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
            'font_size': 11,
            'bg_color': '#FFC0CB',
        })

        wbf['title_doc_brown'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 11,
            'bg_color': '#FFEFD5',
        })

        wbf['title_doc'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 20,
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

        wbf['content'] = workbook.add_format({'valign': 'vcenter', 'align': 'left', 'border': 1, 'text_wrap': True})
        wbf['content'].set_left()
        wbf['content'].set_right()

        wbf['content2'] = workbook.add_format({'valign': 'vcenter', 'align': 'center', 'border': 1, 'text_wrap': True})
        wbf['content2'].set_left()
        wbf['content2'].set_right()

        wbf['total_content'] = workbook.add_format(
            {'font_size': 11, 'bold': 1, 'valign': 'vcenter', 'align': 'left', 'border': 1, 'text_wrap': True, 'bg_color': colors['blue'], 'font_color': '#000000'})
        wbf['total_content'].set_border()

        wbf['total_content_image'] = workbook.add_format(
            {'font_size': 11, 'bold': 1, 'align': 'centre', 'text_wrap': True, 'bg_color': colors['blue'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['total_content_image'].set_border()

        wbf['total_content2'] = workbook.add_format(
            {'font_size': 11, 'bold': 1, 'align': 'center', 'bg_color': colors['blue'], 'font_color': '#000000'})
        wbf['total_content2'].set_border()

        wbf['total_content_float'] = workbook.add_format(
            {'font_size': 11, 'bold': True, 'align': 'right', 'num_format': '#,##0',
             'bg_color': colors['blue'], 'font_color': '#000000', 'valign': 'vcenter', 'border': 1})
        wbf['total_content_float'].set_border()

        wbf['total_content_float_brown'] = workbook.add_format(
            {'font_size': 11, 'bold': True, 'align': 'right', 'num_format': '#,##0',
             'bg_color': colors['brown'], 'font_color': '#000000', 'valign': 'vcenter', 'border': 1})
        wbf['total_content_float_brown'].set_border()

        wbf['total_content_float_price'] = workbook.add_format(
            {'font_size': 11, 'bold': True, 'align': 'right', 'num_format': '#,##0',
             'bg_color': colors['blue'], 'font_color': '#000000', 'valign': 'vcenter', 'border': 1})
        wbf['total_content_float_price'].set_border()

        wbf['content_float'] = workbook.add_format(
            {'font_size': 11, 'bold': True, 'align': 'right', 'num_format': '#,##0', 'valign': 'vcenter', 'border': 1,})
        wbf['content_float'].set_right()
        wbf['content_float'].set_left()

        wbf['content_float_price'] = workbook.add_format(
            {'font_size': 11, 'align': 'right', 'num_format': '#,##0', 'valign': 'vcenter', 'border': 1,})
        wbf['content_float_price'].set_right()
        wbf['content_float_price'].set_left()

        wbf['content_number'] = workbook.add_format({'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_number'].set_right()
        wbf['content_number'].set_left()

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
