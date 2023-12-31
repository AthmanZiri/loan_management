from odoo import models, fields, api
from datetime import datetime

class MemberContribution(models.Model):
    _name = 'member.contribution'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Member Contributions'
    _order = 'name, date desc'

    name = fields.Many2one('res.partner',string="Name",default=lambda self: self.env.user.partner_id.id)
    member_account_id = fields.Many2one('member.account', string="Account")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        related='company_id.currency_id', readonly=True)
    date = fields.Date(string="Date", default=datetime.today().date())
    amount = fields.Monetary(currency_field='currency_id')
    state = fields.Selection([('draft',"Draft"),
                              ('process', "Processing"),
                              ('validate', "Validated")
                              ],default='draft', string="State", tracking=True)
    active = fields.Boolean(string="Active", default=True)

    def action_submit(self):
        self.state = 'process'

    def action_validate(self):
        for rec in self:
            rec.state = 'validate'

    def action_create_contribution_payment(self):
        for rec in self:
            payment_obj = self.env['loan.payment']

            payment_obj.create({
                'payment_type_code': 'CONTRIBUTION',
                'member_id': rec.member_account_id.id,
                'amount': rec.amount,
                'date': rec.date,
                'state': 'validate',
            })