from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta

import io
import base64
from PIL import Image


class XlsxMensClothes(models.Model):
    _name = 'report.sol_bb_report.mens_clothes.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):

        def calculate_scale(file_path, bound_size):
            # check the image size without loading it into memory
            im = Image.open(file_path)
            original_width, original_height = im.size

            # calculate the resize factor, keeping original aspect and staying within boundary
            bound_width, bound_height = bound_size
            ratios = (float(bound_width) / original_width, float(bound_height) / original_height)
            return min(ratios)
        
        

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

        datas = data.get('form', {})

        dt_class_product = datas.get('class_product', False)
        dt_product_model_id = datas.get('product_model_id', False)
        dt_product_category_id = datas.get('product_category_id', False)
        dt_types = datas.get('types', False)
        dt_stock_type = datas.get('stock_type', False)
        dt_pos_config_id = datas.get('pos_config_id', False)
        dt_aging_from = datas.get('aging_from', 0)
        dt_aging_to = datas.get('aging_to', 0)
        dt_is_stock_type = datas.get('is_stock_type', False)

        # product_model_id = self.env['product.model'].sudo().browse(dt_product_model_id)
        product_model_id = self.env['product.category'].sudo().browse(dt_product_model_id)
        
        if dt_pos_config_id:
            pos_order_line = self.env['pos.order.line'].sudo().search([
                ('order_id.date_order', '>=', datas.get('from_date')),
                ('order_id.date_order', '<=', datas.get('to_date')),
                ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
                ('order_id.session_id.config_id', '=', dt_pos_config_id),
            ])
            header_table_real = ['Model', 'Category', 'Style', 'Stock Name', 'Stock ID', 'Color', 'Aging', 'Barcode', 'Size', 'Order Notes', 'Cost Price', 'Retail Price', 'In Stock']
            header_table_real_with_stock_type = ['Category', 'Style', 'Stock Name', 'Stock ID', 'Color', 'Stock Type', 'Aging', 'Barcode', 'Size', 'Photo', 'Order Notes', 'Cost Price', 'Retail Price', 'In Stock']
            warehouse_select = True
        else:
            pos_order_line = self.env['pos.order.line'].sudo().search([
                ('order_id.date_order', '>=', datas.get('from_date')),
                ('order_id.date_order', '<=', datas.get('to_date')),
                ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
            ])
            header_table_real = ['Model', 'Category', 'Style', 'Stock Name', 'Stock ID', 'Color', 'Aging', 'Barcode', 'Size', 'Order Notes', 'Cost Price', 'Retail Price', 'Qty Sold', 'In Stock', 'In Stock']
            header_table_real_with_stock_type = ['Category', 'Style', 'Stock Name', 'Stock ID', 'Color', 'Stock Type', 'Aging', 'Barcode', 'Size', 'Photo', 'Order Notes', 'Cost Price', 'Retail Price', 'Qty Sold', 'In Stock', 'In Stock']
            warehouse_select = False


        if dt_product_category_id:
            categ_ids = self.env['product.category'].sudo().browse(dt_product_category_id)
        else:
            categ_ids = self.env['product.category'].sudo().search([('parent_id', '=', dt_product_model_id)])

        warehouse_name_ids = pos_order_line.mapped('order_id.picking_type_id.warehouse_id.name')
        warehouse_ids = pos_order_line.mapped('order_id.picking_type_id.warehouse_id.id')

        from_date = datetime.strptime(datas.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(datas.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')

        date_period = (datetime.strptime(datas.get('to_date'), '%Y-%m-%d') - datetime.strptime(datas.get('from_date'), '%Y-%m-%d')).days

        sheet = workbook.add_worksheet(f'{product_model_id.name}')
        row = 1

        if dt_is_stock_type:
            sheet.merge_range(row, 0, row, len(header_table_real_with_stock_type)-1, f'BEST SELLER {product_model_id.name} WITH STOCK TYPE', formatNormal)
            row += 1
            sheet.merge_range(row, 0, row, len(header_table_real_with_stock_type)-1, f'PERIODE SALES : {from_date} - {to_date}', formatNormal)
            row += 1
            sheet.merge_range(row, 0, row, len(header_table_real_with_stock_type)-1, f'Data Last Stock : {to_date}', formatNormal)
            row += 1
        else:
            sheet.merge_range(row, 0, row, len(header_table_real)-1, f'BEST SELLER {product_model_id.name}', formatNormal)
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
                        ('stock_type', '=', dt_stock_type),
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
                            ('date', '<=', datas.get('to_date')),
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
                        stock_type = pp.stock_type.name or ''
                        photo = pp.image_1920

                        last_po_id = self.env['purchase.order.line'].sudo().search([
                            ('order_id.date_order', '>=', datas.get('from_date')),
                            ('order_id.date_order', '<=', datas.get('to_date')),
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
                            'stock_type': stock_type,
                            'photo': photo,
                            'aging': aging,
                            'barcode': barcode,
                            'size': size,
                            'order_notes': order_notes,
                            'cost': cost,
                            'sale_price': sale_price,
                        }



                        column_2 = 14
                        for wh in self.env['stock.warehouse'].sudo().browse(warehouse_ids):
                            stock_quant = self.env['stock.quant'].sudo().search([
                                ('location_id', '=', wh.lot_stock_id.id),
                                ('product_id', '=', pp.id),
                            ])
                            pos_order_line = self.env['pos.order.line'].sudo().search([
                                ('order_id.date_order', '>=', datas.get('from_date')),
                                ('order_id.date_order', '<=', datas.get('to_date')),
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

                          
                        
                        # Column Summary Total dan WH
                        # Develop Baru
                        raw_data_order_line_dict['total_qty_sale_retail'] = total_qty_sale_retail
                        raw_data_order_line_dict['total_qty_stock_retail'] = total_qty_stock_retail
                        raw_data_order_line_dict['total_qty_stock_warehouse'] = total_qty_stock_warehouse

                   
                        
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
                
            data_grand_total = {'grand_total_qty_sale_retail': 0, 'grand_total_qty_stock_retail': 0, 'grand_total_qty_stock_warehouse': 0, 'gt_sale_retail': {}, 'gt_stock_retail': {}}
            # number_of_best_product = product_model_id.number_of_best_product
            number_of_best_product = categ.number_of_best_product
            if dt_is_stock_type:
                if raw_data:
                    new_raw_data = sorted(raw_data, key=lambda d: d['all_qty_sale_retail'], reverse=True)
                    max_data = new_raw_data[:number_of_best_product] if number_of_best_product else new_raw_data

                    # Header
                    header_table = header_table_real_with_stock_type.copy()
                    row += 1
                    column = len(header_table)
                    grand_column = len(header_table)
                    
                    if not warehouse_select :
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
                    
                    if not warehouse_select :
                        param1 = 15
                    else :
                        param1 = 13
                    for x in range(0, len(header_table)):
                        sheet.set_column(x, x, param1)
                    row += 1

                    # Detail
                    # for zz in new_raw_data[:number_of_best_product]:
                    for zz in max_data:
                        if date_period < 21:
                            if not (zz['all_qty_sale_retail'] >= product_model_id.less_than_one_month):
                                continue
                        else:
                            if not (zz['all_qty_sale_retail'] >= product_model_id.more_than_one_month):
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
                            sheet.write(row, 5, xx['stock_type'], formatDetailTableReOrder)
                            sheet.write(row, 6, xx['aging'], formatDetailTableReOrder)
                            sheet.write(row, 7, xx['barcode'], formatDetailTableReOrder)
                            sheet.write(row, 8, xx['size'], formatDetailTableReOrder)

                            sheet.write(row, 9, xx['photo'], formatDetailTableReOrder)
                            sheet.set_column(row, 9, 15)
                            sheet.set_row(row, 75)
                            if xx['photo']:
                                sheet.insert_image(row, 9, "image.png", {'image_data': d_photo, 'bg_color': '#FFFFFF', 'x_scale': resize_scale, 'y_scale': resize_scale, 'x_offset': 10, 'y_offset': 10})
                            else:
                                sheet.write(row, 9, '', formatDetailTableReOrder)

                            sheet.write(row, 10, xx['order_notes'], formatDetailTableReOrder)
                            sheet.write(row, 11, xx['cost'], formatDetailCurrencyTableReOrder)
                            sheet.write(row, 12, xx['sale_price'], formatDetailCurrencyTableReOrder)
                            if not warehouse_select :
                                sheet.write(row, 13, xx['total_qty_sale_retail'] or '', formatDetailTableReOrderSand)
                                sheet.write(row, 14, xx['total_qty_stock_retail'] or '', formatDetailTableReOrder)
                                sheet.write(row, 15, xx['total_qty_stock_warehouse'] or '', formatDetailTableReOrder)
                                column_2 = 15
                            else :
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
                        sheet.write(row, 11, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 12, '', formatDetailTableReOrderBlue)
                        if not warehouse_select :
                            sheet.write(row, 13, zz['all_qty_sale_retail'] or '', formatDetailTableReOrderBlue)
                            sheet.write(row, 14, zz['all_qty_stock_retail'] or '', formatDetailTableReOrderBlue)
                            sheet.write(row, 15, zz['all_qty_stock_warehouse'] or '', formatDetailTableReOrderBlue)
                            column_3 = 15
                        else :
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
                    if not warehouse_select :
                        param_a = 4
                    else :
                        param_a = 2
                    sheet.merge_range(row, 0, row, grand_column-param_a, f'Grand Total {categ.name}', formatDetailTableReOrderBlue)
                    if not warehouse_select :
                        sheet.write(row, 13, data_grand_total['grand_total_qty_sale_retail'] or '', formatDetailTableReOrderBlue)
                        sheet.write(row, 14, data_grand_total['grand_total_qty_stock_retail'] or '', formatDetailTableReOrderBlue)
                        sheet.write(row, 15, data_grand_total['grand_total_qty_stock_warehouse'] or '', formatDetailTableReOrderBlue)
                        column_3 = 15
                    else :
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
            else:
                if raw_data:
                    new_raw_data = sorted(raw_data, key=lambda d: d['all_qty_sale_retail'], reverse=True)
                    max_data = new_raw_data[:number_of_best_product] if number_of_best_product else new_raw_data

                    # Header
                    header_table = header_table_real.copy()
                    row += 1
                    column = len(header_table)
                    grand_column = len(header_table)
                    if not warehouse_select :
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
                            if not (zz['all_qty_sale_retail'] >= product_model_id.less_than_one_month):
                                continue
                        else:
                            if not (zz['all_qty_sale_retail'] >= product_model_id.more_than_one_month):
                                continue

                        for xx in zz['order_line']:
                            sheet.write(row, 0, xx['model'], formatDetailTableReOrder)
                            sheet.write(row, 1, xx['category'], formatDetailTableReOrder)
                            sheet.write(row, 2, xx['style'], formatDetailTableReOrder)
                            sheet.write(row, 3, xx['stockname'], formatDetailTableReOrder)
                            sheet.write(row, 4, xx['stockid'], formatDetailTableReOrder)
                            sheet.write(row, 5, xx['color'], formatDetailTableReOrder)
                            sheet.write(row, 6, xx['aging'], formatDetailTableReOrder)
                            sheet.write(row, 7, xx['barcode'], formatDetailTableReOrder)
                            sheet.write(row, 8, xx['size'], formatDetailTableReOrder)
                            sheet.write(row, 9, xx['order_notes'], formatDetailTableReOrder)
                            sheet.write(row, 10, xx['cost'], formatDetailCurrencyTableReOrder)
                            sheet.write(row, 11, xx['sale_price'], formatDetailCurrencyTableReOrder)
                            if not warehouse_select :
                                sheet.write(row, 12, xx['total_qty_sale_retail'] or '', formatDetailTableReOrderSand)
                                sheet.write(row, 13, xx['total_qty_stock_retail'] or '', formatDetailTableReOrder)
                                sheet.write(row, 14, xx['total_qty_stock_warehouse'] or '', formatDetailTableReOrder)
                                column_2 = 14
                            else :
                                sheet.write(row, 12, xx['total_qty_stock_warehouse'] or '', formatDetailTableReOrder)
                                column_2 = 12
                                
                            if warehouse_ids:
                                for ww in warehouse_ids:
                                    column_2 += 1
                                    sheet.write(row, column_2, xx[ww]['qty_sale_retail'] or '', formatDetailTableReOrderSand)
                                    column_2 += 1
                                    sheet.write(row, column_2, xx[ww]['qty_stock_retail'] or '', formatDetailTableReOrder)
                            row += 1
                        sheet.write(row, 0, zz['model'], formatDetailTableReOrderBlue)
                        sheet.write(row, 1, zz['category'], formatDetailTableReOrderBlue)
                        sheet.write(row, 2, zz['style'], formatDetailTableReOrderBlue)
                        sheet.write(row, 3, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 4, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 5, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 6, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 7, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 8, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 9, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 10, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 11, '', formatDetailTableReOrderBlue)
                        if not warehouse_select :
                            sheet.write(row, 12, zz['all_qty_sale_retail'] or '', formatDetailTableReOrderBlue)
                            sheet.write(row, 13, zz['all_qty_stock_retail'] or '', formatDetailTableReOrderBlue)
                            sheet.write(row, 14, zz['all_qty_stock_warehouse'] or '', formatDetailTableReOrderBlue)
                            column_3 = 14
                        else :
                            sheet.write(row, 12, zz['all_qty_stock_warehouse'] or '', formatDetailTableReOrderBlue)
                            column_3 = 12
                            
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
                    if not warehouse_select :
                        param_a = 4
                    else :
                        param_a = 2
                    sheet.merge_range(row, 0, row, grand_column-param_a, f'Grand Total {categ.name}', formatDetailTableReOrderBlue)
                    if not warehouse_select :
                        sheet.write(row, 12, data_grand_total['grand_total_qty_sale_retail'] or '', formatDetailTableReOrderBlue)
                        sheet.write(row, 13, data_grand_total['grand_total_qty_stock_retail'] or '', formatDetailTableReOrderBlue)
                        sheet.write(row, 14, data_grand_total['grand_total_qty_stock_warehouse'] or '', formatDetailTableReOrderBlue)
                        column_3 = 14
                    else :
                        sheet.write(row, 12, data_grand_total['grand_total_qty_stock_warehouse'] or '', formatDetailTableReOrderBlue)
                        column_3 = 12
                        
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
            
