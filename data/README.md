# The text of the game, as files

Everything the game shows as text — dialogue, subtitles, barks, menu labels, item names and
descriptions, notes, letters and journals — is in these files: 63 509 strings in three tables.

| file | columns | what it is |
|---|---|---|
| `tlou_part1_text_english.tsv` | id, table, english, translation | **start here** — every string of the game, translation column empty |
| `tlou_part1_text_english.xlsx` | the same, in Excel | the same file for a spreadsheet |
| `dialog_lithuanian.tsv` | id, table, english, translation | the same strings with the finished Lithuanian translation filled in |
| `dialog_lithuanian.xlsx` | the same, in Excel | |
| `lt_tm.json` | id → text | the Lithuanian translation as the tools read and write it |
| `labels_lt.json` | english label → text | 146 short menu labels |
| `lt_skip.json` | id → reason | strings that are never translated (credits, icons, a test string) |

## The three tables

| table | strings | what it holds |
|---|---|---|
| `common` | 16 962 | menu labels and descriptions, item names, collectibles, **notes, letters and journals** |
| `subtitles` | 13 672 | the story: every spoken line with subtitles |
| `subtitles-systemic` | 32 875 | enemy and companion barks during play ("Check that room.", "One down.") |

## Row rules

- `id` is the game's string id. Do not change it, do not sort it away.
- `table` says which of the three tables the row belongs to.
- `english` is the original text.
- `translation` is yours. The Lithuanian file shows what a finished column looks like.
- Line breaks appear as `\n`, tabs as `\t`.
- Several ids can carry the same sentence — the game stores identical sentences once.
  65 % of the barks repeat another line, so one translated sentence can cover several ids.

Rows whose English is empty, or nothing but a button token (`|move|`), an icon or a number,
cannot be translated; they are listed in `lt_skip.json` with the reason.

## Regenerating these files

They come from your own copy of the game, so they always match your version:

```powershell
python tools\export_dialog.py --archive "E:\tlou\core_pristine.psarc" --out data --xlsx
```
