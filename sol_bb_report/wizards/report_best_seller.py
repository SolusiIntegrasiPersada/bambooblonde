from odoo import api, fields, models

class ReportBestSellerCategory(models.TransientModel):
    _name = 'report.best.seller.category'
    _description = 'Report Best Seller per Category'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    category = fields.Many2one('product.category', string='Category')

    def button_generate_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.best.seller.category'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_best_seller_category_wizard_xlsx').report_action(self, data=datas)