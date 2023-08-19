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
        price_tot = 0
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
                consolidated_lines[key]['qtyy'].append(qty)
            else:
                consolidated_lines[key] = {
                    'sizes': [size],
                    'fabric': fabric,
                    'lining': lining,
                    'qtyy': [qty],
                    'price': price
                }

        consolidated_data = []
        for (name, colour), item_data in consolidated_lines.items():
            sizes = item_data['sizes']
            qtyy = item_data['qtyy']
            price = item_data['price']
            item_type = None

            # Determine item_type based on matching types
            if all(size in type_a for size in sizes):
                item_type = 'A'
            elif all(size in type_b for size in sizes):
                item_type = 'B'
            elif all(size in type_c for size in sizes):
                item_type = 'C'
            elif all(size in type_d for size in sizes):
                item_type = 'D'
            elif all(size in type_e for size in sizes):
                item_type = 'E'
            elif all(size in type_f for size in sizes):
                item_type = 'F'
            elif all(size in type_g for size in sizes):
                item_type = 'G'
            elif all(size in type_h for size in sizes):
                item_type = 'H'
            elif all(size in type_i for size in sizes):
                item_type = 'I'
            else:
                item_type = None

            amounts = {
                'amount_b': sum(qty for size, qty in zip(sizes, qtyy) if size in column_b) or None,
                'amount_c': sum(qty for size, qty in zip(sizes, qtyy) if size in column_c) or None,
                'amount_d': sum(qty for size, qty in zip(sizes, qtyy) if size in column_d) or None,
                'amount_e': sum(qty for size, qty in zip(sizes, qtyy) if size in column_e) or None,
                'amount_f': sum(qty for size, qty in zip(sizes, qtyy) if size in column_f) or None,
                'amount_g': sum(qty for size, qty in zip(sizes, qtyy) if size in column_g) or None,
                'amount_h': sum(qty for size, qty in zip(sizes, qtyy) if size in column_h) or None,
                'amount_i': sum(qty for size, qty in zip(sizes, qtyy) if size in column_i) or None,
            }
            amount_total = sum(amount for amount in amounts.values() if amount is not None)
            total = amount_total * price

            consolidated_data.append({
                'name': name,
                'colour': colour,
                'fabric': item_data['fabric'],
                'lining': item_data['lining'],
                'sizes': sizes,
                'qty': qtyy,
                'price': price,
                'item_type': item_type,
                'amount_b': amounts['amount_b'],
                'amount_c': amounts['amount_c'],
                'amount_d': amounts['amount_d'],
                'amount_e': amounts['amount_e'],
                'amount_f': amounts['amount_f'],
                'amount_g': amounts['amount_g'],
                'amount_h': amounts['amount_h'],
                'amount_i': amounts['amount_i'],
                'amount_total': amount_total,
                'total': total,
            })


        return consolidated_data

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

