from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ReportSampDev(models.TransientModel):
    _name = 'report.sampdev.wizard'
    _description = 'Report SampDev Wizard'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    style_name_id = fields.Many2one('original.sample', string="Style Name")
    style_name = fields.Char(string="Related Style Name", related="style_name_id.name")

    def name_get(self):
        result = []
        for record in self:
            if record.style_name_id:
                result.append((record.id, record.style_name_id.name))
            else:
                result.append((record.id, ''))
        return result

    def button_generate_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.sampdev.wizard'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_sampdev_wizard_xlsx').report_action(self, data=datas)
