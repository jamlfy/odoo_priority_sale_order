{
    "name": "Priority Sale Order",
    "version": "19.0.1.4.2",
    "summary": "Prioritize sales orders and deliveries with configurable volume and time limits.",
    "description": "Created for stores that need to prioritize selected shipments and deliveries. Sales teams can choose how many sales orders may receive high priority during each configured time period.",
    "category": "Sales/Sales",
    "author": "Jam <j4mlfy@gmail.com>",
    "license": "LGPL-3",
    "images": [
        "static/description/main_screenshot.png",
        "static/description/sale_order.png",
        "static/description/picking.png",
        "static/description/settings.png",
    ],
    "depends": [
        "sale_stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "views/res_config_settings_views.xml",
        "data/ir_config_parameter_data.xml",
    ],
    "installable": True,
    "application": False,
}
