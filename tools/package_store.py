#!/usr/bin/env python3
"""Build clean Odoo Apps ZIP packages for each supported Odoo series."""

from __future__ import annotations

import argparse
import ast
import tempfile
import zipfile
from pathlib import Path

from addon_staging import MODULE_NAME, ODOO_VERSIONS, ROOT, package_version, stage_addon

VERSIONS = ODOO_VERSIONS


def addon_manifest() -> dict:
    return ast.literal_eval((ROOT / "__manifest__.py").read_text(encoding="utf-8"))


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
        package = output_dir / f"{MODULE_NAME}-{odoo_version}.zip"
        with tempfile.TemporaryDirectory(prefix=f"{MODULE_NAME}-") as temporary:
            stage = stage_addon(odoo_version, Path(temporary) / MODULE_NAME)

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
