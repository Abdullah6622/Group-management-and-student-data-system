from odoo import api, fields, models, _
from datetime import date


class StudentAttendance(models.Model):
    _name = 'student.attendance'
    _description = 'Attendance of students'

    a_date = fields.Date(string="Date", default=date.today())
    attendance_id = fields.Many2one('op.student')
    student_marks = fields.Float(string='Marks', group_operator="avg")
    memo = fields.Char(string="Memo")
