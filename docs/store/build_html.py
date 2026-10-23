#!/usr/bin/env python3
"""Build standalone, Odoo-inspired HTML pages from the store Markdown files."""

from __future__ import annotations

import argparse
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "html"
TEMPLATES_DIR = HERE / "templates"
STYLES_PATH = HERE / "static" / "styles.css"
SITE_NAME = "Priority Sale Order"
LANGUAGES = {
    "en": {
        "file": "en.md",
        "output": "index.html",
        "label": "English",
        "locale": "en",
        "title": "Priority Sale Order",
        "eyebrow": "Odoo module · Store documentation",
        "footer": "Priority Sale Order · Documentation",
        "sidebar_copy": "Built for Odoo stores and delivery teams.",
        "sidebar_label": "Odoo editions",
        "source_label": "Source",
        "source_link": "Read the Markdown version",
    },
    "es": {
        "file": "es.md",
        "output": "es.html",
        "label": "Español",
        "locale": "es",
        "title": "Prioridad de pedidos de venta",
        "eyebrow": "Módulo de Odoo · Documentación de tienda",
        "footer": "Priority Sale Order · Documentación",
        "sidebar_copy": "Pensado para tiendas y equipos de reparto que usan Odoo.",
        "sidebar_label": "Versiones de Odoo",
        "source_label": "Fuente",
        "source_link": "Leer la versión en Markdown",
    },
    "pt_BR": {
        "file": "pt_BR.md",
        "output": "pt_BR.html",
        "label": "Português (Brasil)",
        "locale": "pt-BR",
        "title": "Prioridade de pedidos de venda",
        "eyebrow": "Módulo Odoo · Documentação da loja",
        "footer": "Priority Sale Order · Documentação",
        "sidebar_copy": "Feito para lojas e equipes de entrega que usam Odoo.",
        "sidebar_label": "Versões do Odoo",
        "source_label": "Fonte",
        "source_link": "Ler a versão em Markdown",
    },
}


def render_page(language: str, store_listing: bool = False) -> str:
    info = LANGUAGES[language]
    source_path = HERE / info["file"]
    parser = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"])
    source = source_path.read_text(encoding="utf-8").splitlines()
    if source and source[0].startswith("# "):
        source = source[1:]
    body = parser.convert("\n".join(source))

    environment = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html"]),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = environment.get_template("page.html")
    return template.render(
        body=body,
        language=info,
        language_code=language,
        languages=LANGUAGES,
        site_name=SITE_NAME,
        store_listing=store_listing,
        styles=STYLES_PATH.read_text(encoding="utf-8"),
    )


def main() -> None:
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument(
        "--language",
        choices=["all", *LANGUAGES],
        default="all",
        help="Language to build (default: all).",
    )
    arg_parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Directory for generated HTML files.",
    )
    arg_parser.add_argument(
        "--store-listing",
        action="store_true",
        help="Omit links to Markdown sources for packaged Odoo Apps descriptions.",
    )
    args = arg_parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    languages = LANGUAGES if args.language == "all" else [args.language]
    for language in languages:
        destination = args.output_dir / LANGUAGES[language]["output"]
        destination.write_text(
            render_page(language, store_listing=args.store_listing),
            encoding="utf-8",
        )
        print(f"Generated {destination}")


if __name__ == "__main__":
    main()
