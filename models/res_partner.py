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


class Partner(models.Model):

    _inherit = 'res.partner'


    def _default_stage_id(self):
        return self.env['crm.stage'].search([], limit=1).id


    stage_id = fields.Many2one('crm.stage', string='Status', index=True, track_visibility='onchange' , group_expand='_read_group_all_states' , default=lambda self: self._default_stage_id())

    state_contact= fields.Many2one('crm.stage', related='stage_id' ,string='Status',
         group_expand='_read_group_contact_states', store=True, track_visibility=False)
    state_target = fields.Many2one('crm.stage', related='stage_id', string='Status',
         group_expand='_read_group_target_states', store=True, track_visibility=False)

    state_account = fields.Many2one('crm.stage', related='stage_id', string='Status',
         group_expand='_read_group_account_states', store=True, track_visibility=False)

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

        elif self.stage_id.id == 3 and self.x_studio_field_8wWZX == False  and self.x_studio_JqT0t == False:
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

        elif self.stage_id.id in (8,16) and self.x_studio_field_EfIaw == False:
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

        elif self.stage_id.id in (8,16) and self.x_studio_field_Ca1DT == False:
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

        if not self.env.user.has_group('sales_team.group_sale_manager') and self.stage_id.id == 16 :
            raise exceptions.Warning(
                _('You are not allowed to pass to Stage Activated, Please contact Administrator'))

        return {}

    # @api.onchange('stage_id')
    # def _onchange_stage_id(self):
    #     print('------1')
    #     values = self._onchange_stage_id_values(self.stage_id.id)
    #     self.update(values)


    @api.multi
    def write(self, vals):
        res = super(Partner, self).write(vals)
        if vals.get('stage_id'):
            vals.update(self._onchange_stage_id_values(vals.get('stage_id')))

        return res




