#!/usr/bin/env python3
"""Write this entry's one-line developer excuse to <output dir>/entry.txt.

Deterministic, offline, no randomness: the line is a single constant and the
program only serialises it as UTF-8 with no trailing newline.
"""

import os
import sys

# The entry: one funny single-line excuse a developer gives when code breaks
# in production. 1-200 Unicode code points, no line breaks.
LINE = "Works on my machine — it's been hitting a mock since the demo in April."


def output_path() -> str:
    """Resolve the entry file: $MAKEFUN_OUTPUT_DIR if set, else /output."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(base, "entry.txt")


def main() -> int:
    # Fail loudly rather than write something the gate would reject.
    if not 1 <= len(LINE) <= 200:
        raise SystemExit("entry text must be 1-200 code points")
    if any(ch in LINE for ch in "\r\n"):
        raise SystemExit("entry text must be a single line")
    if not LINE.strip():
        raise SystemExit("entry text must not be only whitespace")

    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    # newline="" keeps the exact bytes: no translation, no trailing newline.
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)

    sys.stderr.write(f"wrote {len(LINE)} code points to {path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
