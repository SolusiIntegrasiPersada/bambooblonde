from odoo import fields, api, models

class StockPerStoreWizard(models.TransientModel):
  _name = 'stock.per.store.wizard'
  _description = 'Stock Per Store'

  warehouse = fields.Many2one('stock.warehouse', string='Warehouse')

  def action_print_report(self):
    # domain =[]
    # if self.warehouse_id:
    #   domain += [('name_warehouse_id', '=', self.warehouse_id.id)]
    # quant = self.env['stock.quant'].search_read(domain)
    # data = {
    #   'warehouse': self.warehouse_id.name,
    #   'quant': quant,
    #   'form_data': self.read()[0]
    # }

    context = self._context
    datas = {'ids': context.get('active_ids', [])}
    datas['model'] = 'stock.per.store.wizard'
    datas['form'] = self.read()[0]
    for field in datas['form'].keys():
      if isinstance(datas['form'][field], tuple):
        datas['form'][field] = datas['form'][field][0]
    return self.env.ref('sol_stock.stock_per_store_action_xlsx').report_action(self, data=datas)