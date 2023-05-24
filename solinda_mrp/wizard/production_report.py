from odoo import api, fields, models

class ProductionReport(models.TransientModel):
    _name = 'production.report'
    _description = 'Production Report'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    service = fields.Many2one('mrp.workcenter', string='Service')
    supplier = fields.Many2many('res.partner', string='Supplier')

    def action_print_report(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'production.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('solinda_mrp.production_report_action_xlsx').report_action(self, data=datas)