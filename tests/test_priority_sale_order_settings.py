from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestPrioritySaleOrderSettings(TransactionCase):
    def test_state_options_are_synchronized_from_sale_order(self):
        settings_model = self.env["res.config.settings"]
        state_options = settings_model._sync_priority_sale_order_states()
        expected_codes = set(self.env["sale.order"]._get_sale_order_states())

        self.assertEqual(set(state_options.mapped("code")), expected_codes)

    def test_selected_states_and_groups_are_saved_as_parameters(self):
        settings_model = self.env["res.config.settings"]
        states = settings_model._sync_priority_sale_order_states().filtered(
            lambda state: state.code in ("sale", "done")
        )
        group = self.env.ref("sales_team.group_sale_manager")
        settings = settings_model.create(
            {
                "priority_sale_order_only_check_states": [Command.set(states.ids)],
                "priority_sale_order_group_ids": [Command.set(group.ids)],
            }
        )

        settings.set_values()

        params = self.env["ir.config_parameter"].sudo()
        self.assertEqual(
            set(params.get_param("priority_sale_order.only_check_states").split(",")),
            set(states.mapped("code")),
        )
        self.assertEqual(
            params.get_param("priority_sale_order.allowed_group_ids"), str(group.id)
        )

    def test_invalid_state_option_is_rejected(self):
        state = self.env["priority.sale.order.state"].sudo().create(
            {"name": "Invalid state", "code": "not_a_sale_order_state"}
        )
        with self.assertRaises(ValidationError):
            self.env["res.config.settings"].create(
                {"priority_sale_order_only_check_states": [Command.set(state.ids)]}
            )
