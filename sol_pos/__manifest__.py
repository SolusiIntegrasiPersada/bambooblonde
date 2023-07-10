# -*- coding: utf-8 -*-
{
    'name': 'sol_pos',

    'summary': '''
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com''',

    'description': '''
        Long description of module's purpose
    ''',

    'author': 'My Company',
    'website': 'http://www.yourcompany.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1.0.9',

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
        'views/res_users_view.xml',
        'views/sequence_data.xml',
        'report/action_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sol_pos/static/src/js/field_utils.js',
        ],
        'point_of_sale.assets': [
            'sol_pos/static/src/js/GlobalLineDiscount.js',
            'sol_pos/static/src/js/product_screen.js',
            'sol_pos/static/src/js/order_receipt.js',
            'sol_pos/static/src/js/models.js',
        ],
        'web.assets_qweb': [
            'sol_pos/static/src/xml/pos.xml',
            'sol_pos/static/src/xml/pos_screen.xml',
        ],
    },
}
