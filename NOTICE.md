# Copyright notice — read before publishing a translation

## What this repository contains

- the scripts in `tools/` — written for this project, MIT licensed
- the Lithuanian translation in `data/` — a derivative work of the game's script
- a dialogue file exported from the game

**No game files are included:** no archive, no audio, no fonts, no executable. The tools
read them from your own installed copy.

## What that means for publishing

The text of The Last of Us Part I is © Naughty Dog / Sony Interactive Entertainment. A
translation of it is a **derivative work**: publishing the whole dialog — the English
original and the translation together — is legally different from publishing a patch tool.

Three options, in order of risk:

1. **Tools only (safest).** Publish `tools/` and the documentation. Everyone makes the
   dialogue file from their own copy with `export_dialog.py`. Nothing of the game's text is
   redistributed.
2. **Tools + translation without the English column.** Publish the scripts and the
   translation file (`lt_tm.json`: string ids and translated sentences). Reviewers can still
   read the work; the game's English text is not republished. This is what most translation
   projects do.
3. **Everything, including the exported dialog.** Convenient, and the most exposed: it is a
   public copy of a large part of the game's script. Some projects publish it and simply
   remove it on request; others get a takedown notice.

If you publish the full dialogue file anyway, keep the sentence in the README that this is a
non-commercial fan translation, add the copyright line above, and be ready to remove the
exported data while keeping the tools and the translation.

## Credits and marks

The Last of Us is a trademark of Sony Interactive Entertainment. This project is not
affiliated with, endorsed by or sponsored by Naughty Dog or Sony.
