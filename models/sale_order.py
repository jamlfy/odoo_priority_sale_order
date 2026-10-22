import datetime

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    higher_priority = fields.Selection(
        [
            ("0", "Normal"),
            ("1", "High"),
        ],
        string="Priority",
        default="0",
        copy=False,
        index=True,
    )

    higher_disable_priority = fields.Boolean(
        string="Disable priority changes",
        compute="_compute_higher_disable_priority",
        store=False,
    )

    @api.model
    def _get_sale_order_states(self):
        return list(dict(self._fields["state"].selection).keys())

    @api.model
    def _get_current_user_group_ids(self):
        user = self.env.user
        group_field = "group_ids" if "group_ids" in user._fields else "groups_id"
        return set(user[group_field].ids)

    @api.model
    def _get_high_priority_config(self):
        param = self.env["ir.config_parameter"].sudo()
        available_states = self._get_sale_order_states()
        default_states = (
            ",".join(s for s in ("sale", "done") if s in available_states)
            or ",".join(available_states[:2])
            if available_states
            else "sale,done"
        )

        only_check = [
            s.strip()
            for s in param.get_param(
                "priority_sale_order.only_check_states", default_states
            ).split(",")
            if s.strip() and s.strip() in available_states
        ]

        if not only_check:
            only_check = available_states[:]

        try:
            max_times = int(
                param.get_param("priority_sale_order.max_times_high_priority", "3")
            )
        except (TypeError, ValueError):
            max_times = 3

        try:
            extra_days = float(param.get_param("priority_sale_order.days_offset", "1.0"))
        except (TypeError, ValueError):
            extra_days = 1.0

        start_offset = datetime.timedelta(days=extra_days)

        return {
            "only_check_states": only_check,
            "max_times": max_times,
            "start_offset": start_offset,
            "allowed_group_ids": {
                int(group_id.strip())
                for group_id in param.get_param(
                    "priority_sale_order.allowed_group_ids", ""
                ).split(",")
                if group_id.strip().isdigit()
            },
        }

    @api.depends_context("uid")
    @api.depends("state", "higher_priority", "create_date", "date_order")
    def _compute_higher_disable_priority(self):
        now = datetime.datetime.now()
        config = self._get_high_priority_config()

        only_check = config["only_check_states"]
        max_times = config["max_times"]
        start_offset = config["start_offset"]
        is_authorized = bool(
            config["allowed_group_ids"] & self._get_current_user_group_ids()
        )

        for record in self:
            if (
                not is_authorized
                or record.state not in only_check
                or record.state == "done"
            ):
                record.higher_disable_priority = True
                continue

            if record.higher_priority == "1":
                record.higher_disable_priority = False
                continue

            date_ref = record.create_date or record.date_order or now

            record_start = (
                datetime.datetime.combine(date_ref.date(), datetime.time.min)
                + start_offset
            )
            record_end = datetime.datetime.combine(record_start.date(), datetime.time.max)

            count = self.env["sale.order"].search_count(
                [
                    ("higher_priority", "=", "1"),
                    ("date_order", ">=", record_start),
                    ("date_order", "<=", record_end),
                    ("state", "in", only_check),
                ]
            )
            record.higher_disable_priority = count >= max_times

    @api.model
    def _user_can_set_higher_priority(self):
        config = self._get_high_priority_config()
        return bool(config["allowed_group_ids"] & self._get_current_user_group_ids())

    @api.model_create_multi
    def create(self, vals_list):
        if any(vals.get("higher_priority") == "1" for vals in vals_list):
            if not self._user_can_set_higher_priority():
                raise AccessError(
                    _("Only users in the configured groups can set high priority.")
                )
            for vals in vals_list:
                if vals.get("higher_priority") == "1":
                    candidate = self.new({**vals, "higher_priority": "0"})
                    self._check_high_priority_is_allowed(candidate)
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("higher_priority") == "1" and not self._user_can_set_higher_priority():
            raise AccessError(
                _("Only users in the configured groups can set high priority.")
            )
        if vals.get("higher_priority") == "1":
            self._check_high_priority_is_allowed(self)
        return super().write(vals)

    @api.model
    def _check_high_priority_is_allowed(self, orders):
        disabled_orders = orders.filtered("higher_disable_priority")
        if disabled_orders:
            raise UserError(
                _(
                    "High priority cannot be assigned because the order state is not eligible "
                    "or the configured limit has been reached."
                )
            )
