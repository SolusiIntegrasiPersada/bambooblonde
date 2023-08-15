from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ReportSampleDevelopmentWizard(models.TransientModel):
    _name = 'report.sample.development.wizard'
    _description = 'Report Sample Development Wizard'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    sales_from_date = fields.Date(string='Sales From Date')
    sales_to_date = fields.Date(string='Sales To Date')
    incoming_date = fields.Date(string='Incoming Date')

    def button_generate_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.sample.development.wizard'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_sample_development_wizard_xlsx').report_action(self, data=datas)
