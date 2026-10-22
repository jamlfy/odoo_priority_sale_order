from odoo import fields, models


class PrioritySaleOrderState(models.Model):
    _name = "priority.sale.order.state"
    _description = "Sales Order State for Priority Limit"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, index=True)
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ("priority_sale_order_state_code_unique", "unique(code)", "State codes must be unique."),
    ]
