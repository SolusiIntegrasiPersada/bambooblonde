from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta

import io
import base64

header_table = ['No', 'Picture', 'New - Re Order', 'Del Date', 'PO', 'PO Bamboo', 'Style', 'Color', 'Variant Size', 'Qty', 'Trans Date', 'Supplier', 'Date Out', 'Date In', 'Status']

class XlsxSupplierSewingReport(models.Model):
    _name = 'report.sol_bb_report.supplier_sewing_report.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        formatHeaderCompany = workbook.add_format({'font_size': 14, 'valign':'vcenter', 'align': 'center', 'bold': True})
        formatHeaderTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bold': True, 'bg_color':'#8db4e2', 'color':'black', 'text_wrap': True, 'border': 1})
        formatDetailTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True, 'border': 1})
        formatDetailCurrencyTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0.00_-;-"Rp"* #,##0.00_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True, 'border': 1})
        formatDetailNoBorder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True})
        formatDetailCurrencyTableReOrder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'num_format': '_-"Rp"* #,##0.00_-;-"Rp"* #,##0.00_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'border': 1})
        formatImage = workbook.add_format({'text_wrap': True, 'border': 1})

        datas = data.get('form', {})
        mp_ids = self.env['mrp.production'].sudo().search([
                ('trans_date', '>=', datas.get('from_date')),
                ('trans_date', '<=', datas.get('to_date')),
                # ('state', 'in', ['progress', 'to_close', 'done']),
                ('state', '=', 'done'),
            ])
        pt_ids = mp_ids.mapped('product_tmpl_id.id')
        from_date = datetime.strptime(datas.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(datas.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')

        sheet = workbook.add_worksheet('Sewing')
        row = 1
        sheet.merge_range(row, 0, row, len(header_table)-1, f'NEW ORDER & RE-ORDER BAMBOO {from_date} - {to_date}', formatHeaderCompany)
        row += 1
        sheet.merge_range(row, 0, row, len(header_table)-1, f'SUPPLIER SEWING REPORT', formatHeaderCompany)

        row += 1
        column = 0
        for header in header_table:
            sheet.write(row, column, header.upper(), formatHeaderTable)
            column += 1
        
        row += 1

        for x in [1, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]:
            sheet.set_column(x, x, 18)
        for x in [2, 7, 14]:
            sheet.set_column(x, x, 13)
        for x in [0]:
            sheet.set_column(x, x, 7)

        mrp_ids = self.env['mrp.production'].sudo().search([
            ('delivery_date', '>=', datas.get('from_date')),
            ('delivery_date', '<=', datas.get('to_date')),
            # ('state', 'in', ['progress', 'to_close', 'done']),
            ('state', '=', 'done'),
            ('product_tmpl_id', 'in', pt_ids),
        ])
        
        no = 1
        all_qty = 0
        for mrp in mrp_ids:
            wo_ids =  mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'SEWING' and x.state in ['progress', 'done'])

            if not wo_ids:
                continue
            
            po_id = self.env['mrp.production'].sudo().search([('product_tmpl_id', '=', mrp.product_tmpl_id.id), ('state', 'not in', ['draft', 'cancel']), ('is_sample', '!=', True)])
            picture = io.BytesIO(base64.b64decode(mrp.product_tmpl_id.image_128)) if mrp.product_tmpl_id.image_128 else False
            order = 'Re - Order' if len(po_id) > 1 else 'New - Order'
            del_date = ''
            if mrp.delivery_date:
                del_date = f'16 - 30 {mrp.delivery_date.strftime("%b")}' if mrp.delivery_date.day > 15 else f'1 - 15 {mrp.delivery_date.strftime("%b")}'
            # del_date = mrp.delivery_date.strftime('%d/%m/%Y') if mrp.delivery_date else ''
            # po_bamboo= f'BB - {mrp.purchase_id.name}' if mrp.purchase_id else '' or ''
            mo_po_taboo = wo_ids[0].order_id.name if len(wo_ids) > 0 else ''
            po_bamboo= f'BB - {mo_po_taboo}' if mo_po_taboo else '' or ''
            # po_taboo = f'Bamb - {mo_po_taboo}' if mo_po_taboo else ''
            po_taboo = f'Bamb - {mrp.purchase_id.name}' if mrp.purchase_id else ''
            style = mrp.product_tmpl_id.name or ''
            fabric = mrp.purchase_id.order_line[0].fabric_por.name if len(mrp.purchase_id.order_line) > 0 else ''
            color = wo_ids[0].color_id.name or '' if len(wo_ids) > 0 else ''
            # po_sewing = mrp.env['purchase.order'].sudo().browse(wo_ids[0].order_id.id)
            list_variant = []
            total_variant_qty = 0
            for pw_id in mrp.by_product_ids:
                string_variant = f'{pw_id.size} : {int(pw_id.product_uom_qty)}'
                list_variant.append(string_variant)
                total_variant_qty += pw_id.product_uom_qty
            # qty = mrp.qty_producing or 0.0
            variant_size = '\n'.join(list_variant)
            qty = total_variant_qty
            cost_price = mrp.product_tmpl_id.standard_price or 0.0
            total = qty * cost_price
            trans_date = mrp.trans_date.strftime('%d/%m/%Y') if mrp.trans_date else ''
            supplier = wo_ids[0].supplier.name or '' if len(wo_ids) > 0 else '' or ''
            date_out = wo_ids[0].out_date.strftime('%d/%m/%Y') if wo_ids[0].out_date else '' if len(wo_ids) > 0 else '' or ''
            date_in = wo_ids[0].in_date.strftime('%d/%m/%Y') if wo_ids[0].in_date else '' if len(wo_ids) > 0 else '' or ''
            
            if len(wo_ids) > 0:
                if wo_ids[0].state == 'progress':
                    status = 'PROGRESS'
                elif wo_ids[0].state == 'done':
                    status = 'DONE'
                else:
                    status = ''
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
            sheet.write(row, 7, color, formatDetailTableReOrder)
            sheet.write(row, 8, variant_size, formatDetailTableReOrder)
            sheet.write(row, 9, qty, formatDetailTableReOrder)
            sheet.write(row, 10, trans_date, formatDetailTableReOrder)
            sheet.write(row, 11, supplier, formatDetailTableReOrder)
            sheet.write(row, 12, date_out, formatDetailTableReOrder)
            sheet.write(row, 13, date_in, formatDetailTableReOrder)
            sheet.write(row, 14, status, formatDetailTableReOrder)

            sheet.set_row(row, 70)
            column += 1
            row += 1
            no += 1
            all_qty += qty
        sheet.write(row, 8, 'Total', formatDetailNoBorder)
        sheet.write(row, 9, all_qty, formatDetailNoBorder)