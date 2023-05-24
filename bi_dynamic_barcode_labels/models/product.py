# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

BARCODE_PREFIX = "21"
EAN13_LENGTH = 13
PRODUCT_REF_LENGTH = 5
BARCODE_AMOUNT_PLACES = 5
BARCODE_TEMPLATE = "%s%s%s%s"

class Product(models.Model):
    _inherit = "product.product"
    
    def barcode_with_qty(self, product_qty):
        _logger.info(f"original product barcode is {self.barcode}")
        
        if len(str(self.barcode)) == EAN13_LENGTH and self.barcode.startswith(BARCODE_PREFIX):
            reference = str(self.barcode[2:7])
            qty = str(int(product_qty))
            qty_decimal = str(product_qty).split(".")[1]
     
            barcode_config = self.env.ref('bi_dynamic_barcode_labels.barcode_labels_config_data')
            decimal_places = barcode_config.barcode_decimal_places
            whole_places = BARCODE_AMOUNT_PLACES - decimal_places
            
            barcode = BARCODE_TEMPLATE % (BARCODE_PREFIX, 
                                          reference.zfill(PRODUCT_REF_LENGTH), 
                                          qty.zfill(whole_places), 
                                          qty_decimal.ljust(decimal_places, '0'))
            checksum = self.env['barcode.nomenclature'].ean_checksum(barcode + "0")
            _logger.info(f"EAN check calculated as {checksum} for barcode {barcode} ")
            return barcode + str(checksum)
        else:
            _logger.info(f"barcode not starts with the provided prefix {BARCODE_PREFIX}")

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cost_code = fields.Char(compute='_compute_cost_code', string='Cost Code')
    
    @api.depends('standard_price')
    def _compute_cost_code(self):
        for product in self:
            master_code = {
                "1" : "S",
                "2" : "T",
                "3" : "O",
                "4" : "C",
                "5" : "K",
                "6" : "B",
                "7" : "U",
                "8" : "Y",
                "9" : "E",
                "0" : "R"
                }
            code = ''
            if product.standard_price:
                string_cost = str(product.standard_price)
                for i in string_cost[:-5]:
                    code += master_code[i]
                product.cost_code = code
            else:
                product.cost_code = None