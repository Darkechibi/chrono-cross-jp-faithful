# -*- coding: utf-8 -*-
"""Put Chrono Cross proper names back to romaji of the Japanese names."""
import os
import re
import zipfile
from pathlib import Path

LANG = Path(r"lang.dat")

# Exact Japanese name (name-table field) -> romaji. Not a translation, the reading.
KANA = {
    "アルフ": "Alf",
    "イシト": "Ishito",
    "スラッシュ": "Slash",
    "蛇骨": "Jakotsu",
    "マルチェラ": "Marcella",
    "ルチアナ": "Luciana",
    "ポシュル": "Poshuru",
    "ラズリー": "Razuri",
    "オーチャ": "Ocha",
    "ファルガ": "Farga",
    "ママチャ": "Mamacha",
    "レナ": "Rena",
    "ツクヨミ": "Tsukuyomi",
    "龍の子": "Ryunoko",
    "星の子": "Hoshinoko",
    "スプリガン": "Spriggan",
    "ラッキーダン": "Lucky Dan",
    "カブ夫": "Kabuo",
    "改良種フィオ": "Kairyoshu Fio",
    "ジルベルト": "Gilbert",
    "スカール": "Skull",
    "キノコ": "Kinoko",
    "リーア": "Ria",
    "バンクリフ": "Vancliff",
    "ギャダラン": "Gyadaran",
    "ツマル": "Tsumaru",
    "ヤマネコ": "Yamaneko",
    "ソルトン": "Solton",
    "シュガール": "Shugaru",
    "蛇骨大佐": "Colonel Jakotsu",
    "ガッシュ": "Gash",
    "蛇骨館のカギ": "Jakotsu Manor Key",
    "白龍神の祈り": "Hakuryujin no Inori",
    "黒龍神の祈り": "Kokuryujin no Inori",
    "赤龍神の祈り": "Sekiryujin no Inori",
    "青龍神の祈り": "Seiryujin no Inori",
    "黄龍神の祈り": "Ouryujin no Inori",
    "緑龍神の祈り": "Ryokuryujin no Inori",
    "龍神の神子の紋章": "Ryujin no Monsho",
    "龍騎士のこて": "Ryukishi no Kote",
    "龍騎士の誇り": "Ryukishi no Hokori",
    "龍騎士の誓い": "Ryukishi no Chikai",
    "パレポリ兵": "Parepori Soldier",
    "パレポリチーフ": "Parepori Chief",
    "アナザーサイド": "Another Side",
    "刺死炎舞": "Shishienbu",
    "リブスバイパー": "Ribs Viper",
    "ヒドラフレーム": "Hydra Flame",
    "蛇骨団旗": "Jakotsu Flag",
}

# Longer English forms first. Applied only outside {tokens}.
PAIRS = [
    ("Fort Dragonia", "Koryu no Toride"),
    ("Dragonians", "Ryuzoku"),
    ("Dragonian", "Ryuzoku"),
    ("Dragonia", "Koryu"),
    ("Pyre Shore", "Koryu no Kishi"),
    ("Mount Pyre", "Shienzan"),
    ("Sea of Eden", "Kami no Niwa"),
    ("Gaea's Navel", "Sekai no Heso"),
    ("Hermit's Hideaway", "Inja no Koya"),
    ("Divine Dragon Falls", "Ryujin no Taki"),
    ("Land of Genesis", "Hajimari no Chi"),
    ("Dragon Tear", "Ryu no Namida"),
    ("6 Dragon Gods", "Rokuryujin"),
    ("4 Devas", "Shitennou"),
    ("Four Devas", "Shitennou"),
    ("BubbaBeeba", "Pipa"),
    ("Beebas", "Pipa"),
    ("Beeba", "Pipa"),
    ("demi-humans", "ajin"),
    ("Demi-humans", "Ajin"),
    ("demi-human", "ajin"),
    ("Demi-human", "Ajin"),
    ("Acacia Dragoons", "Acacia Ryukishidan"),
    ("Dragoons", "Ryukishidan"),
    ("Dragoon", "Ryukishi"),
    ("Devas", "Shitennou"),
    ("Deva", "Shitennou"),
    ("Schala", "Sara"),
    ("Marbule", "Mabure"),
    ("Porre", "Parepori"),
    ("Harlequin", "Dokeshi"),
    ("Water Dragon Isle", "Suiryu Isle"),
    ("Earth Dragon Isle", "Doryu Isle"),
    ("Fire Dragon Isle", "Enryu Isle"),
    ("Sky Dragon Isle", "Tenryu Isle"),
    ("Black Dragon Isle", "Kokuryu Isle"),
    ("Green Dragon Isle", "Ryokuryu Isle"),
    ("Water Dragon", "Suiryu"),
    ("Earth Dragon", "Doryu"),
    ("Fire Dragon", "Enryu"),
    ("Sky Dragon", "Tenryu"),
    ("Black Dragon", "Kokuryu"),
    ("Green Dragon", "Ryokuryu"),
    ("Moon Dragon", "Getsuryu"),
    ("Cape Howl", "Cape Kazenaki"),
    ("Viper Manor", "Jakotsu Manor"),
    ("General {VIPER%}", "Colonel {VIPER%}"),
    ("General Viper", "Colonel Jakotsu"),
    ("Gen. Viper", "Colonel Jakotsu"),
    ("Viper's", "Jakotsu's"),
    ("Belthasar", "Gash"),
    ("Kairyoshu Fio", "Kairyoshu Fio"),
    ("NeoFio", "Kairyoshu Fio"),
    ("Neofio", "Kairyoshu Fio"),
    ("Shaker Brothers", "Solton and Shugaru"),
    ("Peppor", "Shugaru"),
    ("Solt", "Solton"),
    ("Draggy", "Ryunoko"),
    ("Starky", "Hoshinoko"),
    ("Funguy", "Kinoko"),
    ("Grobyc", "Gyadaran"),
    ("Lucky Dan", "Lucky Dan"),
    ("Mojo", "Lucky Dan"),
    ("Turnip", "Kabuo"),
    ("Sprigg", "Spriggan"),
    ("Skelly", "Skull"),
    ("Guile", "Alf"),
    ("Norris", "Ishito"),
    ("Nikki", "Slash"),
    ("Harle", "Tsukuyomi"),
    ("Greco", "Gilbert"),
    ("Viper", "Jakotsu"),
    ("Lynx", "Yamaneko"),
    ("Marcy", "Marcella"),
    ("Luccia", "Luciana"),
    ("Fargo", "Farga"),
    ("Macha", "Mamacha"),
    ("Leena", "Rena"),
    ("Orcha", "Ocha"),
    ("Poshul", "Poshuru"),
    ("Razzly", "Razuri"),
    ("Orlha", "Oruha"),
    ("Van", "Vancliff"),
    ("Pip", "Tsumaru"),
    ("General", "Colonel"),
    ("Jakotsu Churros", "Jakotsu Manju"),
    ("Jakotsu Churro", "Jakotsu Manju"),
    ("Viper Churros", "Jakotsu Manju"),
    ("Viper Churro", "Jakotsu Manju"),
    ("Churros", "Manju"),
    ("Churro", "Manju"),
]

# Whole lines whose English names the wrong person or invents a meaning.
FIXES = [
    ("Harlequin:\\nSe taire...\\nPleaze, shut up...{mend}",
     "Dokeshi:\\nYou're so loud...{mend}"),
    ("Harlequin:\\nHmmm...\\nYou are {SERGE%}?{mend}",
     "Dokeshi:\\nHeh, so you're\\n{SERGE%}.{mend}"),
    ("Harlequin:\\nYou are even more\\nsexy zan I t'ought!\\nOh myh!{mend}",
     "Dokeshi:\\nJust as I thought.\\nI like you, Serge!{mend}"),
    ("Harlequin:\\nYou are even more\\nsexzy zan I t'ought!\\nOh myh!{mend}",
     "Dokeshi:\\nJust as I thought.\\nI like you, Serge!{mend}"),
    ("Harlequin:\\nAnd this vulgaire one\\nmust be {KID%}...\\nYou disgust moi!{mend}",
     "Dokeshi:\\nHmm...\\nSo the rough one\\nis {KID%}.{mend}"),
    ("Harlequin:\\nMy name is {HARLEY%}.{bpage}\\nI am the right-hand\\nharlequin to Mister Yamaneko.{mend}",
     "Dokeshi:\\nI'm {HARLEY%},\\nthe dokeshi.{bpage}\\nAnd Yamaneko's\\nright hand, too.{mend}"),
    ("{LUCCIA%}:\\nPeppor, ve have some\\ncustomers vaiting.{mend}",
     "{LUCCIA%}:\\nHey, newcomer.\\nShugaru, I'm counting on you.{mend}"),
    ("{SPRIGG%}:\\nVery interesting...{wait(20)}\\nWhat are you going to do now,\\nLynx?{bpage}\\n'Ow about we go explain\\nyour situation to your mother?{wait(20)}\\nWe may be able to find\\nsomething out.{mend}",
     "{SPRIGG%}:\\nWell, this has gotten\\ninteresting.{wait(20)}\\nWhat will you do now,\\nYamaneko?{bpage}\\nHow about telling your family\\nwhat happened?{wait(20)}\\nWe might learn\\nsomething new.{mend}"),
    ("Shugaru:\\nW-We win!\\nSolt, our names are cleared?{mend}",
     "Shugaru:\\nW-We won!\\nOur honor is restored!{mend}"),
    ("We're going to shake it!{mend}",
     "I will do my best!{mend}"),
    ("Your Home World or\\nAnother World.",
     "which of the two worlds."),
]

TOKEN = re.compile(r"\{[^}]*\}")

SHAKER = [
    ("how about\\na handshake", "our names are cleared"),
    ("how about a handshake", "our names are cleared"),
    ("spice, I mean, spite", "spite"),
    ("awfully awful", "terrible"),
    ("carefully careful", "very careful"),
    ("awfully soon", "so soon"),
    ("justly\\nlike", "much\\nlike"),
    ("justly like", "much like"),
    ("shake it on out of here", "get out of here"),
    ("shake it on out", "head out"),
    ("shake on out of here", "get out of here"),
    ("shake it out of here", "get out of here"),
    ("shake it out from there", "get out from there"),
    ("shake it on past", "get past"),
    ("shake it on back", "go back"),
    ("shake it to you", "show you"),
    ("shake it to them", "show them"),
    ("Let's shake it", "Let's go"),
    ("let's shake it", "let's go"),
    ("let's shake | it", "let's show | it"),
    ("Come on, shake it", "Come on"),
    ("shake it and", "go and"),
    ("Shake it and", "Go and"),
    ("shake an attack", "start an attack"),
    ("shake their thanks", "give their thanks"),
    ("shake your order", "take your order"),
    ("shake another game", "play another game"),
    ("another quick shakedown", "another quick beating"),
    ("shake our days of glory", "talk about our days of glory"),
    ("Don't shake ignorance", "Don't play dumb"),
    ("shake it", "do it"),
    ("Shake it", "Come on"),
    ("SHAKE!", "SHOOT!"),
]


def apply_pairs_seg(text):
    for src, dst in PAIRS:
        if src == dst or src not in text:
            continue
        text = re.sub(r"\b" + re.escape(src) + r"\b", dst, text)
        upper = src.upper()
        if upper != src and upper in text:
            text = re.sub(r"\b" + re.escape(upper) + r"\b", dst.upper(), text)
    text = re.sub(r"\bMah\b", "My", text)
    text = re.sub(r"\bmah\b", "my", text)
    text = re.sub(r"\btae\b", "to", text)
    text = text.replace("'Ow", "How")
    return text


def apply_pairs(text):
    # \\n is a two-character control code. The n would glue onto the next word
    # and hide it from a word-boundary match, so split first.
    return "\\n".join(apply_pairs_seg(part) for part in text.split("\\n"))


def restore_plain(text):
    for src, dst in FIXES:
        if src in text:
            text = text.replace(src, dst)
    if any(k in text for k in ("Peppor", "Solt", "Shugaru", "Solton", "shake it")):
        for src, dst in SHAKER:
            text = text.replace(src, dst)
    parts = []
    pos = 0
    for m in TOKEN.finditer(text):
        parts.append(apply_pairs(text[pos:m.start()]))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(apply_pairs(text[pos:]))
    return "".join(parts)


def restore_record(line):
    parts = line.split("\t", 2)
    if len(parts) != 3 or not parts[0].isdigit():
        return restore_plain(line)
    a, b, c = parts
    if c.strip() == "{ERROR}":
        return line
    new = restore_plain(c)
    if line.count("{") != (a + "\t" + b + "\t" + new).count("{"):
        raise SystemExit("brace change: " + line[:100])
    return a + "\t" + b + "\t" + new


def restore_csv(data: bytes) -> bytes:
    text = data.decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in text else "\n"
    ends = text.endswith(("\n", "\r\n"))
    out = [restore_record(line) for line in text.splitlines()]
    body = nl.join(out)
    if ends:
        body += nl
    changed = sum(1 for a, b in zip(text.splitlines(), out) if a != b)
    print("  csv lines changed", changed)
    return body.encode("utf-8")


def restore_sysmes(data: bytes) -> bytes:
    text = data.decode("utf-16")
    nl = "\r\n" if "\r\n" in text else "\n"
    ends = text.endswith(("\n", "\r\n"))
    changed = 0
    out = []
    for line in text.splitlines():
        parts = line.split("\t")
        if len(parts) >= 4:
            raw = parts[1]
            prefix = "β" if raw.startswith("β") else ""
            key = raw[1:] if prefix else raw
            en_prefix = "β" if parts[3].startswith("β") else ""
            en = parts[3][1:] if en_prefix else parts[3]
            if key in KANA:
                en = KANA[key]
                changed += 1
            else:
                new_en = apply_pairs(en)
                if new_en != en:
                    changed += 1
                    en = new_en
            parts[3] = en_prefix + en
            line = "\t".join(parts)
        out.append(line)
    print("  sysmes english fields changed", changed)
    body = nl.join(out)
    if ends:
        body += nl
    # keep the original BOM style
    return body.encode("utf-16")[2:]  # encode adds BOM; caller writes BOM


def main():
    tmp = LANG.with_suffix(".dat.tmp")
    targets = {"en.csv", "btel_en.csv", "shopmenu.txt", "keyitem.txt", "cmnmes.txt"}
    with zipfile.ZipFile(LANG, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename in targets and data:
                print(info.filename)
                if data.startswith((b"\xff\xfe", b"\xfe\xff")):
                    text = data.decode("utf-16")
                    nl = "\r\n" if "\r\n" in text else "\n"
                    ends = text.endswith(("\n", "\r\n"))
                    out = [restore_record(line) for line in text.splitlines()]
                    body = nl.join(out)
                    if ends:
                        body += nl
                    changed = sum(1 for a, b in zip(text.splitlines(), out) if a != b)
                    print("  utf-16 lines changed", changed)
                    data = body.encode("utf-16")
                else:
                    data = restore_csv(data)
            elif info.filename == "sysmes.txt":
                print("sysmes.txt")
                body = restore_sysmes(data)
                data = b"\xff\xfe" + body
            zout.writestr(info, data)
    os.replace(tmp, LANG)

    with zipfile.ZipFile(LANG, "r") as z:
        en = z.read("en.csv").decode("utf-8")
        sysmes = z.read("sysmes.txt").decode("utf-16")
    checks = {
        "Yamaneko": en.count("Yamaneko"),
        "Lynx left": len(re.findall(r"\bLynx\b", en)),
        "Tsukuyomi": en.count("Tsukuyomi"),
        "Solton": en.count("Solton"),
        "Shugaru": en.count("Shugaru"),
        "Peppor left": en.count("Peppor"),
        "Gash": en.count("Gash"),
        "Belthasar left": en.count("Belthasar"),
        "Cape Kazenaki": en.count("Cape Kazenaki"),
        "Colonel": en.count("Colonel"),
        "shake it left": en.count("shake it"),
        "Lynx substr": en.count("Lynx"),
        "Viper substr": en.count("Viper"),
        "Belthasar left": en.count("Belthasar"),
        "Dragonia left": en.count("Dragonia"),
        "Marbule left": en.count("Marbule"),
        "Porre left": en.count("Porre"),
        "Schala left": en.count("Schala"),
        "Eden left": en.count("Eden"),
        "Gaea left": en.count("Gaea"),
        "Pyre left": en.count("Pyre"),
        "Churro left": en.count("Churro"),
        "Dragoon left": en.count("Dragoon"),
        "Harlequin left": en.count("Harlequin"),
        "Mabure": en.count("Mabure"),
        "Parepori": en.count("Parepori"),
        "Sara": en.count("Sara"),
        "Koryu": en.count("Koryu"),
        "Shienzan": en.count("Shienzan"),
        "sys Harle": sysmes.count("\tHarle\t"),
        "sys Tsukuyomi": sysmes.count("Tsukuyomi"),
        "sys Alf": sysmes.count("\tAlf\t"),
    }
    for k, v in checks.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
