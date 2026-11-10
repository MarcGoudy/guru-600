# 23 · The effects (Felucca)
CH("fx", "The effects", "Les effets",
 P2("Press <b>FX</b>. The first six pages belong to the selected track (its sends, SLICER and its two INSERTs). DLY, REVERB and CHORUS are shared by the four tracks; each track sets its own send. Hold FX for the performance effects (chapter {ch:layers}).",
    "Appuyez sur <b>FX</b>. Les six premières pages appartiennent à la piste choisie (ses envois, le SLICER et ses deux INSERT). DLY, REVERB et CHORUS sont communs aux quatre pistes ; chaque piste règle son propre envoi. Maintenez FX pour les effets de jeu (chapitre {ch:layers}).") +
 page("ext", "shots/pg_fx1.png", "FX 1/9", "FX 1/9", "The track's distortion and its sends to the shared effects.", "La distorsion de la piste et ses envois vers les effets communs.",
      [("DST", "Distortion.", "Distorsion.", "0–100 %", "0–100 %"), ("CHO", "Chorus send.", "Envoi vers le chorus.", "0–100 %", "0–100 %"),
       ("DLY", "Delay send.", "Envoi vers le delay.", "0–100 %", "0–100 %"), ("REV", "Reverb send.", "Envoi vers la réverbération.", "0–100 %", "0–100 %")],
      "The FX page.", "La page FX.") +
 page("ext", "shots/pg_fx2.png", "SLICER 2/9", "SLICER 2/9", "A rhythmic gate or stutter, in time with the tempo.", "Un hachage ou un bégaiement rythmique, calé sur le tempo.",
      [("SLCR", "OFF, GATE, STUT.", "OFF, GATE, STUT.", "3 choices", "3 choix"), ("PAT", "One of 16 patterns.", "L'un des 16 motifs.", "1–16", "1–16"),
       ("RATE", "1/8, 8T, 1/16, 16T, 1/32, 32T.", "1/8, 8T, 1/16, 16T, 1/32, 32T.", "6 values", "6 valeurs"), ("DEPTH", "How deep it cuts.", "La profondeur du hachage.", "0–100 %", "0–100 %")],
      "The SLICER page.", "La page SLICER.") +
 page("ext", "shots/pg_fx3.png", "INSERT 3/9", "INSERT 3/9", "An effect inserted on the track: SOFT, HARD, FOLD, FUZZ (distortions: DRIVE, TONE, LEVEL), CRUSH (BITS, RATE, LPF), PHASR, FLANG, CHOR (RATE, DEPTH, FDBK).",
      "Un effet inséré sur la piste : SOFT, HARD, FOLD, FUZZ (saturations : DRIVE, TONE, LEVEL), CRUSH (BITS, RATE, LPF), PHASR, FLANG, CHOR (RATE, DEPTH, FDBK).",
      [("INSRT", "The type, OFF to CHOR.", "Le type, de OFF à CHOR.", "9 types", "9 types"), ("A, B, C", "Its three settings, named by the type.", "Ses trois réglages, nommés selon le type.", "", "")],
      "The INSERT page; INSERT 2 4/9 sets its dry / wet MIX.", "La page INSERT ; INSERT 2 4/9 règle son dosage sec / traité (MIX).") +
 '<div class="shotrow">' + shot("shots/pg_fx5.png", "INSERT B 5/9: a second insert effect, after the first, with the same types and settings.", "INSERT B 5/9 : un second effet inséré, après le premier, avec les mêmes types et réglages.", 180) +
 shot("shots/pg_fx6.png", "INSERT B 2 6/9: its dry / wet MIX.", "INSERT B 2 6/9 : son dosage sec / traité (MIX).", 180) + '</div>' +
 P2("The sound goes through DIST, INSERT, then INSERT B: for example a phaser then a flanger. INSERT B OFF changes nothing.",
    "Le son passe par DIST, l'INSERT, puis l'INSERT B : par exemple un phaser puis un flanger. INSERT B sur OFF ne change rien.") +
 '<div class="shotrow">' + shot("shots/pg_fx7.png", "DLY 7/9: TIME (in note values), FDBK, COLR, MIX.", "DLY 7/9 : TIME (en valeurs de notes), FDBK, COLR, MIX.", 180) +
 shot("shots/pg_fx8.png", "REVERB 8/9: TYPE (HALL, ROOM, SPRING), SIZE, DAMP.", "REVERB 8/9 : TYPE (HALL, ROOM, SPRING), SIZE, DAMP.", 180) +
 shot("shots/pg_fx9.png", "CHORUS 9/9: CRT (rate), CDP (depth).", "CHORUS 9/9 : CRT (vitesse), CDP (profondeur).", 180) + '</div>' +
 LI([("The FX sends are part of a sound: loading a sound resets them. The shared DLY, REVERB and CHORUS settings stay; the project saves them.",
      "Les envois FX font partie d'un son : charger un son les redéfinit. Les réglages communs de DLY, REVERB et CHORUS restent ; le projet les enregistre."),
     ("<b>No reverb?</b> The track's REV send is at 0 %, on FX or on HOME › MIXER (the same setting).", "<b>Pas de réverbération ?</b> L'envoi REV de la piste est à 0 %, sur FX ou sur HOME › MIXER (le même réglage)."),
     ("A limiter on the master keeps the output from clipping.", "Un limiteur sur la sortie générale l'empêche de saturer.")]) +
 felucca("Features", "Felucca's features page describes the effects, the SLICER and the reverb types.",
         "La page des fonctions de Felucca décrit les effets, le SLICER et les types de réverbération."))
