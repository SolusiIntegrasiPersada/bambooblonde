# -*- coding: utf-8 -*-
{
    'name': 'sol_pos',

    'summary': '''Custom PoS module for BambooBlonde''',

    'description': '''
        Rework PoS workflow for requirement made by BambooBlonde
    ''',

    'author': 'Solusi Integrasi Persada',
    'website': 'http://www.solinda.co.id',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    "version": "15.1.0.0.14",
    'license': "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'pos_sale', 'pos_discount', 'product', 'report_xlsx'],

    # always loaded
    'data': [
        'data/receipt.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/stock_need_views.xml',
        'views/stock_comment_views.xml',
        'views/pos_config_views.xml',
        'views/point_of_sale_views.xml',
        'views/pos_receipt_views.xml',
        'views/pos_order_views.xml',
        'views/promotional_message_view.xml',
        'views/res_users_view.xml',
        'views/sequence_data.xml',
        'report/action_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sol_pos/static/src/js/field_utils.js',
        ],
        'web.assets_qweb': [
            'sol_pos/static/src/xml/pos_screen.xml',
        ],
        'point_of_sale.assets': [
            'sol_pos/static/src/js/GlobalLineDiscount.js',
            'sol_pos/static/src/js/OrderReceipt.js',
            'sol_pos/static/src/js/OrderWidget.js',
            'sol_pos/static/src/js/PaymentScreen.js',
            'sol_pos/static/src/js/models.js',
            'sol_pos/static/src/js/screens.js',
        ],
    },
}
