# 03 · The editor at a glance: the header, the tabs, the keyboard, the gestures
KEYS_T = [("A W S E D F T G Y H U J K O L P ;", "the notes, from C4 (A) up to E5 (;)", "les notes, du C4 (A) au E5 (;)"),
          ("← / →", "OCT − / OCT +", "OCT − / OCT +"),
          ("↑ / ↓", "SOUND page: the sound before / after in SOUNDS (the family shown), loaded at once",
           "page SOUND : le son précédent / suivant dans SOUNDS (la famille affichée), chargé aussitôt")]
CH("layout", "The editor at a glance", "L'éditeur d'un coup d'œil",
 P2("The top (header and tabs) and the bottom (keyboard) never change; the page in between is the one of the tab chosen. "
    "The editor keeps the proportions of the panel whatever the size of the window: the rest of the window stays black.",
    "Le haut (en-tête et onglets) et le bas (clavier) ne changent jamais ; entre les deux, la page de l'onglet choisi. "
    "L'éditeur garde les proportions de la façade quelle que soit la taille de la fenêtre : le reste de la fenêtre reste noir.") +
 SHOT("header", "The header and the tabs.", "L'en-tête et les onglets.") +
 H3("The header", "L'en-tête", EDC["sound"]) +
 CTL([("▶", "PLAY: starts the four tracks together. Lit green while the FM-1 plays.", "PLAY : lance les quatre pistes ensemble. Éclairé en vert pendant la lecture."),
      ("■", "STOP: stops them.", "STOP : les arrête."),
      ("●", "REC: arms the selected track for recording. Lit red while it is armed.", "REC : arme la piste choisie pour l'enregistrement. Éclairé en rouge tant qu'elle est armée."),
      ("BPM", "The tempo, 40 to 240. Click ▲ or ▼ (held: it runs); or drag up or down on the box (<kbd>Shift</kbd>: finer), or scroll over it; a double click: 120. The box flashes on each beat while the FM-1 plays, the first of the bar in orange.",
       "Le tempo, de 40 à 240. Cliquez sur ▲ ou ▼ (maintenu : il défile) ; ou glissez vers le haut ou le bas sur le cadre (<kbd>Maj</kbd> : plus fin), ou faites défiler au-dessus ; un double clic : 120. Le cadre clignote à chaque temps pendant la lecture, le premier de la mesure en orange."),
      ("CONNECT FM-1", "The connection (chapter {ch:connect}). FM-1 CONNECTED with its LED lit green: connected.", "La connexion (chapitre {ch:connect}). FM-1 CONNECTED avec son voyant vert allumé : connecté."),
      ("TRACK 1 2 3 4", "The selected track, lit orange: the pages show and change it, and the keyboard plays it.", "La piste choisie, éclairée en orange : les pages la montrent et la modifient, et le clavier la joue.")]) +
 H3("The tabs and the buttons beside them", "Les onglets et les boutons à côté", EDC["sound"]) +
 P2("SOUND, SEQUENCER, SONG, ARP, FX, MOD, TRACKS, PROJECTS, SAMPLES, BACKUP, SETTINGS: click one to show its page. Each has its chapter in this guide.",
    "SOUND, SEQUENCER, SONG, ARP, FX, MOD, TRACKS, PROJECTS, SAMPLES, BACKUP, SETTINGS : cliquez sur l'un d'eux pour afficher sa page. Chacun a son chapitre dans ce guide.") +
 CTL([("LIT / FLAT", "The bulb button. LIT or FLAT: the lights glow as on a lit panel, or plain colors. Kept by the browser (also SETTINGS › EDITOR › LIGHTING).",
       "Le bouton ampoule. LIT ou FLAT : les voyants brillent comme sur une façade éclairée, ou des couleurs unies. Gardé par le navigateur (aussi SETTINGS › EDITOR › LIGHTING)."),
      ("FULL SCREEN", "The button with four corners: full screen, and back. Also <kbd>F11</kbd>, <kbd>Alt</kbd>+<kbd>Enter</kbd> or a double click on the logo; <kbd>Esc</kbd> leaves it.",
       "Le bouton aux quatre coins : plein écran, et retour. Aussi <kbd>F11</kbd>, <kbd>Alt</kbd>+<kbd>Entrée</kbd> ou un double clic sur le logo ; <kbd>Échap</kbd> en sort."),
      ("? (HELP)", "Opens this guide at the chapter of the page shown.", "Ouvre ce guide au chapitre de la page affichée."),
      ("TOOLTIPS", "The speech-bubble button, left of the bulb: switches the tooltips on or off. Hovering a setting shows, in the language chosen, its translation and what it does; hovering a button of the editor, what it does. Kept by the browser.",
       "Le bouton bulle, à gauche de l'ampoule : active ou coupe les infobulles. Au survol d'un réglage, l'infobulle donne, dans la langue choisie, sa traduction et à quoi il sert ; au survol d'un bouton de l'éditeur, à quoi il sert. Gardé par le navigateur.")]) +
 H3("The keyboard", "Le clavier", EDC["sound"]) +
 SHOT("keyboard", "The wheels, OCT − / OCT + and the keyboard.", "Les molettes, OCT − / OCT + et le clavier.") +
 LI([("<b>Click a key</b> to play it on the selected track; drag across the keys for a glissando. Three octaves, C3 to C6; the notes play at velocity 100.",
      "<b>Cliquez sur une touche</b> pour la jouer sur la piste choisie ; glissez sur les touches pour un glissando. Trois octaves, de C3 à C6 ; les notes jouent à la vélocité 100."),
     ("<b>OCT − / OCT +</b>: two octaves down or up at most. Lit while the keyboard is shifted.",
      "<b>OCT − / OCT +</b> : deux octaves plus bas ou plus haut au plus. Allumé tant que le clavier est décalé."),
     ("<b>PITCH</b>: bends the pitch; it springs back to the middle. <b>MOD</b>: the mod wheel; it stays where you leave it.",
      "<b>PITCH</b> : infléchit la hauteur ; elle revient au milieu. <b>MOD</b> : la molette de modulation ; elle reste où vous la laissez."),
     ("Track 1 plays on MIDI channel 1, track 2 on channel 2, and so on.", "La piste 1 joue sur le canal MIDI 1, la piste 2 sur le canal 2, et ainsi de suite.")]) +
 table([("Computer key", "Touche de l'ordinateur"), ("Plays", "Joue")], [[f"<b>{e(a)}</b>", (b, c)] for a, b, c in KEYS_T]) +
 P2("The letters are positions on a QWERTY keyboard; on an AZERTY keyboard, use the keys in the same positions: Q Z S E D… for the notes. They do not play while you type in a field.",
    "Les lettres suivent la position des touches d'un clavier QWERTY ; sur un clavier AZERTY, ce sont les touches situées aux mêmes endroits : Q Z S E D… pour les notes. Elles ne jouent pas pendant la saisie dans un champ.") +
 H3("The gestures", "Les gestes", EDC["sound"]) +
 table([("Control", "Commande"), ("Gesture", "Geste")], [
     [("<b>Knob</b>", "<b>Bouton rotatif</b>"), ("Drag up (more) or down (less); <kbd>Shift</kbd> held: finer. Or scroll over it. Double click: its usual value.",
                                   "Glissez vers le haut (plus) ou le bas (moins) ; <kbd>Maj</kbd> maintenue : plus fin. Ou faites défiler au-dessus. Double clic : sa valeur habituelle.")],
     [("<b>Switch, option, button</b>", "<b>Interrupteur, option, bouton</b>"), ("Click. A lit one is on, or chosen.", "Cliquez. Allumé : activé, ou choisi.")],
     [("<b>Field ◀ value ▶</b>", "<b>Champ ◀ valeur ▶</b>"), ("Click an arrow, or scroll over the field.", "Cliquez sur une flèche, ou faites défiler au-dessus du champ.")],
     [("<b>Grey button</b>", "<b>Bouton gris</b>"), ("Not available now (nothing to do, or the FM-1 is needed).", "Indisponible pour l'instant (rien à faire, ou le FM-1 est nécessaire).")]]) +
 H3("Messages and questions", "Messages et questions", EDC["sound"]) +
 P2("A short message at the bottom of the page says what was done, or why it was not (it goes away by itself). Before anything that replaces or erases, the browser asks for a confirmation: <b>OK</b> goes on, <b>Cancel</b> changes nothing.",
    "Un court message en bas de la page dit ce qui a été fait, ou pourquoi ce ne l'a pas été (il disparaît de lui-même). Avant tout ce qui remplace ou efface, le navigateur demande confirmation : <b>OK</b> continue, <b>Annuler</b> ne change rien."))
