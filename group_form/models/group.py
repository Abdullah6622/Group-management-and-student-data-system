from odoo import api, fields, models, _
from datetime import date


class GroupCode(models.Model):
    _name = "group.code"
    _description = 'Groups'
    _rec_name = "group_code"

    group_code = fields.Char(string='Group Name', required=True, tracking=True)
    number_of_days = fields.Integer(string="Number Of Days", default=2)
    from_hour = fields.Float(string='From', required=True)
    to_hour = fields.Float(string='To', required=True)
    name_ids = fields.Many2many('week.days', 'name')
    students_names_id = fields.One2many('op.student', 'group_code_id')

    def name_get(self):
        result = []
        for rec in self:
            record_id = str(rec.group_code)
            from_hours = str(rec.from_hour)
            to_hours = str(rec.to_hour)
            display_everything = record_id + ' ' + from_hours + ' ' + to_hours
            result.append((rec.id, display_everything))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        rec = self.browse()
        if not rec:
            rec = self.search(['|', '|', ('group_code', operator, name), ('from_hour', operator, name),
                               ('to_hour', operator, name)] + args, limit=limit)
        return rec.name_get()


class StudentDetails(models.Model):
    _inherit = 'op.student'
    _description = "Student Details"
    _rec_name = 'student_code'

    group_code_id = fields.Many2one('group.code')
    student_code = fields.Char(string="Student Code", readonly=True)
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Gender', required=False, default='m')
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=False, ondelete="cascade")
    mobile = fields.Char(required=False)
    parent_mobile_no = fields.Char(required=False)
    email = fields.Char(required=False)
    birth_date = fields.Date(required=False)
    attendance_ids = fields.One2many('student.attendance', 'attendance_id')
    payment_ids = fields.One2many('student.payment', 'student_code_id')

    @api.model
    def create(self, vals):
        vals['student_code'] = self.env['ir.sequence'].next_by_code('op.student')
        return super(StudentDetails, self).create(vals)

    def write(self, vals):
        if not self.student_code and not vals.get('student_code'):
            vals['student_code'] = self.env['ir.sequence'].next_by_code('op.student')
        return super(StudentDetails, self).write(vals)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            return record

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name)

        else:
            self.name = str(self.first_name)

    def name_get(self):
        results = []
        for rec in self:
            rec_id = str(rec.student_code)
            name = rec.name
            display_name = rec_id + ' ' + name
            results.append((rec.id, display_name))
        return results

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search([('student_code', operator, name)] + args, limit=limit)
        return recs.name_get()
