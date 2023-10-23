from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ReportMensClothes(models.TransientModel):
    _name = 'report.mens.clothes.wizard'
    _description = 'Report Mens Clothes Wizard'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    # product_model_id = fields.Many2one('product.model', string='Model')
    class_product = fields.Many2one('class.product', string='Class')
    product_model_id = fields.Many2one('product.category', string='Model', domain=[('category_product', '=', 'department')])
    product_category_id = fields.Many2one('product.category', string='Category')
    pos_config_id = fields.Many2one('pos.config', string='Store')
    types = fields.Selection([("staples","Staples"),("trend","Trend")], string='Type')
    aging_from = fields.Integer(string='Aging From')
    aging_to = fields.Integer(string='Aging To')
    stock_type = fields.Many2one('stock.type', string='Stock Type')
    is_stock_type = fields.Boolean(string='Stock Type ?')
    type_in_report = fields.Selection([("best","best"),("slow","slow")], string='type in report')

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
        datas['model'] = 'report.mens.clothes.wizard'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
                
        print("self.type_in_report")
        print(self.type_in_report)
        if self.type_in_report == 'slow' :
            return self.env.ref('sol_bb_report.report_slow_clothes_wizard_xlsx').report_action(self, data=datas)
        else :
            return self.env.ref('sol_bb_report.report_mens_clothes_wizard_xlsx').report_action(self, data=datas)
