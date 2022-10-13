from email import message
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re
class neww(models.Model):
    _inherit = 'crm.lead'
    mobile_2 = fields.Char(string='Mobile 2')
    def _get_lead_duplicates(self, partner=None, email=None, include_lost=False):
        return self.env['crm.lead'].search([], limit=1)
    def merge_opportunity(self, user_id=False, team_id=False, auto_unlink=True):
        return self.env['crm.lead'].search([], limit=1)
    def write(self, vals):
        if self.sudo().env.context.get("module") and str(self.env.context.get("bin_size")) == "False":
            return super(neww, self.sudo()).write(vals)
        if len(self.user_id.ids)>1:
          return super(neww, self.sudo()).write(vals)
        elif len(self.source_id.ids)>1:
          return super(neww, self.sudo()).write(vals)
        if not self.sudo().env.context.get('active_ids'):
            for x in vals:
                if x == 'mobile':
                    phone_number = vals['mobile']
                    formated_phone = self.Phone_Format(phone_number)
                    if len(str(formated_phone)) < 10 or len(str(formated_phone)) > 15:
                        raise UserError(
                            _("Invalid mobile Number: Please provide a mobile number that has 10 to 15 characters."))
                    else:
                        Opportunities = self.sudo().env['crm.lead'].search(
                            ["&", ['id', '!=', self.id], "|", ["mobile", "=", formated_phone],
                             ["mobile_2", "=", formated_phone]], limit=1)
                        if Opportunities.ids != []:
                            raise UserError(
                                _("Mobile number already exists {} .".format(vals['mobile'])))
                        vals['mobile'] = formated_phone
                        return super(neww, self.sudo()).write(vals)
                elif x == 'mobile_2':
                    phone_number2 = vals['mobile_2']
                    formated_phone2 = self.Phone_Format(phone_number2)
                    if len(str(formated_phone2)) < 10 or len(str(formated_phone2)) > 15:
                        raise UserError(
                            _("Invalid mobile Number: Please provide a mobile number that has 10 to 15 characters."))
                    else:
                        Opportunities = self.sudo().env['crm.lead'].search(
                            ["&", ['id', '!=', self.id], "|", ["mobile", "=", formated_phone2],
                             ["mobile_2", "=", formated_phone2]], limit=1)
                        if Opportunities.ids != []:
                            raise UserError(
                                _("Mobile number already exists {} .".format(vals['mobile_2'])))
                        vals['mobile_2'] = formated_phone2
                        return super(neww, self.sudo()).write(vals)
                elif x == 'email_from':
                    if vals['email_from'] == False:
                        return super(neww, self.sudo()).write(vals)
                    emailstip = str(vals['email_from'])
                    emailstip = emailstip.rstrip()
                    emailstip = emailstip.lstrip()
                    if not self.check(emailstip):
                        raise UserError(_("Invalid Email."))
                    else:
                        vals['email_from'] = emailstip
                        Opportunities = self.sudo().env['crm.lead'].search(
                            ['&', ["email_from", "=", vals['email_from']], ['id', '!=', self.id]], limit=1)
                        if Opportunities.ids != []:
                            raise UserError(
                                _("Email already exists."))
                        return super(neww, self.sudo()).write(vals)
            return super(neww, self.sudo()).write(vals)
        return super(neww, self.sudo()).write(vals)
    @api.model
    def create(self, vals):
        if vals['mobile'] and vals['name']:
            phone_number = vals['mobile']
            vals['mobile'] = self.sudo().Phone_Format(phone_number)
            unique_domain = ["&","|",("active", "=", True),("active", "=", False),"|",("mobile", "=", vals['mobile']),("mobile_2", "=", vals['mobile'])]
            if vals['mobile_2']:
                phone_number2 = vals['mobile_2']
                vals['mobile_2'] = self.sudo().Phone_Format(phone_number2)
                unique_domain= ["&", "|",("active", "=", True),("active", "=", False),"|", "|", "|",["mobile", "=", vals['mobile']], ["mobile", "=", vals['mobile_2']],["mobile_2", "=", vals['mobile']], ["mobile_2", "=",                                         vals['mobile_2']]]
            if vals['email_from']:
                emailstip = str(vals['email_from'])
                emailstip = emailstip.rstrip()
                emailstip = emailstip.lstrip()
                vals['email_from'] = emailstip
                if vals['mobile_2']:
                   unique_domain= ["&", "|",("active", "=", True),("active", "=", False),"|", "|", "|","|",["mobile", "=", vals['mobile']], ["mobile", "=", vals['mobile_2']],["mobile_2", "=", vals['mobile']], ["mobile_2", "=",                                         vals['mobile_2']],["email_from", "=", vals['email_from']]]
                else:
                   unique_domain= ["&", "|",("active", "=", True),("active", "=", False),"|","|",["mobile", "=", vals['mobile']],["mobile_2", "=", vals['mobile']],["email_from", "=", vals['email_from']]]
            ExistingOpportunity = self.sudo().env['crm.lead'].search(unique_domain, limit=1)
            uploader = self.sudo().env.context.get('import_file') and self.sudo().env.context.get('tracking_disable')
            message_text = ""
            if vals['email_from']:
             if not self.check(emailstip):
                if uploader:
                    message_text = f'<strong>Error In Import</strong>' \
                                    'Opportunity {} has invaild email !'.format(vals['name'])
                else:
                    raise UserError(_("Invalid Email."))
            if len(vals['mobile']) < 9 or len(vals['mobile']) > 15:
                if uploader:
                    message_text = f'<strong>[Opportunity mobile Validation]</strong>' \
                                    'Can not create opportunity {} Because it has an invalid mobile Number {} Please provide a mobile number that has 10 to 15 characters.'.format(
                        vals['name'], vals['mobile'])
                else:
                    raise UserError(
                        _("Invalid mobile Number: Mobile number should be between 10 and 15 characters long."))
            elif vals['mobile_2']: 
               if len(vals['mobile_2']) < 9 or len(vals['mobile_2']) > 15 and vals['mobile2']:
                if uploader:
                    message_text = f'<strong>[Opportunity mobile Validation]</strong>' \
                                    'Can not create opportunity {} Because it has an invalid second mobile Number {} Please provide a mobile number that has 10 to 15 characters.'.format(
                        vals['name'], vals['mobile_2'])
                else:
                    raise UserError(
                        _("Invalid mobile Number: The second mobile number  should be between 10 and 15 characters long."))
            elif ExistingOpportunity.sudo() != []:
                if ExistingOpportunity.sudo().active and  str(ExistingOpportunity.sudo().stage_id.is_won)=="False" :
                    if uploader:
                        message_text = f'<strong>[Duplicate Opportunity Validation]</strong>' \
                                        'Can not create opportunity ({}) because a similar opportunity ({}) already exists and its ID is ({}). Please close it to be able to open a new one.'.format(vals['name'], ExistingOpportunity.sudo().name, ExistingOpportunity.sudo().id)
                    else:
                        raise UserError((
                            'Can not create opportunity ({}) because a similar opportunity ({}) already exists and its ID is ({}). Please close it to be able to open a new one.'.format(
                                vals['name'], ExistingOpportunity.sudo().name, ExistingOpportunity.sudo().id)))
                else: 
                    SalesPersonUserId = self.sudo().env['crm.team.member'].search(
                        ["&",["user_id.name", '=', self.sudo().env.user.name],"|",["crm_team_id.name", 'ilike', "Team AA"],["crm_team_id.name", 'ilike', "Team SF"]],limit=1)
                    if ExistingOpportunity.sudo().stage_id.is_won:
                        ExistingOpportunity.sudo().message_post(
                            body="An existing opportunity ({}) whose ID is ({}) was a Closed Won but has been reopened .".format(
                                ExistingOpportunity.sudo().name, ExistingOpportunity.sudo().id))
                        message_text2 = f'<strong>[Duplicate Opportunity Validation]</strong>' \
                                        'An existing opportunity ({}) whose ID is ({}) was a Closed Won but has been reopened .'.format(
                            ExistingOpportunity.sudo().name, ExistingOpportunity.sudo().id)
                        ExistingOpportunity.sudo().write({'stage_id': 1, 'probability': 30})
                    else:
                        ExistingOpportunity.sudo().message_post(
                            body="An existing opportunity ({}) whose ID is ({}) was a Closed Lost but has been reopened.".format(
                                ExistingOpportunity.sudo().name, ExistingOpportunity.sudo().id))
                        ExistingOpportunity.sudo().toggle_active()
                        message_text2 = f'<strong>[Duplicate Opportunity Validation]</strong>' \
                                            'An existing opportunity ({}) whose ID is ({}) was a Closed Lost but has been reopened .'.format(
                                ExistingOpportunity.sudo().name, ExistingOpportunity.sudo().id)
                    if message_text2 != "":
                        if str(SalesPersonUserId.id) != "False":
                                 ExistingOpportunity.sudo().write({'user_id': self.sudo().env.user.id})
                        else:
                                ExistingOpportunity.sudo().write({'team_id': False,'user_id': False})
                        if uploader:
                            RandomOpportunity = self.sudo().env['crm.lead'].search(["|", ["active", "=", True], ["active", "=", False]], limit=1)
                        ExistingOpportunity.sudo().send_message_(message_text2)
                        return ExistingOpportunity.sudo()
            else:
                currnet_opportunity = super(neww, self.sudo()).create(vals)
                return currnet_opportunity
        else:
            if uploader:
                message_text = f'<strong>Error In Import</strong>' \
                    'Opportunity name and mobile are required !'
            else:
                raise UserError(_("Opportunity name and mobile are required !"))

        if message_text != "":
            RandomOpportunity = self.sudo().env['crm.lead'].search(
                ["&", "|", ["active", "=", True], ["active", "=", False],
                    ["user_id.name", "=", self.sudo().env.user.name]], limit=1)
            if RandomOpportunity.ids == []:
                RandomOpportunity = self.sudo().env['crm.lead'].search(
                    ["|", ["active", "=", True], ["active", "=", False]], limit=1)
            RandomOpportunity.sudo().send_message_(message_text)
            return RandomOpportunity
    def send_message_(self, message_text):
        odoobot_id = self.sudo().env['ir.model.data'].sudo()._xmlid_to_res_id("base.partner_root")

        # find if a channel was opened for this user before
        channel = self.sudo().env['mail.channel'].sudo().search([
            ('name', '=', self.sudo().env.user.name),
            ('channel_partner_ids', 'in', [self.sudo().env.user.partner_id.id])
        ],
            limit=1,
        )
        if not channel:
            # create a new channel
            channel = self.sudo().env['mail.channel'].with_context(mail_create_nosubscribe=True).sudo().create({
                'channel_partner_ids': [(4, self.sudo().env.user.partner_id.id), (4, odoobot_id)],
                'public': 'private',
                'channel_type': 'chat',
                'name': self.sudo().env.user.name,
                'display_name': f'Picking Validated', })
        # send a message to the related user
        channel.sudo().message_post(
            body=message_text,
            author_id=odoobot_id,
            message_type="comment",
            subtype_xmlid='mail.mt_comment', )

    def Phone_Format(self, phone_number):
        x = str(re.sub('[^0-9]+', '', phone_number))
        if len(x) < 9:
            clean_phone_number = x
            return clean_phone_number
        else:
            index = phone_number.find('/')
            if index != -1 and index != 0 and index != 1:
                phone_number = phone_number[:index + 1]
            clean_phone_number = re.sub('[^0-9]+', '', phone_number)
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
    def check(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, email)):
            return True
        else:
            if email == "":
                return True
            return False