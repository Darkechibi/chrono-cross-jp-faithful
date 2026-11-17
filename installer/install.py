#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply the JP-faithful English language pack to a Steam install of
CHRONO CROSS: THE RADICAL DREAMERS EDITION.

Safe to re-run after Steam verifies / redownloads game files.
Requires a legal copy of the game. Does not modify Steam itself.
"""
from __future__ import annotations

import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

VERSION = "0.01"
APPID = "1133760"
# Steam installdir uses two spaces between CROSS and THE
DIR_HINTS = (
    "CHRONO CROSS  THE RADICAL DREAMERS EDITION",
    "CHRONO CROSS THE RADICAL DREAMERS EDITION",
)
PATCH_FILES = (
    "en.csv",
    "btel_en.csv",
    "mesgen_en.csv",
    "sysmes.txt",
    "keyitem.txt",
    "shopmenu.txt",
    "cmnmes.txt",
)
BACKUP_NAME = "lang.dat.before-jp-faithful"


def patch_dir() -> Path:
    here = Path(__file__).resolve().parent
    for cand in (here / "patch", here.parent / "patch"):
        if (cand / "en.csv").is_file():
            return cand
    raise SystemExit("patch/ folder with en.csv not found next to this installer.")


def steam_libraries() -> list[Path]:
    libs: list[Path] = []
    candidates: list[Path] = []
    if sys.platform == "win32":
        try:
            import winreg

            for root, path in (
                (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam"),
            ):
                try:
                    with winreg.OpenKey(root, path) as key:
                        val, _ = winreg.QueryValueEx(key, "SteamPath")
                        if val:
                            candidates.append(Path(val))
                except OSError:
                    pass
        except ImportError:
            pass
        for drive in "CDEFG":
            candidates.append(Path(f"{drive}:/Program Files (x86)/Steam"))
            candidates.append(Path(f"{drive}:/Program Files/Steam"))
            candidates.append(Path(f"{drive}:/SteamLibrary"))
            candidates.append(Path(f"{drive}:/Steam"))
    else:
        home = Path.home()
        candidates.extend(
            [
                home / ".steam/steam",
                home / ".local/share/Steam",
                Path("/usr/share/steam"),
            ]
        )

    seen = set()
    for steam in candidates:
        steam = steam.resolve() if steam.exists() else steam
        if not steam.exists():
            continue
        key = str(steam).lower()
        if key in seen:
            continue
        seen.add(key)
        libs.append(steam)
        vdf = steam / "steamapps" / "libraryfolders.vdf"
        if vdf.is_file():
            text = vdf.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r'"path"\s+"([^"]+)"', text):
                p = Path(m.group(1).replace("\\\\", "\\"))
                if p.exists():
                    k = str(p.resolve()).lower()
                    if k not in seen:
                        seen.add(k)
                        libs.append(p.resolve())
    return libs


def find_game() -> Path | None:
    env = os.environ.get("CHRONO_CROSS_PATH")
    if env:
        p = Path(env)
        if (p / "data" / "lang.dat").is_file():
            return p
    for lib in steam_libraries():
        common = lib / "steamapps" / "common"
        if not common.is_dir():
            continue
        for name in DIR_HINTS:
            game = common / name
            if (game / "data" / "lang.dat").is_file():
                return game
        # fuzzy: any folder starting with CHRONO CROSS
        try:
            for child in common.iterdir():
                if child.is_dir() and child.name.upper().startswith("CHRONO CROSS"):
                    if (child / "data" / "lang.dat").is_file():
                        return child
        except OSError:
            pass
        # appmanifest hint
        manifest = lib / "steamapps" / f"appmanifest_{APPID}.acf"
        if manifest.is_file():
            text = manifest.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r'"installdir"\s+"([^"]+)"', text)
            if m:
                game = common / m.group(1)
                if (game / "data" / "lang.dat").is_file():
                    return game
    return None


def apply_patch(game: Path, files: Path) -> None:
    lang = game / "data" / "lang.dat"
    if not lang.is_file():
        raise SystemExit(f"lang.dat not found at {lang}")

    backup = game / "data" / BACKUP_NAME
    if not backup.is_file():
        shutil.copy2(lang, backup)
        print(f"Backup created: {backup.name}")
    else:
        print(f"Backup already present: {backup.name}")

    payload = {name: (files / name).read_bytes() for name in PATCH_FILES}
    for name, data in payload.items():
        if not data:
            raise SystemExit(f"Empty patch file: {name}")

    tmp = lang.with_suffix(".dat.tmp")
    replaced = 0
    with zipfile.ZipFile(lang, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
        for info in zin.infolist():
            data = payload.pop(info.filename, None)
            if data is not None:
                replaced += 1
            else:
                data = zin.read(info.filename)
            # preserve compress type when possible
            if info.filename in PATCH_FILES:
                zi = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
                zi.compress_type = info.compress_type
                zi.external_attr = info.external_attr
                zout.writestr(zi, data)
            else:
                zout.writestr(info, data)
        # if a patch file was missing from the zip, append it
        for name, data in payload.items():
            zout.writestr(name, data)
            replaced += 1
            print(f"Added missing archive member: {name}")

    os.replace(tmp, lang)
    print(f"Patched {replaced} file(s) in lang.dat")
    print(f"Game: {game}")
    print("Done. Launch the English Steam build to play.")


def main() -> None:
    print(f"Chrono Cross JP-Faithful installer v{VERSION}")
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print("Optional: set CHRONO_CROSS_PATH to the game root folder.")
        print("Usage: python install.py")
        return
    files = patch_dir()
    game = find_game()
    if not game:
        raise SystemExit(
            "Could not find Chrono Cross (Radical Dreamers Edition).\n"
            "Install it on Steam, or set CHRONO_CROSS_PATH to the game folder."
        )
    apply_patch(game, files)


if __name__ == "__main__":
    main()
