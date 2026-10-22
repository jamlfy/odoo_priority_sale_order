from odoo.tests import TransactionCase


class TestPrioritySaleOrderStock(TransactionCase):
    @staticmethod
    def _related_path(field):
        if isinstance(field.related, str):
            return tuple(field.related.split("."))
        return tuple(field.related)

    def test_picking_priority_is_a_stored_indexed_related_field(self):
        priority_field = self.env["stock.picking"]._fields["higher_priority"]

        self.assertEqual(
            self._related_path(priority_field), ("sale_id", "higher_priority")
        )
        self.assertTrue(priority_field.store)
        self.assertTrue(priority_field.index)

    def test_stock_move_and_move_line_expose_sales_priority(self):
        move_priority = self.env["stock.move"]._fields["higher_priority"]
        move_line_priority = self.env["stock.move.line"]._fields["higher_priority"]

        self.assertEqual(
            self._related_path(move_priority),
            ("sale_line_id", "order_id", "higher_priority"),
        )
        self.assertEqual(
            self._related_path(move_line_priority),
            ("move_id", "sale_line_id", "order_id", "higher_priority"),
        )

    def test_picking_list_defaults_to_priority_then_scheduled_date(self):
        view_arch = self.env.ref(
            "priority_sale_order.stock_picking_tree_inherit_higher_priority"
        ).arch_db

        self.assertIn(
            "higher_priority desc, scheduled_date asc",
            view_arch,
        )

    def test_priority_is_added_to_sales_and_picking_views(self):
        view_xmlids = (
            "priority_sale_order.sale_order_tree_inherit_higher_priority",
            "priority_sale_order.sale_quotation_tree_inherit_higher_priority",
            "priority_sale_order.stock_picking_tree_inherit_higher_priority",
            "priority_sale_order.view_picking_form_inherit_higher_priority",
            "priority_sale_order.view_stock_move_line_operation_tree_inherit_higher_priority",
            "priority_sale_order.view_stock_move_line_detailed_operation_tree_inherit_higher_priority",
        )

        for xmlid in view_xmlids:
            with self.subTest(view=xmlid):
                self.assertIn("higher_priority", self.env.ref(xmlid).arch_db)
