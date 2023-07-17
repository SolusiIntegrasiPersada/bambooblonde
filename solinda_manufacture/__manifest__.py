# -*- coding: utf-8 -*-
{
    'name': "solinda_manufacture",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Luthfi A.Nizar - 08998046065",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'purchase_stock','sol_purchase','solinda_mrp', 'sale', 'stock', 'quality_mrp',],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/purchase.xml',
        'views/purchase_request.xml',
        'views/stock_picking.xml',
        # 'views/purchase_order_view.xml',
        'views/company.xml',
        'views/mrp_breakdown.xml',
        'views/mrp_production.xml',
        'views/stock_move.xml',
        'views/mrp_workorder_views.xml',
        'report/action_report.xml',
        'report/production_detail.xml',
        'report/sample_detail.xml',
        'views/templates.xml',
    ],
}
