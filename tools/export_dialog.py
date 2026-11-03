"""Write every string of the game into one editable file (TSV, optionally XLSX).

Columns: id | table | english | translation
The translation column is filled from your translation file, so you can see where
you are; empty means "not translated yet, the game will show English".

Usage:
  python tools/export_dialog.py --out data
  python tools/export_dialog.py --out data --xlsx --tm data/lt_tm.json
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tlou


def esc(text):
    return text.replace("\\", "\\\\").replace("\t", "\\t").replace("\r", "").replace("\n", "\\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="", help="game folder (default: find it)")
    ap.add_argument("--archive", default="", help="core.psarc to read (default: the game's)")
    ap.add_argument("--out", default="data", help="folder for the files")
    ap.add_argument("--tm", default="", help="translation json to pre-fill the last column")
    ap.add_argument("--xlsx", action="store_true", help="also write an Excel file")
    ap.add_argument("--name", default="dialog_english", help="file name without extension")
    ap.add_argument("--untranslated-only", action="store_true")
    args = ap.parse_args()

    game = tlou.find_game(args.game)
    tlou.oodle_for(game)
    archive = args.archive or tlou.core_path(game)
    tm = tlou.load_translations(args.tm)
    os.makedirs(args.out, exist_ok=True)

    rows = []
    for table in tlou.TABLES:
        data = tlou.read_table(archive, "eng." + table)
        for sid, text in data.by_id().items():
            translated = tm.get(sid, "")
            if args.untranslated_only and translated:
                continue
            rows.append((f"{sid:#018x}", table, text, translated))
    rows.sort(key=lambda r: (r[1], r[0]))

    tsv = os.path.join(args.out, args.name + ".tsv")
    with open(tsv, "w", encoding="utf-8-sig", newline="\n") as fh:
        fh.write("id\ttable\tenglish\ttranslation\n")
        for sid, table, text, translated in rows:
            fh.write(f"{sid}\t{table}\t{esc(text)}\t{esc(translated)}\n")
    print(f"{tsv}: {len(rows)} rows")

    if args.xlsx:
        from openpyxl import Workbook
        from openpyxl.styles import Font
        wb = Workbook()
        ws = wb.active
        ws.title = "dialog"
        ws.append(["id", "table", "english", "translation"])
        for cell in ws[1]:
            cell.font = Font(bold=True)
        for sid, table, text, translated in rows:
            ws.append([sid, table, text, translated])
        ws.freeze_panes = "A2"
        ws.column_dimensions["A"].width = 20
        ws.column_dimensions["B"].width = 18
        ws.column_dimensions["C"].width = 80
        ws.column_dimensions["D"].width = 80
        xlsx = os.path.join(args.out, args.name + ".xlsx")
        wb.save(xlsx)
        print(f"{xlsx}: {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
