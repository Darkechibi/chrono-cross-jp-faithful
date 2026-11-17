# -*- coding: utf-8 -*-
"""Fix leftover names and lines that still name the wrong person."""
import os
import zipfile
from pathlib import Path

LANG = Path(r"lang.dat")

REPLACEMENTS = [
    ("It's Lynxy!", "It's Yamaneko-niichan!"),
    ("Because of them Porres!!!", "Because of you Parepori!!!"),
    ("Burned-out\\nHermit's Hideout", "Inja no Koya Ato"),
    ("promoted to general.", "promoted to colonel."),
    ("the general's ancestors", "the colonel's ancestors"),
    ("The general has", "The colonel has"),
    ("Is the general trying", "Is the colonel trying"),
    ("The general should", "The colonel should"),
    ("Help the general!!!", "Help the colonel!!!"),
    (
        "Mysterious Swordsman:\\nOh, pardon me, monsieur.\\nMoi forgot to introduce myself.{bpage}\\nMon name is {PIERRE%}.{wait(15)}\\nI am renting this room from\\nMonsieur {ZAPPA%}.{mend}",
        "Mysterious Swordsman:\\nOh, I was late\\nto introduce myself.{bpage}\\nMy name is\\n{PIERRE%}.{wait(15)}\\nI am renting this room from\\nMonsieur {ZAPPA%}.{mend}",
    ),
    (
        "monsieurs are like the\\ntrois stooges without me!",
        "without me, you are just\\nthe three-idiot trio!",
    ),
    (
        "Without my charm and\\ncomplexion, les guards\\nwill turn you away!",
        "Without me, you would\\nbe turned away\\nat the gate!",
    ),
    (
        "Without mon charm and\\ncomplexion, les guards\\nwill turn you away!",
        "Without me, you would\\nbe turned away\\nat the gate!",
    ),
    (
        "One graceful flash of mon sword\\nwill surely have them saluting\\nme as the guest of honor!",
        "One beautiful flash of my sword\\nwill surely have them welcome\\nme as a VIP!",
    ),
    ("lost mon precious", "lost my precious"),
    ("Sacré bleu! What am I to do?", "Ah, what am I to do?"),
    ("Sacré bleu!\\nWhat is a hero like me to do?", "Ah,\\nwhat should I do?"),
    (
        "Merci, merci, thank you!!!\\nAh well, what a darling\\nyou are!",
        "Arigato, thanks,\\nmerci, it's me!",
    ),
    ("rather vulgaire", "rather crude"),
    (
        "{PIERRE%}:\\nYoo-hoo, there!\\nMonsieur soldier-man!{bpage}\\nMe have come here to\\nto do you a favor and\\njoin the Ryukishidan.{bpage}\\nOpen the gates, {wait(20)}mon frère!\\nTa-ta-tah!{mend}",
        "{PIERRE%}:\\nThe lovely hero has come\\nall this way{bpage}\\nto join the Ryukishidan.{bpage}\\nNow,{wait(20)} open the gate\\nand let me through.{mend}",
    ),
    (
        "Ah well...\\nThey said, non.{bpage}\\nEven mon hero's medal\\ndidn't work.",
        "Hahaha...\\nThey refused me.{bpage}\\nEven with the hero's medal,\\nthey don't understand.",
    ),
    (
        "Is something wrongly\\nwrong, Monsieur {PIERRE%}?",
        "Is something the matter,\\n{PIERRE%}-dono?",
    ),
    (
        "This is it!{bpage}\\nThere is no\\nturning back now!",
        "The real fight starts now!{bpage}\\nIf you do not want to die,\\ndo not drop your guard!",
    ),
    (
        "Monsieur {PIERRE%}!\\nLet us be on our way!",
        "{PIERRE%}-dono!\\nLet us go!",
    ),
    (
        "It is you,\\nMonsieur {PIERRE%}!",
        "It is\\n{PIERRE%}-dono!",
    ),
    ("Me seem to have an upset", "I seem to have an upset"),
    (
        "Me should be fine...{wait(15)}\\nMe am a hero...\\nI-I'll do mon best...",
        "No need to worry...{wait(15)}\\nI-I'll manage\\nsomehow...",
    ),
]


def apply_text(text):
    for src, dst in REPLACEMENTS:
        n = text.count(src)
        print(f"  {n:2}  {src[:48]!r}")
        if n:
            # brace guard
            if src.count("{") != dst.count("{"):
                raise SystemExit("brace mismatch in replacement: " + src[:60])
            text = text.replace(src, dst)
    return text


def main():
    tmp = LANG.with_suffix(".dat.tmp")
    with zipfile.ZipFile(LANG, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "en.csv":
                text = data.decode("utf-8")
                text = apply_text(text)
                data = text.encode("utf-8")
            elif info.filename == "cmnmes.txt":
                text = data.decode("utf-16")
                nl = "\r\n" if "\r\n" in text else "\n"
                ends = text.endswith(("\n", "\r\n"))
                out = []
                changed = 0
                for line in text.splitlines():
                    parts = line.split("\t")
                    if parts and parts[0] == "ハッピーダン" and len(parts) > 1 and parts[1] == "Mojoy":
                        parts[1] = "Happy Dan"
                        line = "\t".join(parts)
                        changed += 1
                    out.append(line)
                print("cmnmes Happy Dan", changed)
                body = nl.join(out)
                if ends:
                    body += nl
                data = body.encode("utf-16")
            zout.writestr(info, data)
    os.replace(tmp, LANG)
    with zipfile.ZipFile(LANG, "r") as z:
        en = z.read("en.csv").decode("utf-8")
    for w in ("Lynxy", "Porres", "Hermit's", "mon ", "vulgaire", "Sacré", "trois", "Yamaneko-niichan", "Parepori", "Inja no Koya", "general public", "to colonel", "Mojoy"):
        print(f"left {w}: {en.count(w)}")


if __name__ == "__main__":
    main()
