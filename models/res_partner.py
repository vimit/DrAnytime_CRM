# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, exceptions, _
from odoo.exceptions import UserError, AccessError

class ResUsers(models.Model):
    _inherit = "res.users"


class Stage(models.Model):
    _inherit = "crm.stage"

    @api.model
    def _onchange_restrict_access(self, stage_id):
        """ returns the new values when stage_id has changed """
        print('----------',self.env.uid)
        if self.env.uid != _one :
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
    date_attempt_contact_one = fields.Date('Date')
    bd_attempt_contact_one = fields.Many2one('res.users', 'Business Developer')

    # group _twond attemp of contcat
    date_attempt_contact_two = fields.Date('Date')
    bd_attempt_contact_two = fields.Many2one('res.users', 'Business Developer')

    # group _threerd attemp of contcat
    date_attempt_contact_three = fields.Date('Date')
    bd_attempt_contact_three = fields.Many2one('res.users', 'Business Developer')

    # group _fourth attemp of contcat
    date_attempt_contact_four = fields.Date('Date')
    bd_attempt_contact_four = fields.Many2one('res.users', 'Business Developer')

    # group call pitch
    secretary_call_pitch_one = fields.Boolean('Secretary')
    doctor_call_pitch_one = fields.Boolean('Doctor')
    date_call_pitch_one = fields.Date('Date')
    bd_call_pitch_one = fields.Many2one('res.users', 'Business Developer')
    comment_call_pitch_one = fields.Char('Comment')

    # group _twond call pitch

    secretary_call_pitch_two = fields.Boolean('Secretary')
    doctor_call_pitch_two = fields.Boolean('Doctor')
    date_call_pitch_two = fields.Date('Date')
    bd_call_pitch_two = fields.Many2one('res.users', 'Business Developer')
    comment_call_pitch_two = fields.Char('Comment')

    # group _threerd call pitch

    secretary_call_pitch_three = fields.Boolean('Secretary')
    doctor_call_pitch_three = fields.Boolean('Doctor')
    date_call_pitch_three = fields.Date('Date')
    bd_call_pitch_three = fields.Many2one('res.users', 'Business Developer')
    comment_call_pitch_three = fields.Char('Comment')

    # group _fourth call pitch
    secretary_call_pitch_four = fields.Boolean('Secretary')
    doctor_call_pitch_four = fields.Boolean('Doctor')
    date_call_pitch_four = fields.Date('Date')
    bd_call_pitch_four = fields.Many2one('res.users', 'Business Developer')
    comment_call_pitch_four = fields.Char('Comment')

    # group call back
    date_call_back_one = fields.Datetime('Date Time')
    bd_call_back_one = fields.Many2one('res.users', 'Business Developer')
    comment_call_back_one = fields.Char('Comment')

    # group _twond call back
    date_call_back_two = fields.Datetime('Date Time')
    bd_call_back_two = fields.Many2one('res.users', 'Business Developer')
    comment_call_back_two = fields.Char('Comment')

    # group _threerd call back
    date_call_back_three = fields.Datetime('Date Time')
    bd_call_back_three = fields.Many2one('res.users', 'Business Developer')
    comment_call_back_three = fields.Char('Comment')

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
    date_meeting_set = fields.Date('Date')
    bd_meeting_set = fields.Many2one('res.users', 'Business Developer')
    comment_meeting_set = fields.Char('Comment')

    # group _onest meeting
    date_meeting_one = fields.Date('Date')
    bd_meeting_one = fields.Many2one('res.users', 'Business Developer')
    comment_meeting_one = fields.Char('Comment')

    # group _twond meeting
    date_meeting_two = fields.Date('Date')
    bd_meeting_two = fields.Many2one('res.users', 'Business Developer')
    comment_meeting_two = fields.Char('Comment')

    # group _threerd meeting
    date_meeting_three = fields.Date('Date')
    bd_meeting_three = fields.Many2one('res.users', 'Business Developer')
    comment_meeting_three = fields.Char('Comment')

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



    def _default_stage_id(self):
        return self.env['crm.stage'].search([], limit=1).id

    @api.onchange('stage_id')
    @api.multi
    def onchange_contact_stage_id(self):
        self.state_contact = self.stage_id.id
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

    state_contact= fields.Many2one('crm.stage' ,string='Status',
         group_expand='_read_group_contact_states', track_visibility=False)

    state_target = fields.Many2one('crm.stage',  string='Status',
         group_expand='_read_group_target_states',track_visibility=False)

    state_account = fields.Many2one('crm.stage',  string='Status',
         group_expand='_read_group_account_states',  track_visibility=False)

    stage_sequence = fields.Integer(related='stage_id.sequence', string='Status Sequence',   store=True)


    @api.model
    def _read_group_contact_states(self, stages, domain, order):
        search_domain = [('sequence', 'in', (0,1,2,3,4,5,6))]
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.model
    def _read_group_target_states(self, stages, domain, order):
        search_domain = [('sequence', 'in',(6,7,8,9,10,11,12,13,14))]
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)

        return stages.browse(stage_ids)

    @api.model
    def _read_group_account_states(self, stages, domain, order):
        search_domain = [('sequence', 'in', (14,15,16))]
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
        print('------2')
        if not stage_id:
            return {}
        stage = self.env['crm.stage'].browse(stage_id)

        if self.stage_id.id == 2 and self.x_studio_field_WDmu0 == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (attempt of contact) '))

        elif self.stage_id.id == 3 and self.x_studio_field_8wWZX == False  and self.x_studio_field_JqT0t == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Secretary or Doctor'))

        elif self.stage_id.id == 3 and self.x_studio_field_eLcYs == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (pitched)'))


        elif self.stage_id.id == 9 and self.x_studio_field_5CWT8 == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (callback)'))

        elif self.stage_id.id == 10 and self.x_studio_field_v6GZl == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (meeting set)'))

        elif self.stage_id.id == 6 and self.x_studio_field_WP1ro == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (pre_agreement) '))

        elif self.stage_id.id in (8,16) and self.x_studio_field_g1zcu == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Specialisation'))
        elif self.stage_id.id in (8, 16) and self.x_studio_field_HnDpa == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Skills'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_EBPqm == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Services'))

        elif self.stage_id.id in (8,16) and self.business_developer_id == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Business Developer'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_ZilCW == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Account manager'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_kYZ1u == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field CRM / VISIBILITY   '))

        elif self.stage_id.id in (8,16) and self.x_studio_field_K3GQ1 == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field User Manuel sent'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_6bUX9 == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field URL BACKEND'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_cBgxC == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Website backlink'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_igtTt == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Voicemail'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_iYdhZ == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Email signature '))

        elif self.stage_id.id in (8,16) and self.x_studio_field_RYaI5 == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Translation'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_kQZyr == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Visit card '))

        elif self.stage_id.id in (8,16) and self.x_studio_field_zjMCR == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Marketing kit'))
        elif self.stage_id.id in (8,16) and self.x_studio_field_XiNDd == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Google profile'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_6G6rb == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Google backlink'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_Ca_oneDT == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Happy doctor '))

        elif self.stage_id.id in (8,16) and self.x_studio_field_bIOcq == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Personality'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_dBDfP == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Availability'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_kc22X == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Agenda Synchro'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_16Eot == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Expertise'))

        elif self.stage_id.id in (8,16) and self.x_studio_field_xVtps == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Current CRM'))
        elif self.stage_id.id in (8,16) and self.x_studio_field_puqZa == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Competitors software'))

        elif self.stage_id.id == 17 and self.x_studio_field_v6GZl == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (meeting set)'))

        elif self.stage_id.id == 17 and self.x_studio_field_v6GZl == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (meeting set)'))

        elif self.stage_id.id == 17 and self.x_studio_field_v6GZl == False:
            raise exceptions.Warning(
                _('To move to this step you first need to fill field Date (meeting set)'))

        if not self.env.user.has_group('sales_team.group_sale_manager') and self.stage_id.id == 16 :
            raise exceptions.Warning(
                _('You are not allowed to pass to Stage Activated, Please contact Administrator'))

        return {}


    @api.multi
    def write(self, vals):
        res = super(Partner, self).write(vals)
        if vals.get('stage_id'):
            vals.update(self._onchange_stage_id_values(vals.get('stage_id')))
        if vals.get('state_contact'):
            vals.update(self._onchange_contact_stage_id(vals.get('state_contact')))
        elif vals.get('state_target'):
            vals.update(self._onchange_contact_stage_id(vals.get('state_target')))
        elif vals.get('state_account'):
            vals.update(self._onchange_contact_stage_id(vals.get('state_account')))


        return res




