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


class StockMove(models.Model):
    _inherit = 'stock.move'

    count_product = fields.Integer(string="Quantity")

