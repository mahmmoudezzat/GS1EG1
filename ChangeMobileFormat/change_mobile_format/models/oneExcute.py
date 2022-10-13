from odoo import models, fields, api, _
import re
class one_Excute_phone(models.Model):
 _inherit = 'crm.lead'


 @api.onchange('user_id')
 def one_excute(self):
     all_opportunity=self.sudo().env['crm.lead'].search(['&',"|",["active","=",True],["active","=",False],["mobile","!=",False]])
     for x in  all_opportunity:
        old_phone_number=x.mobile      
        new_number = self.sudo().Phone_Format(old_phone_number)
        x.sudo().write({'mobile':new_number,'x_studio_orignal_mobile':old_phone_number})
 def Phone_Format(self, phone_number):
            x = str(re.sub('[^0-9]+', '', phone_number))
            index = phone_number.find('/')
            if index != -1 and index != 0 and index != 1:
                phone_number = phone_number[:index + 1]
            clean_phone_number = re.sub('[^0-9]+', '', phone_number)
            if len(clean_phone_number) < 10:
                if (clean_phone_number[0] == '+' and int(clean_phone_number[1]) == 2) or (
                        int(clean_phone_number[0]) == 0 and int(clean_phone_number[1]) == 1) or (
                        int(clean_phone_number[0]) == 0 and int(clean_phone_number[1]) == 0 and int(
                    clean_phone_number[2]) == 1):
                    clean_phone_number = clean_phone_number[:11]
                else:
                    clean_phone_number = clean_phone_number[:15]
            
            if int(clean_phone_number[0]) == 0 and int(clean_phone_number[1]) == 0 and int(clean_phone_number[2]) == 1:
                tmp = list(clean_phone_number)
                tmp[0] = '+'
                clean_phone_number = "".join(tmp)
                return clean_phone_number
            elif int(clean_phone_number[0]) == 0 and int(clean_phone_number[1]) == 0:
                res_str = clean_phone_number[1:]
                tmp = list(res_str)
                tmp[0] = '+'
                clean_phone_number = "".join(tmp)
                return clean_phone_number
            elif int(clean_phone_number[0]) == 0:
                clean_phone_number = '+2' + clean_phone_number
                return clean_phone_number
            elif len(clean_phone_number) <= 10:
                clean_phone_number = '+20' + clean_phone_number
                return clean_phone_number
            else:
                clean_phone_number = '+' + clean_phone_number
                return clean_phone_number
            

