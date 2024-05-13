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
    "version": "15.0.1.1",
    'license': "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'pos_sale', 'pos_discount', 'product', 'report_xlsx', 'pos_coupon',
                'pos_settle_due', 'pos_loyalty', 'sol_bb_product', 'coupon', 'account'],

    # always loaded
    'data': [
        'data/receipt.xml',
        'data/receipt_ver2.xml',
        'report/action_report.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/account_journal.xml',
        'views/coupon_program_views.xml',
        'views/function_action.xml',
        'views/point_of_sale_region_views.xml',
        'views/point_of_sale_views.xml',
        'views/pos_config_views.xml',
        'views/pos_order_views.xml',
        'views/pos_receipt_views.xml',
        'views/product_template_views.xml',
        'views/promotional_message_view.xml',
        'views/res_partner.xml',
        'views/res_users_view.xml',
        'views/sequence_data.xml',
        'views/stock_comment_views.xml',
        'views/stock_need_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'sol_pos/static/src/js/OrderReceipt.js',
            'sol_pos/static/src/js/OrderWidget.js',
            'sol_pos/static/src/js/PaymentScreen.js',
            'sol_pos/static/src/js/RegionControlButton.js',
            'sol_pos/static/src/js/RegionList.js',
            'sol_pos/static/src/js/RegionListScreen.js',
            'sol_pos/static/src/js/models.js',
            'sol_pos/static/src/js/screens.js',
        ],
        'web.assets_backend': [
            'sol_pos/static/src/js/field_utils.js',
        ],
        'web.assets_qweb': [
            'sol_pos/static/src/xml/pos_screen.xml',
            'sol_pos/static/src/xml/RegionControlButton.xml',
            'sol_pos/static/src/xml/RegionList.xml',
            'sol_pos/static/src/xml/RegionListScreen.xml',
        ],
    },
}
