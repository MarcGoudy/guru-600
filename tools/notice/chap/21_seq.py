# 21 · The sequencer (Felucca)
CH("seq", "The sequencer", "Le séquenceur",
 P2("Each track has its own sequence of up to 64 steps, with chords, ties, accents, slides, chance, velocity and repeats. <b>PLAY</b> starts and stops all four tracks together. Press <b>SEQ</b>: three pages, STEP, DETAIL and AUTOMATION.",
    "Chaque piste a sa propre séquence, jusqu'à 64 pas, avec accords, liaisons, accents, glissés, probabilité, vélocité et répétitions. <b>PLAY</b> lance et arrête les quatre pistes ensemble. Appuyez sur <b>SEQ</b> : trois pages, STEP, DETAIL et AUTOMATION.") +
 H3("Recording", "Enregistrer") +
 LI([("<b>Live</b>: tap <b>REC</b>; if it is stopped, the sequencer starts, with a count-in if one is set. Play: your notes are recorded in a loop, on top of what is already there.",
      "<b>En direct</b> : appuyez sur <b>REC</b> ; si le séquenceur est arrêté, il démarre, avec le décompte s'il est activé. Jouez : vos notes s'enregistrent en boucle, par-dessus ce qui est déjà enregistré."),
     ("<b>Step by step</b>: on SEQ › STEP, with the sequencer stopped, tap REC (KEYS WRITE STEPS). Each chord or note you play fills the step under the cursor, and the cursor moves on when you let go. With MENU › CONTROL › CHORD ENTRY = ADD, each key adds or removes a note and the cursor stays put.",
      "<b>Pas à pas</b> : sur SEQ › STEP, le séquenceur étant arrêté, appuyez sur REC (KEYS WRITE STEPS). Chaque note ou accord joué remplit le pas sous le curseur, et le curseur avance quand vous relâchez. MENU › CONTROL › CHORD ENTRY ADD : chaque touche ajoute ou retire une note, et le curseur ne bouge pas."),
     ("Tap REC again to stop recording. Your timing is kept as a NUDGE per step; with the track's QUANTIZE ON (the default) the steps play on the grid.",
      "Appuyez de nouveau sur REC pour arrêter l'enregistrement. Votre placement rythmique est conservé sous forme de NUDGE pour chaque pas ; avec le QUANTIZE de la piste sur ON (le réglage d'origine), les pas jouent sur la grille."),
     ("Click and count-in: set them in the REC quick screen or in MENU › AUDIO (chapter {ch:layers}). The count-in (internal clock only) shows COUNT-IN, the bar (1 BAR, BAR 1 OF 2…) and the beats; PLAY cancels it. A note played in the last eighth of the count-in is recorded on step 1.", "Clic et décompte : dans l'écran rapide REC ou dans MENU › AUDIO (chapitre {ch:layers}). Le décompte (horloge interne seulement) affiche COUNT-IN, la mesure (1 BAR, BAR 1 OF 2…) et les temps ; PLAY l'annule. Une note jouée dans le dernier huitième du décompte s'enregistre sur le pas 1.")]) +
 page("osc", "shots/pg_seq1.png", "SEQ › STEP", "SEQ › STEP", "The piano roll of the track's steps; its title shows the scale (C CHR).",
      "Le piano roll des pas de la piste ; son titre indique la gamme (C CHR).",
      [("STEP", "The cursor (also PRESETS).", "Le curseur (aussi PRESETS).", "1–64", "1–64"),
       ("NOTE", "Transposes the step's notes (on an empty step: writes the last note).", "Transpose les notes du pas (sur un pas vide : écrit la dernière note).", "st", "st"),
       ("TIME / LEN", "On a note: its length in steps (ties after it). Otherwise: NOTE, TIE or REST.", "Sur une note : sa longueur en pas (liaisons après elle). Sinon : NOTE, TIE ou REST.", "1–64", "1–64"),
       ("FLAG", "—, ACC (accent), SLD (slide), A+S.", "—, ACC (accent), SLD (glissé), A+S.", "4 choices", "4 choix")],
      "SEQ › STEP.", "SEQ › STEP.") +
 LI([("<b>EDIT</b> on STEP: clears the step under the cursor and moves on (STEP CLEARED).", "<b>EDIT</b> sur STEP : efface le pas sous le curseur et avance (STEP CLEARED)."),
     ("<b>Parameter lock</b>: while entering a step (keys held) or holding a drum step, turn KNOB 1 to 4: that step gets its own value for the setting those knobs controlled on the sound page you last viewed. EDIT with the step held clears its locks. PRESETS with steps held sets their NUDGE.",
      "<b>Verrou de paramètre</b> : pendant la saisie d'un pas (touches tenues) ou en tenant un pas de batterie, tournez KNOB 1 à 4 : ce pas reçoit sa propre valeur pour le réglage que ces boutons pilotaient sur la dernière page de son affichée. EDIT, pas tenu, efface ses verrous. PRESETS, pas tenus, règle leur NUDGE."),
     ("<b>DRUM track</b>: STEP is a grid (GRID). White keys = the 16 steps of the page shown; black keys 1 to 8 = the lanes, 9 held = accent, 10 and 11 = page down and up. Knobs: STEP, LANE, HIT, ACC.",
      "<b>Piste DRUM</b> : STEP est une grille (GRID). Touches blanches = les 16 pas de la page affichée ; touches noires 1 à 8 = les voies, la 9 tenue = accent, 10 et 11 = page précédente et suivante. Boutons rotatifs : STEP, LANE, HIT, ACC."),
     ("MENU › CONTROL › STEP PREVIEW ON: moving the cursor plays the step.", "MENU › CONTROL › STEP PREVIEW sur ON : déplacer le curseur joue le pas.")]) +
 page("osc", "shots/pg_seq2.png", "SEQ › DETAIL", "SEQ › DETAIL", "The step under the cursor, in detail. PRESETS moves the cursor.",
      "Le pas sous le curseur, en détail. PRESETS déplace le curseur.",
      [("CHANCE", "How often it plays (0–100 %), or a condition: 1:2, 2:2, 1:3… (loop 1 of 2…), FILL (only with GLO + E4 held), !FILL (only when they are not held).", "Sa fréquence de jeu (0–100 %), ou une condition : 1:2, 2:2, 1:3… (boucle 1 sur 2…), FILL (seulement quand GLO + E4 sont tenus), !FILL (seulement quand ils ne le sont pas).", "%, conditions", "%, conditions"),
       ("RATCH", "Plays the step 1 to 4 times within its length.", "Le pas joué 1 à 4 fois dans sa durée.", "x1–x4", "x1–x4"),
       ("NUDGE", "Early or late, in sixteenths of a step (applies only with QUANTIZE OFF).", "En avance ou en retard, en seizièmes de pas (appliqué seulement avec QUANTIZE OFF).", "−8 / +7", "−8 / +7"),
       ("VEL", "The step's velocity.", "La vélocité du pas.", "1–127", "1–127")],
      "SEQ › DETAIL.", "SEQ › DETAIL.") +
 P2("EDIT on DETAIL resets the step to 100 %, x1, 0 and 96 (STEP RESET).", "EDIT sur DETAIL : le pas revient à 100 %, x1, 0 et 96 (STEP RESET).") +
 '<div class="split">' + shot("shots/pg_seq3.png", "SEQ › AUTOMATION.", "SEQ › AUTOMATION.", 240) + '<div>' +
 P2("The list of everything on the track's steps: PLAY and QUANTIZE, the locks, the recorded knob moves and the steps' details (CHANCE, RATCH, NUDGE, VEL). KNOB 1 (or PRESETS) chooses the row; the other cards give its step, setting and value. The PLAY row switches the whole automation on or off; QUANTIZE ON plays every step on the grid, OFF plays the NUDGEs.",
    "La liste de tout ce qui figure sur les pas de la piste : PLAY et QUANTIZE, les verrous, les mouvements de boutons enregistrés et les détails des pas (CHANCE, RATCH, NUDGE, VEL). KNOB 1 (ou PRESETS) choisit la ligne ; les autres cartes donnent son pas, son réglage et sa valeur. La ligne PLAY active ou coupe toute l'automation ; QUANTIZE sur ON joue chaque pas sur la grille, sur OFF, il applique les NUDGE.") +
 '</div></div>' +
 LI([("<b>Recording knob moves</b>: arm the track and play: every knob you turn is recorded step by step.",
      "<b>Enregistrer des mouvements de boutons</b> : armez la piste et jouez : chaque bouton rotatif tourné s'enregistre pas à pas."),
     ("OCT+ on + ADD adds a lock or a detail; on a record, switches it between lock and automation; on PLAY, asks CLEAR T1 AUTOMATION?. EDIT deletes the row.",
      "OCT+ sur + ADD ajoute un verrou ou un détail ; sur un enregistrement, change un verrou en automation ou l'inverse ; sur PLAY, demande CLEAR T1 AUTOMATION?. EDIT supprime la ligne."),
     ("128 records at most, shared by the four tracks (AUTOMATION FULL).", "128 enregistrements au plus, partagés par les quatre pistes (AUTOMATION FULL).")]) +
 H3("Length, speed and tools", "Longueur, vitesse et outils") +
 P2("Hold <b>SEQ</b> on any page: KNOB 1 to 4 set LEN (1 to 64 steps), DIV (the step's length, 4 bars to 1/32), SWG (swing) and GATE, and the white keys are the tools: CLEAR, REVERSE, SHIFT, RANDOM, COOK, EUCLID, DOUBLE, HALF… (chapter {ch:layers}). Every edit can be undone by holding SAVE.",
    "Maintenez <b>SEQ</b> sur n'importe quelle page : KNOB 1 à 4 règlent LEN (1 à 64 pas), DIV (la durée d'un pas, de 4 mesures à 1/32), SWG (swing) et GATE, et les touches blanches sont les outils : CLEAR, REVERSE, SHIFT, RANDOM, COOK, EUCLID, DOUBLE, HALF… (chapitre {ch:layers}). Toute modification s'annule en maintenant SAVE.") +
 LI([("STOP TO EDIT: a song is playing (chapter {ch:song}); stop it to edit the steps.", "STOP TO EDIT : un morceau est en lecture (chapitre {ch:song}) ; arrêtez-le pour modifier les pas."),
     ("Changing the sound never changes the sequence; loading a phrase (SAVE › PHRASES) replaces it, after confirmation if it contains your own steps.",
      "Changer de son ne change jamais la séquence ; charger une phrase (SAVE › PHRASES) la remplace, après confirmation si elle contient vos propres pas.")]) +
 felucca("Features", "Felucca's features page describes the sequencer, the locks and the automation in detail.",
         "La page des fonctions de Felucca décrit en détail le séquenceur, les verrous et l'automation."))
