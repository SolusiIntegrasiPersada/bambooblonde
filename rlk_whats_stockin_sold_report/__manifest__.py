{
    "name"          : "What in Stock vs What is Sold",
    "version"       : "1.0",
    "author"        : "Ryan Linno K.",
    "website"       : "https://ryanlinnok.github.io",
    "category"      : "Reporting",
    "license"       : "LGPL-3",
    "support"       : "ryanlinnok@gmail.com",
    "summary"       : "Download report in excel format",
    "description"   : """
        What in Stock vs What is Sold Report
    """,
    "depends"       : [
        "sale_stock",
    ],
    "data"          : [
        "wizard/whats_stockin_sold_report.xml",
        "security/ir.model.access.csv",
    ],
    "demo"          : [],
    "test"          : [],
    "images"        : [],
    "qweb"          : [],
    "css"           : [],
    "application"   : True,
    "installable"   : True,
    "auto_install"  : False,
}