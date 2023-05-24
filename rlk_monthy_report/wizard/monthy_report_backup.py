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

        worksheet.merge_range('FV3:GA3', 'ONLINE STORE', wbf['header_white_orange'])
        worksheet.merge_range('FV4:GA4', 'SOLD', wbf['header_light_green'])

        worksheet.write('FV5:FW5', 'Qty Sold', wbf['header_blue'])
        worksheet.write('FW5:FX5', '%', wbf['header_blue'])
        worksheet.write('FX5:FY5', 'Value Retail Sold', wbf['header_blue'])
        worksheet.write('FY5:FZ5', '%', wbf['header_blue'])
        worksheet.write('FZ5:GA5', 'Value Cost Sold', wbf['header_blue'])
        worksheet.write('GA5:GB5', '%', wbf['header_blue'])

        # filter sales orders based on date range
        pos_orders = self.env['pos.order.line'].search([
            ('order_id.state', 'not in', ['draft','cancel']),
            ('order_id.date_order', '>=', self.last_start_date),
            ('order_id.date_order', '<=', self.end_date)
        ])

        report_data = {}
        for line in pos_orders:
            prod = line.product_id
            class_id = prod.class_product.name
            category = prod.categ_id.name
            category_id = prod.categ_id
            parent_category = category_id.parent_id.name
            cost_price = prod.standard_price
            retail_price = prod.lst_price
            qty_sold = line.qty
            retail_sold = qty_sold * retail_price
            cost_sold = qty_sold * cost_price
            warehouse = line.order_id.picking_type_id.warehouse_id
            qty_stock = sum(line.product_id.stock_quant_ids.filtered(lambda x: x.location_id.usage == 'internal' and x.location_id == warehouse and x.in_date >= self.last_start_date and x.in_date <= self.end_date).mapped('quantity'))
            qty_received = sum(line.product_id.stock_move_ids.filtered(lambda x: x.picking_type_id.code == 'incoming' and x.location_dest_id == warehouse and x.state == 'done' and x.date >= self.last_start_date and x.date <= self.end_date).mapped('product_qty'))
            retail_stock = qty_stock * retail_price
            cost_stock = qty_stock * cost_price
            retail_received = qty_received * retail_price
            cost_received = qty_received * cost_price

            # create keys for the report_data dictionary
            key = (class_id, parent_category, category)

            if key not in report_data:
                report_data[key] = {
                    'class_name': class_id,
                    'parent_category': parent_category,
                    'category': category,
                    'cost_price': cost_price,
                    'retail_price': retail_price,

                    'total_qty_sold': 0,
                    'total_retail_sold': 0,
                    'total_cost_sold': 0,

                    'total_qty_stock_now': 0,
                    'total_retail_stock_now': 0,
                    'total_cost_stock_now': 0,

                    'total_qty_stock_last': 0,
                    'total_retail_stock_last': 0,
                    'total_cost_stock_last': 0,

                    'total_qty_receiving': 0,
                    'total_retail_receiving': 0,
                    'total_cost_receiving': 0,

                    'w_qty_sold': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                    'w_qty_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                    'w_retail_sold': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                    'w_retail_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                    'w_cost_sold': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                    'w_cost_stock': {'WHBB': 0, 'BBFLG': 0, 'BBBBG': 0, 'BBBWK': 0, 'BBBRW': 0, 'BBPDG': 0, 'BBSYV': 0, 'BBGLR': 0, 'BBBLG': 0, 'BBSNR': 0, 'BBPTG': 0, 'BBKTA': 0, 'Online': 0},
                }

            warehouse_key = warehouse.code
            if warehouse_key in ('WHBB','BBFLG','BBBBG','BBBWK','BBBRW','BBPDG','BBSYV','BBGLR','BBBLG','BBSNR','BBPTG','BBKTA','Onlne'):
                if line.order_id.date_order.date() >= self.start_date.replace(day=1) and line.order_id.date_order.date() <= self.end_date.replace(day=calendar.monthrange(self.end_date.year, self.end_date.month)[1]):
                    report_data[key]['total_qty_sold'] += qty_sold
                    report_data[key]['total_retail_sold'] += retail_sold
                    report_data[key]['total_cost_sold'] += cost_sold

                    report_data[key]['total_qty_stock_now'] += qty_stock
                    report_data[key]['total_retail_stock_now'] += retail_stock
                    report_data[key]['total_cost_stock_now'] += cost_stock

                    report_data[key]['total_qty_receiving'] += qty_received
                    report_data[key]['total_retail_receiving'] += retail_received
                    report_data[key]['total_cost_receiving'] += cost_received

                    report_data[key]['w_qty_sold'][warehouse_key] += qty_sold
                    report_data[key]['w_qty_stock'][warehouse_key] += qty_stock

                    report_data[key]['w_retail_sold'][warehouse_key] += retail_sold
                    report_data[key]['w_cost_sold'][warehouse_key] += cost_sold

                    report_data[key]['w_retail_stock'][warehouse_key] += retail_stock
                    report_data[key]['w_cost_stock'][warehouse_key] += cost_stock

                elif line.order_id.date_order.date() >= self.last_start_date.replace(day=1) and line.order_id.date_order.date() <= self.last_end_date.replace(day=calendar.monthrange(self.last_end_date.year, self.last_end_date.month)[1]):
                    report_data[key]['total_qty_stock_last'] += qty_stock
                    report_data[key]['total_retail_stock_last'] += retail_stock
                    report_data[key]['total_cost_stock_last'] += cost_stock

        rows = []
        for data in report_data.values():
            row = [data['class_name'],
                   data['parent_category'],
                   data['category'],
                   data['cost_price'],
                   data['retail_price'],

                   data['total_qty_sold'],
                   data['total_retail_sold'],
                   data['total_cost_sold']
                   ]
            rows.append(row)


        grouped_colors = {}
        total_qty_sold_all_classes = 0
        for row in rows:
            class_id, parent_category, category, cost_price, retail_price, qty_sold, retail_sold, cost_sold = row
            key = (class_id,parent_category,category)
            if key not in grouped_colors:
                grouped_colors[key] = {
                    'class_id': class_id,
                    'parent_categories': {},
                    'total_qty_sold': 0
                }
            else:
                grouped_colors[key]['total_qty_sold'] += qty_sold

            if parent_category not in grouped_colors[key]['parent_categories']:
                grouped_colors[key]['parent_categories'][parent_category] = {
                    'parent_category': parent_category,
                    'categories': {},
                    'total_qty_sold': 0
                }
            else:
                grouped_colors[key]['parent_categories'][parent_category]['total_qty_sold'] += qty_sold


            # if category not in grouped_colors[key]['parent_categories'][parent_category]['categories']:
            #     grouped_colors[key]['parent_categories'][parent_category]['categories'][category] = {
            #         'category': category,
            #         'total_qty_sold': 0
            #     }
            # else:
            #     grouped_colors[key]['parent_categories'][parent_category]['categories'][category]['total_qty_sold'] += qty_sold

            total_qty_sold_all_classes += qty_sold
        print (grouped_colors)

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
            'white_orange': '#FFFFDB',
            'orange': '#FFC300',
            'red': '#FF0000',
            'yellow': '#F6FA03',
            'pink': '#FFC0CB',
            'violet': '#EE82EE',
            'green': '#00FF7F',
            'light_green': '#90EE90',
            'dark_green': '#8FBC8F',
            'blue': '#B0E0E6',
            'brown': '#FFEFD5',
            'salmon': '#FFA07A',
            'beige': '#F5F5DC',
        }

        wbf = {}
        wbf['header'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': '#FFFFFF','font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header'].set_border()

        wbf['header_brown'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['brown'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_brown'].set_border()

        wbf['header_salmon'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['salmon'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_salmon'].set_border()

        wbf['header_beige'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['beige'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_beige'].set_border()

        wbf['header_blue'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['blue'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_blue'].set_border()

        wbf['header_blue2'] = workbook.add_format({'bold': 1,'align': 'left','bg_color': colors['blue'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_blue2'].set_border()

        wbf['header_green'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['green'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_green'].set_border()

        wbf['header_light_green'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['light_green'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_light_green'].set_border()

        wbf['header_dark_green'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['dark_green'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_dark_green'].set_border()

        wbf['header_pink'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['pink'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_pink'].set_border()

        wbf['header_violet'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['violet'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_violet'].set_border()

        wbf['header_orange'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['orange'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_orange'].set_border()

        wbf['header_white_orange'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['white_orange'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_white_orange'].set_border()

        wbf['header_yellow'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': colors['yellow'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_yellow'].set_border()
        
        wbf['header_no'] = workbook.add_format({'bold': 1,'align': 'center','bg_color': '#FFFFDB','font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_no'].set_border()
        wbf['header_no'].set_align('vcenter')
                
        wbf['footer'] = workbook.add_format({'align':'left', 'font_name': 'Georgia'})
        
        wbf['content_datetime'] = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss', 'font_name': 'Georgia'})
        wbf['content_datetime'].set_left()
        wbf['content_datetime'].set_right()
        
        wbf['content_date'] = workbook.add_format({'num_format': 'yyyy-mm-dd', 'font_name': 'Georgia'})
        wbf['content_date'].set_left()
        wbf['content_date'].set_right() 

        wbf['title_doc_pink'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 16,
            'font_name': 'Georgia',
            'bg_color': '#FFC0CB',
        })

        wbf['title_doc_brown'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 14,
            'font_name': 'Georgia',
            'bg_color': '#FFEFD5',
        })
        
        wbf['title_doc'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 20,
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc2'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 14,
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })

        wbf['title_doc3'] = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': 'Georgia',
            'bg_color': '#FFFFFF',
        })
        wbf['title_doc3'].set_top()
        wbf['title_doc3'].set_bottom()            
        wbf['title_doc3'].set_left()
        wbf['title_doc3'].set_right()  
        
        wbf['company'] = workbook.add_format({'align': 'left', 'font_name': 'Georgia'})
        wbf['company'].set_font_size(11)
        
        wbf['content'] = workbook.add_format()
        wbf['content'].set_left()
        wbf['content'].set_right() 

        wbf['content2'] = workbook.add_format({'align': 'center', 'font_name': 'Georgia'})
        wbf['content2'].set_left()
        wbf['content2'].set_right()

        wbf['total_content'] = workbook.add_format({'font_size': 9, 'bold': 1,'align': 'left','bg_color': colors['blue'],'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['total_content'].set_border() 

        wbf['total_content_float'] = workbook.add_format({'font_size': 9,'bold': True, 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia','bg_color': colors['blue'], 'font_color': '#000000'})
        wbf['total_content_float'].set_border() 

        wbf['total_content_float_price'] = workbook.add_format({'font_size': 9,'bold': True, 'align': 'right','num_format': '#,##0.00', 'font_name': 'Georgia','bg_color': colors['blue'], 'font_color': '#000000'})
        wbf['total_content_float_price'].set_border() 
        
        wbf['content_float'] = workbook.add_format({'font_size': 9, 'align': 'center','num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_float'].set_right() 
        wbf['content_float'].set_left()

        wbf['content_float_price'] = workbook.add_format({'font_size': 9, 'align': 'right','num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['content_float_price'].set_right() 
        wbf['content_float_price'].set_left()

        wbf['content_number'] = workbook.add_format({'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_number'].set_right() 
        wbf['content_number'].set_left() 
        
        wbf['content_percent'] = workbook.add_format({'align': 'right','num_format': '0.00%', 'font_name': 'Georgia'})
        wbf['content_percent'].set_right() 
        wbf['content_percent'].set_left() 
                
        wbf['total_float'] = workbook.add_format({'bold':1, 'bg_color':colors['white_orange'], 'align':'right', 'num_format':'#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float'].set_top()
        wbf['total_float'].set_bottom()            
        wbf['total_float'].set_left()
        wbf['total_float'].set_right()         
        
        wbf['total_number'] = workbook.add_format({'align':'right','bg_color': colors['white_orange'],'bold':1, 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_number'].set_top()
        wbf['total_number'].set_bottom()            
        wbf['total_number'].set_left()
        wbf['total_number'].set_right()
        
        wbf['total'] = workbook.add_format({'bold':1, 'bg_color':colors['white_orange'], 'align':'center', 'font_name': 'Georgia'})
        wbf['total'].set_left()
        wbf['total'].set_right()
        wbf['total'].set_top()
        wbf['total'].set_bottom()

        wbf['total_float_yellow'] = workbook.add_format({'bold':1, 'bg_color':colors['yellow'], 'align':'right', 'num_format':'#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_yellow'].set_top()
        wbf['total_float_yellow'].set_bottom()
        wbf['total_float_yellow'].set_left()
        wbf['total_float_yellow'].set_right()
        
        wbf['total_number_yellow'] = workbook.add_format({'align':'right','bg_color': colors['yellow'],'bold':1, 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_number_yellow'].set_top()
        wbf['total_number_yellow'].set_bottom()
        wbf['total_number_yellow'].set_left()
        wbf['total_number_yellow'].set_right()
        
        wbf['total_yellow'] = workbook.add_format({'bold':1, 'bg_color':colors['yellow'], 'align':'center', 'font_name': 'Georgia'})
        wbf['total_yellow'].set_left()
        wbf['total_yellow'].set_right()
        wbf['total_yellow'].set_top()
        wbf['total_yellow'].set_bottom()

        wbf['total_float_orange'] = workbook.add_format({'bold':1, 'bg_color':colors['orange'], 'align':'right', 'num_format':'#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_orange'].set_top()
        wbf['total_float_orange'].set_bottom()            
        wbf['total_float_orange'].set_left()
        wbf['total_float_orange'].set_right()         
        
        wbf['total_number_orange'] = workbook.add_format({'align':'right','bg_color': colors['orange'],'bold':1, 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['total_number_orange'].set_top()
        wbf['total_number_orange'].set_bottom()            
        wbf['total_number_orange'].set_left()
        wbf['total_number_orange'].set_right()
        
        wbf['total_orange'] = workbook.add_format({'bold':1, 'bg_color':colors['orange'], 'align':'center', 'font_name': 'Georgia'})
        wbf['total_orange'].set_left()
        wbf['total_orange'].set_right()
        wbf['total_orange'].set_top()
        wbf['total_orange'].set_bottom()

        wbf['total_pink'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align':'right', 'font_name': 'Georgia'})
        wbf['total_pink'].set_left()
        wbf['total_pink'].set_right()
        wbf['total_pink'].set_top()
        wbf['total_pink'].set_bottom()

        wbf['total_float_pink'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align': 'right','num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_pink'].set_left()
        wbf['total_float_pink'].set_right()
        wbf['total_float_pink'].set_top()
        wbf['total_float_pink'].set_bottom()

        wbf['total_float_pink2'] = workbook.add_format({'bold':1, 'bg_color':colors['pink'], 'align': 'center','num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_pink2'].set_left()
        wbf['total_float_pink2'].set_right()
        wbf['total_float_pink2'].set_top()
        wbf['total_float_pink2'].set_bottom() 

        wbf['total_violet'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align':'right', 'font_name': 'Georgia'})
        wbf['total_violet'].set_left()
        wbf['total_violet'].set_right()
        wbf['total_violet'].set_top()
        wbf['total_violet'].set_bottom()

        wbf['total_float_violet'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align': 'right','num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_violet'].set_left()
        wbf['total_float_violet'].set_right()
        wbf['total_float_violet'].set_top()
        wbf['total_float_violet'].set_bottom()

        wbf['total_float_violet2'] = workbook.add_format({'bold':1, 'bg_color':colors['violet'], 'align': 'center','num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['total_float_violet2'].set_left()
        wbf['total_float_violet2'].set_right()
        wbf['total_float_violet2'].set_top()
        wbf['total_float_violet2'].set_bottom() 
        
        wbf['header_detail_space'] = workbook.add_format({'font_name': 'Georgia'})
        wbf['header_detail_space'].set_left()
        wbf['header_detail_space'].set_right()
        wbf['header_detail_space'].set_top()
        wbf['header_detail_space'].set_bottom()
        
        wbf['header_detail'] = workbook.add_format({'bg_color': '#E0FFC2', 'font_name': 'Georgia'})
        wbf['header_detail'].set_left()
        wbf['header_detail'].set_right()
        wbf['header_detail'].set_top()
        wbf['header_detail'].set_bottom()
        
        return wbf, workbook
