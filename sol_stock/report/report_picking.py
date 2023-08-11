from odoo import fields, api, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def consolidate_lines(self):
        consolidated_lines = {}
        # size = ''
        column = []
        # column_a = ['A','B','C','D','E','F','G','H','I']
        column_b = ['6','7','32','33','11-12','A','XXS','XS/S','15']
        column_c = ['8','9','34','35','12-13','B','XS','S/M','16']
        column_d = ['10','11','36','37','13-14','C','XSS','M/L','17']
        column_e = ['12','38','39','14-15','D','S','L/XL','18']
        column_f = ['14','40','41','15-16','M']
        column_g = ['4','42','43','37-38','L']
        column_h = ['38-39','XL']
        column_i = ['OS','ALL']

        for line in self.move_ids_without_package:
            name = line.product_id.name
            colour = line.colour.strip()
            size = line.size.strip()

            key = (name, colour)
            if key in consolidated_lines:
                consolidated_lines[key].append(size)
            else:
                consolidated_lines[key] = [size]

        consolidated_data = []
        for (name, colour), sizes in consolidated_lines.items():
            # amount_a = sum(1 for size in sizes if size in column0)
            # if any(item in consolidated_lines.items() for item in column):
            amount_b = sum(1 for size in sizes if size in column_b) or ' '
            amount_c = sum(1 for size in sizes if size in column_c) or ' '
            amount_d = sum(1 for size in sizes if size in column_d) or ' '
            amount_e = sum(1 for size in sizes if size in column_e) or ' '
            amount_f = sum(1 for size in sizes if size in column_f) or ' '
            amount_g = sum(1 for size in sizes if size in column_g) or ' '
            amount_h = sum(1 for size in sizes if size in column_h) or ' '
            amount_i = sum(1 for size in sizes if size in column_i) or ' '
            amount_total = amount_i + amount_g + amount_h + amount_f + amount_e + amount_d + amount_b

            # print(f"Sizes: {sizes}")
            # print(f"Amounts: B={amount_b}, C={amount_c}, D={amount_d}, E={amount_e}, F={amount_f}, G={amount_g}, H={amount_h}, I={amount_i}")
            # print(f"Total: {amount_total}")

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
                'amount_total': amount_total,
            })
        return consolidated_data



class StockMove(models.Model):
    _inherit = 'stock.move'

    count_product = fields.Integer(string="Quantity")

