# -*- coding: utf-8 -*-
import os
import zipfile
from pathlib import Path

LANG = Path(r"lang.dat")
REPLACEMENTS = [
    (
        "{PIERRE%}:\\nOhhhhhh...{wait(15)}\\nMe don't feel so good...{bpage}\\nOhhh... Mon stomach...\\nUrgh...{mend}",
        "{PIERRE%}:\\nHaa...{wait(15)}\\nMy stomach,{bpage}\\nafter all...!{mend}",
    ),
    (
        "{KID%}:\\nMon chéri,\\nMon SHMERI!{mend}",
        "{KID%}:\\nWhat do you mean,\\n'ufufu'!\\nThat's disgusting.{mend}",
    ),
]
tmp = LANG.with_suffix(".dat.tmp")
with zipfile.ZipFile(LANG, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == "en.csv":
            text = data.decode("utf-8")
            for src, dst in REPLACEMENTS:
                if src.count("{") != dst.count("{"):
                    raise SystemExit("braces")
                n = text.count(src)
                print(n, src[:40])
                text = text.replace(src, dst)
            data = text.encode("utf-8")
        zout.writestr(info, data)
os.replace(tmp, LANG)
