# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Helpdesk Ticket Hide Parent Automatic",
    "version": "12.0.1.0.0",
    "summary": """
        Hide the email send and reply features for Helpdesk tickets.
        Only when `Helpdesk Automatic Stage Changes` and `Mass Parent Ticket Generation`
        modules are installed.
    """,
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Helpdesk",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "depends": [
        "helpdesk_mgmt",
        "helpdesk_automatic_stage_changes",
        "helpdesk_ticket_parent",
    ],
    "data": [
        "views/helpdesk_ticket_view.xml",
    ],
    "application": False,
    "installable": True,
}
