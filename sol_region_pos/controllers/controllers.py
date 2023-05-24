# -*- coding: utf-8 -*-
# from odoo import http


# class SolRegionPos(http.Controller):
#     @http.route('/sol_region_pos/sol_region_pos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sol_region_pos/sol_region_pos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sol_region_pos.listing', {
#             'root': '/sol_region_pos/sol_region_pos',
#             'objects': http.request.env['sol_region_pos.sol_region_pos'].search([]),
#         })

#     @http.route('/sol_region_pos/sol_region_pos/objects/<model("sol_region_pos.sol_region_pos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sol_region_pos.object', {
#             'object': obj
#         })
