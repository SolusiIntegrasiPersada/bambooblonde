from odoo import api, fields, models

# untuk category women clothes plain and print

class ReportBestSellerCategory(models.TransientModel):
    _name = 'report.best.seller.women'
    _description = 'Report Best Seller Women Clothes Plain & Print'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    print_type = fields.Selection([('print','Print'),('plain','Plain')], string='Print Type')

    def button_generate_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.best.seller.women'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_best_seller_women_wizard_xlsx').report_action(self, data=datas)