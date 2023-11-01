from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext
from datetime import datetime, timedelta

import io
import base64

header_table = ['Category', 'Budget Guide (%)', 'Budget', 'Actual (%)', 'In Stock(%)', 'Order', 'Total']

class XlsxPurchaseBudget(models.Model):
    _name = 'report.purchase_request.purchase_budget.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        formatHeaderTable = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'centre', 'bold': True, 'bg_color':'#92d050', 'color':'black', 'text_wrap': True, 'border': 1})
        formatNormal = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'left', 'bold': True})
        formatPercentage = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'right', 'bold': True})
        formatNormalAmount = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'right', 'num_format': '#,##0', 'text_wrap': True, 'bold': True})
        formatNormalCurrencyCenter = workbook.add_format({'font_size': 11, 'valign':'vcenter', 'align': 'center', 'num_format': '_-"Rp"* #,##0_-;-"Rp"* #,##0_-;_-"Rp"* "-"_-;_-@_-', 'text_wrap': True, 'bold': True})
        formatImage = workbook.add_format({'text_wrap': True, 'border': 1})

        sheet = workbook.add_worksheet('Budget')

        sheet.set_column('B:H', 18)
        sheet.write(1, 1, 'Periode', formatHeaderTable)
        sheet.write(1, 2, f'{objs.month} - {objs.year}', formatHeaderTable)
        sheet.write(2, 1, 'Budget', formatHeaderTable)
        sheet.write(2, 2, objs.budget_amount, formatNormalCurrencyCenter)
        sheet.write(3, 1, 'Used', formatHeaderTable)
        sheet.write(3, 2, objs.usage_amount, formatNormalCurrencyCenter)
        sheet.write(4, 1, 'Balance', formatHeaderTable)
        sheet.write(4, 2, objs.remaining_amount, formatNormalCurrencyCenter)

        row = 6
        column = 1
        for header in header_table:
            sheet.write(row, column, header, formatHeaderTable)
            column += 1

        start_row, row = 8, 7
        for line in objs.budget_ids:
            sheet.write(row, 1, line.category_id.name, formatNormal)
            sheet.write(row, 2, round(line.budget_guide * 100, 2), formatPercentage)
            sheet.write(row, 3, line.budget_amount, formatNormalCurrencyCenter)
            sheet.write(row, 4, round(line.actual_percentage * 100, 2), formatPercentage)
            sheet.write(row, 5, round(line.stock_percentage * 100, 2), formatPercentage)
            sheet.write(row, 6, line.purchase_qty, formatNormalAmount)
            sheet.write(row, 7, line.total_value, formatNormalCurrencyCenter)
            row += 1

        sheet.write(row, 1, 'Total', formatHeaderTable)
        sheet.write_formula(row, 2, f'=SUM(C{start_row}:C{row})', formatPercentage)
        sheet.write_formula(row, 3, f'=SUM(D{start_row}:D{row})', formatNormalCurrencyCenter)
        sheet.write_formula(row, 4, f'=SUM(E{start_row}:E{row})', formatNormalAmount)
        sheet.write_formula(row, 5, f'=SUM(F{start_row}:F{row})', formatPercentage)
        sheet.write_formula(row, 6, f'=SUM(G{start_row}:G{row})', formatNormalAmount)
        sheet.write_formula(row, 7, f'=SUM(H{start_row}:H{row})', formatNormalCurrencyCenter)