from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ReportRibKnitJerseyDress(models.TransientModel):
    _name = 'report.rib.knit.jersey.dress.wizard'
    _description = 'Report RIB KNIT JERSEY DRESS Wizard'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    stock_type = fields.Many2one('stock.type', string='Stock Type')

    # Invisible
    product_model_id = fields.Many2one('product.category', string='Model', domain=[('category_product', '=', 'department')])
    product_category_id = fields.Many2one('product.category', string='Category')
    pos_config_id = fields.Many2one('pos.config', string='Store')
    aging_from = fields.Integer(string='Aging From', default=0)
    aging_to = fields.Integer(string='Aging To', default=1000)

    @api.onchange('product_model_id')
    def onchange_domain_product_category_id(self):
        if self.product_category_id:
            self.write({'product_category_id': False})
        if self.product_model_id:
            domain = [('category_product', '=', 'category'), ('parent_id', '=', self.product_model_id.id)]
            return {'domain': {'product_category_id': domain}}
        else:
            return {}

    def button_generate_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.rib.knit.jersey.dress.wizard'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('sol_bb_report.report_rib_knit_jersey_dress_wizard_xlsx').report_action(self, data=datas)
