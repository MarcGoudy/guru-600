# 14 · Scales, chords and the chord memory
CH("chords", "Scales, chords and the chord memory", "Gammes, accords et mémoire d'accords",
 P2("Press <b>SCL</b>: two pages, SCL (the scale) and CHORD (the chord keys). Both act on the selected track; on a DRUM track the keys keep their drum mapping.",
    "Appuyez sur <b>SCL</b> : deux pages, SCL (la gamme) et CHORD (les accords). Les deux agissent sur la piste choisie ; sur une piste DRUM, les touches gardent leur répartition de batterie.") +
 page("osc", "shots/pg_scl1.png", "SCL 1/2", "SCL 1/2", "The scale the keys play in.", "La gamme dans laquelle jouent les touches.",
      [("ROOT", "The scale's root note, C to B.", "La note de départ de la gamme, de C à B.", "12 notes", "12 notes"),
       ("SCL", "The scale: CHR (chromatic: no scale), MAJ, MIN, DOR, MIX, PEN, MPEN, HARM, PHRY, LYD, LOC, MEL, BLUES, WHOLE, DIMHW, DIMWH.", "La gamme : CHR (chromatique : pas de gamme), MAJ, MIN, DOR, MIX, PEN, MPEN, HARM, PHRY, LYD, LOC, MEL, BLUES, WHOLE, DIMHW, DIMWH.", "16 scales", "16 gammes"),
       ("QNT", "How the keys follow the scale: OFF (every key plays its own note), SNAP (a note outside the scale is moved down into it), WHITE (the scale on the white keys only: C4 plays ROOT, the black keys are silent), SEQ (like SNAP, and the sequence also plays in the scale), SEQ+T (like SEQ, and TRN transposes the sequence too).", "Comment les touches suivent la gamme : OFF (chaque touche joue sa note), SNAP (une note hors gamme est ramenée dans la gamme, vers le bas), WHITE (la gamme sur les seules touches blanches : C4 joue ROOT, les noires sont muettes), SEQ (comme SNAP, et la séquence joue aussi dans la gamme), SEQ+T (comme SEQ, et TRN transpose aussi la séquence).", "5 modes", "5 modes"),
       ("TRN", "Transposes what the keys play, in semitones.", "Transpose ce que jouent les touches, en demi-tons.", "−24 / +24 st", "−24 / +24 st")],
      "The SCL page.", "La page SCL.") +
 LI([("MENU › CONTROL › <b>SCALE LEDS</b> ON lights the keys of the scale.", "MENU › CONTROL › <b>SCALE LEDS</b> sur ON éclaire les touches de la gamme."),
     ("<b>The keys play strange notes?</b> SCL is not on CHR, QNT is not OFF, or TRN is not 0: reset them.", "<b>Les touches jouent des notes étranges ?</b> SCL n'est pas sur CHR, QNT pas sur OFF, ou TRN pas à 0 : rétablissez ces réglages."),
     ("Hold SCL to open a quick screen where a key sets the root instantly (chapter {ch:layers}).", "Maintenu, SCL ouvre un écran rapide où une touche règle aussitôt la note de départ (chapitre {ch:layers}).")]) +
 page("osc", "shots/pg_scl2.png", "CHORD 2/2", "CHORD 2/2", "One finger plays a chord. Press SCL again.", "Un doigt joue un accord. Appuyez de nouveau sur SCL.",
      [("CHRD", "The chord keys: OFF, DIA3 (the scale's triads: every chord is in key), DIA7 (the scale's sevenths), MAJ, MIN, DOM7, MAJ7, MIN7, SUS4, POW (fixed shapes on every key), MEM (your own chord, below).", "Les accords : OFF, DIA3 (les triades de la gamme : chaque accord est dans la tonalité), DIA7 (les septièmes de la gamme), MAJ, MIN, DOM7, MAJ7, MIN7, SUS4, POW (des formes fixes sur chaque touche), MEM (votre propre accord, ci-dessous).", "11 choices", "11 choix"),
       ("VOIC", "The voicing: CLOSE, OPEN (spread out), INV1, INV2 (inversions), +OCT (the root added an octave below; a seventh then drops its fifth).", "La disposition : CLOSE (serré), OPEN (écarté), INV1, INV2 (renversements), +OCT (la fondamentale ajoutée à l'octave inférieure ; une septième perd alors sa quinte).", "5 choices", "5 choix"),
       ("LEARN", "The chord memory: turn right to select LEARN, then press OCT+.", "La mémoire d'accords : tournez à droite pour choisir LEARN, puis OCT+.", "action", "action")],
      "The CHORD page.", "La page CHORD.") +
 P2("DIA3 and DIA7 follow the scale set on the SCL page (with SCL on CHR, the major scale of ROOT); a key outside the scale takes the scale note below it. A chord uses as many voices as it has notes. In MONO, LEG or UNI, the track plays only the chord's root; DRUM and SLICE tracks ignore the chord keys.",
    "DIA3 et DIA7 suivent la gamme réglée sur la page SCL (avec SCL sur CHR, la gamme majeure de ROOT) ; une touche hors gamme prend la note de la gamme juste en dessous. Un accord utilise autant de voix qu'il a de notes. En MONO, LEG ou UNI, la piste ne joue que la fondamentale de l'accord ; les pistes DRUM et SLICE ignorent les accords.") +
 H3("The chord memory (MEM)", "La mémoire d'accords (MEM)") +
 P2("Play a chord of up to four notes once: each key then plays that chord built on it.",
    "Jouez une fois un accord de quatre notes au plus : chaque touche joue ensuite cet accord bâti sur elle.") +
 STEPS([("On the CHORD page, turn <b>KNOB 3</b> right (LEARN).",
         "Sur la page CHORD, tournez <b>KNOB 3</b> à droite (LEARN)."),
        ("Press <b>OCT+</b>: PLAY THE CHORD.",
         "Appuyez sur <b>OCT+</b> : PLAY THE CHORD."),
        ("Play the notes of your chord, together or one after the other (four different notes at most).",
         "Jouez les notes de votre accord, ensemble ou l'une après l'autre (quatre notes différentes au plus)."),
        ("Press <b>OCT+</b> again: CHORD KEPT: MEM. Each key plays your chord.",
         "Appuyez de nouveau sur <b>OCT+</b> : CHORD KEPT: MEM. Chaque touche joue votre accord.")]) +
 LI([("The chord's shape is measured from its lowest note: C E G B gives a major seventh chord on every key.",
      "La forme de l'accord se mesure depuis sa note la plus grave : C E G B donne un accord de septième majeure sur chaque touche."),
     ("The notes may span more than an octave (up to 31 semitones above the lowest).", "Les notes peuvent couvrir plus d'une octave (jusqu'à 31 demi-tons au-dessus de la plus grave)."),
     ("No note played before the second OCT+: NO NOTE, nothing changes. Leaving the page cancels the learning.",
      "Aucune note jouée avant le second OCT+ : NO NOTE, rien ne change. Quitter la page annule l'apprentissage."),
     ("The chord memory belongs to the track: it stays when you change sounds, and it is saved with the project. VOIC applies to it too.",
      "La mémoire d'accords appartient à la piste : elle reste quand vous changez de son, et elle est enregistrée avec le projet. VOIC s'y applique aussi."),
     ("Back to normal keys: CHRD = OFF. Your chord stays in memory: CHRD = MEM brings it back.",
      "Retour aux touches normales : CHRD = OFF. Votre accord reste en mémoire : CHRD = MEM le ramène."),
     ("On the CHORD page, OCT− and OCT+ do not change the octave: they control the LEARN action.",
      "Sur la page CHORD, OCT− et OCT+ ne changent pas l'octave : ils pilotent l'action LEARN.")]) +
 felucca("Scale-Keyboard", "Felucca's scale keyboard page describes the scales, QNT and the chord keys.",
         "La page du clavier à gamme de Felucca décrit les gammes, QNT et les accords."))
