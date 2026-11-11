"""La notice bilingue de Guru 600 (anglais / français) : notice/index.html, un bouton EN / FR, imprimable en PDF
(?lang=en, ?lang=fr). Les listes de sons viennent des banques (factory_bank.json, factory_names.json, factory_notes.json,
banques/v2022_doc.json)."""
import html, json, os, re
H = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(H)
J = lambda f: json.load(open(os.path.join(P, f)))
names, notes, bank = J("factory_names.json"), J("factory_notes.json"), J("factory_bank.json")
v22 = J("banques/v2022_doc.json")
e = html.escape


NNBSP, NBSP = "\u202f", "\u00a0"


SEC = {"en": "s", "fr": "s", "de": "s", "es": "s", "it": "s", "zh": "秒", "ja": "秒"}


def typo(t, lang):                      # French or English typography, on the text between the tags
    parts = re.split(r"(<[^>]+>)", t)
    for k, x in enumerate(parts):
        if not x or x.startswith("<"):
            continue
        x = x.replace("&#x27;", "'").replace("&quot;", '"')
        x = re.sub(r"(?<=\w)'(?=\w)", "’", x)            # apostrophe
        if lang == "de":                                # German quotes „…“ ‚…‘
            x = re.sub(r"(^|[\s(])'", "\\1‚", x).replace("'", "‘")
            x = re.sub(r'(^|[\s(])"', "\\1„", x).replace('"', "“")
        elif lang in ("es", "it"):                      # « … » without spaces
            x = re.sub(r"(^|[\s(])'", "\\1‘", x).replace("'", "’")
            x = re.sub(r'(^|[\s(])"', "\\1«", x).replace('"', "»")
        else:
            x = re.sub(r"(^|[\s(])'", "\\1‘", x)            # opening single quote
            x = x.replace("'", "’")
            x = re.sub(r'(^|[\s(])"', "\\1“", x).replace('"', "”")
        x = re.sub(r"(\d) s\b(?![’'])", "\\1" + NNBSP + SEC[lang], x)   # seconds: s (秒 in Chinese and Japanese)
        x = re.sub(r"(\d) (%|ms|s|Hz|dB|st|mm|cm|Mo|Ko)\b(?![’'])", "\\1" + NNBSP + "\\2", x)
        x = re.sub(r"(\d) %", "\\1" + NNBSP + "%", x)
        x = re.sub(r" ›", NBSP + "›", x)
        if lang == "fr":
            x = x.replace("“", "«" + NNBSP).replace("”", NNBSP + "»")
            x = re.sub(r"«\s*", "«" + NNBSP, x)
            x = re.sub(r"\s*»", NNBSP + "»", x)
            x = re.sub(r"\s+([;!?])", NNBSP + "\\1", x)
            x = re.sub(r"\s+:", NBSP + ":", x)
            x = re.sub(r" (—|–) ", NBSP + "\\1 ", x)
            x = re.sub(r"\b(N°|n°) ", "\\1" + NBSP, x)
        else:                                           # English, German, Spanish, Italian: no space before
            x = re.sub(r"\s+([:;!?])", "\\1", x)
            if lang in ("es", "it"):
                x = re.sub(r"«\s+", "«", x)
                x = re.sub(r"\s+»", "»", x)
            if lang in ("de", "it"):                    # Gedankenstrich / trattino: – with spaces
                x = re.sub(r"\s*—\s*", NBSP + "– ", x)
            if lang == "es":                            # raya: —inciso— against its words
                x = re.sub(r" — ([^—]+?) — ", " —\\1— ", x)
                x = re.sub(r" — ([^—]+?)([.,;:)])", " —\\1\\2", x)
        if lang == "fr":                                # the article, as for "le Prophet-600"
            for a, b in ((r"\bde Guru 600", "du Guru 600"), (r"\bDans Guru 600", "Dans le Guru 600"),
                         (r"\bque Guru 600", "que le Guru 600"), (r"\bpas Guru 600", "pas le Guru 600"),
                         (r"\bInstaller Guru 600", "Installer le Guru 600"),
                         (r"Guru 600 et Prophet-600", "Le Guru 600 et le Prophet-600"),
                         (r"(:\s?)Guru 600 (?=remplace)", "\\1le Guru 600 "),
                         (r"\btourner Guru 600", "tourner le Guru 600"),
                         (r"(\u202f;\s)Guru 600(?= est)", "\\1le Guru 600"),
                         (r"(^\s?|\.\s)Guru 600(?=,| transforme| repose| a | est | sur le FM-1)", "\\1Le Guru 600")):
                x = re.sub(a, b, x)
        x = re.sub(r"\b(chapters?|chapitres?|Kapitel[n]?|capítulos?|capitol[oi]|pages?|Seiten?|páginas?|pagin[ae]|KNOB|TRACK|tracks?|pistes?|Spuren?|pistas?|tracce|traccia|steps?|étapes?|Schritt|pasos?|pass[oi]|places?|emplacements?|Platz|Plätze|posici[oó]n(?:es)?|posizion[ei]|slots?|n°|N°|Nr\.|version|Version|versión|versione) (\d|\{ch:)", "\\1" + NBSP + "\\2", x)   # a word and its number: never apart
        x = x.replace("(‘)", "(')")                    # (the apostrophe key, not a quote)
        x = re.sub(r"Guru 600", "Guru\u2060-\u2060600", x)   # Guru-600, never cut at its hyphen
        x = x.replace("Guru-600", "Guru\u2060-\u2060600")
        x = re.sub(r"Prophet-600", "Prophet\u2060-\u2060600", x)
        parts[k] = x
    t = "".join(parts)
    if lang in ("zh", "ja"):                        # no space between two Chinese or Japanese characters (a tag between
        C = "[\u3000-\u30ff\u3400-\u9fff\uff00-\uffef]"   # them, as around a bold word, included)
        t = re.sub(f"({C})((?:<[^>]+>)*) ((?:<[^>]+>)*)(?={C})", "\\1\\2\\3", t)
        t = re.sub("(\\d)[ \u00a0\u202f]%", "\\1%", t)               # 50%, without a space
        if lang == "ja":                            # ？ and ！ inside a paragraph: a full-width space after them
            t = re.sub(f"({C}) (?=\\d)", "\\1", t)        # を1秒: no space before a number
            t = t.replace("\u202f秒", "秒")                # 1秒
            t = re.sub(f"([？！])(?={C})", "\\1\u3000", t)
    return t


LANGS = ("en", "fr", "de", "es", "it", "zh", "ja")   # (24/10: Simplified Chinese and Japanese, the last two)
LNAME = {"en": "EN", "fr": "FR", "de": "DE", "es": "ES", "it": "IT", "zh": "中文", "ja": "日本語"}
TR = {}                                 # tr_de.json ...: the English text -> its translation
for _l in LANGS[2:]:
    _f = os.path.join(H, f"tr_{_l}.json")
    TR[_l] = json.load(open(_f)) if os.path.exists(_f) else {}
STRINGS, MISSING = {}, set()            # the texts to translate (strings.json), those still missing


def T(en, fr, tag="span"):              # a text in every language (German, Spanish, Italian from tr_*.json)
    txt = {"en": en, "fr": fr}
    text_only = re.sub(r"<[^>]+>", "", en)
    for l in LANGS[2:]:
        if not re.search(r"[A-Za-z]", text_only):
            txt[l] = en
            continue
        STRINGS.setdefault(en, fr)
        if en in TR[l]:
            txt[l] = TR[l][en]
        else:
            MISSING.add(l)
            txt[l] = en
    return "".join(f'<{tag} class="{l}" lang="{l}">{typo(txt[l], l)}</{tag}>' for l in LANGS)


def P2(en, fr):
    return T(en, fr, "p")


def H2(i, en, fr):
    return f'<h2 id="s{i}"><span class="num">{i}</span>{T(en, fr)}</h2>'


def H3(en, fr, color=None):
    st = f' style="--c:{color}"' if color else ""
    return f'<h3{st}>{T(en, fr)}</h3>'


def H4(en, fr):
    return f'<h4>{T(en, fr)}</h4>'


def shot(src, en, fr, w=280):
    return (f'<figure style="width:{w}px"><img src="{src}" style="width:{w}px" alt=""><figcaption>{T(en, fr)}</figcaption></figure>')


def LI(items):                          # [(en, fr), ...]
    return '<ul>' + ''.join(f'<li>{T(a, b)}</li>' for a, b in items) + '</ul>'


def OL(items):
    return '<ol>' + ''.join(f'<li>{T(a, b)}</li>' for a, b in items) + '</ol>'


def table(head, rows, cls=""):          # head: [(en, fr)], rows: [[cell...]] (cells: str or (en, fr))
    c = lambda x: T(*x) if isinstance(x, tuple) else x
    return (f'<table class="{cls}"><thead><tr>' + ''.join(f'<th>{c(h)}</th>' for h in head) + '</tr></thead><tbody>' +
            ''.join('<tr>' + ''.join(f'<td>{c(x)}</td>' for x in r) + '</tr>' for r in rows) + '</tbody></table>')


def knobs(rows):                        # [(name, en, fr, range_en, range_fr)]
    return table([("Knob", "Bouton"), ("What it does", "Ce qu'il fait"), ("Values", "Valeurs")],
                 [[f'<b>{n}</b>', (a, b), (c, d)] for n, a, b, c, d in rows], "knobs")


FAM = {"osc": "#f49638", "flt": "#ff5046", "env": "#fa7cc4", "pm": "#a884ff", "lfo": "#50c8e8", "vce": "#8cd86c",
       "ext": "#ffe428", "mph": "#40e0b4"}


def page(fam, img, title_en, title_fr, intro_en, intro_fr, rows, where_en, where_fr):
    return (f'<div class="page-block" style="--c:{FAM[fam]}">' + H3(title_en, title_fr, FAM[fam]) +
            '<div class="split">' + shot(img, where_en, where_fr, 240) + '<div>' + P2(intro_en, intro_fr) + knobs(rows) +
            '</div></div></div>')


S = []   # the sections, in order
# ------------------------------------------------------------------------------------------------ cover
S.append('<section class="cover lc"><div class="logo-t" role="img" aria-label="guru-600"><span class="g6">guru-600</span><span class="trib">A PROPHET-600 TRIBUTE</span></div>' +
         T("User guide", "Notice d'utilisation", "h1") +
         P2("A Prophet-600 tribute for the M-VAVE FM-1 · version 1.0", "Un hommage au Prophet-600 pour le M-VAVE FM-1 · version 1.0") +
         P2("by Marc Massé · based on Felucca by Leo Kuroshita", "par Marc Massé · d'après Felucca de Leo Kuroshita") +
         '</section>')

# ------------------------------------------------------------------------------------------------ the chapters
# Each file of chap/ (in name order) calls CH(key, en, fr, body): a chapter. Its number is its rank; {ch:key} in any
# text becomes that chapter's number (in every language, after translation).
CHAPS = []


def CH(key, en, fr, body):
    CHAPS.append((key, en, fr, body))


WIKI = "https://github.com/hugelton/Felucca/wiki"


def wiki(page=""):                        # a link to the Felucca wiki (in English)
    u = WIKI + ("/" + page if page else "")
    return f'<a href="{u}">{u.replace("https://", "")}</a>'


def felucca(page, en, fr):                # the box under each Felucca screen: its summary and the wiki
    return ('<div class="fel">' + T('<b>Felucca</b> · ' + en + ' Details: ' + wiki(page) + ' (in English).',
                                    '<b>Felucca</b> · ' + fr + ' Détails : ' + wiki(page) + ' (en anglais).') + '</div>')


def STEPS(items):                         # numbered steps: [(en, fr), ...]
    return '<ol class="steps">' + ''.join(f'<li>{T(a, b)}</li>' for a, b in items) + '</ol>'


def QA(items):                            # questions and answers: [(q_en, q_fr, a_en, a_fr), ...]
    return '<dl class="qa">' + ''.join(f'<dt>{T(q, qf)}</dt><dd>{T(a, af)}</dd>' for q, qf, a, af in items) + '</dl>'


def BOX(cls, *paras):                     # a framed box (note, key, warn, tip) of paragraphs (en, fr)
    return f'<div class="{cls}">' + ''.join(P2(a, b) for a, b in paras) + '</div>'


import glob
for _f in sorted(glob.glob(os.path.join(H, "chap", "*.py"))):
    exec(open(_f).read())

NCH = len(CHAPS)
CHNUM = {k: i + 1 for i, (k, *_r) in enumerate(CHAPS)}
TOC_PAGES = json.load(open(os.path.join(H, "toc_pages.json"))) if os.path.exists(os.path.join(H, "toc_pages.json")) else {}


def toc_pg(k):                            # the page of chapter k (1..) in each language: make_pdf.sh, first pass
    return "".join(f'<span class="pg {l}" lang="{l}">{TOC_PAGES[l][k - 1]}</span>'
                   for l in LANGS if l in TOC_PAGES and len(TOC_PAGES[l]) >= k)


S.append('<section class="toc">' + T("Contents", "Sommaire", "h2") + '<ol>' +
         ''.join(f'<li><span class="n">{i + 1}</span><a href="#s{i + 1}">{T(en, fr)}</a>{toc_pg(i + 1)}</li>'
                 for i, (k, en, fr, b) in enumerate(CHAPS)) +
         f'<li><span class="n">{NCH + 1}</span><a href="https://guru-600.lang/annex" data-l="annex">{T("Appendix: the 255 sounds", "Annexe : les 255 sons")}</a>'
         f'{toc_pg(NCH + 1)}</li></ol></section>')   # (the appendix, in every language's contents: make_pdf.sh links it)
S.append('<div class="thanks">' +       # (before chapter 1: a short thank-you)
         P2("Thank you for downloading the Guru-600, an emulator of the Sequential Circuits Prophet-600. We hope you enjoy playing it as much as we enjoyed creating it. "
            "This guide shows you everything your FM-1 can now do. Enjoy the music!",
            "Merci d'avoir téléchargé le Guru-600, un émulateur du Prophet-600 de Sequential Circuits. Nous espérons qu'il vous donnera autant de plaisir à jouer qu'il nous en a "
            "donné à le créer. Cette notice vous fait découvrir tout ce que votre FM-1 sait désormais faire. Bonne musique !") + '</div>')
for i, (k, en, fr, body) in enumerate(CHAPS):
    S.append(f'<section>{H2(i + 1, en, fr)}' + body + '</section>')
json.dump({"n": NCH}, open(os.path.join(H, "chapters.json"), "w"))

# ------------------------------------------------------------------------------------------------ the common cover
# (first page of the PDF and of the screen version: a link to each language; make_pdf.sh turns the links into pages)
LANG_FULL = [("en", "English", "User guide"), ("fr", "Français", "Notice d'utilisation"),
             ("de", "Deutsch", "Bedienungsanleitung"), ("es", "Español", "Manual de usuario"),
             ("it", "Italiano", "Manuale d'uso"), ("zh", "中文", "用户指南"), ("ja", "日本語", "ユーザーガイド")]
ALLCOVER = ('<section class="cover all"><div class="logo-t" role="img" aria-label="guru-600"><span class="g6">guru-600</span><span class="trib">A PROPHET-600 TRIBUTE</span></div>'
            '<p class="sub">M-VAVE FM-1 · v1.0 · Marc Massé</p>'
            '<img class="fm1" src="img/cover_fm1.png" alt="M-VAVE FM-1, Guru-600">'   # (the FM-1, Guru-600 starting: fm1-live)
            '<nav class="golang">' +
            ''.join(f'<a href="https://guru-600.lang/{l}" data-l="{l}"><b>{n}</b><span>{typo(t, "fr" if l == "fr" else "en")}</span></a>'
                    for l, n, t in LANG_FULL) + '</nav></section>')
S.insert(0, ALLCOVER)

# ------------------------------------------------------------------------------------------------ appendix (every language)
# the sounds' texts in five languages: French from factory_notes / v2022_doc, else trs_fr.json; trs_de/es/it.json
TRS = {l: (json.load(open(os.path.join(H, f"trs_{l}.json"))) if os.path.exists(os.path.join(H, f"trs_{l}.json")) else {})
       for l in ("fr", "de", "es", "it", "zh", "ja")}
FR_KNOWN = {}
for _w_en, _w_fr, _t_en, _t_fr in notes.values():
    FR_KNOWN[_w_en], FR_KNOWN[_t_en] = _w_fr, _t_fr
for _x in v22.values():
    FR_KNOWN[_x["fam"][0]] = _x["fam"][1]
cols = {int(k): v for k, v in json.load(open(os.path.join(P, "banques/v2022/v2022_cols.json"))).items()}


def ml(en, inline=False):               # an appendix text in the five languages, each with its code
    if not en:
        return "—"
    texts = {}                          # the same text in several languages: once, with their codes (English, French)
    for l in ("en", "fr"):
        t = en if l == "en" else (FR_KNOWN.get(en) or TRS["fr"].get(en)) if l == "fr" else TRS[l].get(en)
        if not t:
            MISSING.add("sounds-" + l)
            t = en
        texts.setdefault(t, []).append(l)
    if len(texts) == 1:
        return typo(e(en), "en")
    return "".join(f'<span class="ml"><i>{" ".join(x.upper() for x in ls)}</i> {typo(e(t), ls[0])}</span>'
                   for t, ls in texts.items())


def tr1(en, l):                         # one appendix text in one language
    if l == "en":
        return en
    t = (FR_KNOWN.get(en) or TRS["fr"].get(en)) if l == "fr" else TRS[l].get(en)
    if not t:
        MISSING.add("sounds-" + l)
    return t or en


def fixc(c):                            # the collection's numbers as Guru 600's places, its typos
    return (c.replace("based on 50", "based on 151").replace("compared to 30", "compared to 131")
             .replace("strongy", "strong").replace("Poly-mod to for", "Poly-mod for"))


def feats(c):                           # the collection's columns, short
    f = []
    if c["oscfm"]: f.append("Osc FM " + c["oscfm"])
    if c["filfm"]: f.append("Filter FM " + c["filfm"])
    if c["env"]: f.append("ENV " + c["env"].upper())
    for k, n in (("sync", "SYNC"), ("harm", "HARM"), ("unison", "UNI"), ("vel", "VEL")):
        if c[k]: f.append(n)
    return "<br>".join(e(x) for x in f) or "—"


fac = []
for i in range(100):
    full, short = names[i]
    w_en, w_fr, t_en, t_fr = notes[str(i)]
    fac.append(f'<tr><td><b>{i+1}</b></td><td>{e(full)}</td><td>{ml(w_en)}</td><td>{ml(t_en)}</td></tr>')
v22r = []
for i in range(100):
    x, c = v22[str(i)], cols[i]
    by = c["by"]
    if by.startswith("Z80 Nbr."):
        by = f'{by} (= {int(by.split()[-1]) + 1})'
    v22r.append(f'<tr><td><b>{101+i}</b></td><td>{e(x["name"].upper())}</td><td>{e(by)}</td><td>{ml(x["fam"][0])}</td>'
                f'<td class="ft">{feats(c)}</td><td>{ml(fixc(c["comment"]))}</td></tr>')
ML = lambda *w: " · ".join(w)
LEG = ["Osc FM: how strongly oscillator B modulates oscillator A (Poly-Mod), from * to *****.",
       "Filter FM: how strongly oscillator B modulates the filter (Poly-Mod), from * to *****.",
       "ENV: non-standard envelope routing (POLY or GATE).",
       "SYNC: oscillator sync on. HARM: harmonic filter (full keyboard tracking, resonance near self-oscillation: the filter plays as a third oscillator). UNI: unison. VEL: plays with more expression from a velocity-sensitive MIDI keyboard.",
       "Z80 Nbr. n: a version of the original factory sound n (number n+1 in Guru 600)."]
TH = lambda en: en
GX = json.load(open(os.path.join(P, "banques/guru/guru_extras.json")))
def bi2(en, fr):                         # an appendix cell in English and French, each with its code
    return (f'<span class="ml"><i>EN</i> {typo(e(en), "en")}</span>'
            f'<span class="ml"><i>FR</i> {typo(e(fr), "fr")}</span>')
gr = []
for i, x in enumerate(GX):
    if x["origin"] == "surge":
        who = "Claes Johanson" if x["author"] == "Claes" else x["author"]
        about = bi2(f'Adapted from the Surge XT sound "{x["full"]}" by {who}.',
                    f'Adapté du son « {x["full"]} » de Surge XT, de {who}.')
        orig = "Surge XT"
    else:
        about = bi2(*x["about"])
        orig = "Guru-600"
    gr.append(f'<tr><td><b>{201 + i}</b></td><td>{e(x["full"].upper())}</td><td>{bi2(*x["fam"]) if x["fam"][0] != x["fam"][1] else typo(e(x["fam"][0]), "en")}</td>'
              f'<td>{orig}</td><td>{about}</td></tr>')
GURU_T = ('<h3 class="v22">201–255 · Guru-600</h3><table class="snd g6t"><thead><tr><th>No.</th><th>Name</th>'
          '<th>Family</th><th>Origin</th><th>About</th></tr></thead><tbody>' + "".join(gr) + '</tbody></table>')
ANNEX = ('<section class="annex"><h2><span class="num">' + str(NCH + 1) + '</span>' + ML("Appendix", "Annexe", "Anhang", "Anexo", "Appendice") + '<br>' + ML('<span lang="zh">附录</span>', '<span lang="ja">付録</span>') + '</h2>'
         '<p class="langs">' + ML("The 255 sounds", "Les 255 sons", "Die 255 Klänge", "Los 255 sonidos", "I 255 suoni", '<span lang="zh">255 个音色</span>', '<span lang="ja">255 の音色</span>') + '</p>'
         '<h3>1–100 · Prophet-600 factory sounds</h3>'
         '<table class="snd"><thead><tr><th>No.</th><th>Name</th><th>' + TH("Mod wheel") + '</th><th>' + TH("Tips") +
         '</th></tr></thead><tbody>' + "".join(fac) + '</tbody></table>'
         '<h3 class="v22">101–200 · v2022 (GPL)</h3><div class="legend">' + "".join(
             f'<div class="lgb" lang="{l}"><i>{l.upper()}</i>' + "".join(f'<p>{typo(e(tr1(t, l)), l)}</p>' for t in LEG) + '</div>'
             for l in ("en", "fr", "de", "es", "it", "zh", "ja")) + '</div>'
         '<table class="snd v22t"><thead><tr><th>No.</th><th>Name</th><th>' + TH("Author") + '</th><th>' + TH("Family") +
         '</th><th>' + TH("Features") + '</th><th>' + TH("Comments") + '</th></tr></thead><tbody>' +
         "".join(v22r) + '</tbody></table>' + GURU_T + '</section>')
S.append(ANNEX)

# ------------------------------------------------------------------------------------------------ page
CSS = open(os.path.join(H, "notice.css")).read()

def _elem_end(h, i):                      # the end of the element that starts at h[i] ('<tag ...'), its own tag nested
    m = re.match(r"<([a-zA-Z0-9]+)", h[i:])
    tag = m.group(1)
    depth, j = 0, i
    for t in re.finditer(r"<(/?)" + tag + r"\b[^>]*>", h[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return i + t.end()
    return len(h)


def keep_title(h):                        # every title (h2, h3), its first lines and the block after them, on one page
    out, pos = [], 0
    for m in re.finditer(r"<h([23])\b", h):
        if m.start() < pos:
            continue
        e = h.index("</h%s>" % m.group(1), m.start()) + 5
        for k in range(2):                # the first element, and the second one when the first is a paragraph
            while e < len(h) and h[e].isspace():
                e += 1
            if e >= len(h) or h[e] != "<" or h.startswith("</", e) or re.match(r"<h[23]\b", h[e:]):
                break
            e2 = _elem_end(h, e)
            if k == 1 and e2 - e > 40000:  # (a long table: it may break, the title stays with the first lines; the
                break                     # HTML holds the five languages: 5 x the printed text)
            first_p = h.startswith("<p", e)
            e = e2
            while first_p:                # (a paragraph is one <p> per language: all of them)
                e3 = e
                while e3 < len(h) and h[e3].isspace():
                    e3 += 1
                if not re.match(r'<p class="(en|fr|de|es|it)"', h[e3:]):
                    break
                e = _elem_end(h, e3)
            if not first_p:
                break
        out.append(h[pos:m.start()] + '<div class="keep">' + h[m.start():e] + "</div>")
        pos = e
    return "".join(out) + h[pos:]


S = [keep_title(x) if x.startswith("<section>") else x for x in S]
BADREF = set()
S = [re.sub(r"\{ch:(\w+)\}", lambda m: str(CHNUM[m.group(1)]) if m.group(1) in CHNUM else BADREF.add(m.group(1)) or "??", x)
     for x in S]   # the chapters' numbers   # (the chapters; not the covers, the contents)

out = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Guru-600 · User guide</title><style>' + CSS +
       ''.join(f'body:not([data-lang={l}]) .{l}{{display:none}}' for l in LANGS) + '</style></head><body>'
       '<nav id="lang">' + ''.join(f'<button data-l="{l}" onclick="setLang(\'{l}\')">{LNAME[l]}</button>' for l in LANGS) +
       '</nav>' + ''.join(S) +
       '<script>function setLang(l){document.body.dataset.lang=l;document.documentElement.lang=l;'
       'document.querySelectorAll("#lang button").forEach(function(b){b.classList.toggle("on",b.dataset.l==l)});'
       'try{localStorage.g6lang=l}catch(e){}}'
       'var u=new URLSearchParams(location.search),q=u.get("lang"),s;if(u.get("part"))document.body.classList.add("part-"+u.get("part"));try{s=localStorage.g6lang}catch(e){}'
       'var nl=(navigator.language||"en").slice(0,2);if(["en","fr","de","es","it","zh","ja"].indexOf(nl)<0)nl="en";setLang(q||nl);document.querySelectorAll(".golang a,.toc a[data-l]").forEach(function(a){a.onclick=function(e){e.preventDefault();'
       'var l=a.dataset.l;if(l=="annex"){document.querySelector(".annex").scrollIntoView()}else{setLang(l);'
       'document.querySelector(".toc").scrollIntoView()}}})</script></body></html>')
open(os.path.join(H, "index.html"), "w").write(out)
json.dump([{"en": k, "fr": v} for k, v in STRINGS.items()], open(os.path.join(H, "strings.json"), "w"), ensure_ascii=False, indent=1)
print("strings", len(STRINGS), "missing", sorted(MISSING), "bad refs", sorted(BADREF))
print("index.html", len(out))
