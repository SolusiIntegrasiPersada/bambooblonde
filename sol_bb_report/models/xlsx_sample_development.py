from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta

import io
import base64

header_title_new_order = ['Photo', 'Name', 'Color', 'Fabric', 'Sizes', 'Formula', 'Breakdown Sizes', 'Order Qty',
                          'Taboo Cost Price', 'Minimum Retail', 'Total', 'Delivery Date', 'Notes']
header_title_reorder = ['Photo', 'Name', 'Color', 'Age (Week) Round Up', 'Sizes', 'Qty Sold', 'In Stock',
                        'Last Order Qty', 'Formula', 'Order', 'Taboo Cost Price', 'Minimum Retail', 'Retail Price',
                        'Total']

dictionary_sheet = [{1: 'New Order'}, {2: 'Reorder'}]


class XlsxSampleDevelopment(models.Model):
    _name = 'report.sol_bb_report.sample_development.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        formatHeaderCompany = workbook.add_format(
            {'font_size': 14, 'valign': 'vcenter', 'align': 'center', 'bold': True})
        formatHeaderTable = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre', 'bold': True, 'bg_color': '#8db4e2',
             'color': 'black', 'text_wrap': True, 'border': 1})
        formatDetailTable = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre', 'text_wrap': True, 'border': 1})
        formatDetailCurrencyTable = workbook.add_format({'font_size': 11, 'valign': 'vcenter', 'align': 'centre',
                                                         'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-',
                                                         'text_wrap': True, 'border': 1})

        formatHeaderCompanyReOrder = workbook.add_format(
            {'font_size': 14, 'valign': 'vcenter', 'align': 'center', 'bold': True})
        formatSubHeaderCompanyReOrder = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'center', 'bold': True})
        formatHeaderTableReOrder = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre', 'bold': True, 'bg_color': '#8db4e2',
             'color': 'black', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrder = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre', 'text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrder = workbook.add_format({'font_size': 11, 'valign': 'vcenter', 'align': 'centre',
                                                                'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-',
                                                                'text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrderNoBorder = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre',
             'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True})

        i = 0
        datas = data.get('form', {})
        for sheet in dictionary_sheet:
            i += 1
            sheet = workbook.add_worksheet(sheet[i].upper())

            if i == 1:
                for x in [0, 1, 5, 6, 8, 9, 10, 11]:
                    sheet.set_column(x, x, 15)
                for x in [2, 3, 4, 7]:
                    sheet.set_column(x, x, 10)
                for x in [12]:
                    sheet.set_column(x, x, 25)

                pw_ids = self.env['purchase.order.line'].sudo().search([
                    ('order_id.date_order', '>=', datas.get('from_date')),
                    ('order_id.date_order', '<=', datas.get('to_date')),
                    # ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS'),
                    ('order_id.order_type', '=', 'new_order'),
                    # ('order_id.state', '=', 'draft')
                ])
                # pw_ids = self.env['purchase.order.line'].sudo().search([
                #     ('order_id.date_approve', '>=', datas.get('from_date')),
                #     ('order_id.date_approve', '<=', datas.get('to_date')),
                #     ('order_id.state', 'in', ['purchase', 'done'])
                # ])
                row = 1
                sheet.merge_range(row, 0, row, len(header_title_new_order) - 1,
                                  f'{datas.get("from_date")} - {datas.get("to_date")} NEW ORDER LIST',
                                  formatHeaderCompany)

                row += 1
                column = 0
                sum_total = 0
                for header in header_title_new_order:
                    sheet.write(row, column, header.upper(), formatHeaderTable)
                    column += 1

                row += 1
                # for prl in pw_ids.mapped('name.product_tmpl_id'):
                for prl in pw_ids.mapped('product_id.product_tmpl_id'):
                    product_ids = self.env['product.product'].sudo().search([
                        ('product_tmpl_id', '=', prl.id)
                    ])
                    order_qty = 0.0
                    for product in product_ids:
                        pw_2_ids = prl.env['purchase.order.line'].sudo().search([
                            ('order_id.date_order', '>=', datas.get('from_date')),
                            ('order_id.date_order', '<=', datas.get('to_date')),
                            # ('order_id.state', '=', 'draft'),
                            ('product_id', '=', product.id),
                            ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS'),
                            # ('order_id.partner_id', '=', po_id.company_id.partner_id.id),
                        ])
                        order_qty += sum(pw_2_ids.mapped('product_qty')) if len(pw_2_ids) > 0 else 0 or 0

                    if order_qty < 1:
                        continue
                    list_color = ['COLOR', 'COLOUR', 'COLOURS', 'COLORS', 'WARNA', 'CORAK']
                    list_size = ['SIZE', 'SIZES', 'UKURAN']
                    picture = io.BytesIO(base64.b64decode(prl.image_128)) if prl.image_128 else False
                    name = prl.name
                    color = ', '.join(
                        prl.attribute_line_ids.filtered(lambda x: x.attribute_id.name in list_color).value_ids.mapped(
                            'name')) or ''
                    # fabric = pw_2_ids[0].fabric.name or '' if len(pw_2_ids) > 0 else ''
                    fabric = pw_2_ids[0].fabric_por.name or '' if len(pw_2_ids) > 0 else ''
                    sizes = ', '.join(
                        prl.attribute_line_ids.filtered(lambda x: x.attribute_id.name in list_size).value_ids.mapped(
                            'name')) or ''
                    formula = ''
                    breakdown_sizes = ''
                    flag_formula = 0
                    po_pax_ids = self.env['purchase.order.line'].sudo().search([
                        ('product_id.product_tmpl_id', '=', prl.id),
                        ('order_id.date_order', '>=', datas.get('from_date')),
                        ('order_id.date_order', '<=', datas.get('to_date')),
                        # ('order_id.state', '=', 'draft'),
                        # ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS'),
                    ]).mapped('order_id.qty_pax')
                    pax = sum(po_pax_ids)
                    if '6' in sizes or '8' in sizes or '10' in sizes or '12' in sizes or '14' in sizes:
                        flag_formula = 1
                        formula = f'2.2.2.1.1 X {str(pax)} PAX'
                        breakdown_sizes = f'{str(2 * pax)}.{str(2 * pax)}.{str(2 * pax)}.{str(1 * pax)}.{str(1 * pax)}'
                        order_qty = 8 * pax
                    elif 'os' == sizes.lower():
                        flag_formula = 4
                        formula = f'6 X {str(pax)} PAX'
                        breakdown_sizes = f'{str(6 * pax)}'
                        order_qty = 6 * pax
                    elif 's' in sizes.lower() or 'm' in sizes.lower() or 'l' in sizes.lower() or 'xl' in sizes.lower():
                        flag_formula = 2
                        formula = f'1.2.2.1 X {str(pax)} PAX'
                        breakdown_sizes = f'{str(1 * pax)}.{str(2 * pax)}.{str(2 * pax)}.{str(1 * pax)}'
                        order_qty = 6 * pax
                    elif 's/m' in sizes.lower() or 'm/l' in sizes.lower() or 'l/xl' in sizes.lower():
                        flag_formula = 3
                        formula = f'2.3.1 X {str(pax)} PAX'
                        breakdown_sizes = f'{str(2 * pax)}.{str(3 * pax)}.{str(1 * pax)}'
                        order_qty = 6 * pax

                    # breakdown_sizes = ''
                    # if flag_formula == 0:
                    #     order_qty = 0
                    # elif flag_formula == 1:
                    #     order_qty = 

                    # order_qty = sum(prl_2_ids.mapped('product_qty')) or 0
                    taboo_cost = prl.standard_price or 0.0
                    minimum_retail = (taboo_cost + (taboo_cost * 45 / 100)) * 2 or 0.0
                    total = order_qty * taboo_cost
                    # delivery_date = '' if len(pw_2_ids) < 1 else pw_2_ids[0].purchase_pw.effective_date.strftime('%d/%m/%Y') if pw_2_ids[0].purchase_pw.effective_date else ''
                    delivery_date = '' if len(pw_2_ids) < 1 else pw_2_ids[0].order_id.effective_date.strftime(
                        '%d/%m/%Y') if pw_2_ids[0].order_id.effective_date else ''
                    notes = html2plaintext(pw_2_ids[0].order_id.notes or '').strip() if len(pw_2_ids) > 0 else ''

                    image_width = 140.0
                    image_height = 182.0

                    cell_width = 98.0
                    cell_height = 80.0

                    x_scale = cell_width / image_width
                    y_scale = cell_height / image_height

                    column = 0
                    if picture:
                        sheet.write(row, column, '', formatDetailTableReOrder)
                        sheet.insert_image(row, column, "image.png",
                                           {'image_data': picture, 'object_position': 1, 'x_scale': x_scale,
                                            'y_scale': y_scale, 'x_offset': 10, 'y_offset': 5})
                        # sheet.insert_image(row, 1, "image.png", {'image_data': picture, 'object_position': 1, 'x_scale': 0.3, 'y_scale': 0.3, 'x_offset': 10, 'y_offset': 5}, formatImage)
                    else:
                        sheet.write(row, column, '', formatDetailTableReOrder)
                    sheet.write(row, column + 1, name, formatDetailTable)
                    sheet.write(row, column + 2, color, formatDetailTable)
                    sheet.write(row, column + 3, fabric, formatDetailTable)
                    sheet.write(row, column + 4, sizes, formatDetailTable)
                    sheet.write(row, column + 5, formula, formatDetailTable)
                    sheet.write(row, column + 6, breakdown_sizes, formatDetailTable)
                    sheet.write(row, column + 7, order_qty, formatDetailTable)
                    sheet.write(row, column + 8, taboo_cost, formatDetailCurrencyTable)
                    sheet.write(row, column + 9, minimum_retail, formatDetailCurrencyTable)
                    sheet.write(row, column + 10, total, formatDetailCurrencyTable)
                    sheet.write(row, column + 11, delivery_date, formatDetailTable)
                    sheet.write(row, column + 12, notes, formatDetailTable)
                    sheet.set_row(row, 70)
                    row += 1
                    sum_total += total
                sheet.write(row, 10, sum_total, formatDetailCurrencyTableReOrderNoBorder)

            if i == 2:
                for x in [0, 1, 2, 3, 7, 8]:
                    sheet.set_column(x, x, 15)
                for x in [4, 5, 6, 9]:
                    sheet.set_column(x, x, 10)
                for x in [10, 11, 12, 13]:
                    sheet.set_column(x, x, 20)

                pw_ids = self.env['purchase.order.line'].sudo().search([
                    ('order_id.date_order', '>=', datas.get('from_date')),
                    ('order_id.date_order', '<=', datas.get('to_date')),
                    ('order_id.state', '=', 'draft'),
                    ('order_id.order_type', '=', 're_order'),
                    ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS')
                ])
                # pw_ids = self.env['purchase.order.line'].sudo().search([
                #     ('order_id.date_approve', '>=', datas.get('from_date')),
                #     ('order_id.date_approve', '<=', datas.get('to_date')),
                #     ('order_id.state', 'in', ['purchase', 'done'])
                # ])

                row = 1
                sheet.merge_range(row, 0, row, len(header_title_reorder) - 1,
                                  f'{datas.get("from_date")} - {datas.get("to_date")} REORDER LIST',
                                  formatHeaderCompanyReOrder)

                row += 1
                sheet.merge_range(row, 0, row, len(header_title_reorder) - 1,
                                  f'{datas.get("sales_from_date")} - {datas.get("sales_to_date")} SALES FROM',
                                  formatSubHeaderCompanyReOrder)

                row += 1
                column = 0
                sum_total = 0
                for header in header_title_reorder:
                    sheet.write(row, column, header.upper(), formatHeaderTableReOrder)
                    column += 1

                row += 1
                for product_tmpl in pw_ids.mapped('product_id.product_tmpl_id'):
                    product_ids = self.env['product.product'].sudo().search([
                        ('product_tmpl_id', '=', product_tmpl.id)
                    ])

                    # po_id = self.env['purchase.order.line'].sudo().search([('product_id.product_tmpl_id', '=', product_tmpl.id), ('order_id.state', '=', 'draft'), ('order_id.order_type', '=', 'order_type'), ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS')])
                    # po_id = prl.env['purchase.order.line'].sudo().search([('product_id.product_tmpl_id', '=', product_tmpl.id), ('order_id.state', 'in', ['purchase', 'done']), ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS')])
                    # po_id = prl.env['mrp.production'].sudo().search([('product_tmpl_id', '=', product_tmpl.id), ('state', 'not in', ['draft', 'cancel']), ('is_sample', '!=', True)])
                    # if len(po_id.mapped('order_id')) <= 1:
                    #     continue

                    total_qty_sold = 0
                    total_in_stock = 0
                    total_order_qty = 0
                    row_start = row
                    row_ppw = row

                    stock_move_ids = self.env['stock.move.line'].sudo().search([
                        ('date', '<=', datas.get('to_date')),
                        ('state', '=', 'done'),
                        ('reference', 'ilike', 'whbb/int/'),
                        ('product_id.product_tmpl_id', '=', product_tmpl.id),
                        ('product_id.variant_seller_ids', '!=', False)
                    ], order='date asc', limit=1)
                    diff_date_in_week = int(round((fields.Date.today() - stock_move_ids.date.date()).days / 7,
                                                  0)) if stock_move_ids.date else 0
                    if diff_date_in_week < 1:
                        continue

                    last_pw_ids = self.env['purchase.order.line'].sudo().search([
                        ('order_id.date_order', '<=', datas.get('to_date')),
                        ('order_id.state', 'in', ['purchase', 'done']),
                        ('product_id.product_tmpl_id', '=', product_tmpl.id),
                        # ('product_id.variant_seller_ids', '!=', False),
                        # ('order_id.order_type', '=', 're_order'),
                        ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS')
                    ])
                    # last_pw_ids =  self.env['purchase.order.line'].sudo().search([
                    #     ('order_id.date_approve', '<=', datas.get('to_date')),
                    #     ('order_id.state', 'in', ['purchase', 'done']),
                    #     ('product_id.product_tmpl_id', '=', product_tmpl.id),
                    #     ('product_id.variant_seller_ids', '!=', False)
                    # ])
                    purchase_pw = last_pw_ids.mapped('order_id')
                    list_ppw = []
                    for line in purchase_pw:
                        date_ppw = line.date_order.strftime('%d/%m/%Y') if line.date_order else ''
                        qty_ppw = sum(
                            line.order_line.filtered(lambda x: x.product_id.product_tmpl_id == product_tmpl).mapped(
                                'product_qty')) if len(line.order_line) > 0 else 0
                        last_ppw = [f'{date_ppw} : {int(qty_ppw)}']
                        list_ppw += last_ppw
                    # for mrp in purchase_pw:
                    #     date_ppw = mrp.date_finished.strftime('%d/%m/%Y') if mrp.date_finished else ''
                    #     qty_ppw = sum(mrp.by_product_ids.mapped('product_uom_qty')) if len(mrp.by_product_ids) > 0 else 0
                    #     last_ppw = [f'{date_ppw} : {int(qty_ppw)}']
                    #     list_ppw += last_ppw
                    # for ppw in purchase_pw:
                    #     date_ppw = ppw.date_approve.strftime('%d/%m/%Y') if ppw.date_approve else ''
                    #     qty_ppw = sum(ppw.pw_ids.mapped('product_qty')) if len(ppw.pw_ids) else 0
                    #     last_ppw = [f'{date_ppw} : {int(qty_ppw)}']
                    #     list_ppw += last_ppw
                    list_warna = []
                    for i, product in enumerate(product_ids):
                        pw_2_ids = self.env['purchase.order.line'].sudo().search([
                            ('order_id.date_order', '>=', datas.get('from_date')),
                            ('order_id.date_order', '<=', datas.get('to_date')),
                            # ('order_id.state', '=', 'draft'),
                            ('product_id', '=', product.id),
                            # ('product_id.variant_seller_ids', '!=', False),
                            ('order_id.order_type', '=', 're_order'),
                            ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS')
                        ])
                        # pw_2_ids = self.env['purchase.order.line'].sudo().search([
                        #     ('order_id.date_approve', '>=', datas.get('from_date')),
                        #     ('order_id.date_approve', '<=', datas.get('to_date')),
                        #     ('order_id.state', 'in', ['purchase', 'done']),
                        #     ('product_id', '=', product.id),
                        #     ('product_id.variant_seller_ids', '!=', False)
                        # ])

                        sol_ids = self.env['pos.order.line'].sudo().search([
                            ('order_id.date_order', '>=', datas.get('sales_from_date')),
                            ('order_id.date_order', '<=', datas.get('sales_to_date')),
                            ('order_id.state', 'not in', ['draft', 'cancel']),
                            ('product_id', '=', product.id)
                        ])

                        today = datas.get('sales_to_date')

                        sizes = ', '.join(list(set(pw_2_ids.mapped('size')))) if len(pw_2_ids) > 0 else '' or ''
                        warna = ', '.join(list(set(pw_2_ids.mapped('colour')))) if len(pw_2_ids) > 0 else '' or ''
                        qty_sold = sum(sol_ids.mapped('qty')) if len(sol_ids) > 0 else 0 or 0
                        order_qty = sum(pw_2_ids.mapped('product_qty')) if len(pw_2_ids) > 0 else 0 or 0
                        in_stock = int(product.qty_available) or 0
                        if in_stock < 1:
                            continue
                        # last_order_qty = ', '.join(list_ppw)
                        formula = ''
                        if sizes and warna:
                            sheet.write(row, 4, f'{sizes} ({warna})', formatDetailTableReOrder)
                            list_warna.append(warna)
                        else:
                            sheet.write(row, 4, sizes, formatDetailTableReOrder)
                        sheet.write(row, 5, qty_sold, formatDetailTableReOrder)
                        sheet.write(row, 6, in_stock, formatDetailTableReOrder)
                        # sheet.write(row, 7, last_order_qty, formatDetailTableReOrder)
                        sheet.write(row, 8, formula, formatDetailTableReOrder)
                        # row += 1
                        row += 1 if i != len(product_ids) - 1 else 1
                        total_qty_sold += qty_sold
                        total_in_stock += in_stock
                        total_order_qty += order_qty

                    for loq in list_ppw:
                        sheet.write(row_ppw, 7, loq, formatDetailTableReOrder)
                        row_ppw += 1

                    picture = io.BytesIO(base64.b64decode(product_tmpl.image_128)) if product_tmpl.image_128 else False
                    name = product_tmpl.name
                    age = diff_date_in_week
                    list_color = ['COLOR', 'COLOUR', 'COLOURS', 'COLORS', 'WARNA', 'CORAK']
                    # color = ', '.join(list(set(pw_2_ids.mapped('colour')))) if len(pw_2_ids) > 0 else ''
                    # color = ', '.join(product_tmpl.attribute_line_ids.filtered(lambda x: x.attribute_id.name in list_color).value_ids.mapped('name')) or ''
                    color = ', '.join(list_warna) or ''
                    taboo_cost = product_tmpl.standard_price or 0.0
                    minimum_retail = (taboo_cost + (taboo_cost * 45 / 100)) * 2 or 0.0
                    retail_price = product_tmpl.list_price or 0.0
                    total = total_order_qty * taboo_cost

                    image_width = 140.0
                    image_height = 182.0

                    cell_width = 98.0
                    cell_height = 80.0

                    x_scale = cell_width / image_width
                    y_scale = cell_height / image_height

                    if row_ppw > row:
                        for a in range(row_ppw - row):
                            sheet.write(row, 4, '', formatDetailTableReOrder)
                            sheet.write(row, 5, '', formatDetailTableReOrder)
                            sheet.write(row, 6, '', formatDetailTableReOrder)
                            sheet.write(row, 8, '', formatDetailTableReOrder)
                            row += 1

                    # row += 1
                    if row_start != row:
                        if picture:
                            sheet.insert_image(row_start, 0, "image.png",
                                               {'image_data': picture, 'object_position': 1, 'x_scale': x_scale,
                                                'y_scale': y_scale, 'x_offset': 10, 'y_offset': 5})
                        sheet.merge_range(row_start, 0, row, 0, '', formatDetailTableReOrder)
                        sheet.merge_range(row_start, 1, row, 1, name, formatDetailTableReOrder)
                        sheet.merge_range(row_start, 2, row, 2, color, formatDetailTableReOrder)
                        sheet.merge_range(row_start, 3, row, 3, age, formatDetailTableReOrder)
                        sheet.write(row, 4, 'Total', formatDetailTableReOrder)
                        sheet.write(row, 5, total_qty_sold, formatDetailTableReOrder)
                        sheet.write(row, 6, total_in_stock, formatDetailTableReOrder)
                        sheet.write(row, 7, '', formatDetailTableReOrder)
                        sheet.write(row, 8, '', formatDetailTableReOrder)
                        sheet.merge_range(row_start, 9, row, 9, '', formatDetailTableReOrder)
                        sheet.merge_range(row_start, 10, row, 10, taboo_cost, formatDetailCurrencyTableReOrder)
                        sheet.merge_range(row_start, 11, row, 11, minimum_retail, formatDetailCurrencyTableReOrder)
                        sheet.merge_range(row_start, 12, row, 12, retail_price, formatDetailCurrencyTableReOrder)
                        sheet.merge_range(row_start, 13, row, 13, total, formatDetailCurrencyTableReOrder)
                    else:
                        if picture:
                            sheet.insert_image(row, 0, "image.png",
                                               {'image_data': picture, 'object_position': 1, 'x_scale': x_scale,
                                                'y_scale': y_scale, 'x_offset': 10, 'y_offset': 5})
                        sheet.write(row, 0, '', formatDetailTableReOrder)
                        sheet.write(row, 1, name, formatDetailTableReOrder)
                        sheet.write(row, 2, color, formatDetailTableReOrder)
                        sheet.write(row, 3, age, formatDetailTableReOrder)
                        sheet.write(row, 4, 'Total', formatDetailTableReOrder)
                        sheet.write(row, 5, total_qty_sold, formatDetailTableReOrder)
                        sheet.write(row, 6, total_in_stock, formatDetailTableReOrder)
                        sheet.write(row, 7, '', formatDetailTableReOrder)
                        sheet.write(row, 8, '', formatDetailTableReOrder)
                        sheet.write(row, 9, '', formatDetailTableReOrder)
                        sheet.write(row, 10, taboo_cost, formatDetailCurrencyTableReOrder)
                        sheet.write(row, 11, minimum_retail, formatDetailCurrencyTableReOrder)
                        sheet.write(row, 12, retail_price, formatDetailCurrencyTableReOrder)
                        sheet.write(row, 13, total, formatDetailCurrencyTableReOrder)

                    if (row - row_start) < 1:
                        sheet.set_row(row_start, 70)
                    elif (row - row_start) < 2:
                        sheet.set_row(row_start, 50)
                    elif (row - row_start) < 3:
                        sheet.set_row(row_start, 30)
                    column += 1
                    row += 1
                    sum_total += total
                sheet.write(row, 13, sum_total, formatDetailCurrencyTableReOrderNoBorder)
