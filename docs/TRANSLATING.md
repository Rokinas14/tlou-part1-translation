# Translating the game, step by step

You do not need to know how the archive works. Five commands and one spreadsheet is the
whole job.

## 0. Once

- install Python 3.10+ and run `pip install -r requirements.txt`
- copy `core.psarc` somewhere with room, as shown in [INSTALL.md](INSTALL.md)

## 1. Get the strings

```powershell
python tools\export_dialog.py --archive "E:\tlou\core_pristine.psarc" --out data --xlsx --name tlou_part1_text_english
```

You get `data\tlou_part1_text_english.xlsx` with four columns:

| id | table | english | translation |
|---|---|---|---|
| `0x0004bfa7852ca960` | subtitles | Why don't you just take me back to Marlene? | |

63 509 rows, about 321 000 words. Do not sort or filter the file in a way that moves rows
around — the id is what matters, and it travels with the row.

## 2. Translate

Work in the **translation** column, top to bottom. Practical advice from a finished
translation:

- **Start with the menu (`common`).** 17 000 strings, but most are one or two words, and
  the game becomes usable in your language the moment they are done.
- **Subtitles (`subtitles`)** are the story: 13 672 strings, ~11 000 distinct sentences.
  Use a text editor with search, or the filter in Excel, to keep repeated lines consistent.
- **Barks (`subtitles-systemic`)** are 32 875 lines of enemy and companion chatter;
  65 % of them are duplicates of another line, so translating one sentence fixes several.
  A translation memory tool, or the `import_dialog.py` repeat-filling below, saves most of
  the work.
- Leave a row empty when you are unsure. English stays in place, nothing breaks.

### What must survive

Checked automatically on import, refused when broken:

| keep | example |
|---|---|
| button icons | `|move|`, `|menu:select|`, `|gen:jump|` |
| text tags | `<font color="t2-red">…</font>`, `<br>`, `<break/>`, `<img src="…">` |
| placeholders | `[A]`, `[TEXT]`, `[TIME]`, `%s`, `in_percent` |
| line breaks | a line with two rows of subtitles has one `\n` |
| edge spaces | if the English ends with a space, keep it |

### Names, tone, swearing

Decide early and write it down (`docs/STYLE_GUIDE.md` in this repository is a worked
example): how names are spelled and declined, whether characters address each other with
*tu* or *jūs*, how strong the swearing is. Consistency matters more than any single choice.

## 3. Read the file back

```powershell
python tools\import_dialog.py --file data\tlou_part1_text_english.xlsx --tm data\my_tm.json
```

The command prints how many lines it took, how many were unchanged and which lines it
refused, with the reason. Fix those and run it again; nothing is lost.

## 4. Build and install

```powershell
python tools\build_slot.py --archive "E:\tlou\core_pristine.psarc" --tm data\my_tm.json `
    --labels data\my_labels.json --label "Lietuvių" --out out
python tools\inject.py --archive "E:\tlou\core_pristine.psarc" --out "E:\tlou\core_translated.psarc" --build-dir out
powershell -File tools\swap_in.ps1 -Patched "E:\tlou\core_translated.psarc" -Backup "E:\tlou\core_pristine.psarc"
```

`build_slot.py` prints the coverage of each table, for example:

```
  hun.common              16962 strings, 15146 translated (89.3%)
  hun.subtitles           13672 strings, 13333 translated (97.5%)
  hun.subtitles-systemic  32875 strings, 32861 translated (100.0%)
```

## 5. Repeat

Translation is a loop: translate, import, build, install, play, fix. A build takes about a
second; installing takes under two minutes. Nothing in the game changes until you run
`swap_in.ps1`.

## Taking over the work of someone else

`data/lt_tm.json` is a finished translation in the format `import_dialog.py` writes. Open it
in a text editor, or import it into your spreadsheet as a lookup by id, and you have a
complete reference translation for Lithuanian — tone, names, swearing and all.

## When a line is wrong in the game

Note what is said and to whom. If you keep the id next to your notes (the game does not show
it, but the dialogue file is searchable by the English text), the fix is one row.
