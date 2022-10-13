from odoo import fields, models ,api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

# x_studio_product_list is the technical name of the field product list to choose which product want to add to the opportunity and its relation manytomany with product.template located in crm opportunity view
# x_studio_product_weight is the technical name of the field weight to put a static weight to the product and it is integar field located in product.template form view 
# x_studio_salesperson_weight is the technical name of the field sales preson weight and its an integar field  located in crm.team.member form view 


class gs1_contact(models.Model):
 _inherit = 'crm.lead'
 def write(self, vals):
  if len(self.user_id.ids)>1:
          return super(gs1_contact, self.sudo()).write(vals)
  elif len(self.source_id.ids)>1:
          return super(gs1_contact, self.sudo()).write(vals)
  minProduct = []
  if self.env.context.get("lastcall"):
        
      weight=1
      lis = []
      for x in vals:
          lis.append(x)
      if self.sudo().x_studio_product_list and self.sudo().source_id.name == "Referrals" :
        weight=4
        for product in self.sudo().x_studio_product_list:
              weight += product.x_studio_product_weight
      elif self.sudo().x_studio_product_list:
        for product in self.sudo().x_studio_product_list:
           weight += product.x_studio_product_weight
      elif self.sudo().source_id.name == "Referrals" :
            weight=4                       
      minProduct = []
      team_lead = self.sudo().env['crm.team.member'].search(['&',('assignment_optout', '=', False), ('crm_team_id.name', '!=', 'Team Contracts')])
      for person in team_lead:
            if person.id not in self.sudo().SalesPersonList.ids:
                 minProduct.append(person.x_studio_salesperson_weight)
                 person.assignment_domain = []
      l = int(min(minProduct))
      new_saleperson = self.sudo().env['crm.team.member'].search(['&',('x_studio_salesperson_weight', '=', str(l)),('crm_team_id.name', '!=', 'Team Contracts')], limit=1)
      if 'team_id' in lis :
        vals['team_id']=new_saleperson.crm_team_id.id
      if 'user_id' in lis :
        vals['user_id']=new_saleperson.user_id.id
        new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight + weight)})
      return super(gs1_contact, self.sudo()).write(vals)
  else:
   weight=0
   changes=[]
   for i in vals:
      changes.append(i)
        
   if "source_id" in changes:
    x=self.sudo().env['utm.source'].search([('id','=',vals['source_id'])])
    if str(x.name) == "Referrals":
        if self.user_id and  "user_id" not in changes:
            last_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', self.sudo().user_id.id)])
            last_saleperson.sudo().write({'x_studio_salesperson_weight': int(last_saleperson.x_studio_salesperson_weight+3)})
    elif str(self.sudo().source_id.name) == "Referrals": 
            last_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', self.sudo().user_id.id)])
            last_saleperson.sudo().write({'x_studio_salesperson_weight': int(last_saleperson.x_studio_salesperson_weight-3)})

            
   if self.sudo().user_id and "user_id" in changes and "x_studio_product_list" in changes:
            last_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', self.sudo().user_id.id)])
            new_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', vals['user_id'])])

            if self.sudo().source_id.name == "Referrals":
                 last_saleperson.sudo().write({'x_studio_salesperson_weight': int(last_saleperson.x_studio_salesperson_weight-3)})
                 new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight+3)})
            if self.sudo().x_studio_product_list:
                 for product in self.sudo().x_studio_product_list:
                        weight += product.x_studio_product_weight
                 last_saleperson.sudo().write({'x_studio_salesperson_weight': int(last_saleperson.x_studio_salesperson_weight-weight)})
                 weight=0
                 for product in vals['x_studio_product_list'][0][2]:
                        product = self.sudo().env['product.template'].search([('id', '=', product)])
                        weight += product.x_studio_product_weight
                 new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight+weight)})
                 return  super(gs1_contact, self.sudo()).write(vals)

            else:
                 new_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', vals['user_id'])])
                 for product in vals['x_studio_product_list'][0][2]:
                        product = self.sudo().env['product.template'].search([('id', '=', product)])
                        weight += product.x_studio_product_weight
                 new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight+weight)})
                 return  super(gs1_contact, self.sudo()).write(vals)    
   elif self.sudo().user_id and "user_id" in changes and "x_studio_product_list" not in changes:
    last_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', self.sudo().user_id.id)])
    new_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', vals['user_id'])])
    if self.sudo().source_id.name == "Referrals":
                 last_saleperson.sudo().write({'x_studio_salesperson_weight': int(last_saleperson.x_studio_salesperson_weight-3)})
                 new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight+3)})
    if self.sudo().x_studio_product_list:
        for product in self.sudo().x_studio_product_list:
            weight += product.x_studio_product_weight
        last_saleperson.sudo().write({'x_studio_salesperson_weight': int(last_saleperson.x_studio_salesperson_weight-weight)})
        new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight+weight)})
        return  super(gs1_contact, self.sudo()).write(vals)
    else:
        return super(gs1_contact, self.sudo()).write(vals)
   elif "user_id" in changes:
      new_saleperson = self.env['crm.team.member'].search([('user_id.id', '=', vals['user_id'])])
      if self.sudo().source_id.name == "Referrals":
                 new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight+3)})
      if self.sudo().x_studio_product_list:
          for product in self.sudo().x_studio_product_list:
              weight += product.x_studio_product_weight
          new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight + weight)})
          return super(gs1_contact, self.sudo()).write(vals)
      else:
          return super(gs1_contact, self.sudo()).write(vals)
   elif "x_studio_product_list" in changes:
      if  self.user_id:
          for product in vals['x_studio_product_list'][0][2]:
              product = self.sudo().env['product.template'].search([('id', '=', product)])
              weight += product.x_studio_product_weight
          for product in self.sudo().x_studio_product_list.ids:
              product = self.sudo().env['product.template'].search([('id', '=', product)])
              weight -= product.x_studio_product_weight
          new_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', self.user_id.id)])
          new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight + weight)})
      return super(gs1_contact, self.sudo()).write(vals)
   else:
          return super(gs1_contact, self.sudo()).write(vals)
 @api.model
 def create(self, vals):
    if self.sudo().env.context.get('import_file') and self.sudo().env.context.get('tracking_disable'):
        return super(gs1_contact, self).create(vals)
    if vals['user_id'] and vals['source_id']:
      x=self.sudo().env['utm.source'].search([('id','=',vals['source_id'])])
      if str(x.name) == "Referrals":
        weight=3
        new_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', vals["user_id"])])
        new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight + weight)})

    if vals['user_id'] and vals['x_studio_product_list']:
     weight=0 

     for product in vals['x_studio_product_list'][0][2]:
        product = self.sudo().env['product.template'].search([('id', '=', product)])
        weight += product.x_studio_product_weight
        new_saleperson = self.sudo().env['crm.team.member'].search([('user_id.id', '=', vals["user_id"])])
        new_saleperson.sudo().write({'x_studio_salesperson_weight': int(new_saleperson.x_studio_salesperson_weight + weight)})
    return super(gs1_contact, self.sudo()).create(vals)
