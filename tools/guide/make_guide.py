"""Guru-600 Editor – Guide : le guide de l'éditeur web (p600/editeur), séparé de la notice et complet à lui seul, en sept
langues : guide/index.html (?lang=xx, imprimable en PDF : make_pdf.sh). Même mise en page et mêmes règles
typographiques que la notice : ses fonctions (make_notice.py, jusqu'aux sections) sont reprises telles quelles, avec les
traductions du guide (guide/tr_xx.json, exportées par tr_export.py depuis guide/strings.json).
Chaque fichier de chap/ (dans l'ordre des noms) appelle CH(clé, en, fr, corps) ; {ch:clé} : le numéro d'un chapitre.
Les captures : shots/ (capture.py, l'éditeur hors connexion, ses valeurs de démonstration)."""
import os, re, json, glob, shutil
H = os.path.dirname(os.path.abspath(__file__))
N = os.path.join(os.path.dirname(H), "notice")
_src = open(os.path.join(N, "make_notice.py")).read()
_head = _src.split("S = []   # the sections")[0].replace("H = os.path.dirname(os.path.abspath(__file__))", f"H = {H!r}")
exec(_head)                                            # typo, LANGS, TR (the guide's), T, P2, H2, H3, H4, LI, OL, table...
_m = re.search(r"\nCHAPS = \[\]\n.*?(?=\nimport glob)", _src, re.S)
exec(_m.group(0))                                      # CH, STEPS, QA, BOX (wiki, felucca)
_m = re.search(r"\ndef _elem_end.*?(?=\nS = \[keep_title)", _src, re.S)
exec(_m.group(0))                                      # keep_title

EDC = {"sound": "#EDEBE6", "seq": "#FF7A22", "song": "#40E0B4", "arp": "#50C8E8", "fx": "#4F86FF", "mod": "#A884FF",
       "tracks": "#FF7A22", "projects": "#EDEBE6", "samples": "#FA7CC4", "backup": "#EDEBE6", "settings": "#8CD86C"}


import ui_i18n                                          # (the editor's own words in each language: as on its screen)
_PG = [None]                                           # the chapter being read: its page (ADD, INSERT... of SONG)
_T0 = T


def T(en, fr, tag="span"):
    return re.sub(r'(<(\w+) class="(\w\w)" lang="\3">)(.*?)(</\2>)',
                  lambda m: m.group(1) + ui_i18n.ui(m.group(4), m.group(3), _PG[0]) + m.group(5), _T0(en, fr, tag), flags=re.S)


_TABLE0 = table


def table(head, rows, cls=""):                         # (a row's name cell in each language: as the editor shows it there)
    def name(c):
        if not isinstance(c, str) or "<b>" not in c:
            return c
        return "".join(f'<span class="{l}" lang="{l}">{ui_i18n.ui(c, l, _PG[0]) if l != "en" else c}</span>' for l in LANGS)
    return _TABLE0(head, [[name(r[0])] + list(r[1:]) for r in rows], cls)


_H3_0 = H3


def H3(en, fr, color=None):                            # (a heading naming a box: its title as the editor shows it)
    return re.sub(r'(<(\w+) class="(\w\w)" lang="\3">)(.*?)(</\2>)',
                  lambda m: m.group(1) + ui_i18n.sec(m.group(4), m.group(3), _PG[0]) + m.group(5), _H3_0(en, fr, color), flags=re.S)


def SHOT(name, en, fr, w=680):                         # a capture of the editor (in English for every language: Marc, 10/11)
    return (f'<figure class="ed" style="width:{w}px"><img src="shots/en/{name}.jpg" style="width:{w}px" alt="">'
            f'<figcaption>{T(en, fr)}</figcaption></figure>')


def CTL(rows, head=(("Control", "Commande"), ("What it does", "Ce qu'elle fait"))):   # [(name, en, fr)]
    return table(list(head), [[f'<b>{n}</b>', (a, b)] for n, a, b in rows], "knobs ctl")


def CTL3(rows):                                        # [(name, en, fr, values_en, values_fr)]
    return table([("Control", "Commande"), ("What it does", "Ce qu'elle fait"), ("Values", "Valeurs")],
                 [[f'<b>{n}</b>', (a, b), (c, d)] for n, a, b, c, d in rows], "knobs")


S = []
for _f in sorted(glob.glob(os.path.join(H, "chap", "*.py"))):
    _PG[0] = re.sub(r"^\d+_", "", os.path.basename(_f)[:-3])
    exec(open(_f).read())
NCH = len(CHAPS)
CHNUM = {k: i + 1 for i, (k, *_r) in enumerate(CHAPS)}
json.dump({"n": NCH, "chapters": CHNUM}, open(os.path.join(H, "chapters.json"), "w"))
open(os.path.join(os.path.dirname(H), "editeur", "guru-guide-ch.js"), "w").write(   # (the editor's ?: each page's chapter)
    "// Guru-600 editor: the guide's chapter of each page (written by guide/make_guide.py: do not edit)\n"
    f"const GUIDE_CH = {json.dumps(CHNUM)};\n")
TOC_PAGES = json.load(open(os.path.join(H, "toc_pages.json"))) if os.path.exists(os.path.join(H, "toc_pages.json")) else {}


def toc_pg(k):
    return "".join(f'<span class="pg {l}" lang="{l}">{TOC_PAGES[l][k - 1]}</span>'
                   for l in LANGS if l in TOC_PAGES and len(TOC_PAGES[l]) >= k)


LOGO = ('<div class="logo-t" role="img" aria-label="guru-600"><span class="g6">guru-600</span>'
        '<span class="trib">A PROPHET-600 TRIBUTE</span></div>')
S.append('<section class="cover lc">' + LOGO + T("Editor guide", "Guide de l'éditeur", "h1") +
         P2("The web editor of the Guru-600 for the M-VAVE FM-1 · version 1.0", "L'éditeur web du Guru-600 pour le M-VAVE FM-1 · version 1.0") +
         P2("by Marc Massé · based on Felucca by Leo Kuroshita", "par Marc Massé · d'après Felucca de Leo Kuroshita") + '</section>')
S.append('<section class="toc">' + T("Contents", "Sommaire", "h2") + '<ol>' +
         ''.join(f'<li><span class="n">{i + 1}</span><a href="#s{i + 1}">{T(en, fr)}</a>{toc_pg(i + 1)}</li>'
                 for i, (k, en, fr, b) in enumerate(CHAPS)) + '</ol></section>')
for i, (k, en, fr, body) in enumerate(CHAPS):
    S.append(f'<section>{H2(i + 1, en, fr)}' + body + '</section>')

LANG_FULL = [("en", "English", "Editor guide"), ("fr", "Français", "Guide de l'éditeur"),
             ("de", "Deutsch", "Editor-Handbuch"), ("es", "Español", "Guía del editor"),
             ("it", "Italiano", "Guida all'editor"), ("zh", "中文", "编辑器指南"), ("ja", "日本語", "エディター ガイド")]
S.insert(0, '<section class="cover all">' + LOGO + '<p class="sub">Editor · M-VAVE FM-1 · v1.0 · Marc Massé</p>'
            '<img class="fm1" src="shots/cover.jpg" alt="Guru-600 editor">'
            '<nav class="golang">' + ''.join(f'<a href="https://guru-600.lang/{l}" data-l="{l}"><b>{n}</b><span>{typo(t, "fr" if l == "fr" else "en")}</span></a>'
                                            for l, n, t in LANG_FULL) + '</nav></section>')

S = [keep_title(x) if x.startswith("<section>") else x for x in S]
BADREF = set()
S = [re.sub(r"\{ch:(\w+)\}", lambda m: str(CHNUM[m.group(1)]) if m.group(1) in CHNUM else BADREF.add(m.group(1)) or "??", x) for x in S]
CSS = open(os.path.join(N, "notice.css")).read() + open(os.path.join(H, "guide.css")).read()
out = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Guru-600 Editor · Guide</title><style>' + CSS +
       ''.join(f'body:not([data-lang={l}]) .{l}{{display:none}}' for l in LANGS) + '</style></head><body>'
       '<nav id="lang">' + ''.join(f'<button data-l="{l}" onclick="setLang(\'{l}\')">{LNAME[l]}</button>' for l in LANGS) +
       '</nav>' + ''.join(S) +
       '<script>function setLang(l){document.body.dataset.lang=l;document.documentElement.lang=l;'
       'document.querySelectorAll("#lang button").forEach(function(b){b.classList.toggle("on",b.dataset.l==l)});'
       'try{localStorage.g6lang=l}catch(e){}}'
       'var u=new URLSearchParams(location.search),q=u.get("lang"),s;if(u.get("part"))document.body.classList.add("part-"+u.get("part"));try{s=localStorage.g6lang}catch(e){}'
       'var nl=(navigator.language||"en").slice(0,2);if(["en","fr","de","es","it","zh","ja"].indexOf(nl)<0)nl="en";setLang(q||s||nl);'
       'document.querySelectorAll(".golang a").forEach(function(a){a.onclick=function(e){e.preventDefault();setLang(a.dataset.l);'
       'document.querySelector(".toc").scrollIntoView()}});if(location.hash)setTimeout(function(){var t=document.querySelector(location.hash);if(t)t.scrollIntoView()},0)</script></body></html>')
open(os.path.join(H, "index.html"), "w").write(out)
for d in ("fonts",):                                   # (the guide's folder: complete on its own)
    if not os.path.isdir(os.path.join(H, d)):
        shutil.copytree(os.path.join(N, d), os.path.join(H, d))
json.dump([{"en": k, "fr": v} for k, v in STRINGS.items()], open(os.path.join(H, "strings.json"), "w"), ensure_ascii=False, indent=1)
print("chapters", NCH, "strings", len(STRINGS), "missing", sorted(MISSING), "bad refs", sorted(BADREF))
