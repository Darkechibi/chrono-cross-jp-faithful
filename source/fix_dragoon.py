# -*- coding: utf-8 -*-
import os, zipfile
from pathlib import Path
LANG = Path(r"lang.dat")
tmp = LANG.with_suffix(".dat.tmp")
with zipfile.ZipFile(LANG, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == "en.csv":
            t = data.decode("utf-8")
            t = t.replace("Dragoons", "knights")
            t = t.replace("Dragoon", "Knight")
            t = t.replace("dragoon", "knight")
            data = t.encode("utf-8")
        zout.writestr(info, data)
os.replace(tmp, LANG)
en = zipfile.ZipFile(LANG).read("en.csv").decode("utf-8")
print("Dragoon", en.count("Dragoon"), "dragoon", en.count("dragoon"))
