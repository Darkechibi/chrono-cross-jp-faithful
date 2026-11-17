# -*- coding: utf-8 -*-
import os, zipfile
from pathlib import Path

LANG = Path(r"lang.dat")

NEW = {
# truncated + missing choices
"78\t72":
"{KID%}:\\nWhat are you scared of?\\nQuit your complaining.{bpage}\\nDon't you want to make clear\\nwhat happened ten years ago,\\nand what's going on now?{bpage}\\nThe only leads are\\nthe Acacia Ryukishidan...{bpage}\\nAnd the one who leads them,\\nColonel {VIPER%}.\\nJust them.{bpage}\\nIf we're looking into the\\nAcacia Ryukishidan, we have to\\nsneak into that {VIPER%} guy's manor.{bpage}\\nCome on, {SERGE%}.\\n　　　Alright, let's do it\\n　　　No, I refuse{mend}",

"27\t45":
"Una:\\nWHAT!? What did you say!?{wait(30)}\\nBig bro {-y}{SERGE%}!?{wait(30)}\\nYou're...!?{bpage}\\nDon't screw with me!{wait(20)}\\nBig bro {-y}{SERGE%} is\\na proper human!{bpage}\\nHe's not some ajin\\nlike you!{wait(20)}\\nStop making stuff up!{mend}",

"27\t72":
"Oh, how unusual.{wait(20)}\\nIt's been quite a while since\\nI've seen an ajin\\nin this village.{bpage}\\nI hear these days you only\\nsee ajin around Guldove\\nand Zelbess.{mend}",

"375\t7":
"Where'd that ajin waitress go?\\nI'm dying of thirst.{mend}",

# Genesis -> Hajimari no Chi letter reveal (match JP wait count ~6)
"226\t35":
"{KID%}:\\nYou heard the story from the\\nvillage miko, right?{wait(20)}\\n{speed(72)}The story about\\n“{wait(0)}Ha{wait(0)}ji{wait(0)}ma{wait(0)}ri{wait(0)}no{wait(0)}Chi{wait(0)}.”{mend}",

# photo memory layout closer to JP (names appear on later pages in JP)
"63\t0":
"{fset(0)}{speed(255)}For eternal memories\\n　　Summer, age 12　　　\\n　　　　　　　　　　{fwait(5)}{wend(1)}",
"63\t1":
"{speed(255)}　　　　　　　　　　\\n　　　　　　　　　　\\n　　　　　　　　　　\\n　　{SERGE%}　　{fwait(5)}{wend(1)}",
"63\t2":
"{speed(255)}　　　　　　　　　　\\n　　　　　　　　　　\\n　　　　　　　　　　\\n　　　　　　　　　　\\n　　{LEENA%}　　{wait(60)}{bwait}{fset(5)}{wend(1)}",

"47\t16":
"For tomorrow, part 1~\\n　　Use what's lying around\\n　　and corner it well!{mend}",
"47\t17":
"For tomorrow, part 2~\\n　　Use the terrain,\\n　　and strike by surprise!{mend}",
"47\t18":
"For tomorrow, part 3~\\n　　Some like a chase,\\n　　and run round and round!{mend}",

"245\t0":
"{speed(64)}...This forest... died...\\n\\n　　　The Hydra too... ...perished\\nThose to hate...　　　humans\\n\\nHear the planet's voice... its pain...\\n\\n　　　　Humans...{mend}",
"245\t14":
"{speed(255)}...This forest... died...\\n\\n　　　The Hydra too... ...perished\\nThose to hate...　　　humans\\n\\nHear the planet's voice... its pain...\\n\\n　　　　Humans...{mend}",

"387\t49":
"　　Winning　　　\\n　　was everything...　　　{mend}",
"387\t52":
"　　　Having lost everything,\\n　　scars that were once pride\\nbegin to ache...{mend}",

"469\t85":
"　　{speed(32)}Kingdom Year 1000{wait(20)}\\n　　 Marudia's Bell{wait(40)}\\n　　O our prayer for peace{wait(20)}\\n　Ring out forever...{mend}",

"477\t2":
"Chronopolis Military Research Center{bpage}\\n“　Everlasting peace\\n　　　for the world's children　”\\n　　　　　　　2400{mend}",
}

# global scrap
GLOBAL = [
    ("demi-\\nhuman", "ajin"),
    ("demi-human", "ajin"),
    ("Demi-human", "Ajin"),
    ("Demi-Human", "Ajin"),
]


def main():
    tmp = LANG.with_suffix(".dat.tmp")
    hit = g = 0
    with zipfile.ZipFile(LANG, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "en.csv":
                text = data.decode("utf-8")
                nl = "\r\n" if "\r\n" in text else "\n"
                ends = text.endswith(("\n", "\r\n"))
                out = []
                for line in text.splitlines():
                    a = line.split("\t", 2)
                    if len(a) == 3:
                        key = a[0] + "\t" + a[1]
                        if key in NEW:
                            a[2] = NEW[key]
                            hit += 1
                        else:
                            body = a[2]
                            for s, d in GLOBAL:
                                if s in body:
                                    body = body.replace(s, d)
                                    g += 1
                            a[2] = body
                        line = "\t".join(a)
                    out.append(line)
                body = nl.join(out) + (nl if ends else "")
                data = body.encode("utf-8")
            zout.writestr(info, data)
    os.replace(tmp, LANG)
    print("exact", hit, "global", g)

    # verify
    z = zipfile.ZipFile(LANG)
    en = z.read("en.csv").decode("utf-8")
    for w in ("demi-human", "demi-\\nhuman", "Genesis", "Land of"):
        print(w, en.count(w))
    for line in en.splitlines():
        a = line.split("\t", 2)
        if a[:2] == ["78", "72"]:
            print("78/72 has choices", "Alright, let's do it" in a[2], "mend", "{mend}" in a[2])
            print("len", len(a[2]))


if __name__ == "__main__":
    main()
