# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, exceptions, tools, _
from odoo.exceptions import UserError, AccessError, ValidationError
from datetime import datetime,timedelta

class ResUsers(models.Model):
    _inherit = "res.users"


class Stage(models.Model):
    _inherit = "crm.stage"

    @api.model
    def _onchange_restrict_access(self, stage_id):
        """ returns the new values when stage_id has changed """
        print('----------',self.env.uid)
        # if self.env.uid != 1 :
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

    description = fields.Char('Comment')
    date_attempt = fields.Date('Date')
    bd_attempt = fields.Many2one('res.users', 'Business Developer')
    intern_attempt = fields.Many2one('hr.intern', 'Intern')
    partner_id = fields.Many2one('res.partner','Contact', readonly=True)
    name = fields.Char('Name', related="partner_id.name", store=True, readonly=True)

class CallPitch(models.Model):
    _name = 'call.pitch'
    _order = "date_pitch"

    date_pitch = fields.Date('Date')
    bd_pitch = fields.Many2one('res.users', 'Business Developer')
    intern_pitch = fields.Many2one('hr.intern', 'Intern')
    partner_id = fields.Many2one('res.partner', 'Contact', readonly=True)
    name = fields.Char('Name', related="partner_id.name", store=True, readonly=True)
    comment_call_pitch = fields.Char('Comment')
    sd_call_pitch = fields.Selection(
        [('secretary', 'Secretary'), ('doctor', 'Doctor')],
        string='Secretary / Doctor')

class ContactMeeting(models.Model):
    _name = 'contact.meeting'
    _order = "date_meeting"

    date_meeting = fields.Datetime('Date')
    bd_meeting = fields.Many2one('res.users', 'Business Developer')
    intern_meeting = fields.Many2one('hr.intern', 'Intern')
    partner_id = fields.Many2one('res.partner','Contact', readonly=True)
    name = fields.Char('Name', related="partner_id.name", store=True, readonly=True)
    comment_meeting = fields.Char('Comment')

class Intern(models.Model):
    _name = 'hr.intern'

    name  = fields.Char('Name')
    description = fields.Char('Description')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

class CurrentCRM(models.Model):
    _name = 'current.crm'

    name  = fields.Char('Name')
    description = fields.Char('Description')

class Partner(models.Model):

    _inherit = 'res.partner'



    ###

    sent_by_mail = fields.Boolean('Send by paper mail')
    current_crm = fields.Many2one('current.crm', 'Current CRM')

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

    business_developer_id = fields.Many2one('res.users', 'Business Developer',default=lambda self: self.env.uid)

    personnality = fields.Selection(
        [('analytical', 'Analytical'), ('driving', 'Driving'), ('amiable', 'Amiable'), ('expressive', 'Expressive')],
        string='Doctor personnality')

    happiness = fields.Selection([('0', '0'),
                                  ('1', '1'),
                                  ('2', '2'),
                                  ('3', '3'),
                                  ('4', '4'),
                                  ('5', '5')
                                  ], string='Doctor Happiness')
    intern_ids = fields.Many2one('hr.intern', 'Intern')
    doctor_admin = fields.Char('Doctor AdminID')

    # Prospection Process Tab

    # group attemp of contcat
    call_attempt_ids = fields.One2many('call.attempt','partner_id',string="Attempt of Contact", store=True)

    # group call pitch
    call_pitch_ids = fields.One2many('call.pitch', 'partner_id', string="Call Pitch", store=True)

    # group call back
    date_call_back_one = fields.Datetime('Date Time(Call back)', track_visibility='onchange')
    bd_call_back_one = fields.Many2one('res.users', 'Business Developer (Call back)')
    intern_call_back_one = fields.Many2one('hr.intern', 'Intern (Call back)')
    comment_call_back_one = fields.Char('Comment(Call back)')

    # group Email sent
    date_email_sent = fields.Date('Date(Email sent)')
    bd_email_sent = fields.Many2one('res.users', 'Business Developer(Email sent)')
    intern_email_sent = fields.Many2one('hr.intern', 'Intern (Email sent)')
    comment_email_sent = fields.Char('Comment(Email sent)')

    # group interested
    # date_interested = fields.Date('Date')
    # bd_interested = fields.Many2one('res.users', 'Business Developer')
    # comment_interested = fields.Char('Comment')
    # crm_visibility = fields.Many2many('crm.visibility', 'partner_crm_visibilty_rel', 'partner_id', 'crm_visibilty_id',
    #                                   string='CRM / Visibility')

    # group not interested
    date_notinterested = fields.Date('Date(Not Interested)')
    bd_notinterested = fields.Many2one('res.users', 'Business Developer(Not Interested)')
    intern_notinterested = fields.Many2one('hr.intern', 'Intern (Not Interested)')
    reason_notinterested = fields.Many2one('reason.notinterested', 'Reason')
    comment_not_inteterested = fields.Char('Comment (Not Interested)')

    # group meeting set
    date_meeting_set = fields.Datetime('Date(Meeting Set)', track_visibility='onchange', index=True)
    bd_meeting_set = fields.Many2one('res.users', 'Business Developer(Meeting Set)', index=True)
    intern_meeting_set = fields.Many2one('hr.intern', 'Intern (Meeting Set)')
    comment_meeting_set = fields.Char('Comment(Meeting Set)')

    # group _ meeting
    contact_meeting_ids = fields.One2many('contact.meeting', 'partner_id', string="Meeting", store=True)

    # group offer
    date_offer = fields.Date('Date(Offer)')
    bd_offer = fields.Many2one('res.users', 'Business Developer(Offer)')
    intern_offer = fields.Many2one('hr.intern', 'Intern (Offer)')
    offer_details = fields.Char('Offer Details')

    # group preagreement
    date_preagreement = fields.Date('Date(Pre-agreement)')
    bd_preagreement = fields.Many2one('res.users', 'Business Developer(Pre-agreement)')
    intern_preagreement = fields.Many2one('hr.intern', 'Intern (Pre-agreement)')
    comment_preagreement = fields.Char('Comment(Pre-agreement)')

    # group signed
    date_signed = fields.Date('Date(Signed)')
    bd_signed = fields.Many2one('res.users', 'Business Developer(Signed)')
    intern_signed = fields.Many2one('hr.intern', 'Intern (Signed)')
    comment_signed = fields.Char('Comment(Signed)')

    # Tab Account Management
    first_email = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], '1st email (activation)')
    comment_first_email = fields.Char('Comment(1srt email)')
    #
    service_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Services completed')
    comment_service_completed = fields.Char('Comment(Services completed)')
    #
    price_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Prices completed')
    comment_price_completed = fields.Char('Comment(Prices completed)')
    #
    cv_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')],
                                    'CV/experiences completed')
    comment_cv_completed = fields.Char('Comment(CV/experiences completed)')
    #
    duration_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')],
                                          'Duration completed')
    comment_duration_completed = fields.Char('Comment(Duration completed)')
    #
    personal_message_completed = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')],
                                                  'Personal message completed')
    comment_personal_message_completed = fields.Char('Comment(Personal message completed)')
    #
    profile_picture = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Profile picture')
    comment_profile_picture = fields.Char('Comment(Profile picture)')
    #
    photo_practice = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Photo Practice')
    comment_photo_practice = fields.Char('Comment(Photo Practice)')
    #
    marketing_kit = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Marketing kit')
    comment_marketing_kit = fields.Char('Comment(Marketing kit)')
    #
    synchronisation_completed = fields.Selection(
        [('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going'), ('not_possible', 'Not Possible')], 'Synchronization')
    comment_synchronisation_completed = fields.Char('Comment(Synchronization)')
    #
    backlink = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Backlink')
    comment_backlink = fields.Char('Comment(Backlink)')
    #
    google_profile = fields.Selection(
        [('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going'), ('already_one', 'Already One')], 'Google profile')
    comment_google_profile = fields.Char('Comment(Google profile)')
    #
    voicemail = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Voicemail')
    comment_voicemail = fields.Char('Comment(Voicemail)')
    #
    mail_signature = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Mail signature')
    comment_mail_signature = fields.Char('Comment(Mail signature)')
    #
    email_to_patient = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Email to patient')
    comment_email_to_patient = fields.Char('Comment(Email to patient)')
    #
    translation = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Translation')
    comment_translation = fields.Char('Comment(Translation)')
    #
    business_card = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')], 'Manuel Sent')
    comment_business_card = fields.Char('Comment(Business cards)')
    ###
    manuel_sent = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('proposed', 'Proposed')], 'Business cards')
    comment_manuel_sent = fields.Char('Comment(Manuel Sent)')
    widget = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going'), ('proposed', 'Proposed'), ('sent', 'Sent'), ('todo', 'To Do'), ('topropose', 'To Propose')], 'Widget')
    comment_widget = fields.Char('Comment(Widget)')
    voice_mail = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')],
                                  'Voicemail + email signature')
    comment_voice_mail = fields.Char('Comment(Voicemail + email signature)')
    website_ok = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going')],
                                  'Website')
    comment_website_ok = fields.Char('Comment(Website)')
    customer_service_number = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going'), ('proposed', 'Proposed')],
                                               'Customer service number on google profile ')
    comment_customer_service_number = fields.Char('Comment(Customer service number on google profile)')
    website_backlink = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('on_going', 'On Going'), ('proposed', 'Proposed'), ('sent', 'Sent'), ('todo', 'To Do'), ('topropose', 'To Propose')],
                                       'Backlink on website')
    comment_website_backlink = fields.Char('Comment(Backlink on website)')

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

    # Tab subscription details *****
    # company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
    #                                       readonly=True,
    #                                       help='Utility field to express amount currency')
    subscription_month = fields.Float('Monthly subscription', currency_field='company_currency_id', track_visibility='onchange' )
    subscription_commitment = fields.Selection([('monthly','Monthly'),('trimestrial','Trimestrial'),('semestrial','Semestrial'),('yearly','Yearly')],'Commitment', track_visibility='onchange' )
    subscription_upfront_payment = fields.Selection([('no','NO'),('trimestrial','Trimestrial'),('semestrial','Semestrial'),('yearly','Yearly')], 'Upfront Payment', track_visibility='onchange' )
    subscription_upfront_turnover = fields.Float('Upfront turnover', currency_field='company_currency_id', track_visibility='onchange' )
    telesecretary_contract = fields.Float('Telesecretary contract (in € / month)')
    subsciption_part_condition = fields.Char('Particular Conditions')
    #
    # Tab Lost
    date_lost = fields.Date('Lost Date')
    reason_lost = fields.Many2one('sale.subscription.close.reason','Lost reason')

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
        search_domain = [('sequence', 'in',(0,1,2,3,4,5,6,7,8,9,10,11))]
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)

        return stages.browse(stage_ids)

    @api.model
    def _read_group_account_states(self, stages, domain, order):
        search_domain = [('sequence', 'in', (11,12,13,14))]
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)

        return stages.browse(stage_ids)

    @api.model
    def _read_group_all_states(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)

        return stages.browse(stage_ids)
    ### test if there are at least one file attached onchange stage
    @api.onchange('stage_id')
    def onchange_stage(self):
        file_attached = len(
            self.env['ir.attachment'].search([('res_model', '=', 'res.partner'), ('res_id', '=', self._origin.id)]))
        if self.stage_id.id in (8, 16) and file_attached == 0:
            raise ValidationError('To move to this step you first need to Upload at least one file ')


    ####### Test required field to pass to an other stage ####
    @api.model
    def _onchange_stage_id_values(self, stage_id):
        """ returns the new values when stage_id has changed """
        if not stage_id:
            return {}
        print('1111')

        call_attempt = len(self.env['call.attempt'].browse(self.call_attempt_ids))
        call_pitch = len(self.env['call.pitch'].browse(self.call_pitch_ids))
        contact_meeting =  len(self.env['contact.meeting'].browse(self.contact_meeting_ids))
        # file_attached = len(self.env['ir.attachment'].search([('res_model','=','res.partner'),('res_id','=',self.id)]))
        msg=''
        ## file attached
        file_attached = len(
            self.env['ir.attachment'].search([('res_model', '=', 'res.partner'), ('res_id', '=', self.id)]))
        if self.stage_id.id in (8, 16) and file_attached == 0:
            msg = msg + ' - Upload at least one file \n'
        ##
        if self.stage_id.id == 2 and call_attempt == 0:
            msg = msg + ' - Call Attempt  \n'

        if self.stage_id.id == 3 and call_pitch == 0:
            msg = msg + ' - Call Pitch  \n'

        if self.stage_id.id == 9 and self.date_call_back_one == False:
            msg = msg + ' - Date (callback) '

        if self.stage_id.id == 10 and self.date_meeting_set == False:
            msg = msg + ' - Date (meeting set) \n'

        if self.stage_id.id == 6 and self.date_preagreement == False:
            msg = msg + ' - Date (pre_agreement)  \n'

        ## individual and company contact
        if self.stage_id.id in (8,16) and self.mobile == False:
            msg = msg + ' - Mobile \n'
        if self.stage_id.id in (8,16) and self.email == False:
            msg = msg + ' - Email \n'
        if self.stage_id.id in (8, 16) and self.street == False:
            msg = msg + ' - Street in Adress \n'
        if self.stage_id.id in (8,16) and self.lang == False:
            msg = msg + ' - Language \n'
        if self.stage_id.id in (8, 16) and self.business_developer_id == False:
            msg = msg + ' - Business Developer \n'
        if self.stage_id.id in (8,16) and self.vat == False:
            msg = msg + ' - TIN \n'

        ## individual contact
        if self.stage_id.id  in (8,16) and self.parent_id and self.parent_id.street== False:
            msg = msg + ' - Invoicing Address (Company Adress) \n'
        if self.stage_id.id  in (8,16) and self.inami == False:
            msg = msg + ' - INAMI \n'
        if self.stage_id.id in (8,16) and self.subscription_type == False:
            msg = msg + ' - Subscription Type \n'
        if self.stage_id.id in (8,16) and not self.title and self.is_company != True:
            msg = msg + ' - Title \n'
        if self.stage_id.id in (8,16) and self.specialization == False:
            msg = msg + ' - Specialization \n'
        ### Prospection process
        if self.stage_id.id in (8,16) and self.date_signed == False:
            msg = msg + ' - Date(Signed) \n'
        if self.stage_id.id in (8, 16) and self.bd_signed == False:
            msg = msg + ' - Business Developer (Signed) \n'
        if self.stage_id.id in (8, 16) and self.comment_signed == False:
            msg = msg + ' - Comment (Signed) \n'

        ### Subscription details
        if self.stage_id.id in (8,16) and self.subscription_month == False:
            msg = msg + ' - Monthly subscription \n'
        if self.stage_id.id in (8,16) and self.subscription_commitment == False:
            msg = msg + ' - Commitment \n'
        if self.stage_id.id in (8,16) and self.subscription_upfront_payment == False:
            msg = msg + ' - Upfront Payment \n'
        if self.stage_id.id in (8,16) and self.subscription_upfront_turnover == False:
            msg = msg + ' - Upfront turnover \n'
        if self.stage_id.id in (8,16) and self.subsciption_part_condition == False:
            msg = msg + ' - Particular Conditions \n'

        ## stage activated and only individuals
        if self.stage_id.id == 16 and self.doctor_admin == False:
            msg = msg + ' - Doctor AdminID \n'
        ### stage account managment
        if  self.stage_id.id == 16 and self.first_email == False:
            msg = msg + ' - 1st email (activation) \n'
        if  self.stage_id.id == 16 and self.service_completed == False:
            msg = msg + ' - Services completed \n'
        if  self.stage_id.id == 16 and self.price_completed == False:
            msg = msg + ' - Prices completed \n'
        if  self.stage_id.id == 16 and self.cv_completed == False:
            msg = msg + ' - CV/experiences completed \n'
        if  self.stage_id.id == 16 and self.duration_completed == False:
            msg = msg + ' - Duration completed \n'
        if  self.stage_id.id == 16 and self.personal_message_completed == False:
            msg = msg + ' - Personal message completed \n'
        if  self.stage_id.id == 16 and self.profile_picture == False:
            msg = msg + ' - Profile picture \n'
        if  self.stage_id.id == 16 and self.photo_practice == False:
            msg = msg + ' - Photo Practice \n'
        if  self.stage_id.id == 16 and self.marketing_kit == False:
            msg = msg + ' - Marketing kit \n'
        if  self.stage_id.id == 16 and self.synchronisation_completed == False:
            msg = msg + ' - Synchronization \n'
        if  self.stage_id.id == 16 and self.backlink == False:
            msg = msg + ' - Backlink \n'
        if  self.stage_id.id == 16 and self.google_profile == False:
            msg = msg + ' - Google profile \n'
        if  self.stage_id.id == 16 and self.voicemail == False:
            msg = msg + ' - Voicemail \n'
        if  self.stage_id.id == 16 and self.mail_signature == False:
            msg = msg + ' - Mail signature \n'
        if  self.stage_id.id == 16 and self.email_to_patient == False:
            msg = msg + ' - Email to patient \n'
        if  self.stage_id.id == 16 and self.translation == False:
            msg = msg + ' - Translation \n'
        if  self.stage_id.id == 16 and self.business_card == False:
            msg = msg + ' - Manuel Sent \n'
        if  self.stage_id.id == 16 and self.manuel_sent == False:
            msg = msg + ' - Business cards \n'
        if  self.stage_id.id == 16 and self.widget == False:
            msg = msg + ' - Widget \n'
        if  self.stage_id.id == 16 and self.voice_mail == False:
            msg = msg + ' - Voicemail + email signature \n'
        if  self.stage_id.id == 16 and self.website_ok == False:
            msg = msg + ' - Website \n'
        if  self.stage_id.id == 16 and self.customer_service_number == False:
            msg = msg + ' - Customer service number on google profile  \n'
        if  self.stage_id.id == 16 and self.website_backlink == False:
            msg = msg + ' - Backlink on website \n'

        ## Lost paying, tab lost
        if  self.stage_id.id == 17 and self.date_lost == False:
            msg = msg + ' - Lost Date \n'
        if  self.stage_id.id == 17 and self.reason_lost == False:
            msg = msg + ' - Lost Reason \n'




       ##
        if msg:
            raise ValidationError('To move to this step you first need to fill those fields : \n' + msg)

        return {}

    @api.multi
    def _call_activity_create(self):
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
        list_attendees = [self.bd_meeting_set.partner_id.id,self.id]
        start_datetime = fields.Datetime.from_string(self.date_meeting_set)
        stop_datetime = fields.Datetime.to_string(start_datetime + timedelta(hours=1))
        stop = fields.Datetime.to_string(start_datetime + timedelta(hours=1))
        vals_calendar = {
            'name': self.name,
            'allday': False,
            'duration': 1,
            'start_datetime': self.date_meeting_set,
            'stop_datetime': stop_datetime,
            'start': self.date_meeting_set,
            'stop': stop,
            'description': self.comment_meeting_set,
            'partner_ids':[(6, 0, list_attendees)],

        }

        print('ok2----------------',vals_calendar)
        calendar_id = self.env['calendar.event'].create(vals_calendar)
        print('ok3-------',calendar_id)
        if calendar_id:
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
        print('0000')
        res = super(Partner, self).write(vals)
        if vals.get('stage_id'):
            vals.update(self._onchange_stage_id_values(vals.get('stage_id')))
        elif vals.get('state_target'):
            vals.update(self._onchange_contact_stage_id(vals.get('state_target')))
        elif vals.get('state_account'):
            vals.update(self._onchange_contact_stage_id(vals.get('state_account')))

        if vals.get('date_call_back_one'):
            vals.update(self._call_activity_create())
        if vals.get('date_meeting_set'):
            vals.update(self._meeting_activity_create())


        return res

        # vat constraint

    @api.constrains('vat')
    def check_vat_limit(self):
        for partner in self:
            if not partner.vat:
                continue
            if len(partner.vat) < 9:
                msg = 'The TIN must be at least 10 caracters"'
                raise ValidationError(msg)




