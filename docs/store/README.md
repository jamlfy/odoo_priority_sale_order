# Store documentation builder

The Markdown files in this directory are the editable source for the store listings. `build_html.py` converts them to standalone HTML pages with a responsive layout inspired by Odoo's purple palette, typography, and card-based interface.

## Requirements

Install the Python Markdown dependency:

```bash
python3 -m pip install -r docs/store/requirements.txt
```

## Build all languages

From the repository root, run:

```bash
python3 docs/store/build_html.py
```

This generates:

- `docs/store/html/index.html` for English
- `docs/store/html/es.html` for Spanish
- `docs/store/html/pt_BR.html` for Brazilian Portuguese

Each page is self-contained, including its styles, and links to the other language versions.

## Build one language or choose an output directory

```bash
python3 docs/store/build_html.py --language es
python3 docs/store/build_html.py --language pt_BR --output-dir /tmp/priority-sale-order-pages
```

Use `--language en`, `--language es`, or `--language pt_BR`. If omitted, all languages are built. The default output directory is `docs/store/html/`.

After editing any `*.md` source, run the builder again to refresh the HTML pages.

## Build descriptions for Odoo Apps

From the repository root, generate the localized, standalone descriptions in the addon's expected location:

```bash
python3 docs/store/build_html.py --store-listing --output-dir static/description
```

The English page is `static/description/index.html`; Spanish and Brazilian Portuguese are generated beside it.
Create the store packages with `python3 tools/package_store.py` after adding the icon and screenshots.
