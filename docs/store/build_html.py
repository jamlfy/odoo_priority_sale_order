#!/usr/bin/env python3
"""Build standalone, Odoo-inspired HTML pages from the store Markdown files."""

from __future__ import annotations

import argparse
from pathlib import Path

import markdown


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "html"
LANGUAGES = {
    "en": {"file": "en.md", "output": "index.html", "label": "English", "locale": "en"},
    "es": {"file": "es.md", "output": "es.html", "label": "Español", "locale": "es"},
    "pt_BR": {
        "file": "pt_BR.md",
        "output": "pt_BR.html",
        "label": "Português (Brasil)",
        "locale": "pt-BR",
    },
}

STYLES = """
:root {
  color-scheme: light;
  --odoo-purple: #714b67;
  --odoo-purple-dark: #503348;
  --odoo-purple-pale: #f3edf2;
  --odoo-orange: #e46e3a;
  --ink: #29252c;
  --muted: #6f6a70;
  --line: #e9e5e8;
  --paper: #fff;
  --canvas: #f7f6f7;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--canvas);
  color: var(--ink);
  font: 16px/1.7 Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
a { color: var(--odoo-purple); text-decoration-thickness: 1px; text-underline-offset: 3px; }
a:hover { color: var(--odoo-purple-dark); }
.topbar {
  min-height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 12px max(24px, calc((100vw - 1180px) / 2));
  background: var(--odoo-purple-dark);
  color: white;
}
.brand { display: inline-flex; align-items: center; gap: 11px; color: white; font-weight: 700; text-decoration: none; letter-spacing: -.02em; }
.brand-mark {
  display: grid; place-items: center; width: 34px; height: 34px; border-radius: 11px;
  background: white; color: var(--odoo-purple); font-weight: 850; font-size: 19px;
}
.languages { display: flex; flex-wrap: wrap; gap: 6px; }
.languages a { padding: 7px 11px; border-radius: 8px; color: #f1eaf0; font-size: 13px; text-decoration: none; }
.languages a:hover, .languages a[aria-current="page"] { background: #ffffff20; color: white; }
.hero {
  overflow: hidden;
  background: radial-gradient(ellipse at 85% 5%, #9a6b8d 0, transparent 35%), linear-gradient(125deg, #503348, #714b67 72%, #805573);
  color: white;
}
.hero-inner { max-width: 1180px; margin: 0 auto; padding: 72px 28px 78px; }
.eyebrow { margin: 0 0 14px; color: #f6c7a7; font-size: 12px; font-weight: 750; letter-spacing: .16em; text-transform: uppercase; }
.hero h1 { max-width: 820px; margin: 0; color: white; font-size: clamp(42px, 7vw, 76px); line-height: 1.03; letter-spacing: -.055em; }
.hero p { max-width: 680px; margin: 23px 0 0; color: #f2eaf1; font-size: clamp(17px, 2.4vw, 21px); }
.hero-rule { width: 58px; height: 4px; margin-top: 30px; border-radius: 4px; background: var(--odoo-orange); }
.layout { display: grid; grid-template-columns: minmax(0, 790px) 260px; gap: 34px; max-width: 1180px; margin: -28px auto 0; padding: 0 28px 70px; align-items: start; }
.article, .side-card { border: 1px solid var(--line); border-radius: 15px; background: var(--paper); box-shadow: 0 12px 36px #38233a0c; }
.article { padding: clamp(26px, 5vw, 54px); }
.article h2 { margin: 1.8em 0 .65em; padding-top: .3em; border-top: 1px solid var(--line); color: var(--odoo-purple-dark); font-size: 27px; line-height: 1.25; letter-spacing: -.03em; }
.article h2:first-child { margin-top: 0; border-top: 0; }
.article h3 { margin: 1.5em 0 .5em; color: var(--odoo-purple); font-size: 19px; }
.article p { margin: .75em 0; }
.article strong { color: #362b36; }
.article ul, .article ol { padding-left: 1.4em; }
.article li { padding-left: .25em; margin: .42em 0; }
.article li::marker { color: var(--odoo-orange); }
.article code { padding: .13em .4em; border: 1px solid #eee8ed; border-radius: 5px; background: #f8f5f7; color: #5a3c53; font-size: .9em; }
.article table { display: block; width: 100%; margin: 1.2em 0; overflow-x: auto; border-collapse: collapse; font-size: 14px; }
.article th { background: var(--odoo-purple-pale); color: var(--odoo-purple-dark); text-align: left; }
.article th, .article td { padding: 11px 13px; border: 1px solid var(--line); }
.article blockquote { margin: 1.2em 0; padding: 12px 18px; border-left: 4px solid var(--odoo-orange); background: #fcf7f4; color: var(--muted); }
.sidebar { display: grid; gap: 14px; }
.side-card { padding: 20px; }
.side-label { margin: 0 0 9px; color: var(--muted); font-size: 11px; font-weight: 750; letter-spacing: .12em; text-transform: uppercase; }
.side-card p { margin: 0; font-size: 14px; }
.side-card .accent { color: var(--odoo-purple); font-size: 23px; font-weight: 750; letter-spacing: -.03em; }
.side-card a { font-size: 14px; }
footer { padding: 25px 20px; border-top: 1px solid var(--line); color: var(--muted); text-align: center; font-size: 13px; }
@media (max-width: 850px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); }
  .hero-inner { padding-top: 55px; padding-bottom: 66px; }
}
@media (max-width: 520px) {
  .topbar { align-items: flex-start; flex-direction: column; gap: 10px; padding: 13px 18px; }
  .hero-inner { padding: 44px 20px 58px; }
  .layout { padding-right: 14px; padding-left: 14px; }
  .article { padding: 24px 20px; }
}
"""


def render_page(language: str, output_dir: Path, store_listing: bool = False) -> str:
    info = LANGUAGES[language]
    source_path = HERE / info["file"]
    parser = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"])
    source = source_path.read_text(encoding="utf-8").splitlines()
    if source and source[0].startswith("# "):
        source = source[1:]
    body = parser.convert("\n".join(source))
    nav_items = []
    for code, entry in LANGUAGES.items():
        current = ' aria-current="page"' if code == language else ""
        nav_items.append(
            f'<a href="{entry["output"]}"{current}>{entry["label"]}</a>'
        )
    nav = "\n".join(nav_items)
    title = {
        "en": "Priority Sale Order",
        "es": "Prioridad de pedidos de venta",
        "pt_BR": "Prioridade de pedidos de venda",
    }[language]
    eyebrow = {
        "en": "Odoo module · Store documentation",
        "es": "Módulo de Odoo · Documentación de tienda",
        "pt_BR": "Módulo Odoo · Documentação da loja",
    }[language]
    footer = {
        "en": "Priority Sale Order · Documentation",
        "es": "Priority Sale Order · Documentación",
        "pt_BR": "Priority Sale Order · Documentação",
    }[language]
    sidebar_copy = {
        "en": "Built for Odoo stores and delivery teams.",
        "es": "Pensado para tiendas y equipos de reparto que usan Odoo.",
        "pt_BR": "Feito para lojas e equipes de entrega que usam Odoo.",
    }[language]
    sidebar_label = {"en": "Odoo editions", "es": "Versiones de Odoo", "pt_BR": "Versões do Odoo"}[language]
    return f'''<!doctype html>
<html lang="{info["locale"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{title}</title>
  <style>{STYLES}</style>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="index.html"><span class="brand-mark">O</span><span>Priority Sale Order</span></a>
    <nav class="languages" aria-label="Language">{nav}</nav>
  </header>
  <section class="hero">
    <div class="hero-inner">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <div class="hero-rule"></div>
    </div>
  </section>
  <main class="layout">
    <article class="article">{body}</article>
    <aside class="sidebar">
      <section class="side-card"><p class="side-label">{sidebar_label}</p><p class="accent">17 · 18 · 19 · 20</p><p>{sidebar_copy}</p></section>
      {'' if store_listing else f'<section class="side-card"><p class="side-label">Source</p><p><a href="../{info["file"]}">Read the Markdown version</a></p></section>'}
    </aside>
  </main>
  <footer>{footer}</footer>
</body>
</html>
'''


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
            render_page(language, args.output_dir, store_listing=args.store_listing),
            encoding="utf-8",
        )
        print(f"Generated {destination}")


if __name__ == "__main__":
    main()
