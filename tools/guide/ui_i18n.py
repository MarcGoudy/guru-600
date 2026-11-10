"""Les mots propres à l'éditeur dans la langue de chaque texte du guide (et des infobulles) : ceux que l'éditeur affiche
traduits (editeur/guru-i18n.js, I18N_WORDS, lu par node). Les mots du FM-1 restent en anglais, comme dans l'éditeur.
Règles : un nom de plusieurs mots, un nom d'onglet ou de réglage de l'éditeur est remplacé partout (en capitales, mot
entier) ; un nom d'un seul mot (LOAD, ERASE, SAVE...) seulement en gras (<b>), où le guide cite un bouton ; un nom limité à
une page (@song ADD...) seulement dans le chapitre de cette page."""
import json, os, re, subprocess
_ED = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "editeur", "guru-i18n.js")
_JS = ("const s=require('fs').readFileSync(process.argv[1],'utf8');"
       "const m=/const I18N_WORDS = (\\[[\\s\\S]*?\\n\\]);/.exec(s);console.log(JSON.stringify(eval(m[1])));")
_W = json.loads(subprocess.run(["node", "-e", _JS, _ED], capture_output=True, text=True, check=True).stdout)
_JS2 = ("const s=require('fs').readFileSync(process.argv[1],'utf8');"
        "const m=/const I18N_SEC = (\\{[\\s\\S]*?\\n\\});/.exec(s);console.log(JSON.stringify(eval('('+m[1]+')')));")
SEC = json.loads(subprocess.run(["node", "-e", _JS2, _ED], capture_output=True, text=True, check=True).stdout)   # the boxes' titles


def sec(text, l, page=None):
    """a heading (H3) with the boxes' titles in language l, as the editor shows them (SETTINGS: its menu's names)"""
    if l not in LI:
        return text
    if page in PAGE and text.strip() in PAGE[page]:
        return PAGE[page][text.strip()][LI[l]]
    for k in sorted(SEC, key=len, reverse=True):
        text = _rx(k).sub(SEC[k][LI[l]], text) if k in text else text
    return text
LI = {l: i for i, l in enumerate(["fr", "de", "es", "it", "zh", "ja"])}
ALWAYS = {"SOUND", "SEQUENCER", "SONG", "TRACKS", "PROJECTS", "SAMPLES", "BACKUP", "SETTINGS", "EDITOR", "LIGHTING", "LANGUAGE",
          "SOUNDS", "AUTOMATION", "SEQUENCE", "SECTIONS", "SLOTS", "ACTIVE", "MUSIC"}
WORDS, PAGE = {}, {}
_LB = os.path.join(os.path.dirname(_ED), "guru-labels.js")   # the FM-1's non-technical words, translated (per page)
for _pg, _d in json.loads(open(_LB).read().split("const LABELS = ", 1)[1].rstrip(";\n")).items():
    for _w, _v in _d.items():
        PAGE.setdefault(_pg, {}).setdefault(_w, _v)
for e in _W:
    if e[0].startswith("@"):
        PAGE.setdefault(e[0][1:], {})[e[1]] = e[2:]
    else:
        WORDS[e[0]] = e[1:]


def _rx(k):
    tail = r"(?! [AB]\b)" if k == "SOUND" else ""          # (SOUND A, SOUND B: MORPH's, the FM-1's)
    return re.compile(r"(?<![A-Za-z0-9À-ÿ'])" + re.escape(k) + r"(?![A-Za-z0-9À-ÿ'])" + tail)


_ORDER = sorted(WORDS, key=len, reverse=True)
_RX = {k: _rx(k) for k in _ORDER}


def ui(text, l, page=None):
    """text (a translation, HTML) with the editor's words in language l"""
    if l not in LI:
        return text
    i, out, bold = LI[l], [], 0
    for part in re.split(r"(<[^>]+>)", text):
        if part.startswith("<"):
            if re.match(r"<b\b", part):
                bold += 1
            elif part.startswith("</b"):
                bold = max(0, bold - 1)
            out.append(part)
            continue
        for k in _ORDER:
            if (" " in k or k in ALWAYS or bold) and k in part:
                part = _RX[k].sub(WORDS[k][i], part)
        if page and page in PAGE and bold:
            for k, v in sorted(PAGE[page].items(), key=lambda kv: len(kv[0]), reverse=True):
                if k in part:
                    part = _rx(k).sub(v[i], part)
        out.append(part)
    return "".join(out)
