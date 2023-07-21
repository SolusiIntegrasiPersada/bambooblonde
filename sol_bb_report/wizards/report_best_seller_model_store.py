from odoo import fields, models, api


class ReportBestSellerModelStore(models.TransientModel):
    _name = 'report.best.seller.model.store.wizard'
    _description = 'Report Best Seller Model Store Wizard'

    @api.model
    def default_pos_config_id(self):
        user = self.env['res.users'].browse(self.env.user.uid)
        pos_config_id = user.pos_config_ids[0]
        return pos_config_id

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    product_model_id = fields.Many2one('product.model', string='Model')
    pos_config_id = fields.Many2one('pos.config', string='Store', default=default_pos_config_id)

    def button_generate_excel(self):
        context = self._context
        datas = {
            'ids': context.get('active_ids', []),
            'model': 'report.best.seller.model.store.wizard',
            'form': self.read()[0]
        }
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_best_seller_model_store_wizard_xlsx').report_action(self, data=datas)