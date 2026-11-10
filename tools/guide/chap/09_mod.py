# 09 · MOD: modulations, LFO, voice, envelope
CH("mod", "MOD: modulations", "MOD : les modulations",
 P2("The MOD page gathers what moves the sound beyond the Prophet-600's panel: the modulation matrix, the LFO's other settings, the voice modes and the envelope's destinations. "
    "ACTIVE, on the right, lists everything that modulates the sound now.",
    "La page MOD rassemble ce qui fait bouger le son au-delà de la façade du Prophet-600 : la matrice de modulation, les autres réglages du LFO, les modes de voix et les destinations de l'enveloppe. "
    "ACTIVE, à droite, liste tout ce qui module le son en ce moment.") +
 SHOT("mod", "The MOD page.", "La page MOD.") +
 BOX("note", ("Loading a P600 sound resets this page, except TO AMP and the amounts of slots 3 and 4. Keep your settings with STORE THE TRACK'S SOUND (a USER sound) or a project (chapter {ch:projects}).",
              "Charger un son P600 réinitialise cette page, sauf TO AMP et les quantités des emplacements 3 et 4. Gardez vos réglages avec STORE THE TRACK'S SOUND (un son USER) ou un projet (chapitre {ch:projects}).")) +
 H3("MOD MATRIX", "MOD MATRIX", FAM["lfo"]) +
 P2("The modulation matrix: four slots per track, each sending a source to a destination, in addition to the routings above.",
    "La matrice de modulation : quatre emplacements par piste, chacun envoyant une source vers une destination, en plus des liaisons ci-dessus.") +
 CTL3([("SOURCE", "The source: OFF, LFO, ENV, VEL (velocity), KEY (the note), RAND (random per note), MODW (mod wheel), AT (aftertouch), EXPR (expression pedal), S&H, SLEW (a smoothed S&H).",
        "La source : OFF, LFO, ENV, VEL (vélocité), KEY (la note), RAND (au hasard à chaque note), MODW (molette), AT (aftertouch), EXPR (pédale d'expression), S&H, SLEW (un S&H adouci).", "11 choices", "11 choix"),
       ("DESTINATION", "The destination: PITCH, CUT, SHP, AMP, PAN, the effect sends DIST CHO DLY REV, RATE (the LFO's speed), VIB (vibrato depth), the P600's own settings (WAVE A, FREQ A, WAVE B, FREQ B, CUTOFF, RESONANCE, MIXER, ENV AMOUNT), DEPTH (the LFO's depth), VEL (the note's velocity), TIME (a step plays slightly late).",
        "La destination : PITCH, CUT, SHP, AMP, PAN, les envois d'effets DIST CHO DLY REV, RATE (vitesse du LFO), VIB (profondeur du vibrato), les réglages propres au P600 (WAVE A, FREQ A, WAVE B, FREQ B, CUTOFF, RESONANCE, MIXER, ENV AMOUNT), DEPTH (profondeur du LFO), VEL (vélocité de la note), TIME (un pas joue légèrement en retard).", "23 choices", "23 choix"),
       ("AMOUNT", "The amount, positive or negative. A double click: 0.", "La quantité, positive ou négative. Un double clic : 0.", "−100 / +100 %", "−100 / +100 %")]) +
 LI([("Fields ◀ ▶: click an arrow, or scroll over the field. After the last value comes the first.",
      "Champs ◀ ▶ : cliquez sur une flèche, ou faites défiler au-dessus du champ. Après la dernière valeur revient la première."),
     ("<b>On a P600 track, slots 3 and 4 belong to the sound</b>: VEL › CUT (EXTRAS › VEL > FLT on the SOUND page) and MODW › DEPTH (EXTRAS › WHEEL). Their amounts are those knobs. Slots 1 and 2 are free for your own modulations.",
      "<b>Sur une piste P600, les emplacements 3 et 4 appartiennent au son</b> : VEL › CUT (EXTRAS › VEL > FLT sur la page SOUND) et MODW › DEPTH (EXTRAS › WHEEL). Leurs quantités sont ces boutons. Les emplacements 1 et 2 sont libres pour les vôtres."),
     ("MODW, AT and EXPR come from a MIDI keyboard (or SELECT = MODW for the mod wheel). Until a value is received, MODW and AT are at 0 and EXPR at full.",
      "MODW, AT et EXPR viennent d'un clavier MIDI (ou de SELECT = MODW pour la molette). Tant que rien n'est reçu, MODW et AT valent 0 et EXPR le maximum."),
     ("The editor's MOD wheel, under the keyboard, also drives MODW.", "La molette MOD de l'éditeur, sous le clavier, pilote aussi MODW.")]) +
 H3("LFO", "LFO", FAM["lfo"]) +
 CTL3([("SYNC", "OFF (FREQUENCY on the SOUND page sets the speed) or a note value, 4BAR to 1/32, that follows the tempo.", "OFF (FREQUENCY sur la page SOUND règle la vitesse) ou une valeur de note, de 4BAR à 1/32, qui suit le tempo.", "11 choices", "11 choix"),
       ("TRIG", "NOTE: the wave restarts at each note. FREE: it runs freely.", "NOTE : l'onde repart à chaque note. FREE : elle tourne librement.", "2 choices", "2 choix"),
       ("POLARITY", "BI: up and down around the setting. UNI: only above it.", "BI : au-dessus et au-dessous du réglage. UNI : seulement au-dessus.", "2 choices", "2 choix"),
       ("PHASE", "Where the wave starts at each note.", "Où l'onde commence à chaque note.", "0–127", "0–127"),
       ("FADE", "Time for the LFO to come in after the note starts: a delayed vibrato.", "Temps d'arrivée du LFO après le début de la note : un vibrato retardé.", "1 ms – 10 s", "1 ms – 10 s"),
       ("TO AMP", "Volume: tremolo.", "Volume : trémolo.", "0–100 %", "0–100 %")]) +
 H3("VOICE", "VOICE", FAM["vce"]) +
 CTL3([("MODE", "POLY (up to six notes), MONO (one note, each note restarts the envelopes), LEGATO (one note, the envelopes restart only after a gap), UNISON (all the voices on one note: the SOUND page's UNISON).",
        "POLY (jusqu'à six notes), MONO (une note, chaque note relance les enveloppes), LEGATO (une note, les enveloppes ne repartent qu'après un silence), UNISON (toutes les voix sur une note : l'UNISON de la page SOUND).", "4 modes", "4 modes"),
       ("GLIDE", "How the glide is timed: RATE (a constant speed: a wide interval takes longer) or TIME (always the same time).", "Mode du glide : RATE (vitesse constante : un grand intervalle prend plus de temps) ou TIME (toujours le même temps).", "2 choices", "2 choix"),
       ("PRIORITY", "In MONO and LEGATO, which note sounds when you hold several: LAST, LOW or HIGH.", "En MONO et LEGATO, la note qui sonne quand vous en tenez plusieurs : LAST (la dernière), LOW (la plus grave) ou HIGH (la plus aiguë).", "3 choices", "3 choix"),
       ("VOICES", "How notes take voices: ROTATE (in rotation, so a note's release keeps ringing) or REUSE (a repeated note takes its own voice back).", "Attribution des voix : ROTATE (à tour de rôle : la fin d'une note continue ainsi de sonner) ou REUSE (une note répétée reprend sa propre voix).", "2 choices", "2 choix")]) +
 P2("The four tracks share the FM-1's eight voices: a P600 track takes six at most, fewer if the other tracks are playing many notes.",
    "Les quatre pistes se partagent les huit voix du FM-1 : une piste P600 en prend six au plus, moins si les autres pistes jouent beaucoup de notes.") +
 H3("ENVELOPE", "ENVELOPE", FAM["env"]) +
 P2("The amplifier's envelope (AMPLIFIER on the SOUND page) also moves other settings, by a positive or negative amount.",
    "L'enveloppe de l'amplificateur (AMPLIFIER sur la page SOUND) fait aussi bouger d'autres réglages, d'une quantité positive ou négative.") +
 CTL3([("SYNC", "ON: ATTACK, DECAY and RELEASE become note values (1/16, 1/4, 2BAR…) that follow the tempo.", "ON : ATTACK, DECAY et RELEASE deviennent des valeurs de notes (1/16, 1/4, 2BAR…) qui suivent le tempo.", "OFF / ON", "OFF / ON"),
       ("TO FILTER", "To the cutoff, on top of the filter's own envelope.", "Vers la coupure, en plus de l'enveloppe propre au filtre.", "−100 / +100 %", "−100 / +100 %"),
       ("TO PITCH", "To the pitch.", "Vers la hauteur.", "−100 / +100 %", "−100 / +100 %"),
       ("TO SHAPE", "To the pulse widths.", "Vers les largeurs d'impulsion.", "−100 / +100 %", "−100 / +100 %")]) +
 H3("ACTIVE", "ACTIVE", EDC["sound"]) +
 P2("Every modulation at work, as <i>source</i> → <i>destination</i> and its amount: the matrix slots in use, the LFO's destinations (SOUND page and TO AMP), the POLY-MOD and the envelope's destinations. — : none.",
    "Chaque modulation à l'œuvre, sous la forme <i>source</i> → <i>destination</i> et sa quantité : les emplacements de la matrice utilisés, les destinations du LFO (page SOUND et TO AMP), la POLY-MOD et les destinations de l'enveloppe. — : aucune.") +
 QA([("A modulation does nothing.", "Une modulation ne fait rien.",
      "Its SOURCE, DESTINATION or AMOUNT is at OFF or 0; MODW, AT and EXPR need a MIDI keyboard or the editor's MOD wheel.",
      "Sa SOURCE, sa DESTINATION ou son AMOUNT est sur OFF ou 0 ; MODW, AT et EXPR demandent un clavier MIDI ou la molette MOD de l'éditeur."),
     ("My modulations are gone.", "Mes modulations ont disparu.",
      "A P600 sound was loaded: it resets the page. Keep them in a USER sound or a project.",
      "Un son P600 a été chargé : il réinitialise la page. Gardez-les dans un son USER ou un projet.")]))
