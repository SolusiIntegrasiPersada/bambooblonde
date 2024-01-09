from odoo import fields, api, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def get_last_record_order(self):
        for record in self:
            return record.order_line.sorted(lambda l: l.id, reverse=False)[0]
    def consolidate_lines(self):
        consolidated_lines = {}
        column = []
        # column_a = ['A','B','C','D','E','F','G','H','I']
        type_a = ['6', '8', '10', '12', '14', '4', '06', '08', '04']
        type_b = ['7', '9', '11', '07', '09']
        type_c = ['32', '34', '36', '38', '40', '42']
        type_d = ['33', '35', '37', '39', '41', '43']
        type_e = ['11-12', '12-13', '13-14', '14-15', '15-16', '37-38', '38-39']
        type_f = ['A', 'B', 'C', 'D']
        type_g = ['XXS', 'XS', 'XSS', 'S', 'M', 'L', 'XL', 'OS']
        type_h = ['XS/S', 'S/M', 'M/L', 'L/XL', 'ALL']
        type_i = ['15', '16','17', '18']

        column_b = ['6','7','32','33','11-12','A','XXS','XS/S','15','06','07']
        column_c = ['8','9','34','35','12-13','B','XS','S/M','16','08','09']
        column_d = ['10','11','36','37','13-14','C','XSS','M/L','17']
        column_e = ['12','38','39','14-15','D','S','L/XL','18']
        column_f = ['14','40','41','15-16','M','ALL']
        column_g = ['4','42','43','37-38','L','04']
        column_h = ['38-39','XL']
        column_i = ['OS']

        total = 0
        type = []
        price_tot = 0
        for line in self.order_line:
            if not line.display_type:
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
            size_column_b = None
            size_column_c = None
            size_column_d = None
            size_column_e = None
            size_column_f = None
            size_column_g = None
            size_column_h = None
            size_column_i = None

            # Determine item_type based on matching types
            if all(size in type_a for size in sizes):
                item_type = 'A'
                size_column_b = '6'
                size_column_c = '8'
                size_column_d = '10'
                size_column_e = '12'
                size_column_f = '14'
                size_column_g = '4'
                size_column_h = ''
                size_column_i = ''
            elif all(size in type_b for size in sizes):
                item_type = 'B'
                size_column_b = '7'
                size_column_c = '9'
                size_column_d = '11'
                size_column_e = ''
                size_column_f = ''
                size_column_g = ''
                size_column_h = ''
                size_column_i = ''
            elif all(size in type_c for size in sizes):
                item_type = 'C'
                size_column_b = '32'
                size_column_c = '34'
                size_column_d = '36'
                size_column_e = '38'
                size_column_f = '40'
                size_column_g = '42'
                size_column_h = ''
                size_column_i = ''
            elif all(size in type_d for size in sizes):
                item_type = 'D'
                size_column_b = '33'
                size_column_c = '35'
                size_column_d = '37'
                size_column_e = '39'
                size_column_f = '41'
                size_column_g = '43'
                size_column_h = ''
                size_column_i = ''
            elif all(size in type_e for size in sizes):
                item_type = 'E'
                size_column_b = '11-12'
                size_column_c = '12-13'
                size_column_d = '13-14'
                size_column_e = '14-15'
                size_column_f = '15-16'
                size_column_g = '37-38'
                size_column_h = '38-39'
                size_column_i = ''
            elif all(size in type_f for size in sizes):
                item_type = 'F'
                size_column_b = 'A'
                size_column_c = 'B'
                size_column_d = 'C'
                size_column_e = 'D'
                size_column_f = ''
                size_column_g = ''
                size_column_h = ''
                size_column_i = ''
            elif all(size in type_g for size in sizes):
                item_type = 'G'
                size_column_b = 'XXS'
                size_column_c = 'XS'
                size_column_d = 'XSS'
                size_column_e = 'S'
                size_column_f = 'M'
                size_column_g = 'L'
                size_column_h = 'XL'
                size_column_i = 'OS'
            elif all(size in type_h for size in sizes):
                item_type = 'H'
                size_column_b = 'XS/S'
                size_column_c = 'S/M'
                size_column_d = 'M/L'
                size_column_e = 'L/XL'
                size_column_f = 'ALL'
                size_column_g = ''
                size_column_h = ''
                size_column_i = ''
            elif all(size in type_i for size in sizes):
                item_type = 'I'
                size_column_b = '15'
                size_column_c = '16'
                size_column_d = '17'
                size_column_e = '18'
                size_column_f = '14'
                size_column_g = ''
                size_column_h = ''
                size_column_i = ''
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
                'size_column_b': size_column_b,
                'size_column_c': size_column_c,
                'size_column_d': size_column_d,
                'size_column_e': size_column_e,
                'size_column_f': size_column_f,
                'size_column_g': size_column_g,
                'size_column_h': size_column_h,
                'size_column_i': size_column_i,
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

