#!/usr/bin/env python3
"""Entrypoint for make.fun bounty the-picture-that-tastes-of-one-20261122-2047.

Stdlib only. Copies the pre-rendered entry.png (next to this file) to
$MAKEFUN_OUTPUT_DIR/entry.png (fallback /output).
"""
import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        print(f"entry.png not found next to main.py: {src}", file=sys.stderr)
        return 1
    if src.stat().st_size == 0 or src.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        print(f"entry.png is not a valid non-empty PNG: {src}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    print(f"copied {src} -> {dst} ({dst.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
