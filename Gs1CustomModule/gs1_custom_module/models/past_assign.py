 # -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class produc_oppr(models.Model):
 _inherit = 'crm.lead'
 SalesPersonList = fields.Many2many('crm.team.member',string="Past Assinees",store=True,readonly=True)
 def write(self, vals):
        if len(self.user_id.ids)>1:
          return super(produc_oppr, self.sudo()).write(vals)
        elif len(self.source_id.ids)>1:
          return super(produc_oppr, self.sudo()).write(vals)

        if self.user_id.id:
            SalesPersonUserId = self.sudo().env['crm.team.member'].search(['&',('user_id', '=', self.user_id.id),('crm_team_id.name', '!=', 'Team Contracts')])
            if SalesPersonUserId.id:
                if self.user_id:
                    x = self.SalesPersonList.ids
                    x.append(SalesPersonUserId.id)
                    vals['SalesPersonList']=x
        return super(produc_oppr, self.sudo()).write(vals)