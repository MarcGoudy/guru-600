# 22 · The arpeggiator (Felucca)
CH("arp", "The arpeggiator", "L'arpégiateur",
 P2("The arpeggiator plays the notes you hold one after the other, in time with the tempo. Press <b>ARP</b>. It acts on the selected track, with any engine. Set MODE to OFF to play normally again.",
    "L'arpégiateur joue l'une après l'autre les notes tenues, en rythme avec le tempo. Appuyez sur <b>ARP</b>. Il agit sur la piste choisie, avec n'importe quel moteur. Réglez MODE sur OFF pour revenir au jeu normal.") +
 page("flt", "shots/pg_arp1.png", "ARP 1/2", "ARP 1/2", "The pattern and its speed.", "Le motif et sa vitesse.",
      [("MODE", "OFF, UP, DN, UPDN, RND, ORD (the order you pressed them), REPEAT, and for chords DNUP, UP+8, CONV, DIVG, PINKY, THUMB, WALK, CHORD.", "OFF, UP, DN, UPDN, RND, ORD (l'ordre d'appui), REPEAT, et pour les accords DNUP, UP+8, CONV, DIVG, PINKY, THUMB, WALK, CHORD.", "15 modes", "15 modes"),
       ("RATE", "The note value of each step, 4 bars to 1/32.", "La valeur de chaque note, de 4 mesures à 1/32.", "10 values", "10 valeurs"),
       ("OCT", "How many octaves it climbs.", "Le nombre d'octaves parcourues.", "1–4", "1–4"),
       ("GATE", "The length of each note.", "La longueur de chaque note.", "1–100 %", "1–100 %")],
      "The ARP page.", "La page ARP.") +
 page("flt", "shots/pg_arp2.png", "ARP 2 2/2", "ARP 2 2/2", "Feel and latch.", "Groove et verrouillage.",
      [("SWG", "Swing.", "Swing.", "0–100 %", "0–100 %"),
       ("PROB", "The chance that each note plays.", "La probabilité que chaque note joue.", "0–100 %", "0–100 %"),
       ("HOLD", "ON: the notes keep playing after you let go (latch); a new chord replaces them.", "ON : les notes continuent après le relâchement (verrouillage) ; un nouvel accord les remplace.", "OFF / ON", "OFF / ON"),
       ("ORD", "NOTE: by pitch. PLAY: in the order you played.", "NOTE : par hauteur. PLAY : dans l'ordre joué.", "2 choices", "2 choix")],
      "The ARP 2 page.", "La page ARP 2.") +
 LI([("<b>It plays by itself?</b> HOLD is ON: set it to OFF, or set MODE to OFF. REC › CLEAR also clears a latched chord.",
      "<b>Il joue tout seul ?</b> HOLD est sur ON : repassez-le sur OFF, ou réglez MODE sur OFF. REC › CLEAR oublie aussi un accord verrouillé."),
     ("With the chord keys (SCL › CHORD), one finger plays a whole arpeggiated chord.", "Avec les accords (SCL › CHORD), un seul doigt produit un accord entier arpégé."),
     ("The arpeggiator's settings belong to the track: they stay when you change sounds.", "Les réglages de l'arpégiateur appartiennent à la piste : ils restent quand vous changez de son.")]) +
 felucca("Features", "Felucca's features page lists the arpeggiator's modes.", "La page des fonctions de Felucca liste les modes de l'arpégiateur."))
