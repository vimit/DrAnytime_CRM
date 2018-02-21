# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, exceptions, tools, _
from odoo.exceptions import UserError, AccessError

class ResUsers(models.Model):
    _inherit = "res.users"


class Stage(models.Model):
    _inherit = "crm.stage"

    @api.model
    def _onchange_restrict_access(self, stage_id):
        """ returns the new values when stage_id has changed """
        print('----------',self.env.uid)
        if self.env.uid != 1 :
            raise exceptions.Warning('You are not allowed to change the stages, Please contact the Administrator')
            return  True
        return {}



    @api.multi
    def write(self, vals):
        res = super(Stage, self).write(vals)
        vals.update(self._onchange_restrict_access(vals.get('stage_id')))

        return res

    @api.model
    def create(self, values):
        res = super(Stage, self).create(values)
        values.update(self._onchange_restrict_access(values.get('stage_id')))

        return res

class Specialization(models.Model):
    _name = 'partner.specialization'

    name = fields.Char('Name')
    description = fields.Char('Description')


class CrmVisibility(models.Model):
    _name = 'crm.visibility'

    name = fields.Char('Name')
    description = fields.Char('Description')


class ReasonNotInterested(models.Model):
    _name = 'reason.notinterested'

    name = fields.Char('Name')
    description = fields.Char('Description')

class Skills(models.Model):
    _name = 'partner.skills'
    name = fields.Char('Name')
    description = fields.Char('Description')
class Services(models.Model):
    _name = 'partner.services'
    name = fields.Char('Name')
    description = fields.Char('Description')
class Expertise(models.Model):
    _name = 'partner.expertise'
    name = fields.Char('Name')
    description = fields.Char('Description')
class Studies(models.Model):
    _name = 'partner.studies'
    name = fields.Char('Name')
    description = fields.Char('Description')
class Experience(models.Model):
    _name = 'partner.experience'
    name = fields.Char('Name')
    description = fields.Char('Description')

class CallAttempt(models.Model):
    _name = 'call.attempt'
    _order = "date_attempt"

    description = fields.Char('Description')
    date_attempt = fields.Date('Date')
    bd_attempt = fields.Many2one('res.users', 'Business Developer')
    partner_id = fields.Many2one('res.partner','Contact', readonly=True)
    name = fields.Char('Name', related="partner_id.name", store=True, readonly=True)

class CallPitch(models.Model):
    _name = 'call.pitch'
    _order = "date_pitch"

    date_pitch = fields.Date('Date')
    bd_pitch = fields.Many2one('res.users', 'Business Developer')
    partner_id = fields.Many2one('res.partner', 'Contact', readonly=True)
    name = fields.Char('Name', related="partner_id.name", store=True, readonly=True)
    comment_call_pitch = fields.Char('Comment')
    sd_call_pitch = fields.Selection(
        [('secretary', 'Secretary'), ('doctor', 'Doctor')],
        string='Secretary / Doctor')

class ContactMeeting(models.Model):
    _name = 'contact.meeting'
    _order = "date_meeting"

    date_meeting = fields.Date('Date')
    bd_meeting = fields.Many2one('res.users', 'Business Developer')
    partner_id = fields.Many2one('res.partner','Contact', readonly=True)
    name = fields.Char('Name', related="partner_id.name", store=True, readonly=True)
    comment_meeting = fields.Char('Comment')




class Partner(models.Model):

    _inherit = 'res.partner'

    # principal doctor information
    inami = fields.Char('INAMI / RIZIV')
    subscription_type = fields.Selection([('none', 'None'),
                                          ('free_directory', 'Free Directory'),
                                          ('free_trial', 'Free Trial'),
                                          ('paying_patient', 'Paying / Patient'),
                                          ('paying_directoty', 'Paying Directory'),
                                          ('basic_paying', 'Basic Paying'),
                                          ('premium_paying', 'Premium Paying')
                                          ], 'Subscription Type'
                                         )
    specialization = fields.Many2many('partner.specialization', 'partner_specialization_rel', 'partner_id',
                                      'specialization_id', string='Specialization')

    business_developer_id = fields.Many2one('res.users', 'Business Developer')

    personnality = fields.Selection(
        [('analytical', 'Analytical'), ('driving', 'Driving'), ('amiable', 'Amiable'), ('expressive', 'Expressive')],
        string='Doctor personnality')

    happiness = fields.Selection([('0', '0'),
                                  ('1', '1'),
                                  ('2', '2'),
                                  ('3', '3'),
                                  ('4', '4'),
                                  ('5', '5')
                                  ], string='Doctor Happyness')

    # Prospection Process Tab

    # group attemp of contcat
    call_attempt_ids = fields.One2many('call.attempt','partner_id',string="Attempt of Contact", store=True)

    # group call pitch
    call_pitch_ids = fields.One2many('call.pitch', 'partner_id', string="Call Pitch")

    # group call back
    date_call_back_one = fields.Datetime('Date Time', track_visibility='onchange')
    bd_call_back_one = fields.Many2one('res.users', 'Business Developer')
    comment_call_back_one = fields.Char('Comment')

    # group Email sent
    date_email_sent = fields.Date('Date')
    bd_email_sent = fields.Many2one('res.users', 'Business Developer')
    comment_email_sent = fields.Char('Comment')

    # group interested
    date_interested = fields.Date('Date')
    bd_interested = fields.Many2one('res.users', 'Business Developer')
    comment_interested = fields.Char('Comment')
    crm_visibility = fields.Many2many('crm.visibility', 'partner_crm_visibilty_rel', 'partner_id', 'crm_visibilty_id',
                                      string='CRM / Visibility')

    # group not interested
    date_notinterested = fields.Date('Date')
    bd_notinterested = fields.Many2one('res.users', 'Business Developer')
    reason_notinterested = fields.Many2one('reason.notinterested', 'Reason')

    # group meeting set
    date_meeting_set = fields.Date('Date', track_visibility='onchange')
    bd_meeting_set = fields.Many2one('res.users', 'Business Developer')
    comment_meeting_set = fields.Char('Comment')

    # group _ meeting
    contact_meeting_ids = fields.One2many('contact.meeting', 'partner_id', string="Meeting")

    # group offer
    date_offer = fields.Date('Date')
    bd_offer = fields.Many2one('res.users', 'Business Developer')
    offer_details = fields.Char('Offer Details')

    # group preagreement
    date_preagreement = fields.Date('Date')
    bd_preagreement = fields.Many2one('res.users', 'Business Developer')
    comment_preagreement = fields.Char('Comment')

    # group signed
    date_signed = fields.Date('Date')
    bd_signed = fields.Many2one('res.users', 'Business Developer')
    comment_signed = fields.Char('Comment')

    # Tab Account Management
    first_email = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], '1st email (activation)')
    comment_first_email = fields.Char('Comment')
    #
    service_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Services completed')
    comment_service_completed = fields.Char('Comment')
    #
    price_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Prices completed')
    comment_price_completed = fields.Char('Comment')
    #
    cv_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')],
                                    'CV/experiences completed')
    comment_cv_completed = fields.Char('Comment')
    #
    duration_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')],
                                          'Duration completed')
    comment_duration_completed = fields.Char('Comment')
    #
    personal_message_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')],
                                                  'Personal message completed')
    comment_personal_message_completed = fields.Char('Comment')
    #
    profile_picture = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Profile picture')
    comment_profile_picture = fields.Char('Comment')
    #
    photo_practice = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Photo Practice')
    comment_photo_practice = fields.Char('Comment')
    #
    marketing_kit = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Marketing kit')
    comment_marketing_kit = fields.Char('Comment')
    #
    synchronisation_completed = fields.Selection(
        [('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going'), ('not_possible', 'Not Possible')], 'Synchronisation')
    comment_synchronisation_completed = fields.Char('Comment')
    #
    backlink = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Backlink')
    comment_backlink = fields.Char('Comment')
    #
    google_profile = fields.Selection(
        [('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going'), ('already_one', 'Already One')], 'Google profile')
    comment_google_profile = fields.Char('Comment')
    #
    voicemail = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Voicemail')
    comment_voicemail = fields.Char('Comment')
    #
    mail_signature = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Mail signature ')
    comment_mail_signature = fields.Char('Comment')
    #
    email_to_patient = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Email to patient')
    comment_email_to_patient = fields.Char('Comment')
    #
    translation = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Translation')
    comment_translation = fields.Char('Comment')
    #
    business_card = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Business cards')
    comment_business_card = fields.Char('Comment')
    ## tab DA Profile
    skills = fields.Many2many('partner.skills', 'partner_skills_rel', 'partner_id', 'skills_id',
                                      string='Skills')
    services = fields.Many2many('partner.services', 'partner_services_rel', 'partner_id', 'services_id',
                              string='Services')
    availability = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Availability')
    expertise = fields.Many2many('partner.expertise', 'partner_expertise_rel', 'partner_id', 'expertise_id',
                                string='Expertise')
    facebook_link = fields.Char('Facebook')
    linkedin_link = fields.Char('LinkedIn')
    message_patient = fields.Text('Message to patient')
    studies = fields.Many2many('partner.studies', 'partner_studies_rel', 'partner_id', 'studies_id',
                                 string='Studies')
    experience = fields.Many2many('partner.experience', 'partner_experience_rel', 'partner_id', 'experience_id',
                               string='Professional experiences')
    conference_participation = fields.Char('Participation in conferences')
    asociation_member = fields.Char('Member to associations')
    academic_pub = fields.Char('Academic research / Publications')

    # *** 8 images *******************************
    image1 = fields.Binary("Image", attachment=True )
    image2 = fields.Binary("Image", attachment=True )
    image3 = fields.Binary("Image", attachment=True )
    image4 = fields.Binary("Image", attachment=True )
    image5 = fields.Binary("Image", attachment=True )
    image6 = fields.Binary("Image", attachment=True )
    image7 = fields.Binary("Image", attachment=True )
    image8 = fields.Binary("Image", attachment=True )



    def _default_stage_id(self):
        return self.env['crm.stage'].search([], limit=1).id

    @api.onchange('stage_id')
    @api.multi
    def onchange_contact_stage_id(self):
        self.state_target = self.stage_id.id
        self.state_account = self.stage_id.id


    @api.multi
    def _onchange_contact_stage_id(self,stage):
        if not stage:
            return {}

        self.stage_id = stage
        return {}

    stage_id = fields.Many2one('crm.stage', string='Status', index=True, track_visibility='onchange' ,
        group_expand='_read_group_all_states' , default=lambda self: self._default_stage_id())

    state_target = fields.Many2one('crm.stage',  string='Status',
         group_expand='_read_group_target_states',track_visibility=False)

    state_account = fields.Many2one('crm.stage',  string='Status',
         group_expand='_read_group_account_states',  track_visibility=False)
    state_contact = fields.Many2one('crm.stage', string='Status',track_visibility=False)

    stage_sequence = fields.Integer(related='stage_id.sequence', string='Status Sequence', store=True, readonly=True)



    @api.model
    def _read_group_target_states(self, stages, domain, order):
        search_domain = [('sequence', 'in',(0,1,2,3,4,5,6,7,8,9,10,11,12))]
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)

        return stages.browse(stage_ids)

    @api.model
    def _read_group_account_states(self, stages, domain, order):
        search_domain = [('sequence', 'in', (12,13,14))]
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)

        return stages.browse(stage_ids)

    @api.model
    def _read_group_all_states(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)

        return stages.browse(stage_ids)

    ####### Test required field to pass to an other stage ####

    @api.model
    def _onchange_stage_id_values(self, stage_id):
        """ returns the new values when stage_id has changed """
        if not stage_id:
            return {}
        stage = self.env['crm.stage'].browse(stage_id)
        call_attempt = len(self.env['call.attempt'].browse(self.call_attempt_ids))
        call_pitch = len(self.env['call.pitch'].browse(self.call_attempt_ids))
        if self.stage_id.id == 2 and call_attempt == 0:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Call Attempt '))

        elif self.stage_id.id == 3 and call_pitch == 0:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Call Pitch'))

        elif self.stage_id.id == 9 and self.date_call_back_one == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (callback)'))

        elif self.stage_id.id == 10 and self.date_meeting_set == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (meeting set)'))

        elif self.stage_id.id == 6 and self.date_preagreement == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (pre_agreement) '))

        elif self.stage_id.id in (8,16) and self.specialization == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Specialization'))


        elif self.stage_id.id in (8,16) and self.business_developer_id == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Business Developer'))

        elif self.stage_id.id in (8,16) and self.crm_visibility == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field CRM / VISIBILITY   '))

        elif self.stage_id.id in (8,16) and self.backlink == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Website backlink'))

        elif self.stage_id.id in (8,16) and self.voicemail == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Voicemail'))

        elif self.stage_id.id in (8,16) and self.mail_signature == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Email signature '))

        elif self.stage_id.id in (8,16) and self.translation == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Translation'))

        elif self.stage_id.id in (8,16) and self.business_card == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Business card '))

        elif self.stage_id.id in (8,16) and self.marketing_kit == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Marketing kit'))

        elif self.stage_id.id in (8,16) and self.google_profile == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Google profile'))

        elif self.stage_id.id in (8,16) and self.happiness == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Happy doctor '))

        elif self.stage_id.id in (8,16) and self.personnality == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Personality'))
        elif self.stage_id.id in (8,16) and self.expertise == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Expertise'))

        elif self.stage_id.id in (8,16) and self.availability == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Availability'))
        elif self.stage_id.id in (8, 16) and self.skills == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Skills'))

        elif self.stage_id.id in (8, 16) and self.services == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Services'))


        if not self.env.user.has_group('sales_team.group_sale_manager') and self.stage_id.id == 16 :
            raise exceptions.Warning(
                _('You are not allowed to pass to Stage Activated, Please contact Administrator'))

        return {}

    @api.multi
    def _call_activity_create(self):
        print('---------dd---',self.date_call_back_one)
        model_id = self.env['ir.model'].search([('model','=','res.partner')],limit=1).id
        activity_type_id = self.env['mail.activity.type'].search([('name','=','Call')],limit=1).id

        vals={
            'activity_type_id':activity_type_id,
            'date_deadline':self.date_call_back_one,
            'user_id':self.bd_call_back_one.id,
            'summary':self.comment_call_back_one,
            'res_model_id':model_id,
            'res_id': self.id,
            'res_model': 'res.partner'
        }
        self.env['mail.activity'].create(vals)

        return {}

    @api.multi
    def _meeting_activity_create(self):
        model_id = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1).id
        activity_type_id = self.env['mail.activity.type'].search([('name', '=', 'Meeting')], limit=1).id
        alarm_ten_id = self.env['calendar.alarm'].search([('duration', '=', '1'),('interval', '=', 'days'),('type','=','notification')], limit=1).id

        vals_calendar = {
            'name': self.name,
            'allday': True,
            'start_date': self.date_meeting_set,
            'stop_date': self.date_meeting_set,
            'start': self.date_meeting_set,
            'stop': self.date_meeting_set,
            'description': self.comment_meeting_set,

        }

        calendar_id = self.env['calendar.event'].create(vals_calendar)
        if calendar_id:
            if self.bd_meeting_set.id == self.env.uid:
                self.env.cr.execute(
                    'insert into calendar_event_res_partner_rel (calendar_event_id,res_partner_id) values(%s,%s)',
                    (calendar_id.id, self.env.uid))

            else:
                self.env.cr.execute('insert into calendar_event_res_partner_rel (calendar_event_id,res_partner_id) values(%s,%s)',
                                    (calendar_id.id, self.bd_meeting_set.partner_id.id))
            self.env.cr.execute(
                'insert into calendar_alarm_calendar_event_rel (calendar_event_id,calendar_alarm_id) values(%s,%s)',
                (calendar_id.id, alarm_ten_id))

        vals = {
            'activity_type_id': activity_type_id,
            'date_deadline': self.date_meeting_set,
            'user_id': self.bd_meeting_set.id,
            'summary': self.comment_meeting_set,
            'res_model_id': model_id,
            'res_id': self.id,
            'res_model': 'res.partner',
            # 'calendar_event_id':[(6, 0, calendar_id.ids)]
        }
        activity_id= self.env['mail.activity'].create(vals)
        return {}

    @api.multi
    def write(self, vals):
        res = super(Partner, self).write(vals)
        if vals.get('stage_id'):
            vals.update(self._onchange_stage_id_values(vals.get('stage_id')))
        # if vals.get('state_contact'):
        #     vals.update(self._onchange_contact_stage_id(vals.get('state_contact')))
        elif vals.get('state_target'):
            vals.update(self._onchange_contact_stage_id(vals.get('state_target')))
        elif vals.get('state_account'):
            vals.update(self._onchange_contact_stage_id(vals.get('state_account')))

        if vals.get('date_call_back_one'):
            vals.update(self._call_activity_create())
        if vals.get('date_meeting_set'):
            vals.update(self._meeting_activity_create())


        return res




