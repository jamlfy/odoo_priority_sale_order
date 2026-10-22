# Priority Sale Order

Odoo addon that adds a normal/high priority selector to sales orders, displays it in sales order and picking lists and on linked picking operation lines, and limits how many orders can receive high priority in a configured period.

Compatible with Odoo 17, 18, 19, and 20.

Picking and delivery lists show high-priority transfers first and sort each priority group by scheduled date.

This module was created to address a common need in stores: some shipments and deliveries must be handled ahead of others, while preparation and dispatch capacity is limited. It gives sales teams a clear way to mark those orders and helps prevent high priority from being applied to more orders than the store can manage at once.

Each store can configure the maximum number of high-priority sales orders and the time period over which that limit applies. Priority is carried through to related transfers and their operation lines, so sales and operations can recognize urgent deliveries during follow-up and preparation. Administrators can also select the sales order states included in the limit check and restrict priority assignment to chosen user groups.

The addon interface uses English by default. Settings let administrators select the sales order states included in the limit check and choose which user groups can assign high priority.

Store listing content is maintained in Markdown by language:

- [Español](docs/store/es.md)
- [English](docs/store/en.md)
- [Português (Brasil)](docs/store/pt_BR.md)

The HTML presentation generator is planned separately; these Markdown files are the source content.
