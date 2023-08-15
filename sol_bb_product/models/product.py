from odoo import fields, api, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    order_notes = fields.Html(string="Order Notes")
    collection_product = fields.Many2one("product.collections", string="Collection")
    launch_date = fields.Date(string="Launch Date")
    class_product = fields.Many2one("class.product", string="Class")
    consumption = fields.Float(string="Consumption")
    fabric_width = fields.Float(string="Fabric Width")
    category = fields.Char(related="categ_id.name", string="Category")
    is_print = fields.Boolean(string="Print", default=False)
    main_color_id = fields.Many2one('main.color', string="Main Color")
    product_template_variant_value_ids = fields.Many2many('product.template.attribute.value',
                                                          relation='product_variant_combination',
                                                          domain=[('attribute_line_id.value_count', '>', 0)],
                                                          string="Variant Values", ondelete='restrict')
    internal_location = fields.One2many('stock.quantity', 'product_id', compute='get_product_qty')

    def get_product_qty(self):
        location_list = []
        product_list = []
        obj_location = self.env['stock.location'].search([('usage', '=', 'internal')])
        for i in obj_location:
            location_list.append(i.id)
        obj_quant = self.env['stock.quant'].search([('product_id', '=', self.id),
                                                    ('location_id', 'in', location_list)])
        for obj in obj_quant:
            move_line = {'product_id': obj.product_id.id,
                         'stock_location': obj.location_id.id,
                         'qty_on_hand': obj.available_quantity,
                         }
            product_list.append(move_line)
        for i in product_list:
            if i['qty_on_hand'] > 0:
                self.internal_location |= self.env['stock.quantity'].create(i)

class InternalLocation(models.Model):
    _name = 'stock.quantity'

    stock_location = fields.Many2one('stock.location', string='Location Name')
    qty_on_hand = fields.Float('On Hand')
    forecast = fields.Float('Forecast')
    incoming_qty = fields.Float('Incoming Quantity')
    outgoing_qty = fields.Float('Outgoing Quantity')
    product_id = fields.Many2one('product.product', string='Product')
class ProductCollections(models.Model):
    _name = "product.collections"
    _description = "Product Collections"

    name = fields.Char(string="Name")


class ClassProduct(models.Model):
    _name = "class.product"
    _description = "Class"

    name = fields.Char(string="Class")
