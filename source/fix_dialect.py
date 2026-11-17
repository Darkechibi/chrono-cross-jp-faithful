# -*- coding: utf-8 -*-
"""Turn Chrono Cross eye-dialect into plain English. Control codes are left alone."""
import re
import unicodedata
from pathlib import Path

ROOT = Path(r".")
TOKEN = re.compile(r"\{[^}]*\}")
NAME_TOKEN = re.compile(r"\{[A-Za-z0-9_]+%\}")

# Real English words that already contain a doubled vowel. Starky's accent
# doubles a vowel on top of these, so these exact spellings are left alone.
STARKY_OK = {
    "good", "look", "too", "food", "book", "see", "seen", "been", "meet", "feet",
    "keep", "sleep", "tree", "free", "three", "week", "feel", "seem", "need",
    "speed", "indeed", "door", "floor", "poor", "moon", "soon", "room", "cool",
    "pool", "school", "choose", "shoot", "boot", "root", "wood", "stood", "foot",
    "blood", "flood", "green", "queen", "between", "agree", "coffee", "street",
    "screen", "deep", "tooth", "smooth", "balloon", "afternoon", "moonlight",
    "looks", "looking", "booked", "feeling", "seems", "needed", "keep",
}


def case_like(src, dst):
    if src.isupper():
        return dst.upper()
    if src[:1].isupper():
        return dst[:1].upper() + dst[1:]
    return dst


def subn(pattern, repl, text, flags=0):
    """Replace with simple case copy when repl is a plain string."""
    rx = re.compile(pattern, flags)

    def _repl(m):
        if callable(repl):
            dst = repl(m)
        else:
            dst = repl
        return case_like(m.group(0), dst)

    return rx.sub(_repl, text)


def strip_german_marks(text):
    out = []
    for ch in text:
        if ch in "äöüÄÖÜ":
            folded = unicodedata.normalize("NFKD", ch)
            out.append("".join(c for c in folded if not unicodedata.combining(c)))
        else:
            out.append(ch)
    return "".join(out)


def g_drop(text):
    return re.sub(r"\b([A-Za-z]{2,}in)'", lambda m: m.group(1) + "g", text)


def fix_aint(text):
    text = re.sub(r"\b([Aa])in't no\b", lambda m: "Is no" if m.group(1).isupper() else "is no", text)
    text = re.sub(r"\b([Ii]) ain't\b", "I'm not", text)
    text = re.sub(r"\b([Yy]ou) ain't\b", lambda m: case_like(m.group(1), "you") + " aren't", text)
    text = re.sub(r"\b([Ww]e) ain't\b", lambda m: case_like(m.group(1), "we") + " aren't", text)
    text = re.sub(r"\b([Tt]hey) ain't\b", lambda m: case_like(m.group(1), "they") + " aren't", text)
    text = subn(r"\bain'?t\b", "isn't", text)
    return text


def fix_archaic(text):
    """Plain English for leftover fake-archaic and fake-foreign spellings."""
    reps = [
        (r"\bthou art\b", "you are"),
        (r"\bthou hast\b", "you have"),
        (r"\bthou didst\b", "you did"),
        (r"\bthou seekest\b", "you seek"),
        (r"\bthou sayest\b", "you say"),
        (r"\bthou canst\b", "you can"),
        (r"\bdidst\b", "did"),
        (r"\bseekest\b", "seek"),
        (r"\bsayest\b", "say"),
        (r"\bcanst\b", "can"),
        (r"\btellest\b", "tell"),
        (r"\bneedest\b", "need"),
        (r"'tis\b", "it's"),
        (r"\bon mine part\b", "on my part"),
        (r"\bne'er\b", "never"),
        (r"\bbrains art\b", "brains are"),
        (r"\bthou\b", "you"),
        (r"\bthy\b", "your"),
        (r"\bthee\b", "you"),
        (r"\bthine\b", "yours"),
        (r"\bye're\b", "you're"),
        (r"\bye\b", "you"),
        (r"\bdat\b", "that"),
        (r"\bdis\b", "this"),
        (r"\bvot\b", "what"),
        (r"\bvould\b", "would"),
        (r"\bvill\b", "will"),
    ]
    for pat, repl in reps:
        text = subn(pat, repl, text, flags=re.I)
    text = re.sub(r"\bArr+\.\.\.", "Hmm...", text)
    return text


def fix_mate(text):
    text = re.sub(r"\b[Aa]hoy, mateys!?", "Hello, everyone!", text)
    text = subn(r"\bbest mates\b", "best friends", text, flags=re.I)
    text = subn(r"\bmateys\b", "friends", text, flags=re.I)
    text = re.sub(r",\s*matey\b", "", text, flags=re.I)
    text = subn(r"\bmatey\b", "friend", text, flags=re.I)
    text = subn(r"\bmates\b", "friends", text, flags=re.I)
    text = re.sub(r",\s*mate\b", "", text, flags=re.I)
    text = re.sub(r"\bmate([.!?])", r"\1", text, flags=re.I)
    text = subn(r"\bmate\b", "friend", text, flags=re.I)
    return text


def fix_common(text):
    text = subn(r"\bwhaddaya\b", "what do you", text, flags=re.I)
    text = subn(r"\bwhatcha\b", "what are you", text, flags=re.I)
    text = subn(r"\bwhat're\b", "what are", text, flags=re.I)
    text = subn(r"\bhow 'bout\b", "how about", text, flags=re.I)
    text = subn(r"'bout\b", "about", text, flags=re.I)
    text = subn(r"\byerselves\b", "yourselves", text, flags=re.I)
    text = subn(r"\byerself\b", "yourself", text, flags=re.I)
    text = subn(r"\byer\b", "your", text, flags=re.I)
    text = subn(r"\bya\b", "you", text, flags=re.I)
    text = subn(r"\bgonna\b", "going to", text, flags=re.I)
    text = subn(r"\bwanna\b", "want to", text, flags=re.I)
    text = subn(r"\bgotta\b", "got to", text, flags=re.I)
    text = subn(r"\bdunno\b", "don't know", text, flags=re.I)
    text = subn(r"\bkinda\b", "kind of", text, flags=re.I)
    text = subn(r"\boutta\b", "out of", text, flags=re.I)
    text = subn(r"\bc'mon\b", "come on", text, flags=re.I)
    text = subn(r"'cause\b", "because", text, flags=re.I)
    text = subn(r"\bgive'em\b", "give them", text, flags=re.I)
    text = subn(r"'em\b", "them", text, flags=re.I)
    text = subn(r"\bo'\s+", "of ", text, flags=re.I)
    text = g_drop(text)
    text = fix_aint(text)
    text = fix_mate(text)
    text = subn(r"\bbugger all\b", "anything", text, flags=re.I)
    text = subn(r"\bbugger\b", "damn", text, flags=re.I)
    text = subn(r"\bblokes\b", "guys", text, flags=re.I)
    text = subn(r"\bbloke\b", "guy", text, flags=re.I)
    text = subn(r"\bsheila\b", "girl", text, flags=re.I)
    text = subn(r"\bfellas\b", "guys", text, flags=re.I)
    text = subn(r"\bfella\b", "guy", text, flags=re.I)
    text = subn(r"\barse\b", "ass", text, flags=re.I)
    text = subn(r"\bstrewth\b", "seriously", text, flags=re.I)
    text = subn(r"\bsheeze\b", "jeez", text, flags=re.I)
    text = subn(r"\bold geezer\b", "old man", text, flags=re.I)
    text = subn(r"\bgeezer\b", "man", text, flags=re.I)
    text = subn(r"\bOi\b", "Hey", text)
    text = re.sub(r",\s*eh\?", "?", text, flags=re.I)
    # Baked-in accent suffixes from the old generator: WhatCHA, justCHA, don'tCHA.
    text = re.sub(r"ain'tCHA\?", "aren't you?", text, flags=re.I)
    text = re.sub(r"ain'tCHA\s+([AaEeIiOoUu])", r"isn't an \1", text, flags=re.I)
    text = re.sub(r"ain'tCHA\b", "isn't a", text, flags=re.I)
    text = re.sub(r"\bjustCHA\s+([AaEeIiOoUu])", r"just an \1", text)
    text = text.replace("justCHA", "just a")
    text = text.replace("WhatCHA", "What are you")
    text = text.replace("whatCHA", "what are you")
    text = text.replace("don'tCHA", "don't you")
    text = text.replace("Don'tCHA", "Don't you")
    text = re.sub(r"([A-Za-z]+)CHA\b", r"\1", text)
    text = fix_aint(text)
    text = fix_archaic(text)
    text = text.replace("-om", "")
    text = text.replace("-eth", "")
    text = re.sub(r"\bMotter\b", "Mother", text)
    text = re.sub(r"\bFatter\b", "Father", text)
    text = re.sub(r"  +", " ", text)
    text = re.sub(r" +([,!?;])", r"\1", text)
    text = re.sub(r"\s+([.])", r"\1", text)
    return text


def fix_harle(text):
    reps = [
        (r"Excusez-moi", "Excuse me"),
        (r"comme ça", "like that"),
        (r"comme ca", "like that"),
        (r"mon ami", "my friend"),
        (r"derrière", "rear"),
        (r"derriere", "rear"),
        (r"Réalité", "Reality"),
        (r"Realite", "Reality"),
        (r"prophétie", "prophecy"),
        (r"prophetie", "prophecy"),
        (r"spéculation", "speculation"),
        (r"speculation", "speculation"),
        (r"histoire", "history"),
        (r"'Tiz", "It's"),
        (r"Zut!", "Damn!"),
        (r"Monsieur", "Mister"),
        (r"absolument", "absolutely"),
        (r"geezer", "old man"),
        (r"humain", "human"),
        (r"\bwit'", "with"),
        (r"t'ink", "think"),
        (r"\bit'z\b", "it's"),
        (r"\bwhat'z\b", "what's"),
        (r"zat'z", "that's"),
        (r"\bzat\b", "that"),
        (r"\bzere\b", "there"),
        (r"\bzen\b", "then"),
        (r"\bzis\b", "this"),
        (r"\bzem\b", "them"),
        (r"\bzey\b", "they"),
        (r"\bze\b", "the"),
        (r"\biz\b", "is"),
        (r"\baz\b", "as"),
        (r"\bmon\b", "my"),
        (r"\boui\b", "yes"),
        (r"Je m'appelle", "My name is"),
        (r"Ooh la la", "Oh my"),
    ]
    for pat, repl in reps:
        text = subn(pat, repl, text, flags=re.I)
    def zend(m):
        w = m.group(0)
        if w.lower() in {"quiz", "buzz", "fez", "waltz", "fizz"}:
            return w
        return w[:-1] + ("S" if w[-1].isupper() else "s")
    text = re.sub(r"\b[A-Za-z']*z\b", zend, text)
    return text


def fix_pierre(text):
    text = subn(r"Excusez-moi", "Excuse me", text, flags=re.I)
    text = subn(r"\bdeux\b", "two", text, flags=re.I)
    text = re.sub(r"Ahh la lah", "Ah well", text, flags=re.I)
    text = subn(r"\boui\b", "yes", text, flags=re.I)
    text = re.sub(r",\s*non\?", ", right?", text, flags=re.I)
    text = re.sub(r"\bnon\?", "right?", text, flags=re.I)
    text = subn(r"\bmoi\b", "me", text, flags=re.I)
    return text


def fix_zappa(text):
    text = subn(r"\bye're\b", "you're", text, flags=re.I)
    text = subn(r"\bye\b", "you", text, flags=re.I)
    text = subn(r"\bah've\b", "I've", text, flags=re.I)
    text = subn(r"\bah'm\b", "I'm", text, flags=re.I)
    text = subn(r"\bah\b", "I", text, flags=re.I)
    text = subn(r"\bdinnae\b", "don't", text, flags=re.I)
    text = subn(r"\bken\b", "know", text, flags=re.I)
    text = subn(r"\baulden\b", "olden", text, flags=re.I)
    text = subn(r"\bladdie\b", "boy", text, flags=re.I)
    text = subn(r"\baye\b", "yes", text, flags=re.I)
    text = re.sub(r"\bme arse\b", "my ass", text, flags=re.I)
    text = re.sub(r"\bno from\b", "not from", text, flags=re.I)
    text = re.sub(r"\bthis be\b", "this is", text, flags=re.I)
    return text


def fix_fargo(text):
    text = re.sub(r"\b[Aa]rgh?\b[.!]?", "Ugh.", text)
    text = subn(r"\bbloomin'\b", "", text, flags=re.I)
    text = subn(r"\baye-aye\b", "yes", text, flags=re.I)
    text = subn(r"\baye\b", "yes", text, flags=re.I)
    text = subn(r"\bcap'n\b", "captain", text, flags=re.I)
    text = re.sub(r"\bArr+\.\.\.", "Hmm...", text)
    text = re.sub(r"\bArr+\b", "Hey", text)
    text = subn(r"\bta\b", "to", text, flags=re.I)
    text = re.sub(r"  +", " ", text)
    return text


def fix_luccia(text):
    text = subn(r"\bbrotter\b", "brother", text, flags=re.I)
    text = subn(r"\bpoverful\b", "powerful", text, flags=re.I)
    text = subn(r"\bvould\b", "would", text, flags=re.I)
    text = subn(r"\bvill\b", "will", text, flags=re.I)
    text = subn(r"\bvot\b", "what", text, flags=re.I)
    text = subn(r"\bvith\b", "with", text, flags=re.I)
    text = subn(r"\bkom\b", "come", text, flags=re.I)
    text = subn(r"\bdis\b", "this", text, flags=re.I)
    text = subn(r"\bdat\b", "that", text, flags=re.I)
    return text


def fix_irenes_marks(text):
    """Used on lines that were written with umlauts."""
    text = subn(r"\bist\b", "is", text, flags=re.I)
    text = subn(r"\bdis\b", "this", text, flags=re.I)
    text = subn(r"\bdat\b", "that", text, flags=re.I)
    return text


def fix_greco(text):
    text = subn(r"\bamigo\b", "friend", text, flags=re.I)
    text = subn(r"\breturnest\b", "return", text, flags=re.I)
    text = subn(r"\bthou\b", "you", text, flags=re.I)
    text = subn(r"\bthy\b", "your", text, flags=re.I)
    text = subn(r"\bthee\b", "you", text, flags=re.I)
    text = subn(r"\bGhetz\b", "Getz", text)
    return text


def fix_sprigg(text):
    text = subn(r"\bWot's\b", "What's", text)
    text = subn(r"\bwot's\b", "what's", text)
    text = subn(r"\bWot\b", "What", text)
    text = subn(r"\bwot\b", "what", text)
    text = re.sub(r"'ave\b", "have", text, flags=re.I)
    text = re.sub(r"'ere\b", "here", text, flags=re.I)
    text = re.sub(r"\bYou be\b", "You are", text)
    text = re.sub(r"\byou be\b", "you are", text)
    return text


def fix_poshul_word(word):
    m = re.match(r"^([^A-Za-z]*)([A-Za-z']+)([^A-Za-z]*)$", word)
    if not m:
        return word
    pre, core, post = m.group(1), m.group(2), m.group(3)
    if re.fullmatch(r"[Pp][Oo]-?[Ss][Hh][Uu]", core):
        return word
    low = core.lower()
    specials = {
        "thith": "this", "ith": "is", "ithn't": "isn't", "yeth": "yes",
        "mithter": "mister", "houthe": "house", "yearth": "years",
        "rookth": "looks", "rittle": "little", "deprething": "depressing",
        "momma": "mama",
    }
    if low in specials:
        return pre + case_like(core, specials[low]) + post
    if low in {"the", "that", "than", "then", "they", "them", "their", "there", "this"}:
        return word
    # Leftover lisp: a trailing "th" that means "s".
    if low.endswith("th") and low not in {"with", "both", "bath", "path", "oath"}:
        core = core[:-2] + ("S" if core[-1].isupper() else "s")
    return pre + core + post


def fix_poshul(text):
    return re.sub(r"\S+", lambda m: fix_poshul_word(m.group(0)), text)


def fix_starky_word(word):
    m = re.match(r"^([^A-Za-z]*)([A-Za-z']+)([^A-Za-z]*)$", word)
    if not m:
        return word
    pre, core, post = m.group(1), m.group(2), m.group(3)
    if core.lower() in STARKY_OK:
        return word
    if not re.search(r"([aeiouAEIOU])\1", core):
        return word

    def collapse_once(s):
        return re.sub(r"([aeiouAEIOU])\1", lambda mm: mm.group(1), s, count=1)

    cur = core
    for _ in range(4):
        if cur.lower() in STARKY_OK or not re.search(r"([aeiouAEIOU])\1", cur):
            break
        nxt = collapse_once(cur)
        if nxt == cur:
            break
        cur = nxt
    return pre + cur + post


def fix_starky(text):
    return re.sub(r"\S+", lambda m: fix_starky_word(m.group(0)), text)


def fix_sneff(text):
    text = re.sub(r"f{2,}", lambda m: m.group(0)[0], text, flags=re.I)
    text = subn(r"\boff\b", "of", text, flags=re.I)
    return text


def fix_draggy_word(word):
    if not re.search(r"r{3,}", word, flags=re.I):
        return word
    return re.sub(r"r{2,}", "r", word, flags=re.I)


def fix_draggy(text):
    return re.sub(r"\S+", lambda m: fix_draggy_word(m.group(0)), text)


PIP_W_OK = {
    "with", "we", "will", "what", "where", "when", "who", "how", "now", "down",
    "own", "would", "was", "were", "away", "always", "between", "two", "world",
    "swim", "sweet", "saw", "know", "follow", "power", "show", "slow", "grow",
    "few", "new", "news", "view", "you", "your", "yours",
}


def fix_pip_word(word):
    m = re.match(r"^([^A-Za-z]*)([A-Za-z']+)([^A-Za-z]*)$", word)
    if not m:
        return word
    pre, core, post = m.group(1), m.group(2), m.group(3)
    low = core.lower()
    mapped = {"dis": "this", "de": "the", "dat": "that", "dem": "them"}
    if low in mapped:
        return pre + case_like(core, mapped[low]) + post
    if low in PIP_W_OK or "w" not in low:
        return word
    trial = re.sub(r"w", "r", core, flags=re.I)
    # Keep the original if the swap would hit a protected word's interior.
    return pre + trial + post


def fix_pip(text):
    return re.sub(r"\S+", lambda m: fix_pip_word(m.group(0)), text)


def fix_neofio(text):
    text = re.sub(r"ph", "f", text, flags=re.I)
    text = subn(r"\bfink\b", "think", text)
    return text


def fix_doc(text):
    text = re.sub(r"\b[Dd]udes\b", "friends", text)
    text = re.sub(r"\b[Dd]ude,\s*", "", text)
    text = re.sub(r",\s*[Dd]ude\b", "", text)
    text = re.sub(r"\b[Dd]ude\b", "", text)
    text = re.sub(r"  +", " ", text)
    return text


def speaker_of(text):
    m = re.match(r"\{([A-Z0-9_]+)%\}", text.lstrip())
    if m:
        return m.group(1)
    m = re.match(r"([A-Za-z][A-Za-z .']+):", text.lstrip())
    if m:
        return m.group(1).upper()
    return ""


def visible_len(s):
    def repl(m):
        tok = m.group(0)
        if tok.endswith("%}"):
            return "X" * 6
        return ""
    return len(TOKEN.sub(repl, s))


def wrap_segment(segment, limit):
    if "\u3000" in segment or visible_len(segment) <= limit:
        return [segment]
    # Walk, counting visible width, and split at the last space that fits.
    vis = 0
    last_space = -1
    i = 0
    while i < len(segment):
        if segment[i] == "{":
            j = segment.find("}", i)
            if j == -1:
                break
            tok = segment[i:j + 1]
            vis += 6 if tok.endswith("%}") else 0
            i = j + 1
            continue
        if segment[i] == " ":
            last_space = i
        vis += 1
        if vis > limit and last_space > 0:
            left = segment[:last_space]
            right = segment[last_space + 1:]
            return [left] + wrap_segment(right, limit)
        i += 1
    return [segment]


def reflow(old, new, limit=34):
    if old == new or "\u3000" in new:
        return new
    old_parts = old.split("\\n")
    new_parts = new.split("\\n")
    out = []
    for idx, part in enumerate(new_parts):
        old_len = visible_len(old_parts[idx]) if idx < len(old_parts) else 0
        if visible_len(part) > limit and visible_len(part) > old_len:
            out.extend(wrap_segment(part, limit))
        else:
            out.append(part)
    return "\\n".join(out)


def transform_segment(segment, who, marked):
    def fix_piece(piece):
        if who in {"HARLEY", "HARLE"}:
            piece = fix_harle(piece)
        if who == "PIERRE":
            piece = fix_pierre(piece)
        if who in {"ZAPPA", "ZIPPA"} or who.startswith("ZAPPA"):
            piece = fix_zappa(piece)
        if who == "FARGO":
            piece = fix_fargo(piece)
        if who == "LUCCIA":
            piece = fix_luccia(piece)
        if who == "GRECO":
            piece = fix_greco(piece)
        if who == "SPRIGG":
            piece = fix_sprigg(piece)
        if who == "POSHUL":
            piece = fix_poshul(piece)
        if who == "STARKY":
            piece = fix_starky(piece)
        if who == "SNEFF":
            piece = fix_sneff(piece)
        if who == "DRAGGY" or re.search(r"r{3,}", piece):
            piece = fix_draggy(piece)
        if who == "PIP":
            piece = fix_pip(piece)
        if who == "NEOFIO":
            piece = fix_neofio(piece)
        if who == "DOC":
            piece = fix_doc(piece)
        piece = fix_common(piece)
        if marked:
            piece = strip_german_marks(piece)
            piece = fix_irenes_marks(piece)
            piece = piece.replace("Motter", "Mother").replace("Fatter", "Father")
        return piece

    bits = []
    pos = 0
    for m in TOKEN.finditer(segment):
        bits.append(fix_piece(segment[pos:m.start()]))
        bits.append(m.group(0))
        pos = m.end()
    bits.append(fix_piece(segment[pos:]))
    return "".join(bits)


def transform(text):
    if text.strip() == "{ERROR}":
        return text
    original = text
    who = speaker_of(text)
    who = {"HARLEQUIN": "HARLEY", "ZIPPA": "ZAPPA"}.get(who, who)
    # Untagged lines still written in Harle's spelling. Skip the shared
    # accent-token lines, where "zen" is just the end of "Frozen".
    if (
        who == ""
        and re.search(r"\b(zat|zere|zis|zem|zey|oui|monsieur)\b", text, flags=re.I)
        and not re.search(r"\{(rwr|thd|stz|sth|umeth|rw|thf)\}", text)
    ):
        who = "HARLEY"
    marked = any(ch in text for ch in "äöüÄÖÜ")
    # "\\n" is a backslash plus the letter n. Split first so that n
    # does not glue onto the first word of the next box line.
    parts = text.split("\\n")
    text = "\\n".join(transform_segment(part, who, marked) for part in parts)
    text = reflow(original, text)
    text = re.sub(r" +\\n", "\\n", text)
    text = re.sub(r"\\n +", "\\n", text)
    return text


def transform_record(line):
    if "\t" not in line:
        return transform(line)
    a, b, c = line.split("\t", 2)
    return a + "\t" + b + "\t" + transform(c)


SAMPLES = [
    r'{KID%}:\nCall me “{KID%}.”{wait(15)}\nNice to meet ya.{mend}',
    r'{KID%}:\nHey, {SERGE%}...\nHow about you and me\nteam up for a while?{bpage}\nThat {KARSH%} fella ain\'t\ngonna just leave you alone,\nthat\'s for sure.{mend}',
    r'{KID%}:\nJust you wait, Lynx!\nToday\'s gonna be the\nday of reckonin\'!!!{bpage}\nSay yer prayers!{wait(20)}\n...Not that it\'ll\ndo ya any good!!!{mend}',
    r'{KID%}:\nYou alright, mate?\nYou\'ve been actin\'\nall weird.{bpage}\nWe dunno what\'s up\nahead, so just stay\non yer toes, eh?{mend}',
    r'{HARLEY%}:\nAt zat time, zere\nshall be enmity between\nyou and ze world.{wend(120)}',
    r'{HARLEY%}:\nRéalité iz merely\na dream zat all\nof us share.{bpage}\nZe dream itself may\ndiffer, but everyone\nstill clingz to it.',
    r'{HARLEY%}:\nExcusez-moi, geezer!{wait(20)}\nWhat kind of attitude\niz zat!?{bpage}\nI will kick your derrière\nto ze moon, if you talk\nto mon Lynx comme ça!{mend}',
    r'{PIERRE%}:\nThis is Opassa Beach, oui?{wait(20)}\nThe place where the flow\nof time splits in two, non?{mend}',
    r'{ZAPPA%}:\nYe\'re a pain in me arse.\nScram!{mend}',
    r'{LUCCIA%}:\nI vill give it my all.{wait(30)}\nIt vould be interesting to see\nvot kind of data I can gather.{mend}',
    r'{IRENES%}:\nSö dis ist the finäl\ngäte, which leads to the\ndärkness of time, nö?',
    r'{POSHUL%}:\nYeth? What ith it?{wait(20)}',
    r'{POSHUL%}:\nThe room rookth\ndifferent... | SHU',
    r'{STARKY%}:\n{STARKY%} am suppoosed to\nsaay something graateful,\ncoorrect?',
    r'{STARKY%}:\nNoo problem foor {STARKY%}.\nBlue is fiine with mee.\nDoon\'t try this at\nhoome, thoough.',
    r'{SNEFF%}:\nSo this must be the\nffinal gate to the\ndarkness off time.',
    r'{DRAGGY%}:\nI\'m gonna fight to\nprrrotect all the things\nI\'ve come to love!{mend}',
    r'{PIP%}:\nDis must be de final\ngate to de dawkness\nof time.\nI will puwsue my dweam',
    r'{NEOFIO%}:\nI phink this must\nbe the phinal gate',
    r'{KORCHA%}:\nSo, {SERGE%}.{wait(20)}\nWhatCHA gonna do now?{mend}',
    r'{MACHA%}:\nIt\'s justCHA normal beach,\nbut I like it!{mend}',
    r'{MOJO%}:\nYou are-om...\nMy long lost-om\nbrother...!!',
    r'{TURNIP%}:\nI shall fight-eth for\nthe warm sun',
    r'{FARGO%}:\nAhoy, mateys!\nMake yerselves at home.{mend}',
    r'{PARTY2%}:\n{Cap}{f}{rwr}{o}zen{-}{Cap}{f}{l}{a}me',
]


def self_test():
    print("----- samples -----")
    for s in SAMPLES:
        print("IN ", s.replace("\\n", " | "))
        print("OUT", transform(s).replace("\\n", " | "))
        print()


if __name__ == "__main__":
    self_test()
