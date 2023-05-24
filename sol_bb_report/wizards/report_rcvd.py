from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ReportRcvdWizard(models.TransientModel):
    _name = 'report.rcvd.wizard'
    _description = 'Report RCVD Wizard'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    def button_generate_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.rcvd.wizard'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_rcvd_wizard_xlsx').report_action(self, data=datas)
