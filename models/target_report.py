# -*- coding: utf-8 -*-

from odoo import api, fields, models

class TargetReport(models.Model):
    _name = 'target.report'

    name = fields.Char('Year')
    target_month = fields.Selection(
        selection=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'),
                   (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')],
        string='Month')
    target_number = fields.Float('Target')
    target_bd = fields.Float('#BD')
