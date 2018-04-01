# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Meeting(models.Model):
    _inherit = 'calendar.event'

    event_type_activity = fields.Many2one('mail.activity.type', 'Type', default=3)



