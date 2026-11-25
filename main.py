"""Ship the finished news image to the make.fun output folder.

The artwork itself is produced by ``render.py`` and stored beside this
file as ``entry.png``. This entry point is deliberately boring: it
sanity-checks those bytes as a PNG, then copies them verbatim to the
destination folder, so repeated runs always deliver the identical
file. Nothing here talks to the network.
"""

import os
import struct
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_IMAGE = SCRIPT_DIR / "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# The entry image is a fixed asset with a known rough weight; the size
# window below exists to catch a truncated, swapped or corrupt file
# before it gets copied anywhere.
SMALLEST_OK_BYTES = 10_000
LARGEST_OK_BYTES = 5_000_000
IHDR_LABEL_AT = slice(12, 16)
DIMENSIONS_AT = slice(16, 24)
HEADER_MIN_BYTES = 24


def resolve_destination():
    """Work out where the copy should land and make sure the folder exists.

    The ``MAKEFUN_OUTPUT_DIR`` environment variable wins when set;
    otherwise the copy goes to ``/output``.
    """
    requested = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    folder = Path(requested) if requested else Path("/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def ensure_source_present():
    if not SOURCE_IMAGE.is_file():
        print(f"missing entry image: {SOURCE_IMAGE}", file=sys.stderr)
        raise SystemExit(1)
    data = SOURCE_IMAGE.read_bytes()
    if len(data) < HEADER_MIN_BYTES or data[:8] != PNG_SIGNATURE:
        print("entry.png is not a whole PNG file", file=sys.stderr)
        raise SystemExit(1)
    if data[IHDR_LABEL_AT] != b"IHDR":
        print("entry.png has no IHDR chunk", file=sys.stderr)
        raise SystemExit(1)
    width, height = struct.unpack(">II", data[DIMENSIONS_AT])
    if (width, height) != (1024, 1024):
        print(f"entry.png is {width}x{height}, expected 1024x1024", file=sys.stderr)
        raise SystemExit(1)
    if not SMALLEST_OK_BYTES <= len(data) <= LARGEST_OK_BYTES:
        print(f"entry.png is {len(data)} bytes, outside the sane window", file=sys.stderr)
        raise SystemExit(1)
    return data


def main():
    data = ensure_source_present()
    destination = resolve_destination()
    destination.write_bytes(data)
    print(f"wrote {destination} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
