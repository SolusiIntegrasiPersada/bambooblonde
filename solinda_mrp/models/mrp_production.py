from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    trans_date = fields.Datetime(string='Transaction Date',default=fields.Datetime.now(),required=True,readonly=True,)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mrp.production')
        return super(MrpProduction, self).create(vals)

    @api.depends('initial')
    def _compute_sequence_customer(self):
        n = self.search_count([('customer', '=', self.customer.id)])
        for line in self:
            if line.initial:
                line.seq_report = line.initial + " - " + str(n+1)
            else:
                line.seq_report = str(n+1)

    seq_report = fields.Char(string='Customer', compute="_compute_sequence_customer", store=True)        
    customer = fields.Many2one(related='bom_id.customer', string='Customer', store=True)
    initial = fields.Char(related='customer.customer_initial', string='Initial', store=True)
    sales_order_id = fields.Many2one('sale.order', string='SO No.')
    po_no = fields.Char(string='PO No.')
    purchase_id = fields.Many2one('purchase.order', string='PO Bamboo')
    purchase_taboo_id = fields.Char(string="PO Taboo")
    delivery_date = fields.Date(string="Delivery")
    product_tmpl_id = fields.Many2one('product.template', string='Product',related="product_id.product_tmpl_id")
    move_byproduct_ids = fields.One2many('stock.move')
    # move_byproduct_ids = fields.One2many('stock.move', compute='_compute_move_byproduct_ids', inverse='_set_move_byproduct_ids')

    def _pre_button_mark_done(self):
        productions_to_immediate = self._check_immediate()
        if productions_to_immediate:
            return productions_to_immediate._action_generate_immediate_wizard()

        for production in self:
            if float_is_zero(production.qty_producing, precision_rounding=production.product_uom_id.rounding):
                raise UserError(_('The quantity to produce must be positive!'))
            if production.move_raw_ids and not any(production.move_raw_ids.mapped('quantity_done')):
                raise UserError(_("You must indicate a non-zero amount consumed for at least one of your components"))
        return True
    
