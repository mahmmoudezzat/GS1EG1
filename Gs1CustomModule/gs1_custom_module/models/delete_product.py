from odoo import models, fields, api, _
from odoo.exceptions import UserError
class delete_produc(models.Model):
 _inherit = 'crm.lead'
 def write(self, vals):
   if len(self.user_id.ids)>1:
          return super(delete_produc, self.sudo()).write(vals)
   elif len(self.source_id.ids)>1:
     return super(delete_produc, self.sudo()).write(vals)

   SalesPersonUserId = self.env['crm.team.member'].search(["&", ["user_id.name", '=', self.env.user.name], ["crm_team_id.name", '!=', "Team Contracts"]],limit=1)
   if str(SalesPersonUserId.id) != "False":
        lis=[]
        for x in vals:
          lis.append(x)
        if 'x_studio_product_list' in lis:
            if len(vals['x_studio_product_list'][0][2]) < len(self.sudo().x_studio_product_list.ids):
                   raise UserError(_("you cannot delete "))
        return super(delete_produc, self.sudo()).write(vals)
   return super(delete_produc, self.sudo()).write(vals)


                
    
