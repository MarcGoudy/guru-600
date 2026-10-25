# 4 · First steps
CH("first", "First steps", "Premiers pas",
 P2("Ten minutes to hear the Guru-600, change sounds and find your way around. Every change can be undone.",
    "Dix minutes pour entendre le Guru-600, changer de son et vous repérer. Chaque changement peut être annulé.") +
 H3("1. Switch on", "1. Allumer") +
 '<div class="split">' + shot("shots/home.png", "The HOME page.", "La page HOME.", 240) + '<div>' +
 STEPS([("Switch the FM-1 on.",
         "Allumez le FM-1."),
        ("Turn <b>MASTER</b> (top left) to set the volume.",
         "Tournez <b>MASTER</b> (en haut à gauche) pour régler le volume."),
        ("Play the keys: track 1 plays the Prophet-600's first factory sound, <b>1 ORGAN I</b>.",
         "Jouez sur les touches : la piste 1 joue le premier son d'usine du Prophet-600, <b>1 ORGAN I</b>.")]) +
 '</div></div>' +
 H3("2. Change the sound", "2. Changer de son") +
 STEPS([("Turn <b>PRESETS</b>: one step, one sound.",
         "Tournez <b>PRESETS</b> : un cran, un son."),
        ("Sounds 1 to 100 are the Prophet-600's factory sounds, 101 to 200 the free v2022 collection, 201 to 255 the Guru-600's own. After 255 come the other engines' sounds (chapter {ch:engines}), then your own (chapter {ch:keep}).",
         "Les sons 1 à 100 sont ceux d'usine du Prophet-600, 101 à 200 la collection libre v2022, 201 à 255 ceux du Guru-600. Après le 255 viennent les sons des autres moteurs (chapitre {ch:engines}), puis les vôtres (chapitre {ch:keep})."),
        ("Turn PRESETS the other way to go back.",
         "Tourné dans l'autre sens, PRESETS revient en arrière.")]) +
 H3("3. Shape the sound", "3. Modeler le son") +
 P2("On HOME, the four knobs at the top right change these settings:",
    "Sur HOME, les quatre boutons rotatifs en haut à droite changent ces réglages :") +
 knobs([("KNOB 1", "CUT: the filter's cutoff. Low: muffled; high: bright.", "CUT : la coupure du filtre. Bas : étouffé ; haut : brillant.", "Hz", "Hz"),
        ("KNOB 2", "RES: the resonance. The sound becomes nasal, then whistles.", "RES : la résonance. Le son devient nasal, puis siffle.", "0–100 %", "0–100 %"),
        ("KNOB 3", "FENV: how much the filter envelope opens the filter at each note.", "FENV : à quel point l'enveloppe du filtre ouvre celui-ci à chaque note.", "0–100 %", "0–100 %"),
        ("KNOB 4", "MIX: the balance between oscillators A and B.", "MIX : l'équilibre entre les oscillateurs A et B.", "0–100 %", "0–100 %")]) +
 P2("To get the original sound back, turn PRESETS one step away and back. If you turned PRESETS too far and lost a changed "
    "sound, hold <b>SAVE</b> for 1 s: the previous sound comes back with your changes (hold it again to go forward). Only the "
    "last load comes back: a quick run of turns counts as one; after several separate turns, only the sound before the last "
    "one returns.",
    "Pour retrouver le son d'origine, tournez PRESETS d'un cran puis revenez. Si vous avez tourné PRESETS trop loin et perdu "
    "un son modifié, maintenez <b>SAVE</b> 1 s : le son d'avant revient avec vos changements (maintenez-le de nouveau "
    "pour revenir en avant). Seul le dernier chargement revient : une série rapide de crans compte pour un seul ; après "
    "plusieurs tours séparés, seul le son d'avant le dernier revient.") +
 H3("4. Play higher or lower", "4. Jouer plus aigu ou plus grave") +
 P2("<b>OCT−</b> and <b>OCT+</b> move the keyboard one octave down or up, up to three octaves each way; their lights show when you are away from the middle. Press both together to return to the middle.",
    "<b>OCT−</b> et <b>OCT+</b> descendent ou montent le clavier d'une octave, jusqu'à trois octaves de chaque côté ; leur voyant signale que vous n'êtes plus au milieu. Appuyez sur les deux ensemble : retour au milieu.") +
 H3("5. Go deeper", "5. Aller plus loin") +
 STEPS([("Press <b>EDIT</b> to open the P600 engine's pages; press it again for the next page. Eleven pages, in the order of the "
         "Prophet-600's panel (chapter {ch:p600}).",
         "Appuyez sur <b>EDIT</b> pour ouvrir les pages du moteur P600 ; appuyez de nouveau pour la page suivante. Onze pages, "
         "dans l'ordre de la façade du Prophet-600 (chapitre {ch:p600})."),
        ("Double tap <b>EDIT</b>: back to the previous page.", "Double appui sur <b>EDIT</b> : retour à la page précédente."),
        ("Press <b>HOME</b>: back to the HOME page, from anywhere.", "Appuyez sur <b>HOME</b> : retour à la page HOME, de n'importe où.")]) +
 H3("6. Four tracks", "6. Quatre pistes") +
 P2("The FM-1 plays four tracks at once, each with its own sound. Turn <b>ALGORITHM</b> to choose the track (1 to 4). At "
    "power-on, track 1 is a P600 organ, track 2 an FM6 pad, track 3 a LOFI lead and track 4 a drum kit. The keys, PRESETS and "
    "the knobs always act on the track shown.",
    "Le FM-1 joue quatre pistes à la fois, chacune avec son propre son. Tournez <b>ALGORITHM</b> pour choisir la piste (1 à "
    "4). À l'allumage, la piste 1 est un orgue P600, la piste 2 une nappe FM6, la piste 3 un lead LOFI et la piste 4 une "
    "batterie. Les touches, PRESETS et les boutons rotatifs agissent toujours sur la piste affichée.") +
 H3("7. Switch off", "7. Éteindre") +
 P2("Switch off whenever you like: the FM-1 starts again with the sounds and the music as you left them (<b>MENU › SYSTEM › RESTORE LAST</b>). After a change, stop the sequencer and wait a minute before switching off.",
    "Éteignez quand vous voulez : le FM-1 redémarre avec les sons et la musique tels que vous les avez laissés (<b>MENU › SYSTEM › RESTORE LAST</b>). Après un changement, arrêtez le séquenceur et attendez une minute avant d'éteindre.") +
 BOX("key", ("<b>Restored is not saved.</b> A changed sound comes back after power-off, but it is not saved: turning PRESETS replaces it. To keep it for good, save it to a place of your own (chapter {ch:keep}).",
             "<b>Retrouvé n'est pas enregistré.</b> Un son modifié revient après l'extinction, mais il n'est pas rangé : le prochain tour de PRESETS le remplace. Pour le conserver définitivement, rangez-le dans une place à vous (chapitre {ch:keep}).")))
