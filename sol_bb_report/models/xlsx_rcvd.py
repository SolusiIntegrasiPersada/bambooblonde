from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

import io
import base64


class XlsxRcvd(models.Model):
    _name = 'report.sol_bb_report.rcvd.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        header_table = ['No', 'Po. No', 'Order Type', 'Del Date', 'Image', 'Style Description', 'Color', 'Variant Size', 'Total Qty Pcs', 'Sewing Supplier Name', 'Date Out To Sewing Supplier / Process Print', 'Plan RCVD In Taboo', 'Actual RCVD in Taboo', 'Send Date to Bamb', 'Remarks']

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
        formatDetailNoBorder = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre','text_wrap': True})

        datas = data.get('form', {})
        from_date = datetime.strptime(datas.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(datas.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')

        sheet = workbook.add_worksheet(f'{from_date}')
        row = 1
        sheet.merge_range(row, 0, row, len(header_table)-1, f'REPORT RCVD {from_date} - {to_date}', formatHeaderCompany)
        row += 1
        column = 0
        for header in header_table:
            sheet.write(row, column, header.upper(), formatHeaderTable)
            column += 1

        for x in range(0, len(header_table)):
            sheet.set_column(x, x, 15)
        
        # pol_ids = self.env['purchase.order.line'].sudo().search([
        #     ('order_id.date_approve', '>=', datas.get('from_date')),
        #     ('order_id.date_approve', '<=', datas.get('to_date')),
        #     ('order_id.state', 'in', ['purchase', 'done'])
        # ])
        pol_ids = self.env['by.product.dummy'].sudo().search([
            ('mrp_id.delivery_date', '>=', datas.get('from_date')),
            ('mrp_id.delivery_date', '<=', datas.get('to_date')),
            ('mrp_id.state', 'in', ['progress', 'done'])
        ])

        seq_no = 0
        sum_total_qty_pcs = 0
        for prl in pol_ids.mapped('product_id.product_tmpl_id'):
            list_color = ['COLOR','COLOUR','COLOURS','COLORS','WARNA','CORAK']

            if prl.attribute_line_ids and prl.attribute_line_ids.filtered(lambda x: x.attribute_id.name in list_color).value_ids.mapped('id'):
                po1_ids = self.env['mrp.production'].sudo().search([
                    ('delivery_date', '>=', datas.get('from_date')),
                    ('delivery_date', '<=', datas.get('to_date')),
                    ('state', 'in', ['progress', 'done']), 
                    ('purchase_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS')
                ])
                # po1_ids = self.env['purchase.order'].sudo().search([
                #     ('date_approve', '>=', datas.get('from_date')),
                #     ('date_approve', '<=', datas.get('to_date')),
                #     ('state', 'in', ['purchase', 'done']), 
                #     ('picking_type_id.barcode', '=', 'WHBB-RECEIPTS')
                # ])
                attrt_color = prl.attribute_line_ids.filtered(lambda x: x.attribute_id.name in list_color).value_ids.mapped('name')
                for po1 in po1_ids:
                # for po1 in po1_ids.order_line.filtered(lambda x: x.product_id.product_tmpl_id == prl and x.colour.strip() == color_name):

                    po_no = f'BAMB-{po1.purchase_id.name}' if po1.purchase_id else ''
                    order_type = ''
                    style_desc = prl.name or ''
                    variant_size = ''
                    list_size_qty = []

                    for color_name in attrt_color:
                        # pol_order_ids = self.env['purchase.order.line'].sudo().search([('product_id.product_tmpl_id', '=', prl.id), ('order_id.state', 'in', ['purchase', 'done']), ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS')])
                        # pol_order_ids = self.env['by.product.dummy'].sudo().search([('product_id.product_tmpl_id', '=', prl.id), ('mrp_id.state', 'in', ['progress', 'done']), ('mrp_id.purchase_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS')])
                        # pol_order_ids = self.env['purchase.order.line'].sudo().search([('product_id.product_tmpl_id', '=', prl.id), ('order_id.state', 'in', ['purchase', 'done']), ('order_id.picking_type_id.barcode', '=', 'WHBB-RECEIPTS')])
                        # pol_order_color_ids = pol_order_ids.filtered(lambda x: x.colour.strip() == color_name)
                        # if len(pol_order_color_ids.mapped('order_id')) > 1:
                        #     order_type = 'REORDER'
                        # else:
                        #     order_type = 'NEW ORDER'
                        # order_type = po1.purchase_id.order_type or ''
                        if po1.purchase_id.order_type == 'new_order':
                            order_type = 'NEW ORDER'
                        elif po1.purchase_id.order_type == 're_order':
                            order_type = 'REORDER'
                        else:
                            order_type = ''

                        color = color_name
                        total_qty = 0
                        for po1_line in po1.by_product_ids.filtered(lambda x: x.product_id.product_tmpl_id == prl and x.colour.strip() == color_name):
                            total_qty += po1_line.product_uom_qty
                            list_size_qty += [f'{po1_line.size}: {int(po1_line.product_uom_qty)}']
                        # for po1_line in po1.order_line.filtered(lambda x: x.product_id.product_tmpl_id == prl and x.colour.strip() == color_name):
                        #     total_qty += po1_line.product_qty
                        #     list_size_qty += [f'{po1_line.size}: {int(po1_line.product_qty)}']

                        if total_qty < 1:
                            continue

                        # total_qty_pcs = sum(po1.order_line.filtered(lambda x: x.product_id.product_tmpl_id == prl and x.colour == color_name).mapped('product_qty'))
                        total_qty_pcs = int(total_qty)
                        variant_size = '\n'.join(list_size_qty)
                        # mrp = self.env['mrp.production'].sudo().search([('purchase_id', '=', po1.id), ('state', 'not in', ['draft', 'cancel'])], limit = 1)
                        mrp = po1
                        wo_ids = mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'SEWING' and x.state in ['progress', 'done'])
                        sewing_supplier = wo_ids[0].supplier.name or '' if wo_ids else ''
                        date_out_sewing = wo_ids[0].out_date.strftime('%d/%m/%Y') if wo_ids and wo_ids[0].out_date else ''
                        plan_rcvd_in = (wo_ids[0].order_id.date_approve.date() + relativedelta(weeks=+wo_ids[0].order_id.plan_receive_in_week)).strftime('%d/%m/%Y') if wo_ids and wo_ids[0].order_id.date_approve else ''
                        actual_rcvd_in = wo_ids[0].order_id.effective_date.date().strftime('%d/%m/%Y') if wo_ids and wo_ids[0].order_id.effective_date else ''
                        send_date_to_bamb = mrp.sales_order_id.effective_date.date().strftime('%d/%m/%Y') if mrp.sales_order_id.effective_date else ''

                        flag_plan_rcvd_in = True if wo_ids and wo_ids[0].order_id.date_approve else False
                        flag_actual_rcvd_in = True if wo_ids and wo_ids[0].order_id.effective_date else False
                        flag_washing_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'WASHING' and x.state == 'progress') else False
                        flag_dyeing_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'DYEING' and x.state == 'progress') else False
                        flag_cutting_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'CUTTING' and x.state == 'progress') else False
                        flag_printing_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'PRINTING' and x.state == 'progress') else False
                        flag_sewing_process = True if mrp.workorder_ids and mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'SEWING' and x.state == 'progress') else False
                        remarks = ''
                        if flag_plan_rcvd_in and flag_actual_rcvd_in and mrp.service_ids:
                            remarks = 'SERVICE TO VENDOR PROCESS'
                        elif not flag_plan_rcvd_in and flag_washing_process:
                            remarks = 'WASHING PROCESS'
                        elif not flag_plan_rcvd_in and flag_dyeing_process:
                            remarks = 'DYEING PROCESS'
                        elif not flag_plan_rcvd_in and flag_printing_process:
                            remarks = 'PRINTING PROCESS'
                        elif not flag_plan_rcvd_in and flag_cutting_process:
                            remarks = 'CUTTING PROCESS'
                        elif not flag_plan_rcvd_in and flag_sewing_process:
                            remarks = 'SEWING PROCESS'

                        del_date = mrp.delivery_date.strftime('%d/%m/%Y') if mrp.delivery_date else ''
                        delivery_date = mrp.delivery_date
                        if mrp.delivery_date:
                            del_year = delivery_date.year
                            del_month = delivery_date.month
                            del_day = delivery_date.day
                        if delivery_date and del_day <= 15:
                            del_date = date(del_year, del_month, 15).strftime('%d-%b-%y')
                        elif delivery_date and del_day > 15:
                            # del_date = date(del_year, del_month, 31).strftime('%d-%b-%y')
                            del_date = (delivery_date + relativedelta(day=31)).strftime('%d-%b-%y')

                        # del_date = po1.effective_date.date().strftime('%d/%m/%Y') if po1.effective_date else ''
                        # if po1.effective_date:
                        #     del_year = po1.effective_date.date().year
                        #     del_month = po1.effective_date.date().month
                        #     del_day = po1.effective_date.date().day
                        # if po1.effective_date and po1.effective_date.date().day <= 15:
                        #     del_date = date(del_year, del_month, 15).strftime('%d-%b-%y')
                        # elif po1.effective_date and po1.effective_date.date().day > 15:
                        #     # del_date = date(del_year, del_month, 31).strftime('%d-%b-%y')
                        #     del_date = (po1.effective_date.date() + relativedelta(day=31)).strftime('%d-%b-%y')

                        picture = io.BytesIO(base64.b64decode(prl.image_128)) if prl.image_128 else False
                        image_width = 140.0
                        image_height = 182.0

                        cell_width = 98.0
                        cell_height = 80.0

                        x_scale = cell_width/image_width
                        y_scale = cell_height/image_height

                        row += 1
                        seq_no += 1
                        column = 0

                        sheet.write(row, column, seq_no, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, po_no, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, order_type, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, del_date, formatDetailTableReOrder)
                        column += 1
                        if picture:
                            sheet.write(row, column, '', formatDetailTableReOrder)
                            sheet.insert_image(row, column, "image.png", {'image_data': picture, 'object_position': 1, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 10, 'y_offset': 5})
                            # sheet.insert_image(row, 1, "image.png", {'image_data': picture, 'object_position': 1, 'x_scale': 0.3, 'y_scale': 0.3, 'x_offset': 10, 'y_offset': 5}, formatImage)
                        else:
                            sheet.write(row, column, '', formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, style_desc, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, color, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, variant_size, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, total_qty_pcs, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, sewing_supplier, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, date_out_sewing, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, plan_rcvd_in, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, actual_rcvd_in, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, send_date_to_bamb, formatDetailTableReOrder)
                        column += 1
                        sheet.write(row, column, remarks, formatDetailTableReOrder)
                        column += 1
                        sum_total_qty_pcs += total_qty_pcs
                        
                        sheet.set_row(row, 70)
        row += 1
        column = 0
        sheet.write(row, column, '', formatDetailNoBorder)
        column += 1
        sheet.write(row, column, '', formatDetailNoBorder)
        column += 1
        sheet.write(row, column, '', formatDetailNoBorder)
        column += 1
        sheet.write(row, column, '', formatDetailNoBorder)
        column += 1
        sheet.write(row, column, '', formatDetailNoBorder)
        column += 1
        sheet.write(row, column, '', formatDetailNoBorder)
        column += 1
        sheet.write(row, column, '', formatDetailNoBorder)
        column += 1
        sheet.write(row, column, 'Total', formatDetailNoBorder)
        column += 1
        sheet.write(row, column, sum_total_qty_pcs, formatDetailNoBorder)
