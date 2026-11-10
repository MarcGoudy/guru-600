# 10 · TRACKS: the four tracks side by side
CH("tracks", "TRACKS: the mixer", "TRACKS : la table de mixage",
 P2("The FM-1 plays four tracks at once. The TRACKS page shows them side by side, like the channels of a mixer: each one's engine "
    "and sound, its effect sends, its pan and level, MUTE and SOLO.",
    "Le FM-1 joue quatre pistes à la fois. La page TRACKS les montre côte à côte, comme les voies d'une table de mixage : le moteur "
    "et le son de chacune, ses envois d'effets, son panoramique et son niveau, MUTE et SOLO.") +
 SHOT("tracks", "The TRACKS page; the selected track is lit in orange.", "La page TRACKS ; la piste choisie est éclairée en orange.") +
 table([("Control", "Commande"), ("What it does", "Ce qu'elle fait"), ("Values", "Valeurs")], [
     ["<b>◀ ENGINE ▶</b>", ("The track's engine. ◀ or ▶ moves to the previous or next one, after a confirmation: the track then plays the new engine's first sound.",
                           "Le moteur de la piste. ◀ ou ▶ passe au précédent ou au suivant, après confirmation : la piste joue alors le premier son du nouveau moteur."),
      ("P600, ANALOG, FM6, PHASE, LOFI, SAMPLE, VOICE, TRIO, WHEEL, GRAIN, PHYS, NOISE, SLICE, DRUM", "P600, ANALOG, FM6, PHASE, LOFI, SAMPLE, VOICE, TRIO, WHEEL, GRAIN, PHYS, NOISE, SLICE, DRUM")],
     ["<b>◀ SOUND ▶</b>", ("The track's sound (for P600, its place and name). ◀ or ▶ loads the previous or next sound of its engine (P600: the 255 places).",
                          "Le son de la piste (pour P600, sa place et son nom). ◀ ou ▶ charge le son précédent ou suivant de son moteur (P600 : les 255 places)."), "—"],
     ["<b>CHORUS, DELAY, REVERB</b>", ("How much of the track goes to each shared effect (chapter {ch:fx}).", "La part de la piste envoyée à chaque effet commun (chapitre {ch:fx})."), "0 … 100 %"],
     ["<b>DIST</b>", ("The track's own distortion, above PAN (chapter {ch:fx}).", "La distorsion propre à la piste, au-dessus de PAN (chapitre {ch:fx})."), "0 … 100 %"],
     ["<b>PAN</b>", ("The track's place between left and right.", "La place de la piste entre gauche et droite."), ("L 100 … C … R 100", "L 100 … C … R 100")],
     ["<b>LEVEL</b> (fader)", ("The track's volume: click or drag on the fader. Double click: −4 dB.", "Le volume de la piste : cliquez ou glissez sur le fader. Double clic : −4 dB."),
      ("OFF, −55.5 … +7.5 dB", "OFF, −55,5 … +7,5 dB")],
     ["<b>MUTE</b>", ("Silences the track; click again to hear it.", "Coupe la piste ; cliquez de nouveau pour l'entendre."), "—"],
     ["<b>SOLO</b>", ("Plays this track alone: the others are muted. Click again to hear them all.", "Fait jouer cette piste seule : les autres sont coupées. Cliquez de nouveau pour les entendre toutes."), "—"],
     ["<b>SELECT</b>", ("Selects the track, like TRACK 1 to 4 at the top: the other pages then show and change this track.", "Choisit la piste, comme TRACK 1 à 4 en haut : les autres pages montrent et modifient alors cette piste."), "—"],
     ["LED", ("Lit: the track is armed for recording (● at the top).", "Allumée : la piste est armée pour l'enregistrement (● en haut)."), "—"]]) +
 P2("Knobs: drag up or down, or scroll over them; a double click puts them back to 0 (PAN: center).",
    "Boutons rotatifs : glissez vers le haut ou le bas, ou faites défiler au-dessus d'eux ; un double clic les remet à 0 (PAN : au centre).") +
 BOX("note", ("SOLO belongs to the editor: before closing it, click SOLO again, or the other tracks stay muted on the FM-1 (their MUTE brings them back).",
              "SOLO appartient à l'éditeur : avant de le fermer, cliquez de nouveau sur SOLO, sinon les autres pistes restent coupées sur le FM-1 (leur MUTE les rétablit).")) +
 QA([("Changing the engine erased my sound.", "Changer de moteur a effacé mon son.",
      "The track takes the new engine's first sound. Keep a sound you like before: SAVE TO THIS PLACE (P600, chapter {ch:sound}) or STORE THE TRACK'S SOUND (chapter {ch:projects}).",
      "La piste prend le premier son du nouveau moteur. Gardez avant un son qui vous plaît : SAVE TO THIS PLACE (P600, chapitre {ch:sound}) ou STORE THE TRACK'S SOUND (chapitre {ch:projects})."),
     ("Only P600 tracks have a SOUND page.", "Seules les pistes P600 ont une page SOUND.",
      "The editor edits the P600's sounds. The other engines are played and mixed here, and edited on the FM-1.",
      "L'éditeur modifie les sons du P600. Les autres moteurs se jouent et se mixent ici, et se modifient sur le FM-1.")]))
