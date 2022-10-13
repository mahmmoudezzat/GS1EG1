# -*- coding: utf-8 -*-
# from odoo import http


# class Gs1CustomModule(http.Controller):
#     @http.route('/gs1_custom_module/gs1_custom_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gs1_custom_module/gs1_custom_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gs1_custom_module.listing', {
#             'root': '/gs1_custom_module/gs1_custom_module',
#             'objects': http.request.env['gs1_custom_module.gs1_custom_module'].search([]),
#         })

#     @http.route('/gs1_custom_module/gs1_custom_module/objects/<model("gs1_custom_module.gs1_custom_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gs1_custom_module.object', {
#             'object': obj
#         })
