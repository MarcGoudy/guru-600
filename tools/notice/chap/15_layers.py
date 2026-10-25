# 15 · The quick screens (layers)
FXKEYS = [("F3", "REPEAT 1/8"), ("G3", "REPEAT 1/16"), ("A3", "REPEAT 1/32"), ("B3", "REVERSE"), ("C4", "LPF"), ("D4", "HPF"),
          ("E4", "TAPE STOP"), ("F4", "FREEZE"), ("G4", "OCT UP"), ("A4", "OCT DN"), ("B4", "FLANGER"), ("C5", "PHASER"),
          ("D5", "REV THROW"), ("E5", "ECHO THROW"), ("F5", "—"), ("G5", "—")]
CH("layers", "The quick screens", "Les écrans rapides",
 P2("Hold <b>FX, GLO, SCL, EDIT, SEQ</b> or <b>REC</b> to open its <b>quick screen</b>: shortcuts on the keys and the four knobs. Let go to close it. While the button is held, the keys are shortcuts and make no sound.",
    "Maintenez <b>FX, GLO, SCL, EDIT, SEQ</b> ou <b>REC</b> pour ouvrir son <b>écran rapide</b> : des raccourcis sur les touches et les quatre boutons rotatifs. Relâchez pour le fermer. Tant que le bouton est maintenu, les touches servent de raccourcis et ne sonnent pas.") +
 '<div class="key">' + H3("Opening, keeping open, closing", "Ouvrir, garder ouvert, fermer") +
 LI([("<b>Hold</b> the button: the screen opens after 0.4 s (MENU › CONTROL › HOLD: 0.3 to 0.6 s).",
      "<b>Maintenez</b> le bouton : l'écran s'ouvre après 0,4 s (MENU › CONTROL › HOLD : de 0,3 à 0,6 s)."),
     ("Press a key or turn a knob with the button held: the map opens immediately and the action is performed. The button's own page does not open.",
      "Appuyez sur une touche ou tournez un bouton rotatif en maintenant le bouton : la carte s'ouvre aussitôt et l'action est exécutée. La page du bouton ne s'ouvre pas."),
     ("<b>Keep it open</b>: hold the button for more than 1 s without touching anything else, then let go. It stays open (padlock beside its name). Keys, knobs and OCT− then act as if the button were held.",
      "<b>Le garder ouvert</b> : maintenez le bouton plus de 1 s, sans rien toucher d'autre, et relâchez. Il reste ouvert (cadenas à côté de son nom). Les touches, les boutons rotatifs et OCT− agissent alors comme si le bouton était maintenu."),
     ("GLO and REC also stay open with a double tap. On REC, the double tap also cancels the arming the first tap did.", "GLO et REC restent aussi ouverts avec un double appui. Sur REC, le double appui annule aussi l'armement fait par le premier appui."),
     ("<b>Close it</b>: tap its button. Any other page button, HOME or SAVE also closes it, then performs its usual function. PLAY, REC and OCT± do not close it.",
      "<b>Le fermer</b> : appuyez sur son bouton. Tout autre bouton de page, HOME ou SAVE le ferme aussi, puis remplit sa fonction habituelle. PLAY, REC et OCT± ne le ferment pas."),
     ("<b>OCT−</b> (GLO, SCL, EDIT, SEQ, REC) undoes everything changed in the quick screen since it opened: MIX PUT BACK, SCALE PUT BACK, SEQUENCE PUT BACK…",
      "<b>OCT−</b> (GLO, SCL, EDIT, SEQ, REC) annule tout ce que l'écran rapide a modifié depuis son ouverture : MIX PUT BACK, SCALE PUT BACK, SEQUENCE PUT BACK…"),
     ("One quick screen at a time. With a button held, ALGORITHM, HOME, SAVE and the other page buttons do nothing; PLAY and REC still work.",
      "Un seul écran rapide à la fois. Tant qu'un bouton est maintenu, ALGORITHM, HOME, SAVE et les autres boutons de page ne font rien ; PLAY et REC fonctionnent toujours."),
     ("In the map, a lit key is in effect now, a breathing key can be pressed, a dark key does nothing.",
      "Sur la carte, une touche allumée est active, une touche qui respire peut être pressée, une touche éteinte ne fait rien."),
     ("KNOB 1 to 4 do nothing for a quarter of a second after a quick screen closes.",
      "KNOB 1 à 4 ne font rien pendant un quart de seconde après la fermeture d'un écran rapide.")]) + '</div>' +
 H3("EDIT: engines and sound", "EDIT : moteurs et son") +
 '<div class="split">' + shot("shots/ly_edit.png", "EDIT held: [EDIT] SET.", "EDIT maintenu : [EDIT] SET.", 240) + '<div>' +
 LI([("<b>White keys</b>, from F3: the engines, in order: P600, ANALOG, FM6, PHASE, LOFI, SAMPLE, VOICE, TRIO, WHEEL, GRAIN, PHYS, NOISE, SLICE, DRUM. A key switches the track to that engine with its first sound. <b>Careful</b>: this replaces the track's sound (hold SAVE to undo). The key of the track's current engine does nothing.",
      "<b>Touches blanches</b>, depuis F3 : les moteurs, dans l'ordre : P600, ANALOG, FM6, PHASE, LOFI, SAMPLE, VOICE, TRIO, WHEEL, GRAIN, PHYS, NOISE, SLICE, DRUM. Une touche fait passer la piste sur ce moteur avec son premier son. <b>Attention</b> : cela remplace le son de la piste (maintenez SAVE pour annuler). La touche du moteur actuel de la piste ne fait rien."),
     ("<b>F5 INIT</b>: INITIALIZE SOUND? (the engine's first sound, its defaults). <b>G5 CLEAN</b>: CLEAN INIT SOUND? (the engine's plain voice: no effects, no modulation). OCT+ confirms.",
      "<b>F5 INIT</b> : INITIALIZE SOUND? (le premier son du moteur, ses réglages d'origine). <b>G5 CLEAN</b> : CLEAN INIT SOUND? (la voix nue du moteur : ni effet, ni modulation). OCT+ confirme."),
     ("<b>Black keys</b>, on a DRUM track: mute lanes 1 to 8 (KICK, SNARE, CLAP, HATCL, HATOP, TOM, RIM, BELL); these mutes are neither recorded nor saved. Elsewhere they do nothing.",
      "<b>Touches noires</b>, sur une piste DRUM : coupent les voies 1 à 8 (KICK, SNARE, CLAP, HATCL, HATOP, TOM, RIM, BELL) ; ces coupures ne sont ni enregistrées ni conservées. Ailleurs, elles ne font rien."),
     ("<b>KNOB 1</b> ENG: the engine. <b>KNOB 2</b> No.: the engine's sounds, then your USER sounds of that engine. <b>KNOB 3</b> FAV: favorite on / off.",
      "<b>KNOB 1</b> ENG : le moteur. <b>KNOB 2</b> No. : les sons du moteur, puis vos sons USER de ce moteur. <b>KNOB 3</b> FAV : favori activé / désactivé."),
     ("<b>OCT−</b>: puts the track's sound back as it was when the quick screen opened (and the DRUM lane mutes).", "<b>OCT−</b> : remet le son de la piste tel qu'il était à l'ouverture de l'écran rapide (et les coupures des voies DRUM).")]) +
 '</div></div>' +
 H3("FX: performance effects", "FX : effets de jeu") +
 '<div class="split">' + shot("shots/ly_fx.png", "FX held: [FX] HOLD.", "FX maintenu : [FX] HOLD.", 240) + '<div>' +
 P2("While FX is held, each white key applies an effect to the whole mix for as long as the key is down; the black keys F#3, G#3, A#3 and C#4 silence tracks 1 to 4 while held.",
    "Tant que FX est maintenu, chaque touche blanche applique un effet à tout le mixage pendant qu'elle est enfoncée ; les touches noires F#3, G#3, A#3 et C#4 coupent les pistes 1 à 4 tant qu'elles sont tenues.") +
 table([("Key", "Touche"), ("Effect", "Effet")], [[a, b] for a, b in FXKEYS]) +
 '</div></div>' +
 LI([("REPEAT and REVERSE start on the next sixteenth note (immediately when stopped). An effect that cannot work at this tempo (REPEAT 1/8 or REVERSE below about 81 BPM) appears dimmed.",
      "REPEAT et REVERSE démarrent à la double croche suivante (aussitôt à l'arrêt). Un effet impossible à ce tempo (REPEAT 1/8 ou REVERSE sous environ 81 BPM) apparaît grisé."),
     ("<b>KNOB 1</b> FILTER (left low-pass, right high-pass), <b>KNOB 2</b> CRUSH, <b>KNOB 3</b> THROW (into delay and reverb), <b>KNOB 4</b> DEPTH (SHIMR while OCT UP or DN plays). They return to 0 when you let go of FX.",
      "<b>KNOB 1</b> FILTER (à gauche passe-bas, à droite passe-haut), <b>KNOB 2</b> CRUSH, <b>KNOB 3</b> THROW (vers le delay et la réverbération), <b>KNOB 4</b> DEPTH (SHIMR pendant OCT UP ou DN). Ils reviennent à 0 quand vous relâchez FX."),
     ("<b>Another effect on a key</b>: hold FX, hold the white key, turn PRESETS: the key steps through the effects and NONE (B4 FLANGER…). Press EDIT with the key held to restore its original effect. Your map is kept.",
      "<b>Un autre effet sur une touche</b> : maintenez FX, maintenez la touche blanche, tournez PRESETS : la touche passe d'un effet à l'autre, NONE compris (B4 FLANGER…). EDIT avec la touche tenue : retour à son effet d'origine. Votre carte est conservée."),
     ("MENU › CONTROL › <b>FX LATCH</b> ON: a key switches its effect on and off, the knobs keep their values ([FX] LATCH), and FX + OCT− turns everything off (FX ALL OFF). The FX light stays lit while an effect is on.",
      "MENU › CONTROL › <b>FX LATCH</b> sur ON : une touche allume et éteint son effet, les boutons rotatifs conservent leurs valeurs ([FX] LATCH), et FX + OCT− éteint tout (FX ALL OFF). Le voyant FX reste allumé tant qu'un effet est actif."),
     ("The performance effects are never recorded and never saved with a sound.", "Les effets de jeu ne sont jamais enregistrés ni sauvegardés avec un son.")]) +
 H3("GLO: the mix and the tempo", "GLO : le mixage et le tempo") +
 '<div class="split">' + shot("shots/ly_glo.png", "GLO held: [GLO] SET.", "GLO maintenu : [GLO] SET.", 240) + '<div>' +
 LI([("<b>F3, G3, A3, B3</b>: SOLO tracks 1 to 4 while held.", "<b>F3, G3, A3, B3</b> : SOLO des pistes 1 à 4 tant qu'elles sont tenues."),
     ("<b>Black keys F#3, G#3, A#3, C#4</b>: MUTE tracks 1 to 4 on / off (lit: the track is audible).", "<b>Touches noires F#3, G#3, A#3, C#4</b> : MUTE des pistes 1 à 4, activé / désactivé (touche allumée : la piste sonne)."),
     ("<b>C4</b> ALL: unmute every track. <b>D4</b> LEARN: MIDI LEARN (chapter {ch:midi}). <b>E4</b> FILL: while held, the steps set to FILL play (chapter {ch:seq}). <b>F4</b> TAP: tap the tempo (it takes effect from the third tap; after 2 s without a tap, counting starts over).",
      "<b>C4</b> ALL : rétablit toutes les pistes. <b>D4</b> LEARN : MIDI LEARN (chapitre {ch:midi}). <b>E4</b> FILL : tant que la touche est tenue, les pas réglés sur FILL jouent (chapitre {ch:seq}). <b>F4</b> TAP : tapez le tempo (pris en compte dès le troisième appui ; après 2 s sans appui, le comptage recommence)."),
     ("<b>KNOB 1 to 4</b>: the levels of tracks 1 to 4. <b>SELECT</b>: the tempo, even with BPM LOCK. <b>PLAY</b>: RESTART from the start (GLO held: in a locked GLO screen, PLAY starts and stops as usual).",
      "<b>KNOB 1 à 4</b> : les niveaux des pistes 1 à 4. <b>SELECT</b> : le tempo, même avec BPM LOCK. <b>PLAY</b> : RESTART depuis le début (GLO maintenu : dans un écran GLO verrouillé, PLAY lance et arrête comme d'habitude)."),
     ("<b>OCT−</b>: restores the mutes, levels and tempo (MIX PUT BACK).", "<b>OCT−</b> : sourdines, niveaux et tempo reviennent comme avant (MIX PUT BACK).")]) +
 '</div></div>' +
 H3("SCL: the scale", "SCL : la gamme") +
 '<div class="split">' + shot("shots/ly_scl.png", "SCL held: [SCL] SET.", "SCL maintenu : [SCL] SET.", 240) + '<div>' +
 LI([("<b>Any key</b>: sets the scale's root to that note.", "<b>N'importe quelle touche</b> : règle la note de départ de la gamme sur cette note."),
     ("<b>KNOB 1 to 4</b>: ROOT, SCL (the scale), CHRD (the chord keys), VOIC (the voicing).",
      "<b>KNOB 1 à 4</b> : ROOT, SCL (la gamme), CHRD (les accords), VOIC (la disposition)."),
     ("<b>OCT−</b>: restores the scale and chords (SCALE PUT BACK).", "<b>OCT−</b> : gamme et accords reviennent comme avant (SCALE PUT BACK).")]) +
 '</div></div>' +
 H3("SEQ: the sequence tools", "SEQ : les outils de séquence") +
 '<div class="split">' + shot("shots/ly_seq.png", "SEQ held: [SEQ] TOOLS.", "SEQ maintenu : [SEQ] TOOLS.", 240) + '<div>' +
 LI([("<b>White keys</b>: F3 CLEAR, G3 REVERSE, A3 SHIFT left, B3 SHIFT right, C4 RANDOM, D4 COOK (a musical variation; press again for more), E4 BEAT (DRUM), F4 EUCLID, then on DRUM tracks G4 to C5 the lane's CLEAR, REVERSE, FILL and RANDOM, and D5 DOUBLE (length ×2), E5 HALF (length ÷2). On a DRUM track, a black key (1 to 8) first selects the lane the lane tools act on.",
      "<b>Touches blanches</b> : F3 CLEAR, G3 REVERSE, A3 SHIFT à gauche, B3 SHIFT à droite, C4 RANDOM, D4 COOK (une variation musicale ; un nouvel appui l'accentue), E4 BEAT (DRUM), F4 EUCLID, puis sur les pistes DRUM de G4 à C5 CLEAR, REVERSE, FILL et RANDOM de la voie, et D5 DOUBLE (longueur ×2), E5 HALF (longueur ÷2). Sur une piste DRUM, une touche noire (1 à 8) choisit d'abord la voie sur laquelle agissent les outils de voie."),
     ("<b>KNOB 1 to 4</b>: LEN (1 to 64 steps), DIV (the step's length), SWG (swing), GATE (the notes' length).",
      "<b>KNOB 1 à 4</b> : LEN (1 à 64 pas), DIV (la durée d'un pas), SWG (swing), GATE (la longueur des notes)."),
     ("<b>EUCLID</b> (F4): KNOB 1 HITS, KNOB 2 STEPS, KNOB 3 ROT; OCT+ applies, OCT− cancels. Closing the screen, F4 again or another tool key also applies it.", "<b>EUCLID</b> (F4) : KNOB 1 HITS, KNOB 2 STEPS, KNOB 3 ROT ; OCT+ applique, OCT− annule. Fermer l'écran, un nouvel appui sur F4 ou une autre touche d'outil l'appliquent aussi."),
     ("Each tool can be undone separately (hold SAVE). <b>OCT−</b>: restores the sequence as it was when the screen opened.", "Chaque outil s'annule séparément (maintenez SAVE). <b>OCT−</b> : la séquence revient telle qu'à l'ouverture de l'écran.")]) +
 '</div></div>' +
 H3("REC: recording settings", "REC : réglages d'enregistrement") +
 '<div class="split">' + shot("shots/ly_rec.png", "REC held: [REC] SET.", "REC maintenu : [REC] SET.", 240) + '<div>' +
 LI([("<b>F3</b> CLEAR: erases the track's sequence and automation (can be undone). <b>G3</b> CLICK: OFF, REC (only while recording), ON. <b>A3</b> COUNT-IN: OFF, 1 BAR, 2 BARS. <b>B3</b> LEVEL: the click's level, LOW, MID, HIGH.",
      "<b>F3</b> CLEAR : efface la séquence et l'automation de la piste (annulable). <b>G3</b> CLICK : OFF, REC (seulement pendant l'enregistrement), ON. <b>A3</b> COUNT-IN : OFF, 1 BAR, 2 BARS. <b>B3</b> LEVEL : le volume du clic, LOW, MID, HIGH."),
     ("<b>KNOB 1 to 3</b>: the same three settings as in MENU › AUDIO.", "<b>KNOB 1 à 3</b> : les trois mêmes réglages que dans MENU › AUDIO."),
     ("A tap on REC still arms recording; only holding it opens the screen.", "Un appui sur REC arme toujours l'enregistrement ; seul le maintien ouvre l'écran.")]) +
 '</div></div>' +
 felucca("Controls", "Felucca's controls page describes the quick screens (called layers there).",
         "La page des commandes de Felucca décrit les écrans rapides (appelés layers dans Felucca)."))
