from odoo import api, fields, models, _


class WeekDays(models.Model):
    _name = 'week.days'
    _description = 'Days of the Week'

    name = fields.Char(string="Days", tracking=True)
