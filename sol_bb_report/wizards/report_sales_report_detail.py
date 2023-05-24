from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ReportSalesReportDetailWizard(models.TransientModel):
    _name = 'report.sales.report.detail.wizard'
    _description = 'Report Sales Report Detail Wizard'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    sales_from_date = fields.Date(string='Sales From Date')
    sales_to_date = fields.Date(string='Sales To Date')
    incoming_date = fields.Date(string='Incoming Date')

    def button_generate_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.sales.report.detail.wizard'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_sales_report_detail_wizard_xlsx').report_action(self, data=datas)
