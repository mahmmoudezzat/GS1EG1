# -*- coding: utf-8 -*-
# from odoo import http


# class ChangeMobileFormat(http.Controller):
#     @http.route('/change_mobile_format/change_mobile_format', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/change_mobile_format/change_mobile_format/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('change_mobile_format.listing', {
#             'root': '/change_mobile_format/change_mobile_format',
#             'objects': http.request.env['change_mobile_format.change_mobile_format'].search([]),
#         })

#     @http.route('/change_mobile_format/change_mobile_format/objects/<model("change_mobile_format.change_mobile_format"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('change_mobile_format.object', {
#             'object': obj
#         })
