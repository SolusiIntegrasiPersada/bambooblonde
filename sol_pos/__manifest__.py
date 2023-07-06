# -*- coding: utf-8 -*-
{
    'name': "sol_pos",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'product', 'report_xlsx'], 

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_need_views.xml',
        'views/stock_comment_views.xml',
        'views/pos_config_views.xml',
        'views/sequence_data.xml',
        'report/action_report.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'remove_decimal_zero_trailing/static/src/js/field_utils.js',
                ]
        },
}
