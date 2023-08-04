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
        # column0 = ['A','B','C','D','E','F','G','H','I']
        column1 = ['6','7','32','33','11-12','A','XXS','XS/S','15']
        column2 = ['8','9','34','35','12-13','B','XS','S/M','16']
        column3 = ['10','11','36','37','13-14','C','XSS','M/L','17']
        column4 = ['12','38','39','14-15','D','S','L/XL','18']
        column5 = ['14','40','41','15-16','M']
        column6 = ['4','42','43','37-38','L']
        column7 = ['38-39','XL']
        column8 = ['OS','ALL']


        for line in self.move_ids_without_package:
            name = line.product_id.name
            colour = line.colour
            size = line.size

            key = (name, colour)
            if key in consolidated_lines:
                consolidated_lines[key].append(size)
            else:
                consolidated_lines[key] = [size]

        consolidated_data = []
        for (name, colour), sizes in consolidated_lines.items():
            # amount_a = sum(1 for size in sizes if size in column0)
            amount_b = sum(1 for size in sizes if size in column1)
            amount_c = sum(1 for size in sizes if size in column2)
            amount_d = sum(1 for size in sizes if size in column3)
            amount_e = sum(1 for size in sizes if size in column4)
            amount_f = sum(1 for size in sizes if size in column5)
            amount_g = sum(1 for size in sizes if size in column6)
            amount_h = sum(1 for size in sizes if size in column7)
            amount_i = sum(1 for size in sizes if size in column8)

            consolidated_data.append({
                'name': name,
                'colour': colour,
                # 'amount_a': amount_a,
                'amount_b': amount_b,
                'amount_c': amount_c,
                'amount_d': amount_d,
                'amount_e': amount_e,
                'amount_f': amount_f,
                'amount_g': amount_g,
                'amount_h': amount_h,
                'amount_i': amount_i,
            })
        return consolidated_data


    def test_grouping(self):
        grouped_data = self.group_by_product_name()
        for group in grouped_data:
            print(group)

class StockMove(models.Model):
    _inherit = 'stock.move'

    count_product = fields.Integer(string="Quantity")

