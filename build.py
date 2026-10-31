#!/usr/bin/env python3
"""Build the Gentle Accountability Friendship Kit printables.

Renders every HTML sheet in src/sheets/ to an unbranded PDF in printables/
using WeasyPrint. Usage notes ("how to use this sheet, kindly") live inside
each sheet itself, so every printed page carries its own kindness manual.

Usage:
    python3 build.py            # build all sheets
    python3 build.py --clean    # remove printables/ first
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SHEETS_DIR = ROOT / "src" / "sheets"
OUT_DIR = ROOT / "printables"


def discover_sheets() -> list[Path]:
    if not SHEETS_DIR.is_dir():
        return []
    return sorted(SHEETS_DIR.glob("*.html"))


def build_sheet(html_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (html_path.stem + ".pdf")
    HTML(filename=str(html_path)).write_pdf(target=str(out_path))
    return out_path


def clean(out_dir: Path) -> None:
    if out_dir.is_dir():
        shutil.rmtree(out_dir)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean", action="store_true", help="remove printables/ before building")
    parser.add_argument("--out", type=Path, default=OUT_DIR, help="output directory")
    args = parser.parse_args(argv)

    if args.clean:
        clean(args.out)

    sheets = discover_sheets()
    if not sheets:
        print(f"No sheets found in {SHEETS_DIR}", file=sys.stderr)
        return 1

    failures = 0
    for sheet in sheets:
        try:
            out = build_sheet(sheet, args.out)
            print(f"built {out.relative_to(ROOT)}")
        except Exception as exc:  # noqa: BLE001 - report every sheet's failure
            print(f"FAILED {sheet.name}: {exc}", file=sys.stderr)
            failures += 1

    if failures:
        print(f"{failures} sheet(s) failed", file=sys.stderr)
        return 1
    print(f"done: {len(sheets)} sheet(s) -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
