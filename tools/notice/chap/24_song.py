# 24 · Songs, phrases and projects (Felucca)
CH("song", "Projects, phrases and songs", "Projets, phrases et morceaux",
 H3("Projects: everything at once", "Projets : tout à la fois") +
 page("vce", "shots/pg_save5.png", "SAVE › PROJECT", "SAVE › PROJECT", "Four project slots, A to D. A project holds the four tracks: their sounds, sequences, automation, mix, effects, scales, arpeggiators, and the song.",
      "Quatre emplacements de projet, de A à D. Un projet contient les quatre pistes : leurs sons, séquences, automations, mixage, effets, gammes, arpégiateurs, et le morceau.",
      [("SLOT", "The project, A to D (also PRESETS).", "Le projet, A à D (aussi PRESETS).", "A–D", "A–D"),
       ("ERASE", "Select, then OCT+: ERASE PROJECT A?", "Choisir, puis OCT+ : ERASE PROJECT A?", "action", "action"),
       ("LOAD", "Select, then OCT+: LOADED.", "Choisir, puis OCT+ : LOADED.", "action", "action"),
       ("SAVE", "Select, then OCT+: the NAME screen (KNOB 3: a random name), OCT+ to save: SAVED.", "Choisir, puis OCT+ : l'écran NAME (KNOB 3 : un nom au hasard), OCT+ pour écrire : SAVED.", "action", "action")],
      "SAVE › PROJECT, page 5 of 6.", "SAVE › PROJECT, page 5 sur 6.") +
 LI([("Stop the sequencer first (STOP TO SAVE, STOP TO ERASE). EDIT renames the project.", "Arrêtez d'abord le séquenceur (STOP TO SAVE, STOP TO ERASE). EDIT renomme le projet."),
     ("Saving to a slot in use shows OVERWRITE PROJECT A? with its name.", "Si vous enregistrez sur un emplacement occupé, OVERWRITE PROJECT A? s'affiche avec son nom."),
     ("A project loaded with a missing sample says NO SAMPLE after LOADED.", "Un projet chargé avec un échantillon manquant indique NO SAMPLE après LOADED."),
     ("The current music is kept automatically at switch-off (RESTORE LAST). Use a project to keep several pieces, or a version to come back to.",
      "La musique en cours est conservée automatiquement à l'extinction (RESTORE LAST). Utilisez un projet pour conserver plusieurs morceaux, ou une version à laquelle revenir.")]) +
 H3("Phrases: ready-made sequences", "Phrases : des séquences toutes faites") +
 page("vce", "shots/pg_save4.png", "SAVE › PHRASES", "SAVE › PHRASES", "Loads a ready-made sequence on the selected track: 13 factory phrases (ACID, OFFBEAT, MELODY, LEAD, PAD, KEYS, BELL, SUB, CHOP, STUTTER, SLICES, BEAT, ARP), then those of your USER sounds.",
      "Charge une séquence toute faite sur la piste choisie : 13 phrases d'usine (ACID, OFFBEAT, MELODY, LEAD, PAD, KEYS, BELL, SUB, CHOP, STUTTER, SLICES, BEAT, ARP), puis celles de vos sons USER.",
      [("PAT", "The phrase (also PRESETS).", "La phrase (aussi PRESETS).", "list", "liste"),
       ("LOAD", "OCT+ loads it (REPLACE T1 SEQUENCE? if the track holds your own steps). Hold SAVE to undo.", "OCT+ la charge (REPLACE T1 SEQUENCE? si la piste contient vos propres pas). Maintenez SAVE pour annuler.", "action", "action")],
      "SAVE › PHRASES, page 4 of 6.", "SAVE › PHRASES, page 4 sur 6.") +
 H3("Songs: sections in a row", "Morceaux : des sections à la suite") +
 page("vce", "shots/pg_glo1.png", "GLO › SONG", "GLO › SONG", "Up to 16 sections played one after the other. For each track, a section sets the project (A to D) whose pattern it plays, or - for silence, and its number of repeats.",
      "Jusqu'à 16 sections jouées l'une après l'autre. Pour chaque piste, une section indique le projet (A à D) dont elle joue le motif, ou - pour un silence, et son nombre de répétitions.",
      [("SEC", "The section (also PRESETS); the last row, + ADD, adds one.", "La section (aussi PRESETS) ; la dernière ligne, + ADD, en ajoute une.", "1–16", "1–16"),
       ("TRACK", "The track, T1 to T4.", "La piste, T1 à T4.", "T1–T4", "T1–T4"),
       ("PAT", "A, B, C, D or - (also the keys A3, B3, C4, D4).", "A, B, C, D ou - (aussi les touches A3, B3, C4, D4).", "5 choices", "5 choix"),
       ("REPS", "How many times the section plays.", "Le nombre de répétitions de la section.", "1–16", "1–16")],
      "GLO › SONG.", "GLO › SONG.") +
 LI([("<b>PLAY</b> (or OCT+) on SONG plays the song from the first section; PLAY again stops it. Elsewhere, PLAY plays the current patterns in a loop.",
      "<b>PLAY</b> (ou OCT+) sur SONG joue le morceau depuis la première section ; un nouvel appui sur PLAY l'arrête. Ailleurs, PLAY joue les motifs actuels en boucle."),
     ("While a song plays, the sequences cannot be edited: STOP TO EDIT.", "Pendant qu'un morceau joue, les séquences ne peuvent pas être modifiées : STOP TO EDIT."),
     ("ADD A SECTION: the song is empty. PATTERN A EMPTY: the project named in a section has no pattern for that track.",
      "ADD A SECTION : le morceau est vide. PATTERN A EMPTY : le projet nommé dans une section n'a pas de motif pour cette piste.")]) +
 H3("SAVE › TOOLS: clearing", "SAVE › TOOLS : effacer") +
 page("vce", "shots/pg_save6.png", "SAVE › TOOLS", "SAVE › TOOLS", "Clearing tools, each with a confirmation.", "Effacements, chacun après confirmation.",
      [("PAT", "CLEAR: the track's sequence and automation (CLEAR T1 SEQUENCE?).", "CLEAR : la séquence et l'automation de la piste (CLEAR T1 SEQUENCE?).", "action", "action"),
       ("SOUND", "Turn right once: INIT (the engine's first sound); twice: CLEAN (its plain voice).", "À droite une fois : INIT (le premier son du moteur) ; deux fois : CLEAN (sa voix nue).", "action", "action"),
       ("SEC", "DELETE: the song section shown on GLO › SONG.", "DELETE : la section de morceau affichée sur GLO › SONG.", "action", "action"),
       ("SONG", "CLEAR: the whole song order.", "CLEAR : tout l'ordre du morceau.", "action", "action")],
      "SAVE › TOOLS, page 6 of 6.", "SAVE › TOOLS, page 6 sur 6.") +
 felucca("Features", "Felucca's features page describes projects, phrases and songs.", "La page des fonctions de Felucca décrit les projets, les phrases et les morceaux."))
