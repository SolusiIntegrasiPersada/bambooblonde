from odoo import api, fields, models


class SewingReport(models.TransientModel):
    _name = 'sewing.report'
    _description = 'Sewing Report'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    service = fields.Many2one('mrp.workcenter', string='Service')
    customer = fields.Many2many('res.partner', string='Customer')

    def action_print_report(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'sewing.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('solinda_mrp.sewing_report_action_xlsx').report_action(self, data=datas)
