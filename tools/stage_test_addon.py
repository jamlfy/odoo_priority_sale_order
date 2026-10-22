#!/usr/bin/env python3
"""Stage the addon for tests without requiring Odoo Apps listing assets."""

from __future__ import annotations

import argparse
from pathlib import Path

from addon_staging import MODULE_NAME, ODOO_VERSIONS, stage_addon


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--odoo-version", required=True, choices=ODOO_VERSIONS)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    destination = args.output_dir.resolve() / MODULE_NAME
    stage_addon(args.odoo_version, destination)
    print(f"Staged {MODULE_NAME} for Odoo {args.odoo_version}: {destination}")


if __name__ == "__main__":
    main()
