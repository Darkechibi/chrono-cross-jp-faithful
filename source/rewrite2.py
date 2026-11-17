# -*- coding: utf-8 -*-
import os, re, zipfile
from pathlib import Path
LANG = Path(r"lang.dat")

NEW = {
"1459\t9":
"Dwaff Chief:\\nWhat are you saying,\\nsage of Mabure!\\nHave you forgotten their deeds!?{bpage}\\nLeft alone, the humans\\nwill devour this planet!{mend}",
"96\t4":
"Mysterious Swordsman:\\nSwordsmanship is\\nlike a rose.{bpage}\\nA crimson ambition,\\nhidden in that beauty...\\nThat is exactly about me...{mend}",
"158\t12":
"{HARLEY%}:\\nI don't want to see\\nyou looking sad.\\nRight, {SERGE%}?{mend}",
"158\t34":
"{HARLEY%}:\\nI don't want to see\\nyou looking sad.\\nRight, {SERGE%}?{mend}",
"158\t21":
"{HARLEY%}:\\nWell then, {SERGE%},\\nlet's meet again!{mend}",
"158\t43":
"{HARLEY%}:\\nWell then, {SERGE%},\\nlet's meet again!{mend}",
"165\t29":
"{VIPER%}:\\n{RIDDEL%}!!!\\nYou... coward!{mend}",
"165\t65":
"{VIPER%}:\\n{RIDDEL%}!!!\\nYou... coward!{mend}",
"165\t80":
"{VIPER%}:\\n{RIDDEL%}!!!\\nYou... coward!{mend}",
"175\t50":
"{HARLEY%}:\\nHuh? Me?{mend}",
"175\t52":
"{HARLEY%}:\\nHmm? Me?{mend}",
"175\t68":
"{HARLEY%}:\\nHmm? Me?{mend}",
"175\t70":
"{HARLEY%}:\\nHmm? Me?{mend}",
"178\t5":
"{LUCCIA%}:\\nIf I culture it,\\nI can use it.{bpage}\\nUfufufufu...{mend}",
"214\t49":
"{HARLEY%}:\\nTry it, if you can.{wait(15)}\\nI'm not a {HARLEY%}\\nwho'd lose to a chicken!{mend}",
"236\t19":
"{HARLEY%}:\\nHeh. Lord Yamaneko\\nseems concerned about\\nthat {SERGE%}.{bpage}\\nHey, Lord Yamaneko, remember?{wait(30)}\\n{speed(48)}The place where it all began...{wait(15)}\\n{speed(72)}Led into another world.\\n“Where Even Angels Get Lost.”{mend}",
"244\t16":
"Okutogaru:\\nOhohoho. Such a feast.\\nI won't let it get away\\nthat easily!{bpage}\\nStop resisting in vain\\nand give up.\\n　　　Prepare yourselves\\n　　　Resist in vain{mend}",
"244\t18":
"{speed(255)}\\nWait...{bwait}{fset(1)}{wend(1)}",
"271\t24":
"{HARLEY%}:\\nBye...\\n{SERGE%}...{mend}",
"280\t53":
"{HARLEY%}:\\nWhat's with you,\\n{GLENN%},\\ngetting all fired up.{mend}",
"280\t56":
"{HARLEY%}:\\nOw ow ow...\\nYou really are strong, {SERGE%}.{mend}",
"280\t60":
"{HARLEY%}:\\nBye, {SERGE%}.{mend}",
"492\t38":
"{HARLEY%}:\\n{KID%},{bpage}\\nInside you is a strong urge\\nto return to nothing.{bpage}\\nRolling alone down the slope\\nof destruction\\nis your own affair.{mend}",
"1502\t7":
"{HARLEY%}:\\nAhh, come on.\\nStill fretting?{bpage}\\nYou are Lord Yamaneko.{bpage}\\nThe human called {SERGE%}\\nno longer exists\\nin this world.{bpage}\\nJust accept it...{mend}",
"1502\t10":
"{HARLEY%}:\\nHeh, you were alive.\\nYou're a stubborn one.{mend}",
"1504\t5":
"{HARLEY%}:\\nWell, see you.{mend}",
"1504\t25":
"{HARLEY%}:\\nSee you.{mend}",
"1504\t45":
"{HARLEY%}:\\nYou're so loud.{mend}",
"442\t120":
"{RADIUS%}:\\nOh, with this power,\\neven a withered old me...{bpage}\\nNo!{wait(30)}\\nThis is the same as that time,\\nthe hatred of Grandrion.{bpage}\\nGarai, I was about to\\nrepeat the same mistake.{bpage}\\nWhat...?{wait(30)} It's all right now?\\nI see. You forgive me,\\nGarai...{mend}",
}

SUBS = [
    ("not'ing", "nothing"),
    ("anyt'ing", "anything"),
    ("everyt'ing", "everything"),
    ("somet'ing", "something"),
    ("t'ings", "things"),
    ("t'ing", "thing"),
    ("t'row", "throw"),
    ("naturellement", "naturally"),
    ("mémoire", "memory"),
    ("idiote", "idiot"),
    ("longeur", "longer"),
    ("Zeir", "Their"),
    ("zeir", "their"),
    ("Masamune", "Grandrion"),
    ("Au revoir", "Bye"),
    ("Salut!", "See you!"),
    ("Moi?", "Me?"),
    ("vaiting", "waiting"),
    ("darling couple", "well-matched couple"),
]

WORD = [
    (r"\bvas\b", "was"),
    (r"\bvho\b", "who"),
    (r"\bVho\b", "Who"),
    (r"(?<![A-Za-z'])ve(?![A-Za-z'])", "we"),
    (r"(?<![A-Za-z'])Ve(?![A-Za-z'])", "We"),
]


def main():
    tmp = LANG.with_suffix(".dat.tmp")
    with zipfile.ZipFile(LANG, "r") as zin:
        jp = {}
        for line in zin.read("jp.csv").decode("utf-8-sig").splitlines():
            a = line.split("\t", 2)
            if len(a) == 3:
                jp[(a[0], a[1])] = a[2]
        en_lines = zin.read("en.csv").decode("utf-8").splitlines()
    # Masamune safety
    bad_m = 0
    for line in en_lines:
        a = line.split("\t", 2)
        if len(a) == 3 and "Masamune" in a[2]:
            j = jp.get((a[0], a[1]), "")
            if "グランドリオン" not in j and "マサムネ" not in j:
                bad_m += 1
                print("MASAMUNE unmatched", a[0], a[1], j[:60].replace("\\n", " "))
    print("masamune without grandrion", bad_m)

    nl = "\n"
    text_join = None
    hit = 0
    out = []
    seen = set()
    for line in en_lines:
        a = line.split("\t", 2)
        if len(a) == 3:
            key = a[0] + "\t" + a[1]
            if key in NEW:
                seen.add(key)
                a[2] = NEW[key]
                hit += 1
                line = "\t".join(a)
            else:
                body = a[2]
                for s, d in SUBS:
                    body = body.replace(s, d)
                for pat, d in WORD:
                    body = re.sub(pat, d, body)
                if body != a[2]:
                    a[2] = body
                    line = "\t".join(a)
        out.append(line)
    missing = set(NEW) - seen
    if missing:
        raise SystemExit("missing " + str(missing))
    print("rewrote", hit)
    body = "\n".join(out)
    if True:
        body += "\n"

    tmp = LANG.with_suffix(".dat.tmp")
    with zipfile.ZipFile(LANG, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "en.csv":
                # preserve newline style
                old = data.decode("utf-8")
                if "\r\n" in old:
                    body = body.replace("\n", "\r\n")
                data = body.encode("utf-8")
            zout.writestr(info, data)
    os.replace(tmp, LANG)

    with zipfile.ZipFile(LANG, "r") as z:
        en = z.read("en.csv").decode("utf-8")
    bare = re.sub(r"\{[^}]*\}", " ", en)
    for w in ("not'ing", "t'ing", "vas", "vho", "vaiting", "Masamune", "Au revoir",
              "Salut", "Moi", "beeba", "hi-ho", "Hi-ho", "chicken-hawk", "darling",
              "Voilà", "impératif", "confiance", "dezire", "zan ", "pleaze", "moi"):
        c = bare.count(w) if w in ("zan ", "moi") else len(re.findall(r"(?<![A-Za-z'])"+re.escape(w)+r"(?![A-Za-z'])", bare))
        if c:
            print(f"left {c:4} {w}")

if __name__ == "__main__":
    main()
