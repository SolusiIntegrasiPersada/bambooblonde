# -*- coding: utf-8 -*-
{
    'name': "Cashflow Report",

    'summary': """
        Cashflow Report""",

    'description': """
        Cashflow Report
    """,

    'author': "Luthfi A.Nizar - 08998046065",
    'website': "http://https://www.linkedin.com/in/luthfi-nizar-388a89195/",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'account','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'reports/action.xml',
        'views/views.xml',
    ],
}
