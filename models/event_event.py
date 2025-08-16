from odoo import api, fields, models
import pytz

class EventEvent(models.Model):
    _inherit = 'event.event'  # or _name = 'event.event' if defining from scratch
    _description = 'الرحلة السياحية'

    def _tz_get(self):
        """ Returns a list of timezones for the selection field """
        return [(tz, tz) for tz in sorted(pytz.all_timezones)]

    date_tz = fields.Selection(
        string='Timezone',
        selection='_tz_get',
        default=lambda self: self.env.user.tz or 'UTC',
        required=True,
        help="Timezone where the event takes place."
    )


    # ربط بقالب العرض (الباقة)
    package_template_id = fields.Many2one(
        'sale.order',
        string='القالب السعري',
        domain="[('sale_order_line_ids', '!=', False)]",
        help="اختر قالبًا مسبق التعريف للباقة."
    )

    # أنواع المدة
    duration_type = fields.Selection([
        ('7+7', '7+7 أيام'),
        ('11+3', '11+3 أيام'),
        ('custom', 'مخصص')
    ], string='خطة المدة', default='7+7')

    # أنواع الغرف
    room_type = fields.Selection([
        ('double', 'مزدوجة'),
        ('triple', 'ثلاثية'),
        ('quad', 'رباعية'),
        ('quint', 'خماسية'),
    ], string='نوع الغرفة', default='double')

    # السعر من القالب
    package_price = fields.Monetary(
        string='سعر الباقة',
        compute='_compute_package_price',
        readonly=True
    )

    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

