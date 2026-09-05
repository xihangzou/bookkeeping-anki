#!/usr/bin/env python3
"""Build the canonical Anki export with the approved presentation style.

The semantic/export logic remains in build_anki_export.py. This wrapper replaces
only the Anki model CSS, records itself as the build script identity, and verifies
that the generated APKG contains the exact requested CSS.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import tempfile
import zipfile
from pathlib import Path

import genanki

import build_anki_export as base

CARD_CSS = """.card { font-family: -apple-system, BlinkMacSystemFont, 'Hiragino Sans', sans-serif;
        font-size: 24px; text-align: center; color: #111; background: #fff; }
.cloze { font-weight: 700; color: #c2185b; }"""

_ORIGINAL_MODEL = genanki.Model


class _StyledModelFactory:
    CLOZE = _ORIGINAL_MODEL.CLOZE

    def __call__(self, *args, **kwargs):
        kwargs["css"] = CARD_CSS
        return _ORIGINAL_MODEL(*args, **kwargs)


def _output_dir() -> Path:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--output-dir", type=Path, default=base.ROOT / "export" / "build")
    args, _ = parser.parse_known_args()
    return args.output_dir


def _validate_style(apkg_path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        extracted = Path(tmp)
        with zipfile.ZipFile(apkg_path) as archive:
            archive.extractall(extracted)
        db_path = base.locate_collection(extracted)
        con = sqlite3.connect(db_path)
        try:
            row = con.execute("SELECT models FROM col").fetchone()
        finally:
            con.close()

    if not row:
        raise AssertionError("APKG collection has no model metadata")
    models = json.loads(row[0])
    matching = [model for model in models.values() if model.get("name") == base.MODEL_NAME]
    if len(matching) != 1:
        raise AssertionError(f"expected one {base.MODEL_NAME!r} model, found {len(matching)}")
    if matching[0].get("css") != CARD_CSS:
        raise AssertionError("generated APKG CSS does not match requested card style")


def main() -> int:
    genanki.Model = _StyledModelFactory()
    base.SCRIPT_PATH = Path(__file__).resolve()
    result = base.main()
    if result != 0:
        return result
    apkg_path = _output_dir() / "bookkeeping-master.apkg"
    _validate_style(apkg_path)
    print("Anki card style validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
