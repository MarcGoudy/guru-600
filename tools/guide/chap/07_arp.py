# 07 · ARP: the arpeggiator, the scale and the chord keys
CH("arp", "ARP: arpeggiator, scale and chords", "ARP : arpégiateur, gamme et accords",
 P2("The ARP page gathers what turns the keys you play into music: the arpeggiator, the scale the keys play in, and the chord keys. "
    "These settings belong to the selected track, with any engine: they stay when you change sounds.",
    "La page ARP rassemble ce qui transforme les touches jouées en musique : l'arpégiateur, la gamme dans laquelle jouent les touches, et les accords. "
    "Ces réglages appartiennent à la piste choisie, quel que soit son moteur : ils restent quand vous changez de son.") +
 SHOT("arp", "The ARP page.", "La page ARP.") +
 H3("ARPEGGIATOR", "ARPEGGIATOR", EDC["arp"]) +
 P2("The arpeggiator plays the notes you hold one after the other, in time with the tempo. Set MODE to OFF to play normally again.",
    "L'arpégiateur joue l'une après l'autre les notes tenues, en rythme avec le tempo. Réglez MODE sur OFF pour revenir au jeu normal.") +
 CTL3([("MODE", "OFF, UP, DN, UPDN, RND, ORD (the order you pressed them), REPEAT, and for chords DNUP, UP+8, CONV, DIVG, PINKY, THUMB, WALK, CHORD.",
        "OFF, UP, DN, UPDN, RND, ORD (l'ordre d'appui), REPEAT, et pour les accords DNUP, UP+8, CONV, DIVG, PINKY, THUMB, WALK, CHORD.", "15 modes", "15 modes"),
       ("RATE", "The note value of each step, 4 bars to 1/32.", "La valeur de chaque note, de 4 mesures à 1/32.", "10 values", "10 valeurs"),
       ("OCT", "How many octaves it climbs.", "Le nombre d'octaves parcourues.", "1–4", "1–4"),
       ("GATE", "The length of each note.", "La longueur de chaque note.", "1–100 %", "1–100 %"),
       ("SWING", "Swing.", "Swing.", "0–100 %", "0–100 %"),
       ("PROB", "The chance that each note plays.", "La probabilité que chaque note joue.", "0–100 %", "0–100 %"),
       ("HOLD", "ON: the notes keep playing after you let go (latch); a new chord replaces them.", "ON : les notes continuent après le relâchement (verrouillage) ; un nouvel accord les remplace.", "OFF / ON", "OFF / ON"),
       ("ORDER", "NOTE: by pitch. PLAY: in the order you played.", "NOTE : par hauteur. PLAY : dans l'ordre joué.", "2 choices", "2 choix")]) +
 H3("SCALE", "SCALE", EDC["arp"]) +
 CTL3([("ROOT", "The scale's root note, C to B.", "La note de départ de la gamme, de C à B.", "12 notes", "12 notes"),
       ("SCALE", "The scale: CHR (chromatic: no scale), MAJ, MIN, DOR, MIX, PEN, MPEN, HARM, PHRY, LYD, LOC, MEL, BLUES, WHOLE, DIMHW, DIMWH.",
        "La gamme : CHR (chromatique : pas de gamme), MAJ, MIN, DOR, MIX, PEN, MPEN, HARM, PHRY, LYD, LOC, MEL, BLUES, WHOLE, DIMHW, DIMWH.", "16 scales", "16 gammes"),
       ("QUANTIZE", "How the keys follow the scale: OFF (every key plays its own note), SNAP (a note outside the scale is moved down into it), WHITE (the scale on the white keys only: C4 plays ROOT, the black keys are silent), SEQ (like SNAP, and the sequence also plays in the scale), SEQ+T (like SEQ, and TRANSPOSE transposes the sequence too).",
        "Comment les touches suivent la gamme : OFF (chaque touche joue sa note), SNAP (une note hors gamme est ramenée dans la gamme, vers le bas), WHITE (la gamme sur les seules touches blanches : C4 joue ROOT, les noires sont muettes), SEQ (comme SNAP, et la séquence joue aussi dans la gamme), SEQ+T (comme SEQ, et TRANSPOSE transpose aussi la séquence).", "5 modes", "5 modes"),
       ("TRANSPOSE", "Transposes what the keys play, in semitones.", "Transpose ce que jouent les touches, en demi-tons.", "−24 / +24 st", "−24 / +24 st")]) +
 P2("<b>KEY</b>, on the right: the notes of the scale, lit on one octave (the root marked with a dot), and their number.",
    "<b>KEY</b>, à droite : les notes de la gamme, allumées sur une octave (la note de départ marquée d'un point), et leur nombre.") +
 H3("CHORD", "CHORD", EDC["arp"]) +
 P2("One finger plays a chord.", "Un doigt joue un accord.") +
 CTL3([("CHORD", "The chord keys: OFF, DIA3 (the scale's triads: every chord is in key), DIA7 (the scale's sevenths), MAJ, MIN, DOM7, MAJ7, MIN7, SUS4, POW (fixed shapes on every key), MEM (your own chord, learned on the FM-1).",
        "Les accords : OFF, DIA3 (les triades de la gamme : chaque accord est dans la tonalité), DIA7 (les septièmes de la gamme), MAJ, MIN, DOM7, MAJ7, MIN7, SUS4, POW (des formes fixes sur chaque touche), MEM (votre propre accord, appris sur le FM-1).", "11 choices", "11 choix"),
       ("VOICING", "The voicing: CLOSE, OPEN (spread out), INV1, INV2 (inversions), +OCT (the root added an octave below; a seventh then drops its fifth).",
        "La disposition : CLOSE (serré), OPEN (écarté), INV1, INV2 (renversements), +OCT (la fondamentale ajoutée à l'octave inférieure ; une septième perd alors sa quinte).", "5 choices", "5 choix")]) +
 P2("DIA3 and DIA7 follow the scale set above (with SCALE on CHR, the major scale of ROOT); a key outside the scale takes the scale note below it. A chord uses as many voices as it has notes. In MONO, LEGATO or UNISON, the track plays only the chord's root; DRUM and SLICE tracks ignore the chord keys.",
    "DIA3 et DIA7 suivent la gamme réglée plus haut (avec SCALE sur CHR, la gamme majeure de ROOT) ; une touche hors gamme prend la note de la gamme juste en dessous. Un accord utilise autant de voix qu'il a de notes. En MONO, LEGATO ou UNISON, la piste ne joue que la fondamentale de l'accord ; les pistes DRUM et SLICE ignorent les accords.") +
 QA([("It plays by itself?", "Il joue tout seul ?",
      "HOLD is ON: set it to OFF, or set MODE to OFF.", "HOLD est sur ON : repassez-le sur OFF, ou réglez MODE sur OFF."),
     ("The keys play strange notes?", "Les touches jouent des notes étranges ?",
      "SCALE is not on CHR, QUANTIZE is not OFF, TRANSPOSE is not 0, or CHORD is not OFF: reset them.",
      "SCALE n'est pas sur CHR, QUANTIZE pas sur OFF, TRANSPOSE pas à 0, ou CHORD pas sur OFF : rétablissez ces réglages."),
     ("Recording your own chord (MEM).", "Enregistrer votre propre accord (MEM).",
      "It is learned on the FM-1: SCL › CHORD, LEARN (see the Guru-600 user guide).",
      "Il s'apprend sur le FM-1 : SCL › CHORD, LEARN (voir la notice du Guru-600).")]))
