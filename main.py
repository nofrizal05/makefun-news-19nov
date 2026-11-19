"""News image entry for make.fun news-image-20261119.

Copies the pre-built front-page image beside this file to
/output/entry.png. Standard library only, no network, deterministic:
the same input bytes are copied on every run, so two runs write
the same bytes.
"""
import os
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parent / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, OUT_DIR / "entry.png")
