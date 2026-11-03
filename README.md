# The Last of Us Part I — translation toolkit

Tools and instructions to translate **The Last of Us Part I** (PC, Steam app 1888930) into
any language, plus a finished **Lithuanian** translation you can install as is.

The game keeps all of its text in three small tables inside one archive
(`core.psarc → text2/`). This toolkit reads those tables, gives you every string in one
editable spreadsheet, and writes your translation back into the archive. No game files are
changed until you ask for it, and your own language file never leaves your computer.

> **What this repository does not contain:** the game, its audio, fonts or any of its
> files. See [NOTICE.md](NOTICE.md).

## What is inside

```
tools/     the scripts (Python 3.10+)
data/      the dialogue file, the Lithuanian translation, menu labels
docs/      how it works, step-by-step guide, style guide, glossary
```

| file | what it is |
|---|---|
| `data/dialog_lithuanian.xlsx` | **every string of the game in Excel**: id, table, English, Lithuanian |
| `data/dialog_lithuanian.tsv` | the same as plain text (tab separated) |
| `data/lt_tm.json` | the finished Lithuanian translation, the drop-in file |
| `data/labels_lt.json` | 146 short menu labels |
| `data/lt_skip.json` | strings that are never translated (credits, icons) |

63 509 strings: 16 962 menu and item text, 13 672 story subtitles, 32 875 barks
(enemy and companion chatter).

## Requirements

- Windows, the game installed through Steam
- Python 3.10 or newer (`python --version`)
- about 13 GB of free disk space on a scratch drive (the archive is 6 GB and is always
  written to a copy, never over the live file)
- the Oodle library `oo2core_9_win64.dll` that ships with the game — the tools find it
  automatically when the game is installed, or set `TLOU_OODLE` to its path

```powershell
pip install -r requirements.txt      # only openpyxl, and only for the Excel file
```

## Quick start

```powershell
# 1. make a clean backup of the archive (once, keep it safe)
copy "D:\SteamLibrary\steamapps\common\The Last of Us Part I\build\pc\main\core.psarc" "E:\tlou\core_pristine.psarc"

# 2. write every string of the game into one file, with your translation column
python tools\export_dialog.py --archive "E:\tlou\core_pristine.psarc" --out data --xlsx

# 3. translate the last column of data\dialog_english.xlsx, save it

# 4. read your file back into the translation memory
python tools\import_dialog.py --file data\dialog_english.xlsx --tm data\my_tm.json

# 5. build the three tables for a language slot and put them into a copy of the archive
python tools\build_slot.py --archive "E:\tlou\core_pristine.psarc" --tm data\my_tm.json `
    --labels data\my_labels.json --label "Lietuvių" --out out
python tools\inject.py --archive "E:\tlou\core_pristine.psarc" --out "E:\tlou\core_translated.psarc" --build-dir out
```

Then install the result: see [docs/INSTALL.md](docs/INSTALL.md).

You do not have to translate in one go: untranslated strings fall back to English, so the
game is readable at any stage and you can install after every session.

## The language slot

The game has 26 language slots. The translation goes into one of them — by default `hun`
(Hungarian), which nobody needs — and that slot is renamed to your language, so it shows up
in the menu as, for example, **Lietuvių**. Nothing else is touched:

```powershell
python tools\build_slot.py ... --slot hun --autonym Magyar --label "Lietuvių"
```

`--autonym` is the name the game itself uses for that slot (open the language menu and copy
it), `--label` is what you want it to read.

## Working with the dialogue file

| column | meaning |
|---|---|
| `id` | the game's string id — never change it |
| `table` | which of the three tables it belongs to |
| `english` | the original text |
| `translation` | **you fill this in** |

Rules that cost time when broken (they are checked on import):

- keep everything between `|` — `|move|`, `|menu:select|` are button icons
- keep the tags `<font …>`, `</font>`, `<br>`, `<break/>`, `<img …>` exactly as they are
- keep `[A]`, `[TEXT]`, `[TIME]`, `%s`, `in_percent` as they are
- keep line breaks (they appear as `\n` in the TSV)
- do not add a space at the start or the end unless the English has one

`import_dialog.py` refuses a line that breaks any of these instead of writing it into the
game.

## Menu labels

Short labels (`CRAFTING`, `RECORDS`, `OPTIONS`…) live in `data/labels_lt.json` as
`{"CRAFTING": "GAMINIMAS"}`. Add your own pairs there; anything not listed uses the full
translation from your dialogue file, or English.

## Installing

See [docs/INSTALL.md](docs/INSTALL.md): a script copies the patched archive into the game,
checks the backup first, and refuses to run while the game is open.

## The Lithuanian translation

`data/lt_tm.json` (61 340 strings) is the finished translation this project started as. Its
glossary, style decisions and the reasoning behind them are in
[docs/STYLE_GUIDE.md](docs/STYLE_GUIDE.md) and [docs/GLOSSARY_lt.md](docs/GLOSSARY_lt.md) —
useful as a model for your own language, and the parts about tone, swearing and gender work
the same way in any language.

## Known limits

- **Subtitles have no timing in these tables.** The game takes timing and speaker from the
  level files; translating the text is enough, but you cannot retime a line from here.
- **Text length.** The game does not wrap long lines gracefully in every place; keep
  sentences close to the English length.
- **Fonts.** The game's fonts already cover Latin Extended (Latin, Lithuanian, Polish,
  Czech…). Cyrillic, Greek and CJK need a font from the game's own slots, which is a
  separate job.
- The game is updated sometimes; after a patch, `verify` the archive again and re-install.

## Credits

- Tools, Lithuanian translation, glossary: **Rokinas14**
- Reverse engineering notes: see [docs/HOW_IT_WORKS.md](docs/HOW_IT_WORKS.md)

## Legal

The tools and the translation text are published under the MIT licence (see
[LICENSE](LICENSE)). The game, its text, fonts and audio belong to Naughty Dog and Sony
Interactive Entertainment. Read [NOTICE.md](NOTICE.md) before you publish your own
translation.
