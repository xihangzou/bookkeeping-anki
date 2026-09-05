#!/usr/bin/env python3
"""Synthetic UTF-8/control-character serialization gate for ANKI-043."""

from build_anki_export import decode_schema_escapes, encode_schema_escapes


def main() -> int:
    sample = "日本語\n二行目\t値\\literal\r終"
    encoded = encode_schema_escapes(sample)
    if any(ch in encoded for ch in "\t\r\n"):
        raise AssertionError("serialized fixture contains raw control characters")
    if decode_schema_escapes(encoded) != sample:
        raise AssertionError("schema escape round-trip changed Unicode/control characters")
    if encoded.encode("utf-8").decode("utf-8") != encoded:
        raise AssertionError("UTF-8 byte round-trip failed")
    print("ANKI-043 Unicode/line-break serialization fixture: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
