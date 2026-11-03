"""Shared helpers: find the game, read the text tables, build them back.

A text table is:
    u32 count | count x (u64 string id, u64 offset) | block of NUL-terminated UTF-8
Offset 0 always holds the 18-byte fallback "UNKNOWN STRING!!!".
Strings that are not replaced are copied byte for byte, so a rebuild stays identical.
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import psarc  # noqa: E402

FALLBACK = b"UNKNOWN STRING!!!\x00"
TABLES = ("common", "subtitles", "subtitles-systemic")
# the language slot this project takes over, and the name it shows in the menu
DEFAULT_SLOT = "hun"
SLOT_AUTONYMS = {"hun": "Magyar", "pol": "Polski", "cze": "Čeština", "rus": "Русский",
                 "ger": "Deutsch", "fre": "Français", "ita": "Italiano", "spa": "Español",
                 "por": "Português", "dut": "Nederlands", "swe": "Svenska", "nor": "Norsk",
                 "dan": "Dansk", "fin": "Suomi", "gre": "Ελληνικά", "tur": "Türkçe",
                 "hrv": "Hrvatski", "bra": "Português (Brasil)", "sas": "Español (Latinoamérica)"}

GUESSES = [
    r"D:\SteamLibrary\steamapps\common\The Last of Us Part I",
    r"C:\Program Files (x86)\Steam\steamapps\common\The Last of Us Part I",
    r"C:\Program Files\Steam\steamapps\common\The Last of Us Part I",
    r"E:\SteamLibrary\steamapps\common\The Last of Us Part I",
]


def find_game(explicit=""):
    """The game folder: --game, then TLOU_GAME, then the usual Steam libraries."""
    for path in [explicit, os.environ.get("TLOU_GAME", "")] + GUESSES:
        if path and os.path.exists(os.path.join(path, r"build\pc\main")):
            return os.path.abspath(path)
    raise SystemExit("Game folder not found. Pass --game \"C:\\...\\The Last of Us Part I\" "
                     "or set TLOU_GAME.")


def core_path(game):
    return os.path.join(game, "build", "pc", "main", "core.psarc")


def oodle_for(game):
    psarc.OODLE_PATH = os.path.join(game, "oo2core_9_win64.dll")
    return psarc.OODLE_PATH


def resolve_oodle(archive=""):
    """The Oodle library: from TLOU_OODLE, next to the archive, or from the game folder."""
    path = psarc.find_oodle(archive)
    if not path:
        try:
            path = oodle_for(find_game())
        except SystemExit:
            path = ""
    return path


class Table:
    """One text table: the id -> offset records and the string block."""

    def __init__(self, blob):
        self.count = struct.unpack("<I", blob[:4])[0]
        self.recs = [struct.unpack("<QQ", blob[4 + i * 16:4 + i * 16 + 16])
                     for i in range(self.count)]
        self.block = blob[4 + self.count * 16:]
        self.raw = {}
        for _sid, off in self.recs:
            if off not in self.raw:
                self.raw[off] = self.block[off:self.block.index(b"\x00", off)]

    def text(self, off):
        return self.raw[off].decode("utf-8", "replace")

    def by_id(self):
        return {sid: self.text(off) for sid, off in self.recs}

    def build(self, replace=None):
        """replace: {offset: text}. Everything else is copied byte for byte."""
        replace = replace or {}
        new_off, block = {}, bytearray(FALLBACK)
        for off in sorted(self.raw):
            if off == 0:
                new_off[0] = 0
                continue
            new_off[off] = len(block)
            if off in replace:
                block += replace[off].encode("utf-8") + b"\x00"
            else:
                block += self.raw[off] + b"\x00"
        head = bytearray(struct.pack("<I", self.count))
        for sid, off in self.recs:
            head += struct.pack("<QQ", sid, new_off[off])
        return bytes(head) + bytes(block)


def read_table(archive_path, name):
    """Read text2/<name> out of an archive (the archive is closed afterwards)."""
    a = psarc.PsarcArchive(archive_path)
    try:
        return Table(a.extract_by_name("text2/" + name))
    finally:
        a.close()


def load_translations(path):
    """{int id: text} from a json file written by this project."""
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return {int(k, 16): v for k, v in json.load(fh).items()}


def save_translations(path, tm):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({f"{k:#018x}": v for k, v in sorted(tm.items())}, fh,
                  ensure_ascii=False, indent=1, sort_keys=True)


def load_labels(path):
    """{english label: translation} for short menu labels, kept apart from full strings."""
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
