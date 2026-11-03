"""Read an edited dialogue file back into your translation file.

Accepts the TSV or the XLSX written by export_dialog.py; only the last column is
read. Rows whose translation is empty are skipped, so a half-finished file is fine.
Every line is checked first: a broken <font> tag or a lost |button| token is refused
instead of being written into the game.

Usage:
  python tools/import_dialog.py --file data/dialog_lithuanian.xlsx --tm data/lt_tm.json
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tlou

TOKEN = re.compile(r"\|[^|]{1,40}\|")
TAG = re.compile(r"</?[a-zA-Z][^<>]{0,80}>")
PLACEHOLDER = re.compile(r"%[sd]|\[[A-Z_]+\]|in_percent|\{[^}]{1,20}\}")


def unesc(text):
    return re.sub(r"\\(.)", lambda m: {"n": "\n", "t": "\t", "\\": "\\"}.get(m.group(1), m.group(1)), text)


def check(english, translation):
    """Everything the game needs to survive: tokens, tags, placeholders, line breaks."""
    out = []
    for label, pattern in (("token", TOKEN), ("tag", TAG), ("placeholder", PLACEHOLDER)):
        if sorted(pattern.findall(english)) != sorted(pattern.findall(translation)):
            out.append(f"{label} mismatch")
    if english.count("\n") != translation.count("\n"):
        out.append("line breaks changed")
    if english != english.strip() and translation.strip() == translation:
        out.append("leading/trailing space lost")
    if len(translation) > max(40, len(english) * 2.5):
        out.append("much longer than the English")
    return out


def read_rows(path):
    """[(id, english, translation)] from .tsv or .xlsx."""
    if path.lower().endswith((".xlsx", ".xlsm")):
        from openpyxl import load_workbook
        wb = load_workbook(path, read_only=True, data_only=True)
        ws = wb[wb.sheetnames[0]]
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        wb.close()
        for row in rows:
            if not row or not row[0]:
                continue
            yield str(row[0]).strip(), str(row[2] or ""), str(row[3] or "")
        return
    with open(path, encoding="utf-8-sig", newline="") as fh:
        fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            yield parts[0].strip(), unesc(parts[2]), unesc(parts[3])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="edited TSV or XLSX")
    ap.add_argument("--tm", required=True, help="translation json to update")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    tm = tlou.load_translations(args.tm)
    added = same = bad = 0
    for key, english, translation in read_rows(args.file):
        translation = translation.strip("\r")
        if not translation.strip():
            continue
        try:
            sid = int(key, 16)
        except ValueError:
            continue
        if tm.get(sid) == translation:
            same += 1
            continue
        problems = check(english.replace("\r", ""), translation)
        if problems:
            bad += 1
            print(f"{key}: {', '.join(problems)}")
            continue
        tm[sid] = translation
        added += 1

    print(f"new or changed: {added}, unchanged: {same}, refused: {bad}, memory: {len(tm)}")
    if args.dry_run:
        print("dry run - nothing written")
        return 0
    if added:
        tlou.save_translations(args.tm, tm)
        print(f"written to {args.tm}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
