# 08 · FX: the effects
CH("fx", "FX: the effects", "FX : les effets",
 P2("The FX page follows the sound's path. Under <b>TRACK</b> <i>n</i>, the selected track's own effects: DIST and INSERT, then the SLICER, then the SENDS. Under <b>ALL TRACKS</b>, the effects the four tracks share, in the order of the sends (CHORUS, DELAY, REVERB), and MASTER on the right. A shared effect the track sends nothing to is dimmed and says <b>TRACK</b> <i>n</i> <b>· SEND 0 %</b>: its knobs still work for the other tracks.",
    "La page FX suit le trajet du son. Sous <b>TRACK</b> <i>n</i>, les effets propres à la piste choisie : DIST et INSERT, puis le SLICER, puis les SENDS. Sous <b>ALL TRACKS</b>, les effets communs aux quatre pistes, dans l'ordre des envois (CHORUS, DELAY, REVERB), et MASTER à droite. Un effet commun auquel la piste n'envoie rien est estompé et indique <b>TRACK</b> <i>n</i> <b>· SEND 0 %</b> : ses boutons agissent toujours pour les autres pistes.") +
 SHOT("fx", "The FX page.", "La page FX.") +
 H3("INSERT", "INSERT", EDC["fx"]) +
 P2("<b>DIST</b>, the first knob: the track's own distortion, at the very start of its path. It is part of the sound: loading a sound sets it again.",
    "<b>DIST</b>, le premier bouton : la distorsion propre à la piste, au tout début de son trajet. Elle fait partie du son : charger un son la redéfinit.") +
 P2("An effect inserted on the track. Choose its <b>TYPE</b>; its three knobs take the names of that type. <b>MIX</b>: how much of the effect is heard against the dry sound.",
    "Un effet inséré sur la piste. Choisissez son <b>TYPE</b> ; ses trois boutons prennent les noms de ce type. <b>MIX</b> : la part d'effet entendue par rapport au son direct.") +
 P2("Two INSERTs follow each other on the track: the sound goes through INSERT 1, then INSERT 2 (for example a phaser then a flanger). The buttons <b>1</b> and <b>2</b> above DIST choose which one the TYPE grid and the knobs set. In the grid, the type of the INSERT chosen is lit, the other's dimmer, each marked with its number.",
    "Deux INSERT se suivent sur la piste : le son passe par l'INSERT 1, puis par l'INSERT 2 (par exemple un phaser puis un flanger). Les boutons <b>1</b> et <b>2</b> au-dessus de DIST choisissent celui que règlent la grille TYPE et les boutons. Dans la grille, le type de l'INSERT choisi est allumé, celui de l'autre plus faiblement, chacun marqué de son numéro.") +
 table([("TYPE", "TYPE"), ("What it is", "Ce que c'est"), ("Knobs", "Boutons")], [
     ["<b>OFF</b>", ("No insert effect.", "Pas d'effet inséré."), "—"],
     ["<b>SOFT, HARD, FOLD, FUZZ</b>", ("Distortions, from the gentlest to the harshest.", "Des saturations, de la plus douce à la plus dure."), "DRIVE, TONE, LEVEL"],
     ["<b>CRUSH</b>", ("Fewer bits and a lower sample rate: a lo-fi sound.", "Moins de bits et une fréquence d'échantillonnage plus basse : un son lo-fi."), ("BITS (1 … 16), RATE (689 Hz … 44k), LPF", "BITS (1 … 16), RATE (689 Hz … 44k), LPF")],
     ["<b>PHASR, FLANG, CHOR</b>", ("Phaser, flanger, chorus on the track alone.", "Phaser, flanger, chorus sur la piste seule."), "RATE, DEPTH, FDBK"]]) +
 H3("SLICER", "SLICER", EDC["fx"]) +
 P2("A rhythmic gate or stutter, in time with the tempo.", "Un hachage ou un bégaiement rythmique, calé sur le tempo.") +
 CTL3([("MODE", "OFF, GATE (cuts the sound in rhythm), STUT (repeats it).", "OFF, GATE (coupe le son en rythme), STUT (le répète).", "OFF, GATE, STUT", "OFF, GATE, STUT"),
       ("PATTERN", "One of 16 rhythmic patterns.", "L'un des 16 motifs rythmiques.", "1 … 16", "1 … 16"),
       ("DEPTH", "How deep it cuts.", "La profondeur du hachage.", "0 … 100 %", "0 … 100 %"),
       ("RATE", "The length of each slice.", "La durée de chaque tranche.", "1/8, 8T, 1/16, 16T, 1/32, 32T", "1/8, 8T, 1/16, 16T, 1/32, 32T")]) +
 H3("SENDS", "SENDS", EDC["fx"]) +
 P2("How much of the track goes to CHORUS, DELAY and REVERB, the shared effects below. The same knobs as FX SENDS on the SOUND page and on the TRACKS page. They are part of the sound: loading a sound sets them again.",
    "La part de la piste envoyée vers CHORUS, DELAY et REVERB, les effets communs du dessous. Les mêmes boutons que FX SENDS sur la page SOUND et sur la page TRACKS. Ils font partie du son : charger un son les redéfinit.") +
 H3("CHORUS, DELAY, REVERB (all tracks)", "CHORUS, DELAY, REVERB (toutes les pistes)", EDC["fx"]) +
 CTL3([("CHORUS · RATE", "The speed of the chorus.", "La vitesse du chorus.", "Hz", "Hz"),
       ("CHORUS · DEPTH", "Its depth.", "Sa profondeur.", "0 … 100 %", "0 … 100 %"),
       ("DELAY · TIME", "The time between repeats, in note values of the tempo (D: dotted, T: triplet).", "Le temps entre les répétitions, en valeurs de notes du tempo (D : pointée, T : triolet).",
        "4BAR … 1/32", "4BAR … 1/32"),
       ("DELAY · FEEDBACK", "How long the repeats last: the higher, the more of them. They always fade away in the end.", "La durée des répétitions : plus il est haut, plus elles sont nombreuses. Elles finissent toujours par s'éteindre.", "0 … 120 %", "0 … 120 %"),
       ("DELAY · COLOR", "The tone of the repeats: darker to brighter.", "Le timbre des répétitions : plus sombre à plus clair.", "0 … 100 %", "0 … 100 %"),
       ("DELAY · MIX", "The level of the delay.", "Le niveau du delay.", "0 … 100 %", "0 … 100 %"),
       ("REVERB · TYPE", "ROOM, SPRING or HALL.", "ROOM, SPRING ou HALL.", "ROOM, SPRING, HALL", "ROOM, SPRING, HALL"),
       ("REVERB · SIZE", "The size of the space.", "La taille de l'espace.", "0 … 100 %", "0 … 100 %"),
       ("REVERB · DAMP", "How quickly the high frequencies fade.", "La vitesse à laquelle les aigus s'éteignent.", "0 … 100 %", "0 … 100 %")]) +
 P2("These settings are kept with the project, not with the sounds.", "Ces réglages sont enregistrés avec le projet, pas avec les sons.") +
 H3("MASTER", "MASTER", EDC["fx"]) +
 CTL3([("TUNE", "The tuning of all the tracks, in cents. The same as TUNE on the SETTINGS page (chapter {ch:settings}).", "L'accord de toutes les pistes, en cents. Le même que TUNE sur la page SETTINGS (chapitre {ch:settings}).",
        "−50 … +50 ct", "−50 … +50 ct"),
       ("GROOVE", "The swing of the whole song.", "Le swing de tout le morceau.", "0 … 100 %", "0 … 100 %")]) +
 QA([("The knobs of CHORUS, DELAY or REVERB do nothing?", "Les boutons de CHORUS, DELAY ou REVERB ne font rien ?",
      "The box is dimmed: the track sends nothing to it (SEND 0 %). Turn its send up under SENDS.", "Le cadre est estompé : la piste ne lui envoie rien (SEND 0 %). Montez son envoi dans SENDS."),
     ("No reverb?", "Pas de réverbération ?",
      "The track's REVERB send is at 0 %: turn it up under SENDS.", "L'envoi REVERB de la piste est à 0 % : montez-le dans SENDS."),
     ("No delay?", "Pas de delay ?",
      "The track's DELAY send or DELAY's MIX is at 0 %.", "L'envoi DELAY de la piste ou le MIX du DELAY est à 0 %.")]))
