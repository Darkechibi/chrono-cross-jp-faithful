# -*- coding: utf-8 -*-
import os, re, zipfile
from pathlib import Path
LANG = Path(r"lang.dat")

NEW = {
"43\t15":
"You know how Kiki's\\ngrowing up so quickly?{wait(20)}\\nSometimes I'm startled by how\\nmuch she looks like my wife.{bpage}\\nCome to think of it, my wife\\ntook after her own mother\\nthat way, from way back...{bpage}\\nThat's how it is passed on,\\nparent to child,\\nchild to grandchild.{mend}",
"45\t23":
"Good morning,\\n{SERGE%}.{bpage}\\nWhat, have you been\\nasleep until now!?{wait(20)}\\nWell, they do say sleeping\\nchildren grow well...{bpage}\\n{LEENA%} is over there,\\non the pier.{wait(20)}\\nLooks like her daughter\\nasked her to do something.{mend}",
"47\t2":
"You know the shore southwest\\nof the village, the one everyone\\ncalls Tokage Rock?{bpage}\\nSometimes the parent of a\\nKodomo giant lizard comes out.\\nIt's dangerous.{wait(20)}\\nI've told Kiki many times\\nnot to go play there...{bpage}\\nShe doesn't listen to\\nher parent at all.{mend}",
"108\t9":
"{VAN%}:\\nEh...\\nWork again...?{mend}",
"188\t8":
"{LUCCIA%}:\\nHe is an enhanced human,\\nmade by my brother,\\nwho was in Parepori.{bpage}\\nThey said he died in the lab\\nexplosion 3 years ago,\\nbut he was alive.{mend}",
"190\t5":
"{LUCCIA%}:\\nWhy... you...\\nmy brother...{mend}",
"214\t43":
"{HARLEY%}:\\nHahan, yep.\\nThis one's down.{mend}",
"262\t41":
"{LUCCIA%}:\\n{color(GRAY)}Sigh...{color(0)}\\nThis is why dealing with\\nfools is so tiring.{bpage}\\nListen. We are the ones\\nchasing them, and you\\nare getting in the way.\\nDo you understand?{mend}",
"262\t78":
"{LUCCIA%}:\\nLectured by a pirate...\\nwhat am I to do?{mend}",
"411\t20":
"{HARLEY%}:\\nFufu, that's just like\\nLord Yamaneko.{mend}",
"503\t4":
"There's something written\\non the memo on the floor...{bpage}\\nCircle is friends with “O.”\\nSquare got to know “D.”\\nTriangle is close with “A.”\\nCross, “X,” is all over.{mend}",
}

VH = [
    ("vhereabouts", "whereabouts"),
    ("villing", "willing"),
    ("vorking", "working"),
    ("t'ought", "thought"),
    ("vhom", "whom"),
    ("vhile", "while"),
    ("Vho", "Who"),
    ("vho", "who"),
    ("Vhy", "Why"),
    ("vhy", "why"),
    ("vhen", "when"),
    ("dragoons", "knights"),
]


def fix_seg(seg):
    for src, dst in VH:
        if src not in seg:
            continue
        seg = re.sub(r"\b" + re.escape(src) + r"\b", dst, seg)
    return seg


def fix_body(body):
    return "\\n".join(fix_seg(s) for s in body.split("\\n"))


def main():
    tmp = LANG.with_suffix(".dat.tmp")
    with zipfile.ZipFile(LANG, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename != "en.csv":
                zout.writestr(info, data)
                continue
            text = data.decode("utf-8")
            nl = "\r\n" if "\r\n" in text else "\n"
            ends = text.endswith(("\n", "\r\n"))
            seen = set()
            out = []
            for line in text.splitlines():
                a = line.split("\t", 2)
                if len(a) == 3:
                    key = a[0] + "\t" + a[1]
                    if key in NEW:
                        a[2] = NEW[key]
                        seen.add(key)
                    else:
                        a[2] = fix_body(a[2])
                    line = "\t".join(a)
                out.append(line)
            missing = set(NEW) - seen
            if missing:
                raise SystemExit("missing " + str(missing))
            body = nl.join(out)
            if ends:
                body += nl
            zout.writestr(info, body.encode("utf-8"))
    os.replace(tmp, LANG)
    with zipfile.ZipFile(LANG, "r") as z:
        en = z.read("en.csv").decode("utf-8")
    for w in ("vho", "vhy", "vhen", "t'ought", "Super Mensch", "early bird",
              "Komodo", "beeba", "Masamune", "dragoons", "Taban", "my father once"):
        print(f"{en.count(w):4} {w}")

if __name__ == "__main__":
    main()
