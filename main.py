#!/usr/bin/env python3
"""food-picture-01 entry: a steaming bowl of ramen, close up.

Chopsticks lift the noodles out of the broth, steam rising, soft window
light. The picture ships in this repo as entry.png. Running this program
drops a byte-identical copy into the grader's output folder. Pure standard
library, no network, no randomness: two runs produce the same file.
"""
import hashlib, os, shutil, sys

REPO = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(REPO, "entry.png")
MAX_BYTES = 1024 * 1024


def file_digest(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(SOURCE):
        print(f"missing bundled image: {SOURCE}", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    # A short write would silently hand the grader a corrupt image, so
    # verify the copy byte for byte before doing anything else with it.
    if file_digest(SOURCE) != file_digest(target):
        print("copy mismatch: entry.png", file=sys.stderr)
        return 1
    size = os.path.getsize(target)
    with open(target, "rb") as handle:
        header = handle.read(8)
    # The kit caps entries at 1 MiB and only accepts real JPEG/PNG files.
    looks_jpeg = header[:3] == b"\xff\xd8\xff"
    looks_png = header == b"\x89PNG\r\n\x1a\n"
    if size > MAX_BYTES or not (looks_jpeg or looks_png):
        print(f"entry.png invalid: {size} bytes, header {header.hex()}", file=sys.stderr)
        return 1
    print(f"wrote {target} ({size} bytes, sha256 {file_digest(target)[:16]}...); deterministic copy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
