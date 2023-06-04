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
from odoo.tools import html2plaintext

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
    parent_categ_id = fields.Many2one('product.category', 'Model', domain=[('category_product', '=', 'department')])
    class_id = fields.Many2one('class.product', 'Class')
    types = fields.Selection([('staples','Staples'),('trend','Trend')], string='Type')
    start_aging = fields.Integer('Start Aging')
    end_aging = fields.Integer('End Aging')
    pos_config_id = fields.Many2one('pos.config', string='Store')

    @api.onchange('parent_categ_id')
    def onchange_domain_product_category_id(self):
        if self.categ_id:
            self.write({'categ_id': False})
        if self.parent_categ_id:
            domain = [('category_product', '=', 'category'), ('parent_id', '=', self.parent_categ_id.id)]
            return {'domain': {'categ_id': domain}}
        else:
            return {}

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

        # worksheet = workbook.add_worksheet(report_name)

        # header_table_real = ['Model', 'Category', 'Style', 'Stock Name', 'Stock ID', 'Color', 'Photo', 'Aging', 'Barcode', 'Size', 'Order Notes', 'Cost Price', 'Retail Price', 'Qty Sold', 'In Stock', 'In Stock']
        header_table_real = ['Category', 'Style', 'Stock Name', 'Stock ID', 'Color', 'Photo', 'Aging', 'Barcode', 'Size', 'Cost Price', 'Retail Price', 'Qty Sold', 'In Stock', 'In Stock']

        formatHeaderCompany = workbook.add_format({'font_size': 14, 'valign':'vcenter', 'align': 'center', 'bold': True})
        formatHeaderTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bold': True, 'bg_color':'#8db4e2', 'color':'black', 'text_wrap': True, 'border': 1})
        formatHeaderTableSand = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bold': True, 'bg_color':'#e5b776', 'color':'black', 'text_wrap': True, 'border': 1})
        formatNormal = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'left', 'bold': True})
        formatNormalCenter = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'center', 'text_wrap': True, 'bold': True})
        formatNormalCurrencyCenter = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'center', 'num_format': '_-"Rp"* #,##0.00_-;-"Rp"* #,##0.00_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'bold': True})
        formatDetailTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'text_wrap': True, 'border': 1})
        formatDetailCurrencyTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0.00_-;-"Rp"* #,##0.00_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrderBlue = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bg_color':'#8db4e2', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrderSand = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bg_color':'#e5b776', 'text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrderBlue = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bg_color':'#8db4e2', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatImage = workbook.add_format({'text_wrap': True, 'border': 1})

        dt_class_product = self.class_id.id
        dt_product_model_id = self.parent_categ_id.id
        dt_product_category_id = self.categ_id.id
        dt_types = self.types
        # dt_stock_type = datas.get('stock_type', False)
        dt_pos_config_id = self.pos_config_id.id
        dt_aging_from = self.start_aging
        dt_aging_to = self.end_aging

        dt_from_date = self.start_period.strftime('%Y-%m-%d')
        dt_to_date = self.end_period.strftime('%Y-%m-%d')

        # product_model_id = self.env['product.model'].sudo().browse(dt_product_model_id)
        product_model_id = self.env['product.category'].sudo().browse(dt_product_model_id)
        
        if dt_pos_config_id:
            pos_order_line = self.env['pos.order.line'].sudo().search([
                ('order_id.date_order', '>=', dt_from_date),
                ('order_id.date_order', '<=', dt_to_date),
                ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
                ('order_id.session_id.config_id', '=', dt_pos_config_id),
            ])
        else:
            pos_order_line = self.env['pos.order.line'].sudo().search([
                ('order_id.date_order', '>=', dt_from_date),
                ('order_id.date_order', '<=', dt_to_date),
                ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
            ])

        # if dt_product_category_id:
        #     product_tmpl_ids = self.env['product.template'].sudo().search([
        #         ('active', '=', True),
        #         ('types', '=', dt_types),
        #         '|',
        #         ('categ_id', '=', dt_product_category_id),
        #         ('categ_id.parent_id', '=', dt_product_category_id)
        #     ])
        # else:
        #     product_tmpl_ids = self.env['product.template'].sudo().search([
        #         ('active', '=', True),
        #         ('types', '=', dt_types),
        #         '|',
        #         '|',
        #         ('categ_id', '=', dt_product_model_id),
        #         ('categ_id.parent_id', '=', dt_product_model_id),
        #         ('categ_id.parent_id.parent_id', '=', dt_product_model_id)
        #     ])

        if dt_product_category_id:
            categ_ids = self.env['product.category'].sudo().browse(dt_product_category_id)
        else:
            categ_ids = self.env['product.category'].sudo().search([('parent_id', '=', dt_product_model_id)])

        warehouse_name_ids = pos_order_line.mapped('order_id.picking_type_id.warehouse_id.name')
        warehouse_ids = pos_order_line.mapped('order_id.picking_type_id.warehouse_id.id')

        from_date = datetime.strptime(dt_from_date, '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(dt_to_date, '%Y-%m-%d').strftime('%d/%m/%Y')

        date_period = (datetime.strptime(dt_to_date, '%Y-%m-%d') - datetime.strptime(dt_from_date, '%Y-%m-%d')).days

        sheet = workbook.add_worksheet(f'{product_model_id.name}')
        row = 1
        sheet.merge_range(row, 0, row, len(header_table_real)-1, f'SLOW SELLING {product_model_id.name}', formatNormal)
        row += 1
        sheet.merge_range(row, 0, row, len(header_table_real)-1, f'PERIODE SALES : {from_date} - {to_date}', formatNormal)
        row += 1
        sheet.merge_range(row, 0, row, len(header_table_real)-1, f'Data Last Stock : {to_date}', formatNormal)
        row += 1

        for categ in categ_ids:
            product_tmpl_ids = self.env['product.template'].sudo().search([
                # ('active', '=', True),
                ('types', '=', dt_types),
                '|',
                ('categ_id', '=', categ.id),
                ('categ_id.parent_id', '=', categ.id),
                '|',
                ('active', '=', True),
                ('active', '!=', True)
            ])
            # header_table = []
            header_table = header_table_real.copy()
            # row += 1
            # column = len(header_table)
            # grand_column = len(header_table)
            # sheet.merge_range(row, column-3, row, column-2, 'SUMMARY TOTAL', formatHeaderTableSand)
            # sheet.write(row, column-1, 'WH', formatHeaderTableSand)
            # for warehouse in warehouse_name_ids:
            #     sheet.merge_range(row, column, row, column+1, warehouse.upper(), formatHeaderTableSand)
            #     column += 2
            #     header_table += ['Qty Sold', 'In Stock']

            # row += 1
            # column = 0
            # for header in header_table:
            #     sheet.write(row, column, header.upper(), formatHeaderTable)
            #     column += 1

            # for x in range(0, len(header_table)):
            #     sheet.set_column(x, x, 15)
            
            # row += 1
            pt_temp = False
            wh_temp = False
            grand_total_qty_sale_retail = 0
            grand_total_qty_stock_retail = 0
            grand_total_qty_stock_warehouse = 0
            all_stock_retail = {'grand_total': {}, 'qty': {}}
            all_sale_retail = {'grand_total': {}, 'qty': {}}

            # raw_data = [
            #     {'model': '', 'category': '', 'style': '', 'all_qty_sale_retail': 0, 'all_qty_stock_retail': 0, 'all_qty_stock_warehouse': 0, 'order_line': []}
            #     ]
            raw_data = []
            # raw_data_dict = {'model': '', 'category': '', 'style': '', 'all_qty_sale_retail': 0, 'all_qty_stock_retail': 0, 'all_qty_stock_warehouse': 0, 'order_line': []}

            for pt in product_tmpl_ids:
                list_color = ['COLOR','COLOUR','COLOURS','COLORS','WARNA','CORAK']
                product_color_ids = pt.attribute_line_ids.filtered(lambda x: x.attribute_id.name in list_color).value_ids
                for product_color_id in product_color_ids:
                    product_product_color_ids = self.env['product.product'].sudo().search([
                        ('product_tmpl_id', '=', pt.id),
                        # ('stock_type', '=', dt_stock_type),
                        ('class_product', '=', dt_class_product),
                        '|',
                        ('active', '=', True),
                        ('active', '!=', True)
                    ])
                    product_product_ids = product_product_color_ids.filtered(lambda x: product_color_id.name in x.product_template_variant_value_ids.mapped('name'))
                    all_qty_sale_retail = 0
                    all_qty_stock_retail = 0
                    all_qty_stock_warehouse = 0
                    model = product_model_id.name or ''
                    # category = pt.categ_id.parent_id.name or '' if pt.categ_id.category_product == 'subcategory' else pt.categ_id.name or ''
                    category = categ.name
                    style = ''
                    akumulasi_stock_retail = 0
                    akumulasi_sale_retail = 0

                    len_product = len(product_product_ids)
                    iterasi = 0
                    raw_data_order_line_dict = {}
                    raw_data_dict = {'model': '', 'category': '', 'style': '', 'all_qty_sale_retail': 0, 'all_qty_stock_retail': 0, 'all_qty_stock_warehouse': 0, 'order_line': []}
                    for pp in product_product_ids:
                        stock_move_ids = self.env['stock.move'].sudo().search([
                            ('date', '<=', dt_to_date),
                            ('state', '=', 'done'),
                            ('product_id', '=', pp.id),
                        ], order='date asc', limit=1)
                        diff_date_in_week = int(round((fields.Date.today() - stock_move_ids.date.date()).days / 7, 0)) if stock_move_ids.date else 0

                        if not (dt_aging_to > diff_date_in_week > dt_aging_from) and (dt_aging_to > 0 or dt_aging_from > 0):
                            len_product = len_product - 1


                            # Sum Variant Stock
                            if len_product > 0 and iterasi == len_product:
                                raw_data_dict['model'] = model
                                raw_data_dict['category'] = category
                                raw_data_dict['style'] = f'{style} - Total'
                                raw_data_dict['all_qty_sale_retail'] = all_qty_sale_retail
                                raw_data_dict['all_qty_stock_retail'] = all_qty_stock_retail
                                raw_data_dict['all_qty_stock_warehouse'] = all_qty_stock_warehouse

                                # sheet.write(row, 0, model, formatDetailTableReOrderBlue)
                                # sheet.write(row, 1, category, formatDetailTableReOrderBlue)
                                # sheet.write(row, 2, f'{style} - Total', formatDetailTableReOrderBlue)
                                # sheet.write(row, 3, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 4, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 5, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 6, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 7, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 8, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 9, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 10, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 11, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 12, all_qty_sale_retail, formatDetailTableReOrderBlue)
                                # sheet.write(row, 13, all_qty_stock_retail, formatDetailTableReOrderBlue)
                                # sheet.write(row, 14, all_qty_stock_warehouse, formatDetailTableReOrderBlue)

                                grand_total_qty_sale_retail += all_qty_sale_retail
                                grand_total_qty_stock_retail += all_qty_stock_retail
                                grand_total_qty_stock_warehouse += all_qty_stock_warehouse
                                column_3 = 14
                                for wh in warehouse_ids:
                                    raw_data_dict[wh] = {}
                                    column_3 += 1
                                    if wh in all_sale_retail['qty']:
                                        # sheet.write(row, column_3, all_sale_retail['qty'][wh], formatDetailTableReOrderBlue)
                                        raw_data_dict[wh]['all_sale_retail'] = all_sale_retail['qty'][wh]
                                    else:
                                        # sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                                        raw_data_dict[wh]['all_sale_retail'] = 0
                                    column_3 += 1
                                    if wh in all_stock_retail['qty']:
                                        # sheet.write(row, column_3, all_stock_retail['qty'][wh], formatDetailTableReOrderBlue)
                                        raw_data_dict[wh]['all_stock_retail'] = all_stock_retail['qty'][wh]
                                    else:
                                        # sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                                        raw_data_dict[wh]['all_stock_retail'] = 0
                                raw_data.append(raw_data_dict)
                                # row += 1
                            continue

                        if diff_date_in_week < 1:
                            len_product = len_product - 1

                            # Sum Variant Stock
                            if len_product > 0 and iterasi == len_product:
                                raw_data_dict['model'] = model
                                raw_data_dict['category'] = category
                                raw_data_dict['style'] = f'{style} - Total'
                                raw_data_dict['all_qty_sale_retail'] = all_qty_sale_retail
                                raw_data_dict['all_qty_stock_retail'] = all_qty_stock_retail
                                raw_data_dict['all_qty_stock_warehouse'] = all_qty_stock_warehouse

                                # sheet.write(row, 0, model, formatDetailTableReOrderBlue)
                                # sheet.write(row, 1, category, formatDetailTableReOrderBlue)
                                # sheet.write(row, 2, f'{style} - Total', formatDetailTableReOrderBlue)
                                # sheet.write(row, 3, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 4, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 5, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 6, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 7, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 8, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 9, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 10, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 11, '', formatDetailTableReOrderBlue)
                                # sheet.write(row, 12, all_qty_sale_retail, formatDetailTableReOrderBlue)
                                # sheet.write(row, 13, all_qty_stock_retail, formatDetailTableReOrderBlue)
                                # sheet.write(row, 14, all_qty_stock_warehouse, formatDetailTableReOrderBlue)

                                grand_total_qty_sale_retail += all_qty_sale_retail
                                grand_total_qty_stock_retail += all_qty_stock_retail
                                grand_total_qty_stock_warehouse += all_qty_stock_warehouse
                                column_3 = 14
                                for wh in warehouse_ids:
                                    raw_data_dict[wh] = {}
                                    column_3 += 1
                                    if wh in all_sale_retail['qty']:
                                        # sheet.write(row, column_3, all_sale_retail['qty'][wh], formatDetailTableReOrderBlue)
                                        raw_data_dict[wh]['all_sale_retail'] = all_sale_retail['qty'][wh]
                                    else:
                                        # sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                                        raw_data_dict[wh]['all_sale_retail'] = 0
                                    column_3 += 1
                                    if wh in all_stock_retail['qty']:
                                        # sheet.write(row, column_3, all_stock_retail['qty'][wh], formatDetailTableReOrderBlue)
                                        raw_data_dict[wh]['all_stock_retail'] = all_stock_retail['qty'][wh]
                                    else:
                                        # sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                                        raw_data_dict[wh]['all_stock_retail'] = 0
                                raw_data.append(raw_data_dict)
                                # row += 1
                            continue

                        list_size = ['SIZE','SIZES','UKURAN']
                        list_color = ['COLOR:','COLOUR:','COLOURS:','COLORS:','WARNA:','CORAK:']
                        color = ''
                        size = ''
                        for v in pp.product_template_variant_value_ids:
                            if any(v.display_name.upper().startswith(word) for word in list_size):
                                size += v.name
                            if any(v.display_name.upper().startswith(word) for word in list_color):
                                color += v.name

                        style = f'{pp.name} - {color}' or ''
                        stockname = pp.name or ''
                        stockid = pp.default_code or ''
                        aging = diff_date_in_week
                        barcode = pp.barcode or ''
                        photo = pp.image_1920

                        last_po_id = self.env['purchase.order.line'].sudo().search([
                            ('order_id.date_order', '>=', dt_from_date),
                            ('order_id.date_order', '<=', dt_to_date),
                            ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS'), 
                            ('product_id', '=', pp.id), 
                            ('order_id.state', 'in', ['purchase', 'done'])
                        ], limit=1)

                        order_notes = html2plaintext(last_po_id.order_id.notes or '').strip()
                        # order_notes = html2plaintext(pp.order_notes or '').strip()
                        cost = pp.standard_price or 0
                        sale_price = pp.list_price or 0
                        total_qty_sale_retail = 0
                        total_qty_stock_retail = 0
                        total_qty_stock_warehouse = 0

                        stock_quant_whbb = self.env['stock.quant'].sudo().search([
                            ('location_id', 'ilike', 'whbb/stock'),
                            ('product_id', '=', pp.id),
                        ])
                        if stock_quant_whbb:
                            total_qty_stock_warehouse = stock_quant_whbb.quantity

                        # Tidak ada Penjumlahan
                        # Develop Baru
                        raw_data_order_line_dict = {
                            'model': model,
                            'category': category,
                            'style': style,
                            'stockname': stockname,
                            'stockid': stockid,
                            'color': color,
                            'photo': photo,
                            'aging': aging,
                            'barcode': barcode,
                            'size': size,
                            'order_notes': order_notes,
                            'cost': cost,
                            'sale_price': sale_price,
                        }

                        # sheet.write(row, 0, model, formatDetailTableReOrder)
                        # sheet.write(row, 1, category, formatDetailTableReOrder)
                        # sheet.write(row, 2, style, formatDetailTableReOrder)
                        # sheet.write(row, 3, stockname, formatDetailTableReOrder)
                        # sheet.write(row, 4, stockid, formatDetailTableReOrder)
                        # sheet.write(row, 5, color, formatDetailTableReOrder)
                        # sheet.write(row, 6, aging, formatDetailTableReOrder)
                        # sheet.write(row, 7, barcode, formatDetailTableReOrder)
                        # sheet.write(row, 8, size, formatDetailTableReOrder)
                        # sheet.write(row, 9, order_notes, formatDetailTableReOrder)
                        # sheet.write(row, 10, cost, formatDetailCurrencyTableReOrder)
                        # sheet.write(row, 11, sale_price, formatDetailCurrencyTableReOrder)

                        column_2 = 5
                        for wh in self.env['stock.warehouse'].sudo().browse(warehouse_ids):
                            stock_quant = self.env['stock.quant'].sudo().search([
                                ('location_id', '=', wh.lot_stock_id.id),
                                ('product_id', '=', pp.id),
                            ])
                            pos_order_line = self.env['pos.order.line'].sudo().search([
                                ('order_id.date_order', '>=', dt_from_date),
                                ('order_id.date_order', '<=', dt_to_date),
                                ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
                                ('product_id', '=', pp.id),
                                ('order_id.picking_type_id.warehouse_id', '=', wh.id),
                            ])
                            qty_stock_retail = stock_quant.quantity
                            total_qty_stock_retail += qty_stock_retail
                            qty_sale_retail = sum(pos_order_line.mapped('qty'))
                            total_qty_sale_retail += qty_sale_retail

                            # Develop Baru
                            raw_data_order_line_dict[wh.id] = {'qty_sale_retail': qty_sale_retail, 'qty_stock_retail': qty_stock_retail}

                            column_2 += 1
                            # sheet.write(row, column_2, qty_sale_retail, formatDetailTableReOrderSand)
                            column_2 += 1
                            # sheet.write(row, column_2, qty_stock_retail, formatDetailTableReOrder)

                            if wh.id not in all_stock_retail['grand_total']:
                                all_stock_retail['grand_total'].update({wh.id: 0})
                                all_sale_retail['grand_total'].update({wh.id: 0})

                            if pt.id != pt_temp or wh.id not in all_stock_retail['qty']:
                                if pt.id != pt_temp:
                                    all_stock_retail['qty'] = {}
                                    all_sale_retail['qty'] = {}
                                all_stock_retail['qty'].update({wh.id: 0})
                                all_sale_retail['qty'].update({wh.id: 0})
                                pt_temp = pt.id
                                wh_temp = wh.id
                            all_stock_retail['qty'][wh.id] += qty_stock_retail
                            all_sale_retail['qty'][wh.id] += qty_sale_retail
                            all_stock_retail['grand_total'][wh.id] += qty_stock_retail
                            all_sale_retail['grand_total'][wh.id] += qty_sale_retail

                            # if pt.id != pt_temp or wh.id != wh_temp:
                            #     all_stock_retail[wh.id] = {'qty': 0}
                            #     all_sale_retail[wh.id] = {'qty': 0}
                            #     pt_temp = pt.id
                            #     wh_temp = wh.id
                            # all_stock_retail[wh.id]['qty'] += qty_stock_retail
                            # all_sale_retail[wh.id]['qty'] += qty_sale_retail
                        
                        # Column Summary Total dan WH
                        # Develop Baru
                        raw_data_order_line_dict['total_qty_sale_retail'] = total_qty_sale_retail
                        raw_data_order_line_dict['total_qty_stock_retail'] = total_qty_stock_retail
                        raw_data_order_line_dict['total_qty_stock_warehouse'] = total_qty_stock_warehouse

                        # sheet.write(row, 12, total_qty_sale_retail, formatDetailTableReOrderSand)
                        # sheet.write(row, 13, total_qty_stock_retail, formatDetailTableReOrder)
                        # sheet.write(row, 14, total_qty_stock_warehouse, formatDetailTableReOrder)
                        
                        all_qty_stock_retail += total_qty_stock_retail
                        all_qty_sale_retail += total_qty_sale_retail
                        all_qty_stock_warehouse += total_qty_stock_warehouse
                        # row += 1
                        iterasi += 1

                        # raw_data['order_line'].append(raw_data_order_line_dict)
                        raw_data_dict['order_line'] += [raw_data_order_line_dict]
                    
                        # SUM Variant Stock
                        if iterasi == len_product:
                            
                            raw_data_dict['model'] = model
                            raw_data_dict['category'] = category
                            raw_data_dict['style'] = f'{style} - Total'
                            raw_data_dict['all_qty_sale_retail'] = all_qty_sale_retail
                            raw_data_dict['all_qty_stock_retail'] = all_qty_stock_retail
                            raw_data_dict['all_qty_stock_warehouse'] = all_qty_stock_warehouse

                            # sheet.write(row, 0, model, formatDetailTableReOrderBlue)
                            # sheet.write(row, 1, category, formatDetailTableReOrderBlue)
                            # sheet.write(row, 2, f'{style} - Total', formatDetailTableReOrderBlue)
                            # sheet.write(row, 3, '', formatDetailTableReOrderBlue)
                            # sheet.write(row, 4, '', formatDetailTableReOrderBlue)
                            # sheet.write(row, 5, '', formatDetailTableReOrderBlue)
                            # sheet.write(row, 6, '', formatDetailTableReOrderBlue)
                            # sheet.write(row, 7, '', formatDetailTableReOrderBlue)
                            # sheet.write(row, 8, '', formatDetailTableReOrderBlue)
                            # sheet.write(row, 9, '', formatDetailTableReOrderBlue)
                            # sheet.write(row, 10, '', formatDetailTableReOrderBlue)
                            # sheet.write(row, 11, '', formatDetailTableReOrderBlue)
                            # sheet.write(row, 12, all_qty_sale_retail, formatDetailTableReOrderBlue)
                            # sheet.write(row, 13, all_qty_stock_retail, formatDetailTableReOrderBlue)
                            # sheet.write(row, 14, all_qty_stock_warehouse, formatDetailTableReOrderBlue)

                            grand_total_qty_sale_retail += all_qty_sale_retail
                            grand_total_qty_stock_retail += all_qty_stock_retail
                            grand_total_qty_stock_warehouse += all_qty_stock_warehouse
                            column_3 = 15
                            for wh in warehouse_ids:
                                raw_data_dict[wh] = {}
                                column_3 += 1
                                if wh in all_sale_retail['qty']:
                                    # sheet.write(row, column_3, all_sale_retail['qty'][wh], formatDetailTableReOrderBlue)
                                    raw_data_dict[wh]['all_sale_retail'] = all_sale_retail['qty'][wh]
                                else:
                                    # sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                                    raw_data_dict[wh]['all_sale_retail'] = 0
                                column_3 += 1
                                if wh in all_stock_retail['qty']:
                                    # sheet.write(row, column_3, all_stock_retail['qty'][wh], formatDetailTableReOrderBlue)
                                    raw_data_dict[wh]['all_stock_retail'] = all_stock_retail['qty'][wh]
                                else:
                                    # sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                                    raw_data_dict[wh]['all_stock_retail'] = 0
                            raw_data.append(raw_data_dict)
                            # row += 1
                
            data_grand_total = {'grand_total_qty_sale_retail': 0, 'grand_total_qty_stock_retail': 0, 'grand_total_qty_stock_warehouse': 0, 'gt_sale_retail': {}, 'gt_stock_retail': {}}
            # number_of_best_product = product_model_id.number_of_best_product
            number_of_slow_product = categ.number_of_slow_product
            if raw_data:
                filter_raw_data = []
                if date_period < 21:
                    filter_raw_data = [x for x in raw_data if x['all_qty_sale_retail'] > 0 and x['all_qty_sale_retail'] <= product_model_id.slow_less_than_one_month]
                else:
                    filter_raw_data = [x for x in raw_data if x['all_qty_sale_retail'] > 0 and x['all_qty_sale_retail'] <= product_model_id.slow_more_than_one_month]
                
                if not filter_raw_data:
                    continue

                new_raw_data = sorted(filter_raw_data, key=lambda d: d['all_qty_sale_retail'])
                max_data = new_raw_data[:number_of_slow_product] if number_of_slow_product else new_raw_data

                # Header
                header_table = header_table_real.copy()
                row += 1
                column = len(header_table)
                grand_column = len(header_table)
                sheet.merge_range(row, column-3, row, column-2, 'SUMMARY TOTAL', formatHeaderTableSand)
                sheet.write(row, column-1, 'WH', formatHeaderTableSand)
                for warehouse in warehouse_name_ids:
                    sheet.merge_range(row, column, row, column+1, warehouse.upper(), formatHeaderTableSand)
                    column += 2
                    header_table += ['Qty Sold', 'In Stock']
                row += 1
                column = 0
                for header in header_table:
                    sheet.write(row, column, header.upper(), formatHeaderTable)
                    column += 1
                for x in range(0, len(header_table)):
                    sheet.set_column(x, x, 15)
                row += 1

                # Detail
                # for zz in new_raw_data[:number_of_best_product]:
                for zz in max_data:
                    if date_period < 21:
                        if not (zz['all_qty_sale_retail'] <= product_model_id.slow_less_than_one_month):
                            continue
                    else:
                        if not (zz['all_qty_sale_retail'] <= product_model_id.slow_more_than_one_month):
                            continue

                    for xx in zz['order_line']:
                        d_photo = ''
                        resize_scale = 0
                        if xx['photo']:
                            d_photo = io.BytesIO(base64.b64decode(xx['photo']))
                            bound_width_height = (80, 80)
                            if d_photo:
                                resize_scale = calculate_scale(d_photo, bound_width_height)

                        # sheet.write(row, 0, xx['model'], formatDetailTableReOrder)
                        sheet.write(row, 0, xx['category'], formatDetailTableReOrder)
                        sheet.write(row, 1, xx['style'], formatDetailTableReOrder)
                        sheet.write(row, 2, xx['stockname'], formatDetailTableReOrder)
                        sheet.write(row, 3, xx['stockid'], formatDetailTableReOrder)
                        sheet.write(row, 4, xx['color'], formatDetailTableReOrder)

                        # sheet.write(row, 6, xx['photo'], formatDetailTableReOrder)
                        sheet.set_column(row, 5, 15)
                        sheet.set_row(row, 75)
                        if xx['photo']:
                            sheet.insert_image(row, 5, "image.png", {'image_data': d_photo, 'bg_color': '#FFFFFF', 'x_scale': resize_scale, 'y_scale': resize_scale, 'x_offset': 10, 'y_offset': 10})
                        else:
                            sheet.write(row, 5, '', formatDetailTableReOrder)

                        sheet.write(row, 6, xx['aging'], formatDetailTableReOrder)
                        sheet.write(row, 7, xx['barcode'], formatDetailTableReOrder)
                        sheet.write(row, 8, xx['size'], formatDetailTableReOrder)
                        # sheet.write(row, 10, xx['order_notes'], formatDetailTableReOrder)
                        sheet.write(row, 9, xx['cost'], formatDetailCurrencyTableReOrder)
                        sheet.write(row, 10, xx['sale_price'], formatDetailCurrencyTableReOrder)
                        sheet.write(row, 11, xx['total_qty_sale_retail'] or '', formatDetailTableReOrderSand)
                        sheet.write(row, 12, xx['total_qty_stock_retail'] or '', formatDetailTableReOrder)
                        sheet.write(row, 13, xx['total_qty_stock_warehouse'] or '', formatDetailTableReOrder)
                        column_2 = 13
                        if warehouse_ids:
                            for ww in warehouse_ids:
                                column_2 += 1
                                sheet.write(row, column_2, xx[ww]['qty_sale_retail'] or '', formatDetailTableReOrderSand)
                                column_2 += 1
                                sheet.write(row, column_2, xx[ww]['qty_stock_retail'] or '', formatDetailTableReOrder)
                        row += 1
                    # sheet.write(row, 0, zz['model'], formatDetailTableReOrderBlue)
                    sheet.write(row, 0, zz['category'], formatDetailTableReOrderBlue)
                    sheet.write(row, 1, zz['style'], formatDetailTableReOrderBlue)
                    sheet.write(row, 2, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 3, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 4, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 5, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 6, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 7, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 8, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 9, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 10, '', formatDetailTableReOrderBlue)
                    # sheet.write(row, 12, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 11, zz['all_qty_sale_retail'] or '', formatDetailTableReOrderBlue)
                    sheet.write(row, 12, zz['all_qty_stock_retail'] or '', formatDetailTableReOrderBlue)
                    sheet.write(row, 13, zz['all_qty_stock_warehouse'] or '', formatDetailTableReOrderBlue)
                    column_3 = 13
                    if warehouse_ids:
                        for ww in warehouse_ids:
                            if ww not in data_grand_total['gt_sale_retail']:
                                data_grand_total['gt_sale_retail'][ww] = 0
                            if ww not in data_grand_total['gt_stock_retail']:
                                data_grand_total['gt_stock_retail'][ww] = 0
                            column_3 += 1
                            sheet.write(row, column_3, zz[ww]['all_sale_retail'] or '', formatDetailTableReOrderBlue)
                            data_grand_total['gt_sale_retail'][ww] += zz[ww]['all_sale_retail']
                            column_3 += 1
                            sheet.write(row, column_3, zz[ww]['all_stock_retail'] or '', formatDetailTableReOrderBlue)
                            data_grand_total['gt_stock_retail'][ww] += zz[ww]['all_stock_retail']

                    data_grand_total['grand_total_qty_sale_retail'] += zz['all_qty_sale_retail']
                    data_grand_total['grand_total_qty_stock_retail'] += zz['all_qty_stock_retail']
                    data_grand_total['grand_total_qty_stock_warehouse'] += zz['all_qty_stock_warehouse']
                    row += 1

                # Footer
                sheet.merge_range(row, 0, row, grand_column-4, f'Grand Total {categ.name}', formatDetailTableReOrderBlue)
                sheet.write(row, 11, data_grand_total['grand_total_qty_sale_retail'] or '', formatDetailTableReOrderBlue)
                sheet.write(row, 12, data_grand_total['grand_total_qty_stock_retail'] or '', formatDetailTableReOrderBlue)
                sheet.write(row, 13, data_grand_total['grand_total_qty_stock_warehouse'] or '', formatDetailTableReOrderBlue)
                column_3 = 13
                for wh in warehouse_ids:
                    column_3 += 1
                    if wh in data_grand_total['gt_sale_retail']:
                        sheet.write(row, column_3, data_grand_total['gt_sale_retail'][wh] or '', formatDetailTableReOrderBlue)
                    else:
                        sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                    column_3 += 1
                    if wh in data_grand_total['gt_stock_retail']:
                        sheet.write(row, column_3, data_grand_total['gt_stock_retail'][wh] or '', formatDetailTableReOrderBlue)
                    else:
                        sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                row += 1
            # sheet.write(row, 12, grand_total_qty_sale_retail, formatDetailTableReOrderBlue)
            # sheet.write(row, 13, grand_total_qty_stock_retail, formatDetailTableReOrderBlue)
            # sheet.write(row, 14, grand_total_qty_stock_warehouse, formatDetailTableReOrderBlue)
            # column_3 = 14
            # for wh in warehouse_ids:
            #     column_3 += 1
            #     if wh in all_sale_retail['grand_total']:
            #         sheet.write(row, column_3, all_sale_retail['grand_total'][wh], formatDetailTableReOrderBlue)
            #     else:
            #         sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
            #     column_3 += 1
            #     if wh in all_stock_retail['grand_total']:
            #         sheet.write(row, column_3, all_stock_retail['grand_total'][wh], formatDetailTableReOrderBlue)
            #     else:
            #         sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
            
            # row += 1
            

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


