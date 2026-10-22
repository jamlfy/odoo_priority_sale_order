# Priority Sale Order

Odoo addon that adds a normal/high priority selector to sales orders, displays it in sales order and picking lists and on linked picking operation lines, and limits how many orders can receive high priority in a configured period.

Compatible with Odoo 17, 18, 19, and 20.

Picking and delivery lists show high-priority transfers first and sort each priority group by scheduled date.

This module was created to address a common need in stores: some shipments and deliveries must be handled ahead of others, while preparation and dispatch capacity is limited. It gives sales teams a clear way to mark those orders and helps prevent high priority from being applied to more orders than the store can manage at once.

Each store can configure the maximum number of high-priority sales orders and the time period over which that limit applies. Priority is carried through to related transfers and their operation lines, so sales and operations can recognize urgent deliveries during follow-up and preparation. Administrators can also select the sales order states included in the limit check and restrict priority assignment to chosen user groups.

The addon interface uses English by default. Settings let administrators select the sales order states included in the limit check and choose which user groups can assign high priority.

## Run with Podman or Docker

The repository includes a Compose stack for Odoo and PostgreSQL. Podman is the default:

```bash
make up
```

To use Docker instead:

```bash
make up ENGINE=docker
```

Open [http://localhost:8069](http://localhost:8069), create an Odoo database, enable developer mode, update the Apps list, clear the default Apps filter if needed, and install **Priority Sale Order**. The addon is mounted into the Odoo container and PostgreSQL data persists in a named volume. Choose an Odoo version with `ODOO_VERSION=17.0 make up` (also supports `18.0`, `19.0`, and `20.0`). Use `make down` to stop the stack without deleting database data; `make logs` follows the container logs.

If using Podman, install a Compose provider supported by `podman compose`.

Store listing content is maintained in Markdown by language:

- [Español](docs/store/es.md)
- [English](docs/store/en.md)
- [Português (Brasil)](docs/store/pt_BR.md)

Build the standalone Odoo-styled HTML pages from the Markdown sources with:

```bash
python3 -m pip install -r docs/store/requirements.txt
python3 docs/store/build_html.py
```

The generated pages are written to `docs/store/html/`. See [the store documentation guide](docs/store/README.md) for language-specific and custom output options.
