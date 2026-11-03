# Installing the translation

The game loads `build\pc\main\core.psarc`. The patched archive built by `tools/inject.py`
replaces that one file. Two things matter: keep a clean copy of the original, and let the
script do the copy so the sizes and checksums are checked.

## One-time: keep the original safe

```powershell
mkdir E:\tlou -Force
copy "D:\SteamLibrary\steamapps\common\The Last of Us Part I\build\pc\main\core.psarc" `
     "E:\tlou\core_pristine.psarc"
```

`core_pristine.psarc` is 5.87 GB. Keep it: every future build starts from it, and it is what
you restore if something goes wrong. The build and install scripts refuse to work with a
backup that has been changed.

## Install

```powershell
python tools\inject.py --archive "E:\tlou\core_pristine.psarc" `
    --out "E:\tlou\core_translated.psarc" --build-dir out

powershell -File tools\swap_in.ps1 -Patched "E:\tlou\core_translated.psarc" -Backup "E:\tlou\core_pristine.psarc"
```

`swap_in.ps1`

1. stops if the game is running,
2. stops if the backup is not the file it was the first time (it stores `core_pristine.md5`),
3. frees space on the game drive, copies the patched archive in, and compares checksums,
4. tells you the result.

Typical room needed: the game drive must hold one more 5.87 GB archive for a moment.

## In the game

**Options → Text Language →** the name you passed as `--label` (for the Lithuanian
translation: **Lietuvių**).

The game sometimes switches back to the Steam language on the first start after an update.
Set the Steam client's language for the game to anything, then choose the language in the
game's own menu again.

## Restore the original

```powershell
copy "E:\tlou\core_pristine.psarc" "D:\SteamLibrary\steamapps\common\The Last of Us Part I\build\pc\main\core.psarc"
```

Or let Steam do it: **right-click the game → Properties → Installed Files → Verify integrity
of game files**. That downloads the original archive again and removes the translation —
handy after a game update that broke something.

## If something looks wrong

| symptom | cause |
|---|---|
| the game shows `UNKNOWN STRING!!!` | a string was removed or an id was changed while editing |
| the menu has no new language | `--label` was not passed, or the slot's autonym was wrong |
| text shows as boxes `□□□` | your language needs a font the game does not have |
| the game does not start, or crashes on the menu | the archive was written to while the game was running, or the copy was interrupted — reinstall from the backup |
| after a game update the translation is gone | Steam replaced `core.psarc`; rebuild and install again |
