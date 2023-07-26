# -*- coding: utf-8 -*-
{
    'name': 'sol_bb_product',
    'summary': '''Custom module for BambooBlonde's Product Hierarchy''',
    'description': '''''',
    'author': 'Solusi Integrasi Persada',
    'website': 'https://solinda.co.id/',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.1.0.0.4',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'stock', 'account_taxcloud'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/brand_views.xml',
        'views/class_views.xml',
        'views/collections_views.xml',
        'views/main_color_views.xml',
        'views/size_label_views.xml',
        'views/stock_type_views.xml',
        'views/product_attribute_views.xml',
        'views/product_category_views.xml',
        'views/product_template_views.xml',
        'views/product_views.xml',
        'views/menu_items.xml',
    ],
}
