import xlsxwriter
import base64
from odoo import fields, models, api
from io import BytesIO
from datetime import datetime
from pytz import timezone
import pytz
import io
from PIL import Image


class StockSalesSummaryReport(models.TransientModel):
    _name = "stock.sales.summary.report"
    _description = "Stock Sales Summary Report .xlsx"

    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone(self.env.user.tz or 'UTC'))

    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)
    start_period = fields.Date('Start Period')
    end_period = fields.Date('End Period')
    config_id = fields.Many2one('pos.config', 'Point of Sale')
    shift = fields.Selection(
        [('ALL', 'ALL'), ('Shift A', 'Shift A'), ('Shift B', 'Shift B')], 'Shift', default='ALL')

    # @api.onchange('start_period')
    # def onchange_end_period(self):
    #     self.end_period = self.start_period

    def print_excel_report(self):
        data = self.read()[0]
        pos_name = self.config_id.name
        alamat_name = self.config_id.address
        config_id = self.config_id.id
        start_period = self.start_period
        end_period = self.end_period

        datetime_string = self.get_default_date_model().strftime("%Y-%m-%d %H:%M:%S")
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        report_name = 'Stock Sales Summary Report'
        filename = '%s %s' % (report_name, date_string)

        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf, workbook = self.add_workbook_format(workbook)

        cashier = str(self.shift)

        worksheet = workbook.add_worksheet(report_name)
        worksheet.merge_range('A1:N2', str(pos_name), wbf['title_doc'])
        worksheet.merge_range('A3:N3', str(alamat_name), wbf['title_doc2'])
        worksheet.merge_range('A4:N4', '', wbf['title_doc2'])
        worksheet.merge_range('A5:N6', 'Stock Sales Summary', wbf['title_doc'])
        worksheet.merge_range('A7:N7', 'Period : ' + str(start_period) +
                              ' s/d ' + str(end_period), wbf['title_doc2'])
        worksheet.merge_range('A8:N8', 'Shift : ' +
                              str(cashier), wbf['title_doc2'])
        worksheet.merge_range('A9:N9', '', wbf['title_doc2'])
        worksheet.merge_range('O1:Q9', '', wbf['title_doc2'])

        def calculate_scale(file_path, bound_size):
            # check the image size without loading it into memory
            im = Image.open(file_path)
            original_width, original_height = im.size

            # calculate the resize factor, keeping original aspect and staying within boundary
            bound_width, bound_height = bound_size
            ratios = (float(bound_width) / original_width,
                      float(bound_height) / original_height)
            return min(ratios)

        if self.env.user.company_id.logo:
            logo_company = io.BytesIO(
                base64.b64decode(self.env.user.company_id.logo))
            bound_width_height = (240, 240)
            resize_scale = calculate_scale(logo_company, bound_width_height)
            worksheet.insert_image('O3:Q6', "image.png",
                                   {'image_data': logo_company, 'bg_color': '#FFFFFF', 'x_scale': resize_scale,
                                    'y_scale': resize_scale})

        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)
        worksheet.set_column('J:J', 10)
        worksheet.set_column('K:K', 10)
        worksheet.set_column('L:L', 10)
        worksheet.set_column('M:M', 20)
        worksheet.set_column('N:N', 20)
        worksheet.set_column('O:O', 20)
        worksheet.set_column('P:P', 20)
        worksheet.set_column('Q:Q', 20)


        worksheet.merge_range('A10:A17', "Code/Descriptions", wbf['header_no'])
        worksheet.merge_range('B10:B17', "Color", wbf['header_no'])
        
        worksheet.write(9, 2, "Size Type", wbf['header_no'])
        worksheet.write(10, 2, "A", wbf['header_no'])
        worksheet.write(11, 2, "B", wbf['header_no'])
        worksheet.write(12, 2, "C", wbf['header_no'])
        worksheet.write(13, 2, "D", wbf['header_no'])
        worksheet.write(14, 2, "F", wbf['header_no'])
        worksheet.write(15, 2, "G", wbf['header_no'])
        worksheet.write(16, 2, "H", wbf['header_no'])
        
        worksheet.merge_range('D10:K10', "Quantity", wbf['header_no'])

        worksheet.write(10, 3, "6", wbf['header_number'])
        worksheet.write(11, 3, "7", wbf['header_number'])
        worksheet.write(12, 3, "32", wbf['header_number'])
        worksheet.write(13, 3, "33", wbf['header_number'])
        worksheet.write(14, 3, "A", wbf['header_number'])
        worksheet.write(15, 3, "XXS", wbf['header_number'])
        worksheet.write(16, 3, "XS/S", wbf['header_number'])

        worksheet.write(10, 4, "8", wbf['header_number'])
        worksheet.write(11, 4, "9", wbf['header_number'])
        worksheet.write(12, 4, "34", wbf['header_number'])
        worksheet.write(13, 4, "35", wbf['header_number'])
        worksheet.write(14, 4, "B", wbf['header_number'])
        worksheet.write(15, 4, "XS", wbf['header_number'])
        worksheet.write(16, 4, "S/M", wbf['header_number'])

        worksheet.write(10, 5, "10", wbf['header_number'])
        worksheet.write(11, 5, "11", wbf['header_number'])
        worksheet.write(12, 5, "36", wbf['header_number'])
        worksheet.write(13, 5, "37", wbf['header_number'])
        worksheet.write(14, 5, "C", wbf['header_number'])
        worksheet.write(15, 5, "XSS", wbf['header_number'])
        worksheet.write(16, 5, "M/L", wbf['header_number'])

        worksheet.write(10, 6, "12", wbf['header_number'])
        worksheet.write(11, 6, "", wbf['header_number'])
        worksheet.write(12, 6, "38", wbf['header_number'])
        worksheet.write(13, 6, "39", wbf['header_number'])
        worksheet.write(14, 6, "D", wbf['header_number'])
        worksheet.write(15, 6, "S", wbf['header_number'])
        worksheet.write(16, 6, "L/XL", wbf['header_number'])

        worksheet.write(10, 7, "14", wbf['header_number'])
        worksheet.write(11, 7, "", wbf['header_number'])
        worksheet.write(12, 7, "40", wbf['header_number'])
        worksheet.write(13, 7, "41", wbf['header_number'])
        worksheet.write(14, 7, "", wbf['header_number'])
        worksheet.write(15, 7, "M", wbf['header_number'])
        worksheet.write(16, 7, " ", wbf['header_number'])

        worksheet.write(10, 8, "4", wbf['header_number'])
        worksheet.write(11, 8, "", wbf['header_number'])
        worksheet.write(12, 8, "42", wbf['header_number'])
        worksheet.write(13, 8, "43", wbf['header_number'])
        worksheet.write(14, 8, "", wbf['header_number'])
        worksheet.write(15, 8, "L", wbf['header_number'])
        worksheet.write(16, 8, " ", wbf['header_number'])

        worksheet.write(10, 9, " ", wbf['header_number'])
        worksheet.write(11, 9, " ", wbf['header_number'])
        worksheet.write(12, 9, "", wbf['header_number'])
        worksheet.write(13, 9, " ", wbf['header_number'])
        worksheet.write(14, 9, " ", wbf['header_number'])
        worksheet.write(15, 9, "XL", wbf['header_number'])
        worksheet.write(16, 9, " ", wbf['header_number'])

        worksheet.write(10, 10, " ", wbf['header_number'])
        worksheet.write(11, 10, " ", wbf['header_number'])
        worksheet.write(12, 10, " ", wbf['header_number'])
        worksheet.write(13, 10, " ", wbf['header_number'])
        worksheet.write(14, 10, " ", wbf['header_number'])
        worksheet.write(15, 10, "OS", wbf['header_number'])
        worksheet.write(16, 10, "ALL", wbf['header_number'])


        worksheet.merge_range('L10:L17', "TTL QTY", wbf['header_no'])
        worksheet.merge_range('M10:M17', "Price", wbf['header_no'])
        worksheet.merge_range('N10:N17', "Sub Total", wbf['header_no'])
        worksheet.merge_range('O10:O17', "Cost", wbf['header_no'])
        worksheet.merge_range('P10:P17', "Sub Total", wbf['header_no'])
        worksheet.merge_range('Q10:Q17', "Profit", wbf['header_no'])


        col0 = 'A'
        col1 = 'B'
        col2 = 'C'
        col3 = 'D'
        col4 = 'E'
        col5 = 'F'
        col6 = 'G'
        col7 = 'H'
        col8 = 'I'
        col9 = 'J'
        col10 = 'K'
        col11 = 'L'
        col12 = 'M'
        col13 = 'N'
        col14 = 'O'
        col15 = 'P'
        col16 = 'Q'
        col17 = 'R'

        row = 18

        grandtotal_size1 = 0
        grandtotal_size2 = 0
        grandtotal_size3 = 0
        grandtotal_size4 = 0
        grandtotal_size5 = 0
        grandtotal_size6 = 0
        grandtotal_size7 = 0
        grandtotal_size8 = 0

        domain = []

        if self.shift == 'Shift A':
            domain = [
                ('order_id.state', 'not in', ['draft', 'cancel']),
                ('order_id.date_order', '>=', self.start_period),
                ('order_id.date_order', '<=', self.end_period),
                ('order_id.session_id.shift', '=', 'Shift A'),
            ]
        elif self.shift == 'Shift B':
            domain = [
                ('order_id.state', 'not in', ['draft', 'cancel']),
                ('order_id.date_order', '>=', self.start_period),
                ('order_id.date_order', '<=', self.end_period),
                ('order_id.session_id.shift', '=', 'Shift B'),
            ]
        else:
            domain = [
                ('order_id.state', 'not in', ['draft', 'cancel']),
                ('order_id.date_order', '>=', self.start_period),
                ('order_id.date_order', '<=', self.end_period),
            ]

        docs = self.env['pos.order.line'].search(domain)

        # Membuat daftar kategori, produk, deskripsi, ukuran, warna
        data = {}
        for line in docs.filtered(lambda x: not x.product_id.is_shooping_bag and not x.product_id.is_produk_diskon and not x.product_id.is_produk_promotion):
            product = line.product_id
            color = line.color
            size = line.size
            
            price_unit = line.price_unit
            discount = line.discount
            if discount :
                price_unit_inc_discount = price_unit * (1- discount/100)
            else :
                price_unit_inc_discount = price_unit
                
            program_promotion = line.order_id.applied_program_ids
            for prog in program_promotion:
                if (prog.program_type == 'promotion_program' and prog.reward_type == 'discount' and product.id in prog.valid_product_ids.ids):
                    if prog.discount_type == 'percentage':
                        price_unit_inc_discount *= (1 - prog.discount_percentage / 100)
                    else:
                        price_unit_inc_discount -= prog.discount_fixed_amount
            
            cost_price = line.cost_in_order or product.standard_price or 0

            key = (product.name, color)
            if key not in data:
                data[key] = {
                    'parent_category': product.product_model_categ_id.name or '-',
                    'category': product.product_category_categ_id.name or '-',
                    'product': product.name or '-',
                    'default_code': product.default_code or '-',
                    'color': color or '-',
                    'size': size,
                    'qty': 0,
                    'size_type': 0,
                    'size1': 0,
                    'size2': 0,
                    'size3': 0,
                    'size4': 0,
                    'size5': 0,
                    'size6': 0,
                    'size7': 0,
                    'size8': 0,
                    'sale_price': price_unit_inc_discount or 0,
                    'subtotal': 0,
                    'cost_price': cost_price,
                    'cost_subtotal': 0,
                    'profit': 0,
                }

            data[key]['qty'] += line.qty or 0
            
            # print(size)
            size = size.replace(" ","")
            size_to_group = {
                '6': 'size1', '7': 'size1', '32': 'size1', '33': 'size1', 'A': 'size1', 'XXS': 'size1', 'XS/S': 'size1',
                '8': 'size2', '35': 'size2', 'B': 'size2', 'XS': 'size2', 'S/M': 'size2', '9': 'size2', '34': 'size2',
                '10': 'size3', '37': 'size3', 'C': 'size3', 'M/L': 'size3', 'XSS': 'size3', '11': 'size3', '36': 'size3',
                '12': 'size4', '39': 'size4', 'D': 'size4', 'S': 'size4', 'L/XL': 'size4', '38': 'size4',
                '14': 'size5', '41': 'size5', 'M': 'size5', '40': 'size5',
                '4': 'size6', '43': 'size6', 'L': 'size6', '42': 'size6',
                'XL': 'size7',
                'OS': 'size8', 'ALL': 'size8',
            }

            # Atur nilai berdasarkan ukuran dan grup yang sesuai
            group = size_to_group.get(size, 'size8')
            data[key][group] += line.qty or 0
            
            # size_type_mapping = {
            # '6': 'A', '8': 'A', '10': 'A', '12': 'A', '14': 'A', '4': 'A',
            # '7': 'B', '9': 'B', '11': 'B',
            # '32': 'C', '34': 'C', '36': 'C', '38': 'C', '40': 'C', '42': 'C',
            # '33': 'D', '35': 'D', '37': 'D', '39': 'D', '41': 'D', '43': 'D',
            # 'A': 'F', 'B': 'F', 'C': 'F', 'D': 'F',
            # 'XXS': 'G', 'XS': 'G', 'XSS': 'G', 'S': 'G', 'M': 'G', 'L': 'G', 'XL': 'G', 'OS': 'G',
            # 'XS/S': 'H', 'S/M': 'H', 'M/L': 'H', 'L/XL': 'H'}

            # # Atur tipe ukuran berdasarkan size yang diberikan
            # sizetypess = size_type_mapping.get(size, 'H')
            list_size = ['SIZE', 'SIZES', 'UKURAN']
            sizetypess = "H"  # Default label

            for v in product.product_template_variant_value_ids:
                if any(v.display_name.upper().startswith(word) for word in list_size):
                    attribute_id = v.attribute_id.value_ids.filtered(lambda value: value.name == v.name)
                    if attribute_id and attribute_id.label_id and attribute_id.label_id.name:
                        sizetypess = attribute_id.label_id.name
                        

            sizetypess = sizetypess.replace(" ", "")

            if data[key]['size_type']:
                # Memisahkan tipe ukuran yang sudah ada
                existing_size_types = data[key]['size_type'].split(', ')
                if sizetypess not in existing_size_types:
                    # Tambahkan tipe ukuran baru jika belum ada
                    data[key]['size_type'] += ", " + sizetypess
            else:
                # Jika belum ada, langsung atur tipe ukuran sebagai tipe ukuran baru
                data[key]['size_type'] = sizetypess
                
            subtotal2_price = line.qty * price_unit_inc_discount or 0
            subtotal2_cost = line.qty * cost_price or 0
            data[key]['subtotal'] += subtotal2_price or 0
            data[key]['cost_subtotal'] += subtotal2_cost or 0
            data[key]['profit'] += subtotal2_price - subtotal2_cost or 0

        grouped_data = {}
        for key, line in data.items():
            parent_category = line['parent_category']
            category = line['category']
            if parent_category not in grouped_data:
                grouped_data[parent_category] = {}
            if category not in grouped_data[parent_category]:
                grouped_data[parent_category][category] = []
            grouped_data[parent_category][category].append(line)

        sorted_data = []
        for parent_category, categories in sorted(grouped_data.items()):
            sorted_data.append(
                {'parent_category': parent_category, 'categories': []})
            for category, lines in sorted(categories.items()):
                sorted_data[-1]['categories'].append(
                    {'category': category, 'lines': lines})

        grandtotal_size1 = 0
        grandtotal_size2 = 0
        grandtotal_size3 = 0
        grandtotal_size4 = 0
        grandtotal_size5 = 0
        grandtotal_size6 = 0
        grandtotal_size7 = 0
        grandtotal_size8 = 0
        grandtotal_qty = 0
        grandtotal_price = 0
        grandtotal_cost = 0
        grandtotal_profit = 0
        for rec in sorted_data:
            worksheet.merge_range('A18:Q18', '', wbf['title_doc2'])
            row += 1
            worksheet.merge_range('%s%s:%s%s' % (
                col0, row, col16, row), rec['parent_category'], wbf['title_doc2'])
            row += 1
            total_size1 = 0
            total_size2 = 0
            total_size3 = 0
            total_size4 = 0
            total_size5 = 0
            total_size6 = 0
            total_size7 = 0
            total_size8 = 0
            total_qty = 0
            total_price = 0
            total_cost = 0
            total_profit = 0
            for rec1 in rec['categories']:
                worksheet.merge_range('%s%s:%s%s' % (col0, row, col16, row), '     ' + rec1['category'] or '',
                                      wbf['title_doc3'])
                row += 1
                subtotal_size1 = 0
                subtotal_size2 = 0
                subtotal_size3 = 0
                subtotal_size4 = 0
                subtotal_size5 = 0
                subtotal_size6 = 0
                subtotal_size7 = 0
                subtotal_size8 = 0
                subtotal_qty = 0
                subtotal_price = 0
                subtotal_cost = 0
                subtotal_profit = 0
                for rec2 in rec1['lines']:
                    product_name = '   --- ' + rec2['product']
                    if rec2['default_code']:
                        product_name = '   --- ' + \
                            rec2['default_code'] + ' - ' + rec2['product']

                    worksheet.write('%s%s:%s%s' % (
                        col0, row, col1, row), product_name or '', wbf['content'])
                    worksheet.write('%s%s:%s%s' % (
                        col1, row, col2, row), rec2['color'] or '', wbf['content2'])
                    worksheet.write('%s%s:%s%s' % (
                        col2, row, col3, row), rec2['size_type'], wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (
                        col3, row, col14, row), rec2['size1'] or '', wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (
                        col4, row, col15, row), rec2['size2'] or '', wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (
                        col5, row, col6, row), rec2['size3'] or '', wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (
                        col6, row, col7, row), rec2['size4'] or '', wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (
                        col7, row, col8, row), rec2['size5'] or '', wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (
                        col8, row, col9, row), rec2['size6'] or '', wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (
                        col9, row, col10, row), rec2['size7'] or '', wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (
                        col10, row, col11, row), rec2['size8'] or '', wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (
                        col11, row, col12, row), rec2['qty'] or '', wbf['content_number'])
                    worksheet.write('%s%s:%s%s' % (col12, row, col13, row), rec2['sale_price'] or '',
                                    wbf['content_float'])
                    worksheet.write('%s%s:%s%s' % (col13, row, col14, row), rec2['subtotal'] or '',
                                    wbf['content_float'])
                    worksheet.write('%s%s:%s%s' % (col14, row, col15, row), rec2['cost_price'] or '',
                                    wbf['content_float'])
                    worksheet.write('%s%s:%s%s' % (col15, row, col16, row), rec2['cost_subtotal'] or '',
                                    wbf['content_float'])
                    worksheet.write('%s%s:%s%s' % (
                        col16, row, col17, row), rec2['profit'] or '', wbf['content_float'])
                    row += 1

                    subtotal_size1 += rec2['size1']
                    subtotal_size2 += rec2['size2']
                    subtotal_size3 += rec2['size3']
                    subtotal_size4 += rec2['size4']
                    subtotal_size5 += rec2['size5']
                    subtotal_size6 += rec2['size6']
                    subtotal_size7 += rec2['size7']
                    subtotal_size8 += rec2['size8']
                    subtotal_qty += rec2['qty']
                    subtotal_price += rec2['subtotal']
                    subtotal_cost += rec2['cost_subtotal']
                    subtotal_profit += rec2['profit']

                worksheet.merge_range('%s%s:%s%s' % (col0, row, col2, row), 'Sub Total ' + str(rec1['category']),
                                      wbf['title_doc3_float'])
                worksheet.write('%s%s:%s%s' % (
                    col2, row, col13, row), '', wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (col3, row, col14, row), subtotal_size1 or '',
                                wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (col4, row, col15, row), subtotal_size2 or '',
                                wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (col5, row, col6, row),
                                subtotal_size3 or '', wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (col6, row, col7, row),
                                subtotal_size4 or '', wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (col7, row, col8, row),
                                subtotal_size5 or '', wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (col8, row, col9, row),
                                subtotal_size6 or '', wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (col9, row, col10, row), subtotal_size7 or '',
                                wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (col10, row, col11, row), subtotal_size8 or '',
                                wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (col11, row, col12, row),
                                subtotal_qty or '', wbf['title_content_number'])
                worksheet.write('%s%s:%s%s' % (
                    col12, row, col13, row), '', wbf['title_doc2_float'])
                worksheet.write('%s%s:%s%s' % (col13, row, col14, row),
                                subtotal_price or '', wbf['title_doc2_float'])
                worksheet.write('%s%s:%s%s' % (
                    col14, row, col15, row), '', wbf['title_doc2_float'])
                worksheet.write('%s%s:%s%s' % (col15, row, col16, row),
                                subtotal_cost or '', wbf['title_doc2_float'])
                worksheet.write('%s%s:%s%s' % (col16, row, col17, row),
                                subtotal_profit or '', wbf['title_doc2_float'])
                row += 1

                total_size1 += subtotal_size1
                total_size2 += subtotal_size2
                total_size3 += subtotal_size3
                total_size4 += subtotal_size4
                total_size5 += subtotal_size5
                total_size6 += subtotal_size6
                total_size7 += subtotal_size7
                total_size8 += subtotal_size8
                total_qty += subtotal_qty
                total_price += subtotal_price
                total_cost += subtotal_cost
                total_profit += subtotal_profit

            worksheet.merge_range('%s%s:%s%s' % (col0, row, col2, row), 'Total ' + str(rec['parent_category']),
                                  wbf['title_doc3_float'])
            worksheet.write('%s%s:%s%s' % (col2, row, col13, row),
                            '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col3, row, col14, row),
                            total_size1 or '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col4, row, col15, row),
                            total_size2 or '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col5, row, col6, row),
                            total_size3 or '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col6, row, col7, row),
                            total_size4 or '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col7, row, col8, row),
                            total_size5 or '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col8, row, col9, row),
                            total_size6 or '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col9, row, col10, row),
                            total_size7 or '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col10, row, col11, row),
                            total_size8 or '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col11, row, col12, row),
                            total_qty or '', wbf['title_content_number'])
            worksheet.write('%s%s:%s%s' % (col12, row, col13,
                            row), '', wbf['title_doc2_float'])
            worksheet.write('%s%s:%s%s' % (col13, row, col14, row),
                            total_price or '', wbf['title_doc2_float'])
            worksheet.write('%s%s:%s%s' % (col14, row, col15,
                            row), '', wbf['title_doc2_float'])
            worksheet.write('%s%s:%s%s' % (col15, row, col16, row),
                            total_cost or '', wbf['title_doc2_float'])
            worksheet.write('%s%s:%s%s' % (col16, row, col17, row),
                            total_profit or '', wbf['title_doc2_float'])
            row += 1

            grandtotal_size1 += total_size1
            grandtotal_size2 += total_size2
            grandtotal_size3 += total_size3
            grandtotal_size4 += total_size4
            grandtotal_size5 += total_size5
            grandtotal_size6 += total_size6
            grandtotal_size7 += total_size7
            grandtotal_size8 += total_size8
            grandtotal_qty += total_qty
            grandtotal_price += total_price
            grandtotal_cost += total_cost
            grandtotal_profit += total_profit

        worksheet.merge_range('%s%s:%s%s' % (
            col0, row, col2, row), 'Grand Total ', wbf['title_doc3_float'])
        worksheet.write('%s%s:%s%s' % (col2, row, col13, row),
                        '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col3, row, col14, row),
                        grandtotal_size1 or '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col4, row, col15, row),
                        grandtotal_size2 or '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col5, row, col6, row),
                        grandtotal_size3 or '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col6, row, col7, row),
                        grandtotal_size4 or '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col7, row, col8, row),
                        grandtotal_size5 or '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col8, row, col9, row),
                        grandtotal_size6 or '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col9, row, col10, row),
                        grandtotal_size7 or '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col10, row, col11, row),
                        grandtotal_size8 or '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col11, row, col12, row),
                        grandtotal_qty or '', wbf['title_content_number'])
        worksheet.write('%s%s:%s%s' % (col12, row, col13, row),
                        '', wbf['title_doc2_float'])
        worksheet.write('%s%s:%s%s' % (col13, row, col14, row),
                        grandtotal_price or '', wbf['title_doc2_float'])
        worksheet.write('%s%s:%s%s' % (col14, row, col15, row),
                        '', wbf['title_doc2_float'])
        worksheet.write('%s%s:%s%s' % (col15, row, col16, row),
                        grandtotal_cost or '', wbf['title_doc2_float'])
        worksheet.write('%s%s:%s%s' % (col16, row, col17, row),
                        grandtotal_profit or '', wbf['title_doc2_float'])

        row += 1

        worksheet.merge_range('%s%s:%s%s' % (
            col0, row, col1, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col2, row, col4, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col5, row, col8, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col9, row, col11, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col12, row, col16, row), '', wbf['footer'])
        row += 1
        worksheet.merge_range('%s%s:%s%s' % (
            col0, row, col1, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col2, row, col4, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col5, row, col8, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col9, row, col11, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col12, row, col16, row), '', wbf['footer'])
        row += 1
        worksheet.merge_range('%s%s:%s%s' % (
            col0, row, col1, row), 'Mengetahui,', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col2, row, col4, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col5, row, col8, row), 'Menerima,', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col9, row, col11, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col12, row, col16, row), 'Menyerahkan,', wbf['footer'])
        row += 1
        worksheet.merge_range('%s%s:%s%s' % (
            col0, row, col1, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col2, row, col4, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col5, row, col8, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col9, row, col11, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col12, row, col16, row), '', wbf['footer'])
        row += 1
        worksheet.merge_range('%s%s:%s%s' % (
            col0, row, col1, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col2, row, col4, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col5, row, col8, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col9, row, col11, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col12, row, col16, row), '', wbf['footer'])
        row += 1
        worksheet.merge_range('%s%s:%s%s' % (
            col0, row, col1, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col2, row, col4, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col5, row, col8, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col9, row, col11, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col12, row, col16, row), '', wbf['footer'])
        row += 1
        worksheet.merge_range('%s%s:%s%s' % (
            col0, row, col1, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col2, row, col4, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col5, row, col8, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col9, row, col11, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col12, row, col16, row), '', wbf['footer'])
        row += 1
        worksheet.merge_range('%s%s:%s%s' % (
            col0, row, col1, row), '(____________)', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col2, row, col4, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col5, row, col8, row), '(____________)', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col9, row, col11, row), '', wbf['footer'])
        worksheet.merge_range('%s%s:%s%s' % (
            col12, row, col16, row), '(____________)', wbf['footer'])
        row += 1

        workbook.close()
        out = base64.encodestring(fp.getvalue())
        self.write({'datas': out, 'datas_fname': filename})
        fp.close()
        filename += '%2Exlsx'

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model=' + self._name + '&id=' + str(
                self.id) + '&field=datas&download=true&filename=' + filename,
        }

    def add_workbook_format(self, workbook):
        colors = {
            'white_orange': '#FFFFDB',
            'white': '#FFFFFF',
            'orange': '#FFC300',
            'red': '#FF0000',
            'yellow': '#F6FA03',
            'pink': '#FF69B4',
            'violet': '#EE82EE',
            'gray': '#DCDCDC'
        }

        wbf = {}

        wbf['footer'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'font_color': '#000000', 'font_name': 'Calibri',
             'bg_color': colors['white']})
        # wbf['footer'].set_border()

        wbf['header'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': '#FFFFDB', 'font_color': '#000000', 'font_name': 'Calibri'})
        wbf['header'].set_border()

        wbf['header_pink'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['pink'], 'font_color': '#000000', 'font_name': 'Calibri'})
        wbf['header_pink'].set_border()

        wbf['header_violet'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['violet'], 'font_color': '#000000',
             'font_name': 'Calibri'})
        wbf['header_violet'].set_border()

        wbf['header_orange'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['gray'], 'font_color': '#000000',
             'font_name': 'Calibri'})
        wbf['header_orange'].set_border()

        wbf['header_yellow'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['yellow'], 'font_color': '#000000',
             'font_name': 'Calibri'})
        wbf['header_yellow'].set_border()

        wbf['header_no'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'bg_color': colors['gray'], 'font_color': '#000000', 'font_name': 'Calibri'})

        wbf['header_number'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['gray'], 'font_color': '#000000',
             'font_name': 'Calibri'})
        # wbf['header_no'].set_border()
        # wbf['header_no'].set_align('vcenter')

        # wbf['footer'] = workbook.add_format({'align':'left', 'font_name': 'Calibri'})

        wbf['content_datetime'] = workbook.add_format(
            {'num_format': 'yyyy-mm-dd hh:mm:ss', 'font_name': 'Calibri'})
        wbf['content_datetime'].set_left()
        wbf['content_datetime'].set_right()

        wbf['content_date'] = workbook.add_format(
            {'num_format': 'yyyy-mm-dd', 'font_name': 'Calibri'})
        wbf['content_date'].set_left()
        wbf['content_date'].set_right()

        wbf['bg_color'] = workbook.add_format({
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 20,
            'font_name': 'Calibri',
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc2'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 14,
            'font_name': 'Calibri',
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc3'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': 'Calibri',
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc2_float'] = workbook.add_format({
            'bold': True,
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 14,
            'font_name': 'Calibri',
            'bg_color': '#FFFFFF',
            'num_format': '#,##0',
        })

        wbf['title_doc3_float'] = workbook.add_format({
            'bold': True,
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': 'Calibri',
            'bg_color': '#FFFFFF',
        })

        # wbf['title_doc3'].set_top()
        # wbf['title_doc3'].set_bottom()
        # wbf['title_doc3'].set_left()
        # wbf['title_doc3'].set_right()

        wbf['company'] = workbook.add_format(
            {'align': 'left', 'font_name': 'Calibri'})
        wbf['company'].set_font_size(11)

        wbf['content'] = workbook.add_format(
            {'align': 'left', 'font_name': 'Calibri', 'bg_color': '#FFFFFF', })
        wbf['content'].set_font_size(11)
        # wbf['content'].set_left()
        # wbf['content'].set_right()

        wbf['content2'] = workbook.add_format(
            {'align': 'left', 'font_name': 'Calibri', 'bg_color': '#FFFFFF', })
        wbf['content2'].set_font_size(11)
        # wbf['content2'].set_left()
        # wbf['content2'].set_right()

        wbf['content_float'] = workbook.add_format(
            {'align': 'right', 'num_format': '#,##0', 'font_name': 'Calibri', 'bg_color': '#FFFFFF', })
        # wbf['content_float'].set_right()
        # wbf['content_float'].set_left()

        wbf['title_content_number'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'num_format': '#,##0', 'font_name': 'Calibri', 'bg_color': '#FFFFFF', })
        wbf['content_number'] = workbook.add_format(
            {'align': 'center', 'num_format': '#,##0', 'font_name': 'Calibri', 'bg_color': '#FFFFFF', })
        # wbf['content_number'].set_right()
        # wbf['content_number'].set_left()

        wbf['content_percent'] = workbook.add_format(
            {'align': 'right', 'num_format': '0.00%', 'font_name': 'Calibri'})
        wbf['content_percent'].set_right()
        wbf['content_percent'].set_left()

        wbf['total_float'] = workbook.add_format(
            {'bold': 1, 'align': 'right', 'num_format': '#,##0', 'font_name': 'Calibri', 'bg_color': '#FFFFFF', })
        # wbf['total_float'].set_top()
        # wbf['total_float'].set_bottom()
        # wbf['total_float'].set_left()
        # wbf['total_float'].set_right()

        wbf['total_number'] = workbook.add_format(
            {'align': 'right', 'bg_color': colors['gray'], 'bold': 1, 'num_format': '#,##0',
             'font_name': 'Calibri'})
        wbf['total_number'].set_top()
        wbf['total_number'].set_bottom()
        wbf['total_number'].set_left()
        wbf['total_number'].set_right()

        wbf['total'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['gray'], 'align': 'center', 'font_name': 'Calibri'})
        wbf['total'].set_left()
        wbf['total'].set_right()
        wbf['total'].set_top()
        wbf['total'].set_bottom()

        wbf['total_float_yellow'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['yellow'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Calibri'})
        wbf['total_float_yellow'].set_top()
        wbf['total_float_yellow'].set_bottom()
        wbf['total_float_yellow'].set_left()
        wbf['total_float_yellow'].set_right()

        wbf['total_number_yellow'] = workbook.add_format(
            {'align': 'right', 'bg_color': colors['yellow'], 'bold': 1, 'num_format': '#,##0', 'font_name': 'Calibri'})
        wbf['total_number_yellow'].set_top()
        wbf['total_number_yellow'].set_bottom()
        wbf['total_number_yellow'].set_left()
        wbf['total_number_yellow'].set_right()

        wbf['total_yellow'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['yellow'], 'align': 'center', 'font_name': 'Calibri'})
        wbf['total_yellow'].set_left()
        wbf['total_yellow'].set_right()
        wbf['total_yellow'].set_top()
        wbf['total_yellow'].set_bottom()

        wbf['total_float_orange'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['gray'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Calibri'})
        wbf['total_float_orange'].set_top()
        wbf['total_float_orange'].set_bottom()
        wbf['total_float_orange'].set_left()
        wbf['total_float_orange'].set_right()

        wbf['total_number_orange'] = workbook.add_format(
            {'align': 'right', 'bg_color': colors['gray'], 'bold': 1, 'num_format': '#,##0', 'font_name': 'Calibri'})
        wbf['total_number_orange'].set_top()
        wbf['total_number_orange'].set_bottom()
        wbf['total_number_orange'].set_left()
        wbf['total_number_orange'].set_right()

        wbf['total_orange'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['gray'], 'align': 'center', 'font_name': 'Calibri'})
        wbf['total_orange'].set_left()
        wbf['total_orange'].set_right()
        wbf['total_orange'].set_top()
        wbf['total_orange'].set_bottom()

        wbf['total_pink'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['pink'], 'align': 'right', 'font_name': 'Calibri'})
        wbf['total_pink'].set_left()
        wbf['total_pink'].set_right()
        wbf['total_pink'].set_top()
        wbf['total_pink'].set_bottom()

        wbf['total_float_pink'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['pink'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Calibri'})
        wbf['total_float_pink'].set_left()
        wbf['total_float_pink'].set_right()
        wbf['total_float_pink'].set_top()
        wbf['total_float_pink'].set_bottom()

        wbf['total_float_pink2'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['pink'], 'align': 'center', 'num_format': '#,##0', 'font_name': 'Calibri'})
        wbf['total_float_pink2'].set_left()
        wbf['total_float_pink2'].set_right()
        wbf['total_float_pink2'].set_top()
        wbf['total_float_pink2'].set_bottom()

        wbf['total_violet'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['violet'], 'align': 'right', 'font_name': 'Calibri'})
        wbf['total_violet'].set_left()
        wbf['total_violet'].set_right()
        wbf['total_violet'].set_top()
        wbf['total_violet'].set_bottom()

        wbf['total_float_violet'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['violet'], 'align': 'right', 'num_format': '#,##0', 'font_name': 'Calibri'})
        wbf['total_float_violet'].set_left()
        wbf['total_float_violet'].set_right()
        wbf['total_float_violet'].set_top()
        wbf['total_float_violet'].set_bottom()

        wbf['total_float_violet2'] = workbook.add_format(
            {'bold': 1, 'bg_color': colors['violet'], 'align': 'center', 'num_format': '#,##0', 'font_name': 'Calibri'})
        wbf['total_float_violet2'].set_left()
        wbf['total_float_violet2'].set_right()
        wbf['total_float_violet2'].set_top()
        wbf['total_float_violet2'].set_bottom()

        wbf['header_detail_space'] = workbook.add_format(
            {'font_name': 'Calibri'})
        wbf['header_detail_space'].set_left()
        wbf['header_detail_space'].set_right()
        wbf['header_detail_space'].set_top()
        wbf['header_detail_space'].set_bottom()

        wbf['header_detail'] = workbook.add_format(
            {'bg_color': '#E0FFC2', 'font_name': 'Calibri'})
        wbf['header_detail'].set_left()
        wbf['header_detail'].set_right()
        wbf['header_detail'].set_top()
        wbf['header_detail'].set_bottom()

        return wbf, workbook
