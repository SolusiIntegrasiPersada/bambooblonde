# -*- coding: utf-8 -*-
{
    'name': "sol_region_pos",

    'summary': """
        add region field in POS""",

    'description': """
        additional region field in POS
    """,

    'author': "Luthfi A. Nizar - 08998046065",
    'website': "http://https://www.linkedin.com/in/luthfi-nizar-388a89195/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    "version": "15.1.0.0.1",
    'license': "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base', 'web' ,'point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application': True,
    'assets':{
        'point_of_sale.assets': [
            '/sol_region_pos/static/src/js/RegionControlButton.js',
            '/sol_region_pos/static/src/js/RegionList.js',
            '/sol_region_pos/static/src/js/RegionListScreen.js',
        ],
        'web.assets_qweb': [
            '/sol_region_pos/static/src/xml/RegionControlButton.xml',
            '/sol_region_pos/static/src/xml/RegionList.xml',
            '/sol_region_pos/static/src/xml/RegionListScreen.xml',
        ]
    }
}
