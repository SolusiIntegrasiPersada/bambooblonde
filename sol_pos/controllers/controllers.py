# -*- coding: utf-8 -*-
# from odoo import http


# class SolPos(http.Controller):
#     @http.route('/sol_pos/sol_pos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sol_pos/sol_pos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sol_pos.listing', {
#             'root': '/sol_pos/sol_pos',
#             'objects': http.request.env['sol_pos.sol_pos'].search([]),
#         })

#     @http.route('/sol_pos/sol_pos/objects/<model("sol_pos.sol_pos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sol_pos.object', {
#             'object': obj
#         })
