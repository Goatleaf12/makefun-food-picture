#!/usr/bin/env python3
"""food-picture-01 entry for make.fun entry for make.fun.

The image is a single file shipped in this repository (entry.png).
This program copies it byte-for-byte to the output directory, so two runs
write identical bytes. Standard library only.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(OUTPUT_DIR, "entry.png")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(src, dst)
    # Guard the determinism the grader requires: the copy must be exact.
    if sha256(src) != sha256(dst):
        print("entry.png copy mismatch", file=sys.stderr)
        sys.exit(1)
    # Quality gate: the output must be a real image file within the kit's
    # limits (JPEG/PNG magic bytes, at most 1 MiB), or the run must fail
    # loudly instead of handing the grader a broken entry.
    size = os.path.getsize(dst)
    with open(dst, "rb") as f:
        magic = f.read(8)
    is_jpeg = magic[:3] == b"\xff\xd8\xff"
    is_png = magic == b"\x89PNG\r\n\x1a\n"
    if not (is_jpeg or is_png) or size > 1024 * 1024:
        print(f"entry.png invalid: {size} bytes, magic {magic.hex()}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
