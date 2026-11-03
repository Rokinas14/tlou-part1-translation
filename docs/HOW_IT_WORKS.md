# How the text of this game is stored

Notes from the reverse engineering behind these tools. Everything here is verified against
the retail PC build 1.1.4.0 (Steam app 1888930).

## Where the text lives

```
build\pc\main\core.psarc      5.87 GB, PSARC v1.4, Oodle Kraken, 14 063 entries
  text2\eng.common                    16 962 strings  menus, items, notes, journals
  text2\eng.subtitles                 13 672 strings  story dialogue
  text2\eng.subtitles-systemic        32 875 strings  enemy and companion barks
  text2\<lang>.*                      the same three tables for 25 more languages
  text2\sid-lookup                   string id -> the name of its voice file
  fonts\…                            DINPro, Helvetica, Utrillo, CJK fonts
```

63 509 strings, 321 089 English words. `eng.subtitles-systemic` is not developer text, as is
often assumed: it is what the player hears from enemies and companions during play
("Check that room.", "One down."), and it is shown as subtitles.

## Table format

```
u32 count | count x (u64 string id, u64 offset) | block of NUL-terminated UTF-8 strings
```

- Offset 0 of the block always holds the 18-byte fallback `UNKNOWN STRING!!!`.
- Real strings are stored in a different physical order than the id table, and several ids
  can share one offset (identical sentences are stored once).
- Both facts matter when writing: **replace strings by offset, copy every other string byte
  for byte.** Rebuilding with a naive re-serialisation changes the file by a single byte and
  the game refuses it. `tools/tlou.py` (`Table.build`) does it correctly and reproduces the
  original tables byte-identically.

## Language slots

The text language is a slot; a translation takes over one of the 26. The five Asian slots
carry their own fonts and are the worst choice. Every Latin slot renders with the default
DINPro face, so `hun`, `cze`, `pol`, `dut`, `fre`, `ger`, `ita`, `spa`, `swe`, `tur`, `bra`,
`sas`, `hrv`, `dan`, `fin`, `nor`, `por` are all safe.

`eng.common` also holds the language-name labels (endonyms), which is why one string edit in
it renames the slot in the menu: `Magyar` → `Lietuvių`.

Speech/voice language is a separate setting and is untouched.

## Fonts

| font | used for | Latin Extended (ąčęėįšųūž) |
|---|---|---|
| DINPro-Regular | body text, subtitles | all letters, upper and lower case |
| DINPro-Medium | menus, HUD | all letters |
| HelveticaNeueBold | a few headings | only š, ž |
| SIE-UtrilloPro-DB | handwritten notes | only š, ū, ž |

Lithuanian, Polish, Czech, Turkish and most European languages need **no font work**. The
Cyrillic, Greek and CJK slots use separate fonts; translating into those languages means
replacing the font of the slot you take over.

## Voice files: who speaks a line

`text2\sid-lookup` is `u32 count | count x (u64 id, u64 offset) | strings` and maps every
string id to the name of its voice line:

```
0004bfa7852ca960 -> ELL_GAM_BIL_APPROACH_ROAD_012     (Ellie, scene "GAM_BIL_APPROACH_ROAD")
0001277f1f735b28 -> badf-gen-enmy-srch-spt-plyr-study-sp-001
```

The name carries the speaker code (`ELL`, `JOL`, `TES`, `RIL`, `BLL`, `HEN`, `SAM`, `TMY`,
`DAV`, `MRL`, `SAR`, `MAR`, `ANN`; `BAD*` are generic enemies, `SUB` is unknown) and the
scene. Lines of one scene share the scene part, so a scene with exactly two codes gives the
addressee. This is how the gender pass in `data/lt_tm.json` was checked: 46 506 lines mapped,
2 721 scenes, 404 two-speaker scenes.

Subtitle **timing** is not in these tables — it lives in the level archives
(`world-*.psarc`) and is not needed to translate the text.

## Rebuilding and installing

1. `build_slot.py` reads the pristine archive, builds the three tables of the slot, and the
   English table with the renamed label.
2. `inject.py` replaces those four entries inside a copy of the archive with Oodle Kraken
   compression (~25 s for 6 GB) and then re-reads the copy: our entries must match the built
   files exactly, and unrelated entries must stay byte-identical.
3. `swap_in.ps1` copies the copy into the game, refusing to run while the game is open and
   checking the pristine backup first.

Confirmed by hand: the rebuilt tables are byte-identical to a build the game accepted, and the
patched archive loads with 14 063 entries and an intact font and subtitle table.

## Pitfalls that cost time

- A missing id prints `UNKNOWN STRING!!!` in game; never delete rows, only translate them.
- Several ids share an offset: changing one changes every id that points at it.
- The game reads the archive once at start; replacing it while the game runs corrupts nothing
  but has no effect until a restart, and a half-copied file does crash the game.
- Steam "verify integrity" and every game update restore the original archive.
- Long strings are not wrapped everywhere: `problems()` in `data` conversions warns above
  2.5x the English length for a reason.
