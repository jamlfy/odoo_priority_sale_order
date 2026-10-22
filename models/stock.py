from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    higher_priority = fields.Selection(
        related="sale_id.higher_priority",
        string="Priority",
        readonly=True,
        store=True,
        index=True,
    )


class StockMove(models.Model):
    _inherit = "stock.move"

    higher_priority = fields.Selection(
        related="sale_line_id.order_id.higher_priority",
        string="Priority",
        readonly=True,
    )


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    higher_priority = fields.Selection(
        related="move_id.sale_line_id.order_id.higher_priority",
        string="Priority",
        readonly=True,
    )
