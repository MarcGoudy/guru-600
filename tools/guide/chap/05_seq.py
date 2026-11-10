# 05 · SEQUENCER: the track's steps
CH("seq", "SEQUENCER: the track's steps", "SEQUENCER : les pas de la piste",
 P2("Each track has its own sequence of up to 64 steps, with chords, ties, accents, slides, chance, velocity and repeats. "
    "The SEQUENCER page shows the selected track's: its settings at the top, the notes in the middle (STEPS), the details of each step below (DETAIL), and the automation on the right. "
    "▶ at the top starts the four tracks together.",
    "Chaque piste a sa propre séquence, jusqu'à 64 pas, avec accords, liaisons, accents, glissés, probabilité, vélocité et répétitions. "
    "La page SEQUENCER montre celle de la piste choisie : ses réglages en haut, les notes au milieu (STEPS), le détail de chaque pas en dessous (DETAIL), et l'automation à droite. "
    "▶ en haut lance les quatre pistes ensemble.") +
 SHOT("seq", "The SEQUENCER page.", "La page SEQUENCER.") +
 H3("SEQUENCE", "SEQUENCE", EDC["seq"]) +
 CTL3([("LEN", "The number of steps of the sequence. The steps beyond it are dimmed.", "Le nombre de pas de la séquence. Les pas au-delà sont assombris.", "1 … 64", "1 … 64"),
       ("DIV", "The length of a step, in note values of the tempo.", "La durée d'un pas, en valeurs de notes du tempo.", "4BAR … 1/32", "4BAR … 1/32"),
       ("SWING", "Delays every other step: a shuffle.", "Retarde un pas sur deux : un balancement.", "0 … 100 %", "0 … 100 %"),
       ("GATE", "How long each note lasts, in part of its step.", "La durée de chaque note, en part de son pas.", "1 … 100 %", "1 … 100 %"),
       ("QUANTIZE", "Lit: the steps play on the grid. Unlit: they play their NUDGE (early or late, as recorded).", "Allumé : les pas jouent sur la grille. Éteint : ils jouent leur NUDGE (en avance ou en retard, comme enregistrés).", "OFF / ON", "OFF / ON"),
       ("TRANSPOSE", "Transposes what the keys play, in semitones; the sequence too when QUANTIZE on the ARP page is SEQ+T. The same as TRANSPOSE on the ARP page.", "Transpose ce que jouent les touches, en demi-tons ; la séquence aussi quand le QUANTIZE de la page ARP est sur SEQ+T. Le même que TRANSPOSE sur la page ARP.", "−24 … +24 st", "−24 … +24 st")]) +
 P2("<b>STEPS</b> 1-16, 17-32, 33-48, 49-64: the 16 steps shown. They change only the view.",
    "<b>STEPS</b> 1-16, 17-32, 33-48, 49-64 : les 16 pas affichés. Ils ne changent que l'affichage.") +
 H3("STEPS: writing notes", "STEPS : écrire des notes", EDC["seq"]) +
 LI([("<b>Click in the grid</b>: puts a note in that step at that pitch, or takes it away. A step holds up to 4 notes (a chord). A new note sounds on the FM-1 as you write it.",
      "<b>Cliquez dans la grille</b> : met une note dans ce pas à cette hauteur, ou la retire. Un pas contient jusqu'à 4 notes (un accord). Une nouvelle note sonne sur le FM-1 quand vous l'écrivez."),
     ("<b>Scroll</b> over the grid to see higher or lower notes. The keyboard on the left names each C.",
      "<b>Faites défiler</b> au-dessus de la grille pour voir des notes plus aiguës ou plus graves. Le clavier à gauche nomme chaque do (C)."),
     ("<b>Click a step's number</b> to change it: NOTE, then TIE (the previous note lasts through this step), then REST (silence).",
      "<b>Cliquez sur le numéro d'un pas</b> pour le changer : NOTE, puis TIE (la note précédente dure pendant ce pas), puis REST (silence)."),
     ("The step playing is lit as the music plays.", "Le pas joué s'éclaire pendant la lecture.")]) +
 H3("DETAIL: each step", "DETAIL : chaque pas", EDC["seq"]) +
 CTL3([("VELOCITY", "How hard the step plays: click at the height you want, or drag up or down. Only on a step with notes.",
        "La force du pas : cliquez à la hauteur voulue, ou glissez vers le haut ou le bas. Seulement sur un pas qui a des notes.", "1 … 127", "1 … 127"),
       ("ACCENT", "Click: the step plays louder.", "Cliquez : le pas joue plus fort.", "OFF / ON", "OFF / ON"),
       ("SLIDE", "Click: the note glides into the next one.", "Cliquez : la note glisse vers la suivante.", "OFF / ON", "OFF / ON"),
       ("CHANCE", "How often the step plays: drag up or down. Hidden when the step has a condition (COND).", "La fréquence de jeu du pas : glissez vers le haut ou le bas. Masqué quand le pas a une condition (COND).", "0 … 100 %", "0 … 100 %"),
       ("RATCH", "Click: the step plays 1 to 4 times within its length.", "Cliquez : le pas joue 1 à 4 fois dans sa durée.", "×1 … ×4", "×1 … ×4"),
       ("NUDGE", "Early or late, in sixteenths of a step: drag up or down. Heard only with QUANTIZE unlit.", "En avance ou en retard, en seizièmes de pas : glissez vers le haut ou le bas. Entendu seulement avec QUANTIZE éteint.", "−8 … +7", "−8 … +7"),
       ("COND", "Click to choose when the step plays: 1:2 (the first of every 2 loops), 2:2, 1:3 … 4:4, FILL (only while a fill is held on the FM-1: GLO + E4), !FILL (only when it is not). Choosing a condition puts CHANCE back to 100 %; dragging CHANCE removes the condition.",
        "Cliquez pour choisir quand le pas joue : 1:2 (la première de chaque série de 2 boucles), 2:2, 1:3 … 4:4, FILL (seulement pendant un fill tenu sur le FM-1 : GLO + E4), !FILL (seulement en dehors). Choisir une condition remet CHANCE à 100 % ; glisser CHANCE retire la condition.",
        ("—, 1:2 … 4:4, FILL, !FILL", "—, 1:2 … 4:4, FILL, !FILL")[0], "—, 1:2 … 4:4, FILL, !FILL")]) +
 P2("A double click on a detail's name (VELOCITY, ACCENT…) puts that row back to its usual value on every step of the sequence: velocity 96, ACCENT and SLIDE off, CHANCE 100 %, RATCH ×1, NUDGE 0, no COND.",
    "Un double clic sur le nom d'un détail (VELOCITY, ACCENT…) remet cette ligne à sa valeur habituelle sur tous les pas de la séquence : vélocité 96, ACCENT et SLIDE éteints, CHANCE 100 %, RATCH ×1, NUDGE 0, aucune COND.") +
 H3("TOOLS", "TOOLS", EDC["seq"]) +
 P2("They change the whole sequence of the track. On the FM-1, holding SAVE for 1 s undoes the last one.",
    "Ils modifient toute la séquence de la piste. Sur le FM-1, maintenir SAVE 1 s annule le dernier.") +
 CTL([("CLEAR", "Clears the steps, after a confirmation.", "Efface les pas, après confirmation."),
      ("REVERSE", "Plays the sequence backwards.", "Met la séquence à l'envers."),
      ("SHIFT ◀, SHIFT ▶", "Moves every step one step earlier or later (the last comes back at the start).", "Décale tous les pas d'un pas plus tôt ou plus tard (le dernier revient au début)."),
      ("RANDOM", "New notes taken from the track's scale (ARP page), on the same rhythm. On a DRUM track: a new beat.", "De nouvelles notes prises dans la gamme de la piste (page ARP), sur le même rythme. Sur une piste DRUM : un nouveau rythme."),
      ("COOK", "A musical variation of the sequence; click again for more.", "Une variation musicale de la séquence ; un nouveau clic l'accentue."),
      ("EUCLID", "Spreads a number of hits as evenly as possible over a cycle of steps, turned by a rotation, through the whole LEN. Type the hits, the steps and the rotation (for example <b>5 16 0</b>) and confirm. A hit keeps the step's note (or takes the scale's root); the other steps are emptied.",
       "Répartit un nombre de coups aussi régulièrement que possible sur un cycle de pas, décalé d'une rotation, sur toute la longueur LEN. Tapez les coups, les pas et le décalage (par exemple <b>5 16 0</b>) et confirmez. Un coup garde la note du pas (ou prend la tonique de la gamme) ; les autres pas sont vidés."),
      ("DOUBLE", "Doubles LEN (64 at most): the steps are copied after themselves, ready to be changed.", "Double LEN (64 au plus) : les pas sont recopiés à leur suite, prêts à être modifiés."),
      ("HALF", "Halves LEN: only the first half plays.", "Divise LEN par deux : seule la première moitié joue.")]) +
 H3("SOUND: the track's sound", "SOUND : le son de la piste", EDC["seq"]) +
 P2("At the top right, the selected track's sound: its engine, then ◀ its name ▶. The arrows load the previous or the next sound on the track without leaving the page; the steps stay. On a P600 track they go through the 255 places, as the list of the SOUND page does (a changed sound asks first); on another engine, through that engine's sounds. With the TRACK buttons at the top, you change both the track and its sound from here.",
    "En haut à droite, le son de la piste choisie : son moteur, puis ◀ son nom ▶. Les flèches chargent le son précédent ou suivant sur la piste sans quitter la page ; les pas restent. Sur une piste P600, elles parcourent les 255 places, comme la liste de la page SOUND (un son modifié demande d'abord) ; sur un autre moteur, les sons de ce moteur. Avec les boutons TRACK en haut, vous changez d'ici la piste et son son.") +
 H3("AUTOMATION", "AUTOMATION", EDC["seq"]) +
 P2("The list of the knob moves recorded on the track's steps and of the parameter locks (a padlock): each row gives the step, the setting and its value. Record them on the FM-1: arm the track (●) and turn knobs while it plays.",
    "La liste des mouvements de boutons enregistrés sur les pas de la piste et des verrous de paramètres (un cadenas) : chaque ligne donne le pas, le réglage et sa valeur. Enregistrez-les sur le FM-1 : armez la piste (●) et tournez des boutons pendant la lecture.") +
 CTL([("PLAY", "Switches the whole automation of the track on or off.", "Active ou coupe toute l'automation de la piste."),
      ("DELETE", "Deletes the row chosen (click it first: it lights yellow).", "Supprime la ligne choisie (cliquez d'abord dessus : elle s'éclaire en jaune)."),
      ("CLEAR ALL", "Deletes all the automation of the track, after a confirmation.", "Supprime toute l'automation de la piste, après confirmation.")]) +
 QA([("A step holds 4 notes at most.", "Un pas tient 4 notes au plus.",
      "Take a note away before adding another.", "Retirez une note avant d'en ajouter une autre."),
     ("A step does not play.", "Un pas ne joue pas.",
      "Check that it is within LEN, its CHANCE, its COND and its VELOCITY.", "Vérifiez qu'il est dans LEN, son CHANCE, son COND et sa VELOCITY."),
     ("The tools need the Guru-600 firmware of the FM-1.", "Les outils demandent le firmware Guru-600 du FM-1.",
      "Install the Guru-600 firmware again.", "Réinstallez le firmware Guru-600."),
     ("STOP TO EDIT on the FM-1.", "STOP TO EDIT sur le FM-1.",
      "A song is playing (chapter {ch:song}): stop it to edit the steps.", "Un morceau est en lecture (chapitre {ch:song}) : arrêtez-le pour modifier les pas.")]))
