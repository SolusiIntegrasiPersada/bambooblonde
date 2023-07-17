# -*- coding: utf-8 -*-
{
    "name": "sol_bb_product",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "15.1.0.0.2",
    'license': "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": ["base", "product", "stock"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/product_views.xml",
        "views/product_category_views.xml",
        "views/brand_views.xml",
        "views/class_views.xml",
        "views/collections_views.xml",
        "views/stock_type_views.xml",
        "views/product_attribute_views.xml",
    ],
}
