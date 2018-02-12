# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, exceptions, _


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
    date_attempt_contact1 = fields.Date('Date')
    bd_attempt_contact1 = fields.Many2one('res.users', 'Business Developer')

    # group 2nd attemp of contcat
    date_attempt_contact2 = fields.Date('Date')
    bd_attempt_contact2 = fields.Many2one('res.users', 'Business Developer')

    # group 3rd attemp of contcat
    date_attempt_contact3 = fields.Date('Date')
    bd_attempt_contact3 = fields.Many2one('res.users', 'Business Developer')

    # group 4th attemp of contcat
    date_attempt_contact4 = fields.Date('Date')
    bd_attempt_contact4 = fields.Many2one('res.users', 'Business Developer')

    # group call pitch
    secretary_call_pitch1 = fields.Boolean('Secraty')
    doctor_call_pitch1 = fields.Boolean('Doctor')
    date_call_pitch1 = fields.Date('Date')
    bd_call_pitch1 = fields.Many2one('res.users', 'Business Developer')
    comment_call_pitch1 = fields.Char('Comment')

    # group 2nd call pitch
    secretary_call_pitch2 = fields.Boolean('Secraty')
    doctor_call_pitch2 = fields.Boolean('Doctor')
    date_call_pitch2 = fields.Date('Date')
    bd_call_pitch2 = fields.Many2one('res.users', 'Business Developer')
    comment_call_pitch2 = fields.Char('Comment')

    # group 3rd call pitch
    secretary_call_pitch3 = fields.Boolean('Secraty')
    doctor_call_pitch3 = fields.Boolean('Doctor')
    date_call_pitch3 = fields.Date('Date')
    bd_call_pitch3 = fields.Many2one('res.users', 'Business Developer')
    comment_call_pitch3 = fields.Char('Comment')

    # group 4th call pitch
    secretary_call_pitch4 = fields.Boolean('Secraty')
    doctor_call_pitch4 = fields.Boolean('Doctor')
    date_call_pitch4 = fields.Date('Date')
    bd_call_pitch4 = fields.Many2one('res.users', 'Business Developer')
    comment_call_pitch4 = fields.Char('Comment')

    # group call back
    date_call_back1 = fields.Datetime('Date Time')
    bd_call_back1 = fields.Many2one('res.users', 'Business Developer')
    comment_call_back1 = fields.Char('Comment')

    # group 2nd call back
    date_call_back2 = fields.Datetime('Date Time')
    bd_call_back2 = fields.Many2one('res.users', 'Business Developer')
    comment_call_back2 = fields.Char('Comment')

    # group 3rd call back
    date_call_back3 = fields.Datetime('Date Time')
    bd_call_back3 = fields.Many2one('res.users', 'Business Developer')
    comment_call_back3 = fields.Char('Comment')

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

    # group 1st meeting
    date_meeting1 = fields.Date('Date')
    bd_meeting1 = fields.Many2one('res.users', 'Business Developer')
    comment_meeting1 = fields.Char('Comment')

    # group 2nd meeting
    date_meeting2 = fields.Date('Date')
    bd_meeting2 = fields.Many2one('res.users', 'Business Developer')
    comment_meeting2 = fields.Char('Comment')

    # group 3rd meeting
    date_meeting3 = fields.Date('Date')
    bd_meeting3 = fields.Many2one('res.users', 'Business Developer')
    comment_meeting3 = fields.Char('Comment')

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
