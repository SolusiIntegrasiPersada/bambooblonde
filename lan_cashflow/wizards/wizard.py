from odoo import _, api, fields, models

class GenerateCashflowWizard(models.TransientModel):
    _name = 'generate.cashflow.wizard'
    _description = 'Generate Cashflow Wizard'
    
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    company_id = fields.Many2one('res.company', string='Company')

    def download_xlsx_report(self):
        action_report = 'lan_cashflow.action_report_cashflow'
        return self.env.ref(action_report).report_action(self)