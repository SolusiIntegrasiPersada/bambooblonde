import xlsxwriter
import base64
from odoo import fields, models, api
from io import BytesIO
from datetime import date, datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
from pytz import timezone
import pytz
import io
import itertools
from itertools import groupby

class RlkMonthyReport(models.TransientModel):
    _name = "rlk.monthy.report"
    _description = "Monthy Report .xlsx"
    
    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone(self.env.user.tz or 'UTC'))
    
    def _get_years(self):
        years = []
        show_year = 0
        next_year = datetime.today().year + 1
        while show_year < 4:
            years.append(next_year)
            next_year -= 1
            show_year += 1
        return [(str(year), year) for year in years]

    @api.model
    def _get_this_year(self):
        return str(datetime.today().year)

    @api.model
    def _get_this_month(self):
        return str(datetime.today().month)

    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)
    start_date = fields.Date('Start Period')
    end_date = fields.Date('End Period')
    last_start_date = fields.Date('Start Period')
    last_end_date = fields.Date('End Period')
    month = fields.Selection([('1','Januari'),
                              ('2','Februari'),
                              ('3','Maret'),
                              ('4','April'),
                              ('5','Mei'),
                              ('6','Juni'),
                              ('7','Juli'),
                              ('8','Agustus'),
                              ('9','September'),
                              ('10','Oktober'),
                              ('11','November'),
                              ('12','Desember')], string='Month', default=_get_this_month)
    year = fields.Selection('_get_years', string='Year', default=_get_this_year)

    @api.onchange('month','year')
    def onchange_period(self):
        if self.month and self.year:
            start_date = fields.Date.to_date(str(self.year)+'-'+str(self.month)+'-01')
            end_date = start_date + relativedelta(day=31)
            last_month_date = start_date - relativedelta(months=1)
            last_start_date = fields.Date.to_date(str(last_month_date.year)+'-'+str(last_month_date.month)+'-01')
            last_end_date = last_start_date + relativedelta(day=31)

            self.start_date = start_date
            self.end_date = end_date
            self.last_start_date = last_start_date
            self.last_end_date = last_end_date
        
    def print_excel_report(self):
        start_ds = datetime.strptime(str(self.start_date), '%Y-%m-%d')
        end_ds = datetime.strptime(str(self.end_date), '%Y-%m-%d')
        year = start_ds.strftime('%Y')
        month = start_ds.strftime('%B')
        start_day = start_ds.strftime('%d')
        end_day = end_ds.strftime('%d')

        convert_before_date = datetime.strptime(str(self.last_start_date), "%Y-%m-%d")
        first_day = convert_before_date.replace(day=1)
        month_next = first_day + relativedelta(months=+1)
        last_day = month_next - timedelta(days=1)
        convert_end_date = datetime.strptime(str(last_day), "%Y-%m-%d %H:%M:%S")
        convert_end_date = convert_end_date.strftime("%Y-%m-%d")
        before_end_day = convert_end_date

        before_year_label = convert_before_date.strftime('%Y')
        before_month_label = convert_before_date.strftime('%B')

        datetime_string = self.get_default_date_model().strftime("%Y-%m-%d %H:%M:%S")
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        report_name = 'Monthy Report'
        filename = '%s %s'%(report_name,date_string)
      
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf, workbook = self.add_workbook_format(workbook)

        worksheet = workbook.add_worksheet(report_name)

        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('G:G', 20)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:J', 20)
        worksheet.set_column('K:K', 20)
        worksheet.set_column('L:L', 20)
        worksheet.set_column('M:M', 20)
        worksheet.set_column('N:N', 20)
        worksheet.set_column('O:O', 20)
        worksheet.set_column('P:P', 20)
        worksheet.set_column('Q:Q', 20)
        worksheet.set_column('R:R', 20)
        worksheet.set_column('S:S', 20)
        worksheet.set_column('T:T', 20)
        worksheet.set_column('U:U', 20)
        worksheet.set_column('V:V', 20)
        worksheet.set_column('W:W', 20)
        worksheet.set_column('X:X', 20)
        worksheet.set_column('Y:Y', 20)
        worksheet.set_column('Z:Z', 20)

        worksheet.set_column('AA:AA', 20)
        worksheet.set_column('AB:AB', 20)
        worksheet.set_column('AC:AC', 20)
        worksheet.set_column('AD:AD', 20)
        worksheet.set_column('AE:AE', 20)
        worksheet.set_column('AF:AF', 20)
        worksheet.set_column('AG:AG', 20)
        worksheet.set_column('AH:AH', 20)
        worksheet.set_column('AI:AI', 20)
        worksheet.set_column('AJ:AJ', 20)
        worksheet.set_column('AK:AK', 20)
        worksheet.set_column('AL:AL', 20)
        worksheet.set_column('AM:AM', 20)
        worksheet.set_column('AN:AN', 20)
        worksheet.set_column('AO:AO', 20)
        worksheet.set_column('AP:AP', 20)
        worksheet.set_column('AQ:AQ', 20)
        worksheet.set_column('AR:AR', 20)
        worksheet.set_column('AS:AS', 20)
        worksheet.set_column('AT:AT', 20)
        worksheet.set_column('AU:AU', 20)
        worksheet.set_column('AV:AV', 20)
        worksheet.set_column('AW:AW', 20)
        worksheet.set_column('AX:AX', 20)
        worksheet.set_column('AY:AY', 20)
        worksheet.set_column('AZ:AZ', 20)

        worksheet.set_column('BA:BA', 20)
        worksheet.set_column('BB:BB', 20)
        worksheet.set_column('BC:BC', 20)
        worksheet.set_column('BD:BD', 20)
        worksheet.set_column('BE:BE', 20)
        worksheet.set_column('BF:BF', 20)
        worksheet.set_column('BG:BG', 20)
        worksheet.set_column('BH:BH', 20)
        worksheet.set_column('BI:BI', 20)
        worksheet.set_column('BJ:BJ', 20)
        worksheet.set_column('BK:BK', 20)
        worksheet.set_column('BL:BL', 20)
        worksheet.set_column('BM:BM', 20)
        worksheet.set_column('BN:BN', 20)
        worksheet.set_column('BO:BO', 20)
        worksheet.set_column('BP:BP', 20)
        worksheet.set_column('BQ:BQ', 20)
        worksheet.set_column('BR:BR', 20)
        worksheet.set_column('BS:BS', 20)
        worksheet.set_column('BT:BT', 20)
        worksheet.set_column('BU:BU', 20)
        worksheet.set_column('BV:BV', 20)
        worksheet.set_column('BW:BW', 20)
        worksheet.set_column('BX:BX', 20)
        worksheet.set_column('BY:BY', 20)
        worksheet.set_column('BZ:BZ', 20)

        worksheet.set_column('CA:CA', 20)
        worksheet.set_column('CB:CB', 20)
        worksheet.set_column('CC:CC', 20)
        worksheet.set_column('CD:CD', 20)
        worksheet.set_column('CE:CE', 20)
        worksheet.set_column('CF:CF', 20)
        worksheet.set_column('CG:CG', 20)
        worksheet.set_column('CH:CH', 20)
        worksheet.set_column('CI:CI', 20)
        worksheet.set_column('CJ:CJ', 20)
        worksheet.set_column('CK:CK', 20)
        worksheet.set_column('CL:CL', 20)
        worksheet.set_column('CM:CM', 20)
        worksheet.set_column('CN:CN', 20)
        worksheet.set_column('CO:CO', 20)
        worksheet.set_column('CP:CP', 20)
        worksheet.set_column('CQ:CQ', 20)
        worksheet.set_column('CR:CR', 20)
        worksheet.set_column('CS:CS', 20)
        worksheet.set_column('CT:CT', 20)
        worksheet.set_column('CU:CU', 20)
        worksheet.set_column('CV:CV', 20)
        worksheet.set_column('CW:CW', 20)
        worksheet.set_column('CX:CX', 20)
        worksheet.set_column('CY:CY', 20)
        worksheet.set_column('CZ:CZ', 20)

        worksheet.set_column('DA:DA', 20)
        worksheet.set_column('DB:DB', 20)
        worksheet.set_column('DC:DC', 20)
        worksheet.set_column('DD:DD', 20)
        worksheet.set_column('DE:DE', 20)
        worksheet.set_column('DF:DF', 20)
        worksheet.set_column('DG:DG', 20)
        worksheet.set_column('DH:DH', 20)
        worksheet.set_column('DI:DI', 20)
        worksheet.set_column('DJ:DJ', 20)
        worksheet.set_column('DK:DK', 20)
        worksheet.set_column('DL:DL', 20)
        worksheet.set_column('DM:DM', 20)
        worksheet.set_column('DN:DN', 20)
        worksheet.set_column('DO:DO', 20)
        worksheet.set_column('DP:DP', 20)
        worksheet.set_column('DQ:DQ', 20)
        worksheet.set_column('DR:DR', 20)
        worksheet.set_column('DS:DS', 20)
        worksheet.set_column('DT:DT', 20)
        worksheet.set_column('DU:DU', 20)
        worksheet.set_column('DV:DV', 20)
        worksheet.set_column('DW:DW', 20)
        worksheet.set_column('DX:DX', 20)
        worksheet.set_column('DY:DY', 20)
        worksheet.set_column('DZ:DZ', 20)

        worksheet.set_column('EA:EA', 20)
        worksheet.set_column('EB:EB', 20)
        worksheet.set_column('EC:EC', 20)
        worksheet.set_column('ED:ED', 20)
        worksheet.set_column('EE:EE', 20)
        worksheet.set_column('EF:EF', 20)
        worksheet.set_column('EG:EG', 20)
        worksheet.set_column('EH:EH', 20)
        worksheet.set_column('EI:EI', 20)
        worksheet.set_column('EJ:EJ', 20)
        worksheet.set_column('EK:EK', 20)
        worksheet.set_column('EL:EL', 20)
        worksheet.set_column('EM:EM', 20)
        worksheet.set_column('EN:EN', 20)
        worksheet.set_column('EO:EO', 20)
        worksheet.set_column('EP:EP', 20)
        worksheet.set_column('EQ:EQ', 20)
        worksheet.set_column('ER:ER', 20)
        worksheet.set_column('ES:ES', 20)
        worksheet.set_column('ET:ET', 20)
        worksheet.set_column('EU:EU', 20)
        worksheet.set_column('EV:EV', 20)
        worksheet.set_column('EW:EW', 20)
        worksheet.set_column('EX:EX', 20)
        worksheet.set_column('EY:EY', 20)
        worksheet.set_column('EZ:EZ', 20)

        worksheet.set_column('FA:FA', 20)
        worksheet.set_column('FB:FB', 20)
        worksheet.set_column('FC:FC', 20)
        worksheet.set_column('FD:FD', 20)
        worksheet.set_column('FE:FE', 20)
        worksheet.set_column('FF:FF', 20)
        worksheet.set_column('FG:FG', 20)
        worksheet.set_column('FH:FH', 20)
        worksheet.set_column('FI:FI', 20)
        worksheet.set_column('FJ:FJ', 20)
        worksheet.set_column('FK:FK', 20)
        worksheet.set_column('FL:FL', 20)
        worksheet.set_column('FM:FM', 20)
        worksheet.set_column('FN:FN', 20)
        worksheet.set_column('FO:FO', 20)
        worksheet.set_column('FP:FP', 20)
        worksheet.set_column('FQ:FQ', 20)
        worksheet.set_column('FR:FR', 20)
        worksheet.set_column('FS:FS', 20)
        worksheet.set_column('FT:FT', 20)
        worksheet.set_column('FU:FU', 20)
        worksheet.set_column('FV:FV', 20)
        worksheet.set_column('FW:FW', 20)
        worksheet.set_column('FX:FX', 20)
        worksheet.set_column('FY:FY', 20)
        worksheet.set_column('FZ:FZ', 20)

        worksheet.set_column('GA:GA', 20)

        worksheet.merge_range('A1:C1', 'SALES PERIOD OF : ' + str(start_day) + ' - ' + str(end_day) + ' ' + str(month) + ' ' + str(year) , wbf['title_doc_brown'])
        worksheet.merge_range('A2:C2', 'LAST STOCK : ' + str(end_day) + ' ' + str(month) + ' ' + str(year), wbf['title_doc_brown'])

        worksheet.write('A5:B5', 'Class', wbf['header_blue'])
        worksheet.write('B5:C5', 'Model', wbf['header_blue'])
        worksheet.write('C5:D5', 'Category', wbf['header_blue'])

        worksheet.merge_range('D3:P3', 'TOTAL SALES & STOCK - ALL SHOP + WH ', wbf['header_violet'])
        worksheet.merge_range('D4:I4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('J4:O4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('P4:P5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('D5:E5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('E5:F5', '%', wbf['header_blue'])
        worksheet.write('F5:G5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('G5:H5', '%', wbf['header_blue'])
        worksheet.write('H5:I5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('I5:J5', '%', wbf['header_blue'])
        worksheet.write('J5:K5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('K5:L5', '%', wbf['header_blue'])
        worksheet.write('L5:M5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('M5:N5', '%', wbf['header_blue'])
        worksheet.write('N5:O5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('O5:P5', '%', wbf['header_blue'])

        worksheet.merge_range('Q3:V3', 'STOCK ' + str(before_month_label) + ' ' + str(before_year_label), wbf['header_blue'])
        worksheet.merge_range('Q4:V4', 'LAST STOCK - ' + str(before_month_label), wbf['header_salmon'])

        worksheet.write('Q5:R5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('R5:S5', '%', wbf['header_blue'])
        worksheet.write('S5:T5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('T5:U5', '%', wbf['header_blue'])
        worksheet.write('U5:V5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('V5:W5', '%', wbf['header_blue'])

        worksheet.merge_range('W3:AB3', 'STOCK IN WH', wbf['header_dark_green'])
        worksheet.merge_range('W4:AB4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])

        worksheet.write('W5:X5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('X5:Y5', '%', wbf['header_blue'])
        worksheet.write('Y5:Z5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('Z5:AA5', '%', wbf['header_blue'])
        worksheet.write('AA5:AB5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('AB5:AC5', '%', wbf['header_blue'])

        worksheet.merge_range('AC3:AH3', 'RECEIVING', wbf['header_green'])
        worksheet.merge_range('AC4:AH4', 'RECEIVING - ' + str(month) + ' ' + str(year), wbf['header_dark_green'])

        worksheet.write('AC5:AD5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('AD5:AE5', '%', wbf['header_blue'])
        worksheet.write('AE5:AF5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('AF5:AG5', '%', wbf['header_blue'])
        worksheet.write('AG5:AH5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('AH5:AI5', '%', wbf['header_blue'])

        worksheet.merge_range('AI3:AU3', 'BB FLAGSHIP', wbf['header_white_orange'])
        worksheet.merge_range('AI4:AN4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('AO4:AT4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('AU4:AU5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('AI5:AJ5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('AJ5:AK5', '%', wbf['header_blue'])
        worksheet.write('AK5:AL5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('AL5:AM5', '%', wbf['header_blue'])
        worksheet.write('AM5:AN5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('AN5:AO5', '%', wbf['header_blue'])
        worksheet.write('AO5:AP5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('AP5:AQ5', '%', wbf['header_blue'])
        worksheet.write('AQ5:AR5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('AR5:AS5', '%', wbf['header_blue'])
        worksheet.write('AS5:AT5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('AT5:AU5', '%', wbf['header_blue'])

        worksheet.merge_range('AV3:BH3', 'BB BRAWA', wbf['header_white_orange'])
        worksheet.merge_range('AV4:BA4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('BB4:BG4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('BH4:BH5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('AV5:AW5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('AW5:AX5', '%', wbf['header_blue'])
        worksheet.write('AX5:AY5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('AY5:AZ5', '%', wbf['header_blue'])
        worksheet.write('AZ5:BA5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('BA5:BB5', '%', wbf['header_blue'])
        worksheet.write('BB5:BC5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('BC5:BD5', '%', wbf['header_blue'])
        worksheet.write('BD5:BE5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('BE5:BF5', '%', wbf['header_blue'])
        worksheet.write('BF5:BG5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('BG5:BH5', '%', wbf['header_blue'])

        worksheet.merge_range('BI3:BU3', 'BB BEACHWALK', wbf['header_white_orange'])
        worksheet.merge_range('BI4:BN4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('BO4:BT4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('BU4:BU5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('BI5:BJ5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('BJ5:BK5', '%', wbf['header_blue'])
        worksheet.write('BK5:BL5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('BL5:BM5', '%', wbf['header_blue'])
        worksheet.write('BM5:BN5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('BN5:BO5', '%', wbf['header_blue'])
        worksheet.write('BO5:BP5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('BP5:BQ5', '%', wbf['header_blue'])
        worksheet.write('BQ5:BR5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('BR5:BS5', '%', wbf['header_blue'])
        worksheet.write('BS5:BT5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('BT5:BU5', '%', wbf['header_blue'])

        worksheet.merge_range('BV3:CH3', 'BB GALERIA', wbf['header_white_orange'])
        worksheet.merge_range('BV4:CA4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('CB4:CG4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('CH4:CH5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('BV5:BW5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('BW5:BX5', '%', wbf['header_blue'])
        worksheet.write('BX5:BY5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('BY5:BZ5', '%', wbf['header_blue'])
        worksheet.write('BZ5:CA5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('CA5:CB5', '%', wbf['header_blue'])
        worksheet.write('CB5:CC5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('CC5:CD5', '%', wbf['header_blue'])
        worksheet.write('CD5:CE5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('CE5:CF5', '%', wbf['header_blue'])
        worksheet.write('CF5:CG5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('CG5:CH5', '%', wbf['header_blue'])

        worksheet.merge_range('CI3:CU3', 'BB SEMINYAK VILLAGE', wbf['header_white_orange'])
        worksheet.merge_range('CI4:CN4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('CO4:CT4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('CU4:CU5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('CI5:CJ5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('CJ5:CK5', '%', wbf['header_blue'])
        worksheet.write('CK5:CL5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('CL5:CM5', '%', wbf['header_blue'])
        worksheet.write('CM5:CN5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('CN5:CO5', '%', wbf['header_blue'])
        worksheet.write('CO5:CP5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('CP5:CQ5', '%', wbf['header_blue'])
        worksheet.write('CQ5:CR5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('CR5:CS5', '%', wbf['header_blue'])
        worksheet.write('CS5:CT5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('CT5:CU5', '%', wbf['header_blue'])

        worksheet.merge_range('CV3:DH3', 'BB BATU BOLONG', wbf['header_white_orange'])
        worksheet.merge_range('CV4:DA4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('DB4:DG4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('DH4:DH5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('CV5:CW5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('CW5:CX5', '%', wbf['header_blue'])
        worksheet.write('CX5:CY5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('CY5:CZ5', '%', wbf['header_blue'])
        worksheet.write('CZ5:DA5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('DA5:DB5', '%', wbf['header_blue'])
        worksheet.write('DB5:DC5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('DC5:DD5', '%', wbf['header_blue'])
        worksheet.write('DD5:DE5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('DE5:DF5', '%', wbf['header_blue'])
        worksheet.write('DF5:DG5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('DG5:DH5', '%', wbf['header_blue'])

        worksheet.merge_range('DI3:DU3', 'BB SANUR', wbf['header_white_orange'])
        worksheet.merge_range('DI4:DN4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('DO4:DT4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('DU4:DU5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('DI5:DJ5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('DJ5:DK5', '%', wbf['header_blue'])
        worksheet.write('DK5:DL5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('DL5:DM5', '%', wbf['header_blue'])
        worksheet.write('DM5:DN5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('DN5:DO5', '%', wbf['header_blue'])
        worksheet.write('DO5:DP5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('DP5:DQ5', '%', wbf['header_blue'])
        worksheet.write('DQ5:DR5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('DR5:DS5', '%', wbf['header_blue'])
        worksheet.write('DS5:DT5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('DT5:DU5', '%', wbf['header_blue'])

        worksheet.merge_range('DV3:EH3', 'BB BATU BELIG', wbf['header_white_orange'])
        worksheet.merge_range('DV4:EA4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('EB4:EG4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('EH4:EH5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('DV5:DW5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('DW5:DX5', '%', wbf['header_blue'])
        worksheet.write('DX5:DY5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('DY5:DZ5', '%', wbf['header_blue'])
        worksheet.write('DZ5:EA5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('EA5:EB5', '%', wbf['header_blue'])
        worksheet.write('EB5:EC5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('EC5:ED5', '%', wbf['header_blue'])
        worksheet.write('ED5:EE5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('EE5:EF5', '%', wbf['header_blue'])
        worksheet.write('EF5:EG5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('EG5:EH5', '%', wbf['header_blue'])

        worksheet.merge_range('EI3:EU3', 'BB PADANG', wbf['header_white_orange'])
        worksheet.merge_range('EI4:EN4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('EO4:ET4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('EU4:EU5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('EI5:EJ5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('EJ5:EK5', '%', wbf['header_blue'])
        worksheet.write('EK5:EL5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('EL5:EM5', '%', wbf['header_blue'])
        worksheet.write('EM5:EN5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('EN5:EO5', '%', wbf['header_blue'])
        worksheet.write('EO5:EP5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('EP5:EQ5', '%', wbf['header_blue'])
        worksheet.write('EQ5:ER5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('ER5:ES5', '%', wbf['header_blue'])
        worksheet.write('ES5:ET5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('ET5:EU5', '%', wbf['header_blue'])

        worksheet.merge_range('EV3:FH3', 'BB KUTA', wbf['header_white_orange'])
        worksheet.merge_range('EV4:FA4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('FB4:FG4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('FH4:FH5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('EV5:EW5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('EW5:EX5', '%', wbf['header_blue'])
        worksheet.write('EX5:EY5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('EY5:EZ5', '%', wbf['header_blue'])
        worksheet.write('EZ5:FA5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('FA5:FB5', '%', wbf['header_blue'])
        worksheet.write('FB5:FC5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('FC5:FD5', '%', wbf['header_blue'])
        worksheet.write('FD5:FE5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('FE5:FF5', '%', wbf['header_blue'])
        worksheet.write('FF5:FG5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('FG5:FH5', '%', wbf['header_blue'])

        worksheet.merge_range('FI3:FU3', 'BB PETITENGET', wbf['header_white_orange'])
        worksheet.merge_range('FI4:FN4', 'SOLD', wbf['header_light_green'])
        worksheet.merge_range('FO4:FT4', 'IN STOCK - ' + str(month) + ' ' + str(year), wbf['header_salmon'])
        worksheet.merge_range('FU4:FU5', 'Week Cover Stock', wbf['header_yellow'])

        worksheet.write('FI5:FJ5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('FJ5:FK5', '%', wbf['header_blue'])
        worksheet.write('FK5:FL5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('FL5:FM5', '%', wbf['header_blue'])
        worksheet.write('FM5:FN5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('FN5:FO5', '%', wbf['header_blue'])
        worksheet.write('FO5:FP5', 'Qty Stock', wbf['header_blue'])
        worksheet.write('FP5:FQ5', '%', wbf['header_blue'])
        worksheet.write('FQ5:FR5', 'Value Retail In Stock', wbf['header_blue'])
        worksheet.write('FR5:FS5', '%', wbf['header_blue'])
        worksheet.write('FS5:FT5', 'Value Cost In Stock', wbf['header_blue'])
        worksheet.write('FT5:FU5', '%', wbf['header_blue'])

        worksheet.merge_range('FV3:GA3', 'Onlne STORE', wbf['header_white_orange'])
        worksheet.merge_range('FV4:GA4', 'SOLD', wbf['header_light_green'])

        worksheet.write('FV5:FW5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('FW5:FX5', '%', wbf['header_blue'])
        worksheet.write('FX5:FY5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('FY5:FZ5', '%', wbf['header_blue'])
        worksheet.write('FZ5:GA5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('GA5:GB5', '%', wbf['header_blue'])


        # filter sales orders based on date range

        grandtotal_qty_sold = 0
        grandtotal_retail_sold = 0
        grandtotal_cost_sold = 0
        grandtotal_qty_stock_now = 0
        grandtotal_retail_stock_now = 0
        grandtotal_cost_stock_now = 0
        grandtotal_qty_stock_last = 0
        grandtotal_retail_stock_last = 0
        grandtotal_cost_stock_last = 0
        grandtotal_qty_received = 0
        grandtotal_retail_received = 0
        grandtotal_cost_received = 0

        grandtotal_qty_wh = 0
        grandtotal_retail_wh = 0
        grandtotal_cost_wh = 0

        grandtotal_whbb_qty_sold = 0
        grandtotal_bbflg_qty_sold = 0
        grandtotal_bbbbg_qty_sold = 0
        grandtotal_bbbwk_qty_sold = 0
        grandtotal_bbbrw_qty_sold = 0
        grandtotal_bbpdg_qty_sold = 0
        grandtotal_bbsyv_qty_sold = 0
        grandtotal_bbglr_qty_sold = 0
        grandtotal_bbblg_qty_sold = 0
        grandtotal_bbsnr_qty_sold = 0
        grandtotal_bbptg_qty_sold = 0
        grandtotal_bbkta_qty_sold = 0
        grandtotal_onlne_qty_sold = 0

        grandtotal_whbb_retail_sold = 0
        grandtotal_bbflg_retail_sold = 0
        grandtotal_bbbbg_retail_sold = 0
        grandtotal_bbbwk_retail_sold = 0
        grandtotal_bbbrw_retail_sold = 0
        grandtotal_bbpdg_retail_sold = 0
        grandtotal_bbsyv_retail_sold = 0
        grandtotal_bbglr_retail_sold = 0
        grandtotal_bbblg_retail_sold = 0
        grandtotal_bbsnr_retail_sold = 0
        grandtotal_bbptg_retail_sold = 0
        grandtotal_bbkta_retail_sold = 0
        grandtotal_onlne_retail_sold = 0

        grandtotal_whbb_cost_sold = 0
        grandtotal_bbflg_cost_sold = 0
        grandtotal_bbbbg_cost_sold = 0
        grandtotal_bbbwk_cost_sold = 0
        grandtotal_bbbrw_cost_sold = 0
        grandtotal_bbpdg_cost_sold = 0
        grandtotal_bbsyv_cost_sold = 0
        grandtotal_bbglr_cost_sold = 0
        grandtotal_bbblg_cost_sold = 0
        grandtotal_bbsnr_cost_sold = 0
        grandtotal_bbptg_cost_sold = 0
        grandtotal_bbkta_cost_sold = 0
        grandtotal_onlne_cost_sold = 0

        grandtotal_whbb_qty_stock = 0
        grandtotal_bbflg_qty_stock = 0
        grandtotal_bbbbg_qty_stock = 0
        grandtotal_bbbwk_qty_stock = 0
        grandtotal_bbbrw_qty_stock = 0
        grandtotal_bbpdg_qty_stock = 0
        grandtotal_bbsyv_qty_stock = 0
        grandtotal_bbglr_qty_stock = 0
        grandtotal_bbblg_qty_stock = 0
        grandtotal_bbsnr_qty_stock = 0
        grandtotal_bbptg_qty_stock = 0
        grandtotal_bbkta_qty_stock = 0
        grandtotal_onlne_qty_stock = 0

        grandtotal_whbb_retail_stock = 0
        grandtotal_bbflg_retail_stock = 0
        grandtotal_bbbbg_retail_stock = 0
        grandtotal_bbbwk_retail_stock = 0
        grandtotal_bbbrw_retail_stock = 0
        grandtotal_bbpdg_retail_stock = 0
        grandtotal_bbsyv_retail_stock = 0
        grandtotal_bbglr_retail_stock = 0
        grandtotal_bbblg_retail_stock = 0
        grandtotal_bbsnr_retail_stock = 0
        grandtotal_bbptg_retail_stock = 0
        grandtotal_bbkta_retail_stock = 0
        grandtotal_onlne_retail_stock = 0

        grandtotal_whbb_cost_stock = 0
        grandtotal_bbflg_cost_stock = 0
        grandtotal_bbbbg_cost_stock = 0
        grandtotal_bbbwk_cost_stock = 0
        grandtotal_bbbrw_cost_stock = 0
        grandtotal_bbpdg_cost_stock = 0
        grandtotal_bbsyv_cost_stock = 0
        grandtotal_bbglr_cost_stock = 0
        grandtotal_bbblg_cost_stock = 0
        grandtotal_bbsnr_cost_stock = 0
        grandtotal_bbptg_cost_stock = 0
        grandtotal_bbkta_cost_stock = 0
        grandtotal_onlne_cost_stock = 0

        # pos_orders = self.env['pos.order.line'].search([
        #     ('order_id.state', 'not in', ['draft', 'cancel']),
        #     ('order_id.date_order', '>=', self.start_date),
        #     ('order_id.date_order', '<=', self.end_date)
        # ])


        domain_product = self.env['product.product'].with_context(to_date=self.end_date).search([
            ('type', '=', 'product'),
            # ('product_category_categ_id', '=', 508),
            # ('product_model_categ_id', '=', 484),
        ])
        data_product = domain_product.filtered(lambda x: not x.is_produk_diskon and not x.is_produk_promotion and not x.is_produk_promotion_free and not x.is_shooping_bag)



        # grouped_data = {}
        # for data in data_product:
        #     prod = data
        #     class_id = prod.class_product
        #     category = prod.product_category_categ_id
        #     parent_category = prod.product_model_categ_id
        #     name = prod.display_name
        #     # qty_sold = data.qty
        #     # order_date = data.order_id.date_order
        #     qty_sold_per_warehouse = {}
        #     warehouse_quantities = data.stock_quant_ids.filtered(
        #         lambda x: x.location_id.usage == 'internal' and
        #                   x.location_id.warehouse_id.code in (
        #                       'WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW', 'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG', 'BBSNR',
        #                       'BBPTG', 'BBKTA', 'Onlne')
        #     )
        #     qty_stock_per_warehouse = {wh.code: sum(
        #         quant.quantity for quant in warehouse_quantities if quant.location_id.warehouse_id.code == wh.code)
        #         for wh in set(warehouse_quantities.mapped('location_id.warehouse_id'))}
        #
        #     total_qty_stock = sum(qty_stock_per_warehouse.values())
        #     qty_stock = prod.qty_available
        #
        #     last_stock = self.env['product.product'].with_context(to_date=self.last_end_date).search([
        #         ('type', '=', 'product'),
        #         ('id', '=', prod.id),
        #     ])
        #     result_qty_stock_last = last_stock.mapped('qty_available')
        #     result_retail_stock_last = last_stock.mapped('lst_price')
        #     result_cost_stock_last = last_stock.mapped('standard_price')
        #
        #     qty_stock_last = float(result_qty_stock_last[0])
        #     retail_stock_last = float(result_retail_stock_last[0])
        #     cost_stock_last = float(result_cost_stock_last[0])
        #
        #     group_key = (class_id.id, category.id, parent_category.id)
        #
        #     if group_key not in grouped_data:
        #         grouped_data[group_key] = {
        #             'class_id': class_id.name,
        #             'category_id': category.name,
        #             'parent_id': parent_category.name,
        #             'qty_stock': qty_stock,
        #             'total_qty_sold': 0,
        #             # 'order_date': order_date,
        #             'product': [prod.display_name],
        #
        #             'qty_stock_last': qty_stock_last,
        #             'retail_stock_last': retail_stock_last,
        #             'cost_stock_last': cost_stock_last,
        #
        #             # 'wh': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0,
        #             #              'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
        #             # 'wh_cost_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0,
        #             #        'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
        #             # 'wh_retail_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0,
        #             #        'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
        #         }
        #     else:
        #         grouped_data[group_key]['qty_stock'] += qty_stock
        #         grouped_data[group_key]['qty_stock_last'] += qty_stock_last
        #         grouped_data[group_key]['retail_stock_last'] += retail_stock_last
        #         grouped_data[group_key]['cost_stock_last'] += cost_stock_last
        #         grouped_data[group_key]['product'].append(prod.display_name)

            # for warehouse_key, quantity_sold in qty_sold_per_warehouse.items():
            #     if warehouse_key in (
            #     'WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW', 'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG', 'BBSNR', 'BBPTG',
            #     'BBKTA', 'Onlne'):
            #         grouped_data[group_key]['wh'][warehouse_key] += quantity_sold
            #         grouped_data[group_key]['wh_cost_stock'][warehouse_key] += cost_sold
            #         grouped_data[group_key]['wh_retail_stock'][warehouse_key] += retail_sold

        report_data = {}

        for line in data_product:

            prod = line
            class_id = prod.class_product
            category = prod.product_category_categ_id
            parent_category = prod.product_model_categ_id
            cost_price = prod.standard_price or 0
            retail_price = prod.lst_price

            qty_sold_per_warehouse = {}
            pol = self.env['pos.order.line'].search([
                # ('order_id.picking_ids.move_lines.product_id', '=', prod.id),
                # ('product_id.class_product', '=', class_id.id),
                ('product_id', '=', prod.id),
                # ('order_id.state', 'not in', ['draft', 'cancel']),
                ('order_id.date_order', '>=', self.start_date),
                ('order_id.date_order', '<=', self.end_date),
                ('order_id.picking_ids.state', 'in', ['assigned', 'done']),
                (
                    'order_id.picking_ids.location_id.warehouse_id.code', 'in',
                    ('WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW',
                     'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG',
                     'BBSNR', 'BBPTG', 'BBKTA', 'Onlne'))
            ])
            for lines in pol:
                for order in lines.order_id.picking_ids:
                    wh_code = order.location_id.warehouse_id.code
                    qty_sold_per_warehouse[wh_code] = qty_sold_per_warehouse.get(wh_code, 0) + lines.qty


            warehouse_quantities = line.stock_quant_ids.filtered(
                lambda x: x.location_id.usage == 'internal' and
                          x.location_id.warehouse_id.code in (
                              'WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW', 'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG', 'BBSNR',
                              'BBPTG', 'BBKTA', 'Onlne')
            )
            qty_stock_per_warehouse = {wh.code: sum(
                quant.quantity for quant in warehouse_quantities if quant.location_id.warehouse_id.code == wh.code)
                for wh in set(warehouse_quantities.mapped('location_id.warehouse_id'))}

            total_qty_stock = sum(qty_stock_per_warehouse.values())

            sold_per_warehouse = sum(qty_sold_per_warehouse.values())
            retail_pos = sum(pol.product_id.mapped('lst_price'))
            cost_pos = sum(pol.product_id.mapped('standard_price'))

            retail_sold = sold_per_warehouse * retail_pos
            cost_sold = sold_per_warehouse * cost_pos

            qty_sold = sum(qty_sold_per_warehouse.values())
            qty_stock = prod.qty_available

            # retail_sold = qty_sold * retail_price
            # cost_sold = qty_sold * cost_price
            # warehouse = line.order_id.picking_type_id.warehouse_id

            # qty_stock = sum(line.product_id.stock_quant_ids.filtered(lambda x: x.location_id.usage == 'internal' and x.location_id == warehouse and x.in_date >= self.last_start_date and x.in_date <= self.end_date).mapped('quantity'))
            # qty_stock_wh = sum(line.product_id.stock_quant_ids.filtered(lambda x: x.location_id.usage == 'internal' and x.location_id.warehouse_id.code == 'WHBB' and x.in_date.date() >= self.last_start_date and x.in_date.date() <= self.end_date).mapped('quantity'))
            stock_quant = self.env['stock.quant'].sudo().search([
                        ('location_id.usage', '=', 'internal'),
                        ('name_warehouse_id.code', '=', 'WHBB'),
                        ('product_id', '=', prod.id),
                    ])
            stock_quant_qty = stock_quant.mapped('inventory_quantity_auto_apply')
            stock_quant_retail = stock_quant.mapped('product_id.lst_price')
            stock_quant_cost = stock_quant.mapped('product_id.standard_price')

            qty_stock_wh = sum(stock_quant_qty)
            retail_stock_wh = qty_stock_wh * sum(stock_quant_retail)
            cost_stock_wh = qty_stock_wh * sum(stock_quant_cost)

            # qty_stock_wh = 0
            # for quant in stock_quant:
            #     qty_stock_wh += quant.quantity

            # qty_stock = prod.qty_available
            # qty_stock = sum(line.product_id.qty_available for line in lines)
            # qty_stock = sum(line.product_id.product_tmpl_id.qty_available for line in lines)
            # qty_received = sum(line.product_id.stock_move_ids.filtered(lambda x: x.picking_type_id.code == 'incoming' and x.location_dest_id.warehouse_id.code in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Onlne') and x.state == 'done' and x.date.date() >= self.last_start_date and x.date.date() <= self.end_date).mapped('product_uom_qty'))
            qty_received_qty = self.env['stock.move.line'].search([
                ('product_id.class_product', '=', class_id.id),
                ('product_id', '=', prod.id),
                ('product_id.product_category_categ_id', '=', category.id),
                ('product_id.product_model_categ_id', '=', parent_category.id),
                ('picking_id.picking_type_id.code', '=', 'incoming'),
                ('location_dest_id.warehouse_id.code', 'in', [
                    'WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW',
                    'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG', 'BBSNR',
                    'BBPTG', 'BBKTA', 'Onlne'
                ]),
                ('state', '=', 'done'),
                ('date', '>=', self.start_date),
                ('date', '<=', self.end_date),
            ])
            qty_receiving = qty_received_qty.mapped('qty_done')
            retail_qty_receiving = qty_received_qty.mapped('product_id.lst_price')
            cost_qty_receiving = qty_received_qty.mapped('product_id.standard_price')

            qty_received = sum(qty_receiving)
            retail_received = sum(retail_qty_receiving) * qty_received
            cost_received = sum(cost_qty_receiving) * qty_received

            retail_stock = qty_stock * retail_price
            cost_stock = qty_stock * cost_price

            last_stock = self.env['product.product'].with_context(to_date=self.last_end_date).search([
                ('type', '=', 'product'),
                ('id', '=', prod.id),
            ])
            result_qty_stock_last = last_stock.mapped('qty_available')
            result_retail_stock_last = last_stock.mapped('lst_price')
            result_cost_stock_last = last_stock.mapped('standard_price')

            qty_stock_last = float(result_qty_stock_last[0])
            retail_stock_last = float(result_retail_stock_last[0]) * qty_stock_last
            cost_stock_last = float(result_cost_stock_last[0]) * qty_stock_last

            # create keys for the report_data dictionary
            key = (class_id.id, parent_category.id, category.id)

            if key not in report_data:
                report_data[key] = {
                    'class_name': class_id.name,
                    'parent_category': parent_category.name,
                    'category': category.name,
                    'cost_price': cost_price,
                    'retail_price': retail_price,

                    'total_qty_sold': 0,
                    'total_retail_sold': retail_sold,
                    'total_cost_sold': cost_sold,

                    'total_qty_stock_now': qty_stock,
                    'total_retail_stock_now': retail_stock,
                    'total_cost_stock_now': cost_stock,

                    'total_qty_stock_last': qty_stock_last,
                    'total_retail_stock_last': retail_stock_last,
                    'total_cost_stock_last': cost_stock_last,

                    'total_qty_receiving': qty_received,
                    'total_retail_receiving': retail_received,
                    'total_cost_receiving': cost_received,

                    'total_qty_wh': qty_stock_wh,
                    'total_retail_wh': retail_stock_wh,
                    'total_cost_wh': cost_stock_wh,

                    'w_qty_sold': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Onlne': 0},
                    'w_qty_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Onlne': 0},
                    'w_retail_sold': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Onlne': 0},
                    'w_retail_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Onlne': 0},
                    'w_cost_sold': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Onlne': 0},
                    'w_cost_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Onlne': 0},
                }
            else:

                report_data[key]['total_retail_sold'] += retail_sold
                report_data[key]['total_cost_sold'] += cost_sold

                report_data[key]['total_qty_stock_now'] += qty_stock
                report_data[key]['total_retail_stock_now'] += retail_stock
                report_data[key]['total_cost_stock_now'] += cost_stock

                report_data[key]['total_qty_stock_last'] += qty_stock_last
                report_data[key]['total_retail_stock_last'] += retail_stock_last
                report_data[key]['total_cost_stock_last'] += cost_stock_last

                report_data[key]['total_qty_receiving'] += qty_received
                report_data[key]['total_retail_receiving'] += retail_received
                report_data[key]['total_cost_receiving'] += cost_received

                report_data[key]['total_qty_wh'] += qty_stock_wh
                report_data[key]['total_retail_wh'] += retail_stock_wh
                report_data[key]['total_cost_wh'] += cost_stock_wh

            grandtotal_retail_sold += retail_sold
            grandtotal_cost_sold += cost_sold

            grandtotal_qty_stock_now += qty_stock
            grandtotal_retail_stock_now += retail_stock
            grandtotal_cost_stock_now += cost_stock

            grandtotal_qty_stock_last += qty_stock_last
            grandtotal_retail_stock_last += retail_stock_last
            grandtotal_cost_stock_last += cost_stock_last

            grandtotal_qty_received += qty_received
            grandtotal_retail_received += retail_received
            grandtotal_cost_received += cost_received

            grandtotal_qty_wh += qty_stock_wh
            grandtotal_retail_wh += retail_stock_wh
            grandtotal_cost_wh += cost_stock_wh



            # for warehouse_key, quantity_stock in qty_stock_per_warehouse.items():
            #     if warehouse_key in (
            #     'WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW', 'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG', 'BBSNR', 'BBPTG',
            #     'BBKTA', 'Onlne'):
            #         report_data[key]['total_qty_stock_now'] += quantity_stock
            #         report_data[key]['total_retail_stock_now'] += retail_stock
            #         report_data[key]['total_cost_stock_now'] += cost_stock


            for warehouse_key, quantity_sold in qty_sold_per_warehouse.items():
                if warehouse_key in (
                'WHBB', 'BBFLG', 'BBBBG', 'BBBWK', 'BBBRW', 'BBPDG', 'BBSYV', 'BBGLR', 'BBBLG', 'BBSNR', 'BBPTG',
                'BBKTA', 'Onlne'):
                    grandtotal_qty_sold += quantity_sold

                    report_data[key]['w_cost_sold'][warehouse_key] += cost_sold
                    report_data[key]['w_retail_sold'][warehouse_key] += retail_sold
                    report_data[key]['w_qty_sold'][warehouse_key] += quantity_sold

                    report_data[key]['total_qty_sold'] += quantity_sold

                    if warehouse_key == 'WHBB':
                        grandtotal_whbb_qty_sold += qty_sold
                    elif warehouse_key == 'BBFLG':
                        grandtotal_bbflg_qty_sold += qty_sold
                    elif warehouse_key == 'BBBBG':
                        grandtotal_bbbbg_qty_sold += qty_sold
                    elif warehouse_key == 'BBBWK':
                        grandtotal_bbbwk_qty_sold += qty_sold
                    elif warehouse_key == 'BBBRW':
                        grandtotal_bbbrw_qty_sold += qty_sold
                    elif warehouse_key == 'BBPDG':
                        grandtotal_bbpdg_qty_sold += qty_sold
                    elif warehouse_key == 'BBSYV':
                        grandtotal_bbsyv_qty_sold += qty_sold
                    elif warehouse_key == 'BBGLR':
                        grandtotal_bbglr_qty_sold += qty_sold
                    elif warehouse_key == 'BBBLG':
                        grandtotal_bbblg_qty_sold += qty_sold
                    elif warehouse_key == 'BBSNR':
                        grandtotal_bbsnr_qty_sold += qty_sold
                    elif warehouse_key == 'BBPTG':
                        grandtotal_bbptg_qty_sold += qty_sold
                    elif warehouse_key == 'BBKTA':
                        grandtotal_bbkta_qty_sold += qty_sold
                    elif warehouse_key == 'Onlne':
                        grandtotal_onlne_qty_sold += qty_sold


            # warehouse_key = warehouse.code
            for warehouse_key, quantity_stock in qty_stock_per_warehouse.items():
                if warehouse_key in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Onlne'):
                # if line.order_id.date_order.date() >= self.start_date.replace(day=1) and line.order_id.date_order.date() <= self.end_date.replace(day=calendar.monthrange(self.end_date.year, self.end_date.month)[1]):
            # else:

                    # report_data[key]['w_qty_sold'][warehouse_key] += qty_sold
                    report_data[key]['w_qty_stock'][warehouse_key] += qty_stock

                    # report_data[key]['w_retail_sold'][warehouse_key] += retail_sold
                    # report_data[key]['w_cost_sold'][warehouse_key] += cost_sold

                    report_data[key]['w_retail_stock'][warehouse_key] += retail_stock
                    report_data[key]['w_cost_stock'][warehouse_key] += cost_stock


                    if warehouse_key == 'WHBB':
                        # grandtotal_whbb_qty_sold += qty_sold
                        grandtotal_whbb_retail_sold += retail_sold
                        grandtotal_whbb_cost_sold += cost_sold
                        grandtotal_whbb_qty_stock += qty_stock_wh
                        grandtotal_whbb_retail_stock += retail_stock_wh
                        grandtotal_whbb_cost_stock += cost_stock_wh

                    elif warehouse_key == 'BBFLG':
                        # grandtotal_bbflg_qty_sold += qty_sold
                        grandtotal_bbflg_retail_sold += retail_sold
                        grandtotal_bbflg_cost_sold += cost_sold
                        grandtotal_bbflg_qty_stock += qty_stock
                        grandtotal_bbflg_retail_stock += retail_stock
                        grandtotal_bbflg_cost_stock += cost_stock

                    elif warehouse_key == 'BBBBG':
                        # grandtotal_bbbbg_qty_sold += qty_sold
                        grandtotal_bbbbg_retail_sold += retail_sold
                        grandtotal_bbbbg_cost_sold += cost_sold
                        grandtotal_bbbbg_qty_stock += qty_stock
                        grandtotal_bbbbg_retail_stock += retail_stock
                        grandtotal_bbbbg_cost_stock += cost_stock

                    elif warehouse_key == 'BBBWK':
                        # grandtotal_bbbwk_qty_sold += qty_sold
                        grandtotal_bbbwk_retail_sold += retail_sold
                        grandtotal_bbbwk_cost_sold += cost_sold
                        grandtotal_bbbwk_qty_stock += qty_stock
                        grandtotal_bbbwk_retail_stock += retail_stock
                        grandtotal_bbbwk_cost_stock += cost_stock

                    elif warehouse_key == 'BBBRW':
                        # grandtotal_bbbrw_qty_sold += qty_sold
                        grandtotal_bbbrw_retail_sold += retail_sold
                        grandtotal_bbbrw_cost_sold += cost_sold
                        grandtotal_bbbrw_qty_stock += qty_stock
                        grandtotal_bbbrw_retail_stock += retail_stock
                        grandtotal_bbbrw_cost_stock += cost_stock

                    elif warehouse_key == 'BBPDG':
                        # grandtotal_bbpdg_qty_sold += qty_sold
                        grandtotal_bbpdg_retail_sold += retail_sold
                        grandtotal_bbpdg_cost_sold += cost_sold
                        grandtotal_bbpdg_qty_stock += qty_stock
                        grandtotal_bbpdg_retail_stock += retail_stock
                        grandtotal_bbpdg_cost_stock += cost_stock

                    elif warehouse_key == 'BBSYV':
                        # grandtotal_bbsyv_qty_sold += qty_sold
                        grandtotal_bbsyv_retail_sold += retail_sold
                        grandtotal_bbsyv_cost_sold += cost_sold
                        grandtotal_bbsyv_qty_stock += qty_stock
                        grandtotal_bbsyv_retail_stock += retail_stock
                        grandtotal_bbsyv_cost_stock += cost_stock

                    elif warehouse_key == 'BBGLR':
                        # grandtotal_bbglr_qty_sold += qty_sold
                        grandtotal_bbglr_retail_sold += retail_sold
                        grandtotal_bbglr_cost_sold += cost_sold
                        grandtotal_bbglr_qty_stock += qty_stock
                        grandtotal_bbglr_retail_stock += retail_stock
                        grandtotal_bbglr_cost_stock += cost_stock

                    elif warehouse_key == 'BBBLG':
                        # grandtotal_bbblg_qty_sold += qty_sold
                        grandtotal_bbblg_retail_sold += retail_sold
                        grandtotal_bbblg_cost_sold += cost_sold
                        grandtotal_bbblg_qty_stock += qty_stock
                        grandtotal_bbblg_retail_stock += retail_stock
                        grandtotal_bbblg_cost_stock += cost_stock

                    elif warehouse_key == 'BBSNR':
                        # grandtotal_bbsnr_qty_sold += qty_sold
                        grandtotal_bbsnr_retail_sold += retail_sold
                        grandtotal_bbsnr_cost_sold += cost_sold
                        grandtotal_bbsnr_qty_stock += qty_stock
                        grandtotal_bbsnr_retail_stock += retail_stock
                        grandtotal_bbsnr_cost_stock += cost_stock

                    elif warehouse_key == 'BBPTG':
                        # grandtotal_bbptg_qty_sold += qty_sold
                        grandtotal_bbptg_retail_sold += retail_sold
                        grandtotal_bbptg_cost_sold += cost_sold
                        grandtotal_bbptg_qty_stock += qty_stock
                        grandtotal_bbptg_retail_stock += retail_stock
                        grandtotal_bbptg_cost_stock += cost_stock

                    elif warehouse_key == 'BBKTA':
                        # grandtotal_bbkta_qty_sold += qty_sold
                        grandtotal_bbkta_retail_sold += retail_sold
                        grandtotal_bbkta_cost_sold += cost_sold
                        grandtotal_bbkta_qty_stock += qty_stock
                        grandtotal_bbkta_retail_stock += retail_stock
                        grandtotal_bbkta_cost_stock += cost_stock

                    elif warehouse_key == 'Onlne':
                        # grandtotal_onlne_qty_sold += qty_sold
                        grandtotal_onlne_retail_sold += retail_sold
                        grandtotal_onlne_cost_sold += cost_sold
                        grandtotal_onlne_qty_stock += qty_stock
                        grandtotal_onlne_retail_stock += retail_stock
                        grandtotal_onlne_cost_stock += cost_stock




                # elif line.date_order.date() >= self.last_start_date.replace(day=1) and line.order_id.date_order.date() <= self.last_end_date.replace(day=calendar.monthrange(self.last_end_date.year, self.last_end_date.month)[1]):


        rows = []
        for data in report_data.values():
            row = [data['class_name'],
                   data['parent_category'],
                   data['category'],
                   data['cost_price'],
                   data['retail_price'],

                   data['total_qty_sold'],
                   data['total_retail_sold'],
                   data['total_cost_sold'],

                   data['total_qty_stock_now'],
                   data['total_retail_stock_now'],
                   data['total_cost_stock_now'],

                   data['total_qty_stock_last'],
                   data['total_retail_stock_last'],
                   data['total_cost_stock_last'],

                   data['total_qty_receiving'],
                   data['total_retail_receiving'],
                   data['total_cost_receiving'],

                   data['total_qty_wh'],
                   data['total_retail_wh'],
                   data['total_cost_wh'],

                   data['w_qty_sold']['WHBB'],
                   data['w_qty_sold']['BBFLG'],
                   data['w_qty_sold']['BBBBG'],
                   data['w_qty_sold']['BBBWK'],
                   data['w_qty_sold']['BBBRW'],
                   data['w_qty_sold']['BBPDG'],
                   data['w_qty_sold']['BBSYV'],
                   data['w_qty_sold']['BBGLR'],
                   data['w_qty_sold']['BBBLG'],
                   data['w_qty_sold']['BBSNR'],
                   data['w_qty_sold']['BBPTG'],
                   data['w_qty_sold']['BBKTA'],
                   data['w_qty_sold']['Onlne'],

                   data['w_qty_stock']['WHBB'],
                   data['w_qty_stock']['BBFLG'],
                   data['w_qty_stock']['BBBBG'],
                   data['w_qty_stock']['BBBWK'],
                   data['w_qty_stock']['BBBRW'],
                   data['w_qty_stock']['BBPDG'],
                   data['w_qty_stock']['BBSYV'],
                   data['w_qty_stock']['BBGLR'],
                   data['w_qty_stock']['BBBLG'],
                   data['w_qty_stock']['BBSNR'],
                   data['w_qty_stock']['BBPTG'],
                   data['w_qty_stock']['BBKTA'],
                   data['w_qty_stock']['Onlne'],

                   data['w_retail_sold']['WHBB'],
                   data['w_retail_sold']['BBFLG'],
                   data['w_retail_sold']['BBBBG'],
                   data['w_retail_sold']['BBBWK'],
                   data['w_retail_sold']['BBBRW'],
                   data['w_retail_sold']['BBPDG'],
                   data['w_retail_sold']['BBSYV'],
                   data['w_retail_sold']['BBGLR'],
                   data['w_retail_sold']['BBBLG'],
                   data['w_retail_sold']['BBSNR'],
                   data['w_retail_sold']['BBPTG'],
                   data['w_retail_sold']['BBKTA'],
                   data['w_retail_sold']['Onlne'],

                   data['w_retail_stock']['WHBB'],
                   data['w_retail_stock']['BBFLG'],
                   data['w_retail_stock']['BBBBG'],
                   data['w_retail_stock']['BBBWK'],
                   data['w_retail_stock']['BBBRW'],
                   data['w_retail_stock']['BBPDG'],
                   data['w_retail_stock']['BBSYV'],
                   data['w_retail_stock']['BBGLR'],
                   data['w_retail_stock']['BBBLG'],
                   data['w_retail_stock']['BBSNR'],
                   data['w_retail_stock']['BBPTG'],
                   data['w_retail_stock']['BBKTA'],
                   data['w_retail_stock']['Onlne'],

                   data['w_cost_sold']['WHBB'],
                   data['w_cost_sold']['BBFLG'],
                   data['w_cost_sold']['BBBBG'],
                   data['w_cost_sold']['BBBWK'],
                   data['w_cost_sold']['BBBRW'],
                   data['w_cost_sold']['BBPDG'],
                   data['w_cost_sold']['BBSYV'],
                   data['w_cost_sold']['BBGLR'],
                   data['w_cost_sold']['BBBLG'],
                   data['w_cost_sold']['BBSNR'],
                   data['w_cost_sold']['BBPTG'],
                   data['w_cost_sold']['BBKTA'],
                   data['w_cost_sold']['Onlne'],

                   data['w_cost_stock']['WHBB'],
                   data['w_cost_stock']['BBFLG'],
                   data['w_cost_stock']['BBBBG'],
                   data['w_cost_stock']['BBBWK'],
                   data['w_cost_stock']['BBBRW'],
                   data['w_cost_stock']['BBPDG'],
                   data['w_cost_stock']['BBSYV'],
                   data['w_cost_stock']['BBGLR'],
                   data['w_cost_stock']['BBBLG'],
                   data['w_cost_stock']['BBSNR'],
                   data['w_cost_stock']['BBPTG'],
                   data['w_cost_stock']['BBKTA'],
                   data['w_cost_stock']['Onlne'],
                   ]
            rows.append(row)

        grouped_colors = {}

        for data in report_data.values():
            class_name = data['class_name']
            parent_category = data['parent_category']
            category = data['category']
            total_qty_sold = data['total_qty_sold']
            total_retail_sold = data['total_retail_sold']
            total_cost_sold = data['total_cost_sold']

            total_qty_stock_now = data['total_qty_stock_now']
            total_retail_stock_now = data['total_retail_stock_now']
            total_cost_stock_now = data['total_cost_stock_now']

            total_qty_stock_last = data['total_qty_stock_last']
            total_retail_stock_last = data['total_retail_stock_last']
            total_cost_stock_last = data['total_cost_stock_last']

            total_qty_receiving = data['total_qty_receiving']
            total_retail_receiving = data['total_retail_receiving']
            total_cost_receiving = data['total_cost_receiving']

            total_qty_wh = data['total_qty_wh']
            total_retail_wh = data['total_retail_wh']
            total_cost_wh = data['total_cost_wh']

            whbb_qty_sold = data['w_qty_sold']['WHBB']
            bbflg_qty_sold = data['w_qty_sold']['BBFLG']
            bbbbg_qty_sold = data['w_qty_sold']['BBBBG']
            bbbwk_qty_sold = data['w_qty_sold']['BBBWK']
            bbbrw_qty_sold = data['w_qty_sold']['BBBRW']
            bbpdg_qty_sold = data['w_qty_sold']['BBPDG']
            bbsyv_qty_sold = data['w_qty_sold']['BBSYV']
            bbglr_qty_sold = data['w_qty_sold']['BBGLR']
            bbblg_qty_sold = data['w_qty_sold']['BBBLG']
            bbsnr_qty_sold = data['w_qty_sold']['BBSNR']
            bbptg_qty_sold = data['w_qty_sold']['BBPTG']
            bbkta_qty_sold = data['w_qty_sold']['BBKTA']
            onlne_qty_sold = data['w_qty_sold']['Onlne']

            whbb_qty_stock = data['w_qty_stock']['WHBB']
            bbflg_qty_stock = data['w_qty_stock']['BBFLG']
            bbbbg_qty_stock = data['w_qty_stock']['BBBBG']
            bbbwk_qty_stock = data['w_qty_stock']['BBBWK']
            bbbrw_qty_stock = data['w_qty_stock']['BBBRW']
            bbpdg_qty_stock = data['w_qty_stock']['BBPDG']
            bbsyv_qty_stock = data['w_qty_stock']['BBSYV']
            bbglr_qty_stock = data['w_qty_stock']['BBGLR']
            bbblg_qty_stock = data['w_qty_stock']['BBBLG']
            bbsnr_qty_stock = data['w_qty_stock']['BBSNR']
            bbptg_qty_stock = data['w_qty_stock']['BBPTG']
            bbkta_qty_stock = data['w_qty_stock']['BBKTA']
            onlne_qty_stock = data['w_qty_stock']['Onlne']

            whbb_retail_sold = data['w_retail_sold']['WHBB']
            bbflg_retail_sold = data['w_retail_sold']['BBFLG']
            bbbbg_retail_sold = data['w_retail_sold']['BBBBG']
            bbbwk_retail_sold = data['w_retail_sold']['BBBWK']
            bbbrw_retail_sold = data['w_retail_sold']['BBBRW']
            bbpdg_retail_sold = data['w_retail_sold']['BBPDG']
            bbsyv_retail_sold = data['w_retail_sold']['BBSYV']
            bbglr_retail_sold = data['w_retail_sold']['BBGLR']
            bbblg_retail_sold = data['w_retail_sold']['BBBLG']
            bbsnr_retail_sold = data['w_retail_sold']['BBSNR']
            bbptg_retail_sold = data['w_retail_sold']['BBPTG']
            bbkta_retail_sold = data['w_retail_sold']['BBKTA']
            onlne_retail_sold = data['w_retail_sold']['Onlne']

            whbb_cost_sold = data['w_cost_sold']['WHBB']
            bbflg_cost_sold = data['w_cost_sold']['BBFLG']
            bbbbg_cost_sold = data['w_cost_sold']['BBBBG']
            bbbwk_cost_sold = data['w_cost_sold']['BBBWK']
            bbbrw_cost_sold = data['w_cost_sold']['BBBRW']
            bbpdg_cost_sold = data['w_cost_sold']['BBPDG']
            bbsyv_cost_sold = data['w_cost_sold']['BBSYV']
            bbglr_cost_sold = data['w_cost_sold']['BBGLR']
            bbblg_cost_sold = data['w_cost_sold']['BBBLG']
            bbsnr_cost_sold = data['w_cost_sold']['BBSNR']
            bbptg_cost_sold = data['w_cost_sold']['BBPTG']
            bbkta_cost_sold = data['w_cost_sold']['BBKTA']
            onlne_cost_sold = data['w_cost_sold']['Onlne']

            whbb_retail_stock = data['w_retail_stock']['WHBB']
            bbflg_retail_stock = data['w_retail_stock']['BBFLG']
            bbbbg_retail_stock = data['w_retail_stock']['BBBBG']
            bbbwk_retail_stock = data['w_retail_stock']['BBBWK']
            bbbrw_retail_stock = data['w_retail_stock']['BBBRW']
            bbpdg_retail_stock = data['w_retail_stock']['BBPDG']
            bbsyv_retail_stock = data['w_retail_stock']['BBSYV']
            bbglr_retail_stock = data['w_retail_stock']['BBGLR']
            bbblg_retail_stock = data['w_retail_stock']['BBBLG']
            bbsnr_retail_stock = data['w_retail_stock']['BBSNR']
            bbptg_retail_stock = data['w_retail_stock']['BBPTG']
            bbkta_retail_stock = data['w_retail_stock']['BBKTA']
            onlne_retail_stock = data['w_retail_stock']['Onlne']

            whbb_cost_stock = data['w_cost_stock']['WHBB']
            bbflg_cost_stock = data['w_cost_stock']['BBFLG']
            bbbbg_cost_stock = data['w_cost_stock']['BBBBG']
            bbbwk_cost_stock = data['w_cost_stock']['BBBWK']
            bbbrw_cost_stock = data['w_cost_stock']['BBBRW']
            bbpdg_cost_stock = data['w_cost_stock']['BBPDG']
            bbsyv_cost_stock = data['w_cost_stock']['BBSYV']
            bbglr_cost_stock = data['w_cost_stock']['BBGLR']
            bbblg_cost_stock = data['w_cost_stock']['BBBLG']
            bbsnr_cost_stock = data['w_cost_stock']['BBSNR']
            bbptg_cost_stock = data['w_cost_stock']['BBPTG']
            bbkta_cost_stock = data['w_cost_stock']['BBKTA']
            onlne_cost_stock = data['w_cost_stock']['Onlne']
            
            key = (class_name, parent_category)

            if key not in grouped_colors:
                grouped_colors[key] = {
                    'total_qty_sold': total_qty_sold,
                    'total_retail_sold': total_retail_sold,
                    'total_cost_sold': total_cost_sold,

                    'total_qty_stock_now': total_qty_stock_now,
                    'total_retail_stock_now': total_retail_stock_now,
                    'total_cost_stock_now': total_cost_stock_now,

                    'total_qty_stock_last': total_qty_stock_last,
                    'total_retail_stock_last': total_retail_stock_last,
                    'total_cost_stock_last': total_cost_stock_last,

                    'total_qty_receiving': total_qty_receiving,
                    'total_retail_receiving': total_retail_receiving,
                    'total_cost_receiving': total_cost_receiving,

                    'total_qty_wh': total_qty_wh,
                    'total_retail_wh': total_retail_wh,
                    'total_cost_wh': total_cost_wh,

                    'whbb_qty_sold': whbb_qty_sold,
                    'bbflg_qty_sold': bbflg_qty_sold,
                    'bbbbg_qty_sold': bbbbg_qty_sold,
                    'bbbwk_qty_sold': bbbwk_qty_sold,
                    'bbbrw_qty_sold': bbbrw_qty_sold,
                    'bbpdg_qty_sold': bbpdg_qty_sold,
                    'bbsyv_qty_sold': bbsyv_qty_sold,
                    'bbglr_qty_sold': bbglr_qty_sold,
                    'bbblg_qty_sold': bbblg_qty_sold,
                    'bbsnr_qty_sold': bbsnr_qty_sold,
                    'bbptg_qty_sold': bbptg_qty_sold,
                    'bbkta_qty_sold': bbkta_qty_sold,
                    'onlne_qty_sold': onlne_qty_sold,

                    'whbb_retail_sold': whbb_retail_sold,
                    'bbflg_retail_sold': bbflg_retail_sold,
                    'bbbbg_retail_sold': bbbbg_retail_sold,
                    'bbbwk_retail_sold': bbbwk_retail_sold,
                    'bbbrw_retail_sold': bbbrw_retail_sold,
                    'bbpdg_retail_sold': bbpdg_retail_sold,
                    'bbsyv_retail_sold': bbsyv_retail_sold,
                    'bbglr_retail_sold': bbglr_retail_sold,
                    'bbblg_retail_sold': bbblg_retail_sold,
                    'bbsnr_retail_sold': bbsnr_retail_sold,
                    'bbptg_retail_sold': bbptg_retail_sold,
                    'bbkta_retail_sold': bbkta_retail_sold,
                    'onlne_retail_sold': onlne_retail_sold,

                    'whbb_cost_sold': whbb_cost_sold,
                    'bbflg_cost_sold': bbflg_cost_sold,
                    'bbbbg_cost_sold': bbbbg_cost_sold,
                    'bbbwk_cost_sold': bbbwk_cost_sold,
                    'bbbrw_cost_sold': bbbrw_cost_sold,
                    'bbpdg_cost_sold': bbpdg_cost_sold,
                    'bbsyv_cost_sold': bbsyv_cost_sold,
                    'bbglr_cost_sold': bbglr_cost_sold,
                    'bbblg_cost_sold': bbblg_cost_sold,
                    'bbsnr_cost_sold': bbsnr_cost_sold,
                    'bbptg_cost_sold': bbptg_cost_sold,
                    'bbkta_cost_sold': bbkta_cost_sold,
                    'onlne_cost_sold': onlne_cost_sold,

                    'whbb_qty_stock': whbb_qty_stock,
                    'bbflg_qty_stock': bbflg_qty_stock,
                    'bbbbg_qty_stock': bbbbg_qty_stock,
                    'bbbwk_qty_stock': bbbwk_qty_stock,
                    'bbbrw_qty_stock': bbbrw_qty_stock,
                    'bbpdg_qty_stock': bbpdg_qty_stock,
                    'bbsyv_qty_stock': bbsyv_qty_stock,
                    'bbglr_qty_stock': bbglr_qty_stock,
                    'bbblg_qty_stock': bbblg_qty_stock,
                    'bbsnr_qty_stock': bbsnr_qty_stock,
                    'bbptg_qty_stock': bbptg_qty_stock,
                    'bbkta_qty_stock': bbkta_qty_stock,
                    'onlne_qty_stock': onlne_qty_stock,

                    'whbb_retail_stock': whbb_retail_stock,
                    'bbflg_retail_stock': bbflg_retail_stock,
                    'bbbbg_retail_stock': bbbbg_retail_stock,
                    'bbbwk_retail_stock': bbbwk_retail_stock,
                    'bbbrw_retail_stock': bbbrw_retail_stock,
                    'bbpdg_retail_stock': bbpdg_retail_stock,
                    'bbsyv_retail_stock': bbsyv_retail_stock,
                    'bbglr_retail_stock': bbglr_retail_stock,
                    'bbblg_retail_stock': bbblg_retail_stock,
                    'bbsnr_retail_stock': bbsnr_retail_stock,
                    'bbptg_retail_stock': bbptg_retail_stock,
                    'bbkta_retail_stock': bbkta_retail_stock,
                    'onlne_retail_stock': onlne_retail_stock,

                    'whbb_cost_stock': whbb_cost_stock,
                    'bbflg_cost_stock': bbflg_cost_stock,
                    'bbbbg_cost_stock': bbbbg_cost_stock,
                    'bbbwk_cost_stock': bbbwk_cost_stock,
                    'bbbrw_cost_stock': bbbrw_cost_stock,
                    'bbpdg_cost_stock': bbpdg_cost_stock,
                    'bbsyv_cost_stock': bbsyv_cost_stock,
                    'bbglr_cost_stock': bbglr_cost_stock,
                    'bbblg_cost_stock': bbblg_cost_stock,
                    'bbsnr_cost_stock': bbsnr_cost_stock,
                    'bbptg_cost_stock': bbptg_cost_stock,
                    'bbkta_cost_stock': bbkta_cost_stock,
                    'onlne_cost_stock': onlne_cost_stock,
                    'children': {}
                }

            else:
                grouped_colors[key]['total_qty_sold'] += total_qty_sold
                grouped_colors[key]['total_retail_sold'] += total_retail_sold
                grouped_colors[key]['total_cost_sold'] += total_cost_sold

                grouped_colors[key]['total_qty_stock_now'] += total_qty_stock_now
                grouped_colors[key]['total_retail_stock_now'] += total_retail_stock_now
                grouped_colors[key]['total_cost_stock_now'] += total_cost_stock_now

                grouped_colors[key]['total_qty_stock_last'] += total_qty_stock_last
                grouped_colors[key]['total_retail_stock_last'] += total_retail_stock_last
                grouped_colors[key]['total_cost_stock_last'] += total_cost_stock_last

                grouped_colors[key]['total_qty_receiving'] += total_qty_receiving
                grouped_colors[key]['total_retail_receiving'] += total_retail_receiving
                grouped_colors[key]['total_cost_receiving'] += total_cost_receiving

                grouped_colors[key]['total_qty_wh'] += total_qty_wh
                grouped_colors[key]['total_retail_wh'] += total_retail_wh
                grouped_colors[key]['total_cost_wh'] += total_cost_wh

                grouped_colors[key]['whbb_qty_sold'] += whbb_qty_sold
                grouped_colors[key]['bbflg_qty_sold'] += bbflg_qty_sold
                grouped_colors[key]['bbbbg_qty_sold'] += bbbbg_qty_sold
                grouped_colors[key]['bbbwk_qty_sold'] += bbbwk_qty_sold
                grouped_colors[key]['bbbrw_qty_sold'] += bbbrw_qty_sold
                grouped_colors[key]['bbpdg_qty_sold'] += bbpdg_qty_sold
                grouped_colors[key]['bbsyv_qty_sold'] += bbsyv_qty_sold
                grouped_colors[key]['bbglr_qty_sold'] += bbglr_qty_sold
                grouped_colors[key]['bbblg_qty_sold'] += bbblg_qty_sold
                grouped_colors[key]['bbsnr_qty_sold'] += bbsnr_qty_sold
                grouped_colors[key]['bbptg_qty_sold'] += bbptg_qty_sold
                grouped_colors[key]['bbkta_qty_sold'] += bbkta_qty_sold
                grouped_colors[key]['onlne_qty_sold'] += onlne_qty_sold

                grouped_colors[key]['whbb_retail_sold'] += whbb_retail_sold
                grouped_colors[key]['bbflg_retail_sold'] += bbflg_retail_sold
                grouped_colors[key]['bbbbg_retail_sold'] += bbbbg_retail_sold
                grouped_colors[key]['bbbwk_retail_sold'] += bbbwk_retail_sold
                grouped_colors[key]['bbbrw_retail_sold'] += bbbrw_retail_sold
                grouped_colors[key]['bbpdg_retail_sold'] += bbpdg_retail_sold
                grouped_colors[key]['bbsyv_retail_sold'] += bbsyv_retail_sold
                grouped_colors[key]['bbglr_retail_sold'] += bbglr_retail_sold
                grouped_colors[key]['bbblg_retail_sold'] += bbblg_retail_sold
                grouped_colors[key]['bbsnr_retail_sold'] += bbsnr_retail_sold
                grouped_colors[key]['bbptg_retail_sold'] += bbptg_retail_sold
                grouped_colors[key]['bbkta_retail_sold'] += bbkta_retail_sold
                grouped_colors[key]['onlne_retail_sold'] += onlne_retail_sold

                grouped_colors[key]['whbb_cost_sold'] += whbb_cost_sold
                grouped_colors[key]['bbflg_cost_sold'] += bbflg_cost_sold
                grouped_colors[key]['bbbbg_cost_sold'] += bbbbg_cost_sold
                grouped_colors[key]['bbbwk_cost_sold'] += bbbwk_cost_sold
                grouped_colors[key]['bbbrw_cost_sold'] += bbbrw_cost_sold
                grouped_colors[key]['bbpdg_cost_sold'] += bbpdg_cost_sold
                grouped_colors[key]['bbsyv_cost_sold'] += bbsyv_cost_sold
                grouped_colors[key]['bbglr_cost_sold'] += bbglr_cost_sold
                grouped_colors[key]['bbblg_cost_sold'] += bbblg_cost_sold
                grouped_colors[key]['bbsnr_cost_sold'] += bbsnr_cost_sold
                grouped_colors[key]['bbptg_cost_sold'] += bbptg_cost_sold
                grouped_colors[key]['bbkta_cost_sold'] += bbkta_cost_sold
                grouped_colors[key]['onlne_cost_sold'] += onlne_cost_sold

                grouped_colors[key]['whbb_qty_stock'] += whbb_qty_stock
                grouped_colors[key]['bbflg_qty_stock'] += bbflg_qty_stock
                grouped_colors[key]['bbbbg_qty_stock'] += bbbbg_qty_stock
                grouped_colors[key]['bbbwk_qty_stock'] += bbbwk_qty_stock
                grouped_colors[key]['bbbrw_qty_stock'] += bbbrw_qty_stock
                grouped_colors[key]['bbpdg_qty_stock'] += bbpdg_qty_stock
                grouped_colors[key]['bbglr_qty_stock'] += bbglr_qty_stock
                grouped_colors[key]['bbblg_qty_stock'] += bbblg_qty_stock
                grouped_colors[key]['bbsnr_qty_stock'] += bbsnr_qty_stock
                grouped_colors[key]['bbptg_qty_stock'] += bbptg_qty_stock
                grouped_colors[key]['bbkta_qty_stock'] += bbkta_qty_stock
                grouped_colors[key]['onlne_qty_stock'] += onlne_qty_stock

                grouped_colors[key]['whbb_retail_stock'] += whbb_retail_stock
                grouped_colors[key]['bbflg_retail_stock'] += bbflg_retail_stock
                grouped_colors[key]['bbbbg_retail_stock'] += bbbbg_retail_stock
                grouped_colors[key]['bbbwk_retail_stock'] += bbbwk_retail_stock
                grouped_colors[key]['bbbrw_retail_stock'] += bbbrw_retail_stock
                grouped_colors[key]['bbpdg_retail_stock'] += bbpdg_retail_stock
                grouped_colors[key]['bbsyv_retail_stock'] += bbsyv_retail_stock
                grouped_colors[key]['bbglr_retail_stock'] += bbglr_retail_stock
                grouped_colors[key]['bbblg_retail_stock'] += bbblg_retail_stock
                grouped_colors[key]['bbsnr_retail_stock'] += bbsnr_retail_stock
                grouped_colors[key]['bbptg_retail_stock'] += bbptg_retail_stock
                grouped_colors[key]['bbkta_retail_stock'] += bbkta_retail_stock
                grouped_colors[key]['onlne_retail_stock'] += onlne_retail_stock

                grouped_colors[key]['whbb_cost_stock'] += whbb_cost_stock
                grouped_colors[key]['bbflg_cost_stock'] += bbflg_cost_stock
                grouped_colors[key]['bbbbg_cost_stock'] += bbbbg_cost_stock
                grouped_colors[key]['bbbwk_cost_stock'] += bbbwk_cost_stock
                grouped_colors[key]['bbbrw_cost_stock'] += bbbrw_cost_stock
                grouped_colors[key]['bbpdg_cost_stock'] += bbpdg_cost_stock
                grouped_colors[key]['bbsyv_cost_stock'] += bbsyv_cost_stock
                grouped_colors[key]['bbglr_cost_stock'] += bbglr_cost_stock
                grouped_colors[key]['bbblg_cost_stock'] += bbblg_cost_stock
                grouped_colors[key]['bbsnr_cost_stock'] += bbsnr_cost_stock
                grouped_colors[key]['bbptg_cost_stock'] += bbptg_cost_stock
                grouped_colors[key]['bbkta_cost_stock'] += bbkta_cost_stock
                grouped_colors[key]['onlne_cost_stock'] += onlne_cost_stock

            
            category_data = grouped_colors[key]

            if category not in grouped_colors[key]['children']:
                grouped_colors[key]['children'][category] = {
                    'cost_price': cost_price,
                    'retail_price': retail_price,

                    'total_qty_sold': total_qty_sold,
                    'total_retail_sold': total_retail_sold,
                    'total_cost_sold': total_cost_sold,

                    'total_qty_stock_now': total_qty_stock_now,
                    'total_retail_stock_now': total_retail_stock_now,
                    'total_cost_stock_now': total_cost_stock_now,

                    'total_qty_stock_last': total_qty_stock_last,
                    'total_retail_stock_last': total_retail_stock_last,
                    'total_cost_stock_last': total_cost_stock_last,

                    'total_qty_receiving': total_qty_receiving,
                    'total_retail_receiving': total_retail_receiving,
                    'total_cost_receiving': total_cost_receiving,

                    'total_qty_wh': total_qty_wh,
                    'total_retail_wh': total_retail_wh,
                    'total_cost_wh': total_cost_wh,

                    'whbb_qty_sold': whbb_qty_sold,
                    'bbflg_qty_sold': bbflg_qty_sold,
                    'bbbbg_qty_sold': bbbbg_qty_sold,
                    'bbbwk_qty_sold': bbbwk_qty_sold,
                    'bbbrw_qty_sold': bbbrw_qty_sold,
                    'bbpdg_qty_sold': bbpdg_qty_sold,
                    'bbsyv_qty_sold': bbsyv_qty_sold,
                    'bbglr_qty_sold': bbglr_qty_sold,
                    'bbblg_qty_sold': bbblg_qty_sold,
                    'bbsnr_qty_sold': bbsnr_qty_sold,
                    'bbptg_qty_sold': bbptg_qty_sold,
                    'bbkta_qty_sold': bbkta_qty_sold,
                    'onlne_qty_sold': onlne_qty_sold,

                    'whbb_retail_sold': whbb_retail_sold,
                    'bbflg_retail_sold': bbflg_retail_sold,
                    'bbbbg_retail_sold': bbbbg_retail_sold,
                    'bbbwk_retail_sold': bbbwk_retail_sold,
                    'bbbrw_retail_sold': bbbrw_retail_sold,
                    'bbpdg_retail_sold': bbpdg_retail_sold,
                    'bbsyv_retail_sold': bbsyv_retail_sold,
                    'bbglr_retail_sold': bbglr_retail_sold,
                    'bbblg_retail_sold': bbblg_retail_sold,
                    'bbsnr_retail_sold': bbsnr_retail_sold,
                    'bbptg_retail_sold': bbptg_retail_sold,
                    'bbkta_retail_sold': bbkta_retail_sold,
                    'onlne_retail_sold': onlne_retail_sold,

                    'whbb_cost_sold': whbb_cost_sold,
                    'bbflg_cost_sold': bbflg_cost_sold,
                    'bbbbg_cost_sold': bbbbg_cost_sold,
                    'bbbwk_cost_sold': bbbwk_cost_sold,
                    'bbbrw_cost_sold': bbbrw_cost_sold,
                    'bbpdg_cost_sold': bbpdg_cost_sold,
                    'bbsyv_cost_sold': bbsyv_cost_sold,
                    'bbglr_cost_sold': bbglr_cost_sold,
                    'bbblg_cost_sold': bbblg_cost_sold,
                    'bbsnr_cost_sold': bbsnr_cost_sold,
                    'bbptg_cost_sold': bbptg_cost_sold,
                    'bbkta_cost_sold': bbkta_cost_sold,
                    'onlne_cost_sold': onlne_cost_sold,

                    'whbb_qty_stock': whbb_qty_stock,
                    'bbflg_qty_stock': bbflg_qty_stock,
                    'bbbbg_qty_stock': bbbbg_qty_stock,
                    'bbbwk_qty_stock': bbbwk_qty_stock,
                    'bbbrw_qty_stock': bbbrw_qty_stock,
                    'bbpdg_qty_stock': bbpdg_qty_stock,
                    'bbsyv_qty_stock': bbsyv_qty_stock,
                    'bbglr_qty_stock': bbglr_qty_stock,
                    'bbblg_qty_stock': bbblg_qty_stock,
                    'bbsnr_qty_stock': bbsnr_qty_stock,
                    'bbptg_qty_stock': bbptg_qty_stock,
                    'bbkta_qty_stock': bbkta_qty_stock,
                    'onlne_qty_stock': onlne_qty_stock,

                    'whbb_retail_stock': whbb_retail_stock,
                    'bbflg_retail_stock': bbflg_retail_stock,
                    'bbbbg_retail_stock': bbbbg_retail_stock,
                    'bbbwk_retail_stock': bbbwk_retail_stock,
                    'bbbrw_retail_stock': bbbrw_retail_stock,
                    'bbpdg_retail_stock': bbpdg_retail_stock,
                    'bbsyv_retail_stock': bbsyv_retail_stock,
                    'bbglr_retail_stock': bbglr_retail_stock,
                    'bbblg_retail_stock': bbblg_retail_stock,
                    'bbsnr_retail_stock': bbsnr_retail_stock,
                    'bbptg_retail_stock': bbptg_retail_stock,
                    'bbkta_retail_stock': bbkta_retail_stock,
                    'onlne_retail_stock': onlne_retail_stock,

                    'whbb_cost_stock': whbb_cost_stock,
                    'bbflg_cost_stock': bbflg_cost_stock,
                    'bbbbg_cost_stock': bbbbg_cost_stock,
                    'bbbwk_cost_stock': bbbwk_cost_stock,
                    'bbbrw_cost_stock': bbbrw_cost_stock,
                    'bbpdg_cost_stock': bbpdg_cost_stock,
                    'bbsyv_cost_stock': bbsyv_cost_stock,
                    'bbglr_cost_stock': bbglr_cost_stock,
                    'bbblg_cost_stock': bbblg_cost_stock,
                    'bbsnr_cost_stock': bbsnr_cost_stock,
                    'bbptg_cost_stock': bbptg_cost_stock,
                    'bbkta_cost_stock': bbkta_cost_stock,
                    'onlne_cost_stock': onlne_cost_stock,
                }
            else:
                grouped_colors[key]['total_qty_sold'] += total_qty_sold
                grouped_colors[key]['total_retail_sold'] += total_retail_sold
                grouped_colors[key]['total_cost_sold'] += total_cost_sold

                grouped_colors[key]['total_qty_stock_now'] += total_qty_stock_now
                grouped_colors[key]['total_retail_stock_now'] += total_retail_stock_now
                grouped_colors[key]['total_cost_stock_now'] += total_cost_stock_now

                grouped_colors[key]['total_qty_stock_last'] += total_qty_stock_last
                grouped_colors[key]['total_retail_stock_last'] += total_retail_stock_last
                grouped_colors[key]['total_cost_stock_last'] += total_cost_stock_last

                grouped_colors[key]['total_qty_receiving'] += total_qty_receiving
                grouped_colors[key]['total_retail_receiving'] += total_retail_receiving
                grouped_colors[key]['total_cost_receiving'] += total_cost_receiving

                grouped_colors[key]['total_qty_wh'] += total_qty_wh
                grouped_colors[key]['total_retail_wh'] += total_retail_wh
                grouped_colors[key]['total_cost_wh'] += total_cost_wh

                grouped_colors[key]['whbb_qty_sold'] += whbb_qty_sold
                grouped_colors[key]['bbflg_qty_sold'] += bbflg_qty_sold
                grouped_colors[key]['bbbbg_qty_sold'] += bbbbg_qty_sold
                grouped_colors[key]['bbbwk_qty_sold'] += bbbwk_qty_sold
                grouped_colors[key]['bbbrw_qty_sold'] += bbbrw_qty_sold
                grouped_colors[key]['bbpdg_qty_sold'] += bbpdg_qty_sold
                grouped_colors[key]['bbsyv_qty_sold'] += bbsyv_qty_sold
                grouped_colors[key]['bbglr_qty_sold'] += bbglr_qty_sold
                grouped_colors[key]['bbblg_qty_sold'] += bbblg_qty_sold
                grouped_colors[key]['bbsnr_qty_sold'] += bbsnr_qty_sold
                grouped_colors[key]['bbptg_qty_sold'] += bbptg_qty_sold
                grouped_colors[key]['bbkta_qty_sold'] += bbkta_qty_sold
                grouped_colors[key]['onlne_qty_sold'] += onlne_qty_sold

                grouped_colors[key]['whbb_retail_sold'] += whbb_retail_sold
                grouped_colors[key]['bbflg_retail_sold'] += bbflg_retail_sold
                grouped_colors[key]['bbbbg_retail_sold'] += bbbbg_retail_sold
                grouped_colors[key]['bbbwk_retail_sold'] += bbbwk_retail_sold
                grouped_colors[key]['bbbrw_retail_sold'] += bbbrw_retail_sold
                grouped_colors[key]['bbpdg_retail_sold'] += bbpdg_retail_sold
                grouped_colors[key]['bbsyv_retail_sold'] += bbsyv_retail_sold
                grouped_colors[key]['bbglr_retail_sold'] += bbglr_retail_sold
                grouped_colors[key]['bbblg_retail_sold'] += bbblg_retail_sold
                grouped_colors[key]['bbsnr_retail_sold'] += bbsnr_retail_sold
                grouped_colors[key]['bbptg_retail_sold'] += bbptg_retail_sold
                grouped_colors[key]['bbkta_retail_sold'] += bbkta_retail_sold
                grouped_colors[key]['onlne_retail_sold'] += onlne_retail_sold

                grouped_colors[key]['whbb_cost_sold'] += whbb_cost_sold
                grouped_colors[key]['bbflg_cost_sold'] += bbflg_cost_sold
                grouped_colors[key]['bbbbg_cost_sold'] += bbbbg_cost_sold
                grouped_colors[key]['bbbwk_cost_sold'] += bbbwk_cost_sold
                grouped_colors[key]['bbbrw_cost_sold'] += bbbrw_cost_sold
                grouped_colors[key]['bbpdg_cost_sold'] += bbpdg_cost_sold
                grouped_colors[key]['bbsyv_cost_sold'] += bbsyv_cost_sold
                grouped_colors[key]['bbglr_cost_sold'] += bbglr_cost_sold
                grouped_colors[key]['bbblg_cost_sold'] += bbblg_cost_sold
                grouped_colors[key]['bbsnr_cost_sold'] += bbsnr_cost_sold
                grouped_colors[key]['bbptg_cost_sold'] += bbptg_cost_sold
                grouped_colors[key]['bbkta_cost_sold'] += bbkta_cost_sold
                grouped_colors[key]['onlne_cost_sold'] += onlne_cost_sold

                grouped_colors[key]['whbb_qty_stock'] += whbb_qty_stock
                grouped_colors[key]['bbflg_qty_stock'] += bbflg_qty_stock
                grouped_colors[key]['bbbbg_qty_stock'] += bbbbg_qty_stock
                grouped_colors[key]['bbbwk_qty_stock'] += bbbwk_qty_stock
                grouped_colors[key]['bbbrw_qty_stock'] += bbbrw_qty_stock
                grouped_colors[key]['bbpdg_qty_stock'] += bbpdg_qty_stock
                grouped_colors[key]['bbsyv_qty_stock'] += bbsyv_qty_stock
                grouped_colors[key]['bbglr_qty_stock'] += bbglr_qty_stock
                grouped_colors[key]['bbblg_qty_stock'] += bbblg_qty_stock
                grouped_colors[key]['bbsnr_qty_stock'] += bbsnr_qty_stock
                grouped_colors[key]['bbptg_qty_stock'] += bbptg_qty_stock
                grouped_colors[key]['bbkta_qty_stock'] += bbkta_qty_stock
                grouped_colors[key]['onlne_qty_stock'] += onlne_qty_stock

                grouped_colors[key]['whbb_retail_stock'] += whbb_retail_stock
                grouped_colors[key]['bbflg_retail_stock'] += bbflg_retail_stock
                grouped_colors[key]['bbbbg_retail_stock'] += bbbbg_retail_stock
                grouped_colors[key]['bbbwk_retail_stock'] += bbbwk_retail_stock
                grouped_colors[key]['bbbrw_retail_stock'] += bbbrw_retail_stock
                grouped_colors[key]['bbpdg_retail_stock'] += bbpdg_retail_stock
                grouped_colors[key]['bbsyv_retail_stock'] += bbsyv_retail_stock
                grouped_colors[key]['bbglr_retail_stock'] += bbglr_retail_stock
                grouped_colors[key]['bbblg_retail_stock'] += bbblg_retail_stock
                grouped_colors[key]['bbsnr_retail_stock'] += bbsnr_retail_stock
                grouped_colors[key]['bbptg_retail_stock'] += bbptg_retail_stock
                grouped_colors[key]['bbkta_retail_stock'] += bbkta_retail_stock
                grouped_colors[key]['onlne_retail_stock'] += onlne_retail_stock

                grouped_colors[key]['whbb_cost_stock'] += whbb_cost_stock
                grouped_colors[key]['bbflg_cost_stock'] += bbflg_cost_stock
                grouped_colors[key]['bbbbg_cost_stock'] += bbbbg_cost_stock
                grouped_colors[key]['bbbwk_cost_stock'] += bbbwk_cost_stock
                grouped_colors[key]['bbbrw_cost_stock'] += bbbrw_cost_stock
                grouped_colors[key]['bbpdg_cost_stock'] += bbpdg_cost_stock
                grouped_colors[key]['bbsyv_cost_stock'] += bbsyv_cost_stock
                grouped_colors[key]['bbglr_cost_stock'] += bbglr_cost_stock
                grouped_colors[key]['bbblg_cost_stock'] += bbblg_cost_stock
                grouped_colors[key]['bbsnr_cost_stock'] += bbsnr_cost_stock
                grouped_colors[key]['bbptg_cost_stock'] += bbptg_cost_stock
                grouped_colors[key]['bbkta_cost_stock'] += bbkta_cost_stock
                grouped_colors[key]['onlne_cost_stock'] += onlne_cost_stock

        # Print the result
        row = 6
        gt_qty_sold = grandtotal_qty_sold
        gt_retail_sold = grandtotal_retail_sold
        gt_cost_sold = grandtotal_cost_sold

        gt_qty_stock_now = grandtotal_qty_stock_now
        gt_retail_stock_now = grandtotal_retail_stock_now
        gt_cost_stock_now = grandtotal_cost_stock_now

        gt_qty_stock_last = grandtotal_qty_stock_last
        gt_retail_stock_last = grandtotal_retail_stock_last
        gt_cost_stock_last = grandtotal_cost_stock_last

        gt_qty_receiving = grandtotal_qty_received
        gt_retail_receiving = grandtotal_retail_received
        gt_cost_receiving = grandtotal_cost_received

        gt_qty_wh = grandtotal_qty_wh
        gt_retail_wh = grandtotal_retail_wh
        gt_cost_wh = grandtotal_cost_wh

        gt_whbb_qty_sold = grandtotal_whbb_qty_sold
        gt_bbflg_qty_sold = grandtotal_bbflg_qty_sold
        gt_bbbbg_qty_sold = grandtotal_bbbbg_qty_sold
        gt_bbbwk_qty_sold = grandtotal_bbbwk_qty_sold
        gt_bbbrw_qty_sold = grandtotal_bbbrw_qty_sold
        gt_bbpdg_qty_sold = grandtotal_bbpdg_qty_sold
        gt_bbsyv_qty_sold = grandtotal_bbsyv_qty_sold
        gt_bbglr_qty_sold = grandtotal_bbglr_qty_sold
        gt_bbblg_qty_sold = grandtotal_bbblg_qty_sold
        gt_bbsnr_qty_sold = grandtotal_bbsnr_qty_sold
        gt_bbptg_qty_sold = grandtotal_bbptg_qty_sold
        gt_bbkta_qty_sold = grandtotal_bbkta_qty_sold
        gt_onlne_qty_sold = grandtotal_onlne_qty_sold

        gt_whbb_retail_sold = grandtotal_whbb_retail_sold
        gt_bbflg_retail_sold = grandtotal_bbflg_retail_sold
        gt_bbbbg_retail_sold = grandtotal_bbbbg_retail_sold
        gt_bbbwk_retail_sold = grandtotal_bbbwk_retail_sold
        gt_bbbrw_retail_sold = grandtotal_bbbrw_retail_sold
        gt_bbpdg_retail_sold = grandtotal_bbpdg_retail_sold
        gt_bbsyv_retail_sold = grandtotal_bbsyv_retail_sold
        gt_bbglr_retail_sold = grandtotal_bbglr_retail_sold
        gt_bbblg_retail_sold = grandtotal_bbblg_retail_sold
        gt_bbsnr_retail_sold = grandtotal_bbsnr_retail_sold
        gt_bbptg_retail_sold = grandtotal_bbptg_retail_sold
        gt_bbkta_retail_sold = grandtotal_bbkta_retail_sold
        gt_onlne_retail_sold = grandtotal_onlne_retail_sold

        gt_whbb_cost_sold = grandtotal_whbb_cost_sold
        gt_bbflg_cost_sold = grandtotal_bbflg_cost_sold
        gt_bbbbg_cost_sold = grandtotal_bbbbg_cost_sold
        gt_bbbwk_cost_sold = grandtotal_bbbwk_cost_sold
        gt_bbbrw_cost_sold = grandtotal_bbbrw_cost_sold
        gt_bbpdg_cost_sold = grandtotal_bbpdg_cost_sold
        gt_bbsyv_cost_sold = grandtotal_bbsyv_cost_sold
        gt_bbglr_cost_sold = grandtotal_bbglr_cost_sold
        gt_bbblg_cost_sold = grandtotal_bbblg_cost_sold
        gt_bbsnr_cost_sold = grandtotal_bbsnr_cost_sold
        gt_bbptg_cost_sold = grandtotal_bbptg_cost_sold
        gt_bbkta_cost_sold = grandtotal_bbkta_cost_sold
        gt_onlne_cost_sold = grandtotal_onlne_cost_sold

        # gt_whbb_qty_stock = grandtotal_whbb_qty_stock
        gt_bbflg_qty_stock = grandtotal_bbflg_qty_stock
        gt_bbbbg_qty_stock = grandtotal_bbbbg_qty_stock
        gt_bbbwk_qty_stock = grandtotal_bbbwk_qty_stock
        gt_bbbrw_qty_stock = grandtotal_bbbrw_qty_stock
        gt_bbpdg_qty_stock = grandtotal_bbpdg_qty_stock
        gt_bbsyv_qty_stock = grandtotal_bbsyv_qty_stock
        gt_bbglr_qty_stock = grandtotal_bbglr_qty_stock
        gt_bbblg_qty_stock = grandtotal_bbblg_qty_stock
        gt_bbsnr_qty_stock = grandtotal_bbsnr_qty_stock
        gt_bbptg_qty_stock = grandtotal_bbptg_qty_stock
        gt_bbkta_qty_stock = grandtotal_bbkta_qty_stock
        gt_onlne_qty_stock = grandtotal_onlne_qty_stock

        # gt_whbb_retail_stock = grandtotal_whbb_retail_stock
        gt_bbflg_retail_stock = grandtotal_bbflg_retail_stock
        gt_bbbbg_retail_stock = grandtotal_bbbbg_retail_stock
        gt_bbbwk_retail_stock = grandtotal_bbbwk_retail_stock
        gt_bbbrw_retail_stock = grandtotal_bbbrw_retail_stock
        gt_bbpdg_retail_stock = grandtotal_bbpdg_retail_stock
        gt_bbsyv_retail_stock = grandtotal_bbsyv_retail_stock
        gt_bbglr_retail_stock = grandtotal_bbglr_retail_stock
        gt_bbblg_retail_stock = grandtotal_bbblg_retail_stock
        gt_bbsnr_retail_stock = grandtotal_bbsnr_retail_stock
        gt_bbptg_retail_stock = grandtotal_bbptg_retail_stock
        gt_bbkta_retail_stock = grandtotal_bbkta_retail_stock
        gt_onlne_retail_stock = grandtotal_onlne_retail_stock

        # gt_whbb_cost_stock = grandtotal_whbb_cost_stock
        gt_bbflg_cost_stock = grandtotal_bbflg_cost_stock
        gt_bbbbg_cost_stock = grandtotal_bbbbg_cost_stock
        gt_bbbwk_cost_stock = grandtotal_bbbwk_cost_stock
        gt_bbbrw_cost_stock = grandtotal_bbbrw_cost_stock
        gt_bbpdg_cost_stock = grandtotal_bbpdg_cost_stock
        gt_bbsyv_cost_stock = grandtotal_bbsyv_cost_stock
        gt_bbglr_cost_stock = grandtotal_bbglr_cost_stock
        gt_bbblg_cost_stock = grandtotal_bbblg_cost_stock
        gt_bbsnr_cost_stock = grandtotal_bbsnr_cost_stock
        gt_bbptg_cost_stock = grandtotal_bbptg_cost_stock
        gt_bbkta_cost_stock = grandtotal_bbkta_cost_stock
        gt_onlne_cost_stock = grandtotal_onlne_cost_stock

        gt_whbb_qty_stock = gt_qty_wh
        gt_whbb_retail_stock = gt_retail_wh
        gt_whbb_cost_stock = gt_cost_wh

        gt_percent_qty_sold = 0
        gt_percent_retail_sold = 0
        gt_percent_cost_sold = 0
        gt_percent_qty_receiving = 0
        gt_percent_retail_receiving = 0
        gt_percent_cost_receiving = 0
        gt_percent_qty_stock_now = 0
        gt_percent_retail_stock_now = 0
        gt_percent_cost_stock_now = 0
        gt_week_cover_all = 0
        gt_percent_qty_stock_last = 0
        gt_percent_retail_stock_last = 0
        gt_percent_cost_stock_last = 0
        gt_percent_qty_whbb_stock = 0
        gt_percent_retail_whbb_stock = 0
        gt_percent_cost_whbb_stock = 0
        gt_percent_qty_bbflg_sold = 0
        gt_percent_retail_bbflg_sold = 0
        gt_percent_cost_bbflg_sold = 0
        gt_percent_qty_bbflg_stock = 0
        gt_percent_retail_bbflg_stock = 0
        gt_percent_cost_bbflg_stock = 0
        gt_week_cover_bbflg = 0
        gt_percent_qty_bbbrw_sold = 0
        gt_percent_retail_bbbrw_sold = 0
        gt_percent_cost_bbbrw_sold = 0
        gt_percent_qty_bbbrw_stock = 0
        gt_percent_retail_bbbrw_stock = 0
        gt_percent_cost_bbbrw_stock = 0
        gt_week_cover_bbbrw = 0
        gt_percent_qty_bbbwk_sold = 0
        gt_percent_retail_bbbwk_sold = 0
        gt_percent_cost_bbbwk_sold = 0
        gt_percent_qty_bbbwk_stock = 0
        gt_percent_retail_bbbwk_stock = 0
        gt_percent_cost_bbbwk_stock = 0
        gt_week_cover_bbbwk = 0
        gt_percent_qty_bbglr_sold = 0
        gt_percent_retail_bbglr_sold = 0
        gt_percent_cost_bbglr_sold = 0
        gt_percent_qty_bbglr_stock = 0
        gt_percent_retail_bbglr_stock = 0
        gt_percent_cost_bbglr_stock = 0
        gt_week_cover_bbglr = 0
        gt_percent_qty_bbsyv_sold = 0
        gt_percent_retail_bbsyv_sold = 0
        gt_percent_cost_bbsyv_sold = 0
        gt_percent_qty_bbsyv_stock = 0
        gt_percent_retail_bbsyv_stock = 0
        gt_percent_cost_bbsyv_stock = 0
        gt_week_cover_bbsyv = 0
        gt_percent_qty_bbbbg_sold = 0
        gt_percent_retail_bbbbg_sold = 0
        gt_percent_cost_bbbbg_sold = 0
        gt_percent_qty_bbbbg_stock = 0
        gt_percent_retail_bbbbg_stock = 0
        gt_percent_cost_bbbbg_stock = 0
        gt_week_cover_bbbbg = 0
        gt_percent_qty_bbsnr_sold = 0
        gt_percent_retail_bbsnr_sold = 0
        gt_percent_cost_bbsnr_sold = 0
        gt_percent_qty_bbsnr_stock = 0
        gt_percent_retail_bbsnr_stock = 0
        gt_percent_cost_bbsnr_stock = 0
        gt_week_cover_bbsnr = 0
        gt_percent_qty_bbblg_sold = 0
        gt_percent_retail_bbblg_sold = 0
        gt_percent_cost_bbblg_sold = 0
        gt_percent_qty_bbblg_stock = 0
        gt_percent_retail_bbblg_stock = 0
        gt_percent_cost_bbblg_stock = 0
        gt_week_cover_bbblg = 0
        gt_percent_qty_bbpdg_sold = 0
        gt_percent_retail_bbpdg_sold = 0
        gt_percent_cost_bbpdg_sold = 0
        gt_percent_qty_bbpdg_stock = 0
        gt_percent_retail_bbpdg_stock = 0
        gt_percent_cost_bbpdg_stock = 0
        gt_week_cover_bbpdg = 0
        gt_percent_qty_bbkta_sold = 0
        gt_percent_retail_bbkta_sold = 0
        gt_percent_cost_bbkta_sold = 0
        gt_percent_qty_bbkta_stock = 0
        gt_percent_retail_bbkta_stock = 0
        gt_percent_cost_bbkta_stock = 0
        gt_week_cover_bbkta = 0
        gt_percent_qty_bbptg_sold = 0
        gt_percent_retail_bbptg_sold = 0
        gt_percent_cost_bbptg_sold = 0
        gt_percent_qty_bbptg_stock = 0
        gt_percent_retail_bbptg_stock = 0
        gt_percent_cost_bbptg_stock = 0
        gt_week_cover_bbptg = 0
        gt_percent_qty_onlne_sold = 0
        gt_percent_retail_onlne_sold = 0
        gt_percent_cost_onlne_sold = 0
        gt_percent_qty_onlne_stock = 0
        gt_percent_retail_onlne_stock = 0
        gt_percent_cost_onlne_stock = 0
        gt_week_cover_onlne = 0

        dt_percent_qty_sold = 0
        dt_percent_retail_sold = 0
        dt_percent_cost_sold = 0
        dt_percent_qty_receiving = 0
        dt_percent_retail_receiving = 0
        dt_percent_cost_receiving = 0
        dt_percent_qty_stock_now = 0
        dt_percent_retail_stock_now = 0
        dt_percent_cost_stock_now = 0
        dt_week_cover_all = 0
        dt_percent_qty_stock_last = 0
        dt_percent_retail_stock_last = 0
        dt_percent_cost_stock_last = 0
        dt_percent_qty_whbb_stock = 0
        dt_percent_retail_whbb_stock = 0
        dt_percent_cost_whbb_stock = 0
        dt_percent_qty_bbflg_sold = 0
        dt_percent_retail_bbflg_sold = 0
        dt_percent_cost_bbflg_sold = 0
        dt_percent_qty_bbflg_stock = 0
        dt_percent_retail_bbflg_stock = 0
        dt_percent_cost_bbflg_stock = 0
        dt_week_cover_bbflg = 0
        dt_percent_qty_bbbrw_sold = 0
        dt_percent_retail_bbbrw_sold = 0
        dt_percent_cost_bbbrw_sold = 0
        dt_percent_qty_bbbrw_stock = 0
        dt_percent_retail_bbbrw_stock = 0
        dt_percent_cost_bbbrw_stock = 0
        dt_week_cover_bbbrw = 0
        dt_percent_qty_bbbwk_sold = 0
        dt_percent_retail_bbbwk_sold = 0
        dt_percent_cost_bbbwk_sold = 0
        dt_percent_qty_bbbwk_stock = 0
        dt_percent_retail_bbbwk_stock = 0
        dt_percent_cost_bbbwk_stock = 0
        dt_week_cover_bbbwk = 0
        dt_percent_qty_bbglr_sold = 0
        dt_percent_retail_bbglr_sold = 0
        dt_percent_cost_bbglr_sold = 0
        dt_percent_qty_bbglr_stock = 0
        dt_percent_retail_bbglr_stock = 0
        dt_percent_cost_bbglr_stock = 0
        dt_week_cover_bbglr = 0
        dt_percent_qty_bbsyv_sold = 0
        dt_percent_retail_bbsyv_sold = 0
        dt_percent_cost_bbsyv_sold = 0
        dt_percent_qty_bbsyv_stock = 0
        dt_percent_retail_bbsyv_stock = 0
        dt_percent_cost_bbsyv_stock = 0
        dt_week_cover_bbsyv = 0
        dt_percent_qty_bbbbg_sold = 0
        dt_percent_retail_bbbbg_sold = 0
        dt_percent_cost_bbbbg_sold = 0
        dt_percent_qty_bbbbg_stock = 0
        dt_percent_retail_bbbbg_stock = 0
        dt_percent_cost_bbbbg_stock = 0
        dt_week_cover_bbbbg = 0
        dt_percent_qty_bbsnr_sold = 0
        dt_percent_retail_bbsnr_sold = 0
        dt_percent_cost_bbsnr_sold = 0
        dt_percent_qty_bbsnr_stock = 0
        dt_percent_retail_bbsnr_stock = 0
        dt_percent_cost_bbsnr_stock = 0
        dt_week_cover_bbsnr = 0
        dt_percent_qty_bbblg_sold = 0
        dt_percent_retail_bbblg_sold = 0
        dt_percent_cost_bbblg_sold = 0
        dt_percent_qty_bbblg_stock = 0
        dt_percent_retail_bbblg_stock = 0
        dt_percent_cost_bbblg_stock = 0
        dt_week_cover_bbblg = 0
        dt_percent_qty_bbpdg_sold = 0
        dt_percent_retail_bbpdg_sold = 0
        dt_percent_cost_bbpdg_sold = 0
        dt_percent_qty_bbpdg_stock = 0
        dt_percent_retail_bbpdg_stock = 0
        dt_percent_cost_bbpdg_stock = 0
        dt_week_cover_bbpdg = 0
        dt_percent_qty_bbkta_sold = 0
        dt_percent_retail_bbkta_sold = 0
        dt_percent_cost_bbkta_sold = 0
        dt_percent_qty_bbkta_stock = 0
        dt_percent_retail_bbkta_stock = 0
        dt_percent_cost_bbkta_stock = 0
        dt_week_cover_bbkta = 0
        dt_percent_qty_bbptg_sold = 0
        dt_percent_retail_bbptg_sold = 0
        dt_percent_cost_bbptg_sold = 0
        dt_percent_qty_bbptg_stock = 0
        dt_percent_retail_bbptg_stock = 0
        dt_percent_cost_bbptg_stock = 0
        dt_week_cover_bbptg = 0
        dt_percent_qty_onlne_sold = 0
        dt_percent_retail_onlne_sold = 0
        dt_percent_cost_onlne_sold = 0
        dt_percent_qty_onlne_stock = 0
        dt_percent_retail_onlne_stock = 0
        dt_percent_cost_onlne_stock = 0
        dt_week_cover_onlne = 0

        for key, value in grouped_colors.items():

            class_name, parent_category = key
            total_qty_sold, total_retail_sold, total_cost_sold, total_qty_stock_now, total_retail_stock_now, total_cost_stock_now, total_qty_stock_last, total_retail_stock_last, total_cost_stock_last, total_qty_receiving, total_retail_receiving, total_cost_receiving, total_qty_wh, total_retail_wh, total_cost_wh = value['total_qty_sold'], value['total_retail_sold'], value['total_cost_sold'], value['total_qty_stock_now'], value['total_retail_stock_now'], value['total_cost_stock_now'], value['total_qty_stock_last'], value['total_retail_stock_last'], value['total_cost_stock_last'], value['total_qty_receiving'], value['total_retail_receiving'], value['total_cost_receiving'], value['total_qty_wh'], value['total_retail_wh'], value['total_cost_wh']
            
            whbb_qty_sold, bbflg_qty_sold, bbbbg_qty_sold, bbbwk_qty_sold, bbbrw_qty_sold, bbpdg_qty_sold, bbsyv_qty_sold, bbglr_qty_sold, bbblg_qty_sold, bbsnr_qty_sold, bbptg_qty_sold, bbkta_qty_sold, onlne_qty_sold, whbb_qty_stock, bbflg_qty_stock, bbbbg_qty_stock, bbbwk_qty_stock, bbbrw_qty_stock, bbpdg_qty_stock, bbsyv_qty_stock, bbglr_qty_stock, bbblg_qty_stock, bbsnr_qty_stock, bbptg_qty_stock, bbkta_qty_stock, onlne_qty_stock = value['whbb_qty_sold'], value['bbflg_qty_sold'], value['bbbbg_qty_sold'], value['bbbwk_qty_sold'], value['bbbrw_qty_sold'], value['bbpdg_qty_sold'], value['bbsyv_qty_sold'], value['bbglr_qty_sold'], value['bbblg_qty_sold'], value['bbsnr_qty_sold'], value['bbptg_qty_sold'], value['bbkta_qty_sold'], value['onlne_qty_sold'],  value['whbb_qty_stock'], value['bbflg_qty_stock'], value['bbbbg_qty_stock'], value['bbbwk_qty_stock'], value['bbbrw_qty_stock'], value['bbpdg_qty_stock'], value['bbsyv_qty_stock'], value['bbglr_qty_stock'], value['bbblg_qty_stock'], value['bbsnr_qty_stock'], value['bbptg_qty_stock'], value['bbkta_qty_stock'], value['onlne_qty_stock']
            whbb_retail_sold, bbflg_retail_sold, bbbbg_retail_sold, bbbwk_retail_sold, bbbrw_retail_sold, bbpdg_retail_sold, bbsyv_retail_sold, bbglr_retail_sold, bbblg_retail_sold, bbsnr_retail_sold, bbptg_retail_sold, bbkta_retail_sold, onlne_retail_sold, whbb_retail_stock, bbflg_retail_stock, bbbbg_retail_stock, bbbwk_retail_stock, bbbrw_retail_stock, bbpdg_retail_stock, bbsyv_retail_stock, bbglr_retail_stock, bbblg_retail_stock, bbsnr_retail_stock, bbptg_retail_stock, bbkta_retail_stock, onlne_retail_stock = value['whbb_retail_sold'], value['bbflg_retail_sold'], value['bbbbg_retail_sold'], value['bbbwk_retail_sold'], value['bbbrw_retail_sold'], value['bbpdg_retail_sold'], value['bbsyv_retail_sold'], value['bbglr_retail_sold'], value['bbblg_retail_sold'], value['bbsnr_retail_sold'], value['bbptg_retail_sold'], value['bbkta_retail_sold'], value['onlne_retail_sold'],  value['whbb_retail_stock'], value['bbflg_retail_stock'], value['bbbbg_retail_stock'], value['bbbwk_retail_stock'], value['bbbrw_retail_stock'], value['bbpdg_retail_stock'], value['bbsyv_retail_stock'], value['bbglr_retail_stock'], value['bbblg_retail_stock'], value['bbsnr_retail_stock'], value['bbptg_retail_stock'], value['bbkta_retail_stock'], value['onlne_retail_stock']
            whbb_cost_sold, bbflg_cost_sold, bbbbg_cost_sold, bbbwk_cost_sold, bbbrw_cost_sold, bbpdg_cost_sold, bbsyv_cost_sold, bbglr_cost_sold, bbblg_cost_sold, bbsnr_cost_sold, bbptg_cost_sold, bbkta_cost_sold, onlne_cost_sold, whbb_cost_stock, bbflg_cost_stock, bbbbg_cost_stock, bbbwk_cost_stock, bbbrw_cost_stock, bbpdg_cost_stock, bbsyv_cost_stock, bbglr_cost_stock, bbblg_cost_stock, bbsnr_cost_stock, bbptg_cost_stock, bbkta_cost_stock, onlne_cost_stock = value['whbb_cost_sold'], value['bbflg_cost_sold'], value['bbbbg_cost_sold'], value['bbbwk_cost_sold'], value['bbbrw_cost_sold'], value['bbpdg_cost_sold'], value['bbsyv_cost_sold'], value['bbglr_cost_sold'], value['bbblg_cost_sold'], value['bbsnr_cost_sold'], value['bbptg_cost_sold'], value['bbkta_cost_sold'], value['onlne_cost_sold'],  value['whbb_cost_stock'], value['bbflg_cost_stock'], value['bbbbg_cost_stock'], value['bbbwk_cost_stock'], value['bbbrw_cost_stock'], value['bbpdg_cost_stock'], value['bbsyv_cost_stock'], value['bbglr_cost_stock'], value['bbblg_cost_stock'], value['bbsnr_cost_stock'], value['bbptg_cost_stock'], value['bbkta_cost_stock'], value['onlne_cost_stock']
            # qty_sold_total = whbb_qty_sold + bbflg_qty_sold + bbbbg_qty_sold + bbbwk_qty_sold + bbbrw_qty_sold + bbpdg_qty_sold + bbsyv_qty_sold + bbglr_qty_sold + bbblg_qty_sold + bbsnr_qty_sold + bbptg_qty_sold + bbkta_qty_sold + onlne_qty_sold
            # qty_stock_total = whbb_qty_stock + bbflg_qty_stock + bbbbg_qty_stock + bbbwk_qty_stock + bbbrw_qty_stock + bbpdg_qty_stock + bbsyv_qty_stock + bbglr_qty_stock + bbblg_qty_stock + bbsnr_qty_stock + bbptg_qty_stock + bbkta_qty_stock + onlne_qty_stock
            
            dt_class_name = class_name
            dt_parent_category = parent_category
            dt_category = category

            dt_total_qty_sold = total_qty_sold
            dt_total_retail_sold = total_retail_sold
            dt_total_cost_sold = total_cost_sold

            dt_total_qty_stock_now = total_qty_stock_now
            dt_total_retail_stock_now = total_retail_stock_now
            dt_total_cost_stock_now = total_cost_stock_now

            dt_total_qty_stock_last = total_qty_stock_last
            dt_total_retail_stock_last = total_retail_stock_last
            dt_total_cost_stock_last = total_cost_stock_last

            dt_total_qty_receiving = total_qty_receiving
            dt_total_retail_receiving = total_retail_receiving
            dt_total_cost_receiving = total_cost_receiving

            dt_whbb_qty_sold = whbb_qty_sold
            dt_bbflg_qty_sold = bbflg_qty_sold
            dt_bbbbg_qty_sold = bbbbg_qty_sold
            dt_bbbwk_qty_sold = bbbwk_qty_sold
            dt_bbbrw_qty_sold = bbbrw_qty_sold
            dt_bbpdg_qty_sold = bbpdg_qty_sold
            dt_bbsyv_qty_sold = bbsyv_qty_sold
            dt_bbglr_qty_sold = bbglr_qty_sold
            dt_bbblg_qty_sold = bbblg_qty_sold
            dt_bbsnr_qty_sold = bbsnr_qty_sold
            dt_bbptg_qty_sold = bbptg_qty_sold
            dt_bbkta_qty_sold = bbkta_qty_sold
            dt_onlne_qty_sold = onlne_qty_sold

            dt_whbb_retail_sold = whbb_retail_sold
            dt_bbflg_retail_sold = bbflg_retail_sold
            dt_bbbbg_retail_sold = bbbbg_retail_sold
            dt_bbbwk_retail_sold = bbbwk_retail_sold
            dt_bbbrw_retail_sold = bbbrw_retail_sold
            dt_bbpdg_retail_sold = bbpdg_retail_sold
            dt_bbsyv_retail_sold = bbsyv_retail_sold
            dt_bbglr_retail_sold = bbglr_retail_sold
            dt_bbblg_retail_sold = bbblg_retail_sold
            dt_bbsnr_retail_sold = bbsnr_retail_sold
            dt_bbptg_retail_sold = bbptg_retail_sold
            dt_bbkta_retail_sold = bbkta_retail_sold
            dt_onlne_retail_sold = onlne_retail_sold

            dt_whbb_cost_sold = whbb_cost_sold
            dt_bbflg_cost_sold = bbflg_cost_sold
            dt_bbbbg_cost_sold = bbbbg_cost_sold
            dt_bbbwk_cost_sold = bbbwk_cost_sold
            dt_bbbrw_cost_sold = bbbrw_cost_sold
            dt_bbpdg_cost_sold = bbpdg_cost_sold
            dt_bbsyv_cost_sold = bbsyv_cost_sold
            dt_bbglr_cost_sold = bbglr_cost_sold
            dt_bbblg_cost_sold = bbblg_cost_sold
            dt_bbsnr_cost_sold = bbsnr_cost_sold
            dt_bbptg_cost_sold = bbptg_cost_sold
            dt_bbkta_cost_sold = bbkta_cost_sold
            dt_onlne_cost_sold = onlne_cost_sold

            # dt_whbb_qty_stock = whbb_qty_stock
            dt_bbflg_qty_stock = bbflg_qty_stock
            dt_bbbbg_qty_stock = bbbbg_qty_stock
            dt_bbbwk_qty_stock = bbbwk_qty_stock
            dt_bbbrw_qty_stock = bbbrw_qty_stock
            dt_bbpdg_qty_stock = bbpdg_qty_stock
            dt_bbsyv_qty_stock = bbsyv_qty_stock
            dt_bbglr_qty_stock = bbglr_qty_stock
            dt_bbblg_qty_stock = bbblg_qty_stock
            dt_bbsnr_qty_stock = bbsnr_qty_stock
            dt_bbptg_qty_stock = bbptg_qty_stock
            dt_bbkta_qty_stock = bbkta_qty_stock
            dt_onlne_qty_stock = onlne_qty_stock

            # dt_whbb_retail_stock = whbb_retail_stock
            dt_bbflg_retail_stock = bbflg_retail_stock
            dt_bbbbg_retail_stock = bbbbg_retail_stock
            dt_bbbwk_retail_stock = bbbwk_retail_stock
            dt_bbbrw_retail_stock = bbbrw_retail_stock
            dt_bbpdg_retail_stock = bbpdg_retail_stock
            dt_bbsyv_retail_stock = bbsyv_retail_stock
            dt_bbglr_retail_stock = bbglr_retail_stock
            dt_bbblg_retail_stock = bbblg_retail_stock
            dt_bbsnr_retail_stock = bbsnr_retail_stock
            dt_bbptg_retail_stock = bbptg_retail_stock
            dt_bbkta_retail_stock = bbkta_retail_stock
            dt_onlne_retail_stock = onlne_retail_stock

            # dt_whbb_cost_stock = whbb_cost_stock
            dt_bbflg_cost_stock = bbflg_cost_stock
            dt_bbbbg_cost_stock = bbbbg_cost_stock
            dt_bbbwk_cost_stock = bbbwk_cost_stock
            dt_bbbrw_cost_stock = bbbrw_cost_stock
            dt_bbpdg_cost_stock = bbpdg_cost_stock
            dt_bbsyv_cost_stock = bbsyv_cost_stock
            dt_bbglr_cost_stock = bbglr_cost_stock
            dt_bbblg_cost_stock = bbblg_cost_stock
            dt_bbsnr_cost_stock = bbsnr_cost_stock
            dt_bbptg_cost_stock = bbptg_cost_stock
            dt_bbkta_cost_stock = bbkta_cost_stock
            dt_onlne_cost_stock = onlne_cost_stock

            dt_whbb_qty_stock = total_qty_wh
            dt_whbb_retail_stock = total_retail_wh
            dt_whbb_cost_stock = total_cost_wh

            children = value['children']
            for category, categ_value in children.items():
                d_class_name = class_name
                d_parent_category = parent_category
                d_category = category

                d_cost_price = categ_value['cost_price']
                d_retail_price = categ_value['retail_price']

                d_total_qty_sold = categ_value['total_qty_sold']
                d_total_retail_sold = categ_value['total_retail_sold']
                d_total_cost_sold = categ_value['total_cost_sold']

                d_total_qty_stock_now = categ_value['total_qty_stock_now']
                d_total_retail_stock_now = categ_value['total_retail_stock_now']
                d_total_cost_stock_now = categ_value['total_cost_stock_now']

                d_total_qty_stock_last = categ_value['total_qty_stock_last']
                d_total_retail_stock_last = categ_value['total_retail_stock_last']
                d_total_cost_stock_last = categ_value['total_cost_stock_last']

                d_total_qty_receiving = categ_value['total_qty_receiving']
                d_total_retail_receiving = categ_value['total_retail_receiving']
                d_total_cost_receiving = categ_value['total_cost_receiving']

                d_whbb_qty_sold = categ_value['whbb_qty_sold']
                d_bbflg_qty_sold = categ_value['bbflg_qty_sold']
                d_bbbbg_qty_sold = categ_value['bbbbg_qty_sold']
                d_bbbwk_qty_sold = categ_value['bbbwk_qty_sold']
                d_bbbrw_qty_sold = categ_value['bbbrw_qty_sold']
                d_bbpdg_qty_sold = categ_value['bbpdg_qty_sold']
                d_bbsyv_qty_sold = categ_value['bbsyv_qty_sold']
                d_bbglr_qty_sold = categ_value['bbglr_qty_sold']
                d_bbblg_qty_sold = categ_value['bbblg_qty_sold']
                d_bbsnr_qty_sold = categ_value['bbsnr_qty_sold']
                d_bbptg_qty_sold = categ_value['bbptg_qty_sold']
                d_bbkta_qty_sold = categ_value['bbkta_qty_sold']
                d_onlne_qty_sold = categ_value['onlne_qty_sold']

                d_whbb_retail_sold = categ_value['whbb_retail_sold']
                d_bbflg_retail_sold = categ_value['bbflg_retail_sold']
                d_bbbbg_retail_sold = categ_value['bbbbg_retail_sold']
                d_bbbwk_retail_sold = categ_value['bbbwk_retail_sold']
                d_bbbrw_retail_sold = categ_value['bbbrw_retail_sold']
                d_bbpdg_retail_sold = categ_value['bbpdg_retail_sold']
                d_bbsyv_retail_sold = categ_value['bbsyv_retail_sold']
                d_bbglr_retail_sold = categ_value['bbglr_retail_sold']
                d_bbblg_retail_sold = categ_value['bbblg_retail_sold']
                d_bbsnr_retail_sold = categ_value['bbsnr_retail_sold']
                d_bbptg_retail_sold = categ_value['bbptg_retail_sold']
                d_bbkta_retail_sold = categ_value['bbkta_retail_sold']
                d_onlne_retail_sold = categ_value['onlne_retail_sold']

                d_whbb_cost_sold = categ_value['whbb_cost_sold']
                d_bbflg_cost_sold = categ_value['bbflg_cost_sold']
                d_bbbbg_cost_sold = categ_value['bbbbg_cost_sold']
                d_bbbwk_cost_sold = categ_value['bbbwk_cost_sold']
                d_bbbrw_cost_sold = categ_value['bbbrw_cost_sold']
                d_bbpdg_cost_sold = categ_value['bbpdg_cost_sold']
                d_bbsyv_cost_sold = categ_value['bbsyv_cost_sold']
                d_bbglr_cost_sold = categ_value['bbglr_cost_sold']
                d_bbblg_cost_sold = categ_value['bbblg_cost_sold']
                d_bbsnr_cost_sold = categ_value['bbsnr_cost_sold']
                d_bbptg_cost_sold = categ_value['bbptg_cost_sold']
                d_bbkta_cost_sold = categ_value['bbkta_cost_sold']
                d_onlne_cost_sold = categ_value['onlne_cost_sold']

                # d_whbb_qty_stock = categ_value['whbb_qty_stock']
                d_bbflg_qty_stock = categ_value['bbflg_qty_stock']
                d_bbbbg_qty_stock = categ_value['bbbbg_qty_stock']
                d_bbbwk_qty_stock = categ_value['bbbwk_qty_stock']
                d_bbbrw_qty_stock = categ_value['bbbrw_qty_stock']
                d_bbpdg_qty_stock = categ_value['bbpdg_qty_stock']
                d_bbsyv_qty_stock = categ_value['bbsyv_qty_stock']
                d_bbglr_qty_stock = categ_value['bbglr_qty_stock']
                d_bbblg_qty_stock = categ_value['bbblg_qty_stock']
                d_bbsnr_qty_stock = categ_value['bbsnr_qty_stock']
                d_bbptg_qty_stock = categ_value['bbptg_qty_stock']
                d_bbkta_qty_stock = categ_value['bbkta_qty_stock']
                d_onlne_qty_stock = categ_value['onlne_qty_stock']

                # d_whbb_retail_stock = categ_value['whbb_retail_stock']
                d_bbflg_retail_stock = categ_value['bbflg_retail_stock']
                d_bbbbg_retail_stock = categ_value['bbbbg_retail_stock']
                d_bbbwk_retail_stock = categ_value['bbbwk_retail_stock']
                d_bbbrw_retail_stock = categ_value['bbbrw_retail_stock']
                d_bbpdg_retail_stock = categ_value['bbpdg_retail_stock']
                d_bbsyv_retail_stock = categ_value['bbsyv_retail_stock']
                d_bbglr_retail_stock = categ_value['bbglr_retail_stock']
                d_bbblg_retail_stock = categ_value['bbblg_retail_stock']
                d_bbsnr_retail_stock = categ_value['bbsnr_retail_stock']
                d_bbptg_retail_stock = categ_value['bbptg_retail_stock']
                d_bbkta_retail_stock = categ_value['bbkta_retail_stock']
                d_onlne_retail_stock = categ_value['onlne_retail_stock']

                # d_whbb_cost_stock = categ_value['whbb_cost_stock']
                d_bbflg_cost_stock = categ_value['bbflg_cost_stock']
                d_bbbbg_cost_stock = categ_value['bbbbg_cost_stock']
                d_bbbwk_cost_stock = categ_value['bbbwk_cost_stock']
                d_bbbrw_cost_stock = categ_value['bbbrw_cost_stock']
                d_bbpdg_cost_stock = categ_value['bbpdg_cost_stock']
                d_bbsyv_cost_stock = categ_value['bbsyv_cost_stock']
                d_bbglr_cost_stock = categ_value['bbglr_cost_stock']
                d_bbblg_cost_stock = categ_value['bbblg_cost_stock']
                d_bbsnr_cost_stock = categ_value['bbsnr_cost_stock']
                d_bbptg_cost_stock = categ_value['bbptg_cost_stock']
                d_bbkta_cost_stock = categ_value['bbkta_cost_stock']
                d_onlne_cost_stock = categ_value['onlne_cost_stock']

                d_whbb_qty_stock = categ_value['total_qty_wh']
                d_whbb_retail_stock = categ_value['total_retail_wh']
                d_whbb_cost_stock = categ_value['total_cost_wh']

                percent_qty_sold = 0
                if gt_qty_sold != 0:
                    percent_qty_sold = round(d_total_qty_sold/gt_qty_sold, 2)
                percent_retail_sold = 0
                if gt_retail_sold != 0:
                    percent_retail_sold = round(d_total_retail_sold/gt_retail_sold, 2)
                percent_cost_sold = 0
                if gt_cost_sold != 0:
                    percent_cost_sold = round(d_total_cost_sold/gt_cost_sold, 2)


                percent_qty_receiving = 0
                if gt_qty_receiving != 0:
                    percent_qty_receiving = round(d_total_qty_receiving/gt_qty_receiving, 2)
                percent_retail_receiving = 0
                if gt_retail_receiving != 0:
                    percent_retail_receiving = round(d_total_retail_receiving/gt_retail_receiving, 2)
                percent_cost_receiving = 0
                if gt_cost_receiving != 0:
                    percent_cost_receiving = round(d_total_cost_receiving/gt_cost_receiving, 2)

                percent_qty_stock_now = 0
                if gt_qty_stock_now != 0:
                    percent_qty_stock_now = round(d_total_qty_stock_now/gt_qty_stock_now, 2)
                percent_retail_stock_now = 0
                if gt_retail_stock_now != 0:
                    percent_retail_stock_now = round(d_total_retail_stock_now/gt_retail_stock_now, 2)
                percent_cost_stock_now = 0
                if gt_cost_stock_now != 0:
                    percent_cost_stock_now = round(d_total_cost_stock_now/gt_cost_stock_now, 2)

                week_cover_all = 0
                if d_total_qty_sold != 0:
                    week_cover_all = (d_total_qty_stock_now/d_total_qty_sold)*4.5

                percent_qty_stock_last = 0
                if gt_qty_stock_last != 0:
                    percent_qty_stock_last = round(d_total_qty_stock_last/gt_qty_stock_last, 2)
                percent_retail_stock_last = 0
                if gt_retail_stock_last != 0:
                    percent_retail_stock_last = round(d_total_retail_stock_last/gt_retail_stock_last, 2)
                percent_cost_stock_last = 0
                if gt_cost_stock_last != 0:
                    percent_cost_stock_last = round(d_total_cost_stock_last/gt_cost_stock_last, 2)

                percent_qty_whbb_stock = 0
                if gt_whbb_qty_stock != 0:
                    percent_qty_whbb_stock = round(d_whbb_qty_stock/gt_whbb_qty_stock, 2)
                percent_retail_whbb_stock = 0
                if gt_whbb_retail_stock != 0:
                    percent_retail_whbb_stock = round(d_whbb_retail_stock/gt_whbb_retail_stock, 2)
                percent_cost_whbb_stock = 0
                if gt_whbb_cost_stock != 0:
                    percent_cost_whbb_stock = round(d_whbb_cost_stock/gt_whbb_cost_stock, 2)

                percent_qty_bbflg_sold = 0
                if gt_bbflg_qty_sold != 0:
                    percent_qty_bbflg_sold = round(d_bbflg_qty_sold/gt_bbflg_qty_sold, 2)
                percent_retail_bbflg_sold = 0
                if gt_bbflg_retail_sold != 0:
                    percent_retail_bbflg_sold = round(d_bbflg_retail_sold/gt_bbflg_retail_sold, 2)
                percent_cost_bbflg_sold = 0
                if gt_bbflg_cost_sold != 0:
                    percent_cost_bbflg_sold = round(d_bbflg_cost_sold/gt_bbflg_cost_sold, 2)
                percent_qty_bbflg_stock = 0
                if gt_bbflg_qty_stock != 0:
                    percent_qty_bbflg_stock = round(d_bbflg_qty_stock/gt_bbflg_qty_stock, 2)
                percent_retail_bbflg_stock = 0
                if gt_bbflg_retail_stock != 0:
                    percent_retail_bbflg_stock = round(d_bbflg_retail_stock/gt_bbflg_retail_stock, 2)
                percent_cost_bbflg_stock = 0
                if gt_bbflg_cost_stock != 0:
                    percent_cost_bbflg_stock = round(d_bbflg_cost_stock/gt_bbflg_cost_stock, 2)

                week_cover_bbflg = 0
                if d_bbflg_qty_sold != 0:
                    week_cover_bbflg = (d_bbflg_qty_stock/d_bbflg_qty_sold)*4.5

                percent_qty_bbbrw_sold = 0
                if gt_bbbrw_qty_sold != 0:
                    percent_qty_bbbrw_sold = round(d_bbbrw_qty_sold/gt_bbbrw_qty_sold, 2)
                percent_retail_bbbrw_sold = 0
                if gt_bbbrw_retail_sold != 0:
                    percent_retail_bbbrw_sold = round(d_bbbrw_retail_sold/gt_bbbrw_retail_sold, 2)
                percent_cost_bbbrw_sold = 0
                if gt_bbbrw_cost_sold != 0:
                    percent_cost_bbbrw_sold = round(d_bbbrw_cost_sold/gt_bbbrw_cost_sold, 2)
                percent_qty_bbbrw_stock = 0
                if gt_bbbrw_qty_stock != 0:
                    percent_qty_bbbrw_stock = round(d_bbbrw_qty_stock/gt_bbbrw_qty_stock, 2)
                percent_retail_bbbrw_stock = 0
                if gt_bbbrw_retail_stock != 0:
                    percent_retail_bbbrw_stock = round(d_bbbrw_retail_stock/gt_bbbrw_retail_stock, 2)
                percent_cost_bbbrw_stock = 0
                if gt_bbbrw_cost_stock != 0:
                    percent_cost_bbbrw_stock = round(d_bbbrw_cost_stock/gt_bbbrw_cost_stock, 2)
                
                week_cover_bbbrw = 0
                if d_bbbrw_qty_sold != 0:
                    week_cover_bbbrw = (d_bbbrw_qty_stock/d_bbbrw_qty_sold)*4.5

                percent_qty_bbbwk_sold = 0
                if gt_bbbwk_qty_sold != 0:
                    percent_qty_bbbwk_sold = round(d_bbbwk_qty_sold/gt_bbbwk_qty_sold, 2)
                percent_retail_bbbwk_sold = 0
                if gt_bbbwk_retail_sold != 0:
                    percent_retail_bbbwk_sold = round(d_bbbwk_retail_sold/gt_bbbwk_retail_sold, 2)
                percent_cost_bbbwk_sold = 0
                if gt_bbbwk_cost_sold != 0:
                    percent_cost_bbbwk_sold = round(d_bbbwk_cost_sold/gt_bbbwk_cost_sold, 2)
                percent_qty_bbbwk_stock = 0
                if gt_bbbwk_qty_stock != 0:
                    percent_qty_bbbwk_stock = round(d_bbbwk_qty_stock/gt_bbbwk_qty_stock, 2)
                percent_retail_bbbwk_stock = 0
                if gt_bbbwk_retail_stock != 0:
                    percent_retail_bbbwk_stock = round(d_bbbwk_retail_stock/gt_bbbwk_retail_stock, 2)
                percent_cost_bbbwk_stock = 0
                if gt_bbbwk_cost_stock != 0:
                    percent_cost_bbbwk_stock = round(d_bbbwk_cost_stock/gt_bbbwk_cost_stock, 2)

                week_cover_bbbwk = 0
                if d_bbbwk_qty_sold != 0:
                    week_cover_bbbwk = (d_bbbwk_qty_stock/d_bbbwk_qty_sold)*4.5


                percent_qty_bbglr_sold = 0
                if gt_bbglr_qty_sold != 0:
                    percent_qty_bbglr_sold = round(d_bbglr_qty_sold/gt_bbglr_qty_sold, 2)
                percent_retail_bbglr_sold = 0
                if gt_bbglr_retail_sold != 0:
                    percent_retail_bbglr_sold = round(d_bbglr_retail_sold/gt_bbglr_retail_sold, 2)
                percent_cost_bbglr_sold = 0
                if gt_bbglr_cost_sold != 0:
                    percent_cost_bbglr_sold = round(d_bbglr_cost_sold/gt_bbglr_cost_sold, 2)
                percent_qty_bbglr_stock = 0
                if gt_bbglr_qty_stock != 0:
                    percent_qty_bbglr_stock = round(d_bbglr_qty_stock/gt_bbglr_qty_stock, 2)
                percent_retail_bbglr_stock = 0
                if gt_bbglr_retail_stock != 0:
                    percent_retail_bbglr_stock = round(d_bbglr_retail_stock/gt_bbglr_retail_stock, 2)
                percent_cost_bbglr_stock = 0
                if gt_bbglr_cost_stock != 0:
                    percent_cost_bbglr_stock = round(d_bbglr_cost_stock/gt_bbglr_cost_stock, 2)

                week_cover_bbglr = 0
                if d_bbglr_qty_sold != 0:
                    week_cover_bbglr = (d_bbglr_qty_stock/d_bbglr_qty_sold)*4.5

                percent_qty_bbsyv_sold = 0
                if gt_bbsyv_qty_sold != 0:
                    percent_qty_bbsyv_sold = round(d_bbsyv_qty_sold/gt_bbsyv_qty_sold, 2)
                percent_retail_bbsyv_sold = 0
                if gt_bbsyv_retail_sold != 0:
                    percent_retail_bbsyv_sold = round(d_bbsyv_retail_sold/gt_bbsyv_retail_sold, 2)
                percent_cost_bbsyv_sold = 0
                if gt_bbsyv_cost_sold != 0:
                    percent_cost_bbsyv_sold = round(d_bbsyv_cost_sold/gt_bbsyv_cost_sold, 2)
                percent_qty_bbsyv_stock = 0
                if gt_bbsyv_qty_stock != 0:
                    percent_qty_bbsyv_stock = round(d_bbsyv_qty_stock/gt_bbsyv_qty_stock, 2)
                percent_retail_bbsyv_stock = 0
                if gt_bbsyv_retail_stock != 0:
                    percent_retail_bbsyv_stock = round(d_bbsyv_retail_stock/gt_bbsyv_retail_stock, 2)
                percent_cost_bbsyv_stock = 0
                if gt_bbsyv_cost_stock != 0:
                    percent_cost_bbsyv_stock = round(d_bbsyv_cost_stock/gt_bbsyv_cost_stock, 2)

                week_cover_bbsyv = 0
                if d_bbsyv_qty_sold != 0:
                    week_cover_bbsyv = (d_bbsyv_qty_stock/d_bbsyv_qty_sold)*4.5

                percent_qty_bbbbg_sold = 0
                if gt_bbbbg_qty_sold != 0:
                    percent_qty_bbbbg_sold = round(d_bbbbg_qty_sold/gt_bbbbg_qty_sold, 2)
                percent_retail_bbbbg_sold = 0
                if gt_bbbbg_retail_sold != 0:
                    percent_retail_bbbbg_sold = round(d_bbbbg_retail_sold/gt_bbbbg_retail_sold, 2)
                percent_cost_bbbbg_sold = 0
                if gt_bbbbg_cost_sold != 0:
                    percent_cost_bbbbg_sold = round(d_bbbbg_cost_sold/gt_bbbbg_cost_sold, 2)
                percent_qty_bbbbg_stock = 0
                if gt_bbbbg_qty_stock != 0:
                    percent_qty_bbbbg_stock = round(d_bbbbg_qty_stock/gt_bbbbg_qty_stock, 2)
                percent_retail_bbbbg_stock = 0
                if gt_bbbbg_retail_stock != 0:
                    percent_retail_bbbbg_stock = round(d_bbbbg_retail_stock/gt_bbbbg_retail_stock, 2)
                percent_cost_bbbbg_stock = 0
                if gt_bbbbg_cost_stock != 0:
                    percent_cost_bbbbg_stock = round(d_bbbbg_cost_stock/gt_bbbbg_cost_stock, 2)

                week_cover_bbbbg = 0
                if d_bbbbg_qty_sold != 0:
                    week_cover_bbbbg = (d_bbbbg_qty_stock/d_bbbbg_qty_sold)*4.5

                percent_qty_bbsnr_sold = 0
                if gt_bbsnr_qty_sold != 0:
                    percent_qty_bbsnr_sold = round(d_bbsnr_qty_sold/gt_bbsnr_qty_sold, 2)
                percent_retail_bbsnr_sold = 0
                if gt_bbsnr_retail_sold != 0:
                    percent_retail_bbsnr_sold = round(d_bbsnr_retail_sold/gt_bbsnr_retail_sold, 2)
                percent_cost_bbsnr_sold = 0
                if gt_bbsnr_cost_sold != 0:
                    percent_cost_bbsnr_sold = round(d_bbsnr_cost_sold/gt_bbsnr_cost_sold, 2)
                percent_qty_bbsnr_stock = 0
                if gt_bbsnr_qty_stock != 0:
                    percent_qty_bbsnr_stock = round(d_bbsnr_qty_stock/gt_bbsnr_qty_stock, 2)
                percent_retail_bbsnr_stock = 0
                if gt_bbsnr_retail_stock != 0:
                    percent_retail_bbsnr_stock = round(d_bbsnr_retail_stock/gt_bbsnr_retail_stock, 2)
                percent_cost_bbsnr_stock = 0
                if gt_bbsnr_cost_stock != 0:
                    percent_cost_bbsnr_stock = round(d_bbsnr_cost_stock/gt_bbsnr_cost_stock, 2)

                week_cover_bbsnr = 0
                if d_bbsnr_qty_sold != 0:
                    week_cover_bbsnr = (d_bbsnr_qty_stock/d_bbsnr_qty_sold)*4.5


                percent_qty_bbblg_sold = 0
                if gt_bbblg_qty_sold != 0:
                    percent_qty_bbblg_sold = round(d_bbblg_qty_sold/gt_bbblg_qty_sold, 2)
                percent_retail_bbblg_sold = 0
                if gt_bbblg_retail_sold != 0:
                    percent_retail_bbblg_sold = round(d_bbblg_retail_sold/gt_bbblg_retail_sold, 2)
                percent_cost_bbblg_sold = 0
                if gt_bbblg_cost_sold != 0:
                    percent_cost_bbblg_sold = round(d_bbblg_cost_sold/gt_bbblg_cost_sold, 2)
                percent_qty_bbblg_stock = 0
                if gt_bbblg_qty_stock != 0:
                    percent_qty_bbblg_stock = round(d_bbblg_qty_stock/gt_bbblg_qty_stock, 2)
                percent_retail_bbblg_stock = 0
                if gt_bbblg_retail_stock != 0:
                    percent_retail_bbblg_stock = round(d_bbblg_retail_stock/gt_bbblg_retail_stock, 2)
                percent_cost_bbblg_stock = 0
                if gt_bbblg_cost_stock != 0:
                    percent_cost_bbblg_stock = round(d_bbblg_cost_stock/gt_bbblg_cost_stock, 2)

                week_cover_bbblg = 0
                if d_bbblg_qty_sold != 0:
                    week_cover_bbblg = (d_bbblg_qty_stock/d_bbblg_qty_sold)*4.5

                percent_qty_bbpdg_sold = 0
                if gt_bbpdg_qty_sold != 0:
                    percent_qty_bbpdg_sold = round(d_bbpdg_qty_sold/gt_bbpdg_qty_sold, 2)
                percent_retail_bbpdg_sold = 0
                if gt_bbpdg_retail_sold != 0:
                    percent_retail_bbpdg_sold = round(d_bbpdg_retail_sold/gt_bbpdg_retail_sold, 2)
                percent_cost_bbpdg_sold = 0
                if gt_bbpdg_cost_sold != 0:
                    percent_cost_bbpdg_sold = round(d_bbpdg_cost_sold/gt_bbpdg_cost_sold, 2)
                percent_qty_bbpdg_stock = 0
                if gt_bbpdg_qty_stock != 0:
                    percent_qty_bbpdg_stock = round(d_bbpdg_qty_stock/gt_bbpdg_qty_stock, 2)
                percent_retail_bbpdg_stock = 0
                if gt_bbpdg_retail_stock != 0:
                    percent_retail_bbpdg_stock = round(d_bbpdg_retail_stock/gt_bbpdg_retail_stock, 2)
                percent_cost_bbpdg_stock = 0
                if gt_bbpdg_cost_stock != 0:
                    percent_cost_bbpdg_stock = round(d_bbpdg_cost_stock/gt_bbpdg_cost_stock, 2)

                week_cover_bbpdg = 0
                if d_bbpdg_qty_sold != 0:
                    week_cover_bbpdg = (d_bbpdg_qty_stock/d_bbpdg_qty_sold)*4.5


                percent_qty_bbkta_sold = 0
                if gt_bbkta_qty_sold != 0:
                    percent_qty_bbkta_sold = round(d_bbkta_qty_sold/gt_bbkta_qty_sold, 2)
                percent_retail_bbkta_sold = 0
                if gt_bbkta_retail_sold != 0:
                    percent_retail_bbkta_sold = round(d_bbkta_retail_sold/gt_bbkta_retail_sold, 2)
                percent_cost_bbkta_sold = 0
                if gt_bbkta_cost_sold != 0:
                    percent_cost_bbkta_sold = round(d_bbkta_cost_sold/gt_bbkta_cost_sold, 2)
                percent_qty_bbkta_stock = 0
                if gt_bbkta_qty_stock != 0:
                    percent_qty_bbkta_stock = round(d_bbkta_qty_stock/gt_bbkta_qty_stock, 2)
                percent_retail_bbkta_stock = 0
                if gt_bbkta_retail_stock != 0:
                    percent_retail_bbkta_stock = round(d_bbkta_retail_stock/gt_bbkta_retail_stock, 2)
                percent_cost_bbkta_stock = 0
                if gt_bbkta_cost_stock != 0:
                    percent_cost_bbkta_stock = round(d_bbkta_cost_stock/gt_bbkta_cost_stock, 2)

                week_cover_bbkta = 0
                if d_bbkta_qty_sold != 0:
                    week_cover_bbkta = (d_bbkta_qty_stock/d_bbkta_qty_sold)*4.5

                percent_qty_bbptg_sold = 0
                if gt_bbptg_qty_sold != 0:
                    percent_qty_bbptg_sold = round(d_bbptg_qty_sold/gt_bbptg_qty_sold, 2)
                percent_retail_bbptg_sold = 0
                if gt_bbptg_retail_sold != 0:
                    percent_retail_bbptg_sold = round(d_bbptg_retail_sold/gt_bbptg_retail_sold, 2)
                percent_cost_bbptg_sold = 0
                if gt_bbptg_cost_sold != 0:
                    percent_cost_bbptg_sold = round(d_bbptg_cost_sold/gt_bbptg_cost_sold, 2)
                percent_qty_bbptg_stock = 0
                if gt_bbptg_qty_stock != 0:
                    percent_qty_bbptg_stock = round(d_bbptg_qty_stock/gt_bbptg_qty_stock, 2)
                percent_retail_bbptg_stock = 0
                if gt_bbptg_retail_stock != 0:
                    percent_retail_bbptg_stock = round(d_bbptg_retail_stock/gt_bbptg_retail_stock, 2)
                percent_cost_bbptg_stock = 0
                if gt_bbptg_cost_stock != 0:
                    percent_cost_bbptg_stock = round(d_bbptg_cost_stock/gt_bbptg_cost_stock, 2)

                week_cover_bbptg = 0
                if d_bbptg_qty_sold != 0:
                    week_cover_bbptg = (d_bbptg_qty_stock/d_bbptg_qty_sold)*4.5

                percent_qty_onlne_sold = 0
                if gt_onlne_qty_sold != 0:
                    percent_qty_onlne_sold = round(d_onlne_qty_sold/gt_onlne_qty_sold, 2)
                percent_retail_onlne_sold = 0
                if gt_onlne_retail_sold != 0:
                    percent_retail_onlne_sold = round(d_onlne_retail_sold/gt_onlne_retail_sold, 2)
                percent_cost_onlne_sold = 0
                if gt_onlne_cost_sold != 0:
                    percent_cost_onlne_sold = round(d_onlne_cost_sold/gt_onlne_cost_sold, 2)
                percent_qty_onlne_stock = 0
                if gt_onlne_qty_stock != 0:
                    percent_qty_onlne_stock = round(d_onlne_qty_stock/gt_onlne_qty_stock, 2)
                percent_retail_onlne_stock = 0
                if gt_onlne_retail_stock != 0:
                    percent_retail_onlne_stock = round(d_onlne_retail_stock/gt_onlne_retail_stock, 2)
                percent_cost_onlne_stock = 0
                if gt_onlne_cost_stock != 0:
                    percent_cost_onlne_stock = round(d_onlne_cost_stock/gt_onlne_cost_stock, 2)

                week_cover_onlne = 0
                if d_onlne_qty_sold != 0:
                    week_cover_onlne = (d_onlne_qty_stock/d_onlne_qty_sold)*4.5


                worksheet.write('A%s:B%s' %(row, row), d_class_name or '', wbf['content'])
                worksheet.write('B%s:C%s' %(row, row), d_parent_category or '', wbf['content'])
                worksheet.write('C%s:D%s' %(row, row), d_category or '', wbf['content'])

                worksheet.write('D%s:E%s' %(row, row), d_total_qty_sold or 0, wbf['content_float'])
                worksheet.write('E%s:F%s' %(row, row), str(round(percent_qty_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('F%s:G%s' %(row, row), d_total_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('G%s:H%s' %(row, row), str(round(percent_retail_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('H%s:I%s' %(row, row), d_total_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('I%s:J%s' %(row, row), str(round(percent_cost_sold, 2)) + '%' or '', wbf['content_float'])

                worksheet.write('J%s:K%s' %(row, row), d_total_qty_stock_now or 0, wbf['content_float'])
                worksheet.write('K%s:L%s' %(row, row), str(round(percent_qty_stock_now, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('L%s:M%s' %(row, row), d_total_retail_stock_now or 0, wbf['content_float_price'])
                worksheet.write('M%s:N%s' %(row, row), str(round(percent_retail_stock_now, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('N%s:O%s' %(row, row), d_total_cost_stock_now or 0, wbf['content_float_price'])
                worksheet.write('O%s:P%s' %(row, row), str(round(percent_cost_stock_now, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('P%s:Q%s' %(row, row), week_cover_all or 0, wbf['content_float'])

                worksheet.write('Q%s:R%s' %(row, row), d_total_qty_stock_last or 0, wbf['content_float']) 
                worksheet.write('R%s:S%s' %(row, row), str(round(percent_qty_stock_last, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('S%s:T%s' %(row, row), d_total_retail_stock_last or 0, wbf['content_float_price']) 
                worksheet.write('T%s:U%s' %(row, row), str(round(percent_retail_stock_last, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('U%s:V%s' %(row, row), d_total_cost_stock_last or 0, wbf['content_float_price']) 
                worksheet.write('V%s:W%s' %(row, row), str(round(percent_cost_stock_last, 2)) + '%' or '', wbf['content_float'])
              
                worksheet.write('W%s:X%s' %(row, row), d_whbb_qty_stock or 0, wbf['content_float'])
                worksheet.write('X%s:Y%s' %(row, row), str(round(percent_qty_whbb_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('Y%s:Z%s' %(row, row), d_whbb_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('Z%s:AA%s' %(row, row), str(round(percent_retail_whbb_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AA%s:AB%s' %(row, row), d_whbb_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('AB%s:AC%s' %(row, row), str(round(percent_cost_whbb_stock, 2)) + '%' or '', wbf['content_float'])

                # RECEIVING
                worksheet.write('AC%s:AD%s' %(row, row), d_total_qty_receiving or 0, wbf['content_float'])
                worksheet.write('AD%s:AE%s' %(row, row), str(round(percent_qty_receiving, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AE%s:AF%s' %(row, row), d_total_retail_receiving or 0, wbf['content_float_price'])
                worksheet.write('AF%s:AG%s' %(row, row), str(round(percent_retail_receiving, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AG%s:AH%s' %(row, row), d_total_cost_receiving or 0, wbf['content_float_price'])
                worksheet.write('AH%s:AI%s' %(row, row), str(round(percent_cost_receiving, 2)) + '%' or '', wbf['content_float'])

                worksheet.write('AI%s:AJ%s' %(row, row), d_bbflg_qty_sold or 0, wbf['content_float'])
                worksheet.write('AJ%s:AK%s' %(row, row), str(round(percent_qty_bbflg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AK%s:AL%s' %(row, row), d_bbflg_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('AL%s:AM%s' %(row, row), str(round(percent_retail_bbflg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AM%s:AN%s' %(row, row), d_bbflg_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('AN%s:AO%s' %(row, row), str(round(percent_cost_bbflg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AO%s:AP%s' %(row, row), d_bbflg_qty_stock or 0, wbf['content_float'])
                worksheet.write('AP%s:AQ%s' %(row, row), str(round(percent_qty_bbflg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AQ%s:AR%s' %(row, row), d_bbflg_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('AR%s:AS%s' %(row, row), str(round(percent_retail_bbflg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AS%s:AT%s' %(row, row), d_bbflg_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('AT%s:AU%s' %(row, row), str(round(percent_cost_bbflg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AU%s:AV%s' %(row, row), week_cover_bbflg or 0, wbf['content_float'])

                worksheet.write('AV%s:AW%s' %(row, row), d_bbbrw_qty_sold or 0, wbf['content_float'])
                worksheet.write('AW%s:AX%s' %(row, row), str(round(percent_qty_bbbrw_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AX%s:AY%s' %(row, row), d_bbbrw_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('AY%s:AZ%s' %(row, row), str(round(percent_retail_bbbrw_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('AZ%s:BA%s' %(row, row), d_bbbrw_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('BA%s:BB%s' %(row, row), str(round(percent_cost_bbbrw_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BB%s:BC%s' %(row, row), d_bbbrw_qty_stock or 0, wbf['content_float'])
                worksheet.write('BC%s:BD%s' %(row, row), str(round(percent_qty_bbbrw_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BD%s:BE%s' %(row, row), d_bbbrw_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('BE%s:BF%s' %(row, row), str(round(percent_retail_bbbrw_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BF%s:BG%s' %(row, row), d_bbbrw_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('BG%s:BH%s' %(row, row), str(round(percent_cost_bbbrw_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BH%s:BI%s' %(row, row), week_cover_bbbrw or 0, wbf['content_float'])

                worksheet.write('BI%s:BJ%s' %(row, row), d_bbbwk_qty_sold or 0, wbf['content_float'])
                worksheet.write('BJ%s:BK%s' %(row, row), str(round(percent_qty_bbbwk_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BK%s:BL%s' %(row, row), d_bbbwk_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('BL%s:BM%s' %(row, row), str(round(percent_retail_bbbwk_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BM%s:BN%s' %(row, row), d_bbbwk_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('BN%s:BO%s' %(row, row), str(round(percent_cost_bbbwk_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BO%s:BP%s' %(row, row), d_bbbwk_qty_stock or 0, wbf['content_float'])
                worksheet.write('BP%s:BQ%s' %(row, row), str(round(percent_qty_bbbwk_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BQ%s:BR%s' %(row, row), d_bbbwk_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('BR%s:BS%s' %(row, row), str(round(percent_retail_bbbwk_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BS%s:BT%s' %(row, row), d_bbbwk_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('BT%s:BU%s' %(row, row), str(round(percent_cost_bbbwk_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BU%s:BV%s' %(row, row), week_cover_bbbwk or 0, wbf['content_float'])

                worksheet.write('BV%s:BW%s' %(row, row), d_bbglr_qty_sold or 0, wbf['content_float'])
                worksheet.write('BW%s:BX%s' %(row, row), str(round(percent_qty_bbglr_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BX%s:BY%s' %(row, row), d_bbglr_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('BY%s:BZ%s' %(row, row), str(round(percent_retail_bbglr_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('BZ%s:CA%s' %(row, row), d_bbglr_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('CA%s:CB%s' %(row, row), str(round(percent_cost_bbglr_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CB%s:CC%s' %(row, row), d_bbglr_qty_stock or 0, wbf['content_float'])
                worksheet.write('CC%s:CD%s' %(row, row), str(round(percent_qty_bbglr_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CD%s:CE%s' %(row, row), d_bbglr_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('CE%s:CF%s' %(row, row), str(round(percent_retail_bbglr_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CF%s:CG%s' %(row, row), d_bbglr_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('CG%s:CH%s' %(row, row), str(round(percent_cost_bbglr_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CH%s:CI%s' %(row, row), week_cover_bbglr or 0, wbf['content_float'])

                worksheet.write('CI%s:BJ%s' %(row, row), d_bbsyv_qty_sold or 0, wbf['content_float'])
                worksheet.write('CJ%s:CK%s' %(row, row), str(round(percent_qty_bbsyv_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CK%s:CL%s' %(row, row), d_bbsyv_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('CL%s:CM%s' %(row, row), str(round(percent_retail_bbsyv_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CM%s:CN%s' %(row, row), d_bbsyv_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('CN%s:CO%s' %(row, row), str(round(percent_cost_bbsyv_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CO%s:CP%s' %(row, row), d_bbsyv_qty_stock or 0, wbf['content_float'])
                worksheet.write('CP%s:CQ%s' %(row, row), str(round(percent_qty_bbsyv_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CQ%s:CR%s' %(row, row), d_bbsyv_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('CR%s:CS%s' %(row, row), str(round(percent_retail_bbsyv_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CS%s:CT%s' %(row, row), d_bbsyv_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('CT%s:CU%s' %(row, row), str(round(percent_cost_bbsyv_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CU%s:CV%s' %(row, row), week_cover_bbsyv or 0, wbf['content_float'])

                worksheet.write('CV%s:CW%s' %(row, row), d_bbbbg_qty_sold or 0, wbf['content_float'])
                worksheet.write('CW%s:CX%s' %(row, row), str(round(percent_qty_bbbbg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CX%s:CY%s' %(row, row), d_bbbbg_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('CY%s:CZ%s' %(row, row), str(round(percent_retail_bbbbg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('CZ%s:DA%s' %(row, row), d_bbbbg_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('DA%s:DB%s' %(row, row), str(round(percent_cost_bbbbg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DB%s:DC%s' %(row, row), d_bbbbg_qty_stock or 0, wbf['content_float'])
                worksheet.write('DC%s:DD%s' %(row, row), str(round(percent_qty_bbbbg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DD%s:DE%s' %(row, row), d_bbbbg_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('DE%s:DF%s' %(row, row), str(round(percent_retail_bbbbg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DF%s:DG%s' %(row, row), d_bbbbg_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('DG%s:DH%s' %(row, row), str(round(percent_cost_bbbbg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DH%s:DI%s' %(row, row), week_cover_bbbbg or 0, wbf['content_float'])

                worksheet.write('DI%s:DJ%s' %(row, row), d_bbsnr_qty_sold or 0, wbf['content_float'])
                worksheet.write('DJ%s:DK%s' %(row, row), str(round(percent_qty_bbsnr_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DK%s:DL%s' %(row, row), d_bbsnr_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('DL%s:DM%s' %(row, row), str(round(percent_retail_bbsnr_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DM%s:DN%s' %(row, row), d_bbsnr_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('DN%s:DO%s' %(row, row), str(round(percent_cost_bbsnr_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DO%s:DP%s' %(row, row), d_bbsnr_qty_stock or 0, wbf['content_float'])
                worksheet.write('DP%s:DQ%s' %(row, row), str(round(percent_qty_bbsnr_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DQ%s:DR%s' %(row, row), d_bbsnr_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('DR%s:DS%s' %(row, row), str(round(percent_retail_bbsnr_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DS%s:DT%s' %(row, row), d_bbsnr_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('DT%s:DU%s' %(row, row), str(round(percent_cost_bbsnr_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DU%s:DV%s' %(row, row), week_cover_bbsnr or 0, wbf['content_float'])

                worksheet.write('DV%s:DW%s' %(row, row), d_bbblg_qty_sold or 0, wbf['content_float'])
                worksheet.write('DW%s:DX%s' %(row, row), str(round(percent_qty_bbblg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DX%s:DY%s' %(row, row), d_bbblg_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('DY%s:DZ%s' %(row, row), str(round(percent_retail_bbblg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('DZ%s:EA%s' %(row, row), d_bbblg_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('EA%s:EB%s' %(row, row), str(round(percent_cost_bbblg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EB%s:EC%s' %(row, row), d_bbblg_qty_stock or 0, wbf['content_float'])
                worksheet.write('EC%s:ED%s' %(row, row), str(round(percent_qty_bbblg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('ED%s:EE%s' %(row, row), d_bbblg_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('EE%s:EF%s' %(row, row), str(round(percent_retail_bbblg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EF%s:EG%s' %(row, row), d_bbblg_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('EG%s:EH%s' %(row, row), str(round(percent_cost_bbblg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EH%s:EI%s' %(row, row), week_cover_bbblg or 0, wbf['content_float'])

                worksheet.write('EI%s:EJ%s' %(row, row), d_bbpdg_qty_sold or 0, wbf['content_float'])
                worksheet.write('EJ%s:EK%s' %(row, row), str(round(percent_qty_bbpdg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EK%s:EL%s' %(row, row), d_bbpdg_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('EL%s:EM%s' %(row, row), str(round(percent_retail_bbpdg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EM%s:EN%s' %(row, row), d_bbpdg_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('EN%s:EO%s' %(row, row), str(round(percent_cost_bbpdg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EO%s:EP%s' %(row, row), d_bbpdg_qty_stock or 0, wbf['content_float'])
                worksheet.write('EP%s:EQ%s' %(row, row), str(round(percent_qty_bbpdg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EQ%s:ER%s' %(row, row), d_bbpdg_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('ER%s:ES%s' %(row, row), str(round(percent_retail_bbpdg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('ES%s:ET%s' %(row, row), d_bbpdg_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('ET%s:EU%s' %(row, row), str(round(percent_cost_bbpdg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EU%s:EV%s' %(row, row), week_cover_bbpdg or 0, wbf['content_float'])

                worksheet.write('EV%s:EW%s' %(row, row), d_bbkta_qty_sold or 0, wbf['content_float'])
                worksheet.write('EW%s:EX%s' %(row, row), str(round(percent_qty_bbkta_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EX%s:EY%s' %(row, row), d_bbkta_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('EY%s:EZ%s' %(row, row), str(round(percent_retail_bbkta_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('EZ%s:FA%s' %(row, row), d_bbkta_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('FA%s:FB%s' %(row, row), str(round(percent_cost_bbkta_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FB%s:FC%s' %(row, row), d_bbkta_qty_stock or 0, wbf['content_float'])
                worksheet.write('FC%s:FD%s' %(row, row), str(round(percent_qty_bbkta_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FD%s:FE%s' %(row, row), d_bbkta_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('FE%s:FF%s' %(row, row), str(round(percent_retail_bbkta_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FF%s:FG%s' %(row, row), d_bbkta_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('FG%s:FH%s' %(row, row), str(round(percent_cost_bbkta_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FH%s:FI%s' %(row, row), week_cover_bbkta or 0, wbf['content_float'])

                worksheet.write('FI%s:FJ%s' %(row, row), d_bbptg_qty_sold or 0, wbf['content_float'])
                worksheet.write('FJ%s:FK%s' %(row, row), str(round(percent_qty_bbptg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FK%s:FL%s' %(row, row), d_bbptg_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('FL%s:FM%s' %(row, row), str(round(percent_retail_bbptg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FM%s:FN%s' %(row, row), d_bbptg_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('FN%s:FO%s' %(row, row), str(round(percent_cost_bbptg_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FO%s:FP%s' %(row, row), d_bbptg_qty_stock or 0, wbf['content_float'])
                worksheet.write('FP%s:FQ%s' %(row, row), str(round(percent_qty_bbptg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FQ%s:FR%s' %(row, row), d_bbptg_retail_stock or 0, wbf['content_float_price'])
                worksheet.write('FR%s:FS%s' %(row, row), str(round(percent_retail_bbptg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FS%s:FT%s' %(row, row), d_bbptg_cost_stock or 0, wbf['content_float_price'])
                worksheet.write('FT%s:FU%s' %(row, row), str(round(percent_cost_bbptg_stock, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FU%s:FV%s' %(row, row), week_cover_bbptg or 0, wbf['content_float'])

                worksheet.write('FV%s:FW%s' %(row, row), d_onlne_qty_sold or 0, wbf['content_float'])
                worksheet.write('FW%s:FX%s' %(row, row), str(round(percent_qty_onlne_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FX%s:FY%s' %(row, row), d_onlne_retail_sold or 0, wbf['content_float_price'])
                worksheet.write('FY%s:FZ%s' %(row, row), str(round(percent_retail_onlne_sold, 2)) + '%' or '', wbf['content_float'])
                worksheet.write('FZ%s:GA%s' %(row, row), d_onlne_cost_sold or 0, wbf['content_float_price'])
                worksheet.write('GA%s:GB%s' %(row, row), str(round(percent_cost_onlne_sold, 2)) + '%' or '', wbf['content_float'])
                row+=1

                dt_percent_qty_sold += percent_qty_sold
                dt_percent_retail_sold += percent_retail_sold
                dt_percent_cost_sold += percent_cost_sold
                dt_percent_qty_receiving += percent_qty_receiving
                dt_percent_retail_receiving += percent_retail_receiving
                dt_percent_cost_receiving += percent_cost_receiving
                dt_percent_qty_stock_now += percent_qty_stock_now
                dt_percent_retail_stock_now += percent_retail_stock_now
                dt_percent_cost_stock_now += percent_cost_stock_now
                dt_week_cover_all += week_cover_all
                dt_percent_qty_stock_last += percent_qty_stock_last
                dt_percent_retail_stock_last += percent_retail_stock_last
                dt_percent_cost_stock_last += percent_cost_stock_last
                dt_percent_qty_whbb_stock += percent_qty_whbb_stock
                dt_percent_retail_whbb_stock += percent_retail_whbb_stock
                dt_percent_cost_whbb_stock += percent_cost_whbb_stock
                dt_percent_qty_bbflg_sold += percent_qty_bbflg_sold
                dt_percent_retail_bbflg_sold += percent_retail_bbflg_sold
                dt_percent_cost_bbflg_sold += percent_cost_bbflg_sold
                dt_percent_qty_bbflg_stock += percent_qty_bbflg_stock
                dt_percent_retail_bbflg_stock += percent_retail_bbflg_stock
                dt_percent_cost_bbflg_stock += percent_cost_bbflg_stock
                dt_week_cover_bbflg += week_cover_bbflg
                dt_percent_qty_bbbrw_sold += percent_qty_bbbrw_sold
                dt_percent_retail_bbbrw_sold += percent_retail_bbbrw_sold
                dt_percent_cost_bbbrw_sold += percent_cost_bbbrw_sold
                dt_percent_qty_bbbrw_stock += percent_qty_bbbrw_stock
                dt_percent_retail_bbbrw_stock += percent_retail_bbbrw_stock
                dt_percent_cost_bbbrw_stock += percent_cost_bbbrw_stock
                dt_week_cover_bbbrw += week_cover_bbbrw
                dt_percent_qty_bbbwk_sold += percent_qty_bbbwk_sold
                dt_percent_retail_bbbwk_sold += percent_retail_bbbwk_sold
                dt_percent_cost_bbbwk_sold += percent_cost_bbbwk_sold
                dt_percent_qty_bbbwk_stock += percent_qty_bbbwk_stock
                dt_percent_retail_bbbwk_stock += percent_retail_bbbwk_stock
                dt_percent_cost_bbbwk_stock += percent_cost_bbbwk_stock
                dt_week_cover_bbbwk += week_cover_bbbwk
                dt_percent_qty_bbglr_sold += percent_qty_bbglr_sold
                dt_percent_retail_bbglr_sold += percent_retail_bbglr_sold
                dt_percent_cost_bbglr_sold += percent_cost_bbglr_sold
                dt_percent_qty_bbglr_stock += percent_qty_bbglr_stock
                dt_percent_retail_bbglr_stock += percent_retail_bbglr_stock
                dt_percent_cost_bbglr_stock += percent_cost_bbglr_stock
                dt_week_cover_bbglr += week_cover_bbglr
                dt_percent_qty_bbsyv_sold += percent_qty_bbsyv_sold
                dt_percent_retail_bbsyv_sold += percent_retail_bbsyv_sold
                dt_percent_cost_bbsyv_sold += percent_cost_bbsyv_sold
                dt_percent_qty_bbsyv_stock += percent_qty_bbsyv_stock
                dt_percent_retail_bbsyv_stock += percent_retail_bbsyv_stock
                dt_percent_cost_bbsyv_stock += percent_cost_bbsyv_stock
                dt_week_cover_bbsyv += week_cover_bbsyv
                dt_percent_qty_bbbbg_sold += percent_qty_bbbbg_sold
                dt_percent_retail_bbbbg_sold += percent_retail_bbbbg_sold
                dt_percent_cost_bbbbg_sold += percent_cost_bbbbg_sold
                dt_percent_qty_bbbbg_stock += percent_qty_bbbbg_stock
                dt_percent_retail_bbbbg_stock += percent_retail_bbbbg_stock
                dt_percent_cost_bbbbg_stock += percent_cost_bbbbg_stock
                dt_week_cover_bbbbg += week_cover_bbbbg
                dt_percent_qty_bbsnr_sold += percent_qty_bbsnr_sold
                dt_percent_retail_bbsnr_sold += percent_retail_bbsnr_sold
                dt_percent_cost_bbsnr_sold += percent_cost_bbsnr_sold
                dt_percent_qty_bbsnr_stock += percent_qty_bbsnr_stock
                dt_percent_retail_bbsnr_stock += percent_retail_bbsnr_stock
                dt_percent_cost_bbsnr_stock += percent_cost_bbsnr_stock
                dt_week_cover_bbsnr += week_cover_bbsnr
                dt_percent_qty_bbblg_sold += percent_qty_bbblg_sold
                dt_percent_retail_bbblg_sold += percent_retail_bbblg_sold
                dt_percent_cost_bbblg_sold += percent_cost_bbblg_sold
                dt_percent_qty_bbblg_stock += percent_qty_bbblg_stock
                dt_percent_retail_bbblg_stock += percent_retail_bbblg_stock
                dt_percent_cost_bbblg_stock += percent_cost_bbblg_stock
                dt_week_cover_bbblg += week_cover_bbblg
                dt_percent_qty_bbpdg_sold += percent_qty_bbpdg_sold
                dt_percent_retail_bbpdg_sold += percent_retail_bbpdg_sold
                dt_percent_cost_bbpdg_sold += percent_cost_bbpdg_sold
                dt_percent_qty_bbpdg_stock += percent_qty_bbpdg_stock
                dt_percent_retail_bbpdg_stock += percent_retail_bbpdg_stock
                dt_percent_cost_bbpdg_stock += percent_cost_bbpdg_stock
                dt_week_cover_bbpdg += week_cover_bbpdg
                dt_percent_qty_bbkta_sold += percent_qty_bbkta_sold
                dt_percent_retail_bbkta_sold += percent_retail_bbkta_sold
                dt_percent_cost_bbkta_sold += percent_cost_bbkta_sold
                dt_percent_qty_bbkta_stock += percent_qty_bbkta_stock
                dt_percent_retail_bbkta_stock += percent_retail_bbkta_stock
                dt_percent_cost_bbkta_stock += percent_cost_bbkta_stock
                dt_week_cover_bbkta += week_cover_bbkta
                dt_percent_qty_bbptg_sold += percent_qty_bbptg_sold
                dt_percent_retail_bbptg_sold += percent_retail_bbptg_sold
                dt_percent_cost_bbptg_sold += percent_cost_bbptg_sold
                dt_percent_qty_bbptg_stock += percent_qty_bbptg_stock
                dt_percent_retail_bbptg_stock += percent_retail_bbptg_stock
                dt_percent_cost_bbptg_stock += percent_cost_bbptg_stock
                dt_week_cover_bbptg += week_cover_bbptg
                dt_percent_qty_onlne_sold += percent_qty_onlne_sold
                dt_percent_retail_onlne_sold += percent_retail_onlne_sold
                dt_percent_cost_onlne_sold += percent_cost_onlne_sold
                dt_percent_qty_onlne_stock += percent_qty_onlne_stock
                dt_percent_retail_onlne_stock += percent_retail_onlne_stock
                dt_percent_cost_onlne_stock += percent_cost_onlne_stock
                dt_week_cover_onlne += week_cover_onlne


            worksheet.write('A%s:B%s' %(row, row), dt_class_name or '', wbf['total_content'])
            worksheet.write('B%s:C%s' %(row, row), dt_parent_category or '', wbf['total_content'])
            worksheet.write('C%s:D%s' %(row, row), '', wbf['total_content'])

            worksheet.write('D%s:E%s' %(row, row), dt_total_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('E%s:F%s' %(row, row), str(round(dt_percent_qty_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('F%s:G%s' %(row, row), dt_total_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('G%s:H%s' %(row, row), str(round(dt_percent_retail_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('H%s:I%s' %(row, row), dt_total_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('I%s:J%s' %(row, row), str(round(dt_percent_cost_sold, 2)) + '%' or '', wbf['total_content_float'])

            worksheet.write('J%s:K%s' %(row, row), dt_total_qty_stock_now or 0, wbf['total_content_float'])
            worksheet.write('K%s:L%s' %(row, row), str(round(dt_percent_qty_stock_now, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('L%s:M%s' %(row, row), dt_total_retail_stock_now or 0, wbf['total_content_float_price'])
            worksheet.write('M%s:N%s' %(row, row), str(round(dt_percent_retail_stock_now, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('N%s:O%s' %(row, row), dt_total_cost_stock_now or 0, wbf['total_content_float_price'])
            worksheet.write('O%s:P%s' %(row, row), str(round(dt_percent_cost_stock_now, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('P%s:Q%s' %(row, row), dt_week_cover_all or 0, wbf['total_content_float'])

            worksheet.write('Q%s:R%s' %(row, row), dt_total_qty_stock_last or 0, wbf['total_content_float']) 
            worksheet.write('R%s:S%s' %(row, row), str(round(dt_percent_qty_stock_last, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('S%s:T%s' %(row, row), dt_total_retail_stock_last or 0, wbf['total_content_float_price']) 
            worksheet.write('T%s:U%s' %(row, row), str(round(dt_percent_retail_stock_last, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('U%s:V%s' %(row, row), dt_total_cost_stock_last or 0, wbf['total_content_float_price']) 
            worksheet.write('V%s:W%s' %(row, row), str(round(dt_percent_cost_stock_last, 2)) + '%' or '', wbf['total_content_float'])
          
            worksheet.write('W%s:X%s' %(row, row), dt_whbb_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('X%s:Y%s' %(row, row), str(round(dt_percent_qty_whbb_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('Y%s:Z%s' %(row, row), dt_whbb_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('Z%s:AA%s' %(row, row), str(round(dt_percent_retail_whbb_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AA%s:AB%s' %(row, row), dt_whbb_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('AB%s:AC%s' %(row, row), str(round(dt_percent_cost_whbb_stock, 2)) + '%' or '', wbf['total_content_float'])

            # RECEIVING
            worksheet.write('AC%s:AD%s' %(row, row), dt_total_qty_receiving or 0, wbf['total_content_float'])
            worksheet.write('AD%s:AE%s' %(row, row), str(round(dt_percent_qty_receiving, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AE%s:AF%s' %(row, row), dt_total_retail_receiving or 0, wbf['total_content_float_price'])
            worksheet.write('AF%s:AG%s' %(row, row), str(round(dt_percent_retail_receiving, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AG%s:AH%s' %(row, row), dt_total_cost_receiving or 0, wbf['total_content_float_price'])
            worksheet.write('AH%s:AI%s' %(row, row), str(round(dt_percent_cost_receiving, 2)) + '%' or '', wbf['total_content_float'])

            worksheet.write('AI%s:AJ%s' %(row, row), dt_bbflg_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('AJ%s:AK%s' %(row, row), str(round(dt_percent_qty_bbflg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AK%s:AL%s' %(row, row), dt_bbflg_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('AL%s:AM%s' %(row, row), str(round(dt_percent_retail_bbflg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AM%s:AN%s' %(row, row), dt_bbflg_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('AN%s:AO%s' %(row, row), str(round(dt_percent_cost_bbflg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AO%s:AP%s' %(row, row), dt_bbflg_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('AP%s:AQ%s' %(row, row), str(round(dt_percent_qty_bbflg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AQ%s:AR%s' %(row, row), dt_bbflg_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('AR%s:AS%s' %(row, row), str(round(dt_percent_retail_bbflg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AS%s:AT%s' %(row, row), dt_bbflg_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('AT%s:AU%s' %(row, row), str(round(dt_percent_cost_bbflg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AU%s:AV%s' %(row, row), dt_week_cover_bbflg or 0, wbf['total_content_float'])

            worksheet.write('AV%s:AW%s' %(row, row), dt_bbbrw_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('AW%s:AX%s' %(row, row), str(round(dt_percent_qty_bbbrw_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AX%s:AY%s' %(row, row), dt_bbbrw_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('AY%s:AZ%s' %(row, row), str(round(dt_percent_retail_bbbrw_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('AZ%s:BA%s' %(row, row), dt_bbbrw_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('BA%s:BB%s' %(row, row), str(round(dt_percent_cost_bbbrw_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BB%s:BC%s' %(row, row), dt_bbbrw_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('BC%s:BD%s' %(row, row), str(round(dt_percent_qty_bbbrw_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BD%s:BE%s' %(row, row), dt_bbbrw_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('BE%s:BF%s' %(row, row), str(round(dt_percent_retail_bbbrw_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BF%s:BG%s' %(row, row), dt_bbbrw_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('BG%s:BH%s' %(row, row), str(round(dt_percent_cost_bbbrw_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BH%s:BI%s' %(row, row), dt_week_cover_bbbrw or 0, wbf['total_content_float'])

            worksheet.write('BI%s:BJ%s' %(row, row), dt_bbbwk_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('BJ%s:BK%s' %(row, row), str(round(dt_percent_qty_bbbwk_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BK%s:BL%s' %(row, row), dt_bbbwk_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('BL%s:BM%s' %(row, row), str(round(dt_percent_retail_bbbwk_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BM%s:BN%s' %(row, row), dt_bbbwk_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('BN%s:BO%s' %(row, row), str(round(dt_percent_cost_bbbwk_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BO%s:BP%s' %(row, row), dt_bbbwk_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('BP%s:BQ%s' %(row, row), str(round(dt_percent_qty_bbbwk_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BQ%s:BR%s' %(row, row), dt_bbbwk_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('BR%s:BS%s' %(row, row), str(round(dt_percent_retail_bbbwk_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BS%s:BT%s' %(row, row), dt_bbbwk_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('BT%s:BU%s' %(row, row), str(round(dt_percent_cost_bbbwk_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BU%s:BV%s' %(row, row), dt_week_cover_bbbwk or 0, wbf['total_content_float'])

            worksheet.write('BV%s:BW%s' %(row, row), dt_bbglr_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('BW%s:BX%s' %(row, row), str(round(dt_percent_qty_bbglr_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BX%s:BY%s' %(row, row), dt_bbglr_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('BY%s:BZ%s' %(row, row), str(round(dt_percent_retail_bbglr_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('BZ%s:CA%s' %(row, row), dt_bbglr_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('CA%s:CB%s' %(row, row), str(round(dt_percent_cost_bbglr_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CB%s:CC%s' %(row, row), dt_bbglr_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('CC%s:CD%s' %(row, row), str(round(dt_percent_qty_bbglr_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CD%s:CE%s' %(row, row), dt_bbglr_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('CE%s:CF%s' %(row, row), str(round(dt_percent_retail_bbglr_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CF%s:CG%s' %(row, row), dt_bbglr_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('CG%s:CH%s' %(row, row), str(round(dt_percent_cost_bbglr_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CH%s:CI%s' %(row, row), dt_week_cover_bbglr or 0, wbf['total_content_float'])

            worksheet.write('CI%s:BJ%s' %(row, row), dt_bbsyv_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('CJ%s:CK%s' %(row, row), str(round(dt_percent_qty_bbsyv_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CK%s:CL%s' %(row, row), dt_bbsyv_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('CL%s:CM%s' %(row, row), str(round(dt_percent_retail_bbsyv_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CM%s:CN%s' %(row, row), dt_bbsyv_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('CN%s:CO%s' %(row, row), str(round(dt_percent_cost_bbsyv_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CO%s:CP%s' %(row, row), dt_bbsyv_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('CP%s:CQ%s' %(row, row), str(round(dt_percent_qty_bbsyv_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CQ%s:CR%s' %(row, row), dt_bbsyv_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('CR%s:CS%s' %(row, row), str(round(dt_percent_retail_bbsyv_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CS%s:CT%s' %(row, row), dt_bbsyv_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('CT%s:CU%s' %(row, row), str(round(dt_percent_cost_bbsyv_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CU%s:CV%s' %(row, row), dt_week_cover_bbsyv or 0, wbf['total_content_float'])

            worksheet.write('CV%s:CW%s' %(row, row), dt_bbbbg_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('CW%s:CX%s' %(row, row), str(round(dt_percent_qty_bbbbg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CX%s:CY%s' %(row, row), dt_bbbbg_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('CY%s:CZ%s' %(row, row), str(round(dt_percent_retail_bbbbg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('CZ%s:DA%s' %(row, row), dt_bbbbg_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('DA%s:DB%s' %(row, row), str(round(dt_percent_cost_bbbbg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DB%s:DC%s' %(row, row), dt_bbbbg_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('DC%s:DD%s' %(row, row), str(round(dt_percent_qty_bbbbg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DD%s:DE%s' %(row, row), dt_bbbbg_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('DE%s:DF%s' %(row, row), str(round(dt_percent_retail_bbbbg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DF%s:DG%s' %(row, row), dt_bbbbg_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('DG%s:DH%s' %(row, row), str(round(dt_percent_cost_bbbbg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DH%s:DI%s' %(row, row), dt_week_cover_bbbbg or 0, wbf['total_content_float'])

            worksheet.write('DI%s:DJ%s' %(row, row), dt_bbsnr_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('DJ%s:DK%s' %(row, row), str(round(dt_percent_qty_bbsnr_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DK%s:DL%s' %(row, row), dt_bbsnr_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('DL%s:DM%s' %(row, row), str(round(dt_percent_retail_bbsnr_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DM%s:DN%s' %(row, row), dt_bbsnr_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('DN%s:DO%s' %(row, row), str(round(dt_percent_cost_bbsnr_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DO%s:DP%s' %(row, row), dt_bbsnr_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('DP%s:DQ%s' %(row, row), str(round(dt_percent_qty_bbsnr_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DQ%s:DR%s' %(row, row), dt_bbsnr_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('DR%s:DS%s' %(row, row), str(round(dt_percent_retail_bbsnr_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DS%s:DT%s' %(row, row), dt_bbsnr_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('DT%s:DU%s' %(row, row), str(round(dt_percent_cost_bbsnr_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DU%s:DV%s' %(row, row), dt_week_cover_bbsnr or 0, wbf['total_content_float'])

            worksheet.write('DV%s:DW%s' %(row, row), dt_bbblg_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('DW%s:DX%s' %(row, row), str(round(dt_percent_qty_bbblg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DX%s:DY%s' %(row, row), dt_bbblg_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('DY%s:DZ%s' %(row, row), str(round(dt_percent_retail_bbblg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('DZ%s:EA%s' %(row, row), dt_bbblg_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('EA%s:EB%s' %(row, row), str(round(dt_percent_cost_bbblg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EB%s:EC%s' %(row, row), dt_bbblg_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('EC%s:ED%s' %(row, row), str(round(dt_percent_qty_bbblg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('ED%s:EE%s' %(row, row), dt_bbblg_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('EE%s:EF%s' %(row, row), str(round(dt_percent_retail_bbblg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EF%s:EG%s' %(row, row), dt_bbblg_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('EG%s:EH%s' %(row, row), str(round(dt_percent_cost_bbblg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EH%s:EI%s' %(row, row), dt_week_cover_bbblg or 0, wbf['total_content_float'])

            worksheet.write('EI%s:EJ%s' %(row, row), dt_bbpdg_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('EJ%s:EK%s' %(row, row), str(round(dt_percent_qty_bbpdg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EK%s:EL%s' %(row, row), dt_bbpdg_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('EL%s:EM%s' %(row, row), str(round(dt_percent_retail_bbpdg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EM%s:EN%s' %(row, row), dt_bbpdg_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('EN%s:EO%s' %(row, row), str(round(dt_percent_cost_bbpdg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EO%s:EP%s' %(row, row), dt_bbpdg_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('EP%s:EQ%s' %(row, row), str(round(dt_percent_qty_bbpdg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EQ%s:ER%s' %(row, row), dt_bbpdg_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('ER%s:ES%s' %(row, row), str(round(dt_percent_retail_bbpdg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('ES%s:ET%s' %(row, row), dt_bbpdg_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('ET%s:EU%s' %(row, row), str(round(dt_percent_cost_bbpdg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EU%s:EV%s' %(row, row), dt_week_cover_bbpdg or 0, wbf['total_content_float'])

            worksheet.write('EV%s:EW%s' %(row, row), dt_bbkta_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('EW%s:EX%s' %(row, row), str(round(dt_percent_qty_bbkta_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EX%s:EY%s' %(row, row), dt_bbkta_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('EY%s:EZ%s' %(row, row), str(round(dt_percent_retail_bbkta_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('EZ%s:FA%s' %(row, row), dt_bbkta_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('FA%s:FB%s' %(row, row), str(round(dt_percent_cost_bbkta_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FB%s:FC%s' %(row, row), dt_bbkta_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('FC%s:FD%s' %(row, row), str(round(dt_percent_qty_bbkta_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FD%s:FE%s' %(row, row), dt_bbkta_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('FE%s:FF%s' %(row, row), str(round(dt_percent_retail_bbkta_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FF%s:FG%s' %(row, row), dt_bbkta_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('FG%s:FH%s' %(row, row), str(round(dt_percent_cost_bbkta_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FH%s:FI%s' %(row, row), dt_week_cover_bbkta or 0, wbf['total_content_float'])

            worksheet.write('FI%s:FJ%s' %(row, row), dt_bbptg_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('FJ%s:FK%s' %(row, row), str(round(dt_percent_qty_bbptg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FK%s:FL%s' %(row, row), dt_bbptg_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('FL%s:FM%s' %(row, row), str(round(dt_percent_retail_bbptg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FM%s:FN%s' %(row, row), dt_bbptg_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('FN%s:FO%s' %(row, row), str(round(dt_percent_cost_bbptg_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FO%s:FP%s' %(row, row), dt_bbptg_qty_stock or 0, wbf['total_content_float'])
            worksheet.write('FP%s:FQ%s' %(row, row), str(round(dt_percent_qty_bbptg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FQ%s:FR%s' %(row, row), dt_bbptg_retail_stock or 0, wbf['total_content_float_price'])
            worksheet.write('FR%s:FS%s' %(row, row), str(round(dt_percent_retail_bbptg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FS%s:FT%s' %(row, row), dt_bbptg_cost_stock or 0, wbf['total_content_float_price'])
            worksheet.write('FT%s:FU%s' %(row, row), str(round(dt_percent_cost_bbptg_stock, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FU%s:FV%s' %(row, row), dt_week_cover_bbptg or 0, wbf['total_content_float'])

            worksheet.write('FV%s:FW%s' %(row, row), dt_onlne_qty_sold or 0, wbf['total_content_float'])
            worksheet.write('FW%s:FX%s' %(row, row), str(round(dt_percent_qty_onlne_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FX%s:FY%s' %(row, row), dt_onlne_retail_sold or 0, wbf['total_content_float_price'])
            worksheet.write('FY%s:FZ%s' %(row, row), str(round(dt_percent_retail_onlne_sold, 2)) + '%' or '', wbf['total_content_float'])
            worksheet.write('FZ%s:FA%s' %(row, row), dt_onlne_cost_sold or 0, wbf['total_content_float_price'])
            worksheet.write('GA%s:GB%s' %(row, row), str(round(dt_percent_cost_onlne_sold, 2)) + '%' or '', wbf['total_content_float'])
            row+=1

            gt_percent_qty_sold += dt_percent_qty_sold
            gt_percent_retail_sold += dt_percent_retail_sold
            gt_percent_cost_sold += dt_percent_cost_sold
            gt_percent_qty_receiving += dt_percent_qty_receiving
            gt_percent_retail_receiving += dt_percent_retail_receiving
            gt_percent_cost_receiving += dt_percent_cost_receiving
            gt_percent_qty_stock_now += dt_percent_qty_stock_now
            gt_percent_retail_stock_now += dt_percent_retail_stock_now
            gt_percent_cost_stock_now += dt_percent_cost_stock_now
            gt_week_cover_all += dt_week_cover_all
            gt_percent_qty_stock_last += dt_percent_qty_stock_last
            gt_percent_retail_stock_last += dt_percent_retail_stock_last
            gt_percent_cost_stock_last += dt_percent_cost_stock_last
            gt_percent_qty_whbb_stock += dt_percent_qty_whbb_stock
            gt_percent_retail_whbb_stock += dt_percent_retail_whbb_stock
            gt_percent_cost_whbb_stock += dt_percent_cost_whbb_stock
            gt_percent_qty_bbflg_sold += dt_percent_qty_bbflg_sold
            gt_percent_retail_bbflg_sold += dt_percent_retail_bbflg_sold
            gt_percent_cost_bbflg_sold += dt_percent_cost_bbflg_sold
            gt_percent_qty_bbflg_stock += dt_percent_qty_bbflg_stock
            gt_percent_retail_bbflg_stock += dt_percent_retail_bbflg_stock
            gt_percent_cost_bbflg_stock += dt_percent_cost_bbflg_stock
            gt_week_cover_bbflg += dt_week_cover_bbflg
            gt_percent_qty_bbbrw_sold += dt_percent_qty_bbbrw_sold
            gt_percent_retail_bbbrw_sold += dt_percent_retail_bbbrw_sold
            gt_percent_cost_bbbrw_sold += dt_percent_cost_bbbrw_sold
            gt_percent_qty_bbbrw_stock += dt_percent_qty_bbbrw_stock
            gt_percent_retail_bbbrw_stock += dt_percent_retail_bbbrw_stock
            gt_percent_cost_bbbrw_stock += dt_percent_cost_bbbrw_stock
            gt_week_cover_bbbrw += dt_week_cover_bbbrw
            gt_percent_qty_bbbwk_sold += dt_percent_qty_bbbwk_sold
            gt_percent_retail_bbbwk_sold += dt_percent_retail_bbbwk_sold
            gt_percent_cost_bbbwk_sold += dt_percent_cost_bbbwk_sold
            gt_percent_qty_bbbwk_stock += dt_percent_qty_bbbwk_stock
            gt_percent_retail_bbbwk_stock += dt_percent_retail_bbbwk_stock
            gt_percent_cost_bbbwk_stock += dt_percent_cost_bbbwk_stock
            gt_week_cover_bbbwk += dt_week_cover_bbbwk
            gt_percent_qty_bbglr_sold += dt_percent_qty_bbglr_sold
            gt_percent_retail_bbglr_sold += dt_percent_retail_bbglr_sold
            gt_percent_cost_bbglr_sold += dt_percent_cost_bbglr_sold
            gt_percent_qty_bbglr_stock += dt_percent_qty_bbglr_stock
            gt_percent_retail_bbglr_stock += dt_percent_retail_bbglr_stock
            gt_percent_cost_bbglr_stock += dt_percent_cost_bbglr_stock
            gt_week_cover_bbglr += dt_week_cover_bbglr
            gt_percent_qty_bbsyv_sold += dt_percent_qty_bbsyv_sold
            gt_percent_retail_bbsyv_sold += dt_percent_retail_bbsyv_sold
            gt_percent_cost_bbsyv_sold += dt_percent_cost_bbsyv_sold
            gt_percent_qty_bbsyv_stock += dt_percent_qty_bbsyv_stock
            gt_percent_retail_bbsyv_stock += dt_percent_retail_bbsyv_stock
            gt_percent_cost_bbsyv_stock += dt_percent_cost_bbsyv_stock
            gt_week_cover_bbsyv += dt_week_cover_bbsyv
            gt_percent_qty_bbbbg_sold += dt_percent_qty_bbbbg_sold
            gt_percent_retail_bbbbg_sold += dt_percent_retail_bbbbg_sold
            gt_percent_cost_bbbbg_sold += dt_percent_cost_bbbbg_sold
            gt_percent_qty_bbbbg_stock += dt_percent_qty_bbbbg_stock
            gt_percent_retail_bbbbg_stock += dt_percent_retail_bbbbg_stock
            gt_percent_cost_bbbbg_stock += dt_percent_cost_bbbbg_stock
            gt_week_cover_bbbbg += dt_week_cover_bbbbg
            gt_percent_qty_bbsnr_sold += dt_percent_qty_bbsnr_sold
            gt_percent_retail_bbsnr_sold += dt_percent_retail_bbsnr_sold
            gt_percent_cost_bbsnr_sold += dt_percent_cost_bbsnr_sold
            gt_percent_qty_bbsnr_stock += dt_percent_qty_bbsnr_stock
            gt_percent_retail_bbsnr_stock += dt_percent_retail_bbsnr_stock
            gt_percent_cost_bbsnr_stock += dt_percent_cost_bbsnr_stock
            gt_week_cover_bbsnr += dt_week_cover_bbsnr
            gt_percent_qty_bbblg_sold += dt_percent_qty_bbblg_sold
            gt_percent_retail_bbblg_sold += dt_percent_retail_bbblg_sold
            gt_percent_cost_bbblg_sold += dt_percent_cost_bbblg_sold
            gt_percent_qty_bbblg_stock += dt_percent_qty_bbblg_stock
            gt_percent_retail_bbblg_stock += dt_percent_retail_bbblg_stock
            gt_percent_cost_bbblg_stock += dt_percent_cost_bbblg_stock
            gt_week_cover_bbblg += dt_week_cover_bbblg
            gt_percent_qty_bbpdg_sold += dt_percent_qty_bbpdg_sold
            gt_percent_retail_bbpdg_sold += dt_percent_retail_bbpdg_sold
            gt_percent_cost_bbpdg_sold += dt_percent_cost_bbpdg_sold
            gt_percent_qty_bbpdg_stock += dt_percent_qty_bbpdg_stock
            gt_percent_retail_bbpdg_stock += dt_percent_retail_bbpdg_stock
            gt_percent_cost_bbpdg_stock += dt_percent_cost_bbpdg_stock
            gt_week_cover_bbpdg += dt_week_cover_bbpdg
            gt_percent_qty_bbkta_sold += dt_percent_qty_bbkta_sold
            gt_percent_retail_bbkta_sold += dt_percent_retail_bbkta_sold
            gt_percent_cost_bbkta_sold += dt_percent_cost_bbkta_sold
            gt_percent_qty_bbkta_stock += dt_percent_qty_bbkta_stock
            gt_percent_retail_bbkta_stock += dt_percent_retail_bbkta_stock
            gt_percent_cost_bbkta_stock += dt_percent_cost_bbkta_stock
            gt_week_cover_bbkta += dt_week_cover_bbkta
            gt_percent_qty_bbptg_sold += dt_percent_qty_bbptg_sold
            gt_percent_retail_bbptg_sold += dt_percent_retail_bbptg_sold
            gt_percent_cost_bbptg_sold += dt_percent_cost_bbptg_sold
            gt_percent_qty_bbptg_stock += dt_percent_qty_bbptg_stock
            gt_percent_retail_bbptg_stock += dt_percent_retail_bbptg_stock
            gt_percent_cost_bbptg_stock += dt_percent_cost_bbptg_stock
            gt_week_cover_bbptg += dt_week_cover_bbptg
            gt_percent_qty_onlne_sold += dt_percent_qty_onlne_sold
            gt_percent_retail_onlne_sold += dt_percent_retail_onlne_sold
            gt_percent_cost_onlne_sold += dt_percent_cost_onlne_sold
            gt_percent_qty_onlne_stock += dt_percent_qty_onlne_stock
            gt_percent_retail_onlne_stock += dt_percent_retail_onlne_stock
            gt_percent_cost_onlne_stock += dt_percent_cost_onlne_stock
            gt_week_cover_onlne += dt_week_cover_onlne

        worksheet.write('A%s:B%s' %(row, row), 'Grand Total', wbf['total_content'])
        worksheet.write('B%s:C%s' %(row, row), '', wbf['total_content'])
        worksheet.write('C%s:D%s' %(row, row), '', wbf['total_content'])

        worksheet.write('D%s:E%s' %(row, row), gt_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('E%s:F%s' %(row, row), str(round(gt_percent_qty_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('F%s:G%s' %(row, row), gt_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('G%s:H%s' %(row, row), str(round(gt_percent_retail_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('H%s:I%s' %(row, row), gt_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('I%s:J%s' %(row, row), str(round(gt_percent_cost_sold, 2)) + '%' or '', wbf['total_content_float'])

        worksheet.write('J%s:K%s' %(row, row), gt_qty_stock_now or 0, wbf['total_content_float'])
        worksheet.write('K%s:L%s' %(row, row), str(round(gt_percent_qty_stock_now, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('L%s:M%s' %(row, row), gt_retail_stock_now or 0, wbf['total_content_float_price'])
        worksheet.write('M%s:N%s' %(row, row), str(round(gt_percent_retail_stock_now, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('N%s:O%s' %(row, row), gt_cost_stock_now or 0, wbf['total_content_float_price'])
        worksheet.write('O%s:P%s' %(row, row), str(round(gt_percent_cost_stock_now, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('P%s:Q%s' %(row, row), gt_week_cover_all or 0, wbf['total_content_float'])

        worksheet.write('Q%s:R%s' %(row, row), gt_qty_stock_last or 0, wbf['total_content_float']) 
        worksheet.write('R%s:S%s' %(row, row), str(round(gt_percent_qty_stock_last, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('S%s:T%s' %(row, row), gt_retail_stock_last or 0, wbf['total_content_float_price']) 
        worksheet.write('T%s:U%s' %(row, row), str(round(gt_percent_retail_stock_last, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('U%s:V%s' %(row, row), gt_cost_stock_last or 0, wbf['total_content_float_price']) 
        worksheet.write('V%s:W%s' %(row, row), str(round(gt_percent_cost_stock_last, 2)) + '%' or '', wbf['total_content_float'])
      
        worksheet.write('W%s:X%s' %(row, row), gt_whbb_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('X%s:Y%s' %(row, row), str(round(gt_percent_qty_whbb_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('Y%s:Z%s' %(row, row), gt_whbb_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('Z%s:AA%s' %(row, row), str(round(gt_percent_retail_whbb_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AA%s:AB%s' %(row, row), gt_whbb_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('AB%s:AC%s' %(row, row), str(round(gt_percent_cost_whbb_stock, 2)) + '%' or '', wbf['total_content_float'])

        # RECEIVING
        worksheet.write('AC%s:AD%s' %(row, row), gt_qty_receiving or 0, wbf['total_content_float'])
        worksheet.write('AD%s:AE%s' %(row, row), str(round(gt_percent_qty_receiving, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AE%s:AF%s' %(row, row), gt_retail_receiving or 0, wbf['total_content_float_price'])
        worksheet.write('AF%s:AG%s' %(row, row), str(round(gt_percent_retail_receiving, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AG%s:AH%s' %(row, row), gt_cost_receiving or 0, wbf['total_content_float_price'])
        worksheet.write('AH%s:AI%s' %(row, row), str(round(gt_percent_cost_receiving, 2)) + '%' or '', wbf['total_content_float'])

        worksheet.write('AI%s:AJ%s' %(row, row), gt_bbflg_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('AJ%s:AK%s' %(row, row), str(round(gt_percent_qty_bbflg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AK%s:AL%s' %(row, row), gt_bbflg_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('AL%s:AM%s' %(row, row), str(round(gt_percent_retail_bbflg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AM%s:AN%s' %(row, row), gt_bbflg_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('AN%s:AO%s' %(row, row), str(round(gt_percent_cost_bbflg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AO%s:AP%s' %(row, row), gt_bbflg_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('AP%s:AQ%s' %(row, row), str(round(gt_percent_qty_bbflg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AQ%s:AR%s' %(row, row), gt_bbflg_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('AR%s:AS%s' %(row, row), str(round(gt_percent_retail_bbflg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AS%s:AT%s' %(row, row), gt_bbflg_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('AT%s:AU%s' %(row, row), str(round(gt_percent_cost_bbflg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AU%s:AV%s' %(row, row), gt_week_cover_bbflg or 0, wbf['total_content_float'])

        worksheet.write('AV%s:AW%s' %(row, row), gt_bbbrw_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('AW%s:AX%s' %(row, row), str(round(gt_percent_qty_bbbrw_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AX%s:AY%s' %(row, row), gt_bbbrw_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('AY%s:AZ%s' %(row, row), str(round(gt_percent_retail_bbbrw_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('AZ%s:BA%s' %(row, row), gt_bbbrw_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('BA%s:BB%s' %(row, row), str(round(gt_percent_cost_bbbrw_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BB%s:BC%s' %(row, row), gt_bbbrw_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('BC%s:BD%s' %(row, row), str(round(gt_percent_qty_bbbrw_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BD%s:BE%s' %(row, row), gt_bbbrw_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('BE%s:BF%s' %(row, row), str(round(gt_percent_retail_bbbrw_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BF%s:BG%s' %(row, row), gt_bbbrw_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('BG%s:BH%s' %(row, row), str(round(gt_percent_cost_bbbrw_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BH%s:BI%s' %(row, row), gt_week_cover_bbbrw or 0, wbf['total_content_float'])

        worksheet.write('BI%s:BJ%s' %(row, row), gt_bbbwk_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('BJ%s:BK%s' %(row, row), str(round(gt_percent_qty_bbbwk_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BK%s:BL%s' %(row, row), gt_bbbwk_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('BL%s:BM%s' %(row, row), str(round(gt_percent_retail_bbbwk_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BM%s:BN%s' %(row, row), gt_bbbwk_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('BN%s:BO%s' %(row, row), str(round(gt_percent_cost_bbbwk_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BO%s:BP%s' %(row, row), gt_bbbwk_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('BP%s:BQ%s' %(row, row), str(round(gt_percent_qty_bbbwk_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BQ%s:BR%s' %(row, row), gt_bbbwk_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('BR%s:BS%s' %(row, row), str(round(gt_percent_retail_bbbwk_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BS%s:BT%s' %(row, row), gt_bbbwk_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('BT%s:BU%s' %(row, row), str(round(gt_percent_cost_bbbwk_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BU%s:BV%s' %(row, row), gt_week_cover_bbbwk or 0, wbf['total_content_float'])

        worksheet.write('BV%s:BW%s' %(row, row), gt_bbglr_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('BW%s:BX%s' %(row, row), str(round(gt_percent_qty_bbglr_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BX%s:BY%s' %(row, row), gt_bbglr_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('BY%s:BZ%s' %(row, row), str(round(gt_percent_retail_bbglr_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('BZ%s:CA%s' %(row, row), gt_bbglr_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('CA%s:CB%s' %(row, row), str(round(gt_percent_cost_bbglr_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CB%s:CC%s' %(row, row), gt_bbglr_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('CC%s:CD%s' %(row, row), str(round(gt_percent_qty_bbglr_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CD%s:CE%s' %(row, row), gt_bbglr_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('CE%s:CF%s' %(row, row), str(round(gt_percent_retail_bbglr_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CF%s:CG%s' %(row, row), gt_bbglr_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('CG%s:CH%s' %(row, row), str(round(gt_percent_cost_bbglr_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CH%s:CI%s' %(row, row), gt_week_cover_bbglr or 0, wbf['total_content_float'])

        worksheet.write('CI%s:BJ%s' %(row, row), gt_bbsyv_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('CJ%s:CK%s' %(row, row), str(round(gt_percent_qty_bbsyv_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CK%s:CL%s' %(row, row), gt_bbsyv_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('CL%s:CM%s' %(row, row), str(round(gt_percent_retail_bbsyv_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CM%s:CN%s' %(row, row), gt_bbsyv_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('CN%s:CO%s' %(row, row), str(round(gt_percent_cost_bbsyv_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CO%s:CP%s' %(row, row), gt_bbsyv_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('CP%s:CQ%s' %(row, row), str(round(dt_percent_qty_bbsyv_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CQ%s:CR%s' %(row, row), gt_bbsyv_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('CR%s:CS%s' %(row, row), str(round(gt_percent_retail_bbsyv_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CS%s:CT%s' %(row, row), gt_bbsyv_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('CT%s:CU%s' %(row, row), str(round(gt_percent_cost_bbsyv_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CU%s:CV%s' %(row, row), gt_week_cover_bbsyv or 0, wbf['total_content_float'])

        worksheet.write('CV%s:CW%s' %(row, row), gt_bbbbg_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('CW%s:CX%s' %(row, row), str(round(gt_percent_qty_bbbbg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CX%s:CY%s' %(row, row), gt_bbbbg_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('CY%s:CZ%s' %(row, row), str(round(gt_percent_retail_bbbbg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('CZ%s:DA%s' %(row, row), gt_bbbbg_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('DA%s:DB%s' %(row, row), str(round(gt_percent_cost_bbbbg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DB%s:DC%s' %(row, row), gt_bbbbg_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('DC%s:DD%s' %(row, row), str(round(gt_percent_qty_bbbbg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DD%s:DE%s' %(row, row), gt_bbbbg_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('DE%s:DF%s' %(row, row), str(round(gt_percent_retail_bbbbg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DF%s:DG%s' %(row, row), gt_bbbbg_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('DG%s:DH%s' %(row, row), str(round(gt_percent_cost_bbbbg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DH%s:DI%s' %(row, row), gt_week_cover_bbbbg or 0, wbf['total_content_float'])

        worksheet.write('DI%s:DJ%s' %(row, row), gt_bbsnr_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('DJ%s:DK%s' %(row, row), str(round(gt_percent_qty_bbsnr_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DK%s:DL%s' %(row, row), gt_bbsnr_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('DL%s:DM%s' %(row, row), str(round(gt_percent_retail_bbsnr_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DM%s:DN%s' %(row, row), gt_bbsnr_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('DN%s:DO%s' %(row, row), str(round(gt_percent_cost_bbsnr_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DO%s:DP%s' %(row, row), gt_bbsnr_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('DP%s:DQ%s' %(row, row), str(round(gt_percent_qty_bbsnr_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DQ%s:DR%s' %(row, row), gt_bbsnr_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('DR%s:DS%s' %(row, row), str(round(gt_percent_retail_bbsnr_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DS%s:DT%s' %(row, row), gt_bbsnr_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('DT%s:DU%s' %(row, row), str(round(gt_percent_cost_bbsnr_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DU%s:DV%s' %(row, row), gt_week_cover_bbsnr or 0, wbf['total_content_float'])

        worksheet.write('DV%s:DW%s' %(row, row), gt_bbblg_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('DW%s:DX%s' %(row, row), str(round(gt_percent_qty_bbblg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DX%s:DY%s' %(row, row), gt_bbblg_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('DY%s:DZ%s' %(row, row), str(round(gt_percent_retail_bbblg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('DZ%s:EA%s' %(row, row), gt_bbblg_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('EA%s:EB%s' %(row, row), str(round(gt_percent_cost_bbblg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EB%s:EC%s' %(row, row), gt_bbblg_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('EC%s:ED%s' %(row, row), str(round(gt_percent_qty_bbblg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('ED%s:EE%s' %(row, row), gt_bbblg_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('EE%s:EF%s' %(row, row), str(round(gt_percent_retail_bbblg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EF%s:EG%s' %(row, row), gt_bbblg_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('EG%s:EH%s' %(row, row), str(round(gt_percent_cost_bbblg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EH%s:EI%s' %(row, row), gt_week_cover_bbblg or 0, wbf['total_content_float'])

        worksheet.write('EI%s:EJ%s' %(row, row), gt_bbpdg_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('EJ%s:EK%s' %(row, row), str(round(gt_percent_qty_bbpdg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EK%s:EL%s' %(row, row), gt_bbpdg_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('EL%s:EM%s' %(row, row), str(round(gt_percent_retail_bbpdg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EM%s:EN%s' %(row, row), gt_bbpdg_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('EN%s:EO%s' %(row, row), str(round(gt_percent_cost_bbpdg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EO%s:EP%s' %(row, row), gt_bbpdg_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('EP%s:EQ%s' %(row, row), str(round(gt_percent_qty_bbpdg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EQ%s:ER%s' %(row, row), gt_bbpdg_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('ER%s:ES%s' %(row, row), str(round(gt_percent_retail_bbpdg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('ES%s:ET%s' %(row, row), gt_bbpdg_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('ET%s:EU%s' %(row, row), str(round(gt_percent_cost_bbpdg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EU%s:EV%s' %(row, row), gt_week_cover_bbpdg or 0, wbf['total_content_float'])

        worksheet.write('EV%s:EW%s' %(row, row), gt_bbkta_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('EW%s:EX%s' %(row, row), str(round(gt_percent_qty_bbkta_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EX%s:EY%s' %(row, row), gt_bbkta_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('EY%s:EZ%s' %(row, row), str(round(gt_percent_retail_bbkta_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('EZ%s:FA%s' %(row, row), gt_bbkta_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('FA%s:FB%s' %(row, row), str(round(gt_percent_cost_bbkta_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FB%s:FC%s' %(row, row), gt_bbkta_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('FC%s:FD%s' %(row, row), str(round(gt_percent_qty_bbkta_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FD%s:FE%s' %(row, row), gt_bbkta_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('FE%s:FF%s' %(row, row), str(round(gt_percent_retail_bbkta_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FF%s:FG%s' %(row, row), gt_bbkta_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('FG%s:FH%s' %(row, row), str(round(gt_percent_cost_bbkta_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FH%s:FI%s' %(row, row), gt_week_cover_bbkta or 0, wbf['total_content_float'])

        worksheet.write('FI%s:FJ%s' %(row, row), gt_bbptg_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('FJ%s:FK%s' %(row, row), str(round(gt_percent_qty_bbptg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FK%s:FL%s' %(row, row), gt_bbptg_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('FL%s:FM%s' %(row, row), str(round(gt_percent_retail_bbptg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FM%s:FN%s' %(row, row), gt_bbptg_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('FN%s:FO%s' %(row, row), str(round(gt_percent_cost_bbptg_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FO%s:FP%s' %(row, row), gt_bbptg_qty_stock or 0, wbf['total_content_float'])
        worksheet.write('FP%s:FQ%s' %(row, row), str(round(gt_percent_qty_bbptg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FQ%s:FR%s' %(row, row), gt_bbptg_retail_stock or 0, wbf['total_content_float_price'])
        worksheet.write('FR%s:FS%s' %(row, row), str(round(gt_percent_retail_bbptg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FS%s:FT%s' %(row, row), gt_bbptg_cost_stock or 0, wbf['total_content_float_price'])
        worksheet.write('FT%s:FU%s' %(row, row), str(round(gt_percent_cost_bbptg_stock, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FU%s:FV%s' %(row, row), gt_week_cover_bbptg or 0, wbf['total_content_float'])

        worksheet.write('FV%s:FW%s' %(row, row), gt_onlne_qty_sold or 0, wbf['total_content_float'])
        worksheet.write('FW%s:FX%s' %(row, row), str(round(gt_percent_qty_onlne_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FX%s:FY%s' %(row, row), gt_onlne_retail_sold or 0, wbf['total_content_float_price'])
        worksheet.write('FY%s:FZ%s' %(row, row), str(round(gt_percent_retail_onlne_sold, 2)) + '%' or '', wbf['total_content_float'])
        worksheet.write('FZ%s:GA%s' %(row, row), gt_onlne_cost_sold or 0, wbf['total_content_float_price'])
        worksheet.write('GA%s:GB%s' %(row, row), str(round(gt_percent_cost_onlne_sold, 2)) + '%' or '', wbf['total_content_float'])

        workbook.close()
        out=base64.encodestring(fp.getvalue())
        self.write({'datas':out, 'datas_fname':filename})
        fp.close()
        filename += '%2Exlsx'

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model='+self._name+'&id='+str(self.id)+'&field=datas&download=true&filename='+filename,
        }

    def add_workbook_format(self, workbook):
        colors = {
            'white_orange': '#DDD9C4',
            'orange': '#FFC300',
            'red': '#FF0000',
            'yellow': '#FFC000',
            'pink': '#FFC0CB',
            'violet': '#E6B8B7',
            'green': '#00B050',
            'light_green': '#90EE90',
            'dark_green': '#C4D79B',
            'blue': '#DBE5F1',
            'brown': '#DDD9C3',
            'salmon': '#FFA07A',
            'beige': '#F5F5DC',
            'blue_old': '#B8CCE4',
        }

        wbf = {}
        wbf['header'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': '#FFFFFF','font_color': '#000000', })
        wbf['header'].set_border()

        wbf['header_brown'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['brown'],'font_color': '#000000', })
        wbf['header_brown'].set_border()

        wbf['header_salmon'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['salmon'],'font_color': '#000000', })
        wbf['header_salmon'].set_border()

        wbf['header_beige'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['beige'],'font_color': '#000000', })
        wbf['header_beige'].set_border()

        wbf['header_blue'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['blue'],'font_color': '#000000', })
        wbf['header_blue'].set_border()

        wbf['header_blue2'] = workbook.add_format({'bold': 1,'align': 'left','bg_color': colors['blue'],'font_color': '#000000', })
        wbf['header_blue2'].set_border()

        wbf['header_green'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['green'],'font_color': '#000000', })
        wbf['header_green'].set_border()

        wbf['header_light_green'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['light_green'],'font_color': '#000000', })
        wbf['header_light_green'].set_border()

        wbf['header_dark_green'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['dark_green'],'font_color': '#000000', })
        wbf['header_dark_green'].set_border()

        wbf['header_pink'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['pink'],'font_color': '#000000', })
        wbf['header_pink'].set_border()

        wbf['header_violet'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['violet'],'font_color': '#000000', })
        wbf['header_violet'].set_border()

        wbf['header_orange'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['orange'],'font_color': '#000000', })
        wbf['header_orange'].set_border()

        wbf['header_white_orange'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['white_orange'],'font_color': '#000000', })
        wbf['header_white_orange'].set_border()

        wbf['header_yellow'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['yellow'],'font_color': '#000000', })
        wbf['header_yellow'].set_border()
        
        wbf['header_no'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': '#FFFFDB','font_color': '#000000', })
        wbf['header_no'].set_border()
        wbf['header_no'].set_align('vcenter')
                
        wbf['footer'] = workbook.add_format({'align':'left', })
        
        wbf['content_datetime'] = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss', })
        wbf['content_datetime'].set_left()
        wbf['content_datetime'].set_right()
        
        wbf['content_date'] = workbook.add_format({'num_format': 'yyyy-mm-dd', })
        wbf['content_date'].set_left()
        wbf['content_date'].set_right() 

        wbf['title_doc_pink'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 16,
            'bg_color': '#FFC0CB',
        })

        wbf['title_doc_brown'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 14,
            'bg_color': '#FFEFD5',
        })
        
        wbf['title_doc'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 20,
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc2'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 14,
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc3'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 12,
            'bg_color': '#FFFFFF',
        })
        wbf['title_doc3'].set_top()
        wbf['title_doc3'].set_bottom()            
        wbf['title_doc3'].set_left()
        wbf['title_doc3'].set_right()  
        
        wbf['company'] = workbook.add_format({'align': 'left', })
        wbf['company'].set_font_size(11)
        
        wbf['content'] = workbook.add_format()
        wbf['content'].set_left()
        wbf['content'].set_right() 

        wbf['content2'] = workbook.add_format({'align': 'center', })
        wbf['content2'].set_left()
        wbf['content2'].set_right()

        wbf['total_content'] = workbook.add_format({'font_size': 9, 'bold': 1,'align': 'left','bg_color': colors['blue_old'],'font_color': '#000000', })
        wbf['total_content'].set_border()

        wbf['total_content_float'] = workbook.add_format({'font_size': 9,'bold': True, 'align': 'center','num_format': '#,##0', 'bg_color': colors['blue_old'], 'font_color': '#000000'})
        wbf['total_content_float'].set_border() 

        wbf['total_content_float_price'] = workbook.add_format({'font_size': 9,'bold': True, 'align': 'right','num_format': '#,##0.00', 'bg_color': colors['blue_old'], 'font_color': '#000000'})
        wbf['total_content_float_price'].set_border() 
        
        wbf['content_float'] = workbook.add_format({'font_size': 9, 'align': 'center','num_format': '#,##0', })
        wbf['content_float'].set_right() 
        wbf['content_float'].set_left()

        wbf['content_float_price'] = workbook.add_format({'font_size': 9, 'align': 'right','num_format': '#,##0.00', })
        wbf['content_float_price'].set_right() 
        wbf['content_float_price'].set_left()

        wbf['content_number'] = workbook.add_format({'align': 'right', 'num_format': '#,##0', })
        wbf['content_number'].set_right() 
        wbf['content_number'].set_left() 
        
        wbf['content_percent'] = workbook.add_format({'align': 'right','num_format': '0.00%', })
        wbf['content_percent'].set_right() 
        wbf['content_percent'].set_left() 
                
        wbf['total_float'] = workbook.add_format({'bold':1, 'bg_color':colors['white_orange'], 'align':'right', 'num_format':'#,##0.00', })
        wbf['total_float'].set_top()
        wbf['total_float'].set_bottom()            
        wbf['total_float'].set_left()
        wbf['total_float'].set_right()         
        
        wbf['total_number'] = workbook.add_format({'align':'right','bg_color': colors['white_orange'],'bold':1, 'num_format': '#,##0', })
        wbf['total_number'].set_top()
        wbf['total_number'].set_bottom()            
        wbf['total_number'].set_left()
        wbf['total_number'].set_right()
        
        wbf['total'] = workbook.add_format({'bold':1, 'bg_color':colors['white_orange'], 'align':'center', })
        wbf['total'].set_left()
        wbf['total'].set_right()
        wbf['total'].set_top()
        wbf['total'].set_bottom()

        wbf['total_float_yellow'] = workbook.add_format({'bold':1, 'bg_color':colors['yellow'], 'align':'right', 'num_format':'#,##0.00', })
        wbf['total_float_yellow'].set_top()
        wbf['total_float_yellow'].set_bottom()
        wbf['total_float_yellow'].set_left()
        wbf['total_float_yellow'].set_right()
        
        wbf['total_number_yellow'] = workbook.add_format({'align':'right','bg_color': colors['yellow'],'bold':1, 'num_format': '#,##0', })
        wbf['total_number_yellow'].set_top()
        wbf['total_number_yellow'].set_bottom()
        wbf['total_number_yellow'].set_left()
        wbf['total_number_yellow'].set_right()
        
        wbf['total_yellow'] = workbook.add_format({'bold':1, 'bg_color':colors['yellow'], 'align':'center', })
        wbf['total_yellow'].set_left()
        wbf['total_yellow'].set_right()
        wbf['total_yellow'].set_top()
        wbf['total_yellow'].set_bottom()

        wbf['total_float_orange'] = workbook.add_format({'bold':1, 'bg_color':colors['orange'], 'align':'right', 'num_format':'#,##0.00', })
        wbf['total_float_orange'].set_top()
        wbf['total_float_orange'].set_bottom()            
        wbf['total_float_orange'].set_left()
        wbf['total_float_orange'].set_right()         
        
        wbf['total_number_orange'] = workbook.add_format({'align':'right','bg_color': colors['orange'],'bold':1, 'num_format': '#,##0', })
        wbf['total_number_orange'].set_top()
        wbf['total_number_orange'].set_bottom()            
        wbf['total_number_orange'].set_left()
        wbf['total_number_orange'].set_right()
        
        wbf['total_orange'] = workbook.add_format({'bold':1, 'bg_color':colors['orange'], 'align':'center', })
        wbf['total_orange'].set_left()
        wbf['total_orange'].set_right()
        wbf['total_orange'].set_top()
        wbf['total_orange'].set_bottom()

        wbf['total_pink'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align':'right', })
        wbf['total_pink'].set_left()
        wbf['total_pink'].set_right()
        wbf['total_pink'].set_top()
        wbf['total_pink'].set_bottom()

        wbf['total_float_pink'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align': 'right','num_format': '#,##0.00', })
        wbf['total_float_pink'].set_left()
        wbf['total_float_pink'].set_right()
        wbf['total_float_pink'].set_top()
        wbf['total_float_pink'].set_bottom()

        wbf['total_float_pink2'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align': 'center','num_format': '#,##0.00', })
        wbf['total_float_pink2'].set_left()
        wbf['total_float_pink2'].set_right()
        wbf['total_float_pink2'].set_top()
        wbf['total_float_pink2'].set_bottom() 

        wbf['total_violet'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align':'right', })
        wbf['total_violet'].set_left()
        wbf['total_violet'].set_right()
        wbf['total_violet'].set_top()
        wbf['total_violet'].set_bottom()

        wbf['total_float_violet'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align': 'right','num_format': '#,##0.00', })
        wbf['total_float_violet'].set_left()
        wbf['total_float_violet'].set_right()
        wbf['total_float_violet'].set_top()
        wbf['total_float_violet'].set_bottom()

        wbf['total_float_violet2'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align': 'center','num_format': '#,##0.00', })
        wbf['total_float_violet2'].set_left()
        wbf['total_float_violet2'].set_right()
        wbf['total_float_violet2'].set_top()
        wbf['total_float_violet2'].set_bottom() 
        
        wbf['header_detail_space'] = workbook.add_format({})
        wbf['header_detail_space'].set_left()
        wbf['header_detail_space'].set_right()
        wbf['header_detail_space'].set_top()
        wbf['header_detail_space'].set_bottom()
        
        wbf['header_detail'] = workbook.add_format({'bg_color': '#E0FFC2', })
        wbf['header_detail'].set_left()
        wbf['header_detail'].set_right()
        wbf['header_detail'].set_top()
        wbf['header_detail'].set_bottom()
        
        return wbf, workbook
