from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta

import io
import base64

class XlsxStaplesStyle(models.Model):
    _name = 'report.sol_bb_report.staples_style.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        header_table = ['Category', 'Style', 'Stock Name', 'Stock ID', 'Color', 'Barcode', 'Size', 'Aging', 'Cost Price', 'Retail Price', 'Qty Sold', 'In Stock', 'In Stock']
        column_to_a = {13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25:'Z'}

        formatHeaderCompany = workbook.add_format({'font_size': 14, 'valign':'vcenter', 'align': 'center', 'bold': True})
        formatHeaderTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bold': True, 'bg_color':'#8db4e2', 'color':'black', 'text_wrap': True, 'border': 1})
        formatHeaderTableSand = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bold': True, 'bg_color':'#e5b776', 'color':'black', 'text_wrap': True, 'border': 1})
        formatNormal = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'left', 'bold': True})
        formatNormalCenter = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'center', 'text_wrap': True, 'bold': True})
        formatNormalCurrencyCenter = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'center', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'bold': True})
        formatDetailTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'text_wrap': True, 'border': 1})
        formatDetailCurrencyTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrderBlue = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bg_color':'#8db4e2', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrderSand = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bg_color':'#e5b776', 'text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrderBlue = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bg_color':'#8db4e2', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatImage = workbook.add_format({'text_wrap': True, 'border': 1})

        datas = data.get('form', {})
        
        pos_order_line = self.env['pos.order.line'].sudo().search([
            ('order_id.date_order', '>=', datas.get('from_date')),
            ('order_id.date_order', '<=', datas.get('to_date')),
            ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
        ])

        product_tmpl_ids = self.env['product.template'].sudo().search([
            ('active', '=', True),
            ('product_model_id.name', 'ilike', 'STAPLES STYLES')
        ])

        warehouse_name_ids = pos_order_line.mapped('order_id.picking_type_id.warehouse_id.name')
        warehouse_ids = pos_order_line.mapped('order_id.picking_type_id.warehouse_id.id')

        from_date = datetime.strptime(datas.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(datas.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')

        sheet = workbook.add_worksheet(f'STAPLES STYLES')
        row = 1
        sheet.merge_range(row, 0, row, len(header_table)-1, f'PERIODE SALES : {from_date} - {to_date}', formatNormal)
        row += 1
        sheet.merge_range(row, 0, row, len(header_table)-1, f'Data Last Stock : {to_date}', formatNormal)

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
        start_row = row+1
        pt_temp = False
        wh_temp = False
        grand_total_qty_sale_retail = 0
        grand_total_qty_stock_retail = 0
        grand_total_qty_stock_warehouse = 0
        all_stock_retail = {'grand_total': {}, 'qty': {}}
        all_sale_retail = {'grand_total': {}, 'qty': {}}
        for pt in product_tmpl_ids:
            product_product_ids = self.env['product.product'].sudo().search([
                ('product_tmpl_id', '=', pt.id),
                ('active', '=', True)
            ])
            all_qty_sale_retail = 0
            all_qty_stock_retail = 0
            all_qty_stock_warehouse = 0
            model = pt.product_model_id.name or ''
            category = pt.categ_id.name or ''
            stock_type = pt.stock_type.name or ''
            style = ''
            akumulasi_stock_retail = 0
            akumulasi_sale_retail = 0
            len_product = len(product_product_ids)
            iterasi = 0
            for pp in product_product_ids:
                stock_move_ids = self.env['stock.move'].sudo().search([
                    ('date', '<=', datas.get('to_date')),
                    ('state', '=', 'done'),
                    ('product_id', '=', pp.id),
                ], order='date asc', limit=1)
                diff_date_in_week = int(round((fields.Date.today() - stock_move_ids.date.date()).days / 7, 0)) if stock_move_ids.date else 0
                if diff_date_in_week < 1:
                    len_product = len_product - 1

                    # SUM Variant Stock
                    if len_product > 0 and iterasi == len_product:
                        sheet.write(row, 0, category, formatDetailTableReOrderBlue)
                        sheet.write(row, 1, f'{style} Total', formatDetailTableReOrderBlue)
                        sheet.write(row, 2, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 3, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 4, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 5, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 6, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 7, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 8, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 9, '', formatDetailTableReOrderBlue)
                        sheet.write(row, 10, all_qty_sale_retail, formatDetailTableReOrderBlue)
                        sheet.write(row, 11, all_qty_stock_retail, formatDetailTableReOrderBlue)
                        sheet.write(row, 12, all_qty_stock_warehouse, formatDetailTableReOrderBlue)
                        grand_total_qty_sale_retail += all_qty_sale_retail
                        grand_total_qty_stock_retail += all_qty_stock_retail
                        grand_total_qty_stock_warehouse += all_qty_stock_warehouse
                        column_3 = 12
                        for wh in warehouse_ids:
                            column_3 += 1
                            if wh in all_sale_retail['qty']:
                                sheet.write(row, column_3, all_sale_retail['qty'][wh], formatDetailTableReOrderBlue)
                                # all_sale_retail['grand_total'][wh] += all_sale_retail[wh]['qty']
                            else:
                                sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                            column_3 += 1
                            if wh in all_stock_retail['qty']:
                                sheet.write(row, column_3, all_stock_retail['qty'][wh], formatDetailTableReOrderBlue)
                                # all_stock_retail['grand_total'][wh] += all_stock_retail[wh]['qty']
                            else:
                                sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                        row += 1
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
                order_notes = html2plaintext(pp.order_notes or '').strip()
                photo = ''
                cost = pp.standard_price or 0
                sale_price = pp.list_price or 0
                total_qty_sale_retail = 0
                total_qty_stock_retail = 0
                total_qty_stock_warehouse = 0

                # Tidak ada Penjumlahan
                sheet.write(row, 0, category, formatDetailTableReOrder)
                sheet.write(row, 1, style, formatDetailTableReOrder)
                sheet.write(row, 2, stockname, formatDetailTableReOrder)
                sheet.write(row, 3, stockid, formatDetailTableReOrder)
                sheet.write(row, 4, color, formatDetailTableReOrder)
                sheet.write(row, 5, barcode, formatDetailTableReOrder)
                sheet.write(row, 6, size, formatDetailTableReOrder)
                sheet.write(row, 7, aging, formatDetailTableReOrder)
                sheet.write(row, 8, cost, formatDetailCurrencyTableReOrder)
                sheet.write(row, 9, sale_price, formatDetailCurrencyTableReOrder)

                column_2 = 12
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
                    column_2 += 1
                    sheet.write(row, column_2, qty_sale_retail, formatDetailTableReOrderSand)
                    column_2 += 1
                    sheet.write(row, column_2, qty_stock_retail, formatDetailTableReOrder)

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
                sheet.write(row, 10, total_qty_sale_retail, formatDetailTableReOrderSand)
                sheet.write(row, 11, total_qty_stock_retail, formatDetailTableReOrder)
                sheet.write(row, 12, total_qty_stock_warehouse, formatDetailTableReOrder)
                
                all_qty_stock_retail += total_qty_stock_retail
                all_qty_sale_retail += total_qty_sale_retail
                all_qty_stock_warehouse += total_qty_stock_warehouse
                row += 1
                iterasi += 1

                # SUM Variant Stock
                if iterasi == len_product:
                    sheet.write(row, 0, category, formatDetailTableReOrderBlue)
                    sheet.write(row, 1, f'{style} Total', formatDetailTableReOrderBlue)
                    sheet.write(row, 2, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 3, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 4, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 5, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 6, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 7, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 8, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 9, '', formatDetailTableReOrderBlue)
                    sheet.write(row, 10, all_qty_sale_retail, formatDetailTableReOrderBlue)
                    sheet.write(row, 11, all_qty_stock_retail, formatDetailTableReOrderBlue)
                    sheet.write(row, 12, all_qty_stock_warehouse, formatDetailTableReOrderBlue)
                    grand_total_qty_sale_retail += all_qty_sale_retail
                    grand_total_qty_stock_retail += all_qty_stock_retail
                    grand_total_qty_stock_warehouse += all_qty_stock_warehouse
                    column_3 = 12
                    for wh in warehouse_ids:
                        column_3 += 1
                        if wh in all_sale_retail['qty']:
                            sheet.write(row, column_3, all_sale_retail['qty'][wh], formatDetailTableReOrderBlue)
                        else:
                            sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                        column_3 += 1
                        if wh in all_stock_retail['qty']:
                            sheet.write(row, column_3, all_stock_retail['qty'][wh], formatDetailTableReOrderBlue)
                        else:
                            sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
                    row += 1
        
        sheet.merge_range(row, 0, row, grand_column-4, 'Grand Total', formatDetailTableReOrderBlue)
        sheet.write(row, 10, grand_total_qty_sale_retail, formatDetailTableReOrderBlue)
        sheet.write(row, 11, grand_total_qty_stock_retail, formatDetailTableReOrderBlue)
        sheet.write(row, 12, grand_total_qty_stock_warehouse, formatDetailTableReOrderBlue)
        column_3 = 12
        for wh in warehouse_ids:
            column_3 += 1
            if wh in all_sale_retail['grand_total']:
                sheet.write(row, column_3, all_sale_retail['grand_total'][wh], formatDetailTableReOrderBlue)
            else:
                sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)
            column_3 += 1
            if wh in all_stock_retail['grand_total']:
                sheet.write(row, column_3, all_stock_retail['grand_total'][wh], formatDetailTableReOrderBlue)
            else:
                sheet.write(row, column_3, 0, formatDetailTableReOrderBlue)