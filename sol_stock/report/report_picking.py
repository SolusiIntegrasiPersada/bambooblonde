from odoo import fields, api, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def consolidate_lines(self):
        consolidated_lines = {}
        model_category_dict = {}

        type_a = ['6', '8', '10', '12', '14', '4']
        type_b = ['7', '9', '11']
        type_c = ['32', '34', '36', '38', '40', '42']
        type_d = ['33', '35', '37', '39', '41', '43']
        type_e = ['11-12', '12-13', '13-14', '14-15', '15-16', '37-38', '38-39']
        type_f = ['A', 'B', 'C', 'D']
        type_g = ['XXS', 'XS', 'XSS', 'S', 'M', 'L', 'XL', 'OS']
        type_h = ['XS/S', 'S/M', 'M/L', 'L/XL', 'ALL']
        type_i = ['15', '16', '17', '18']

        column_b = ['6','7','32','33','11-12','A','XXS','XS/S','15']
        column_c = ['8','9','34','35','12-13','B','XS','S/M','16']
        column_d = ['10','11','36','37','13-14','C','XSS','M/L','17']
        column_e = ['12','38','39','14-15','D','S','L/XL','18']
        column_f = ['14','40','41','15-16','M']
        column_g = ['4','42','43','37-38','L']
        column_h = ['38-39','XL']
        column_i = ['OS','ALL']

        tot_b = 0
        tot_c = 0
        tot_d = 0
        tot_e = 0
        tot_f = 0
        tot_g = 0
        tot_h = 0
        tot_i = 0

        total_qty = 0
        total_retail = 0
        total_price = 0
        for line in self.move_ids_without_package:
            name = line.product_id.name
            colour = line.colour.strip()
            size = line.size.strip()
            retail = line.product_id.lst_price
            price = line.product_id.standard_price
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
            qty = line.quantity_done
            price_receipt = line.price

            model_category_pair = (model, category)
            if model_category_pair not in model_category_dict:
                model_category_dict[model_category_pair] = True  # Mark the pair as processed

            key = (name, colour)
            if key in consolidated_lines:
                consolidated_lines[key]['sizes'].append(size)
                consolidated_lines[key]['qtyy'].append(qty)
            else:
                consolidated_lines[key] = {
                    'sizes': [size], 
                    'model': model,
                    'category': category,
                    'price': price,
                    'code': code,
                    'qtyy': [qty],
                    'price_receipt': price_receipt
                }
        category_list = []
        consolidated_data = []
        for (name, colour), type_data in consolidated_lines.items():

            sizes = type_data['sizes']
            model = type_data['model']
            category = type_data['category']
            item_type = None
            price = type_data['price']
            code = type_data['code']
            qtyy = type_data['qtyy']
            price_receipt = type_data['price_receipt']

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
                'amount_b': sum(1 for size in sizes if size in column_b),
                'amount_c': sum(1 for size in sizes if size in column_c),
                'amount_d': sum(1 for size in sizes if size in column_d),
                'amount_e': sum(1 for size in sizes if size in column_e),
                'amount_f': sum(1 for size in sizes if size in column_f),
                'amount_g': sum(1 for size in sizes if size in column_g),
                'amount_h': sum(1 for size in sizes if size in column_h),
                'amount_i': sum(1 for size in sizes if size in column_i),
            }

            amount_total = sum(amount for amount in amounts.values() if amount is not None)
            total_retail += retail

            amounts_receipt = {
                'amount_b': sum(qty for size, qty in zip(sizes, qtyy) if size in column_b),
                'amount_c': sum(qty for size, qty in zip(sizes, qtyy) if size in column_c),
                'amount_d': sum(qty for size, qty in zip(sizes, qtyy) if size in column_d),
                'amount_e': sum(qty for size, qty in zip(sizes, qtyy) if size in column_e),
                'amount_f': sum(qty for size, qty in zip(sizes, qtyy) if size in column_f),
                'amount_g': sum(qty for size, qty in zip(sizes, qtyy) if size in column_g),
                'amount_h': sum(qty for size, qty in zip(sizes, qtyy) if size in column_h),
                'amount_i': sum(qty for size, qty in zip(sizes, qtyy) if size in column_i),
            }

            amount_total_receipt = sum(amounts_receipt for amounts_receipt in amounts_receipt.values() if amounts_receipt is not None)
            total_receipt = amount_total_receipt * price_receipt

            tot_b += amounts['amount_b']
            tot_c += amounts['amount_c']
            tot_d += amounts['amount_d']
            tot_e += amounts['amount_e']
            tot_f += amounts['amount_f']
            tot_g += amounts['amount_g']
            tot_h += amounts['amount_h']
            tot_i += amounts['amount_i']
            total_qty = tot_b + tot_c + tot_d + tot_e + tot_f + tot_g + tot_h + tot_i

            # if model_category_pair in model_category_dict:
            consolidated_data.append({
                'name': name,
                'colour': colour,
                'model': model,
                'category': category,
                'item_type': item_type,
                'total_qty': total_qty,
                'qty': qtyy,
                'amount_b': amounts['amount_b'],
                'amount_c': amounts['amount_c'],
                'amount_d': amounts['amount_d'],
                'amount_e': amounts['amount_e'],
                'amount_f': amounts['amount_f'],
                'amount_g': amounts['amount_g'],
                'amount_h': amounts['amount_h'],
                'amount_i': amounts['amount_i'],
                'tot_b': tot_b,
                'tot_c': tot_c,
                'tot_d': tot_d,
                'tot_e': tot_e,
                'tot_f': tot_f,
                'tot_g': tot_g,
                'tot_h': tot_h,
                'tot_i': tot_i,
                'receipt_amount_b': amounts_receipt['amount_b'],
                'receipt_amount_c': amounts_receipt['amount_c'],
                'receipt_amount_d': amounts_receipt['amount_d'],
                'receipt_amount_e': amounts_receipt['amount_e'],
                'receipt_amount_f': amounts_receipt['amount_f'],
                'receipt_amount_g': amounts_receipt['amount_g'],
                'receipt_amount_h': amounts_receipt['amount_h'],
                'receipt_amount_i': amounts_receipt['amount_i'],
                'total_retail': total_retail,
                'amount_total': amount_total,
                'retail': retail,
                'price': price,
                'price_receipt': price_receipt,
                'code': code,
                'total_receipt': total_receipt,
                'amount_total_receipt': amount_total_receipt,
            })

        return consolidated_data


class StockMove(models.Model):
    _inherit = 'stock.move'

    count_product = fields.Integer(string="Quantity")

