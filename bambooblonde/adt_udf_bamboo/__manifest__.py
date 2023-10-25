# -*- coding: utf-8 -*-
{
    'name': "ADT UDF BAMBOO",

    'summary': """
        ADT UDF BAMBOO """,

    'description': """
        STD UDF all module by Aditya
    """,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
            'base',
            'mrp',
            'solinda_manufacture',
            'stock',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}