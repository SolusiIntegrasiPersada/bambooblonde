from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta

import io
import base64

header_table = ['No', 'Transaction No', 'User', 'Photo', 'Transaction Date', 'Source Document', 'Status of Sample',
                'Style Name', 'Costing Order']


class XlsxSampDev(models.Model):
    _name = 'report.sol_bb_report.sampdev.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        formatHeaderCompany = workbook.add_format(
            {'font_size': 14, 'valign': 'vcenter', 'align': 'center', 'bold': True})
        formatHeaderTable = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre', 'bold': True, 'bg_color': '#8de29d',
             'color': 'black', 'text_wrap': True, 'border': 1})
        formatDetailTable = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre', 'text_wrap': True, 'border': 1})
        formatDetailCurrencyTable = workbook.add_format({'font_size': 11, 'valign': 'vcenter', 'align': 'centre',
                                                         'num_format': '_-"Rp"* #,##0.00_-;-"Rp"* #,##0.00_-;_-"Rp"* "-"_-;_-@_-',
                                                         'text_wrap': True, 'border': 1})
        formatDetailTableReOrder = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre', 'text_wrap': True, 'border': 1})
        formatDetailTableReOrderNoBorder = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre', 'text_wrap': True})
        formatDetailCurrencyTableReOrder = workbook.add_format({'font_size': 11, 'valign': 'vcenter', 'align': 'centre',
                                                                'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-',
                                                                'text_wrap': True, 'border': 1})
        formatDetailCurrencyTableReOrderNoBorder = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'align': 'centre',
             'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True})
        formatImage = workbook.add_format({'text_wrap': True, 'border': 1})

        datas = data.get('form', {})

        pr_ids = self.env['purchase.request'].sudo().search([
            ('date_start', '>=', datas.get('from_date')),
            ('date_start', '<=', datas.get('to_date')),
            # ('name_source', '=', datas.get('style_name'))
        ])

        from_date = datetime.strptime(datas.get('from_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(datas.get('to_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        sum_total = 0
        costing = 0
        sum_qty = 0

        # for pr_id in pr_ids:
        if datas.get('style_name'):
            sheet = workbook.add_worksheet(datas.get('style_name'))
        else:
            sheet = workbook.add_worksheet("All Style Name")
        row = 1
        sheet.merge_range(row, 0, row, len(header_table) - 1,
                          f'SAMPLE DEVELOPMENT {from_date} - {to_date}', formatHeaderCompany)

        row += 1
        column = 0
        for header in header_table:
            sheet.write(row, column, header.upper(), formatHeaderTable)
            column += 1

        row += 1

        for x in [1, 2, 3, 4, 5, 6, 7, 8]:
            sheet.set_column(x, x, 17)
        for x in [0]:
            sheet.set_column(x, x, 7)

        no = 1

        if datas.get('style_name'):
            prq_ids = self.env['purchase.request'].sudo().search([
                ('date_start', '>=', datas.get('from_date')),
                ('date_start', '<=', datas.get('to_date')),
                ('name_source', '=', datas.get('style_name'))
            ])
        else:
            prq_ids = self.env['purchase.request'].sudo().search([
                ('date_start', '>=', datas.get('from_date')),
                ('date_start', '<=', datas.get('to_date')),
                # ('name_source', '=', datas.get('style_name'))
            ])

        for pr in prq_ids:
            trans_no = pr.name
            user = pr.requested_by.name if pr.requested_by else ''
            picture = io.BytesIO(
                base64.b64decode(
                    pr.line_ids.product_id.image_1920)) if pr.line_ids.product_id.image_1920 else ''
            trans_date = pr.date_start.strftime('%d/%m/%Y') if pr.date_start else ''
            source = pr.name_source
            status_of_sample = pr.status_of_sample if pr.status_of_sample else ''
            style_name = pr.line_ids.product_id.name
            if pr.state == 'done':
                costing_product = pr.get_actual_pps if pr.get_actual_pps else 0
            else:
                costing_product = 0

            sheet.write(row, 0, no, formatDetailTableReOrder)
            sheet.write(row, 1, trans_no, formatDetailTableReOrder)
            sheet.write(row, 2, user, formatDetailTableReOrder)
            if picture:
                sheet.write(row, 3, '', formatDetailTableReOrder)
                sheet.insert_image(row, 3, "image.png",
                                   {'image_data': picture, 'x_scale': 0.21,
                                    'y_scale': 0.15, 'object_position': 1, 'x_offset': 30, 'y_offset': 5})
            else:
                sheet.write(row, 3, '', formatDetailTableReOrder)
            sheet.write(row, 4, trans_date, formatDetailTableReOrder)
            sheet.write(row, 5, source, formatDetailTableReOrder)
            sheet.write(row, 6, status_of_sample, formatDetailTableReOrder)
            sheet.write(row, 7, style_name, formatDetailTableReOrder)

            costing = costing_product if pr.state == 'done' else 0
            sheet.write(row, 8, costing, formatDetailCurrencyTableReOrder)

            sum_total += costing

            sheet.set_row(row, 70)
            column += 1
            row += 1
            no += 1
        sheet.write(row, 8, sum_total, formatDetailCurrencyTableReOrderNoBorder)

