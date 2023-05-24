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
    "website": "http://",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "account"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "security/security.xml",
        "views/account_move.xml",
        "views/templates.xml",
        "views/journal_views.xml",
        "views/account_payment_views.xml",
        "report/action_report.xml",
        "report/report_invoice_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
