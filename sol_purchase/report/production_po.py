from odoo import fields, api, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def consolidate_lines(self):
        consolidated_lines = {}
        column = []
        # column_a = ['A','B','C','D','E','F','G','H','I']
        type_a = ['6', '8', '10', '12', '14', '4']
        type_b = ['7', '9', '11']
        type_c = ['32', '34', '36', '38', '40', '42']
        type_d = ['33', '35', '37', '39', '41', '43']
        type_e = ['11-12', '12-13', '13-14', '14-15', '15-16', '37-38', '38-39']
        type_f = ['A', 'B', 'C', 'D']
        type_g = ['XXS', 'XS', 'XSS', 'S', 'M', 'L', 'XL', 'OS']
        type_h = ['XS/S', 'S/M', 'M/L', 'L/XL', 'ALL']
        type_i = ['15', '16','17', '18']

        column_b = ['6','7','32','33','11-12','A','XXS','XS/S','15']
        column_c = ['8','9','34','35','12-13','B','XS','S/M','16']
        column_d = ['10','11','36','37','13-14','C','XSS','M/L','17']
        column_e = ['12','38','39','14-15','D','S','L/XL','18']
        column_f = ['14','40','41','15-16','M']
        column_g = ['4','42','43','37-38','L']
        column_h = ['38-39','XL']
        column_i = ['OS','ALL']

        total = 0
        type = []
        # for line in self.order_line:
        #     name = line.product_id.name
        #     colour = line.colour.strip()
        #     size = line.size.strip()
        #     fabric = line.fabric_por.name
        #     lining = line.lining_por.name
        #     qty = line.product_qty
        #     price = line.price_unit
        #
        #
        #     key = (name, colour)
        #     if key in consolidated_lines:
        #         consolidated_lines[key].append(size)
        #     else:
        #         consolidated_lines[key] = [size]
        #
        # consolidated_data = []
        # for (name, colour), sizes in consolidated_lines.items():
        #     amounts = {
        #         'amount_b': sum(1 for size in sizes if size in column_b),
        #         'amount_c': sum(1 for size in sizes if size in column_c),
        #         'amount_d': sum(1 for size in sizes if size in column_d),
        #         'amount_e': sum(1 for size in sizes if size in column_e),
        #         'amount_f': sum(1 for size in sizes if size in column_f),
        #         'amount_g': sum(1 for size in sizes if size in column_g),
        #         'amount_h': sum(1 for size in sizes if size in column_h),
        #         'amount_i': sum(1 for size in sizes if size in column_i),
        #     }
        #     amount_total = sum(amount for amount in amounts.values() if amount is not None)
        #
        #
        #     consolidated_data.append({
        #         'name': name,
        #         'colour': colour,
        #         'fabric': fabric,
        #         'lining': lining,
        #         # 'amount_a': amount_a,
        #         'amount_b': amounts['amount_b'],
        #         'amount_c': amounts['amount_c'],
        #         'amount_d': amounts['amount_d'],
        #         'amount_e': amounts['amount_e'],
        #         'amount_f': amounts['amount_f'],
        #         'amount_g': amounts['amount_g'],
        #         'amount_h': amounts['amount_h'],
        #         'amount_i': amounts['amount_i'],
        #         'amount_total': amount_total,
        #
        #     })
        # return consolidated_data

        for line in self.order_line:
            name = line.product_id.name
            colour = line.colour.strip()
            size = line.size.strip()
            fabric = line.fabric_por.name
            lining = line.lining_por.name
            qty = line.product_qty
            price = line.price_unit

            key = (name, colour)
            if key in consolidated_lines:
                consolidated_lines[key]['sizes'].append(size)
            else:
                consolidated_lines[key] = {
                    'sizes': [size],
                    'fabric': fabric,
                    'lining': lining,
                    'qty': qty,
                    'price': price
                }

        consolidated_data = []
        for (name, colour), item_data in consolidated_lines.items():
            sizes = item_data['sizes']
            qty = item_data['qty']
            price = item_data['price']
            item_type = None

            # Check if the same name and color exist in column and type
            if name in column and colour in type:
                consolidated_lines[key]['sizes'].extend(sizes)
                item_type = type

            amount_total = qty * price

            consolidated_data.append({
                'name': name,
                'colour': colour,
                'fabric': item_data['fabric'],
                'lining': item_data['lining'],
                'sizes': sizes,
                'qty': qty,
                'price': price,
                'item_type': item_type,
                'amount_total': amount_total
            })

        return consolidated_data