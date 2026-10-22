from odoo import Command, fields
from odoo.exceptions import AccessError, UserError
from odoo.tests import TransactionCase


class TestPrioritySaleOrder(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_manager = cls.env.ref("sales_team.group_sale_manager")
        cls.partner = cls.env["res.partner"].create({"name": "Priority Test Customer"})
        cls.authorized_user = cls._create_user("priority_authorized", [cls.group_manager.id])
        cls.unauthorized_user = cls._create_user(
            "priority_unauthorized", [cls.env.ref("sales_team.group_sale_salesman").id]
        )

    @classmethod
    def _create_user(cls, login, group_ids):
        user_model = cls.env["res.users"].sudo().with_context(no_reset_password=True)
        groups_field = "group_ids" if "group_ids" in user_model._fields else "groups_id"
        return user_model.create(
            {
                "name": login,
                "login": login,
                groups_field: [Command.set(group_ids)],
            }
        )

    def setUp(self):
        super().setUp()
        params = self.env["ir.config_parameter"].sudo()
        params.set_param("priority_sale_order.allowed_group_ids", str(self.group_manager.id))
        params.set_param("priority_sale_order.only_check_states", "sale")
        params.set_param("priority_sale_order.max_times_high_priority", "3")
        params.set_param("priority_sale_order.days_offset", "0")

    def _make_order(self, user=None, state="sale", higher_priority="0"):
        user = user or self.authorized_user
        return self.env["sale.order"].with_user(user).create(
            {
                "partner_id": self.partner.id,
                "state": state,
                "date_order": fields.Datetime.now(),
                "higher_priority": higher_priority,
            }
        )

    def test_available_states_come_from_sale_order(self):
        states = self.env["sale.order"]._get_sale_order_states()
        self.assertIn("sale", states)
        selection = self.env["sale.order"]._fields["state"].selection
        if callable(selection):
            selection = selection(self.env["sale.order"])
        self.assertEqual(states, list(dict(selection)))
        self.assertEqual(len(states), len(set(states)))

    def test_priority_is_enabled_for_authorized_user_and_included_state(self):
        order = self._make_order()
        self.assertFalse(order.higher_disable_priority)

    def test_priority_is_disabled_for_unauthorized_user(self):
        order = self._make_order(user=self.unauthorized_user)
        self.assertTrue(order.higher_disable_priority)

    def test_priority_is_disabled_outside_configured_state(self):
        order = self._make_order(state="draft")
        self.assertTrue(order.higher_disable_priority)

    def test_done_orders_are_always_disabled(self):
        if "done" not in self.env["sale.order"]._get_sale_order_states():
            self.skipTest("This Odoo version does not define a done sales order state.")
        self.env["ir.config_parameter"].sudo().set_param(
            "priority_sale_order.only_check_states", "sale,done"
        )
        order = self._make_order(state="done")
        self.assertTrue(order.higher_disable_priority)

    def test_priority_is_disabled_after_limit_is_reached(self):
        params = self.env["ir.config_parameter"].sudo()
        params.set_param("priority_sale_order.max_times_high_priority", "1")
        self._make_order(higher_priority="1")
        order = self._make_order()
        self.assertTrue(order.higher_disable_priority)

    def test_unauthorized_user_cannot_assign_priority_on_create_or_write(self):
        with self.assertRaises(AccessError):
            self._make_order(user=self.unauthorized_user, higher_priority="1")

        order = self._make_order()
        with self.assertRaises(AccessError):
            order.with_user(self.unauthorized_user).write({"higher_priority": "1"})

    def test_ineligible_state_cannot_be_prioritized_on_create_or_write(self):
        with self.assertRaises(UserError):
            self._make_order(state="draft", higher_priority="1")

        order = self._make_order(state="draft")
        with self.assertRaises(UserError):
            order.write({"higher_priority": "1"})

    def test_priority_limit_is_enforced_on_create_and_write(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "priority_sale_order.max_times_high_priority", "1"
        )
        first_order = self._make_order(higher_priority="1")
        second_order = self._make_order()

        with self.assertRaises(UserError):
            self._make_order(higher_priority="1")
        with self.assertRaises(UserError):
            second_order.write({"higher_priority": "1"})

        self.assertEqual(first_order.higher_priority, "1")
        self.assertEqual(second_order.higher_priority, "0")

    def test_invalid_state_configuration_falls_back_to_available_states(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "priority_sale_order.only_check_states", "invalid_state"
        )

        config = self.env["sale.order"]._get_high_priority_config()

        self.assertEqual(
            set(config["only_check_states"]),
            set(self.env["sale.order"]._get_sale_order_states()),
        )

    def test_invalid_numeric_configuration_uses_safe_defaults(self):
        params = self.env["ir.config_parameter"].sudo()
        params.set_param("priority_sale_order.max_times_high_priority", "invalid")
        params.set_param("priority_sale_order.days_offset", "invalid")

        config = self.env["sale.order"]._get_high_priority_config()

        self.assertEqual(config["max_times"], 3)
        self.assertEqual(config["start_offset"].days, 1)
