from odoo import api, fields, models
from datetime import date


class StudentPayment(models.Model):
    _name = "student.payment"
    _description = 'Student Payment'

    payment_date = fields.Date(string="Date", default=date.today())
    student_code_id = fields.Many2one('op.student', 'student_code')
    student_payment = fields.Integer(string="Amount")
    memo = fields.Char(string="Memo")
