from odoo import fields, api, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def consolidate_lines(self):
        consolidated_lines = {}
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
            retail = line.product_id.lst_price
            code = line.product_id.default_code
            model_rec = self.env['product.category'].search([
                '&', ('category_product', '=', 'department'),
                ('id', 'parent_of', line.product_id.categ_id.id)
            ]).mapped('name')
            category_rec = self.env['product.category'].search([
                '&', ('category_product', '=', 'category'),
                ('id', 'parent_of', line.product_id.categ_id.id)
            ]).mapped('name')
            model = ''.join(model_rec)
            category = ''.join(category_rec)

            key = (name, colour, model, category)
            if key in consolidated_lines:
                consolidated_lines[key].append(size)
            else:
                consolidated_lines[key] = [size]

        consolidated_data = []
        for (name, colour, model, category), sizes in consolidated_lines.items():
            # amount_a = sum(1 for size in sizes if size in column0)
            # if any(item in consolidated_lines.items() for item in column):
            amounts = {
                'amount_b': sum(1 for size in sizes if size in column_b) or None,
                'amount_c': sum(1 for size in sizes if size in column_c) or None,
                'amount_d': sum(1 for size in sizes if size in column_d) or None,
                'amount_e': sum(1 for size in sizes if size in column_e) or None,
                'amount_f': sum(1 for size in sizes if size in column_f) or None,
                'amount_g': sum(1 for size in sizes if size in column_g) or None,
                'amount_h': sum(1 for size in sizes if size in column_h) or None,
                'amount_i': sum(1 for size in sizes if size in column_i) or None,
            }
            amount_total = sum(amount for amount in amounts.values() if amount is not None)

            consolidated_data.append({
                'name': name,
                'colour': colour,
                'model': model,
                'category': category,
                # 'amount_a': amount_a,
                'amount_b': amounts['amount_b'],
                'amount_c': amounts['amount_c'],
                'amount_d': amounts['amount_d'],
                'amount_e': amounts['amount_e'],
                'amount_f': amounts['amount_f'],
                'amount_g': amounts['amount_g'],
                'amount_h': amounts['amount_h'],
                'amount_i': amounts['amount_i'],
                'amount_total': amount_total,
                'retail': retail,
                'code': code,
            })
        return consolidated_data



class StockMove(models.Model):
    _inherit = 'stock.move'

    count_product = fields.Integer(string="Quantity")

