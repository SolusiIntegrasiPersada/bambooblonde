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
    "version": "0.1",
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
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
