from odoo import fields, api, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_paid_amount(self):
        paid_amount = 0
        residual_amount = 0
        bill_data = []
        for rec in self:
            po = self.env['purchase.order'].search([
                ('product_mo', '=', rec.style_name),
                ('state', '=', 'purchase'),
                ('name', '=', rec.origin)
            ])
            if po:
                for invoice in po.invoice_ids.filtered(lambda x: x.state_bill == 'approve'):
                    paid_amount += invoice.amount_total - invoice.amount_residual
                    residual_amount += invoice.amount_residual

                bill_data.append({
                    'paid_amount': paid_amount,
                    'residual_amount': residual_amount,
                })

        return bill_data
    def internal_transfer(self):

        type_a = ['06', '08', '10', '12', '14', '04', '6', '8', '4']
        type_b = ['07', '09', '11', '7', '9']
        type_c = ['32', '34', '36', '38', '40', '42']
        type_d = ['33', '35', '37', '39', '41', '43']
        type_e = ['11-12', '12-13', '13-14', '14-15', '15-16', '37-38', '38-39']
        type_f = ['A', 'B', 'C', 'D']
        type_g = ['XXS', 'XS', 'XSS', 'S', 'M', 'L', 'XL', 'OS']
        type_h = ['XS/S', 'S/M', 'M/L', 'L/XL', 'ALL']
        type_i = ['15', '16', '17', '18']

        column_b = ['06','07','32','33','11-12','A','XXS','XS/S','15','6','7']
        column_c = ['08','09','34','35','12-13','B','XS','S/M','16','8','9']
        column_d = ['10','11','36','37','13-14','C','XSS','M/L','17']
        column_e = ['12','38','39','14-15','D','S','L/XL','18']
        column_f = ['14','40','41','15-16','M']
        column_g = ['04','42','43','37-38','L','4']
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

        consolidated_lines = {}

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

            if (model, category) not in consolidated_lines:
                consolidated_lines[(model, category)] = {
                    'names': {},
                    'model': model,
                    'category': category,
                }
            name_group = consolidated_lines[(model, category)]['names']

            # Group by (name, colour) within the (model, category) group
            if (name, colour) not in name_group:
                name_group[(name, colour)] = {
                    'colour': colour,
                    'name': name,
                    'sizes': [],
                    'price': price,
                    'price_receipt': price_receipt,
                    'code': code,
                    'retail': retail,
                    'qtyy': [],
                }

            size_group = name_group[(name, colour)]['sizes']
            qty_group = name_group[(name, colour)]['qtyy']

            # Append size to the (name, colour) group
            size_group.append(size)
            qty_group.append(qty)

        consolidated_data = []

        for (model, category), model_data in consolidated_lines.items():
            model = model_data['model']
            category = model_data['category']
            size_data = []

            # total qty dan total retail
            sub_total = []

            for (name, colour), type_data in model_data['names'].items():

                sizes = type_data['sizes']
                item_type = None
                price = type_data['price']
                code = type_data['code']
                retail = type_data['retail']
                qtyy = type_data['qtyy']

                # price_receipt = type_data['price_receipt']

                # Determine item_type based on matching types
                if all(sizes in type_a for sizes in sizes):
                    item_type = 'A'
                elif all(sizes in type_b for sizes in sizes):
                    item_type = 'B'
                elif all(sizes in type_c for sizes in sizes):
                    item_type = 'C'
                elif all(sizes in type_d for sizes in sizes):
                    item_type = 'D'
                elif all(sizes in type_e for sizes in sizes):
                    item_type = 'E'
                elif all(sizes in type_f for sizes in sizes):
                    item_type = 'F'
                elif all(sizes in type_g for sizes in sizes):
                    item_type = 'G'
                elif all(sizes in type_h for sizes in sizes):
                    item_type = 'H'
                elif all(sizes in type_i for sizes in sizes):
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
                total_price = amount_total * price

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
                amount_total_receipt = sum(
                    amounts_receipt for amounts_receipt in amounts_receipt.values() if amounts_receipt is not None)

                tot_b += amounts['amount_b']
                tot_c += amounts['amount_c']
                tot_d += amounts['amount_d']
                tot_e += amounts['amount_e']
                tot_f += amounts['amount_f']
                tot_g += amounts['amount_g']
                tot_h += amounts['amount_h']
                tot_i += amounts['amount_i']
                total_qty = tot_b + tot_c + tot_d + tot_e + tot_f + tot_g + tot_h + tot_i

                name_color_dict = ({
                    'name': name,
                    'colour': colour,
                    'item_type': item_type,
                    'model': model,
                    'category': category,
                    'qty': qtyy,
                    'amount_b': amounts['amount_b'],
                    'amount_c': amounts['amount_c'],
                    'amount_d': amounts['amount_d'],
                    'amount_e': amounts['amount_e'],
                    'amount_f': amounts['amount_f'],
                    'amount_g': amounts['amount_g'],
                    'amount_h': amounts['amount_h'],
                    'amount_i': amounts['amount_i'],
                    'receipt_amount_b': amounts_receipt['amount_b'],
                    'receipt_amount_c': amounts_receipt['amount_c'],
                    'receipt_amount_d': amounts_receipt['amount_d'],
                    'receipt_amount_e': amounts_receipt['amount_e'],
                    'receipt_amount_f': amounts_receipt['amount_f'],
                    'receipt_amount_g': amounts_receipt['amount_g'],
                    'receipt_amount_h': amounts_receipt['amount_h'],
                    'receipt_amount_i': amounts_receipt['amount_i'],
                    'tot_b': tot_b,
                    'tot_c': tot_c,
                    'tot_d': tot_d,
                    'tot_e': tot_e,
                    'tot_f': tot_f,
                    'tot_g': tot_g,
                    'tot_h': tot_h,
                    'tot_i': tot_i,
                    'total_price': total_price,
                    'amount_total': amount_total,
                    'retail': retail,
                    'price': price,
                    'price_receipt': price_receipt,
                    'code': code,
                    'amount_total_receipt': amount_total_receipt,
                })
                size_data.append(name_color_dict)
            consolidated_data.append({
                'model': model,
                'category': category,
                'name': size_data,
            })
        return consolidated_data
        # return


class StockMove(models.Model):
    _inherit = 'stock.move'

    count_product = fields.Integer(string="Quantity")

