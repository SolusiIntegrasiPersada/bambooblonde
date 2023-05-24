from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ReportStaplesStyle(models.TransientModel):
    _name = 'report.staples.style.wizard'
    _description = 'Report Staples Style Wizard'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    def button_generate_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.staples.style.wizard'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_staples_styles_wizard_xlsx').report_action(self, data=datas)
