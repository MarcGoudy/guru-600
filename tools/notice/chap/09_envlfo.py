# 9 · The envelope, the LFO and the modulation matrix (Felucca pages, used by every engine and by P600)
def fpage(fam, img, title, intro_en, intro_fr, rows, where_en, where_fr):
    return page(fam, img, title, title, intro_en, intro_fr, rows, where_en, where_fr)


CH("envlfo", "The amplifier envelope, the LFO and the modulation", "L'enveloppe d'amplitude, le LFO et la modulation",
 P2("These pages serve every engine. On a P600 track they are the Prophet-600's amplifier envelope and LFO; each P600 sound sets them.",
    "Ces pages servent à tous les moteurs. Sur une piste P600, ce sont l'enveloppe d'amplitude et le LFO du Prophet-600 ; chaque son P600 les règle.") +
 H3("ENV: the amplifier envelope", "ENV : l'enveloppe d'amplitude") +
 fpage("env", "shots/pg_env1.png", "ENV 1/2", "How the volume changes during a note. Press <b>ENV</b>.",
       "Comment le volume évolue pendant une note. Appuyez sur <b>ENV</b>.",
       [("ATK", "ATTACK: time to reach full volume.", "ATTACK : temps pour atteindre le plein volume.", "1 ms – 10 s", "1 ms – 10 s"),
        ("DEC", "DECAY: time to fall to the sustain level.", "DECAY : temps pour descendre au niveau de maintien.", "1 ms – 10 s", "1 ms – 10 s"),
        ("SUS", "SUSTAIN: the volume held while the key is down.", "SUSTAIN : le volume tenu tant que la touche est enfoncée.", "0–100 %", "0–100 %"),
        ("REL", "RELEASE: time to die away after the key is released.", "RELEASE : temps d'extinction après le relâchement.", "1 ms – 10 s", "1 ms – 10 s")],
       "The ENV page.", "La page ENV.") +
 fpage("env", "shots/pg_env2.png", "ENV DEST 2/2", "The envelope also moves other settings, by a positive or negative amount.",
       "L'enveloppe fait aussi bouger d'autres réglages, d'une quantité positive ou négative.",
       [("FLT", "To the cutoff.", "Vers la coupure.", "−100 / +100 %", "−100 / +100 %"),
        ("PIT", "To the pitch.", "Vers la hauteur.", "−100 / +100 %", "−100 / +100 %"),
        ("SHP", "To the shape (on P600: the pulse widths).", "Vers la forme (sur P600 : les largeurs d'impulsion).", "−100 / +100 %", "−100 / +100 %"),
        ("ESYNC", "ON: ATK, DEC and REL become note values (1/16, 1/4, 2BAR…) that follow the tempo.", "ON : ATK, DEC et REL deviennent des valeurs de notes (1/16, 1/4, 2BAR…) qui suivent le tempo.", "OFF / ON", "OFF / ON")],
       "The ENV DEST page.", "La page ENV DEST.") +
 LI([("<b>No sound at all?</b> SUSTAIN at 0 % with a very short DECAY gives a click and nothing else; raise SUSTAIN or DECAY.",
      "<b>Plus aucun son ?</b> SUSTAIN à 0 % avec un DECAY très court ne donne qu'un clic ; montez SUSTAIN ou DECAY."),
     ("<b>The sound never stops?</b> RELEASE is very long: lower it.", "<b>Le son ne s'arrête plus ?</b> RELEASE est très long : baissez-le."),
     ("On P600, the filter has its own envelope on EDIT › FLT ENV (chapter {ch:p600}); ENV DEST › FLT adds the amplifier envelope on top.",
      "Sur P600, le filtre a sa propre enveloppe dans EDIT › FLT ENV (chapitre {ch:p600}) ; ENV DEST › FLT y ajoute l'enveloppe d'amplitude.")]) +
 H3("LFO: the slow movement", "LFO : le mouvement lent") +
 fpage("lfo", "shots/pg_lfo1.png", "LFO 1/4", "A slow wave that moves other settings up and down. Press <b>LFO</b>.",
       "Une onde lente qui fait monter et descendre d'autres réglages. Appuyez sur <b>LFO</b>.",
       [("RATE", "Its speed. Dimmed when LFO 2 › SYNC follows the tempo.", "Sa vitesse. Grisée quand LFO 2 › SYNC suit le tempo.", "0.05 – 40 Hz", "0,05 – 40 Hz"),
        ("WAVE", "Its shape: SIN, TRI, SAW, SQR (square), S&H (random steps).", "Sa forme : SIN, TRI, SAW, SQR (carré), S&H (paliers aléatoires).", "5 choices", "5 choix"),
        ("PHS", "Where the wave starts at each note.", "Où l'onde commence à chaque note.", "0–127", "0–127"),
        ("FADE", "Time for the LFO to come in after the note starts: a delayed vibrato.", "Temps d'arrivée du LFO après le début de la note : un vibrato retardé.", "1 ms – 10 s", "1 ms – 10 s")],
       "The LFO page.", "La page LFO.") +
 fpage("lfo", "shots/pg_lfo2.png", "LFO 2 2/4", "Tempo sync and behavior.", "Synchronisation au tempo et comportement.",
       [("SYNC", "OFF (RATE sets the speed) or a note value, 4BAR to 1/32, that follows the tempo.", "OFF (RATE règle la vitesse) ou une valeur de note, de 4BAR à 1/32, qui suit le tempo.", "11 choices", "11 choix"),
        ("TRIG", "NOTE: the wave restarts at each note. FREE: it runs freely.", "NOTE : l'onde repart à chaque note. FREE : elle tourne librement.", "2 choices", "2 choix"),
        ("POL", "BI: up and down around the setting. UNI: only above it.", "BI : au-dessus et au-dessous du réglage. UNI : seulement au-dessus.", "2 choices", "2 choix")],
       "The LFO 2 page.", "La page LFO 2.") +
 fpage("lfo", "shots/pg_lfo3.png", "LFO DEST 3/4", "Where the LFO goes, and how much.",
       "Où va le LFO, et de combien.",
       [("PIT", "Pitch: vibrato.", "Hauteur : vibrato.", "−100 / +100 %", "−100 / +100 %"),
        ("FLT", "Cutoff: wah-wah.", "Coupure : wah-wah.", "−100 / +100 %", "−100 / +100 %"),
        ("SHP", "Shape (on P600: the pulse widths): the shimmer of strings.", "Forme (sur P600 : les largeurs d'impulsion) : le scintillement des cordes.", "−100 / +100 %", "−100 / +100 %"),
        ("AMP", "Volume: tremolo.", "Volume : trémolo.", "0–100 %", "0–100 %")],
       "The LFO DEST page.", "La page LFO DEST.") +
 fpage("lfo", "shots/pg_lfo4.png", "MOD 4/4", "The modulation matrix: four slots per track, each sending a source to a destination, in addition to the routings above.",
       "La matrice de modulation : quatre emplacements par piste, chacun envoyant une source vers une destination, en plus des liaisons ci-dessus.",
       [("SLOT", "Which of the four slots the other knobs edit.", "L'emplacement que modifient les autres boutons rotatifs.", "1–4", "1–4"),
        ("SRC", "The source: OFF, LFO, ENV, VEL (velocity), KEY (the note), RAND (random per note), MODW (mod wheel), AT (aftertouch), EXPR (expression pedal), S&H, SLEW (a smoothed S&H).", "La source : OFF, LFO, ENV, VEL (vélocité), KEY (la note), RAND (au hasard à chaque note), MODW (molette), AT (aftertouch), EXPR (pédale d'expression), S&H, SLEW (un S&H adouci).", "11 choices", "11 choix"),
        ("DST", "The destination: PITCH, CUT, SHP, AMP, PAN, the effect sends DIST CHO DLY REV, RATE (the LFO's speed), VIB (vibrato depth), E1 to E8 (the engine's own settings), DEPTH (the LFO's depth), VEL (the note's velocity), TIME (a step plays slightly late).", "La destination : PITCH, CUT, SHP, AMP, PAN, les envois d'effets DIST CHO DLY REV, RATE (vitesse du LFO), VIB (profondeur du vibrato), E1 à E8 (les réglages du moteur), DEPTH (profondeur du LFO), VEL (vélocité de la note), TIME (un pas joue légèrement en retard).", "23 choices", "23 choix"),
        ("AMT", "The amount, positive or negative.", "La quantité, positive ou négative.", "−100 / +100 %", "−100 / +100 %")],
       "The MOD page.", "La page MOD.") +
 LI([("<b>On a P600 track, slots 3 and 4 belong to the sound</b>: VEL › CUT (EXTRAS › VEL>FLT) and MODW › DEPTH (EXTRAS › WHEEL). Loading a P600 sound resets them. Slots 1 and 2 are free for your own modulations; loading a sound clears them too. Only a USER place or a project keeps them, not a P600 place.",
      "<b>Sur une piste P600, les emplacements 3 et 4 appartiennent au son</b> : VEL › CUT (EXTRAS › VEL>FLT) et MODW › DEPTH (EXTRAS › WHEEL). Chaque chargement de son P600 les réinitialise. Les emplacements 1 et 2 sont libres pour les vôtres ; tout chargement de son les efface aussi. Seuls un emplacement USER ou un projet les gardent, pas une place P600."),
     ("MODW, AT and EXPR come from a MIDI keyboard (or SELECT = MODW for the mod wheel). Until a value is received, MODW and AT are at 0 and EXPR at full.",
      "MODW, AT et EXPR viennent d'un clavier MIDI (ou de SELECT = MODW pour la molette). Tant que rien n'est reçu, MODW et AT valent 0 et EXPR le maximum."),
     ("ENV › DEPTH gives an LFO that follows the note's envelope; LFO › RATE gives an LFO whose speed changes.",
      "ENV › DEPTH donne un LFO qui suit l'enveloppe de la note ; LFO › RATE, un LFO dont la vitesse change.")]) +
 H3("MOMENTARY: changes that snap back", "MOMENTARY : des changements qui reviennent") +
 STEPS([("On HOME, a sound or effect page, or MIXER: <b>hold LFO</b> and turn any of KNOB 1 to 4 (band: MOMENTARY [OCT+] KEEP).",
         "Sur HOME, sur une page de son ou d'effet, ou sur MIXER : <b>maintenez LFO</b> et tournez KNOB 1 à 4 (bandeau : MOMENTARY [OCT+] KEEP)."),
        ("Let go of LFO: every value returns to where it was (BACK).", "Relâchez LFO : chaque valeur revient comme avant (BACK)."),
        ("To keep the changes, press <b>OCT+</b> while still holding LFO (KEPT).", "Pour conserver les changements, appuyez sur <b>OCT+</b> sans relâcher LFO (KEPT).")]) +
 LI([("Up to eight values at once (beyond that: MOMENTARY FULL). They are not recorded as automation and do not create an undo step.",
      "Jusqu'à huit valeurs à la fois (MOMENTARY FULL au-delà). Elles ne sont pas enregistrées en automation et ne créent pas d'annulation."),
     ("Opening the menu, a dialog or a quick screen, or loading another sound on that track, also reverts them.",
      "Ouvrir le menu, un dialogue, un écran rapide ou charger un autre son sur cette piste annule aussi ces changements."),
     ("A tap on LFO after a MOMENTARY turn does not change the page.", "Un appui sur LFO après un réglage en MOMENTARY ne change pas de page.")]) +
 felucca("Features", "Felucca's features page describes the envelope, the LFO and the modulation matrix of the original firmware.",
         "La page des fonctions de Felucca décrit l'enveloppe, le LFO et la matrice de modulation du firmware d'origine."))
