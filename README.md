# Chrono Cross JP-Faithful (Steam)

English language pack for **CHRONO CROSS: THE RADICAL DREAMERS EDITION** (Steam) that keeps proper nouns as Japanese readings (romaji), removes the localization’s cartoon accents, and corrects lines that invented jokes or misnamed people/places.

You need a legal Steam copy of the game. This project does **not** include the game binary.

## What it changes

- Character / enemy / place names → romaji of the Japanese (e.g. Yamaneko, Jakotsu, Shugaru, Solton, Tsukuyomi, Parepori, Mabure, Koryu no Toride)
- `mesgen_en.csv` accent table flattened to neutral English
- Hardcoded eye-dialect and fake national accents cleaned where they were inventing flavor
- Clear misrepresentations fixed against the Japanese script

Common English words stay English so dialogue still reads. This is not a full line-by-line retranslation of every sentence.

## Install

1. Install / update the game on Steam (English).
2. Close the game.
3. Run:

```powershell
cd installer
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Or:

```text
python installer/install.py
```

Optional: set `CHRONO_CROSS_PATH` to the game root if Steam auto-detect fails.

The installer:

- finds the Steam install (appid `1133760`)
- backs up `data/lang.dat` once as `lang.dat.before-jp-faithful`
- replaces the English language members inside `lang.dat`

### After Steam “Verify integrity” / redownload

Steam will restore stock English. Run the installer again.

## Uninstall

Restore the backup:

```text
copy /Y "data\lang.dat.before-jp-faithful" "data\lang.dat"
```

(from the game folder), or use Steam → Verify integrity of game files.

## Requirements

- Windows (installer auto-detects Steam libraries; other OS: set `CHRONO_CROSS_PATH`)
- Python 3.8+

## Source

`source/` holds the Python tools used to build this pack from a stock `lang.dat` (dialect flatten, name restore, invent/option fixes). The playable pack is the files in `patch/`, applied by `installer/install.py`.

## Legal

Chrono Cross and all related assets are © Square Enix. This repository distributes a fan-made language modification for owners of the Steam release only. Scripts in this repo are MIT-licensed; game text remains Square Enix property.
