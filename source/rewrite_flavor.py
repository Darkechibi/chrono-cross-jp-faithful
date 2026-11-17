# -*- coding: utf-8 -*-
"""Rewrite lines that still invent flavor or name the wrong person."""
import os
import re
import zipfile
from pathlib import Path

LANG = Path(r"lang.dat")

# room \t index -> new English body. Control codes kept where the scene needs them.
NEW = {
"15\t0":
"Dwaff Chief:\\nYou humans who dirty\\nthis forest!{wait(15)}\\nReceive the anger of nature!{bpage}\\nAnswer my voice, Hydra.{wait(15)}\\nTeach these foolish humans\\n{speed(24)}the pain of the green...{wait(5)}\\n{speed(128)}no, of the planet!!{bwait}{fset(3)}{fwait(1)}{wend(1)}",
"15\t2":
"Dwaff Chief:\\nDo you think you are the only\\nones living on this planet!?{bpage}\\nThat no other life\\nmatters to you...{mend}",
"15\t3":
"Dwaff Chief:\\n{speed(255)}Don't be ridiculous!{wait(15)}{speed(128)}\\nYou hairless apes!{wait(10)}\\nFreaks of evolution!{mend}",
"32\t23":
"{POSHUL%}:\\nWait, hold on!{wait(20)}\\n{POSHUL%} is coming too.{bpage}\\nA field trip, all together!\\nSing, Bobonga!\\nDance, Koinga!{wait(20)}\\nField trip, field trip,\\ntariratta~.{mend}",
"148\t4":
"Wahahaha...{wait(10)}\\nBut this is as far\\nas you go!{wait(30)}\\nUraaa!!{wend(10)}",
"148\t6":
"Wahahaha...{wait(10)}\\nNo matter how many times,\\nit's the same!{wait(30)}\\nUraaa!!{wend(10)}",
"158\t11":
"{HARLEY%}:\\nHey, {SERGE%}.\\nYou should do that.{mend}",
"158\t33":
"{HARLEY%}:\\nHey, {SERGE%}.\\nYou should do that.{mend}",
"158\t45":
"Dream of me\\nevery night!\\nUfufu!{mend}",
"214\t42":
"You bump into me\\nout of nowhere.{wait(15)}\\nYou've got no manners.{mend}",
"214\t46":
"{HARLEY%}:\\nSo noisy.{wait(15)}\\nI've got no business\\nwith a chicken-head.{bpage}\\nThe one I want is\\n{SERGE%}.\\nOutsiders are noisy,\\nso be quiet.{mend}",
"214\t55":
"{HARLEY%}:\\nWell then, {SERGE%},\\nlet's meet again!{bpage}\\nDream of me\\nevery night!{wait(5)}\\nUfufu!{mend}",
"218\t9":
"Hey now, the marsh plants\\nrespond to this bell's tone.{wait(20)}\\nI don't need it anymore.\\nHere,{wait(5)} it's yours, kid!{mend}",
"230\t35":
"Dwaff Chief:\\nYou're persistent. Leave, now!\\n　　　We'll leave right away\\n　　　We're not leaving!{mend}",
"230\t37":
"???:\\nDon't come any further!{mend}",
"230\t39":
"Dwaff Chief:\\nWhat do you humans want\\nin this forest?{wait(15)}\\nThis is no place for you\\nto wander around.{bpage}\\nLeave quietly, and I may\\nlet you go.\\n　　　We'll leave quietly\\n　　　We're not leaving!{mend}",
"230\t40":
"Dwaff Chief:\\nHmph. A wise choice.{wait(15)}\\nThis is the forest we protect.\\nHumans should not come here!{mend}",
"230\t42":
"Dwaff Chief:\\nIf you know you can't win,\\nyou run. That is also wise.{wait(15)}\\nI won't chase you.\\nLeave the forest.{mend}",
"234\t0":
"Higeff:\\n{speed(32)}They're strong...{wait(2)}{mend}",
"234\t1":
"Noff:\\n{speed(48)}Y-you mean{wait(2)}\\nto kill the forest...?{wait(2)}{mend}",
"234\t2":
"Dwaff Chief:\\nNo matter how many times,\\nyou go no further!{wait(15)}\\nGive up and leave the forest.{mend}",
"234\t5":
"Noff:{speed(96)}\\nThe Hydra is this forest's\\nguardian deity.{wait(15)}\\nIf it is lost,\\nthis forest will die...{mend}",
"234\t6":
"Higeff:\\nIf you still mean to go on,\\nwe will show no mercy.\\nPrepare yourselves,\\nyou humans!{mend}",
"236\t2":
"{speed(48)}Humans... I hate them.{wait(15)}\\n{speed(32)}...That's how it is.{mend}",
"236\t6":
"You are persistent!{wait(15)}\\nI hate persistent people!{mend}",
"236\t8":
"Whoever disturbs my sleep,\\nI will not forgive them!{wait(15)}\\nBut chasing you is a pain,\\nso I'll let you go this time.{mend}",
"236\t9":
"If you understand,\\nget out of this forest!{mend}",
"236\t13":
"{HARLEY%}:\\nWe're back, in the real world.{wait(20)}\\nWell, Lord Yamaneko,\\ndo you know where this is?{bpage}\\nShall I tell you?\\n　　　No, I'm fine\\n　　　Tell me{mend}",
"238\t0":
"Pipa:\\nYou want to go to\\n“Furuki Daichi”?{wait(20)}\\nThen call Rosary here.{bpage}\\nWith the flute alone,\\neven I get attacked.\\nYou need {color(4)}{itemwork(3)}{color(0)}.{wait(15)}\\nIt's Rosary's one favorite.\\nFlute and fruit, perfect!{mend}",
"238\t1":
"Pipa:\\nWait. You don't have the fruit.\\nDon't blow that flute here!{wait(15)}\\nEven I would be attacked.{mend}",
"238\t9":
"Pipa:\\nI don't like humans.\\nBut I don't hate them either.{wait(20)}\\nI just like strong ones.{bpage}\\nWhich are you?{wait(15)}\\n　　　Pretty strong\\n　　　Completely weak{mend}",
"238\t11":
"That was pretty fun.{wait(15)}\\nThe treasure further in,\\nI'll give it to you.{mend}",
"238\t12":
"......Farewell.{mend}",
"238\t13":
"That you are strong\\nwas a complete lie.\\nThe strong never run!{mend}",
"240\t0":
"Pipa:\\nI'm sorry.{wait(15)}\\nI'll give you this,\\nso please forgive me.{bpage}\\nThis is a strange flute\\npassed down by the Pipa.{wait(15)}\\nWith this, you can\\ntame Rosary.{mend}",
"240\t1":
"Pipa:\\nA “wide, open place”\\nis best. Yes!{wait(15)}\\nWell, good luck.{mend}",
"240\t2":
"Pipa:\\nYou and I are comrades.{wait(20)}\\nIf you don't understand,\\nask me anything.{bpage}\\n　　　It's nothing\\n　　　What's Furuki Daichi?\\n　　　What's Maboroshi no Kajitsu?\\n　　　What's Rosary?{mend}",
"240\t4":
"Pipa:\\n“Furuki Daichi,” passed down\\nby us Pipa.{wait(20)}\\nIn your words,\\n“Sekai no Heso.”{bpage}\\nA lone island at the very edge\\nof El Nido, ringed by cliffs.{wait(15)}\\nA mystical place, where a\\nprimeval forest still breathes.{mend}",
"240\t5":
"Pipa:\\nI only heard it from the elder\\nlong ago. I don't really know\\nFuruki Daichi either.{wait(20)}\\nI like this forest.{mend}",
"240\t6":
"Pipa:\\nHmm...?{wait(15)}\\nYou want Maboroshi no Kajitsu?\\nThere's plenty. Don't hold back.{mend}",
"240\t8":
"Pipa:\\nReally, the flute's tone alone\\nand even we get attacked.{wait(15)}\\nSo, “Maboroshi no Kajitsu.”{bpage}\\nA seed that was on Rosary.\\nWe raised it. It isn't on\\nthis island.{wait(15)}\\nThat's why it's called phantom.\\nThe fruit is big, and so is Rosary.{mend}",
"240\t9":
"Pipa:\\nBut it's all right. One bite\\nand Rosary is satisfied.{wait(20)}\\nOne is enough for the\\ntrip there and back.{mend}",
"240\t10":
"Pipa:\\nIf you run out, just say so.\\nI have plenty of fruit.{wait(15)}\\nI'll share any time.{mend}",
"240\t11":
"Pipa:\\nYou fought it once.\\nLike you saw, a huge bug.{wait(20)}\\nIt often flies in this forest.{bpage}\\nRosary flies here from\\nFuruki Daichi.{wait(15)}\\nRide Rosary, and you can go\\nto “Furuki Daichi.”{mend}",
"240\t12":
"Pipa:\\nTo call Rosary safely,\\nyou need two things:{bpage}\\nthe Mushibue, and\\nMaboroshi no Kajitsu.{bpage}\\nA friend is at the end of\\nthe branch ahead. Blow the\\nflute there and Rosary comes.\\nThen you just ride.{mend}",
"240\t13":
"Pipa:\\nHmm... what you have\\nis a flute of the Pipa.{wait(15)}\\n{speed(80)}And it's mine{wait(1)}...{wait(1)}...{wait(1)}...{wait(1)}...{wait(1)}!!{mend}",
"240\t14":
"Pipa:\\nDogege!!{wait(20)}\\n{speed(160)}Why are you alive?{wait(15)}\\nRosary, what happened!?{mend}",
"240\t15":
"Pipa:\\n{speed(80)}Kuu~,{wait(5)} letting people like you\\nbeat us as they please is\\nthe shame of the Pipa.{wait(15)}{speed(192)}\\nThe revenge!!{mend}",
"240\t17":
"Pipa:\\nI'm sorry.{wait(15)}\\nI'll give you this,\\nso please forgive me.{bpage}\\nThis is Maboroshi no Kajitsu,\\nthe fruit of “Furuki Daichi.”{wait(15)}\\nWith this, you really can\\ntame Rosary.{mend}",
"240\t18":
"Pipa:\\nAfter that, just blow\\nthat Mushibue.{wait(15)}\\nI won't lie anymore.{bpage}\\nBlow it where my friend is,\\nat the end of the branch ahead,\\nand ride Rosary.\\nThat place is “Furuki Daichi.”{mend}",
"240\t19":
"Pipa:\\n{speed(72)}Why do you have the fruit?{wait(20)}\\n......Well, I won't worry\\nabout the small things.{mend}",
"240\t22":
"Pipa:\\nI hate persistent people.{wait(15)}\\nI'll make you regret\\nnot going home!{mend}",
"240\t26":
"Pipa:\\nThis is no place for\\nhumans to set foot.{wait(15)}\\nRemove yourselves. Now.{mend}",
"240\t27":
"Pipa:\\nIf you leave this place\\nquietly, I'll make an exception\\nand let you go.{wait(15)}\\nLeave, quickly.{mend}",
"240\t28":
"Revenge Pipa:\\n......Still just as\\npersistent.{wait(15)}\\nNow it's time for revenge!{mend}",
"240\t29":
"Pipa:\\nThis is what I can do.{wait(15)}\\nThe likes of you are\\nno match for me!{mend}",
"240\t33":
"Pipa:\\nWrong. This isn't open at all,\\nand there's no room to call Rosary!{wait(15)}\\nSomewhere wider, and open.{mend}",
"241\t0":
"Pipa:\\nHmm...?{wait(15)}\\nYou want Maboroshi no Kajitsu?\\nThere's plenty. Don't hold back.{mend}",
"241\t2":
"Pipa:\\nIf you run out, just say so.\\nI have plenty of fruit.{wait(15)}\\nI'll share any time.{mend}",
"241\t4":
"Pipa:\\nThank you for helping me\\nwhen it was dangerous.{wait(15)}\\nI was about to be done in.{bpage}\\nIt's nothing much,\\nbut please take this.{wait(15)}\\nIt grows in “Furuki Daichi.”\\nIt's called “Maboroshi no Kajitsu.”{mend}",
"241\t5":
"Pipa:\\n{speed(72)}Why do you have the fruit?{wait(20)}\\n......Well, I won't worry\\nabout the small things.{mend}",
"241\t7":
"Pipa:\\nI don't know if it suits\\nyour taste, but that fruit\\nis pretty good.{bpage}\\nIf you run out,\\nI'll share any time.{wait(20)}\\nYou helped me.\\nThis is the least I can do.{mend}",
"248\t1":
"Dwaff Chief:\\nYou humans who dirty\\nthis forest!{wait(15)}\\nReceive the anger of nature!{bpage}\\nAnswer my voice, Hydra.{wait(15)}\\nTeach these foolish humans\\n{speed(24)}the pain of the green...{wait(5)}\\n{speed(128)}no, of the planet!!{bwait}{fset(3)}{fwait(1)}{wend(1)}",
"248\t3":
"Dwaff Chief:\\nDo you think you are the only\\nones living on this planet!?{bpage}\\nThat no other life\\nmatters to you...{mend}",
"248\t4":
"Dwaff Chief:\\n{speed(255)}Don't be ridiculous!{wait(15)}{speed(128)}\\nYou hairless apes!{wait(10)}\\nFreaks of evolution!{mend}",
"248\t5":
"Higeff:\\nThis forest is enough\\nfor us.{mend}",
"248\t6":
"Higeff:\\n{speed(72)}This forest is finished too.\\nI won't forgive you,{wait(5)} humans...{wait(15)}\\nI won't forget{wait(5)} what you did!{mend}",
"248\t7":
"Noff:\\nThe friends who left the forest\\nwill be back soon. For a while,\\nthe three of us will hold on.{mend}",
"248\t8":
"Noff:\\n{speed(96)}Wh-what is this...\\nDo you understand\\nwhat you have done?{mend}",
"248\t17":
"Dwaff Chief:\\nUseless. You won't escape\\nfrom here.{wait(15)}\\nYou end in this forest.\\nGive up.{mend}",
"248\t23":
"Higeff:\\nNow that you've come this far,\\nwe can't let you go.{mend}",
"248\t24":
"Noff:\\n{speed(96)}To protect the forest...\\nanyone who has seen the Hydra\\nwill disappear here.{mend}",
"248\t25":
"Noff:\\nLike the fairy who wandered\\ninto this forest, I'll make you\\nfood for Okutogaru.{mend}",
"280\t45":
"{HARLEY%}:\\nHii, {SERGE%}.\\nIt's been a while.{mend}",
"280\t51":
"{HARLEY%}:\\nAnd, {SERGE%}.{wait(30)}\\nOne more order,\\nfrom Lord Yamaneko.{bpage}\\nI'll stop you\\nin your tracks.{mend}",
"280\t55":
"{HARLEY%}:\\nHey, {SERGE%}.{bpage}\\nI know very well\\nyou don't want to fight me.{bpage}\\nSave my face,\\nand let's fight.{mend}",
"280\t57":
"{HARLEY%}:\\nMmm, hey, {SERGE%}.\\nI'm saying this for your sake.\\nTurn back.{mend}",
"287\t0":
"Dwaff Chief:\\nHmph. Humans in this remote land,\\nand it's you. It's been a while.{bpage}\\n{speed(64)}Look at this land...{wait(30)}\\n{speed(128)}Beautiful, and fit to be\\nour clan's new home.\\nToo good for the fairies.{bpage}\\nYou humans taught us a world\\nbuilt on one species' corpse.\\nYou, and the fairies,\\nreturn to the sea here!{mend}",
"287\t10":
"Hoho! You and the fairies,\\nbecome scraps of the sea.{wait(15)}\\nFilthy humans!{mend}",
"411\t16":
"{HARLEY%}:\\n{speed(80)}If told to choose\\nthe world, or me...\\nwhich would Lord Yamaneko take?{mend}",
"438\t4":
"{HARLEY%}:\\nHey, take me along\\nsometimes, too.{mend}",
"1459\t16":
"Dwaff Chief:\\nWhat are you saying,\\nsage of Mabure!\\nHave you forgotten their deeds!?{bpage}\\nLeft alone, the humans\\nwill devour this planet!{mend}",
"1459\t15":
"Dwaff Chief:\\nFuhahaha!\\nPrepare yourselves, humans!{bpage}\\nNow, which bunch shall I\\nsacrifice first!\\nFuhahaha!{mend}",
"1461\t10":
"The Dragon God is with us.\\nHowever many humans come,\\nwe can crush them easily.{mend}",
"1502\t6":
"{HARLEY%}:\\nYeah?\\nThen I'll put my skill into it.{bpage}\\nI'll go take...{wait(30)}\\nI mean, I'll go get them\\nto share some ingredients.\\nWait here!{bpage}\\nUfufu.{mend}",
"1504\t0":
"{HARLEY%}:\\nOh, good morning,\\nLord Yamaneko!{bpage}\\nDid you dream of me?\\nUfufu.{mend}",
"1540\t5":
"{HARLEY%}:\\nYou...{wait(30)}...{wait(30)}I see...{bpage}\\nSorry, but I'm in a hurry.\\nWould you step aside?{mend}",
"1540\t6":
"{KID%}:\\nHah!\\nThe toll for this road\\nis a little steep.{bpage}\\nIf you want through,\\npay what there is to pay!{mend}",
"1543\t65":
"{HARLEY%}:\\nI've been walking nonstop,\\nand I'm tired.\\nLet's rest somewhere.{mend}",
"1544\t13":
"{HARLEY%}:\\nC'mon, if you crush an umeboshi\\nand drink it,{wait(15)}\\nit's delicious!{mend}",
}

PAIRS = [
    ("Land of Genesis", "Hajimari no Chi"),
    ("Daffy Dwarf", "Noff"),
    ("Daggy Dwarf", "Higeff"),
    ("Dwarf Chieftain", "Dwaff Chief"),
    ("Ancient Ground", "Furuki Daichi"),
    ("Ancient Fruit", "Maboroshi no Kajitsu"),
    ("ancient fruit", "Maboroshi no Kajitsu"),
    ("Wingapede", "Rosary"),
    ("Pentapus", "Okutogaru"),
    ("BobbaBeeba", "Pipa"),
    ("BubbaBeeba", "Pipa"),
    ("Dwarves", "Dwaff"),
    ("Dwarf", "Dwaff"),
]


def apply_pairs_seg(text):
    for src, dst in PAIRS:
        if src not in text:
            continue
        text = re.sub(r"\b" + re.escape(src) + r"\b", dst, text)
    return text


def apply_pairs(text):
    return "\\n".join(apply_pairs_seg(part) for part in text.split("\\n"))


def restore_plain(text):
    parts = []
    pos = 0
    for m in re.finditer(r"\{[^}]*\}", text):
        parts.append(apply_pairs(text[pos:m.start()]))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(apply_pairs(text[pos:]))
    return "".join(parts)


def main():
    tmp = LANG.with_suffix(".dat.tmp")
    hit = 0
    with zipfile.ZipFile(LANG, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "en.csv":
                text = data.decode("utf-8")
                nl = "\r\n" if "\r\n" in text else "\n"
                ends = text.endswith(("\n", "\r\n"))
                out = []
                seen = set()
                for line in text.splitlines():
                    parts = line.split("\t", 2)
                    if len(parts) == 3:
                        key = parts[0] + "\t" + parts[1]
                        if key in NEW:
                            seen.add(key)
                            parts[2] = NEW[key]
                            line = "\t".join(parts)
                            hit += 1
                        else:
                            new = restore_plain(parts[2])
                            if new != parts[2]:
                                parts[2] = new
                                line = "\t".join(parts)
                    out.append(line)
                missing = set(NEW) - seen
                if missing:
                    raise SystemExit("missing ids " + ",".join(sorted(missing)[:20]))
                body = nl.join(out)
                if ends:
                    body += nl
                data = body.encode("utf-8")
                print("rewrote", hit)
            zout.writestr(info, data)
    os.replace(tmp, LANG)

    with zipfile.ZipFile(LANG, "r") as z:
        en = z.read("en.csv").decode("utf-8")
    bare = re.sub(r"\{[^}]*\}", " ", en)
    for w in ("beeba", "Beeba", "chéri", "pleaze", "Pleaze", "honneur", "fatigué",
              "Wingapede", "Ancient Ground", "Ancient Fruit", "Daffy", "Daggy",
              "Bobba", "Genesis", "moi", "Moi", "Pentapus", "Dwarf", "merry-o",
              "Mr. Universe", "chicken-hawk"):
        c = len(re.findall(r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])", bare))
        if c:
            print(f"left {c:4}  {w}")
    # hi-ho that is not the real ハイホー line
    hi = 0
    for line in en.splitlines():
        if "Hi-ho" in line or "hi-ho" in line or "Hiiii-ho" in line:
            hi += 1
    print("hi-ho lines", hi)


if __name__ == "__main__":
    main()
