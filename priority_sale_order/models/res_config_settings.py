from odoo import Command, api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    priority_sale_order_group_ids = fields.Many2many(
        comodel_name="res.groups",
        string="Groups allowed to assign high priority",
    )
    priority_sale_order_only_check_states = fields.Many2many(
        comodel_name="priority.sale.order.state",
        relation="priority_sale_order_settings_state_rel",
        column1="settings_id",
        column2="state_id",
        string="States included in the limit check",
        help="Select the sales order states included in the high-priority limit check.",
    )
    priority_sale_order_max_times_high_priority = fields.Integer(
        string="Maximum number of high-priority orders",
        default=3,
        config_parameter="priority_sale_order.max_times_high_priority",
        help="Maximum number of high-priority orders allowed during the configured period.",
    )
    priority_sale_order_days_offset = fields.Float(
        string="Period day offset",
        default=1.0,
        config_parameter="priority_sale_order.days_offset",
        help="Day offset used to determine the period for counting orders.",
    )

    @api.model
    def _sync_priority_sale_order_states(self):
        State = self.env["priority.sale.order.state"].sudo()
        selection = self.env["sale.order"]._fields["state"].selection
        if callable(selection):
            selection = selection(self.env["sale.order"])
        current = dict(selection)
        existing = {state.code: state for state in State.search([])}
        for code, label in current.items():
            vals = {"code": code, "name": str(label)}
            if code in existing:
                existing[code].write(vals)
            else:
                State.create(vals)
        stale = State.search([("code", "not in", list(current))]) if current else State.search([])
        stale.unlink()
        return State.search([("code", "in", list(current))])

    @api.model
    def get_values(self):
        values = super().get_values()
        states = self._sync_priority_sale_order_states()
        raw_states = self.env["ir.config_parameter"].sudo().get_param(
            "priority_sale_order.only_check_states", "sale"
        )
        selected_codes = {code.strip() for code in raw_states.split(",") if code.strip()}
        values["priority_sale_order_only_check_states"] = [
            Command.set(states.filtered(lambda state: state.code in selected_codes).ids)
        ]
        raw_group_ids = self.env["ir.config_parameter"].sudo().get_param(
            "priority_sale_order.allowed_group_ids", ""
        )
        group_ids = [
            int(group_id.strip())
            for group_id in raw_group_ids.split(",")
            if group_id.strip().isdigit()
        ]
        values["priority_sale_order_group_ids"] = [Command.set(group_ids)]
        return values

    def set_values(self):
        super().set_values()
        group_ids = ",".join(str(group_id) for group_id in self.priority_sale_order_group_ids.ids)
        self.env["ir.config_parameter"].sudo().set_param(
            "priority_sale_order.allowed_group_ids", group_ids
        )
        state_codes = ",".join(self.priority_sale_order_only_check_states.mapped("code"))
        self.env["ir.config_parameter"].sudo().set_param(
            "priority_sale_order.only_check_states", state_codes
        )

    @api.constrains("priority_sale_order_only_check_states")
    def _check_priority_sale_order_states(self):
        valid_states = set(self.env["sale.order"]._get_sale_order_states())
        for settings in self:
            selected_states = set(settings.priority_sale_order_only_check_states.mapped("code"))
            invalid_states = selected_states - valid_states
            if invalid_states:
                raise ValidationError(
                    _(
                        "Selected values must be states defined on sales orders. "
                        "Invalid values: %(states)s",
                        states=", ".join(sorted(invalid_states)),
                    )
                )
