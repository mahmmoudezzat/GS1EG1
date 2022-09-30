# -*- coding: utf-8 -*-
# from odoo import http


# class DuplicateOpportunities(http.Controller):
#     @http.route('/duplicate_opportunities/duplicate_opportunities', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/duplicate_opportunities/duplicate_opportunities/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('duplicate_opportunities.listing', {
#             'root': '/duplicate_opportunities/duplicate_opportunities',
#             'objects': http.request.env['duplicate_opportunities.duplicate_opportunities'].search([]),
#         })

#     @http.route('/duplicate_opportunities/duplicate_opportunities/objects/<model("duplicate_opportunities.duplicate_opportunities"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('duplicate_opportunities.object', {
#             'object': obj
#         })
