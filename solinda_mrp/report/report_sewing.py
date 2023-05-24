from odoo import api, fields, models
from datetime import datetime, timedelta


class SewingReportXlsx(models.AbstractModel):
    _name = 'report.solinda_mrp.report_sewing'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):

        datas = data.get('form', {})
        mp_ids = self.env['mrp.production'].sudo().search([
                ('trans_date', '>=', datas.get('start_date')),
                ('trans_date', '<=', datas.get('end_date')),
                ('state', 'in', ['progress', 'to_close', 'done']),
                ('customer', 'in', datas.get('customer')),
            ])

        # title_workcenter = self.env['mrp.workcenter'].sudo().search([('id', '=', datas.get('service'))])
        from_date = datetime.strptime(datas.get('start_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        to_date = datetime.strptime(datas.get('end_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        year_title = datetime.strptime(datas.get('start_date'), '%Y-%m-%d')
        year = str(year_title.year)


        for s in mp_ids['customer']:
            sheet = workbook.add_worksheet(s.name)

            title = "Sewing Report"
            customer_title = s.name + " " + year

            bold = workbook.add_format({'bold': True})
            format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'green', 'border': 1})
            format_2 = workbook.add_format({'align': 'center', 'border': 1})
            format_header = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True, 'size': 14, 'top': 1, 'left': 1, 'right': 1, 'bottom': 1, 'text_wrap': True, 'font': 'arial'})

            sheet.merge_range('A1:K1', title, format_header)
            sheet.merge_range('A2:K2', customer_title, format_header)
            sheet.merge_range('A3:K3', f'{from_date} - {to_date}', format_header)

            row = 3
            col = 0
            sheet.write(row, col, 'No', format_1)
            sheet.write(row, col + 1, 'Date', format_1)
            sheet.write(row, col + 2, 'Style Name', format_1)
            sheet.write(row, col + 3, 'Customer', format_1)
            sheet.write(row, col + 4, 'Fabric', format_1) #dyeing
            sheet.write(row, col + 5, 'Color', format_1) #dyeing
            sheet.write(row, col + 6, 'Consumption Need', format_1) #dyeing
            sheet.write(row, col + 7, 'TOTAL MTR FROM DYE/PRINT', format_1) #dyeing
            sheet.write(row, col + 8, 'Date Out', format_1)
            sheet.write(row, col + 9, 'Supplier', format_1)
            sheet.write(row, col + 10, 'Total', format_1)


            no = 1
            row += 1

            mrp_ids = self.env['mrp.production'].sudo().search([
                        ('trans_date', '>=', datas.get('start_date')),
                        ('trans_date', '<=', datas.get('end_date')),
                        ('state', 'in', ['progress', 'to_close', 'done']),
                        ('customer', '=', s.id),
                    ])

            for mrp in mrp_ids:
                sewing_ids =  mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'SEWING' and x.state in ['progress', 'done'])
                dyeing_ids =  mrp.workorder_ids.filtered(lambda x: x.workcenter_id.name.upper() == 'DYEING' and x.state in ['progress', 'done'])
                fabric_dyeing = []
                for f in dyeing_ids:
                    fabric_dyeing.append(f.fabric_id.product_id.id)
                move_ids =  mrp.move_raw_ids.filtered(lambda x: x.product_id.id in fabric_dyeing)
                if not sewing_ids:
                    continue
                 

                date = mrp.trans_date.strftime('%d/%m/%Y') if mrp.trans_date else ''
                customer = mrp.seq_report or ''
                product = mrp.product_tmpl_id.name or ''
                total = mrp.total_qty
                date_out = sewing_ids[0].out_date.strftime('%d/%m/%Y') if sewing_ids[0].out_date else '' if len(sewing_ids) > 0 else '' or ''
                supplier = sewing_ids[0].supplier.name or '' if len(sewing_ids) > 0 else '' or ''

                fabric_1 = dyeing_ids[0].fabric_id.product_id.name or '' if len(dyeing_ids) > 0 else '' or ''
                color_1 = dyeing_ids[0].color_id.name or '' if len(dyeing_ids) > 0 else '' or ''
                consumption_1 = move_ids[0].product_uom_qty or '' if len(move_ids) > 0 else '' or ''
                tot_dye_1 = dyeing_ids[0].total_dyeing or '' if len(dyeing_ids) > 0 else '' or ''


                sheet.write(row, col, no, format_2)
                sheet.write(row, col + 1, date, format_2)
                sheet.write(row, col + 2, product or '', format_2)
                sheet.write(row, col + 3, customer, format_2)
                sheet.write(row, col + 8, date_out, format_2)
                sheet.write(row, col + 9, supplier, format_2)
                sheet.write(row, col + 10, total, format_2)
                if len(dyeing_ids) > 1:
                    for dye in dyeing_ids:
                        fabric = dye.fabric_id.product_id.name or ''
                        consumption_2 =  mrp.move_raw_ids.filtered(lambda x: x.product_id.id == dye.fabric_id.product_id.id)
                        consumption = consumption_2.product_uom_qty or '' if len(move_ids) > 0 else '' or ''
                        color = dye.color_id.name or ''
                        tot_dye = dye.total_dyeing or ''
                        sheet.write(row, col + 4, fabric, format_2)
                        sheet.write(row, col + 5, color, format_2)
                        sheet.write(row, col + 6, consumption, format_2)
                        sheet.write(row, col + 7, tot_dye, format_2)
                        row += 1
                else:
                    sheet.write(row, col + 4, fabric_1, format_2)
                    sheet.write(row, col + 5, color_1, format_2)
                    sheet.write(row, col + 6, consumption_1, format_2)
                    sheet.write(row, col + 7, tot_dye_1, format_2)

                row += 1
                no += 1