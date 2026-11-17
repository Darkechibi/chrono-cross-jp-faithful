# -*- coding: utf-8 -*-
import os, zipfile
from pathlib import Path
LANG = Path(r"lang.dat")
subs = [
    ("Ain't that right", "Isn't that right"),
    ("Ain't nothing", "Nothing"),
    ("ain't", "aren't"),
    ("Ain't", "Aren't"),
    ("apprentice\\ndragoon", "apprentice\\nknight"),
    ("fine\\ndragoon", "fine\\nknight"),
    ("dragoon youth", "knight youth"),
    ("dragoon,", "knight,"),
    ("dragoon.", "knight."),
    ("dragoon?", "knight?"),
    (" a dragoon", " a knight"),
    ("dragoon", "knight"),
]
tmp = LANG.with_suffix(".dat.tmp")
with zipfile.ZipFile(LANG, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == "en.csv":
            t = data.decode("utf-8")
            for a, b in subs:
                t = t.replace(a, b)
            data = t.encode("utf-8")
        zout.writestr(info, data)
os.replace(tmp, LANG)
en = zipfile.ZipFile(LANG).read("en.csv").decode("utf-8")
print("Ain", en.count("Ain"), "dragoon", en.count("dragoon"))
