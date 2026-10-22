#!/usr/bin/env python3
"""Build clean Odoo Apps ZIP packages for each supported Odoo series."""

from __future__ import annotations

import argparse
import ast
import re
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "priority_sale_order"
VERSIONS = ("17.0", "18.0", "19.0", "20.0")
PACKAGE_PATHS = (
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


def addon_manifest() -> dict:
    return ast.literal_eval((ROOT / "__manifest__.py").read_text(encoding="utf-8"))


def package_version(base_version: str, odoo_version: str) -> str:
    match = re.fullmatch(r"\d+\.\d+\.(.+)", base_version)
    if not match:
        raise ValueError(f"Expected an Odoo version prefix in manifest version: {base_version}")
    return f"{odoo_version}.{match.group(1)}"


def validate_assets(manifest: dict) -> None:
    required = ["static/description/icon.png", *manifest.get("images", [])]
    required.extend(
        f"static/description/{filename}"
        for filename in ("index.html", "es.html", "pt_BR.html")
    )
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise FileNotFoundError("Missing store assets: " + ", ".join(missing))


def build_packages(output_dir: Path, versions: tuple[str, ...] = VERSIONS) -> list[Path]:
    manifest_path = ROOT / "__manifest__.py"
    manifest_text = manifest_path.read_text(encoding="utf-8")
    manifest = ast.literal_eval(manifest_text)
    validate_assets(manifest)
    base_version = manifest["version"]
    output_dir.mkdir(parents=True, exist_ok=True)
    packages = []

    for odoo_version in versions:
        target_version = package_version(base_version, odoo_version)
        rewritten_manifest, count = MANIFEST_VERSION.subn(
            lambda match: f"{match.group(1)}{target_version}{match.group(3)}",
            manifest_text,
            count=1,
        )
        if count != 1:
            raise ValueError("Could not update the version in __manifest__.py")

        package = output_dir / f"{MODULE_NAME}-{odoo_version}.zip"
        with tempfile.TemporaryDirectory(prefix=f"{MODULE_NAME}-") as temporary:
            stage = Path(temporary) / MODULE_NAME
            stage.mkdir()
            for relative in PACKAGE_PATHS:
                source = ROOT / relative
                destination = stage / relative
                if source.is_dir():
                    shutil.copytree(
                        source,
                        destination,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
                    )
                elif source.is_file():
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
            (stage / "__manifest__.py").write_text(rewritten_manifest, encoding="utf-8")

            with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for path in sorted(stage.rglob("*")):
                    if path.is_file():
                        archive.write(path, path.relative_to(stage.parent))
        packages.append(package)
        print(f"Built {package} (manifest version {target_version})")
    return packages


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, default=ROOT / "dist", help="Directory for ZIP packages."
    )
    parser.add_argument(
        "--odoo-version",
        choices=VERSIONS,
        help="Build only the package for this Odoo series (all four by default).",
    )
    args = parser.parse_args()
    versions = (args.odoo_version,) if args.odoo_version else VERSIONS
    build_packages(args.output_dir.resolve(), versions)


if __name__ == "__main__":
    main()
