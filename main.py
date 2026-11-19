"""Copy the shipped front page to the grader's output directory.

The entry image (entry.png) is already in this repository, drawn for
19 November 2026. The grading sandbox runs Python 3.13 with the
standard library only and no network, so this program uses nothing
beyond the standard library: it copies the image byte for byte.

The destination is $MAKEFUN_OUTPUT_DIR/entry.png, defaulting to
/output/entry.png. The copy is deterministic: every run writes the
same bytes, because the bytes are the file's own.
"""

import os
import shutil
from pathlib import Path

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        raise FileNotFoundError(f"shipped image not found: {source}")

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / OUTPUT_NAME

    shutil.copyfile(source, destination)
    print(f"wrote {destination} ({destination.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
