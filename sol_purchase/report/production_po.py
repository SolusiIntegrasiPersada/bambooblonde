from odoo import fields, api, models
#
# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
#
#     def consolidate_lines(self):
#         consolidated_lines = {}
#         column = []
#         # column_a = ['A','B','C','D','E','F','G','H','I']
#         column_b = ['6','7','32','33','11-12','A','XXS','XS/S','15']
#         column_c = ['8','9','34','35','12-13','B','XS','S/M','16']
#         column_d = ['10','11','36','37','13-14','C','XSS','M/L','17']
#         column_e = ['12','38','39','14-15','D','S','L/XL','18']
#         column_f = ['14','40','41','15-16','M']
#         column_g = ['4','42','43','37-38','L']
#         column_h = ['38-39','XL']
#         column_i = ['OS','ALL']
#
#         grand_total_amount = 0
#         grand_total_retail = 0
#
#         for line in self.move_ids_without_package:
#             name = line.product_id.name
#             # colour = line.colour.strip()
#             # size = line.size.strip()
#             retail = line.product_id.lst_price
#             code = line.product_id.default_code
#
#             key = (name, colour)
#             if key in consolidated_lines:
#                 consolidated_lines[key].append(size)
#             else:
#                 consolidated_lines[key] = [size]
#
#         consolidated_data = []
#         for (category), sizes in consolidated_lines.items():
#             # for (name, colour), sizes in sub_lines.items():
#             # amount_a = sum(1 for size in sizes if size in column0)
#             # if any(item in consolidated_lines.items() for item in column):
#             amounts = {
#                 'amount_b': sum(1 for size in sizes if size in column_b),
#                 'amount_c': sum(1 for size in sizes if size in column_c),
#                 'amount_d': sum(1 for size in sizes if size in column_d),
#                 'amount_e': sum(1 for size in sizes if size in column_e),
#                 'amount_f': sum(1 for size in sizes if size in column_f),
#                 'amount_g': sum(1 for size in sizes if size in column_g),
#                 'amount_h': sum(1 for size in sizes if size in column_h),
#                 'amount_i': sum(1 for size in sizes if size in column_i),
#             }
#             amount_total = sum(amount for amount in amounts.values() if amount is not None)
#             tot_b += amounts['amount_b']
#             tot_c += amounts['amount_c']
#             tot_d += amounts['amount_d']
#             tot_e += amounts['amount_e']
#             tot_f += amounts['amount_f']
#             tot_g += amounts['amount_g']
#             tot_h += amounts['amount_h']
#             tot_i += amounts['amount_i']
#             grand_total_amount += amount_total
#             grand_total_retail += retail
#
#             # name, colour, category = key
#             # model = model_key
#
#             consolidated_data.append({
#                 'name': name,
#                 'colour': colour,
#                 # 'amount_a': amount_a,
#                 'amount_b': amounts['amount_b'],
#                 'amount_c': amounts['amount_c'],
#                 'amount_d': amounts['amount_d'],
#                 'amount_e': amounts['amount_e'],
#                 'amount_f': amounts['amount_f'],
#                 'amount_g': amounts['amount_g'],
#                 'amount_h': amounts['amount_h'],
#                 'amount_i': amounts['amount_i'],
#                 'amount_total': amount_total,
#                 'grand_total_amount': grand_total_amount,
#                 'grand_total_retail': grand_total_retail,
#                 'retail': retail,
#                 'code': code,
#             })
#         return consolidated_data