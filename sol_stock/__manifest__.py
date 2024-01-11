# -*- coding: utf-8 -*-
{
    'name': "sol_stock",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Solusi Integrasi Persada",
    'website': "http://www.solinda.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    "version": "1.0",
    'license': "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sol_purchase', 'report_xlsx', 'product', 'solinda_manufacture','barcodes'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'security/security_stock.xml',
        'security/record_rule.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant.xml',
        'report/action_report.xml',
        'wizard/stock_per_store_wizard.xml',
        'views/stock_location.xml',
        'views/stock_move_line.xml',
        'views/res_users.xml',
        'report/report_internal.xml',
        'report/report_receipt.xml',
        'report/report_return.xml',
        'report/report_production.xml',
        'report/report_foc.xml',
        'report/report_receive_supp.xml',
    ],
}
