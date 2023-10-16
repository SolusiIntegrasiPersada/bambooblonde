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
    'category': 'Customizations',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': [
            'base',
            'mrp',
            'solinda_manufacture',
                ],

    # always loaded
    'data': [
        'views/stock.picking.xml',
    ],
}