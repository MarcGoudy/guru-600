# 06 · SONG: a song from the four projects
CH("song", "SONG: building a song", "SONG : construire un morceau",
 P2("A song is a list of up to 16 <b>sections</b>. Each section says, for each of the four tracks, which project's part it plays "
    "(A, B, C or D, saved on the PROJECTS page, chapter {ch:projects}) or that it is silent (–), and how many times the section repeats.",
    "Un morceau est une liste de 16 <b>sections</b> au plus. Chaque section indique, pour chacune des quatre pistes, la partie de quel projet elle joue "
    "(A, B, C ou D, enregistrés sur la page PROJECTS, chapitre {ch:projects}) ou qu'elle se tait (–), et combien de fois la section se répète.") +
 SHOT("song", "The SONG page.", "La page SONG.") +
 H3("Before you start", "Avant de commencer", EDC["song"]) +
 STEPS([("Make a first part of the music on the four tracks and save it as project A (PROJECTS page).",
         "Faites une première partie de la musique sur les quatre pistes et enregistrez-la comme projet A (page PROJECTS)."),
        ("Change it into a second part (a chorus, a break…) and save it as B; then C and D if you need them.",
         "Transformez-la en une deuxième partie (un refrain, un pont…) et enregistrez-la comme B ; puis C et D si besoin."),
        ("The SLOTS LEDs on the right show which projects are saved.",
         "Les voyants SLOTS à droite montrent quels projets sont enregistrés.")]) +
 H3("SECTIONS", "SECTIONS", EDC["song"]) +
 LI([("<b>ADD</b>: adds a section at the end, a copy of the last one.", "<b>ADD</b> : ajoute une section à la fin, copie de la dernière."),
     ("Click a track's letter to change it: A, B, C, D, then – (the track is silent in that section).",
      "Cliquez sur la lettre d'une piste pour la changer : A, B, C, D, puis – (la piste se tait dans cette section)."),
     ("<b>▲ ▼</b> beside ×<i>n</i>: how many times the section plays (1 to 16).",
      "<b>▲ ▼</b> à côté de ×<i>n</i> : combien de fois la section joue (1 à 16)."),
     ("Click a row to choose it (its number lights yellow), then:", "Cliquez sur une ligne pour la choisir (son numéro s'éclaire en jaune), puis :")]) +
 CTL([("INSERT", "Inserts a new section (A A A A ×1) at the chosen row.", "Insère une nouvelle section (A A A A ×1) à la ligne choisie."),
      ("DELETE", "Deletes the chosen section.", "Supprime la section choisie."),
      ("MOVE UP, MOVE DOWN", "Moves the chosen section one row up or down.", "Monte ou descend la section choisie d'une ligne."),
      ("CLEAR SONG", "Deletes every section, after a confirmation.", "Supprime toutes les sections, après confirmation.")]) +
 P2("Each change is sent to the FM-1 at once.", "Chaque changement est envoyé aussitôt au FM-1.") +
 H3("Playing the song", "Jouer le morceau", EDC["song"]) +
 CTL([("▶ PLAY SONG", "Plays the sections from the first one. Lit green while the song plays. The section playing is lit in the list; the panel shows SECTION <i>n</i> / <i>total</i> and REPEAT <i>n</i> / <i>total</i>.",
       "Joue les sections depuis la première. Éclairé en vert pendant le morceau. La section jouée s'éclaire dans la liste ; le panneau indique SECTION <i>n</i> / <i>total</i> et REPEAT <i>n</i> / <i>total</i>."),
      ("■ STOP", "Stops the song.", "Arrête le morceau.")]) +
 P2("While a song plays, the steps cannot be edited: stop it first.", "Pendant le morceau, les pas ne peuvent pas être modifiés : arrêtez-le d'abord.") +
 QA([("Slot A is empty: save a pattern in it (PROJECTS) first.", "L'emplacement A est vide : enregistrez-y d'abord un motif (PROJECTS).",
      "A section uses a project that is not saved. Save it on PROJECTS, or change the letter.",
      "Une section utilise un projet qui n'est pas enregistré. Enregistrez-le sur PROJECTS, ou changez la lettre."),
     ("The FM-1 is busy: try again.", "Le FM-1 est occupé : réessayez.",
      "Wait a moment and do it again.", "Attendez un instant et recommencez."),
     ("Is the song kept?", "Le morceau est-il gardé ?",
      "Yes, with the music of the moment, and in a project when you save one (PROJECTS) and in a backup (BACKUP).",
      "Oui, avec la musique du moment, et dans un projet quand vous en enregistrez un (PROJECTS) et dans une sauvegarde (BACKUP).")]))
