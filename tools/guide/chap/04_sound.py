# 04 · SOUND: a panel inspired by the Prophet-600
# (the parameters' texts: the notice's, chapter "The P600 engine, page by page", read from its file: the same texts,
# so the same translations)
_P6 = {}
def _p6page(fam, img, t, t2, ie, if_, rows, we, wf):
    for r in rows:
        _P6[(t.split(" · ")[1], r[0])] = r[1:]
    return ""
exec(open(os.path.join(N, "chap", "08_p600.py")).read(),
     dict(page=_p6page, CH=lambda *a: None, P2=lambda *a: "", H3=lambda *a: "", LI=lambda *a: "", BOX=lambda *a: "", T=lambda *a: ""))


def P6R(label, page, key):                  # a row of the notice's: the editor's label, its texts and values
    en, fr, ven, vfr = _P6[(page, key)]
    return (label, en, fr, ven, vfr)


TIME_V = ("1 ms … 10 s", "1 ms … 10 s")
CH("sound", "SOUND: a panel inspired by the Prophet-600", "SOUND : une façade inspirée du Prophet-600",
 P2("The SOUND page shows the sound of the selected track on a panel inspired by the Prophet-600: every knob and switch of the "
    "original, plus what the Guru-600 adds (VOICE, FX SENDS, EXTRAS, MORPH). A change is heard at once on the FM-1. "
    "On the right, SOUNDS holds every sound the FM-1 can play, and saves and exchanges the 255 P600 sounds.",
    "La page SOUND présente le son de la piste choisie sur une façade inspirée du Prophet-600 : chaque bouton et chaque "
    "interrupteur de l'original, plus ce qu'ajoute le Guru-600 (VOICE, FX SENDS, EXTRAS, MORPH). Un changement s'entend "
    "aussitôt sur le FM-1. À droite, SOUNDS contient tous les sons que peut jouer le FM-1, et enregistre et échange les 255 sons P600.") +
 SHOT("sound", "The SOUND page.", "La page SOUND.") +
 BOX("note", ("A change affects the track's sound, not the saved sound. To keep it: SAVE TO THIS PLACE (below), or STORE THE TRACK'S SOUND on the PROJECTS page (chapter {ch:projects}).",
              "Un changement modifie le son de la piste, pas le son enregistré. Pour le garder : SAVE TO THIS PLACE (plus bas), ou STORE THE TRACK'S SOUND sur la page PROJECTS (chapitre {ch:projects}).")) +
 H3("When the track does not play P600", "Quand la piste ne joue pas P600", EDC["sound"]) +
 P2("When the track plays a sound of the FM-1 (another engine than P600), the panel, MORPH and MUTATE dim and stay still, and a message says which engine the track plays: they set the Guru-600 sounds only. Click a Guru-600 sound (1 to 255) in SOUNDS: the track switches to P600 and plays it. The keyboard still shows the keys played on the FM-1, and the other pages work with every engine.",
    "Quand la piste joue un son du FM-1 (un autre moteur que P600), la façade, MORPH et MUTATE s'assombrissent et restent inactifs, et un message indique le moteur que joue la piste : ils ne règlent que les sons Guru-600. Cliquez sur un son Guru-600 (1 à 255) dans SOUNDS : la piste passe en P600 et le joue. Le clavier montre toujours les touches jouées sur le FM-1, et les autres pages fonctionnent avec tous les moteurs.") +
 H3("POLY-MOD", "POLY-MOD", FAM["pm"]) +
 P2("In each voice, two sources modulate oscillator A's pitch and/or the filter.", "Dans chaque voix, deux sources modulent la hauteur de l'oscillateur A et/ou le filtre.") +
 CTL3([P6R("FIL ENV", "POLY MOD", "PM EN"), P6R("OSC B", "POLY MOD", "PM B"),
       ("FREQ A, FILTER", "DESTINATION: where the modulation goes. Both lit: both; both unlit: nowhere.",
        "DESTINATION : où va la modulation. Les deux allumés : les deux ; les deux éteints : nulle part.", "OFF / ON", "OFF / ON")]) +
 H3("LFO", "LFO", FAM["lfo"]) +
 CTL3([("FREQUENCY", "The LFO's speed.", "La vitesse du LFO.", "0.1 … 40 Hz", "0,1 … 40 Hz"),
       ("SHAPE", "Click to choose the triangle (left) or the square (right). Unlit: a shape the Prophet-600 does not have, set on the FM-1.",
        "Cliquez pour choisir le triangle (à gauche) ou le carré (à droite). Éteint : une forme que le Prophet-600 n'a pas, réglée sur le FM-1.", "△ / □", "△ / □"),
       ("INITIAL AMOUNT", "How much of the LFO plays with the mod wheel down. The rest, the wheel adds it. It is EXTRAS' WHEEL seen the other way round: the two knobs move together.",
        "La part du LFO qui joue molette en bas. Le reste, la molette l'ajoute. C'est le WHEEL d'EXTRAS vu dans l'autre sens : les deux boutons bougent ensemble.", "0 … 100 %", "0 … 100 %"),
       ("FREQ A-B, PW A-B, FILTER", "DESTINATION: what the LFO moves: the pitch of both oscillators, their pulse widths, the filter. Any combination.",
        "DESTINATION : ce que fait bouger le LFO : la hauteur des deux oscillateurs, leurs largeurs d'impulsion, le filtre. Toute combinaison.", "OFF / ON", "OFF / ON")]) +
 H3("OSCILLATOR A, OSCILLATOR B", "OSCILLATOR A, OSCILLATOR B", FAM["osc"]) +
 CTL3([P6R("FREQUENCY (A)", "OSC", "A FRQ"), P6R("FREQUENCY (B)", "OSC", "B FRQ"), P6R("FINE (B)", "OSC 2", "B FIN"),
       P6R("SYNC (A)", "OSC 2", "SYNC"),
       ("SAW, TRI, PULSE", "The waveforms of the oscillator: light one, two or three to combine them; all unlit: the oscillator is silent.",
        "Les formes d'onde de l'oscillateur : allumez-en une, deux ou trois pour les combiner ; toutes éteintes : l'oscillateur se tait.", "OFF / ON", "OFF / ON"),
       P6R("PULSE WIDTH (A)", "OSC 2", "A PW"), P6R("PULSE WIDTH (B)", "OSC 2", "B PW")]) +
 H3("MIXER, GLIDE, UNISON", "MIXER, GLIDE, UNISON", FAM["osc"]) +
 CTL3([P6R("MIXER", "MIXER", "MIX"), P6R("GLIDE", "MIXER", "GLD"),
       ("UNISON", "All the voices on one note, huge. Unlit: the track plays chords (POLY). The other voice modes (MONO, LEGATO) are on the MOD page (chapter {ch:mod}).",
        "Toutes les voix sur une note, énorme. Éteint : la piste joue des accords (POLY). Les autres modes de voix (MONO, LEGATO) sont sur la page MOD (chapitre {ch:mod}).", "OFF / ON", "OFF / ON")]) +
 H3("FILTER, FILTER ENVELOPE", "FILTER, FILTER ENVELOPE", FAM["flt"]) +
 CTL3([P6R("CUTOFF", "FILTER", "CUT"), P6R("RESONANCE", "FILTER", "RES"), P6R("ENVELOPE AMOUNT", "FILTER", "FENV"),
       ("KEYBOARD", "Higher notes open the filter: OFF, HALF, FULL (the filter follows the keyboard note for note). Click an option.",
        "Les notes aiguës ouvrent le filtre : OFF, HALF, FULL (le filtre suit le clavier note pour note). Cliquez sur une option.", "OFF, HALF, FULL", "OFF, HALF, FULL"),
       P6R("ATTACK", "FLT ENV", "ATK"), P6R("DECAY", "FLT ENV", "DEC"), P6R("SUSTAIN", "FLT ENV", "SUS"), P6R("RELEASE", "FLT ENV", "REL")]) +
 H3("AMPLIFIER", "AMPLIFIER", FAM["env"]) +
 CTL3([("ATTACK", "Time for the sound to reach its full level.", "Temps pour que le son atteigne son plein niveau.") + TIME_V,
       ("DECAY", "Time to fall back to the sustain level.", "Temps de redescente vers le niveau de maintien.") + TIME_V,
       ("SUSTAIN", "The level held while the key is down.", "Le niveau tenu tant que la touche est enfoncée.", "0 … 100 %", "0 … 100 %"),
       ("RELEASE", "Time for the sound to die away after the key is released.", "Temps d'extinction du son après le relâchement de la touche.") + TIME_V]) +
 H3("VOICE, FX SENDS", "VOICE, FX SENDS", FAM["vce"]) +
 CTL3([("LEVEL", "The track's volume (the same as its fader on TRACKS).", "Le volume de la piste (le même que son fader sur TRACKS).", ("OFF, −55.5 … +7.5 dB", "OFF, −55,5 … +7,5 dB")[0], "OFF, −55,5 … +7,5 dB"),
       ("PAN", "The track's position, left / right.", "La position de la piste, gauche / droite.", "L 100 … C … R 100", "L 100 … C … R 100"),
       P6R("SPREAD", "VOICE 3", "SPRD"),
       ("DIST, CHORUS, DELAY, REVERB", "How much of the track goes to each effect (chapter {ch:fx}).", "La part de la piste envoyée à chaque effet (chapitre {ch:fx}).", "0 … 100 %", "0 … 100 %")]) +
 H3("EXTRAS", "EXTRAS", FAM["ext"]) +
 P2("Features the Prophet-600 did not have, set per sound.", "Ce que le Prophet-600 n'avait pas, réglé par chaque son.") +
 CTL3([P6R("VINTAGE", "EXTRAS", "VINTAGE"),
       ("WHEEL", "How much of the LFO the mod wheel controls. 0 %: the LFO always plays fully and the wheel does nothing. 100 %: no LFO until you push the wheel. The LFO's INITIAL AMOUNT shows the same thing the other way round.",
        "La part du LFO que commande la molette. 0 % : le LFO joue toujours en entier et la molette ne fait rien. 100 % : pas de LFO tant que vous ne poussez pas la molette. L'INITIAL AMOUNT du LFO montre la même chose dans l'autre sens.", "0 … 100 %", "0 … 100 %"),
       P6R("VEL > FLT", "EXTRAS", "VEL>FLT"), P6R("DETUNE", "EXTRAS", "DETUNE")]) +
 H3("Turning the knobs", "Tourner les boutons", EDC["sound"]) +
 LI([("Drag up or down on a knob; hold <kbd>Shift</kbd> for finer steps. Or scroll over it.",
      "Glissez vers le haut ou le bas sur un bouton ; maintenez <kbd>Maj</kbd> pour des pas plus fins. Ou faites défiler au-dessus de lui."),
     ("A double click puts it back to its usual value.", "Un double clic le remet à sa valeur habituelle."),
     ("Switches and options: click.", "Interrupteurs et options : cliquez.")]) +
 H3("SOUNDS: every sound", "SOUNDS : tous les sons", EDC["sound"]) +
 '<div class="split">' + SHOT("sounds", "SOUNDS.", "SOUNDS.", 200) + '<div>' +
 LI([("<b>1 to 255</b>: the Guru-600 sounds (P600). <b>From 256, number on a grey-blue ground</b>: the sounds of the FM-1's other engines. <b>U1, U2…</b>: your USER sounds (chapter {ch:projects}).",
      "<b>1 à 255</b> : les sons Guru-600 (P600). <b>À partir de 256, numéro sur fond gris-bleu</b> : les sons des autres moteurs du FM-1. <b>U1, U2…</b> : vos sons USER (chapitre {ch:projects})."),
     ("<b>Click a sound</b> to load it on the track; a sound of another engine switches the track to that engine. If you changed the sound without saving it, the editor asks first.",
      "<b>Cliquez sur un son</b> pour le charger sur la piste ; un son d'un autre moteur fait passer la piste sur ce moteur. Si vous avez modifié le son sans l'enregistrer, l'éditeur demande d'abord."),
     ("<b>Right-click a Guru-600 sound</b> to rename it (11 characters at most): the name is kept on the FM-1.",
      "<b>Clic droit sur un son Guru-600</b> pour le renommer (11 caractères au plus) : le nom est gardé dans le FM-1."),
     ("<b>ALL, BASS, LEAD, PAD, PLUCK, KEYS, DRUM, FX</b>: show only that family, among all the sounds. DRUM holds the percussion sounds and the drum kits.",
      "<b>ALL, BASS, LEAD, PAD, PLUCK, KEYS, DRUM, FX</b> : n'affiche que cette famille, parmi tous les sons. DRUM regroupe les sons de percussion et les kits de batterie."),
     ("<b>Lit yellow</b>: the track's sound. <b>Orange name</b>: one of your sounds (a place you saved or imported, or a USER sound).",
      "<b>Éclairé en jaune</b> : le son de la piste. <b>Nom orange</b> : l'un de vos sons (une place enregistrée ou importée, ou un son USER).")]) +
 '</div></div>' +
 CTL([("SAVE TO THIS PLACE", "Saves the track's sound in the place lit yellow, after a confirmation: it replaces the sound there. To save it elsewhere, click that place first, then SAVE TO THIS PLACE.",
       "Enregistre le son de la piste dans la place éclairée en jaune, après confirmation : il remplace le son qui s'y trouve. Pour l'enregistrer ailleurs, cliquez d'abord sur cette place, puis sur SAVE TO THIS PLACE."),
      ("BACK TO ORIGINAL", "On a place in orange: brings back the sound the place had at first, after a confirmation. Grey on a place that still holds its original.",
       "Sur une place en orange : rétablit le son d'origine de la place, après confirmation. Gris sur une place qui a encore son son d'origine."),
      ("EXPORT .SYX", "Saves the sound of the place as a Prophet-600 file (<i>number name</i>.syx) in the browser's downloads, under the name you give it: the Prophet-600 SysEx format, which other Prophet-600 tools read. It holds the sound as saved in the place: save your changes first.",
       "Enregistre le son de la place dans un fichier Prophet-600 (<i>numéro nom</i>.syx), dans les téléchargements du navigateur, sous le nom que vous lui donnez : le format SysEx du Prophet-600, que lisent d'autres outils du Prophet-600. Il contient le son tel qu'il est enregistré dans la place : enregistrez d'abord vos changements."),
      ("IMPORT .SYX", "Puts a Prophet-600 sound from a file (.syx or .mid, Sequential's format or GliGli's) in the place lit yellow, after a confirmation, with its name (the one given on export, else the file's). With several sounds in the file, the first one.",
       "Met un son de Prophet-600 tiré d'un fichier (.syx ou .mid, au format de Sequential ou de GliGli) dans la place éclairée en jaune, après confirmation, avec son nom (celui donné à l'export, sinon celui du fichier). Si le fichier en contient plusieurs, le premier."),
      ("RESET ALL SOUNDS", "Brings back the 255 original sounds, after a confirmation: every sound you saved or imported is erased. Make a backup first (chapter {ch:backup}).",
       "Rétablit les 255 sons d'origine, après confirmation : tous les sons enregistrés ou importés sont effacés. Faites d'abord une sauvegarde (chapitre {ch:backup}).")]) +
 P2("SAVE TO THIS PLACE, BACK TO ORIGINAL and EXPORT .SYX act on a Guru-600 sound: they are grey while the track plays a sound of the FM-1.",
    "SAVE TO THIS PLACE, BACK TO ORIGINAL et EXPORT .SYX agissent sur un son Guru-600 : ils sont gris quand la piste joue un son du FM-1.") +
 H3("What a place keeps", "Ce que garde une place", EDC["sound"]) +
 P2("<b>Saved with the sound</b>: the oscillators, the mixer, the filter and its envelope, the Poly-Mod, the amplifier envelope, the glide, UNI on or off (with its DETUNE), the LFO's rate, shape and destinations, WHEEL and VEL>FLT. "
    "<b>Not saved</b>: VINTAGE (back to 24 at each load), the effect sends (a kept sound plays dry, all sends at 0), the INSERT, MONO and LEG (a kept sound always plays POLY, or UNI if its unison was on), "
    "the LFO's PHASE and FADE and the other LFO settings of the MOD page, the ENVELOPE settings of the MOD page, MOD MATRIX slots 1–2, the VOICE settings of the MOD page and SPREAD.",
    "<b>Enregistrés avec le son</b> : les oscillateurs, le mixeur, le filtre et son enveloppe, la Poly-Mod, l'enveloppe d'amplitude, le glide, UNI actif ou non (avec son DETUNE), la vitesse, la forme et les destinations du LFO, WHEEL et VEL>FLT. "
    "<b>Non enregistrés</b> : VINTAGE (revient à 24 à chaque chargement), les envois d'effets (un son gardé joue sec, tous les envois à 0), l'INSERT, MONO et LEG (un son gardé joue toujours en POLY, ou en UNI si son unisson était actif), "
    "PHASE et FADE du LFO et les autres réglages du LFO de la page MOD, les réglages ENVELOPE de la page MOD, les emplacements 1 et 2 de MOD MATRIX, les réglages VOICE de la page MOD et SPREAD.") +
 P2("To keep everything, use STORE THE TRACK'S SOUND on the PROJECTS page (a USER sound), or save the project. "
    "The places of your own are 55 at most, shared by the sounds you save and the sounds you import. Beyond: the message <b>The memory of the places is full</b>; free some with BACK TO ORIGINAL.",
    "Pour tout garder, utilisez STORE THE TRACK'S SOUND sur la page PROJECTS (un son USER), ou enregistrez le projet. "
    "Les places à vous sont 55 au plus, partagées entre les sons enregistrés et les sons importés. Au-delà : le message <b>La mémoire des places est pleine</b> ; libérez-en avec BACK TO ORIGINAL.") +
 H3("MORPH", "MORPH", FAM["mph"]) +
 SHOT("morph", "MORPH, under the panel.", "MORPH, sous la façade.") +
 P2("MORPH turns the track's sound (SOUND A) into another one (SOUND B), little by little, and MUTATE makes a variation of it.",
    "MORPH transforme peu à peu le son de la piste (SOUND A) en un autre (SOUND B), et MUTATE en fait une variante.") +
 CTL([("SOUND A ◀ ▶", "The track's sound. The arrows load the previous or next place (after 255 comes 1), as a click in SOUNDS.",
       "Le son de la piste. Les flèches chargent la place précédente ou suivante (après 255 vient 1), comme un clic dans SOUNDS."),
      ("SOUND B ◀ ▶", "The sound to reach. Choosing another B puts the slider back at A.", "Le son à atteindre. Choisir un autre B ramène le curseur sur A."),
      ("MORPH", "Click or drag on the rail, from A (0 %) to B (100 %). The value shows after the title. The sound changes as you move.",
       "Cliquez ou glissez sur le rail, de A (0 %) à B (100 %). La valeur s'affiche après le titre. Le son change à mesure."),
      ("MUTATE", "Changes the sound at random, by the AMOUNT shown. Click again for another variation.",
       "Modifie le son au hasard, de la quantité AMOUNT indiquée. Cliquez de nouveau pour une autre variante."),
      ("AMOUNT", "How far MUTATE goes: a little (1 %) to a lot (100 %).", "Jusqu'où va MUTATE : un peu (1 %) à beaucoup (100 %).")]) +
 P2("A morphed or mutated sound is a changed sound: keep it with SAVE TO THIS PLACE or STORE THE TRACK'S SOUND. Load SOUND A again to come back to it.",
    "Un son morphé ou muté est un son modifié : gardez-le avec SAVE TO THIS PLACE ou STORE THE TRACK'S SOUND. Rechargez SOUND A pour y revenir.") +
 QA([("No sound?", "Pas de son ?",
      "Check SAW, TRI, PULSE (at least one lit on an oscillator heard), the MIXER, CUTOFF and ENVELOPE AMOUNT (not both at the bottom), the LEVEL, and that the track is not muted (TRACKS).",
      "Vérifiez SAW, TRI, PULSE (au moins un allumé sur un oscillateur entendu), le MIXER, CUTOFF et ENVELOPE AMOUNT (pas tous les deux en bas), le LEVEL, et que la piste n'est pas coupée (TRACKS)."),
     ("My saved sound sounds dry.", "Mon son enregistré sonne sec.",
      "A saved P600 sound loads with its effect sends at 0 (see What a place keeps): turn FX SENDS up again, or keep the sound as a USER sound.",
      "Un son P600 enregistré se charge avec ses envois d'effets à 0 (voir Ce que garde une place) : remontez FX SENDS, ou gardez le son comme son USER."),
     ("The memory of the places is full (55 sounds).", "La mémoire des places est pleine (55 sons).",
      "Bring some places back to their original sound (BACK TO ORIGINAL), or keep sounds as USER sounds.",
      "Rétablissez le son d'origine de quelques places (BACK TO ORIGINAL), ou gardez des sons comme sons USER."),
     ("No Prophet-600 sound in this file.", "Aucun son de Prophet-600 dans ce fichier.",
      "The file is not a Prophet-600 SysEx file (a bank of another synthesizer, for instance).",
      "Le fichier n'est pas un fichier SysEx de Prophet-600 (une banque d'un autre synthétiseur, par exemple)."),
     ("I changed a sound and loaded another one.", "J'ai modifié un son puis chargé un autre.",
      "On the FM-1, hold SAVE for 1 s: it undoes the track's last sound load, and the changed sound comes back.",
      "Sur le FM-1, maintenez SAVE 1 s : cela annule le dernier chargement de son de la piste, et le son modifié revient.")]))
