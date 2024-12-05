from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = "mail.message"

    has_global_ticket = fields.Boolean(
        string="Has Global Ticket",
        compute="_compute_has_global_ticket"
    )

    @api.one
    @api.depends('res_id', 'model')
    def _compute_has_global_ticket(self):
        if self.res_id and self.model == "helpdesk.ticket":
            self.has_global_ticket = bool(self.env['helpdesk.ticket'].browse(self.res_id).global_child_ticket_ids_count)
        else:
            self.has_global_ticket = False
