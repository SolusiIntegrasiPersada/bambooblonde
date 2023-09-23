# -*- coding: utf-8 -*-
{
    "name": "sol_account",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "Solusi Integrasi Persada",
    "website": "http://solinda.co.id",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "1.0",
    'license': "LGPL-3",

    # any module necessary for this one to work correctly
    "depends": ["base", "account","sale"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "security/security.xml",
        "views/account_move.xml",
        "views/account_move_line.xml",
        "views/journal_views.xml",
        "views/res_partner_views.xml",
        "views/account_payment_views.xml",
        "report/action_report.xml",
        "report/report_invoice_views.xml",
    ],
}
