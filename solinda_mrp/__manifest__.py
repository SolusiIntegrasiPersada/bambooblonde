# -*- coding: utf-8 -*-
{
    'name': "solinda_mrp",

    'summary': """Custom MRP Manufacture for BambooBlonde""",

    'description': """""",

    'author': "Solusi Integrasi Persada",
    'website': "http://www.solinda.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    "version": "1.0",
    'license': "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'purchase_stock', 'sol_purchase', 'sale', 'purchase', 'sol_bb_report', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        "views/sequence_data.xml",
        'views/menu_items.xml',
        'views/mrp_routing_views.xml',
        'views/mrp_bom_views.xml',
        'views/tender_bom.xml',
        'views/mrp_workcenter_views.xml',
        'views/stock_move_views.xml',
        'report/action_report.xml',
        'report/costing_product.xml',
        'report/costing_sample.xml',
        'wizard/production_report_views.xml',
        'wizard/sewing_report_views.xml',

    ],
}
