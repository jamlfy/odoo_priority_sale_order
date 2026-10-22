# Priority Sale Order

**Manage high-priority sales orders with a configurable period limit.**

## Overview

Priority Sale Order adds a selector to the sales order form so each order can be marked **Normal** or **High**. It lets you limit how many orders can receive high priority during a configured period, helping sales teams distribute priority handling.

The module grew out of a practical need in retail stores: some orders need their shipment or delivery handled ahead of others, while the capacity to prepare and dispatch orders is limited. Without a clear way to identify those sales, teams can lose track of urgent deliveries or end up treating too many orders as top priority.

Priority Sale Order lets the sales team flag orders that need priority handling and gives each store a way to manage that capacity. Administrators configure the maximum number of orders that can receive high priority and the time period used to apply that limit. Each store can therefore adapt the control to its workload and to how often it organizes order preparation, shipments, or deliveries.

The priority is visible on sales orders, their related transfers, and transfer operation lines, helping teams identify urgent deliveries during follow-up and preparation. Administrators can also choose which sales order states take part in the limit check and which user groups are allowed to assign high priority. Sales and operations teams can then work from the same visible signal and shared criteria when organizing urgent deliveries.

## Features

- Mark each sales order as normal or high priority and show that value in order, quotation, and linked transfer lists.
- Display the linked order's priority on its transfer operation lines and detailed operation lines.
- Sort picking and delivery lists with high-priority transfers first, then by scheduled date.
- Show priority on the sales order form and prevent changes when the order state is not enabled, the limit has been reached, or the order is done.
- Configure participating order states, the maximum number of high-priority orders, and the period day offset.

## Requirements

- Odoo 17.0, 18.0, 19.0, and 20.0
- Sales and Inventory applications (`sale_stock`)

## Installation and use

1. Install `priority_sale_order` from Apps.
2. Open a quotation or sales order.
3. Use the **Priority** selector to choose **Normal** or **High**, when changes are allowed.

## Configuration

Configure the module under **Settings → Priority Sale Order**. All control parameters are managed in this section and stored as system parameters. Only users in the selected groups can assign high priority; the Sales Administrator group is selected by default.

| Setting | Default | Purpose |
|---|---:|---|
| Included states | `sale`, `done` | Select one or more states defined by the `sale.order` model. |
| High-priority limit | `3` | Maximum number of high-priority orders in the period. |
| Period day offset | `1.0` day | Day offset used to determine the period being checked. |

Orders in the **Done** state are always locked. Orders whose states are not listed in `only_check_states` are also locked; with the default configuration, cancelled orders are excluded from the check.
