"""Tests for the toolkit: table round-trip, escaping, translation validation."""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))

import export_dialog  # noqa: E402
import import_dialog  # noqa: E402
import tlou  # noqa: E402


def make_table(strings):
    """A table blob in the game's format, with the fallback at offset 0."""
    block = bytearray(tlou.FALLBACK)
    offsets = {}
    for sid, text in strings:
        offsets[sid] = len(block)
        block += text.encode("utf-8") + b"\x00"
    head = bytearray(struct.pack("<I", len(strings)))
    for sid, _text in strings:
        head += struct.pack("<QQ", sid, offsets[sid])
    return bytes(head) + bytes(block)


STRINGS = [(0x10, "Joel"), (0x20, "You're capable."), (0x30, ""), (0x40, "two\nlines")]


def test_round_trip_is_byte_identical():
    blob = make_table(STRINGS)
    table = tlou.Table(blob)
    assert table.build({}) == blob


def test_only_the_replaced_string_changes():
    blob = make_table(STRINGS)
    table = tlou.Table(blob)
    target = [off for sid, off in table.recs if sid == 0x20][0]
    built = tlou.Table(table.build({target: "Tu esi pajėgi."}))
    assert built.by_id()[0x20] == "Tu esi pajėgi."
    assert built.by_id()[0x10] == "Joel"
    assert built.by_id()[0x40] == "two\nlines"


def test_ids_stay_in_the_same_order():
    blob = make_table(STRINGS)
    table = tlou.Table(blob)
    assert [sid for sid, _ in tlou.Table(table.build({})).recs] == [0x10, 0x20, 0x30, 0x40]


def test_export_escapes_tabs_and_newlines():
    assert export_dialog.esc("a\tb\nc") == "a\\tb\\nc"
    assert import_dialog.unesc("a\\tb\\nc") == "a\tb\nc"


def test_check_accepts_a_good_line_and_refuses_a_broken_one():
    english = "Press |move| to open the <font color=\"t2-red\">door</font>."
    good = "Spausk |move|, kad atidarytum <font color=\"t2-red\">duris</font>."
    assert import_dialog.check(english, good) == []
    assert import_dialog.check(english, "Spausk, kad atidarytum duris.")          # tokens gone
    assert import_dialog.check(english, "Spausk |move| <font color=\"t2-red\">duris.")  # </font> lost


def test_slot_autonyms_are_known_for_the_latin_slots():
    for slot in ("hun", "pol", "cze", "ger", "fre", "ita", "spa"):
        assert slot in tlou.SLOT_AUTONYMS, slot
