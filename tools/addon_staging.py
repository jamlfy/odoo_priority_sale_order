"""Shared helpers for building version-specific addon stages."""

from __future__ import annotations

import ast
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "priority_sale_order"
ODOO_VERSIONS = ("17.0", "18.0", "19.0", "20.0")
ADDON_PATHS = (
    "__init__.py",
    "__manifest__.py",
    "data",
    "i18n",
    "models",
    "security",
    "static",
    "tests",
    "views",
)
MANIFEST_VERSION = re.compile(r'("version"\s*:\s*")([^"]+)(")')


def package_version(base_version: str, odoo_version: str) -> str:
    match = re.fullmatch(r"\d+\.\d+\.(.+)", base_version)
    if not match:
        raise ValueError(f"Expected an Odoo version prefix in manifest version: {base_version}")
    if odoo_version not in ODOO_VERSIONS:
        raise ValueError(f"Unsupported Odoo version: {odoo_version}")
    return f"{odoo_version}.{match.group(1)}"


def stage_addon(odoo_version: str, destination: Path) -> Path:
    """Copy just the addon files and rewrite its manifest for one Odoo series."""
    manifest_path = ROOT / "__manifest__.py"
    manifest_text = manifest_path.read_text(encoding="utf-8")
    manifest = ast.literal_eval(manifest_text)
    target_version = package_version(manifest["version"], odoo_version)
    rewritten_manifest, count = MANIFEST_VERSION.subn(
        lambda match: f"{match.group(1)}{target_version}{match.group(3)}",
        manifest_text,
        count=1,
    )
    if count != 1:
        raise ValueError("Could not update the version in __manifest__.py")

    destination.mkdir(parents=True, exist_ok=True)
    for relative in ADDON_PATHS:
        source = ROOT / relative
        target = destination / relative
        if source.is_dir():
            shutil.copytree(
                source,
                target,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            )
        elif source.is_file() and relative != "__manifest__.py":
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    (destination / "__manifest__.py").write_text(rewritten_manifest, encoding="utf-8")
    return destination
