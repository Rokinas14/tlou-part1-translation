"""Build the three text tables of a language slot from your translation file.

Takes over one of the game's 26 language slots (default: hun, Hungarian) and fills
it with your translation. Strings you have not translated fall back to English, so
the slot is readable at any stage of the work.

Usage:
  python tools/build_slot.py --archive "E:\\backup\\core.psarc" --tm data/lt_tm.json \
      --labels data/labels_lt.json --label "Lietuvių" --out out
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tlou


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True, help="a clean copy of core.psarc to read")
    ap.add_argument("--game", default="", help="game folder, only used to find the Oodle library")
    ap.add_argument("--slot", default=tlou.DEFAULT_SLOT, help="language slot to take over")
    ap.add_argument("--autonym", default="", help="the slot's own language name in the game "
                                                "(default: known name for the slot)")
    ap.add_argument("--label", default="", help="language name to show in the menu, e.g. Lietuvių")
    ap.add_argument("--tm", default="", help="translation json")
    ap.add_argument("--labels", default="", help="json of short menu labels (english -> translation)")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    game = tlou.find_game(args.game)
    tlou.oodle_for(game)
    tm = tlou.load_translations(args.tm)
    labels = tlou.load_labels(args.labels)
    out = os.path.join(args.out, "text2")
    os.makedirs(out, exist_ok=True)

    eng = {name: tlou.read_table(args.archive, "eng." + name) for name in tlou.TABLES}
    slot = {name: tlou.read_table(args.archive, f"{args.slot}.{name}") for name in tlou.TABLES}

    print(f"archive: {args.archive}")
    print(f"slot: {args.slot}   translations: {len(tm)}   labels: {len(labels)}")

    # --- the slot's main table: your strings, then labels, then English ---
    table = slot["common"]
    english = eng["common"].by_id()
    replace, hits = {}, {"translation": 0, "label": 0, "english": 0}
    for sid, off in table.recs:
        en = english.get(sid, "")
        if sid in tm:
            replace[off] = tm[sid]
            hits["translation"] += 1
        elif en in labels:
            replace[off] = labels[en]
            hits["label"] += 1
        else:
            replace[off] = en
            hits["english"] += 1
    path = os.path.join(out, f"{args.slot}.common")
    open(path, "wb").write(table.build(replace))
    total = len(table.recs)
    covered = hits["translation"] + hits["label"]
    print(f"  {os.path.basename(path):22s} {total:6d} strings, {covered} translated "
          f"({100 * covered / max(total, 1):.1f}%) -> {path}")

    # --- the two subtitle tables: your strings, then English ---
    for name in tlou.TABLES[1:]:
        table = slot[name]
        english = eng[name].by_id()
        replace, n = {}, 0
        for sid, off in table.recs:
            if sid in tm:
                replace[off] = tm[sid]
                n += 1
            else:
                replace[off] = english.get(sid, "")
        path = os.path.join(out, f"{args.slot}.{name}")
        open(path, "wb").write(table.build(replace))
        print(f"  {os.path.basename(path):22s} {len(table.recs):6d} strings, {n} translated "
              f"({100 * n / max(len(table.recs), 1):.1f}%) -> {path}")

    # --- the English table only gets the language name, so the menu reads "Lietuvių" ---
    autonym = args.autonym or tlou.SLOT_AUTONYMS.get(args.slot, "")
    eng_table = eng["common"]
    if args.label and autonym:
        replace = {off: args.label for sid, off in eng_table.recs if eng_table.text(off) == autonym}
        path = os.path.join(out, "eng.common")
        open(path, "wb").write(eng_table.build(replace))
        print(f"  {'eng.common':22s} language name {autonym!r} -> {args.label!r} "
              f"({len(replace)} strings) -> {path}")
    else:
        print("  eng.common untouched (no --label or unknown autonym; "
              "the menu will show the slot's original name)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
