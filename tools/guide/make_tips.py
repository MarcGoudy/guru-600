"""Les infobulles de l'éditeur : chaque réglage décrit dans les tableaux du guide (CTL, CTL3), avec sa page (le chapitre),
son cadre (le dernier intertitre H3) et sa description dans les sept langues (anglais + tr_xx.json du guide).
Écrit editeur/guru-tips.js (TIPS[page] = [{n: le libellé, s: le cadre, d: {en, fr, de, es, it, zh, ja}}]).
Lancer après make_guide.py (mêmes chapitres, mêmes traductions)."""
import os, re, json, glob
import ui_i18n
H = os.path.dirname(os.path.abspath(__file__))
N = os.path.join(os.path.dirname(H), "notice")
_src = open(os.path.join(N, "make_notice.py")).read()
_head = _src.split("S = []   # the sections")[0].replace("H = os.path.dirname(os.path.abspath(__file__))", f"H = {H!r}")
exec(_head)
_m = re.search(r"\nCHAPS = \[\]\n.*?(?=\nimport glob)", _src, re.S)
exec(_m.group(0))
EDC = {k: "" for k in ("sound", "seq", "song", "arp", "fx", "mod", "tracks", "projects", "samples", "backup", "settings")}
_rows, _sec, TIPS = [], [""], {}
_H3 = H3


def H3(en, fr, color=None):                            # (the box the next tables describe)
    _sec[0] = re.sub(r"<[^>]+>", "", en)
    return _H3(en, fr, color)


def SHOT(name, en, fr, w=680):
    return ""


def CTL(rows, head=None):
    _rows.extend((n, a, b, _sec[0]) for n, a, b in rows)
    return ""


def CTL3(rows):
    _rows.extend((n, a, b, _sec[0]) for n, a, b, c, d in rows)
    return ""


_table = table


def table(head, rows, cls=""):                         # the other control tables (TRACKS, SETTINGS, INSERT's TYPE...):
    for r in rows:                                     # a row's name, then its first (en, fr) cell: the description
        name = re.sub(r"<[^>]+>", "", r[0] if isinstance(r[0], str) else r[0][0])
        name = re.sub(r"\s*\((?:fader)\)", "", name).replace("◀", "").replace("▶", "").strip()
        desc = next((c for c in r[1:] if isinstance(c, tuple)), None)
        if not desc or not re.search(r"[A-Z]{2}", name) or re.search(r"[a-z]", re.sub(r"\(.*?\)", "", name)):
            continue
        for nm in [x.strip() for x in name.split(",")]:
            _rows.append((nm, desc[0], desc[1], _sec[0]))
    return _table(head, rows, cls)


_CH = CH


def CH(key, en, fr, body):                             # the rows read while the body was built: this chapter's
    TIPS[key] = TIPS.get(key, []) + [(n, a, b, s) for n, a, b, s in _rows]
    _rows.clear(); _sec[0] = ""
    return _CH(key, en, fr, body)


S = []
for _f in sorted(glob.glob(os.path.join(H, "chap", "*.py"))):
    exec(open(_f).read())
CHNUM = {k: i + 1 for i, (k, *_r) in enumerate(CHAPS)}
CHW = {"en": "chapter", "fr": "chapitre", "de": "Kapitel", "es": "capítulo", "it": "capitolo", "zh": "第", "ja": "第"}


def clean(t, l):
    t = re.sub(r"\{ch:(\w+)\}", lambda m: str(CHNUM.get(m.group(1), "")), t)
    t = re.sub(r"<[^>]+>", "", t).replace("&nbsp;", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", t).strip()


out, missing = {}, 0
for page, rows in TIPS.items():
    lst = []
    for n, en, fr, sec in rows:
        d = {"en": clean(en, "en"), "fr": clean(fr, "fr")}
        for l in LANGS[2:]:
            t = TR[l].get(en)
            if t is None:
                missing += 1
            d[l] = clean(t, l) if t else d["en"]
        for l in LANGS[1:]:                                # (the editor's own words as it shows them in that language)
            d[l] = clean(ui_i18n.ui(d[l], l, page), l)
        lst.append({"n": re.sub(r"<[^>]+>", "", n), "s": sec, "d": d})
    out[page] = lst
open(os.path.join(os.path.dirname(H), "editeur", "guru-tips.js"), "w").write(
    "// Guru-600 editor: the tooltips' descriptions, from the guide's tables (written by guide/make_tips.py: do not edit)\n"
    f"const TIPS = {json.dumps(out, ensure_ascii=False)};\n")
print({k: len(v) for k, v in out.items()}, "traductions manquantes :", missing)
