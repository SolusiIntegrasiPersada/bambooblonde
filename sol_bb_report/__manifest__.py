# -*- coding: utf-8 -*-
{
    'name': "sol_bb_report",

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
    "version": "15.1.0.0.1",
    'license': "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['report_xlsx', 'sol_purchase', 'sol_sale', 'sol_pos'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/templates.xml',
        'wizards/report_sample_development_view.xml',
        'wizards/report_bamboo_view.xml',
        'wizards/report_rekap_penjualan_view.xml',
        'wizards/report_sales_report_detail_view.xml',
        'wizards/report_supplier_sewing_report_view.xml',
        # 'wizards/report_best_seller_view.xml',
        # 'wizards/report_best_seller_store_view.xml',
        # 'wizards/report_best_seller_women_view.xml',
        'wizards/report_mens_clothes_view.xml',
        'wizards/report_rib_knit_jersey_dress_view.xml',
        'wizards/report_staples_style_view.xml',
        'wizards/report_best_seller_model_store_view.xml',
        'wizards/report_rcvd_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
