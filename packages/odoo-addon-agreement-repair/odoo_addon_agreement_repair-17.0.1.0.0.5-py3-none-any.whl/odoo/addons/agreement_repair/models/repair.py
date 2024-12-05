# Copyright (C) 2021 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Repair(models.Model):
    _inherit = "repair.order"

    agreement_id = fields.Many2one("agreement", "Agreement")
