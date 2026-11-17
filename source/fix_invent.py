# -*- coding: utf-8 -*-
"""Fix remaining invent leftovers without dumping the whole script."""
import os, re, zipfile
from pathlib import Path

LANG = Path(r"lang.dat")

# Exact line replacements (room\tindex -> new body). Only clear meaning fixes.
NEW = {
"98\t56":
"{KARSH%}:\\nBut what surprised me\\nwas {GLENN%}.{bpage}\\nWhen did he get\\nthat good?{bpage}\\nWe can't let our guard down.\\nRight, {GLENN%}?{mend}",
"78\t53":
"{GLENN%}:\\nIf you mean to go to\\nKoryu no Toride, I'll tell you\\nsomething useful.{bpage}\\nGo north by boat, then east.\\nThere's a small island.\\nA retired knight lives there.{bpage}\\nTalk to that old knight once.{bpage}\\nThere are many frightening\\nrumors about that fort.{mend}",
"76\t28":
"I love boats!{wait(10)}\\nI can watch them all day\\nand never get bored.{bpage}\\nBut I get seasick bad,\\nso I can't be a sailor...{bpage}\\nSo I decided to be a boat builder\\nand make a fast, cool boat!{bpage}\\nFor that: first research,{wait(10)}\\nsecond research,{wait(10)}\\nI study all kinds of boats.{wait(10)}\\nPretty great, right?{bpage}\\nOf the boats I've seen,\\n{KORCHA%}'s is the coolest\\nand fastest.{wait(10)}\\nI want to build one like that...{mend}",
"75\t7":
"I love boats!{wait(10)}\\nBut I get seasick bad,\\nso I can't be a sailor...{bpage}\\nSo I decided to be a boat builder\\nand make a fast, cool boat!{bpage}\\nFor that: first research,{wait(10)}\\nsecond research,{wait(10)}\\nI study boats here.{wait(10)}\\nPretty great, right?{bpage}\\nOf the boats I've seen,\\nthe one at the harbor is\\nthe coolest and fastest.{wait(10)}\\nI want to build one like that...{mend}",
"534\t31":
"{LEENA%}:\\nSo this is goodbye.{wait(30)}\\nYou're going back to\\nyour world...{bpage}\\nThank you...{bpage}\\nfor giving me new memories\\nwith the {SERGE%} who\\ndied ten years ago...{wait(30)}{bpage}\\nGoodbye,\\nthe other {SERGE%}.{wait(30)}\\nGet along with the me\\nin your world...{bpage}\\nGoodbye...{mend}",
"534\t30":
"{GLENN%}:\\nAlright! From tomorrow I'll\\nwork hard and become a knight\\nwho surpasses my brother!{bpage}\\nYou work hard too,\\n{SERGE%}!{wait(30)}\\nI'll look forward to\\nthe day we meet again.{mend}",
"32\t6":
"Come on, everyone,\\nwake up!{wait(20)}\\nThe early bird gets the worm!\\nA morning of bright hope!{mend}",
"244\t43":
"{RAZZLY%}\\n{speed(96)}Another world...\\nYou came to this forest to\\nsave a friend from there?{mend}",
"226\t35":
"{KID%}:\\nYou heard the story from the\\nvillage miko, right?{wait(20)}\\n{speed(72)}The story about\\n“{wait(0)}H{wait(0)}a{wait(0)}j{wait(0)}i{wait(0)}m{wait(0)}a{wait(0)}r{wait(0)}i{wait(0)} {wait(0)}n{wait(0)}o{wait(0)} {wait(0)}C{wait(0)}h{wait(0)}i{wait(0)} {wait(0)}.”{mend}",
"211\t27":
"{DOC%}:\\n{speed(72)}Another world?{wait(30)}\\nYou're saying such a thing\\nexists...{mend}",
"155\t13":
"{ZOAH%}:\\nWIELDER OF THE WHITE SWORD EINLANZER.{bpage}\\nHE HAD COLONEL {CAP}{VIPER%}'S DEEP TRUST.{bpage}\\nHE WAS ENGAGED TO THE COLONEL'S DAUGHTER, MISS {CAP}{RIDDEL%}, AND WAS SAID TO BE THE NEXT HEAD OF THE HOUSE.{bpage}\\nTHREE YEARS AGO, ON THE ISLE OF THE DAMNED ON A HUNT FOR THE DEAD, HE DIED AN HONORABLE DEATH.{mend}",
"149\t10":
"Dario:\\n{RIDDEL%}, you said you\\ncame from another world.{bpage}\\nThen where are you and\\n{KARSH%} in this world?{mend}",
"88\t9":
"{ZOAH%}:\\nTAKING ADVANTAGE OF THAT,\\nTHE PAREPORI ARMY WAS MOVING\\nTO TAKE TERMINA...{mend}",
"88\t14":
"{ZOAH%}:\\nFROM THE COLONEL'S SLEEP-TALK\\nWE FIGURED OUT ROUGHLY\\nWHAT HAPPENED THERE.{bpage}\\nTHE KID RAMPAGING AROUND HERE\\nIS YAMANEKO, RIGHT?{mend}",
"88\t1":
"{ZOAH%}:\\nWATCH OUT.{bpage}\\nTHERE'S NO TELLING WHAT\\nTHE PAREPORI ARMY WILL SEND.{mend}",
"430\t62":
"{RIDDEL%}:\\nAh, Dario.\\nYou don't know me?{bpage}\\nI may be a {RIDDEL%}\\nyou don't know,{bpage}\\nbut I... I have always\\nonly you...{bpage}\\nAnd yet...\\nhave you forgotten?{mend}",
"430\t49":
"{KARSH%}:\\nDario!\\nThat...\\nI see. Different worlds.{mend}",
"430\t39":
"{RIDDEL%}:\\nYou are...{wait(40)}\\nDario!?{bpage}\\nYes, of course. Different worlds.\\nAh, but I'm glad.{bpage}\\nIn this world,\\nyou were alive.{mend}",
"430\t36":
"{RIDDEL%}:\\nAh, Dario.\\nYou don't know me?{bpage}\\nI may be a {RIDDEL%}\\nyou don't know,{bpage}\\nbut I... I have always\\nonly you...{bpage}\\nAnd yet...\\nhave you forgotten?{mend}",
"430\t34":
"{RIDDEL%}:\\nYou are...{wait(40)}\\nDario!?{bpage}\\nYes, of course. Different worlds.\\nAh, but I'm glad.{bpage}\\nIn this world,\\nyou were alive.{mend}",
"430\t19":
"{RIDDEL%}:\\nAh, Dario.\\nYou don't know me?{bpage}\\nI may be a {RIDDEL%}\\nyou don't know,{bpage}\\nbut I... I have always\\nonly you...{bpage}\\nAnd yet...\\nhave you forgotten?{mend}",
"214\t65":
"{KORCHA%}:\\nHey, what are you going to do?{wait(15)}\\n　　　...I don't know\\n　　　Look for a way to save her{mend}",
"206\t2":
"Sorry to be abrupt, but have you\\never seen a “shining material”?{wait(15)}\\n　　　...Shining material?\\n　　　I've seen one{mend}",
"193\t75":
"Forever and ever, your friend,\\n　　　　Lucca Ashtear{mend}",
"47\t18":
"For tomorrow, part 3~\\n　　Some like to chase,\\n　　and run round and round!{mend}",
"47\t17":
"For tomorrow, part 2~\\n　　Use the terrain,\\n　　and strike by surprise!{mend}",
"387\t49":
"　　The days when winning　　\\n　　meant everything...　　{mend}",
"245\t14":
"{speed(255)}...This forest... is dead...\\n\\n　　The Hydra too... ...perished\\nThose to hate...　　　humans\\n\\nHear the planet's voice... its pain...\\n\\n　　　　Humans...{mend}",
"477\t2":
"Chronopolis Military Research Center{bpage}\\n“　Everlasting peace\\n　　　for the world's children　”\\n　　　　　　　2400{mend}",
}

# Global invent scraps outside NEW (only outside tokens)
GLOBAL = [
    (r"\bAin't I right\b", "Right"),
    (r"\bAin't I smart\?\b", "Pretty great, right?"),
    (r"\bain't\b", "aren't"),
    (r"\bAin't\b", "Aren't"),
    (r"\bTHE PORRE\b", "THE PAREPORI"),
    (r"\bPorre military\b", "Parepori military"),
    (r"\bPORRE MILITARY\b", "PAREPORI ARMY"),
    (r"\ba retired dragoon\b", "a retired knight"),
    (r"\bas a great dragoon\b", "as a great knight"),
    (r"\bdragoon\b", "knight"),
    (r"\bDragoon\b", "Knight"),
]

TOKEN = re.compile(r"\{[^}]*\}")


def global_fix(text):
    parts, pos = [], 0
    for m in TOKEN.finditer(text):
        seg = text[pos:m.start()]
        for pat, rep in GLOBAL:
            seg = re.sub(pat, rep, seg)
        parts.append(seg)
        parts.append(m.group(0))
        pos = m.end()
    seg = text[pos:]
    for pat, rep in GLOBAL:
        seg = re.sub(pat, rep, seg)
    parts.append(seg)
    return "".join(parts)


def main():
    tmp = LANG.with_suffix(".dat.tmp")
    hit = ghit = 0
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
                            new = global_fix(a[2])
                            if new != a[2]:
                                ghit += 1
                                a[2] = new
                        line = "\t".join(a)
                    out.append(line)
                body = nl.join(out) + (nl if ends else "")
                data = body.encode("utf-8")
            zout.writestr(info, data)
    os.replace(tmp, LANG)
    print("exact", hit, "global", ghit)
    with zipfile.ZipFile(LANG, "r") as z:
        en = z.read("en.csv").decode("utf-8")
    for w in ("ain't", "Ain't", "PORRE", "dragoon", "Dragoon", "Land of Genesis", "Genesis"):
        print(w, en.count(w))


if __name__ == "__main__":
    main()
