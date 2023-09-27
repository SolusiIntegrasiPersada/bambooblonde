# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import ast
import copy
import datetime
import io
import json
import logging
import markupsafe
from collections import defaultdict
from math import copysign, inf

import lxml.html
from babel.dates import get_quarter_names
from dateutil.relativedelta import relativedelta
from markupsafe import Markup

from odoo import models, fields, api, _
from odoo.addons.web.controllers.main import clean_action
from odoo.exceptions import RedirectWarning
from odoo.osv import expression
from odoo.tools import config, date_utils, get_lang
from odoo.tools.misc import formatLang, format_date
from odoo.tools.misc import xlsxwriter

_logger = logging.getLogger(__name__)


class AccountReport(models.AbstractModel):
    _inherit = 'account.report'
    _description = 'Account Report'

    def get_xlsx(self, options, response=None):
        res = super(AccountReport, self).get_xlsx(options)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {
            'in_memory': True,
            'strings_to_formulas': False,
        })
        sheet = workbook.add_worksheet(self._get_report_name()[:31])

        date_default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2, 'num_format': 'yyyy-mm-dd'})
        date_default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'num_format': 'yyyy-mm-dd'})
        default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2})
        default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666'})
        style_header = workbook.add_format({
                                            'font_name': 'Arial',
                                            'font_size': 18,
                                            'font_color': '#666666',
                                            'text_wrap': True,  # Untuk memungkinkan teks melingkar dalam sel
                                            'valign': 'vcenter',  # Untuk mengatur teks ke tengah sel secara vertikal
                                        })
        style_parent_header = workbook.add_format({
                                            'font_name': 'Arial',
                                            'font_size': 12,
                                            'font_color': '#666666',
                                            'text_wrap': True,  # Untuk memungkinkan teks melingkar dalam sel
                                            'valign': 'vcenter',  # Untuk mengatur teks ke tengah sel secara vertikal
                                        })
        title_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'bottom': 2})
        level_0_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 'bottom': 6, 'font_color': '#666666'})
        level_1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 'bottom': 1, 'font_color': '#666666'})
        level_2_col1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666', 'indent': 1})
        level_2_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666'})
        level_2_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666'})
        level_3_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2})
        level_3_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666', 'indent': 1})
        level_3_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666'})

        #Set the first column width to 50
        sheet.set_column(0, 1, 60)
        sheet.set_row(0, 20)
        sheet.set_row(1, 50)
        sheet.set_row(2, 50)
        y_offset = 0
        company_ids = self.env.context.get('allowed_company_ids')
        company_res = [self.env['res.company'].browse(company_id).name for company_id in company_ids]
        company_names = ', '.join(company_res)
        journals_data = options.get('journals', [])
        # Mengambil daftar nama jurnal
        cont = self._set_context(options)
        tags = cont.get('analytic_account_ids', [])
        analytic = [tag['name'] for tag in tags]
        analytic_name = ', '.join(analytic)
        journal_names = [journal['code'] for journal in journals_data if journal['id'] != 'divider']
        # Cetak daftar nama jurnal
        journal = ', '.join(journal_names)

        get_name = self._name
        name_parts = get_name.split(".")

        # Ubah format huruf besar di depan setiap bagian
        model_name = " ".join([part.title() for part in name_parts])

        try:
            name_report = self.display_name
        except:
            name_report = model_name

        headers, lines = self.with_context(no_format=True, print_mode=True, prefetch_fields=False)._get_table(options)
        sheet.write(y_offset, 0, name_report, style_header)
        y_offset += 1
        # Tambahkan "Journals: Info Journals"
        sheet.write(y_offset, 0, 'Company : %s' %(company_names), style_parent_header)
        sheet.write(y_offset, 1, 'Journals : %s' %(journal), style_parent_header)
        y_offset += 1
        sheet.write(y_offset, 1, 'Analytic Accounts : %s' %(analytic_name), style_parent_header)
        y_offset += 2
        # Add headers.
        for header in headers:
            x_offset = 0
            for column in header:
                column_name_formated = column.get('name', '').replace('<br/>', ' ').replace('&nbsp;', ' ')
                colspan = column.get('colspan', 1)
                if colspan == 1:
                    sheet.write(y_offset, x_offset, column_name_formated, title_style)
                else:
                    sheet.merge_range(y_offset, x_offset, y_offset, x_offset + colspan - 1, column_name_formated, title_style)
                x_offset += colspan
            y_offset += 1

        if options.get('hierarchy'):
            lines = self._create_hierarchy(lines, options)
        if options.get('selected_column'):
            lines = self._sort_lines(lines, options)

        # Add lines.
        for y in range(0, len(lines)):
            level = lines[y].get('level')
            if lines[y].get('caret_options'):
                style = level_3_style
                col1_style = level_3_col1_style
            elif level == 0:
                y_offset += 1
                style = level_0_style
                col1_style = style
            elif level == 1:
                style = level_1_style
                col1_style = style
            elif level == 2:
                style = level_2_style
                col1_style = 'total' in lines[y].get('class', '').split(' ') and level_2_col1_total_style or level_2_col1_style
            elif level == 3:
                style = level_3_style
                col1_style = 'total' in lines[y].get('class', '').split(' ') and level_3_col1_total_style or level_3_col1_style
            else:
                style = default_style
                col1_style = default_col1_style

            #write the first column, with a specific style to manage the indentation
            cell_type, cell_value = self._get_cell_type_value(lines[y])
            if cell_type == 'date':
                sheet.write_datetime(y + y_offset, 0, cell_value, date_default_col1_style)
            else:
                sheet.write(y + y_offset, 0, cell_value, col1_style)

            #write all the remaining cells
            for x in range(1, len(lines[y]['columns']) + 1):
                cell_type, cell_value = self._get_cell_type_value(lines[y]['columns'][x - 1])
                if cell_type == 'date':
                    sheet.write_datetime(y + y_offset, x + lines[y].get('colspan', 1) - 1, cell_value, date_default_style)
                else:
                    sheet.write(y + y_offset, x + lines[y].get('colspan', 1) - 1, cell_value, style)

        workbook.close()
        output.seek(0)
        generated_file = output.read()
        output.close()

        return generated_file