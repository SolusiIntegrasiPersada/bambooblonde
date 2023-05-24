from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta

import io
import base64

header_table = ['No', 'Picture', 'New-Re Order', 'Del Date', 'Po Bamboo', 'PO Taboo', 'Style', 'Fabric', 'Color', 'Size', 'Qty', 'Cost Price', 'Total', 'Trans Date', 'Supplier', 'Date Out', 'Date In', 'Status']

dictionary_sheet = [{1: 'New Order'}, {2: 'Reorder'}]

class XlsxBamboo(models.Model):
    _name = 'report.sol_bb_report.bamboo.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        formatHeaderCompany = workbook.add_format({'font_size': 14, 'valign':'vcenter', 'align': 'center', 'bold': True})
        formatHeaderTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bold': True, 'bg_color':'#8db4e2', 'color':'black', 'text_wrap': True, 'border': 1})
        formatDetailTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True, 'border': 1})
        formatDetailCurrencyTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0.00_-;-"Rp"* #,##0.00_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True, 'border': 1})
        formatDetailTableReOrderNoBorder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True})
        formatDetailCurrencyTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrderNoBorder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True})
        formatImage = workbook.add_format({'text_wrap': True, 'border': 1})

        datas = data.get('form', {})
        # mp_ids = self.env['mrp.production'].sudo().search([
        #         ('trans_date', '>=', datas.get('from_date')),
        #         ('trans_date', '<=', datas.get('to_date')),
        #         ('state', 'in', ['progress', 'to_close', 'done']),
        #     ])
        mp_ids = self.env['mrp.production'].sudo().search([
                ('delivery_date', '>=', datas.get('from_date')),
                ('delivery_date', '<=', datas.get('to_date')),
                ('state', 'in', ['progress', 'to_close', 'done']),
            ])
        from_date = datetime.strptime(datas.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(datas.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        sum_total = 0
        sum_qty = 0
        list_categ_ids = []

        for categ in mp_ids.mapped('product_tmpl_id.categ_id'):
            if categ.category_product == 'subcategory' and categ.parent_id.parent_id.id not in list_categ_ids :
                list_categ_ids.append(categ.parent_id.parent_id.id)
            elif categ.category_product == 'category' and categ.parent_id.id not in list_categ_ids :
                list_categ_ids.append(categ.parent_id.id)
            elif categ.category_product == 'department' and categ.id not in list_categ_ids :
                list_categ_ids.append(categ.id)
            # else:
            #     list_categ_ids.append(categ.id)

        # for pc in mp_ids.mapped('product_tmpl_id.categ_id'):
        for pc_id in list_categ_ids:
            pc = self.env['product.category'].sudo().browse(pc_id)
            sheet = workbook.add_worksheet(f'{pc.display_name}')
            row = 1
            sheet.merge_range(row, 0, row, len(header_table)-1, f'NEW ORDER & RE-ORDER BAMBOO {from_date} - {to_date}', formatHeaderCompany)

            row += 1
            column = 0
            for header in header_table:
                sheet.write(row, column, header.upper(), formatHeaderTable)
                column += 1
            
            row += 1

            for x in [1, 6, 8, 9, 11, 12, 17]:
                sheet.set_column(x, x, 17)
            for x in [2, 3, 4, 5, 7, 13, 14, 15, 16]:
                sheet.set_column(x, x, 13)
            for x in [0, 10]:
                sheet.set_column(x, x, 7)

            mrp_ids = self.env['mrp.production'].sudo().search([
                ('delivery_date', '>=', datas.get('from_date')),
                ('delivery_date', '<=', datas.get('to_date')),
                ('state', 'in', ['progress', 'to_close', 'done']),
                '|',
                '|',
                ('product_tmpl_id.categ_id', '=', pc.id),
                ('product_tmpl_id.categ_id.parent_id', '=', pc.id),
                ('product_tmpl_id.categ_id.parent_id.parent_id', '=', pc.id),
            ])
            # mrp_ids = self.env['mrp.production'].sudo().search([
            #     ('trans_date', '>=', datas.get('from_date')),
            #     ('trans_date', '<=', datas.get('to_date')),
            #     ('state', 'in', ['progress', 'to_close', 'done']),
            #     '|',
            #     '|',
            #     ('product_tmpl_id.categ_id', '=', pc.id),
            #     ('product_tmpl_id.categ_id.parent_id', '=', pc.id),
            #     ('product_tmpl_id.categ_id.parent_id.parent_id', '=', pc.id),
            # ])
            
            no = 1
            for mrp in mrp_ids:
                wo_ids =  mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'SEWING' and x.state in ['progress', 'done'])

                if not wo_ids:
                    continue

                picture = io.BytesIO(base64.b64decode(mrp.product_tmpl_id.image_128)) if mrp.product_tmpl_id.image_128 else False
                # order = 'Re - Order' if mrp.product_id.variant_seller_ids else 'New - Order'
                # order = mrp.purchase_id.order_type if mrp.purchase_id else ''
                if mrp.purchase_id.order_type == 'new_order':
                    order = 'NEW ORDER'
                elif mrp.purchase_id.order_type == 're_order':
                    order = 'REORDER'
                else:
                    order = ''
                if mrp.delivery_date and mrp.delivery_date.day <= 15:
                    del_date = '1-15'
                else:
                    del_date = '15-30'
                # del_date = mrp.delivery_date.strftime('%d/%m/%Y') if mrp.delivery_date else ''
                po_bamboo= f'BB - {mrp.purchase_id.name}' if mrp.purchase_id else '' or ''
                mo_po_taboo = wo_ids[0].order_id.name if len(wo_ids) > 0 else ''
                po_taboo = f'Bamb - {mo_po_taboo}' if mo_po_taboo else ''
                style = mrp.product_tmpl_id.name or ''
                fabric = mrp.purchase_id.order_line[0].fabric_por.name or '' if len(mrp.purchase_id.order_line) > 0 else ''
                list_size = ['SIZE','SIZES','UKURAN']
                list_variant = []
                total_variant_qty = 0
                for pw_id in mrp.by_product_ids:
                    string_variant = f'{pw_id.size} : {int(pw_id.product_uom_qty)}'
                    list_variant.append(string_variant)
                    total_variant_qty += pw_id.product_uom_qty
                # size = ', '.join(mrp.product_tmpl_id.attribute_line_ids.filtered(lambda x: x.attribute_id.name in list_size).value_ids.mapped('name')) or ''
                size = '\n'.join(list_variant)
                color = wo_ids[0].color_id.name or '' if len(wo_ids) > 0 else ''
                qty = total_variant_qty
                # qty = sum(product.product_uom_qty for product in mrp.by_product_ids)
                # cost_price = mrp.product_tmpl_id.standard_price or 0.0
                po_line_product = mrp.purchase_id.order_line.filtered(lambda x: x.product_id.product_tmpl_id == mrp.product_tmpl_id)
                cost_price = po_line_product[0].price_unit if len(po_line_product) >= 1 else 0.00
                total = qty * cost_price
                trans_date = mrp.trans_date.strftime('%d/%m/%Y') if mrp.trans_date else ''
                supplier = wo_ids[0].supplier.name or '' if len(wo_ids) > 0 else '' or ''
                date_out = wo_ids[0].out_date.strftime('%d/%m/%Y') if wo_ids[0].out_date else '' if len(wo_ids) > 0 else '' or ''
                date_in = wo_ids[0].in_date.strftime('%d/%m/%Y') if wo_ids[0].in_date else '' if len(wo_ids) > 0 else '' or ''

                flag_washing_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'WASHING' and x.state == 'progress') else False
                flag_dyeing_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'DYEING' and x.state == 'progress') else False
                flag_cutting_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'CUTTING' and x.state == 'progress') else False
                flag_printing_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'PRINTING' and x.state == 'progress') else False
                flag_sewing_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'SEWING' and x.state == 'progress') else False
                
                # if len(wo_ids) > 0:
                #     if wo_ids[0].state == 'progress':
                #         status = 'Sewing process'
                #     elif wo_ids[0].state == 'done':
                #         status = 'Delived in taboo warehouse'
                #     else:
                #         status = ''
                # else:
                #     status = ''
                if mrp.state == 'done':
                    status = 'Delivered in taboo warehouse'
                else:
                    if flag_washing_process:
                        status = 'WASHING PROCESS'
                    elif flag_dyeing_process:
                        status = 'DYEING PROCESS'
                    elif flag_printing_process:
                        status = 'PRINTING PROCESS'
                    elif flag_cutting_process:
                        status = 'CUTTING PROCESS'
                    elif flag_sewing_process:
                        status = 'SEWING PROCESS'
                    else:
                        status = ''

                image_width = 140.0
                image_height = 182.0

                cell_width = 98.0
                cell_height = 80.0

                x_scale = cell_width/image_width
                y_scale = cell_height/image_height

                sheet.write(row, 0, no, formatDetailTableReOrder)
                if picture:
                    sheet.write(row, 1, '', formatDetailTableReOrder)
                    sheet.insert_image(row, 1, "image.png", {'image_data': picture, 'object_position': 1, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 10, 'y_offset': 5})
                    # sheet.insert_image(row, 1, "image.png", {'image_data': picture, 'object_position': 1, 'x_scale': 0.3, 'y_scale': 0.3, 'x_offset': 10, 'y_offset': 5}, formatImage)
                else:
                    sheet.write(row, 1, '', formatDetailTableReOrder)
                sheet.write(row, 2, order, formatDetailTableReOrder)
                sheet.write(row, 3, del_date, formatDetailTableReOrder)
                sheet.write(row, 4, po_bamboo, formatDetailTableReOrder)
                sheet.write(row, 5, po_taboo, formatDetailTableReOrder)
                sheet.write(row, 6, style, formatDetailTableReOrder)
                sheet.write(row, 7, fabric, formatDetailTableReOrder)
                sheet.write(row, 8, color, formatDetailTableReOrder)
                sheet.write(row, 9, size, formatDetailTableReOrder)
                sheet.write(row, 10, qty, formatDetailTableReOrder)
                sheet.write(row, 11, cost_price, formatDetailCurrencyTableReOrder)
                sheet.write(row, 12, total, formatDetailCurrencyTableReOrder)
                sheet.write(row, 13, trans_date, formatDetailTableReOrder)
                sheet.write(row, 14, supplier, formatDetailTableReOrder)
                sheet.write(row, 15, date_out, formatDetailTableReOrder)
                sheet.write(row, 16, date_in, formatDetailTableReOrder)
                sheet.write(row, 17, status, formatDetailTableReOrder)

                sum_total += total
                sum_qty += qty

                sheet.set_row(row, 70)
                column += 1
                row += 1
                no += 1
            sheet.write(row, 10, sum_qty, formatDetailTableReOrderNoBorder)
            sheet.write(row, 12, sum_total, formatDetailCurrencyTableReOrderNoBorder)
                        