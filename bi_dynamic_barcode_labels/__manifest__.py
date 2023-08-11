# -*- coding: utf-8 -*-
{
    "name": "Barcode Labels All",
    "category": "Sales",
    'summary': 'All in one Barcode Labels Product Template barcode label for product barcode label for sale barcode label for purchase barcode label for picking barcode label print Dynamic Barcode Label print product labels print label from sales order print barcode label',
    "description": """
                """,
    "author": "BrowseInfo",
    "website": "https://www.tradetec.info",
    "depends": ['base', 'web', 'sale_management', 'stock', 'purchase'],
    "data": [
        'security/ir.model.access.csv',
        'data/barcode_config_data.xml',
        'views/barcode_config_views.xml',
        'views/product_views.xml',
        'report/report_barcode_product_labels_temp.xml',
        'report/report_barcode_product_temp_labels.xml',
        'report/report_barcode_sale_labels.xml',
        # 'report/report_barcode_purchase_labels.xml',
        # 'report/report_barcode_stock_labels.xml',
        'report/report.xml',
        'wizard/barcode_product_labels_view.xml',
        'wizard/barcode_product_temp_labels_view.xml',
        'wizard/barcode_sales_labels_view.xml',
        # 'wizard/barcode_purchase_labels_view.xml',
        # 'wizard/barcode_stock_labels_view.xml',
    ],
    "auto_install": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
