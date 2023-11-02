from odoo import fields, models

class ReportSupplierSewingReport(models.TransientModel):
    _name = 'report.supplier.sewing.report.wizard'
    _description = 'Report Supplier Sewing Report Wizard'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    def button_generate_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.supplier.sewing.report.wizard'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_supplier_sewing_report_wizard_xlsx').report_action(self, data=datas)
