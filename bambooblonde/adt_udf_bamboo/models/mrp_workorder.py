from odoo import fields, models, api, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    # total_receipt = fields.Float(string='Total Receipt',)

    def button_finish(self):
        """
        Function to inherit button finish and automatically creates stock_move based on pair with
        MRP Workorder create_po function
        """
        res = super(MrpWorkorder, self).button_finish()
        for data in self :
            if data.order_id :
                picking_obj = self.env['stock.picking'].search([('origin','=',data.order_id.name)])
                if picking_obj :
                    for picking in picking_obj :
                        if picking.state != 'done' :
                            raise UserError(_('Picking has not been done !'))
                        else :
                            data.in_date = picking.date_done
                            stock_move_obj = self.env['stock.move'].search([('picking_id','=',picking.id)])
                            if stock_move_obj :
                                for stock_move in stock_move_obj :
                                    # if data.workcenter_id.id not in (4,5) :
                                    #     data.total_receipt = stock_move.quantity_done
                                    data.total_receipt += stock_move.quantity_done
            if data.workcenter_id.name == 'CUTTING' :
                sql_query = """
                    update mrp_workorder set total_dyeing = %s where production_id = %s and workcenter_id = 5
                    """
                self.env.cr.execute(sql_query, (data.total_receipt,data.production_id.id,))

        x=1
        return res