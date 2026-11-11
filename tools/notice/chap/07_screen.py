# 7 · Reading the screen
CH("screen", "Reading the screen: pages, colors, messages, help", "Lire l'écran : pages, couleurs, messages, aide",
 '<figure class="wide scr"><img src="img/ecran_reperes.png" alt=""></figure>' +
 table([("No.", "N°"), ("Element", "Élément"), ("What it shows", "Ce qu'il montre")], [
   ['1', ('<b>Track</b>', '<b>Piste</b>'), ('The selected track, 1 to 4 (ALGORITHM); it lights up when a MIDI note arrives for it.', "La piste choisie, 1 à 4 (ALGORITHM) ; elle s'allume quand une note MIDI lui arrive.")],
   ['2', ('<b>Project</b>', '<b>Projet</b>'), ("The project letter, A to D: the PROJECT slot the track's pattern comes from (or, while a song plays, the one its section plays; - for silence). A * after it: the pattern has unsaved changes.", "La lettre du projet, A à D : l'emplacement PROJECT d'où vient la séquence de la piste (ou, pendant un morceau, celui que joue sa section ; - pour un silence). Un * après elle : la séquence a des modifications non enregistrées.")],
   ['3', ('<b>REC mark</b>', '<b>Marque REC</b>'), ('A filled red dot: the selected track is armed for recording. A red ring: another track is armed.', "Un point rouge plein : la piste choisie est armée pour l'enregistrement. Un anneau rouge : une autre piste est armée.")],
   ['4', ('<b>Transport and tempo</b>', '<b>Lecture et tempo</b>'), ('A square when the sequencer is stopped, a triangle when it plays (in the accent color during a count-in), a disc while a song plays; then the tempo in BPM, followed by a padlock when BPM LOCK is on. In a quick screen: its name ([EDIT] SET, [FX] HOLD…), with a padlock when it is locked open.', "Un carré quand le séquenceur est arrêté, un triangle quand il joue (dans la couleur d'accent pendant un décompte), un disque pendant un morceau ; puis le tempo en BPM, suivi d'un cadenas quand BPM LOCK est sur ON. Dans un écran rapide : son nom ([EDIT] SET, [FX] HOLD…), avec un cadenas quand il est verrouillé en position ouverte.")],
   ['5', ('<b>Octave</b>', '<b>Octave</b>'), ('OCT +1, OCT −2…: the keyboard is off the middle octave. While a song plays: the disc and the number of the section playing.', "OCT +1, OCT −2… : le clavier n'est pas à l'octave du milieu. Pendant un morceau : le disque et le numéro de la section jouée.")],
   ['6', ('<b>Battery</b>', '<b>Batterie</b>'), ('The battery (a charging icon on USB power).', "La batterie (une icône de charge sur l'alimentation USB).")],
   ['7', ('<b>The four cards</b>', '<b>Les quatre cartes</b>'), ('The four settings of the page, one per knob, left to right: name, value and a bar. A dimmed card is unavailable right now; an empty one is not linked to any knob.', "Les quatre réglages de la page, un par bouton rotatif, de gauche à droite : nom, valeur et une barre. Une carte grisée n'est pas utilisable pour l'instant ; une carte vide n'est reliée à aucun bouton.")],
   ['8', ('<b>The panel</b>', '<b>Le panneau</b>'), ('A picture of what the page sets: the sound drawn in real time, a list, a graph or a Prophet-600-style panel.', "Une image de ce que règle la page : le son dessiné en temps réel, une liste, un graphique ou un panneau à l'image du Prophet-600.")],
   ['9', ('<b>The row of marks</b>', '<b>La rangée de repères</b>'), ("Sixteen steps of the track's pattern (the group the cursor is in); a bar is a note (accented: in the accent color); the white mark is the step now playing, and on the SEQ pages a colored mark shows the cursor. On action pages this row shows what OCT+ and OCT− do.", "Seize pas de la séquence de la piste (le groupe où se trouve le curseur) ; une barre est une note (accentuée : dans la couleur d'accent) ; le repère blanc est le pas en cours, et sur les pages SEQ un repère de couleur montre le curseur. Sur les pages qui exécutent une action, cette rangée indique ce que font OCT+ et OCT−.")],
   ['10', ('<b>Engine and sound</b>', '<b>Moteur et son</b>'), ("The track's engine (in the palette's main color, red with P600) and its sound.", 'Le moteur de la piste (dans la couleur principale de la palette, rouge avec P600) et le son choisi.')],
   ['11', ('<b>Page</b>', '<b>Page</b>'), ("The page's name and its number in the family, for example FILTER 5/11.", 'Le nom de la page et son numéro dans la famille, par exemple FILTER 5/11.')]]) +
 H3("Families and colors", "Familles et couleurs") +
 P2("Each button opens a <b>family</b> of pages. On a P600 track, each family of controls has its color, on the page's frame and the knobs' arcs:",
    "Chaque bouton ouvre une <b>famille</b> de pages. Sur une piste P600, chaque famille de commandes a sa couleur, sur le cadre de la page et sur les arcs des boutons rotatifs :") +
 '<div class="chips">' + ''.join(f'<span style="--c:{FAM[k]}">{T(a, b)}</span>' for k, a, b in
    [("osc", "Oscillators, mixer", "Oscillateurs, mixeur"), ("flt", "Filter", "Filtre"),
     ("env", "Envelopes", "Enveloppes"), ("pm", "Poly-Mod", "Poly-Mod"), ("lfo", "LFO", "LFO"),
     ("vce", "Voices", "Voix"), ("ext", "Extras", "Extras"), ("mph", "Morph", "Morph")]) + '</div>' +
 P2("A knob's lit arc shows its value; on a two-way setting (− / +) the arc starts from the middle. Some P600 pages show round knobs, like the Prophet-600; others, the four cards with a 3D picture of the sound.",
    "L'arc lumineux d'un bouton montre sa valeur ; sur un réglage à deux sens (− / +), l'arc part du milieu. Certaines pages P600 montrent des boutons ronds, comme le Prophet-600 ; d'autres, les quatre cartes avec une image 3D du son.") +
 H3("The pages of each family", "Les pages de chaque famille") +
 table([("Button", "Bouton"), ("Pages, in order", "Pages, dans l'ordre"), ("Chapter", "Chapitre")], [
   ["<b>HOME</b>", ("HOME, MIXER, CLOCK", "HOME, MIXER, CLOCK"), "{ch:first}, {ch:tracks}"],
   ["<b>EDIT</b>", ("P600: POLY MOD, OSC, OSC 2, MIXER, FILTER, FLT ENV, EXTRAS, MORPH, VOICE, VOICE 2, VOICE 3. Other engines: their own pages, then VOICE, VOICE 2, VOICE 3.", "P600 : POLY MOD, OSC, OSC 2, MIXER, FILTER, FLT ENV, EXTRAS, MORPH, VOICE, VOICE 2, VOICE 3. Autres moteurs : leurs pages, puis VOICE, VOICE 2, VOICE 3."), "{ch:p600}, {ch:morph}, {ch:engines}"],
   ["<b>ENV</b>", ("ENV, ENV DEST", "ENV, ENV DEST"), "{ch:envlfo}"],
   ["<b>LFO</b>", ("LFO, LFO 2, LFO DEST, MOD", "LFO, LFO 2, LFO DEST, MOD"), "{ch:envlfo}"],
   ["<b>FX</b>", ("FX, SLICER, INSERT, INSERT 2, INSERT B, INSERT B 2, DLY, REVERB, CHORUS", "FX, SLICER, INSERT, INSERT 2, INSERT B, INSERT B 2, DLY, REVERB, CHORUS"), "{ch:fx}"],
   ["<b>SEL</b>", ("SCL, CHORD", "SCL, CHORD"), "{ch:chords}"],
   ["<b>ARP</b>", ("ARP, ARP 2", "ARP, ARP 2"), "{ch:arp}"],
   ["<b>SEQ</b>", ("STEP, DETAIL, AUTOMATION", "STEP, DETAIL, AUTOMATION"), "{ch:seq}"],
   ["<b>GLO</b>", ("SONG", "SONG"), "{ch:song}"],
   ["<b>SAVE</b>", ("USER, PLACE (P600 tracks), PRESETS, PHRASES, PROJECT, TOOLS", "USER, PLACE (pistes P600), PRESETS, PHRASES, PROJECT, TOOLS"), "{ch:keep}, {ch:sounds}, {ch:song}"]]) +
 P2("A page that does not apply to the track's engine is hidden (the P600 pages on a DRUM track, for example); the numbers n/m count only the pages shown.",
    "Une page sans objet pour le moteur de la piste n'apparaît pas (les pages P600 sur une piste DRUM, par exemple) ; les numéros n/m ne comptent que les pages affichées.") +
 H3("The message band", "Le bandeau de messages") +
 '<div class="split">' + shot("shots/scr_banner.png", "A message: the band at the top of the screen.", "Un message : le bandeau en haut de l'écran.", 240) + '<div>' +
 P2("The results of actions (SAVED U01, MUTATED, STOP TO SAVE…) appear for about 2 s in a green-to-blue band at the top of the screen. It needs no response. Two messages can follow one another: LOADED then NO SAMPLE, or a tool's result then [SAVE] HOLD TO UNDO. Chapter {ch:faq} lists every message and what to do about it.",
    "Les résultats des actions (SAVED U01, MUTATED, STOP TO SAVE…) s'affichent environ 2 s dans un bandeau vert-bleu en haut de l'écran. Il n'attend aucune réponse. Deux messages peuvent se suivre : LOADED puis NO SAMPLE, ou le résultat d'un outil puis [SAVE] HOLD TO UNDO. Le chapitre {ch:faq} liste chaque message et indique quoi faire.") +
 P2("A missing sample: NO SAMPLE, with a crossed-out file icon (chapter {ch:engines}). Until you have opened a quick screen once, each tap of its button shows HOLD [EDIT] QUICK: hold the button to open the quick screen.",
    "Un échantillon manquant : NO SAMPLE, avec une icône de fichier barré (chapitre {ch:engines}). Tant que vous n'avez pas ouvert un écran rapide une première fois, chaque appui sur son bouton affiche HOLD [EDIT] QUICK : maintenez le bouton pour ouvrir l'écran rapide.") +
 '</div></div>' +
 H3("Dialogs", "Les dialogues") +
 P2("Before anything is erased or replaced, a dialog asks for confirmation (sometimes a second line names what will be replaced): <span class='k'>OCT−</span> NO, <span class='k'>OCT+</span> YES. The other controls then do nothing; holding HOME opens the menu and cancels the dialog.",
    "Avant toute action qui efface ou remplace, un dialogue demande confirmation (parfois, une deuxième ligne nomme ce qui sera remplacé) : <span class='k'>OCT−</span> NON, <span class='k'>OCT+</span> OUI. Les autres commandes ne font alors rien ; maintenir HOME ouvre le menu et annule le dialogue.") +
 H3("On-screen help", "L'aide à l'écran") +
 '<div class="split">' + shot("shots/scr_help.png", "MENU › SYSTEM › HELP ON: the hint under the page.", "MENU › SYSTEM › HELP sur ON : l'astuce sous la page.", 240) + '<div>' +
 P2("<b>MENU › SYSTEM › HELP</b> ON: when a page opens, the bottom of the screen shows its main controls for 2 s, for example <span class='k'>K1</span> FILTER ENV <span class='k'>K2</span> OSC B <span class='k'>K3</span> DEST. In a quick screen, a second help line stays while it is open.",
    "<b>MENU › SYSTEM › HELP</b> sur ON : à l'ouverture d'une page, le bas de l'écran montre ses principales commandes pendant 2 s, par exemple <span class='k'>K1</span> FILTER ENV <span class='k'>K2</span> OSC B <span class='k'>K3</span> DEST. Dans un écran rapide, une deuxième ligne d'aide reste affichée tant qu'il est ouvert.") +
 P2("On action pages, the bottom of the screen shows what OCT+ and OCT− do: <span class='k'>OCT+</span> SAVE <span class='k'>OCT−</span> CANCEL.",
    "Sur les pages qui exécutent une action, le bas de l'écran indique ce que font OCT+ et OCT− : <span class='k'>OCT+</span> SAVE <span class='k'>OCT−</span> CANCEL.") +
 '</div></div>' +
 H3("The sound, drawn in real time", "Le son, dessiné en temps réel") +
 P2("The panel under the four cards is drawn from the sound itself: left and right output, level, frequencies and the notes you play. Each page has its own picture.",
    "Le panneau sous les quatre cartes est dessiné à partir du son lui-même : sortie gauche et droite, volume, fréquences et notes jouées. Chaque page a sa propre image.") +
 '<div class="grid">' +
 shot("shots/home.png", "HOME: the spectrum as bars around a disc, lows at the back, highs at the front; the left half is the left channel, the right half the right one.",
      "HOME : le spectre en barres autour d'un disque, graves au fond, aigus devant ; la moitié gauche est le canal gauche, la moitié droite le canal droit.", 200) +
 shot("shots/style_cell.png", "REVERB: a shape, round when the sound is dark, square when it is bright, spikes on each note; it splits in stereo and glows with the reverb.",
      "REVERB : une forme ronde quand le son est sombre, carrée quand il est brillant, des pointes à chaque note ; elle se divise en stéréo et rayonne avec la réverbération.", 200) +
 shot("shots/style_walls.png", "CHORUS: the left and right waves as two walls; merged into one in mono, they move apart as the sound gets wider and louder.",
      "CHORUS : les ondes gauche et droite en deux murs ; ils n'en forment qu'un en mono et s'écartent quand le son s'élargit et que son volume monte.", 200) +
 shot("shots/style_tunnel.png", "DLY: each waveform becomes a ring flying toward you, like echoes.",
      "DLY : chaque forme d'onde devient un anneau qui fonce vers vous, comme des échos.", 200) +
 shot("shots/style_sparks.png", "ARP 2: the keyboard bent into a circle; each note throws sparks from its side, blue and slow in the bass, red and fast in the treble.",
      "ARP 2 : le clavier courbé en cercle ; chaque note lance des étincelles de son côté, bleues et lentes dans les graves, rouges et rapides dans les aigus.", 200) +
 shot("shots/style_waves.png", "ENV DEST: the last waveforms piled up in depth.",
      "ENV DEST : les dernières formes d'onde empilées en profondeur.", 200) +
 shot("shots/style_flower.png", "CLOCK: the waveform wound into a flower, with more petals when the sound is brighter.",
      "CLOCK : la forme d'onde enroulée en fleur, avec plus de pétales quand le son est brillant.", 200) +
 shot("shots/style_blocks.png", "ARP: the spectrum in blocks; each new row pushes the older ones back.",
      "ARP : le spectre en blocs ; chaque nouvelle rangée repousse les précédentes vers le fond.", 200) +
 shot("shots/style_cascade.png", "OSC and OSC 2: the waveform as it comes out, the previous ones falling back in a cascade.",
      "OSC et OSC 2 : la forme d'onde qui sort, les précédentes reculant en cascade.", 200) +
 shot("shots/style_ribbon.png", "POLY MOD: the envelope that drives the modulation, as a ribbon in depth.",
      "POLY MOD : l'enveloppe qui pilote la modulation, en ruban dans la profondeur.", 200) +
 shot("shots/style_helix.png", "LFO 2: the LFO wave wound into a helix.",
      "LFO 2 : l'onde du LFO enroulée en hélice.", 200) +
 shot("shots/style_tracks.png", "MIXER (EDIT): the four tracks, each with its sound and its level.",
      "MIXER (EDIT) : les quatre pistes, chacune avec son propre son et son niveau.", 200) +
 '</div>' +
 P2("Other sound pages: <b>ENV</b> the sound's actual level over the last few seconds, a light marking the present; <b>FLT ENV</b> a plate of columns where the spectrum spreads from the center; <b>LFO</b> a ring the LFO wave deforms; <b>FILTER</b> the spectrum as a landscape, warm below the cutoff, cold above, with a wall of light at the cutoff that brightens with the resonance. With MENU › DISPLAY › LARGE ON, some pages show large values instead. MENU › DISPLAY › SCOPE: OUT (the default) takes the sound after MASTER, so the pictures go flat with MASTER turned down; MIX shows them at any volume.",
    "Autres pages du son : <b>ENV</b> le volume réel du son au cours des dernières secondes, une lumière marquant l'instant présent ; <b>FLT ENV</b> un plateau de colonnes où le spectre se propage depuis le centre ; <b>LFO</b> un anneau que l'onde du LFO déforme ; <b>FILTER</b> le spectre en paysage, chaud sous la coupure, froid au-dessus, avec un mur de lumière à la coupure qui brille davantage avec la résonance. Avec MENU › DISPLAY › LARGE sur ON, certaines pages affichent de grandes valeurs à la place. MENU › DISPLAY › SCOPE : OUT (par défaut) prend le son après MASTER, donc les images restent plates MASTER baissé ; MIX les montre quel que soit le volume.") +
 H3("Screen and colors", "Écran et couleurs") +
 LI([("<b>MENU › DISPLAY › COLOR</b> chooses the palette (P600 by default); <b>STYLE</b> FLAT or LINE, <b>LARGE</b> bigger values, <b>ANIM</b> the animations (chapter {ch:menu}).",
      "<b>MENU › DISPLAY › COLOR</b> choisit la palette (P600 par défaut) ; <b>STYLE</b> FLAT ou LINE, <b>LARGE</b> des valeurs plus grandes, <b>ANIM</b> les animations (chapitre {ch:menu})."),
     ("<b>MENU › DISPLAY › SCREEN OFF</b> turns the screen off after 5 to 60 minutes of inactivity (NEVER by default). The sound and the sequencer keep running. The touch that wakes it does nothing else: no note, no change.",
      "<b>MENU › DISPLAY › SCREEN OFF</b> éteint l'écran après 5 à 60 minutes sans aucune manipulation (NEVER par défaut). Le son et le séquenceur continuent. Le geste qui le rallume ne fait rien d'autre : ni note, ni changement.")]))
