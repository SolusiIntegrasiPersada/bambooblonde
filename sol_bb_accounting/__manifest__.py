# -*- coding: utf-8 -*-
{
    'name': "sol_bb_accounting",

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
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'views/sequence_data.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            '/sol_bb_accounting/static/src/xml/account_payment.xml',
        ],
    }
}
