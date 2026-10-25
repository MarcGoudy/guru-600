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
        x = re.sub(r"Guru 600", "Guru\u2060-\u2060600", x)   # Guru-600, never cut at its hyphen
        x = re.sub(r"Prophet-600", "Prophet\u2060-\u2060600", x)
        x = re.sub(r"\b(section|Section|Abschnitt|sección|Sección|sezione|Sezione)(\s|\xa0)(\d{1,2})\b",
                   lambda m: m.group(1) + m.group(2) + str(NUM[int(m.group(3)) - 1]), x)
        x = re.sub(r"第(\d{1,2})章", lambda m: "第" + str(NUM[int(m.group(1)) - 1]) + "章", x)   # (Chinese, Japanese)
        parts[k] = x
    return "".join(parts)


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
       "ext": "#ffe428"}


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

# ------------------------------------------------------------------------------------------------ contents
TOC = [("Welcome", "Bienvenue"), ("Synthesizer basics, in plain words", "Le synthétiseur expliqué simplement"),
       ("First steps", "Premiers pas"), ("The FM-1's controls", "Les commandes du FM-1"),
       ("Finding your way: pages and colors", "Se repérer : pages et couleurs"),
       ("The Guru 600 pages, one by one", "Les pages de Guru 600, une par une"),
       ("Felucca's other pages", "Les autres pages de Felucca"), ("The 255 sounds", "Les 255 sons"),
       ("Keeping your sounds: 32 USER places and 55 P600 places", "Garder ses sons : 32 emplacements USER et 55 places P600"),
       ("Importing Prophet-600 sounds from a computer", "Importer des sons Prophet-600 depuis un ordinateur"),
       ("Back to the original sounds (reset)", "Revenir aux sons d'origine (réinitialisation)"),
       ("The mod wheel and MIDI control", "La molette et le pilotage MIDI"), ("The Guru 600 app on a Mac", "L'application Guru 600 sur Mac"),
       ("Installing Guru 600 on an FM-1", "Installer Guru 600 sur un FM-1"),
       ("Prophet-600 panel ↔ Guru 600", "Façade du Prophet-600 ↔ Guru 600"),
       ("Guru 600 and the Prophet-600: what changes", "Guru 600 et Prophet-600 : ce qui change"),
       ("Credits and licenses", "Crédits et licences")]
ORDER = [0, 13] + list(range(1, 13)) + [14, 15, 16]     # TOC's sections as the guide shows them: installing second
NUM = {old: k + 1 for k, old in enumerate(ORDER)}      # TOC index -> section number
TOC_PAGES = json.load(open(os.path.join(H, "toc_pages.json"))) if os.path.exists(os.path.join(H, "toc_pages.json")) else {}


def toc_pg(k):                            # the page of chapter k (1..) in each language: make_pdf.sh, first pass
    return "".join(f'<span class="pg {l}" lang="{l}">{TOC_PAGES[l][k - 1]}</span>'
                   for l in LANGS if l in TOC_PAGES and len(TOC_PAGES[l]) >= k)


S.append('<section class="toc">' + T("Contents", "Sommaire", "h2") + '<ol>' +
         ''.join(f'<li><span class="n">{NUM[i]}</span><a href="#s{NUM[i]}">{T(*TOC[i])}</a>{toc_pg(NUM[i])}</li>'
                 for i in ORDER) +
         f'<li><span class="n">18</span><a href="https://guru-600.lang/annex" data-l="annex">{T("Appendix: the 255 sounds", "Annexe : les 255 sons")}</a>'
         f'{toc_pg(18)}</li></ol></section>')   # (the appendix, in every language's contents: make_pdf.sh links it)



def sec(en, fr):
    k = NUM[TOC.index((en, fr))]
    return f'<section>{H2(k, en, fr)}'


# ------------------------------------------------------------------------------------------------ 1 welcome
S.append(sec(*TOC[0]) +
 P2("Guru 600 turns the M-VAVE FM-1 into a tribute to the <b>Sequential Circuits Prophet-600</b> (1982), one of the first "
    "synthesizers with MIDI. It adds a <b>P600</b> sound engine built like the original — two oscillators per voice, a "
    "24 dB filter, two envelopes, Poly-Mod, an LFO, six voices — and the original's <b>100 factory sounds</b> with their "
    "real names, <b>100 free sounds</b> from the Prophet-600 community and <b>55 sounds of its own</b>.",
    "Guru 600 transforme le M-VAVE FM-1 en hommage au <b>Prophet-600 de Sequential Circuits</b> (1982), l'un des premiers "
    "synthétiseurs MIDI. Il ajoute un moteur sonore <b>P600</b> construit comme l'original — deux oscillateurs par voix, un "
    "filtre 24 dB, deux enveloppes, la Poly-Mod, un LFO, six voix — avec les <b>100 sons d'usine</b> de l'original sous "
    "leurs vrais noms, <b>100 sons libres</b> créés par la communauté du Prophet-600 et <b>55 sons à lui</b>.") +
 P2("Guru 600 is built on <b>Felucca</b>, a free firmware for the FM-1 by Leo Kuroshita. Everything Felucca does is still "
    "there: four tracks, a step sequencer, an arpeggiator, effects, scales and chords, and its other sound engines.",
    "Guru 600 repose sur <b>Felucca</b>, un firmware libre pour le FM-1 écrit par Leo Kuroshita. Tout ce que fait Felucca "
    "est toujours là : quatre pistes, un séquenceur pas à pas, un arpégiateur, des effets, des gammes et des accords, et "
    "ses autres moteurs sonores.") +
 P2("This guide is written for everyone, including people who have never used a synthesizer. Words in "
    "<b>CAPITALS</b> are what you read on the FM-1's buttons and screen.",
    "Cette notice s'adresse à tout le monde, y compris à ceux qui n'ont jamais touché un synthétiseur. Les mots en "
    "<b>CAPITALES</b> sont ceux que vous lisez sur les boutons et l'écran du FM-1.") +
 '<div class="key">' + H3("Getting around", "Se déplacer dans le Guru 600") +
 LI([("<b>Page buttons</b> (ENV, LFO, EDIT, FX, SAVE…): one press opens the family's pages; each new press shows the next page.", "<b>Boutons de page</b> (ENV, LFO, EDIT, FX, SAVE…) : un appui ouvre les pages de la famille ; chaque nouvel appui montre la page suivante."),
     ("<b>Two quick presses</b> on the same button: the page before. This works on every page button.", "<b>Deux appuis rapides</b> sur le même bouton : la page précédente. Cela marche sur tous les boutons de page."),
     ("<b>HOME</b>: back to the home page. Held: the menu.", "<b>HOME</b> : retour à la page d'accueil. Maintenu : le menu."),
     ("<b>Holding</b> FX, GLO, SCL, EDIT, REC or SEQ shows a quick layer: shortcuts on the keys and knobs, for as long as you hold it.", "<b>Maintenir</b> FX, GLO, SCL, EDIT, REC ou SEQ affiche un calque rapide : des raccourcis sur les touches et les boutons, tant que vous le maintenez."),
     ("<b>KNOB 1 to 4</b> change the four settings shown on the screen; <b>PRESETS</b> changes the sound; <b>ALGORITHM</b> picks the track.", "<b>KNOB 1 à 4</b> changent les quatre réglages affichés à l'écran ; <b>PRESETS</b> change le son ; <b>ALGORITHM</b> choisit la piste."),
     ("In dialogs and on pages that do something (save, load, erase): <b>OCT+</b> confirms, <b>OCT−</b> cancels or goes back.", "Dans les dialogues et sur les pages qui exécutent une action (enregistrer, charger, effacer) : <b>OCT+</b> confirme, <b>OCT−</b> annule ou revient en arrière.")]) +
 P2("Section 5 explains the pages and their colors in detail.", "La section 5 détaille les pages et leurs couleurs.") + '</div></section>')

# ------------------------------------------------------------------------------------------------ 14 installing
S.append(sec(*TOC[13]) +
 '<div class="warn">' + P2("Installing a firmware is at your own risk. The FM-1 holds one firmware at a time: Guru 600 "
    "replaces the M-VAVE one, which can be put back at any time.", "Installer un firmware se fait à vos risques. Le FM-1 "
    "ne contient qu'un firmware à la fois : Guru 600 remplace celui de M-VAVE, qu'on peut remettre à tout moment.") + '</div>' +
 P2("You install Guru 600 and send it sounds from the browser, on a Mac, a PC or Linux.", "L'installation du Guru 600 et l'envoi des sons se font dans le navigateur, sur Mac, PC ou Linux.") +
 OL([("Connect the FM-1 by USB (data cable), open the installation page in Chrome, Edge or another Chrome-based browser (Brave, Opera…), and install guru-600.fwsc. Safari cannot talk to the FM-1.",
      "Branchez le FM-1 en USB (câble de données), ouvrez la page d'installation dans Chrome, Edge ou un autre navigateur basé sur Chrome (Brave, Opera…) et installez guru-600.fwsc. Safari ne peut pas communiquer avec le FM-1."),
     ("When it restarts, the Guru 600 screen appears.", "Au redémarrage, l'écran Guru 600 apparaît.")]) +
 H3("If something goes wrong", "En cas de problème") +
 LI([("If the installer cannot start the update, put back M-VAVE's original firmware with its updater (M-UPGRADE), then install again.", "Si l'installeur n'arrive pas à lancer la mise à jour, remettez le firmware d'origine avec l'outil de mise à jour M-VAVE (M-UPGRADE), puis recommencez l'installation."),
     ("Try another USB data cable, close every app that uses MIDI, and install again.",
      "Essayez un autre câble USB de données, fermez toutes les applications qui utilisent le MIDI, et réinstallez."),
     ("If a computer sees a USB device named <b>WL80UBOOT</b>, the chip is in its boot mode and can be recovered "
      "(FM-1 Transporter, or MvaveFM1Unbricker on Windows/Linux).", "Si un ordinateur voit un périphérique USB nommé "
      "<b>WL80UBOOT</b>, la puce est en mode démarrage et peut être récupérée (FM-1 Transporter, ou MvaveFM1Unbricker "
      "sous Windows/Linux).")]) +
 P2("Back to the original: reinstall M-VAVE's firmware with its updater (M-UPGRADE).", "Retour à l'origine : réinstallez le firmware de M-VAVE avec son outil de mise à jour (M-UPGRADE).") +
 '</section>')

# ------------------------------------------------------------------------------------------------ 2 basics
S.append(sec(*TOC[1]) +
 P2("A synthesizer builds a sound in a few stages, always in the same order. Knowing these stages is all you need to "
    "understand every page of Guru 600.",
    "Un synthétiseur fabrique un son en quelques étapes, toujours dans le même ordre. Connaître ces étapes suffit pour "
    "comprendre toutes les pages de Guru 600.") +
 '<div class="chain">' + ''.join(f'<span style="--c:{c}">{T(a, b)}</span>' for a, b, c in
    [("Oscillators", "Oscillateurs", FAM["osc"]), ("Mixer", "Mixeur", FAM["osc"]), ("Filter", "Filtre", FAM["flt"]),
     ("Amplifier", "Amplificateur", FAM["env"]), ("Effects", "Effets", "#9a9486")]) + '</div>' +
 H3("1. The oscillators: the raw sound", "1. Les oscillateurs : le son brut", FAM["osc"]) +
 P2("An oscillator vibrates and makes a steady tone, like a string being bowed without stopping. Its <b>shape</b> "
    "(waveform) gives its color:", "Un oscillateur vibre et produit un son continu, comme une corde frottée sans s'arrêter. "
    "Sa <b>forme d'onde</b> lui donne sa couleur :") +
 LI([("<b>SAW</b> (sawtooth): bright and buzzy, rich in harmonics — brass, strings, leads.",
      "<b>SAW</b> (dent de scie) : brillante et nasillarde, riche en harmoniques — cuivres, cordes, leads."),
     ("<b>TRI</b> (triangle): soft and round, close to a flute.", "<b>TRI</b> (triangle) : douce et ronde, proche d'une flûte."),
     ("<b>PLS</b> (pulse): hollow and woody. Its <b>pulse width</b> changes its character: square (50 %) sounds like a "
      "clarinet, narrow sounds thin and nasal. Moving the width slowly gives the shimmering of string ensembles.",
      "<b>PLS</b> (impulsion) : creuse et boisée. Sa <b>largeur d'impulsion</b> change son caractère : carrée (50 %), elle "
      "évoque la clarinette ; étroite, elle devient fine et nasale. La faire bouger lentement donne le scintillement des "
      "ensembles de cordes.")]) +
 P2("Guru 600, like the Prophet-600, has two oscillators per voice, <b>A</b> and <b>B</b>. Each can use several shapes at once. "
    "Tuning them apart (an octave, a fifth, or just slightly) makes the sound fuller. <b>SYNC</b> forces A to restart with B: "
    "a hard, biting sound, very 80s.",
    "Guru 600, comme le Prophet-600, a deux oscillateurs par voix, <b>A</b> et <b>B</b>. Chacun peut combiner plusieurs formes d'onde. "
    "Les accorder différemment (une octave, une quinte, ou juste un peu) épaissit le son. La <b>SYNC</b> oblige A à "
    "redémarrer avec B : un son dur et mordant, très années 80.") +
 H3("2. The mixer", "2. Le mixeur", FAM["osc"]) +
 P2("The <b>MIXER</b> sets the balance between oscillator A and oscillator B.", "Le <b>MIXER</b> règle l'équilibre entre "
    "l'oscillateur A et l'oscillateur B.") +
 H3("3. The filter: the tone control", "3. Le filtre : le réglage de timbre", FAM["flt"]) +
 P2("The filter removes the high frequencies, like a very powerful treble knob. <b>CUTOFF</b> sets how bright the "
    "sound is: low, it is muffled; high, it is bright. <b>RESONANCE</b> boosts the frequencies right at the cutoff: the "
    "sound becomes nasal, then whistles. Turned very high, the filter whistles on its own — some sound effects use only that.",
    "Le filtre retire les aigus, comme un réglage de tonalité très puissant. <b>CUTOFF</b> (coupure) règle la "
    "brillance : bas, le son est étouffé ; haut, il est brillant. La <b>RESONANCE</b> renforce les fréquences proches de la "
    "coupure : le son devient nasal, puis siffle. Poussé très haut, le filtre siffle tout seul — certains effets sonores "
    "n'utilisent que cela.") +
 H3("4. The envelopes: how the sound evolves", "4. Les enveloppes : comment le son évolue", FAM["env"]) +
 P2("An envelope describes what happens from the moment you press a key until after you release it, in four steps:",
    "Une enveloppe décrit ce qui se passe entre le moment où vous appuyez sur une touche et celui où le son s'arrête, en "
    "quatre étapes :") +
 LI([("<b>ATTACK</b>: how fast the sound appears (a piano: instant; strings: slow).",
      "<b>ATTACK</b> (attaque) : la vitesse d'apparition du son (un piano : immédiate ; des cordes : lente)."),
     ("<b>DECAY</b>: how fast it then falls back.", "<b>DECAY</b> (déclin) : la vitesse à laquelle il redescend ensuite."),
     ("<b>SUSTAIN</b>: the level it holds while you keep the key down.", "<b>SUSTAIN</b> (maintien) : le niveau gardé tant "
      "que la touche reste enfoncée."),
     ("<b>RELEASE</b>: how long it takes to die away once you let go.", "<b>RELEASE</b> (relâchement) : le temps qu'il met à "
      "s'éteindre une fois la touche relâchée.")]) +
 P2("Guru 600, like the Prophet-600, has two: the <b>AMPLIFIER</b> envelope shapes the volume, the <b>FILTER ENVELOPE</b> opens and closes "
    "the filter — the 'wah' of a brass attack, the 'pluck' of a clavinet.",
    "Guru 600, comme le Prophet-600, en a deux : l'enveloppe d'<b>AMPLIFIER</b> façonne le volume, la <b>FILTER ENVELOPE</b> ouvre et ferme "
    "le filtre — le « wah » d'une attaque de cuivre, le « pincé » d'un clavinet.") +
 H3("5. The LFO: movement", "5. Le LFO : le mouvement", FAM["lfo"]) +
 P2("The LFO (low-frequency oscillator) is a slow, inaudible wave that moves another setting up and down: the pitch "
    "(<b>vibrato</b>), the filter (<b>wah-wah</b>), the pulse width (shimmer) or the volume (<b>tremolo</b>).",
    "Le LFO (oscillateur basse fréquence) est une onde lente, inaudible, qui fait bouger un autre réglage : la hauteur "
    "(<b>vibrato</b>), le filtre (<b>wah-wah</b>), la largeur d'impulsion (scintillement) ou le volume (<b>trémolo</b>).") +
 H3("6. Poly-Mod: the Prophet's signature", "6. La Poly-Mod : la signature du Prophet", FAM["pm"]) +
 P2("<b>POLY-MOD</b> lets the filter envelope or oscillator B shape oscillator A's pitch or the filter, inside each voice. "
    "Small amounts add bite; larger amounts make bells, metallic sounds, sweeps and sound effects that ordinary "
    "synthesizers cannot do.",
    "La <b>POLY-MOD</b> permet à l'enveloppe du filtre ou à l'oscillateur B de modeler la hauteur de l'oscillateur A ou le "
    "filtre, dans chaque voix. Un peu ajoute du mordant ; beaucoup donne des cloches, des sons métalliques, des balayages "
    "et des effets qu'un synthétiseur ordinaire ne sait pas faire.") +
 H3("7. Voices, unison and glide", "7. Voix, unisson et glide", FAM["vce"]) +
 P2("Six <b>voices</b> mean six notes at once. <b>UNISON</b> stacks all the voices on one note for a huge single-note "
    "sound (basses, leads). <b>GLIDE</b> slides from one note to the next instead of jumping.",
    "Six <b>voix</b>, c'est six notes en même temps. L'<b>UNISON</b> empile toutes les voix sur une seule note pour un son "
    "énorme (basses, leads). Le <b>GLIDE</b> fait glisser d'une note à l'autre au lieu de sauter.") +
 H3("8. Effects", "8. Les effets", "#9a9486") +
 LI([("<b>REV</b> (reverb): the sound of a room or a hall around the instrument.", "<b>REV</b> (réverbération) : le son "
      "d'une pièce ou d'une salle autour de l'instrument."),
     ("<b>DLY</b> (delay): echoes that repeat the sound.", "<b>DLY</b> (délai) : des échos qui répètent le son."),
     ("<b>CHO</b> (chorus): a slightly doubled, wider sound.", "<b>CHO</b> (chorus) : un son légèrement doublé, plus large."),
     ("<b>DST</b> (distortion): saturates the sound, from warm to aggressive.", "<b>DST</b> (distorsion) : sature le son, "
      "du chaud à l'agressif.")]) + '</section>')

# ------------------------------------------------------------------------------------------------ 3 first steps
S.append(sec(*TOC[2]) +
 P2("Switch the FM-1 on. The Guru 600 screen plays for about six seconds, then the controls appear. Track 1 is "
    "ready with the Prophet-600's first factory sound, <b>1 ORGAN I</b>: play the keys.",
    "Allumez le FM-1. L'écran Guru 600 s'anime pendant environ six secondes, puis les commandes apparaissent. La "
    "piste 1 est prête avec le premier son d'usine du Prophet-600, <b>1 ORGAN I</b> : jouez sur les touches.") +
 '<div class="split">' + shot("shots/home.png", "The HOME page.", "La page HOME.", 240) + '<div>' +
 OL([("Turn <b>PRESETS</b> to change the sound. Sounds 1 to 100 are the Prophet-600's factory sounds, 101 to 200 the free collection, 201 to 255 the Guru-600's own.", "Tournez <b>PRESETS</b> pour changer de son. Les sons 1 à 100 sont ceux d'usine du Prophet-600, 101 à 200 la collection libre, 201 à 255 ceux du Guru-600."),
     ("Turn <b>KNOB 1 to 4</b> to shape the sound: on HOME they are CUTOFF, RESONANCE, the filter envelope amount "
      "and the mixer.", "Tournez <b>KNOB 1 à 4</b> pour modeler le son : sur HOME ce sont la coupure, la résonance, "
      "la quantité d'enveloppe du filtre et le mixeur."),
     ("Press <b>EDIT</b> to reach every Guru 600 control, page by page (section 6).",
      "Appuyez sur <b>EDIT</b> pour atteindre toutes les commandes de Guru 600, page par page (section 6)."),
     ("<b>OCT−</b> and <b>OCT+</b> move the keyboard down or up an octave; both together: back to the middle.",
      "<b>OCT−</b> et <b>OCT+</b> descendent ou montent le clavier d'une octave ; les deux ensemble : retour au milieu.")]) +
 '</div></div>' +
 '<div class="note">' + P2("Your changes are not lost when you switch off: the FM-1 starts again with the music and "
    "sounds as you left them (MENU › RESTORE LAST). But a sound you changed is not <i>saved</i> until you store it in a "
    "user place (section 9).", "Vos réglages ne sont pas perdus à l'extinction : le FM-1 redémarre avec la musique et "
    "les sons tels que vous les avez laissés (MENU › RESTORE LAST). Mais un son modifié n'est pas <i>enregistré</i> tant "
    "que vous ne l'avez pas rangé dans un emplacement utilisateur (section 9).") + '</div></section>')

# ------------------------------------------------------------------------------------------------ 4 controls
CTL = [("1", "MASTER", "Overall volume.", "Volume général."),
       ("2", "SELECT", "Tempo (BPM) by default; can step the pages or play the mod wheel (MENU › CONTROL › SELECT).", "Le tempo (BPM) par défaut ; peut faire défiler les pages ou servir de molette de modulation (MENU › CONTROL › SELECT)."),
       ("3", "PRESETS", "Changes the sound of the selected track.", "Change le son de la piste choisie."),
       ("4", "ALGORITHM", "Selects the track (1 to 4).", "Choisit la piste (1 à 4)."),
       ("5", "OCT− / OCT+", "Octave down / up; on dialogs: back / confirm.", "Octave en bas / en haut ; dans les dialogues : retour / confirmer."),
       ("6", "KNOB 1–4", "The four settings shown on the screen.", "Les quatre réglages affichés à l'écran."),
       ("7", "FX", "Effects pages; held: the FX performance layer.", "Pages des effets ; maintenu : le calque d'effets en jeu."),
       ("8", "SCL", "Scale and chord keys; held: its layer.", "Gammes et accords ; maintenu : son calque."),
       ("9", "ENV", "The amplifier envelope.", "L'enveloppe d'amplitude."),
       ("10", "LFO", "LFO pages and the modulation matrix.", "Pages du LFO et matrice de modulation."),
       ("11", "EDIT", "The sound engine's pages (all the Guru 600 controls); held: the EDIT layer.", "Les pages du moteur sonore (toutes les commandes de Guru 600) ; maintenu : le calque EDIT."),
       ("12", "GLO", "Song; held: mutes, levels, tap tempo.", "Morceau ; maintenu : sourdines, niveaux, tempo tapé."),
       ("13", "HOME", "Back to HOME; held: the menu.", "Retour à HOME ; maintenu : le menu."),
       ("14", "SAVE", "Save sounds and projects; held: undo.", "Enregistrer sons et projets ; maintenu : annuler."),
       ("15", "ARP", "The arpeggiator.", "L'arpégiateur."),
       ("16", "SEQ", "The step sequencer; held: its tools.", "Le séquenceur pas à pas ; maintenu : ses outils."),
       ("17", "PLAY", "Starts / stops the sequencer.", "Lance / arrête le séquenceur."),
       ("18", "REC", "Arms recording; held: its layer.", "Arme l'enregistrement ; maintenu : son calque."),
       ("19", "KEYS", "The 25 keys: play, or shortcuts in a layer.", "Les 25 touches : jouer, ou raccourcis dans un calque."),
       ("20", ("SCREEN", "ÉCRAN"), "The screen: the page shown, its four settings, the sound and the track.", "L'écran : la page affichée, ses quatre réglages, le son et la piste.")]
S.append(sec(*TOC[3]) + '<figure class="wide"><img src="img/facade_reperes.png" alt=""></figure>' +
 table([("No.", "N°"), ("Control", "Commande"), ("What it does", "Rôle")], [[a, f"<b>{b}</b>" if isinstance(b, str) else T(f"<b>{b[0]}</b>", f"<b>{b[1]}</b>"), (c, d)] for a, b, c, d in CTL]) +
 P2("The <b>USB</b> socket, on the back, gives power, MIDI and audio, and receives imported sounds.", "La prise <b>USB</b>, à l'arrière, assure l'alimentation, le MIDI et l'audio, et reçoit les sons importés.") +
 P2("Page buttons act when you <b>let go</b>. Holding FX, GLO, SCL, EDIT, REC or SEQ opens a <b>quick layer</b>: "
    "shortcuts on the keys and knobs, shown on the screen, for as long as you hold it.",
    "Les boutons de page agissent quand on les <b>relâche</b>. Maintenir FX, GLO, SCL, EDIT, REC ou SEQ ouvre un "
    "<b>calque rapide</b> : des raccourcis sur les touches et les boutons, affichés à l'écran, tant qu'on le maintient.") +
 '</section>')

# ------------------------------------------------------------------------------------------------ 5 navigation
S.append(sec(*TOC[4]) +
 P2("Each button opens a <b>family</b> of pages. Its first press shows the family's page you saw last; each new press "
    "shows the next one. The bottom line of the screen gives the page's name and its number, for example "
    "<b>FILTER 5/10</b>.",
    "Chaque bouton ouvre une <b>famille</b> de pages. Le premier appui montre la dernière page vue de cette famille ; "
    "chaque nouvel appui montre la suivante. La ligne du bas de l'écran donne le nom de la page et son numéro, par "
    "exemple <b>FILTER 5/10</b>.") +
 '<div class="key">' + H3("Going back a page", "Revenir à la page précédente") +
 LI([("<b>One press</b> on a page button: the next page (it appears after a third of a second).", "<b>Un appui</b> sur un bouton de page : la page suivante (elle apparaît après un tiers de seconde)."),
     ("<b>Two quick presses</b> on the same button: the page before. The next page is not shown in between.", "<b>Deux appuis rapides</b> sur le même bouton : la page précédente. La page suivante ne s'affiche pas entre les deux."),
     ("It works on every page button: HOME, SAVE, ENV, LFO, FX, SCL, EDIT, ARP and SEQ. For example, on EDIT, two quick presses lead from FILTER 5/10 back to MIXER 4/10.", "Cela marche sur tous les boutons de page : HOME, SAVE, ENV, LFO, FX, SCL, EDIT, ARP et SEQ. Par exemple, sur EDIT, deux appuis rapides ramènent de FILTER 5/10 à MIXER 4/10."),
     ("From the first page, going back leads to the last one, and from the last, forward leads to the first.",
      "Depuis la première page, reculer mène à la dernière ; depuis la dernière, avancer mène à la première."),
     ("To move forward several pages, leave a short pause between presses, or they count as a double press.",
      "Pour avancer de plusieurs pages, laissez une courte pause entre les appuis, sinon ils comptent comme un double appui.")]) +
 P2("Another way, for every family: MENU › CONTROL › <b>SELECT = PAGE</b>. The SELECT knob then steps through the "
    "pages, forward to the right and back to the left (the tempo moves to GLO + SELECT).",
    "Autre solution, pour toutes les familles : MENU › CONTROL › <b>SELECT = PAGE</b>. Le bouton SELECT fait alors "
    "défiler les pages, en avant vers la droite et en arrière vers la gauche (le tempo passe à GLO + SELECT).") +
 P2("Unlike the original Felucca, a double press no longer locks a quick layer open (except GLO, which has a single page): holding the button still opens it.", "Contrairement à Felucca d'origine, un double appui ne verrouille plus un calque rapide (sauf GLO, qui n'a qu'une page) : maintenir le bouton l'ouvre toujours.") + '</div>' +
 H3("The colors of the Guru 600 pages", "Les couleurs des pages de Guru 600") +
 P2("Each family of controls has its own color, on the frame and on the knobs' arcs:",
    "Chaque famille de commandes a sa couleur, sur le cadre et sur les arcs des boutons :") +
 '<div class="chips">' + ''.join(f'<span style="--c:{FAM[k]}">{T(a, b)}</span>' for k, a, b in
    [("osc", "Oscillators, mixer", "Oscillateurs, mixeur"), ("flt", "Filter", "Filtre"),
     ("env", "Envelopes", "Enveloppes"), ("pm", "Poly-Mod", "Poly-Mod"), ("lfo", "LFO", "LFO"),
     ("vce", "Voices", "Voix"), ("ext", "Extras (Guru 600)", "Extras (Guru 600)")]) + '</div>' +
 P2("A knob's lit arc shows its value; on a two-way setting (−/+) the arc starts from the middle.",
    "L'arc lumineux d'un bouton montre sa valeur ; sur un réglage à deux sens (−/+), l'arc part du milieu.") +
 '</section>')

# ------------------------------------------------------------------------------------------------ 6 P600 pages
WAVES_EN = "OFF, SAW, TRI, SAW+T, PLS, SAW+P, TRI+P, ALL (all three)"
WAVES_FR = "OFF, SAW, TRI, SAW+T, PLS, SAW+P, TRI+P, ALL (les trois)"
S.append(sec(*TOC[5]) +
 P2("Press EDIT: ten pages, in the order of the Prophet-600's panel, left to right. The four knobs under the screen "
    "turn the four controls shown.", "Appuyez sur EDIT : dix pages, dans l'ordre de la façade du Prophet-600, de gauche "
    "à droite. Les quatre boutons sous l'écran règlent les quatre commandes affichées.") +
 page("pm", "shots/edit1.png", "1/10 · POLY-MOD", "1/10 · POLY-MOD",
      "Two sources inside each voice modulate oscillator A's pitch and/or the filter.",
      "Deux sources, dans chaque voix, modulent la hauteur de l'oscillateur A et/ou le filtre.",
      [("FIL ENV", "How much the filter envelope modulates the destination.", "Quantité de modulation par l'enveloppe du filtre.", "0–100 %", "0–100 %"),
       ("OSC B", "How much oscillator B modulates the destination (metallic, bell-like).", "Quantité de modulation par l'oscillateur B (métallique, cloches).", "0–100 %", "0–100 %"),
       ("DEST", "Where it goes: OFF, FRQ A (osc A pitch), FILT (filter), BOTH.", "Destination : OFF, FRQ A (hauteur de l'osc A), FILT (filtre), BOTH (les deux).", "4 choices", "4 choix")],
      "The POLY-MOD page.", "La page POLY-MOD.") +
 page("osc", "shots/edit2.png", "2/10 · OSCILLATORS", "2/10 · OSCILLATORS",
      "The shapes and pitches of oscillators A and B.", "Les formes d'onde et hauteurs des oscillateurs A et B.",
      [("SHAPE A", "Oscillator A's waveforms: " + WAVES_EN + ".", "Formes d'onde de l'oscillateur A : " + WAVES_FR + ".", "8 choices", "8 choix"),
       ("FREQ A", "Oscillator A's pitch, in semitones.", "Hauteur de l'oscillateur A, en demi-tons.", "semitones", "demi-tons"),
       ("SHAPE B", "Oscillator B's waveforms.", "Formes d'onde de l'oscillateur B.", "8 choices", "8 choix"),
       ("FREQ B", "Oscillator B's pitch, in semitones.", "Hauteur de l'oscillateur B, en demi-tons.", "semitones", "demi-tons")],
      "The OSCILLATORS page.", "La page OSCILLATORS.") +
 page("osc", "shots/edit3.png", "3/10 · OSCILLATORS 2", "3/10 · OSCILLATORS 2",
      "Pulse widths, fine tuning and sync.", "Largeurs d'impulsion, accord fin et synchronisation.",
      [("PW A", "Pulse width of A (used when its shape includes PLS).", "Largeur d'impulsion de A (quand sa forme contient PLS).", "0–100 %", "0–100 %"),
       ("PW B", "Pulse width of B.", "Largeur d'impulsion de B.", "0–100 %", "0–100 %"),
       ("FINE B", "Detunes B slightly, up to a semitone: a fuller, beating sound.", "Désaccorde légèrement B, jusqu'à un demi-ton : un son plus épais, qui bat.", "0–127", "0–127"),
       ("SYNC", "A restarts with B: a hard, biting tone.", "A redémarre avec B : un son dur et mordant.", "OFF / ON", "OFF / ON")],
      "The OSCILLATORS 2 page.", "La page OSCILLATORS 2.") +
 page("osc", "shots/edit4.png", "4/10 · MIXER GLIDE UNISON", "4/10 · MIXER GLIDE UNISON",
      "The balance of the two oscillators, the glide and the voice mode.", "L'équilibre des deux oscillateurs, le glide et le mode de voix.",
      [("MIXER", "0 % only A, 100 % only B.", "0 % seulement A, 100 % seulement B.", "0–100 %", "0–100 %"),
       ("GLIDE", "Slide time between notes.", "Temps de glissement entre les notes.", "time", "durée"),
       ("VOICES", "POLY (six notes), MONO, LEG (legato) or UNI (unison: all voices on one note).", "POLY (six notes), MONO, LEG (legato) ou UNI (unisson : toutes les voix sur une note).", "modes", "modes")],
      "The MIXER page.", "La page MIXER.") +
 page("flt", "shots/edit5.png", "5/10 · FILTER", "5/10 · FILTER",
      "The 24 dB low-pass filter.", "Le filtre passe-bas 24 dB.",
      [("CUTOFF", "Brightness (in Hz).", "Brillance (en Hz).", "Hz", "Hz"),
       ("RES", "Resonance; past about 70 % the filter whistles on its own.", "Résonance ; au-delà d'environ 70 %, le filtre siffle tout seul.", "0–100 %", "0–100 %"),
       ("ENV AMT", "How much the filter envelope opens the filter.", "Quantité d'ouverture du filtre par son enveloppe.", "0–100 %", "0–100 %"),
       ("KBD", "Keyboard tracking: higher notes open the filter (OFF, HALF, FULL).", "Suivi de clavier : les notes aiguës ouvrent le filtre (OFF, HALF, FULL).", "3 choices", "3 choix")],
      "The FILTER page.", "La page FILTER.") +
 page("env", "shots/edit6.png", "6/10 · FILTER ENVELOPE", "6/10 · FILTER ENVELOPE",
      "The filter's own envelope (section 2).", "L'enveloppe propre au filtre (section 2).",
      [("ATTACK", "Time to open.", "Temps d'ouverture.", "1 ms – 10 s", "1 ms – 10 s"),
       ("DECAY", "Time to fall to the sustain level.", "Temps de descente vers le maintien.", "time", "durée"),
       ("SUSTAIN", "Level held while the key is down.", "Niveau tenu tant que la touche est enfoncée.", "0–100 %", "0–100 %"),
       ("RELEASE", "Time to close after the key is let go.", "Temps de fermeture après relâchement.", "time", "durée")],
      "The FILTER ENVELOPE page.", "La page FILTER ENVELOPE.") +
 page("ext", "shots/edit7.png", "7/10 · EXTRAS", "7/10 · EXTRAS",
      "Guru 600's additions, set by each sound.", "Les ajouts de Guru 600, réglés par chaque son.",
      [("VINTAGE", "Slight random drift of each voice, like an old analog synth.", "Légère dérive aléatoire de chaque voix, comme un vieux synthé analogique.", "0–100 %", "0–100 %"),
       ("WHEEL", "How much the mod wheel brings in the sound's modulation (section 12).", "Quantité de modulation apportée par la molette (section 12).", "−100 / +100 %", "−100 / +100 %"),
       ("VEL>FLT", "Playing harder opens the filter (velocity).", "Jouer plus fort ouvre le filtre (vélocité).", "0–100 %", "0–100 %"),
       ("DETUNE", "Spread of the voices in UNISON.", "Écart des voix en UNISON.", "0–127", "0–127")],
      "The EXTRAS page.", "La page EXTRAS.") +
 page("vce", "shots/edit8.png", "8/10 · VOICE", "8/10 · VOICE",
      "Felucca's voice page, for every engine.", "La page de voix de Felucca, commune à tous les moteurs.",
      [("VOICES", "The voice mode, as on the MIXER page.", "Le mode de voix, comme sur la page MIXER.", "modes", "modes"),
       ("GLIDE", "The glide time.", "Le temps de glide.", "time", "durée"),
       ("GLMOD", "How the glide is timed: RATE or TIME.", "Le mode de calcul du glide : RATE ou TIME.", "2 choices", "2 choix"),
       ("PRIO", "In MONO, which note wins: LAST, LOW or HIGH.", "En MONO, la note prioritaire : LAST, LOW ou HIGH.", "3 choices", "3 choix")],
      "The VOICE page.", "La page VOICE.") +
 page("vce", "shots/edit9.png", "9/10 · VOICE 2", "9/10 · VOICE 2",
      "Voice allocation, unison detune, panning and mute.", "Répartition des voix, désaccord d'unisson, panoramique et sourdine.",
      [("ALLOC", "How new notes take voices: ROT (in turn) or REUSE.", "Attribution des voix aux notes : ROT (à tour de rôle) ou REUSE.", "2 choices", "2 choix"),
       ("DETUNE", "Unison detune (same as EXTRAS).", "Désaccord d'unisson (comme EXTRAS).", "0–127", "0–127"),
       ("PAN", "Left / right position of the track.", "Position gauche / droite de la piste.", "−/+", "−/+"),
       ("MUTE", "Silences the track.", "Coupe le son de la piste.", "OFF / ON", "OFF / ON")],
      "The VOICE 2 page.", "La page VOICE 2.") +
 page("vce", "shots/edit10.png", "10/10 · VOICE 3", "10/10 · VOICE 3",
      "Stereo spread.", "Étalement stéréo.",
      [("SPRD", "The voices alternate left and right of the track's PAN.", "Les voix alternent à gauche et à droite du PAN de la piste.", "0–100 %", "0–100 %")],
      "The VOICE 3 page.", "La page VOICE 3.") +
 H3("The amplifier envelope and the LFO", "L'enveloppe d'amplitude et le LFO", FAM["env"]) +
 P2("In Guru 600, the <b>AMPLIFIER</b> envelope is on the <b>ENV</b> button, and the <b>LFO</b> on the LFO button. "
    "Felucca's LFO pages are richer than the original: rate or tempo sync, several waves, destinations.",
    "Dans Guru 600, l'enveloppe <b>AMPLIFIER</b> est sur le bouton <b>ENV</b>, et le <b>LFO</b> sur le bouton LFO. "
    "Les pages LFO de Felucca sont plus riches que l'original : vitesse ou synchro au tempo, plusieurs formes, destinations.") +
 '<div class="grid">' + shot("shots/env1.png", "ENV: ATTACK, DECAY, SUSTAIN, RELEASE.", "ENV : ATTACK, DECAY, SUSTAIN, RELEASE.", 200) +
 shot("shots/lfo1.png", "LFO: RATE, WAVE, PHASE, FADE.", "LFO : RATE, WAVE, PHS, FADE.", 200) +
 shot("shots/lfo3.png", "LFO DEST: pitch, filter, pulse width (SHP), volume.", "LFO DEST : hauteur, filtre, largeur d'impulsion (SHP), volume.", 200) +
 shot("shots/lfo4.png", "MOD: the modulation matrix (slot 4 = mod wheel).", "MOD : la matrice de modulation (emplacement 4 = molette).", 200) + '</div>' +
 H3("The animated screens", "Les écrans animés") +
 P2("The panel under the four cards is drawn from the sound itself: what comes out, left and right, its level, its frequencies, and the notes you play. Each screen has its own animation, chosen for what the page sets; there is nothing to switch on.",
    "Le panneau sous les quatre cartes est dessiné à partir du son lui-même : ce qui sort, à gauche et à droite, son volume, ses fréquences, et les notes que vous jouez. Chaque écran a son animation, choisie pour ce que la page règle ; il n'y a rien à activer.") +
 '<div class="grid">' +
 shot("shots/home.png", "HOME: the spectrum as bars round a disc, lows at the back, highs at the front; the left half is the left channel, the right half the right one.",
      "HOME : le spectre en barres autour d'un disque, graves au fond, aigus devant ; la moitié gauche est le canal gauche, la droite le canal droit.", 200) +
 shot("shots/style_cell.png", "REVERB: a shape, round when the sound is dark, square when it is bright, spikes on each note; it divides in stereo and glows with the reverb.",
      "REVERB : une forme ronde quand le son est sombre, carrée quand il est brillant, des pointes à chaque note ; elle se divise en stéréo et rayonne avec la réverbération.", 200) +
 shot("shots/style_walls.png", "CHORUS: the left and right waves as two walls; one in mono, they part as the sound gets wider and louder.",
      "CHORUS : les ondes gauche et droite en deux murs ; un seul en mono, ils s'écartent quand le son s'élargit et monte.", 200) +
 shot("shots/style_tunnel.png", "DLY: each waveform becomes a ring flying toward you, like echoes.",
      "DLY : chaque forme d'onde devient un anneau qui fonce vers vous, comme des échos.", 200) +
 shot("shots/style_sparks.png", "ARP 2: the keyboard bent into a circle; each note throws sparks from its side, blue and slow in the bass, red and fast in the treble.",
      "ARP 2 : le clavier courbé en cercle ; chaque note lance des étincelles de son côté, bleues et lentes dans les graves, rouges et rapides dans les aigus.", 200) +
 shot("shots/style_waves.png", "ENV DEST: the last waveforms piled up in depth.",
      "ENV DEST : les dernières formes d'onde empilées en profondeur.", 200) +
 shot("shots/style_flower.png", "CLOCK: the waveform wound into a flower, with more petals when the sound is brighter.",
      "CLOCK : la forme d'onde enroulée en fleur, avec plus de pétales quand le son est brillant.", 200) +
 shot("shots/style_blocks.png", "ARP: the spectrum in blocks; each new row pushes the older ones back.",
      "ARP : le spectre en blocs ; chaque nouvelle rangée repousse les précédentes vers le fond.", 200) +
 shot("shots/style_cascade.png", "OSCILLATORS and OSCILLATORS 2: the waveform as it comes out, the previous ones falling back in a cascade.",
      "OSCILLATORS et OSCILLATORS 2 : la forme d'onde qui sort, les précédentes reculant en cascade.", 200) +
 shot("shots/style_ribbon.png", "POLY-MOD: the envelope that drives the modulation, as a ribbon in depth.",
      "POLY-MOD : l'enveloppe qui pilote la modulation, en ruban dans la profondeur.", 200) +
 shot("shots/style_helix.png", "LFO 2: the LFO wave wound into a helix.",
      "LFO 2 : l'onde du LFO enroulée en hélice.", 200) +
 shot("shots/style_tracks.png", "MIXER: the four tracks, each with its sound and its level.",
      "MIXER : les quatre pistes, chacune avec son son et son niveau.", 200) +
 '</div>' +
 P2("The sound pages have theirs too: <b>ENV</b> the real envelope of the sound (its level over the last seconds) with "
    "a light at the present; <b>FLT ENV</b> a plate of columns where the spectrum spreads from the center; <b>LFO</b> "
    "a ring the LFO wave deforms; <b>FILTER</b> the spectrum as a landscape, warm below the cutoff and cold above, with "
    "a wall of light at the cutoff that shines brighter with the resonance.",
    "Les pages du son ont aussi la leur : <b>ENV</b> l'enveloppe réelle du son (son volume des dernières secondes) avec "
    "une lumière au présent ; <b>FLT ENV</b> un plateau de colonnes où le spectre se propage depuis le centre ; "
    "<b>LFO</b> un anneau que l'onde du LFO déforme ; <b>FILTER</b> le spectre en paysage, chaud sous la coupure et "
    "froid au-dessus, avec un mur de lumière à la coupure qui brille davantage avec la résonance.") +
 '</section>')

# ------------------------------------------------------------------------------------------------ 7 Felucca pages
S.append(sec(*TOC[6]) +
 P2("Everything below comes from Felucca and works with the P600 engine as with the others.",
    "Tout ce qui suit vient de Felucca et fonctionne avec le moteur P600 comme avec les autres.") +
 '<div class="grid">' +
 shot("shots/fx1.png", "<b>FX</b>: distortion, chorus, delay and reverb sends; INSERT effects. Held: performance effects on the keys.",
      "<b>FX</b> : distorsion, envois chorus, délai et réverbération ; effets INSERT. Maintenu : effets de jeu sur les touches.", 200) +
 shot("shots/scl1.png", "<b>SCL</b>: the scale, and chord keys (one finger plays a chord).",
      "<b>SCL</b> : la gamme, et les accords (un doigt joue un accord).", 200) +
 shot("shots/arp1.png", "<b>ARP</b>: the arpeggiator: MODE, RATE, octaves, GATE.",
      "<b>ARP</b> : l'arpégiateur : MODE, RATE, octaves, GATE.", 200) +
 shot("shots/seq1.png", "<b>SEQ</b>: the 64-step sequencer per track; held: its tools (CLEAR, RANDOM, EUCLID…).",
      "<b>SEQ</b> : le séquenceur de 64 pas par piste ; maintenu : ses outils (CLEAR, RANDOM, EUCLID…).", 200) +
 shot("shots/glo1.png", "<b>GLO</b>: the song (up to 16 sections); held: mutes, levels, tap tempo.",
      "<b>GLO</b> : le morceau (jusqu'à 16 sections) ; maintenu : sourdines, niveaux, tempo tapé.", 200) +
 shot("shots/menu.png", "<b>MENU</b> (hold HOME): display, controls, audio, MIDI, system.",
      "<b>MENU</b> (maintenir HOME) : affichage, commandes, audio, MIDI, système.", 200) +
 shot("shots/layer_edit.png", "<b>EDIT held</b>: the engine on the keys. Careful: a key changes the track's engine.",
      "<b>EDIT maintenu</b> : le moteur sur les touches. Attention : une touche change le moteur de la piste.", 200) +
 shot("shots/lfo4.png", "<b>MOD</b> (LFO, 4th page): 4 modulation slots per track.",
      "<b>MOD</b> (LFO, 4e page) : 4 emplacements de modulation par piste.", 200) + '</div>' +
 H3("Four tracks", "Quatre pistes") +
 P2("The FM-1 plays four tracks at once, each with its own engine and sound. <b>ALGORITHM</b> selects the track; its "
    "number is at the top left of the screen. The P600 engine can be used on several tracks; the voices are shared.",
    "Le FM-1 joue quatre pistes à la fois, chacune avec son moteur et son son. <b>ALGORITHM</b> choisit la piste ; son "
    "numéro est en haut à gauche de l'écran. Le moteur P600 peut servir sur plusieurs pistes ; les voix sont partagées.") +
 '</section>')

# ------------------------------------------------------------------------------------------------ 8 the sounds
S.append(sec(*TOC[7]) +
 P2("Turn <b>PRESETS</b>: the P600 sounds come first. The screen shows the place number and the name; the name is "
    "shortened when it is long. Any place can take a sound you save or import (section 10).",
    "Tournez <b>PRESETS</b> : les sons P600 viennent en premier. L'écran affiche le numéro de place et le nom, abrégé "
    "s'il est long. N'importe quelle place peut recevoir un son enregistré ou importé (section 10).") +
 P2("On the <b>SAVE › PRESETS</b> page, <b>KNOB 4 (LIST)</b> shows only one family: BASS, LEAD, PAD, PLUCK (plucked sounds and bells), KEYS, DRUM or FX. Every P600 sound belongs to one.",
    "Sur la page <b>SAVE › PRESETS</b>, le <b>bouton 4 (LIST)</b> n'affiche qu'une famille : BASS, LEAD, PAD, PLUCK (sons pincés et cloches), KEYS, DRUM ou FX. Chaque son P600 appartient à l'une d'elles.") +
 '<div class="split">' + shot("shots/presets_turn.png", "Changing sound with PRESETS.", "Changer de son avec PRESETS.", 220) +
 shot("shots/save_presets.png", "SAVE › PRESETS: the whole list.", "SAVE › PRESETS : toute la liste.", 220) + '</div>' +
 H3("1–100: the Prophet-600 factory sounds", "1–100 : les sons d'usine du Prophet-600") +
 P2("The 100 programs Sequential Circuits put in the Prophet-600 in 1982, with the names and advice of the original "
    "owner's manual: what the mod wheel adds to each sound, and tips to play or change it.",
    "Les 100 programmes installés par Sequential Circuits dans le Prophet-600 en 1982, avec les noms et conseils du "
    "manuel d'origine : ce que la molette de modulation ajoute à chaque son, et des astuces pour le jouer ou le modifier.") +
 H3("101–200: the free v2022 collection", "101–200 : la collection libre v2022") +
 P2("100 sounds made by Prophet-600 owners for the GliGli firmware and shared under the GPL license, with their "
    "family, author and remarks.", "100 sons créés par des propriétaires de Prophet-600 pour le firmware GliGli et "
    "partagés sous licence GPL, avec leur famille, leur auteur et leurs remarques.") +
 H3("201–255: the Guru-600's own sounds", "201–255 : les sons du Guru-600") +
 P2("55 sounds made for the Guru-600, chosen to differ from the 200 above: 30 adapted from the factory sounds of Surge XT, a free synthesizer (GPL-3 license, sounds by Claes Johanson), and 25 originals: bells, gong, sync scream, filter percussion, sound effects, random sequences, slow pads.", "55 sons faits pour le Guru-600, choisis pour être différents des 200 précédents : 30 adaptés des sons d'usine de Surge XT, un synthétiseur libre (licence GPL-3, sons de Claes Johanson), et 25 originaux : cloches, gong, cri de synchro, percussions au filtre, bruitages, séquences aléatoires, nappes lentes.") +
 '<div class="note">' + P2("The complete list of the 255 sounds is in the <b>appendix</b>, at the end of this guide.", "La liste complète des 255 sons est en <b>annexe</b>, à la fin de cette notice.") + '</div></section>')

# ------------------------------------------------------------------------------------------------ 9 keeping sounds
S.append(sec(*TOC[8]) +
 '<div class="key">' + P2("<b>The essentials.</b> Guru-600 has two separate kinds of places for sounds:", "<b>L'essentiel.</b> Le Guru-600 a deux sortes de places distinctes pour les sons :") +
 table([("", ""), ("32 USER places", "32 emplacements USER"), ("55 P600 places", "55 places P600")], [
   [("What goes in", "Ce qu'on y met"), ("A sound you changed on the FM-1, any engine", "Un son modifié sur le FM-1, de n'importe quel moteur"),
    ("A P600 sound saved in its place on the FM-1, or sent from a computer (.syx)", "Un son P600 enregistré à sa place sur le FM-1, ou envoyé depuis un ordinateur (.syx)")],
   [("Where", "Où"), ("SAVE › USER (U01 to U32), and at the end of the PRESETS list", "SAVE › USER (U01 à U32), et à la fin de la liste PRESETS"),
    ("PRESETS 1 to 255, in place of the built-in sound", "PRESETS 1 à 255, à la place du son intégré")],
   [("Kept after power-off", "Gardé après extinction"), ("Yes", "Oui"), ("Yes, until the reset", "Oui, jusqu'à la réinitialisation")]]) + '</div>' +
 H3("Changing a sound and getting the original back", "Modifier un son et retrouver l'original") +
 P2("Turn any knob: the sound changes at once, but the built-in sound itself is not changed. To get the original back, "
    "turn <b>PRESETS</b> one step and back again: the sound reloads as it was.",
    "Tournez n'importe quel bouton : le son change aussitôt, mais le son intégré lui-même n'est pas modifié. Pour "
    "retrouver l'original, tournez <b>PRESETS</b> d'un cran puis revenez : le son se recharge tel qu'il était.") +
 H3("Saving a P600 sound in its own place", "Enregistrer un son P600 à sa place") +
 '<div class="split">' + shot("shots/save_place.png", "SAVE › PLACE.", "SAVE › PLACE.", 220) + '<div>' +
 OL([("Stop the sequencer (PLAY).", "Arrêtez le séquenceur (PLAY)."),
     ("Press <b>SAVE</b> twice: the PLACE page opens, on the sound's own place.", "Appuyez deux fois sur <b>SAVE</b> : la page PLACE s'ouvre, sur la place du son."),
     ("To save it elsewhere, choose another place (1 to 255) with <b>KNOB 1</b>.", "Pour l'enregistrer ailleurs, choisissez une autre place (1 à 255) avec <b>KNOB 1</b>."),
     ("Press <b>OCT+</b>, then <b>OCT+</b> again to confirm. The sound replaces the one in that place and keeps its name.", "Appuyez sur <b>OCT+</b>, puis de nouveau sur <b>OCT+</b> pour confirmer. Le son remplace celui de cette place et garde son nom.")]) +
 P2("To get a place's original sound back: on PLACE, choose the place, turn <b>KNOB 3</b> (ORIG), then press <b>OCT+</b> twice. Places holding a saved or imported sound show in color in the list.", "Pour retrouver le son d'origine d'une place : sur PLACE, choisissez la place, tournez <b>KNOB 3</b> (ORIG), puis appuyez deux fois sur <b>OCT+</b>. Les places qui contiennent un son enregistré ou importé apparaissent en couleur dans la liste.") +
 '</div></div>' +
 '<div class="note">' + P2("The 55 P600 places are shared by the sounds saved on the FM-1 and the sounds sent from a computer. The reset (section 12) brings back every original sound and forgets both. Saved with the sound: the oscillators, filter, envelopes, Poly-Mod, LFO, glide, unison and the EXTRAS except VINTAGE.", "Les 55 places P600 sont partagées entre les sons enregistrés sur le FM-1 et les sons envoyés depuis un ordinateur. La réinitialisation (section 12) ramène tous les sons d'origine et oublie les uns comme les autres. Sont enregistrés avec le son : les oscillateurs, le filtre, les enveloppes, la Poly-Mod, le LFO, le glide, l'unisson et les EXTRAS sauf VINTAGE.") + '</div>' +
 H3("Saving a sound in the 32 USER places", "Enregistrer un son dans les 32 emplacements USER") +
 '<div class="split">' + shot("shots/save_user.png", "SAVE › USER.", "SAVE › USER.", 220) + '<div>' +
 OL([("Stop the sequencer (PLAY).", "Arrêtez le séquenceur (PLAY)."),
     ("Press <b>SAVE</b>: the USER page opens.", "Appuyez sur <b>SAVE</b> : la page USER s'ouvre."),
     ("Choose a place (U01 to U32) with <b>KNOB 1</b>.", "Choisissez un emplacement (U01 à U32) avec <b>KNOB 1</b>."),
     ("Press <b>OCT+</b>, name the sound with the keys if you wish, and press <b>OCT+</b> again.",
      "Appuyez sur <b>OCT+</b>, nommez le son avec les touches si vous voulez, puis appuyez de nouveau sur <b>OCT+</b>.")]) +
 P2("To load it later: turn PRESETS to the end of the list, or on SAVE › USER pick it with KNOB 1, turn KNOB 2 "
    "(LOAD) and press OCT+.", "Pour le recharger : tournez PRESETS jusqu'à la fin de la liste, ou sur SAVE › USER "
    "choisissez-le avec KNOB 1, tournez KNOB 2 (LOAD) et appuyez sur OCT+.") + '</div></div>' +
 '</section>')

# ------------------------------------------------------------------------------------------------ 10 import
S.append(sec(*TOC[9]) +
 P2("The <b>Guru 600 Sound Sender</b> page (envoi-sons.html, in the installation folder) sends Prophet-600 sounds to "
    "the FM-1. They stay in it, even switched off.", "La page <b>Guru 600 Sound Sender</b> (envoi-sons.html, dans le "
    "dossier d'installation) envoie des sons Prophet-600 au FM-1. Ils y restent, même éteint.") +
 '<div class="split">' + T('<img src="img/envoi_en.png" style="width:360px" alt="">', '<img src="img/envoi_fr.png" style="width:360px" alt="">', "figure") + '<div>' +
 OL([("Connect the FM-1 with a USB <b>data</b> cable and switch it on. Open the page in <b>Chrome, Edge or another Chrome-based browser (Brave, Opera…)</b> and press Connect; allow MIDI (SysEx) when asked. Safari cannot talk to the FM-1.", "Branchez le FM-1 avec un câble USB <b>de données</b> et allumez-le. Ouvrez la page dans <b>Chrome, Edge ou un autre navigateur basé sur Chrome (Brave, Opera…)</b> et cliquez sur Connecter ; autorisez le MIDI (SysEx) quand c'est demandé. Safari ne peut pas communiquer avec le FM-1."),
     ("Open a .syx file: an original Sequential dump or a GliGli patch file, one sound or a bank of 100.",
      "Ouvrez un fichier .syx : une sauvegarde d'origine Sequential ou un fichier GliGli, un son ou une banque de 100."),
     ("Choose each sound's place (1 to 255) and press Send, or Send all from a place.",
      "Choisissez la place de chaque son (1 à 255) et cliquez sur Envoyer, ou Tout envoyer à partir d'une place.")]) +
 '</div></div>' +
 LI([("Every place, 1 to 255, holds a built-in sound: a sent sound replaces it until the reset.", "Chaque place, de 1 à 255, contient un son intégré : un son envoyé le remplace jusqu'à la réinitialisation."),
     ("<b>55 sounds at most</b> can be sent in all, wherever they go.", "<b>55 sons au maximum</b> peuvent être envoyés en tout, quelle que soit leur place."),
     ("USB only: the TRS MIDI socket does not receive sounds.", "USB seulement : la prise MIDI TRS ne reçoit pas les sons."),
     ("An imported sound's name begins with its place number.", "Le nom d'un son importé commence par son numéro de place.")]) +
 H3("Getting sounds back from the FM-1", "Récupérer des sons du FM-1") +
 P2("In the GET SOUNDS BACK box of the same page, once connected: <b>Get this place</b> (one sound), <b>Get the saved and imported sounds</b>, or <b>Get all 255</b>. The sounds arrive in a .syx file in your Downloads folder, in the Prophet-600's own format (Sequential's): it can be sent back to the FM-1, kept as a backup, shared, or loaded into a real Prophet-600.", "Dans le cadre RÉCUPÉRER DES SONS de la même page, une fois connecté : <b>Récupérer cette place</b> (un son), <b>Récupérer les sons enregistrés et importés</b>, ou <b>Tout récupérer (255)</b>. Les sons arrivent dans un fichier .syx, dans le dossier Téléchargements, au format d'origine du Prophet-600 (celui de Sequential) : on peut le renvoyer au FM-1, le garder en sauvegarde, le partager ou le charger dans un vrai Prophet-600.") +
 P2("An unmodified factory sound comes back exactly as Sequential's original. Where the Guru-600 has finer settings than the Prophet-600, the nearest original value is used.", "Un son d'usine non modifié revient exactement identique à l'original de Sequential. Là où le Guru-600 a des réglages plus fins que le Prophet-600, c'est la valeur d'origine la plus proche qui est utilisée.") +
 '</section>')

# ------------------------------------------------------------------------------------------------ 11 reset
S.append(sec(*TOC[10]) +
 P2("The reset forgets every sound sent from a computer or saved in a place: the 255 built-in sounds come back. Your 32 USER sounds and your projects are not touched. Three ways:", "La réinitialisation oublie tous les sons envoyés depuis un ordinateur ou enregistrés dans une place : les 255 sons intégrés reviennent. Vos 32 sons USER et vos projets ne sont pas touchés. Trois façons :") +
 '<div class="split">' + shot("shots/menu_p600reset.png", "MENU › SYSTEM: RESET SOUNDS and RESET GURU-600.", "MENU › SYSTEM : RESET SOUNDS et RESET GURU-600.", 220) + '<div>' +
 OL([("<b>On the FM-1, from the menu:</b> hold HOME, go to the SYSTEM tab with ALGORITHM, choose RESET SOUNDS with "
      "PRESETS and press OCT+.", "<b>Sur le FM-1, par le menu :</b> maintenez HOME, allez à l'onglet "
      "SYSTEM avec ALGORITHM, choisissez RESET SOUNDS avec PRESETS et appuyez sur OCT+."),
     ("<b>On the FM-1, at power-on:</b> hold SAVE while switching on. The screen asks RESET SOUNDS ?: OCT+ yes, OCT− no.",
      "<b>Sur le FM-1, à l'allumage :</b> maintenez SAVE en l'allumant. L'écran demande RESET SOUNDS ? : OCT+ oui, OCT− non."),
     ("<b>From a computer:</b> on the Sound Sender page, press Restore the original sounds.",
      "<b>Depuis un ordinateur :</b> sur la page d'envoi, cliquez sur Rétablir les sons d'origine.")]) + '</div></div>' +
 '<div class="warn">' + P2("<b>RESET GURU-600</b>, just below, is the factory reset: it erases everything (settings, USER sounds, projects, samples, sent sounds) and restarts Guru 600 as new. Only the calibration of the buttons is kept. Choose it with PRESETS, press OCT+, then confirm ARE YOU SURE? with OCT+ (OCT− cancels).",
    "<b>RESET GURU-600</b>, juste en dessous, est la remise à zéro d'usine : elle efface tout (réglages, sons USER, projets, samples, sons envoyés) et redémarre le Guru 600 comme neuf. Seul le calibrage des boutons est conservé. Choisissez-la avec PRESETS, appuyez sur OCT+, puis confirmez ARE YOU SURE? avec OCT+ (OCT− annule).") + '</div>' +
 '</section>')

# ------------------------------------------------------------------------------------------------ 12 mod wheel
S.append(sec(*TOC[11]) +
 P2("The Prophet-600 has a mod wheel; each factory sound says what it does (see the appendix). The FM-1 has none, so:",
    "Le Prophet-600 a une molette de modulation ; chaque son d'usine indique son effet (voir l'annexe). Le FM-1 n'en a pas, donc :") +
 LI([("play from a MIDI keyboard: its mod wheel works (CC1);", "jouez depuis un clavier MIDI : sa molette fonctionne (CC1) ;"),
     ("or set MENU › CONTROL › <b>SELECT = MODW</b>: the SELECT knob becomes the mod wheel.",
      "ou réglez MENU › CONTROL › <b>SELECT = MODW</b> : le bouton SELECT devient la molette.")]) +
 P2("How much the wheel acts is set by <b>WHEEL</b> on the EXTRAS page.", "L'action de la molette se dose avec <b>WHEEL</b> sur la page EXTRAS.") +
 H3("Driving every control by MIDI", "Piloter chaque commande en MIDI") +
 P2("On a P600 track, each Guru-600 setting answers a fixed MIDI CC number: a controller's knobs, or a music software (Logic, Ableton…) that records and plays back the knob moves. The numbers are those of the GliGli firmware for the Prophet-600, so a setup made for a real Prophet-600 works as is; only the glide is on CC 5 instead of 38. The CC comes on the track's channel (MENU › MIDI), and a CC set up with MIDI LEARN takes priority.", "Sur une piste P600, chaque réglage du Guru-600 répond à un numéro de CC MIDI fixe : les boutons d'un contrôleur, ou un logiciel de musique (Logic, Ableton…) qui enregistre et rejoue les mouvements de boutons. Les numéros sont ceux du firmware GliGli pour le Prophet-600 : un réglage prévu pour un vrai Prophet-600 marche tel quel ; seul le glide est sur le CC 5 au lieu du 38. Le CC arrive sur le canal de la piste (MENU › MIDI), et un CC réglé avec MIDI LEARN est prioritaire.") +
 table([("CC", "CC"), ("Control", "Commande"), ("Values", "Valeurs")], [["1", '<b>MOD WHEEL</b>', ("0 to 127", "0 à 127")],
       ["5", '<b>GLIDE</b>', ("0 to 127", "0 à 127")],
       ["7", '<b>VOLUME</b>', ("0 to 127", "0 à 127")],
       ["16", '<b>OSC A FREQUENCY</b>', ("0 to 127", "0 à 127")],
       ["17", '<b>OSC A LEVEL (MIXER)</b>', ("127 = only A", "127 = seulement A")],
       ["18", '<b>OSC A PULSE WIDTH</b>', ("0 to 127", "0 à 127")],
       ["19", '<b>OSC B FREQUENCY</b>', ("0 to 127", "0 à 127")],
       ["20", '<b>OSC B LEVEL (MIXER)</b>', ("127 = only B", "127 = seulement B")],
       ["21", '<b>OSC B PULSE WIDTH</b>', ("0 to 127", "0 à 127")],
       ["22", '<b>OSC B FINE</b>', ("0 to 127", "0 à 127")],
       ["23 / 74", '<b>FILTER CUTOFF</b>', ("0 to 127", "0 à 127")],
       ["24 / 71", '<b>RESONANCE</b>', ("0 to 127", "0 à 127")],
       ["25", '<b>FILTER ENVELOPE AMOUNT</b>', ("0 to 127", "0 à 127")],
       ["26 \u00b7 27 \u00b7 28 \u00b7 29", '<b>FILTER ENVELOPE RELEASE · SUSTAIN · DECAY · ATTACK</b>', ("0 to 127", "0 à 127")],
       ["30 \u00b7 31 \u00b7 32 \u00b7 33", '<b>AMPLIFIER RELEASE · SUSTAIN · DECAY · ATTACK</b>', ("0 to 127", "0 à 127")],
       ["34", '<b>POLY-MOD FIL ENV</b>', ("0 to 127", "0 à 127")],
       ["35", '<b>POLY-MOD OSC B</b>', ("0 to 127", "0 à 127")],
       ["36", '<b>LFO FREQUENCY</b>', ("0 to 127", "0 à 127")],
       ["37", '<b>LFO INITIAL AMOUNT</b>', ("0 to 127", "0 à 127")],
       ["40", '<b>VEL > FLT (EXTRAS)</b>', ("0 to 127", "0 à 127")],
       ["44", '<b>DETUNE (UNISON)</b>', ("0 to 127", "0 à 127")],
       ["48 \u00b7 49 \u00b7 50", '<b>OSC A SAW · TRI · PULSE</b>', ("64 to 127 = on", "64 à 127 = allumé")],
       ["51 \u00b7 52 \u00b7 53", '<b>OSC B SAW · TRI · PULSE</b>', ("64 to 127 = on", "64 à 127 = allumé")],
       ["54", '<b>SYNC</b>', ("64 to 127 = on", "64 à 127 = allumé")],
       ["55 \u00b7 56", '<b>POLY-MOD › FREQ A · FILTER</b>', ("64 to 127 = on", "64 à 127 = allumé")],
       ["57", '<b>LFO SHAPE</b>', ("0 to 63 triangle, 64 to 127 square", "0 à 63 triangle, 64 à 127 carré")],
       ["60", '<b>FILTER KEYBOARD</b>', ("0 to 42 OFF, 43 to 85 HALF, 86 to 127 FULL", "0 à 42 OFF, 43 à 85 HALF, 86 à 127 FULL")],
       ["66", '<b>UNISON</b>', ("64 to 127 = on", "64 à 127 = allumé")],
       ["113 \u00b7 114 \u00b7 115", '<b>LFO › FREQ A-B · PW A-B · FILTER</b>', ("64 to 127 = on", "64 à 127 = allumé")],
       ["116", '<b>VINTAGE (EXTRAS)</b>', ("0 to 127", "0 à 127")]], "knobs") +
 '</section>')

# ------------------------------------------------------------------------------------------------ 13 the app
KEYS = [("A W S E D F T G Y H U J K O L P ; '", "the keys, from C to F an octave and a half higher", "les touches, de do au fa une octave et demie au-dessus"),
        ("Z / X", "OCT− / OCT+", "OCT− / OCT+"), ("Space", "PLAY", "PLAY"), ("R", "REC", "REC"),
        ("1 2 3 4 5", "FX, SCL, ENV, LFO, EDIT", "FX, SCL, ENV, LFO, EDIT"),
        ("6 7 8 9 0", "GLO, HOME, SAVE, ARP, SEQ", "GLO, HOME, SAVE, ARP, SEQ"),
        ("mouse", "click the buttons and keys, drag or scroll the knobs", "cliquer boutons et touches, glisser ou faire défiler sur les boutons rotatifs"),
        ("Esc", "quit (the memory is saved)", "quitter (la mémoire est enregistrée)")]
S.append(sec(*TOC[12]) +
 P2("The Guru-600 application runs on Macs with Apple Silicon only. It is not available on Intel Macs or on PCs.", "L'application Guru-600 tourne sur Mac à puce Apple (Apple Silicon) uniquement. Elle n'est pas disponible sur les Mac Intel ni sur PC.") +
 P2("<b>Guru 600.app</b> brings Guru 600 to your Mac, with the FM-1's panel on screen: to try sounds, learn the pages, or "
    "play without the device. It is a real FM-1 emulator running the same firmware.",
    "<b>Guru 600.app</b> fait fonctionner Guru 600 sur un Mac, avec la façade du FM-1 à l'écran : pour essayer les sons, "
    "apprendre les pages, ou jouer sans l'appareil. C'est un véritable émulateur du FM-1 qui exécute le même firmware.") +
 LI([("The first time: right-click the app › Open.",
      "La première fois : clic droit sur l'application › Ouvrir."),
     ("Its memory (USER sounds, imported sounds, settings) is kept between launches when you quit normally.",
      "Sa mémoire (sons USER, sons importés, réglages) est gardée d'un lancement à l'autre si on quitte normalement."),
     ("A MIDI keyboard connected to the Mac plays it.", "Un clavier MIDI branché au Mac le fait jouer."),
     ("The <b>Help</b> menu opens this guide, in the Mac's language.", "Le menu <b>Aide</b> ouvre cette notice, dans la langue du Mac.")]) +
 table([("Mac key", "Touche du Mac"), ("FM-1", "FM-1")], [[f"<b>{e(a)}</b>", (b, c)] for a, b, c in KEYS]) +
 P2("In the app, a double press is the same key twice quickly: <b>5</b> for EDIT, <b>3</b> for ENV, <b>4</b> for LFO, and so on.", "Dans l'application, un double appui se fait avec la même touche deux fois rapidement : <b>5</b> pour EDIT, <b>3</b> pour ENV, <b>4</b> pour LFO, etc.") +
 '</section>')

# ------------------------------------------------------------------------------------------------ 15 mapping
MAP = [("POLY-MOD › FILTER ENVELOPE / OSC B / FREQ A / FILTER", "EDIT 1/10 › FIL ENV, OSC B, DEST"),
       ("LFO › FREQUENCY, SHAPE", "LFO › RATE, WAVE"), ("LFO › INITIAL AMOUNT", "LFO DEST › PIT / FLT / SHP"),
       ("LFO › FREQ / PW / FILTER", "LFO DEST › PIT, SHP, FLT"),
       ("OSC A › FREQUENCY, SAW / TRI / PULSE", "EDIT 2/10 › FREQ A, SHAPE A"),
       ("OSC A › PULSE WIDTH, SYNC", "EDIT 3/10 › PW A, SYNC"),
       ("OSC B › FREQUENCY, FINE, SAW / TRI / PULSE, PULSE WIDTH", "EDIT 2/10 › FREQ B, SHAPE B; EDIT 3/10 › FINE B, PW B"),
       ("GLIDE", "EDIT 4/10 › GLIDE"), ("MIXER › OSC A / OSC B", "EDIT 4/10 › MIXER"),
       ("UNISON", "EDIT 4/10 › VOICES = UNI"),
       ("FILTER › CUTOFF, RESONANCE, ENVELOPE AMOUNT", "EDIT 5/10 › CUTOFF, RES, ENV AMT (also HOME)"),
       ("FILTER › KEYBOARD HALF / FULL", "EDIT 5/10 › KBD"),
       ("FILTER ENVELOPE › ATTACK, DECAY, SUSTAIN, RELEASE", "EDIT 6/10"),
       ("AMPLIFIER › ATTACK, DECAY, SUSTAIN, RELEASE", "ENV › AMPLIFIER"),
       ("MASTER VOLUME", "MASTER"), ("TUNE", "MENU › AUDIO › TUNE"),
       ("PROGRAM / RECORD", "PRESETS / SAVE"), ("Pitch and mod wheels", "MIDI keyboard, or SELECT = MODW")]
S.append(sec(*TOC[14]) + '<figure class="wide"><img src="img/facade.png" alt=""></figure>' +
 table([("Prophet-600 panel", "Façade du Prophet-600"), ("Guru 600 on the FM-1", "Guru 600 sur le FM-1")],
       [[e(a), e(b)] for a, b in MAP]) + '</section>')

# ------------------------------------------------------------------------------------------------ 16 differences
S.append(sec(*TOC[15]) +
 H3("The sound", "Le son") +
 P2("Guru 600 is a digital imitation of an analog synthesizer. The settings of the 100 factory sounds are the "
    "original ones, read from Sequential's own files, and the envelopes, filter and LFO are calibrated on the "
    "Prophet-600's measured behavior. But no digital model sounds exactly like a given analog instrument: each "
    "Prophet-600 sounded a little different from the next. Expect the same character, not the same machine.",
    "Guru 600 est une imitation numérique d'un synthétiseur analogique. Les réglages des 100 sons d'usine sont ceux "
    "d'origine, lus dans les fichiers de Sequential, et les enveloppes, le filtre et le LFO sont calibrés d'après le "
    "comportement mesuré du Prophet-600. Mais aucun modèle numérique ne sonne exactement comme un instrument analogique "
    "donné : chaque Prophet-600 sonnait un peu différemment du suivant. Attendez-vous au même caractère, pas à la même machine.") +
 H3("What Guru 600 can do and the Prophet-600 cannot", "Ce que Guru 600 sait faire et pas le Prophet-600") +
 LI([("Four tracks with other engines at the same time, a 64-step sequencer, songs, an arpeggiator with many modes.",
      "Quatre pistes avec d'autres moteurs en même temps, un séquenceur 64 pas, des morceaux, un arpégiateur à nombreux modes."),
     ("Effects: reverb, delay, chorus, distortion, INSERT effects, performance effects.",
      "Des effets : réverbération, délai, chorus, distorsion, effets INSERT, effets de jeu."),
     ("An LFO with tempo sync and more shapes, a modulation matrix, velocity on the filter, stereo spread.",
      "Un LFO synchronisable au tempo avec plus de formes, une matrice de modulation, la vélocité sur le filtre, l'étalement stéréo."),
     ("Mono, legato and note priorities; the 100 v2022 sounds; scales and chord keys; USB audio and MIDI.",
      "Mono, legato et priorités de notes ; les 100 sons v2022 ; gammes et accords ; audio et MIDI par USB."),
     ("A Mac app to play it without the device.", "Une application Mac pour en jouer sans l'appareil.")]) +
 H3("What the Prophet-600 can do and Guru 600 cannot", "Ce que le Prophet-600 sait faire et pas Guru 600") +
 LI([("A real analog sound, with its own warmth and accidents.", "Un vrai son analogique, avec sa chaleur et ses accidents."),
     ("A full-size 61-key keyboard with pitch and mod wheels, and a knob per control.",
      "Un clavier de 61 touches de taille normale avec molettes de hauteur et de modulation, et un bouton par réglage."),
     ("A real analog output stage.", "Un véritable étage de sortie analogique.")]) + '</section>')

# ------------------------------------------------------------------------------------------------ 17 credits
S.append(sec(*TOC[16]) +
 LI([("Guru-600: Marc Massé, 2026, GPL-3 license.", "Guru-600 : Marc Massé, 2026, licence GPL-3."),
     ("Felucca: Leo Kuroshita (hugelton), GPL-3 license.",
      "Felucca : Leo Kuroshita (hugelton), licence GPL-3."),
     ("Prophet-600 factory programs: Sequential Circuits, 1982. Prophet-600 is a trademark of its owner; the Guru-600 is not affiliated with Sequential.",
      "Programmes d'usine du Prophet-600 : Sequential Circuits, 1982. Prophet-600 est une marque de son propriétaire ; le Guru-600 est sans lien avec Sequential."),
     ("v2022 collection: its authors (see appendix), GPL license, from the GliGli Prophet-600 firmware project.",
      "Collection v2022 : ses auteurs (voir annexe), licence GPL, issue du projet de firmware Prophet-600 GliGli."),
     ("Sounds 201 to 230: adapted from the factory sounds of Surge XT (surge-synthesizer.github.io, GPL-3), by Claes Johanson. Sounds 231 to 255: originals made for the Guru-600.",
      "Sons 201 à 230 : adaptés des sons d'usine de Surge XT (surge-synthesizer.github.io, GPL-3), de Claes Johanson. Sons 231 à 255 : originaux créés pour le Guru-600."),
     ("FM-1 emulator: fm1-emu (Joakim Eriksson).",
      "Émulateur FM-1 : fm1-emu (Joakim Eriksson)."),
     ("Fonts: Inter Tight (SIL Open Font License); VI Mong Rong (VN-Fonts Team, 1994).",
      "Polices : Inter Tight (licence SIL Open Font) ; VI Mong Rong (VN-Fonts Team, 1994).")]) +
 '<div class="ded">' + T("To Éric Le Yavanc, my brother at heart,", "À Éric Le Yavanc, mon frère de cœur,", "p") + T("passionate about sound and a techie like no other.", "passionné de son et techos hors pair.", "p") + T("Love you, lil’ bro! It's all thanks to you!", "Je t'aime, p'tit frère ! C'est grâce à toi, tout ça !", "p") + '</div>' +   # the dedication (Marc), four lines
 '</section>')

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
    v22r.append(f'<tr><td><b>{101+i}</b></td><td>{e(x["name"])}</td><td>{e(by)}</td><td>{ml(x["fam"][0])}</td>'
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
    gr.append(f'<tr><td><b>{201 + i}</b></td><td>{e(x["name"])}</td><td>{bi2(*x["fam"]) if x["fam"][0] != x["fam"][1] else typo(e(x["fam"][0]), "en")}</td>'
              f'<td>{orig}</td><td>{about}</td></tr>')
GURU_T = ('<h3 class="v22">201–255 · Guru-600</h3><table class="snd g6t"><thead><tr><th>No.</th><th>Name</th>'
          '<th>Family</th><th>Origin</th><th>About</th></tr></thead><tbody>' + "".join(gr) + '</tbody></table>')
ANNEX = ('<section class="annex"><h2><span class="num">18</span>' + ML("Appendix", "Annexe", "Anhang", "Anexo", "Appendice") + '<br>' + ML('<span lang="zh">附录</span>', '<span lang="ja">付録</span>') + '</h2>'
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


S = [keep_title(x) if x.startswith("<section>") else x for x in S]   # (the chapters; not the covers, the contents)

out = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Guru-600 · User guide</title><style>' + CSS +
       ''.join(f'body:not([data-lang={l}]) .{l}{{display:none}}' for l in LANGS) + '</style></head><body>'
       '<nav id="lang">' + ''.join(f'<button data-l="{l}" onclick="setLang(\'{l}\')">{LNAME[l]}</button>' for l in LANGS) +
       '</nav>' + ''.join(S) +
       '<script>function setLang(l){document.body.dataset.lang=l;document.documentElement.lang=l;'
       'document.querySelectorAll("#lang button").forEach(function(b){b.classList.toggle("on",b.dataset.l==l)});'
       'try{localStorage.g6lang=l}catch(e){}}'
       'var u=new URLSearchParams(location.search),q=u.get("lang"),s;if(u.get("part"))document.body.classList.add("part-"+u.get("part"));try{s=localStorage.g6lang}catch(e){}'
       'var nl=(navigator.language||"en").slice(0,2);if(["en","fr","de","es","it","zh","ja"].indexOf(nl)<0)nl="en";setLang(q||s||nl);document.querySelectorAll(".golang a,.toc a[data-l]").forEach(function(a){a.onclick=function(e){e.preventDefault();'
       'var l=a.dataset.l;if(l=="annex"){document.querySelector(".annex").scrollIntoView()}else{setLang(l);'
       'document.querySelector(".toc").scrollIntoView()}}})</script></body></html>')
open(os.path.join(H, "index.html"), "w").write(out)
json.dump([{"en": k, "fr": v} for k, v in STRINGS.items()], open(os.path.join(H, "strings.json"), "w"), ensure_ascii=False, indent=1)
print("strings", len(STRINGS), "missing", sorted(MISSING))
print("index.html", len(out))
