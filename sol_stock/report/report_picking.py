from odoo import fields, api, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_rec(self):
        vals = {}
        for move in self.move_ids_without_package:
            if move.product_id.name in vals:
                vals[move.product_id.name] += move.product_uom_qty
            # else:
            #     vals.update({move.product_id.name: move.product_uom_qty})
        return vals

    def get_recs(self):
        data = {}
        for move in self.move_ids_without_package:
            product = move.product_id.name
            color = move.colour
            key = (product, color)
            if key in data:
                data[key].append(move)
            else:
                data[key] = [move]
        return data

    def get_last_rec(self):
        for rec in self:
            return rec.move_ids_without_package.sorted(lambda l: l.id, reverse=True)[0]

        # move_ids = self.env['stock.move'].sudo().search()
        # move_items = move_ids.mapped('move_ids_without_package')
        # list_move = []
        # print("Testing", self.read([0]))
        # data = {
        #     'form': self.read()[0],
        # }
        # return self.env.ref('sol_stock.action_report_picking_action').report_action(self, data=data)

    def consolidate_lines(self):
        consolidated_lines = {}
        for line in self.move_ids_without_package:
            name = line.product_id.name  # Assuming 'product_id' is the field holding the product name.
            amount = line.product_uom_qty  # Assuming 'product_uom_qty' is the field holding the quantity.
            if name in consolidated_lines:
                consolidated_lines[name] += amount
            else:
                consolidated_lines[name] = amount

        # Convert the dictionary into a list of dictionaries for QWeb
        return [{'name': name, 'amount': consolidated_lines[name]} for name in consolidated_lines]

    def test_grouping(self):
        grouped_data = self.group_by_product_name()
        for group in grouped_data:
            print(group)

class StockMove(models.Model):
    _inherit = 'stock.move'

    count_product = fields.Integer(string="Quantity")

