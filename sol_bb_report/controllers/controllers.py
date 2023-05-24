# -*- coding: utf-8 -*-
# from odoo import http


# class SolBbReport(http.Controller):
#     @http.route('/sol_bb_report/sol_bb_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sol_bb_report/sol_bb_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sol_bb_report.listing', {
#             'root': '/sol_bb_report/sol_bb_report',
#             'objects': http.request.env['sol_bb_report.sol_bb_report'].search([]),
#         })

#     @http.route('/sol_bb_report/sol_bb_report/objects/<model("sol_bb_report.sol_bb_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sol_bb_report.object', {
#             'object': obj
#         })
