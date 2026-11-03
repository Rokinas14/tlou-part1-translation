"""Put the built tables into a copy of core.psarc and check the result.

The archive is 6 GB, so it is written next to a scratch disk with room, never over
the live file: you copy the result into the game yourself (see docs/INSTALL.md).

Usage:
  python tools/inject.py --archive "E:\\backup\\core.psarc" --out "E:\\core_translated.psarc" \
      --slot hun --build-dir out
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psarc
import psarc_injector
import tlou


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True, help="clean core.psarc to start from")
    ap.add_argument("--out", required=True, help="where to write the patched archive")
    ap.add_argument("--slot", default=tlou.DEFAULT_SLOT)
    ap.add_argument("--build-dir", default="out")
    args = ap.parse_args()

    if os.path.abspath(args.archive) == os.path.abspath(args.out):
        raise SystemExit("Refusing to overwrite the archive you read from.")

    path = tlou.resolve_oodle(args.archive)
    if not path:
        raise SystemExit("Oodle library (oo2core_9_win64.dll) not found. Put it next to this "
                         "script, or set TLOU_OODLE to its full path, or pass --game.")
    psarc.OODLE_PATH = path

    files = {f"text2/{args.slot}.{name}": os.path.join(args.build_dir, "text2", f"{args.slot}.{name}")
             for name in tlou.TABLES}
    files["text2/eng.common"] = os.path.join(args.build_dir, "text2", "eng.common")
    missing = [p for p in files.values() if not os.path.exists(p)]
    if missing:
        raise SystemExit("Build the tables first (build_slot.py). Missing: " + ", ".join(missing))

    replace = {name: open(path, "rb").read() for name, path in files.items()}
    print(f"writing {args.out} from {args.archive} ...")
    t0 = time.time()
    psarc_injector.patch_psarc(args.archive, args.out, replace)
    print(f"done in {time.time() - t0:.1f}s, {os.path.getsize(args.out) / 1024 ** 3:.2f} GB")

    # --- check the patched archive: our tables exactly, everything else untouched ---
    bad = []
    a = psarc.PsarcArchive(args.out)
    b = psarc.PsarcArchive(args.archive)
    for name, want in replace.items():
        got = a.extract_by_name(name)
        ok = got == want
        print(f"  [{'ok' if ok else 'BAD'}] {name:30s} {len(got):8d} bytes")
        if not ok:
            bad.append(name)
    for name in ["text2/pol.common", "text2/eng.subtitles", "fonts/DINPro-Regular.otf"]:
        same = a.extract_by_name(name) == b.extract_by_name(name)
        print(f"  [{'ok' if same else 'BAD'}] {name:30s} untouched: {same}")
        if not same:
            bad.append(name)
    a.close()
    b.close()

    print("\nRESULT:", "patched archive is sound" if not bad else f"PROBLEM: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
