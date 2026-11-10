# 16 · The menu, row by row
def mrows(rows):
    return table([("Row", "Ligne"), ("Values (default in bold)", "Valeurs (réglage d'origine en gras)"), ("What it does", "Rôle")],
                 [[f"<b>{a}</b>", b, (c, d)] for a, b, c, d in rows])


CH("menu", "The menu, row by row", "Le menu, ligne par ligne",
 '<div class="key">' + H3("Using the menu", "Utiliser le menu") +
 LI([("<b>Open</b>: hold HOME for 1 s. It reopens at the tab and row where you left it.", "<b>Ouvrir</b> : maintenez HOME 1 s. Il s'ouvre sur l'onglet et la ligne où vous l'avez quitté."),
     ("<b>ALGORITHM</b>: the tab (DISPLAY, CONTROL, AUDIO, MIDI, SYSTEM). <b>PRESETS</b>: the row. <b>KNOB 1 to 4</b> or <b>OCT− / OCT+</b>: the value. On a row ending with a chevron (›), <b>OCT+</b> opens or runs it.",
      "<b>ALGORITHM</b> : l'onglet (DISPLAY, CONTROL, AUDIO, MIDI, SYSTEM). <b>PRESETS</b> : la ligne. <b>KNOB 1 à 4</b> ou <b>OCT− / OCT+</b> : la valeur. Sur une ligne terminée par un chevron (›), <b>OCT+</b> l'ouvre ou l'exécute."),
     ("Changes apply immediately. The OCT lights breathe in the direction the value can still move.",
      "Un changement s'applique aussitôt. Les voyants OCT respirent dans le ou les sens où la valeur peut encore évoluer."),
     ("<b>Close</b>: tap HOME. The settings are saved when the menu closes, provided the sequencer is stopped: <b>close the menu before switching off</b>.",
      "<b>Fermer</b> : appuyez sur HOME. Les réglages sont enregistrés à la fermeture du menu, une fois le séquenceur arrêté : <b>fermez le menu avant d'éteindre</b>."),
     ("While the menu is open, the keys still play; the other buttons do nothing.", "Tant que le menu est ouvert, les touches jouent toujours ; les autres boutons ne font rien.")]) + '</div>' +
 '<div class="shotrow">' + "".join(shot(f"shots/menu_{i}.png", n, n, 180) for i, n in enumerate(("DISPLAY", "CONTROL", "AUDIO", "MIDI", "SYSTEM"))) + '</div>' +
 H3("DISPLAY", "DISPLAY") +
 mrows([("COLOR", "GREY, GREEN, AMBER, ICE, VIOLET, ROSE, PAPER, HI-CON, NIGHT, MONO, <b>P600</b> (+ CUSTOM)", "The screen's palette. CUSTOM appears only when a palette was made in the Felucca web editor.", "La palette de l'écran. CUSTOM n'apparaît que si une palette a été créée dans l'éditeur web Felucca."),
        ("STYLE", "<b>FLAT</b>, LINE", "FLAT: filled cards. LINE: dark areas separated by thin lines.", "FLAT : cartes pleines. LINE : zones sombres séparées par des filets."),
        ("LARGE", "<b>OFF</b>, ON", "Larger names and values on the pages.", "Noms et valeurs plus grands sur les pages."),
        ("ANIM", "OFF, <b>ON</b>, IDLE", "OFF: no animation (values change at once, no light sweep at power-on). IDLE: like ON, and the lights animate after a minute of inactivity.", "OFF : aucune animation (les valeurs changent d'un coup, pas de balayage lumineux à l'allumage). IDLE : comme ON, et les voyants s'animent après une minute sans manipulation."),
        ("LEDS", "OFF, DIM LO, <b>DIM HI</b>, INV, INV LO, INV HI", "The lights' style: DIM: unused lights glow faintly; OFF: they are dark; INV: the reverse (like the M-VAVE firmware).", "Le style des voyants : DIM : les voyants inutilisés luisent faiblement ; OFF : ils sont éteints ; INV : l'inverse (comme le firmware M-VAVE)."),
        ("SCREEN OFF", "<b>NEVER</b>, 5, 15, 30, 60 MIN", "Turns the screen off after that much inactivity; the sound keeps playing.", "Éteint l'écran après ce délai sans manipulation ; le son continue."),
        ("SCOPE", "<b>OUT</b>, MIX", "Where the visuals pick up the sound: after MASTER (OUT) or before (MIX).", "Où les images captent le son : après MASTER (OUT) ou avant (MIX).")]) +
 H3("CONTROL", "CONTROL") +
 mrows([("HOLD", "0.3, <b>0.4</b>, 0.5, 0.6 s", "How long a quick-screen button is held before its screen opens.", "Durée de maintien d'un bouton d'écran rapide avant que l'écran s'ouvre."),
        ("KNOB ACCEL", "<b>OFF</b>, ON", "A fast turn moves faster on long ranges.", "Un tour rapide avance plus vite sur les grandes plages."),
        ("FX LATCH", "<b>OFF</b>, ON", "FX quick screen: keys switch effects on and off instead of working only while held.", "Écran rapide FX : les touches allument et éteignent les effets au lieu de les maintenir."),
        ("BPM LOCK", "<b>OFF</b>, ON", "SELECT changes the tempo only with GLO held.", "SELECT ne change le tempo qu'avec GLO maintenu."),
        ("SCALE LEDS", "<b>OFF</b>, ON", "The keys of the scale light up.", "Les touches de la gamme s'allument."),
        ("STEP PREVIEW", "<b>OFF</b>, ON", "On SEQ › STEP, the step under the cursor sounds when you move to it (sequencer stopped).", "Sur SEQ › STEP, le pas sous le curseur sonne quand vous l'atteignez (séquenceur arrêté)."),
        ("CHORD ENTRY", "<b>HOLD</b>, ADD", "Step recording: HOLD writes the keys held together; ADD adds or removes each key in the step.", "Enregistrement pas à pas : HOLD écrit les touches tenues ensemble ; ADD ajoute ou retire chaque touche dans le pas."),
        ("SELECT", "<b>BPM</b>, PAGE, MODW, VEL", "What SELECT does: the tempo, the pages, the mod wheel (also sent as MIDI CC 1), or the keys' velocity.", "Ce que fait SELECT : le tempo, les pages, la molette de modulation (aussi envoyée en MIDI CC 1), ou la vélocité des touches.")]) +
 H3("AUDIO", "AUDIO") +
 mrows([("SPEAKER EQ", "<b>FLAT</b>, LOWCUT, BASS+", "A tone correction for the small speaker; it also affects headphones and USB audio.", "Une correction de timbre pour le petit haut-parleur ; elle s'applique aussi au casque et l'audio USB."),
        ("USB LEVEL", "<b>MASTER</b>, FIXED", "FIXED: the USB audio stays at full level regardless of MASTER.", "FIXED : l'audio USB reste à plein niveau quel que soit MASTER."),
        ("CLICK", "<b>OFF</b>, REC, ON", "The metronome; REC: only while recording.", "Le métronome ; REC : seulement pendant l'enregistrement."),
        ("CLICK LEVEL", "LOW, <b>MID</b>, HIGH", "The metronome's volume.", "Le volume du métronome."),
        ("COUNT-IN", "<b>OFF</b>, 1 BAR, 2 BARS", "A count before recording starts.", "Un décompte avant le début de l'enregistrement."),
        ("TUNE", "−50 … <b>0</b> … +50 ct", "The overall tuning, in cents. Kept with the project, not with the settings.", "L'accord général, en cents. Enregistré avec le projet, pas avec les réglages.")]) +
 H3("MIDI", "MIDI") +
 mrows([("MIDI IN", "<b>CH1-4</b>, SEL, CH5-8, CH9-12, CH13-16, TRACK", "Which MIDI channels play which track: CH1-4 = channels 1 to 4 on tracks 1 to 4 (same for the other blocks); SEL = every channel on the selected track; TRACK = the channels set below. Kept with the project.", "Quels canaux MIDI jouent quelle piste : CH1-4 = canaux 1 à 4 sur les pistes 1 à 4 (de même pour les autres blocs) ; SEL = tous les canaux sur la piste choisie ; TRACK = les canaux réglés ci-dessous. Enregistré avec le projet."),
        ("T1 … T4 CHANNEL", "1 … 16, OMNI, OFF (<b>T1 = 1, T2 = 2, T3 = 3, T4 = 4</b>)", "Each track's channel, used only with MIDI IN = TRACK (grayed out otherwise). Kept with the project.", "Le canal de chaque piste, utilisé seulement avec MIDI IN = TRACK (grisé sinon). Enregistré avec le projet."),
        ("AUTO SELECT", "<b>OFF</b>, ON", "A MIDI note for another track selects that track.", "Une note MIDI destinée à une autre piste sélectionne cette piste."),
        ("SCREEN WAKE", "<b>+MIDI</b>, PANEL", "What wakes a dark screen: the panel and MIDI notes, or the panel only.", "Ce qui rallume l'écran : la façade et les notes MIDI, ou la façade seulement."),
        ("LEARN CLEAR", "NONE / n CC ›", "OCT+ forgets every MIDI LEARN assignment at once, without confirmation (LEARN CLEARED; NOTHING LEARNED if there was none). Saved at once, even with the menu open.", "OCT+ oublie d'un coup toutes les attributions MIDI LEARN, sans confirmation (LEARN CLEARED ; NOTHING LEARNED s'il n'y en avait pas). Enregistré aussitôt, même menu ouvert.")]) +
 H3("SYSTEM", "SYSTEM") +
 mrows([("RESTORE LAST", "<b>ON</b>, OFF", "ON: the music and the sounds are kept when you switch off and come back at power-on. OFF: the FM-1 starts fresh each time.", "ON : la musique et les sons sont conservés à l'extinction et reviennent à l'allumage. OFF : le FM-1 démarre comme neuf à chaque fois."),
        ("HELP", "<b>OFF</b>, ON", "Hints at the bottom of each page and quick screen (chapter {ch:screen}).", "Des astuces en bas de chaque page et de chaque écran rapide (chapitre {ch:screen})."),
        ("2ND CORE", "<b>OFF</b>, ON (BETA)", "Uses the chip's second core, starting at the next power-on (2ND CORE ON: RESTART). It switches itself off if it misbehaves.", "Utilise le second cœur de la puce, au prochain allumage (2ND CORE ON: RESTART). Il se désactive de lui-même en cas de problème."),
        ("CALIBRATION", "›", "Teaches the FM-1 each button and knob again (chapter {ch:reset}).", "Réapprend au FM-1 chaque bouton et chaque bouton rotatif (chapitre {ch:reset})."),
        ("RESET SOUNDS", "›", "Erases every P600 sound you saved or imported (chapter {ch:reset}).", "Oublie tous les sons P600 enregistrés ou importés (chapitre {ch:reset})."),
        ("RESET GURU-600", "›", "Erases everything and restarts fresh, after ARE YOU SURE? (chapter {ch:reset}).", "Efface tout et redémarre comme neuf, après ARE YOU SURE? (chapitre {ch:reset})."),
        ("INFO", "›", "The firmware version (v1.6.1, Felucca's numbering), the USB state (OFF, WAIT, BUS, ENUM, MIDI) and the audio processor's load. OCT− goes back. The Guru-600's own version is shown on its start screen.", "La version du firmware (v1.6.1, la numérotation de Felucca), l'état de l'USB (OFF, WAIT, BUS, ENUM, MIDI) et la charge du processeur audio. OCT− pour revenir. La version du Guru-600 lui-même s'affiche sur son écran de démarrage."),
        ("ABOUT", "›", "Felucca's credits and licenses, with a QR code to its site; PRESETS scrolls. OCT− goes back.", "Les crédits et licences de Felucca, avec un QR code vers son site ; PRESETS fait défiler. OCT− pour revenir.")]) +
 P2("<b>2ND CORE</b>: the FM-1's chip has two cores; the Guru-600 uses one by default. With 2ND CORE ON, part of the tracks' work moves to the second, and the load drops (measured on the FM-1 with four tracks, effects and a big chord: from 72 % to 60 %). Switching it on is worth it without being needed: one core already copes, but the second leaves room, so the sound stays clean when everything plays at once (four tracks, both INSERTs, heavy sounds). It is still a trial option (BETA): if anything goes wrong, it switches itself off and everything carries on.",
    "<b>2ND CORE</b> : la puce du FM-1 a deux cœurs ; le Guru-600 n'en utilise qu'un par défaut. Avec 2ND CORE sur ON, une partie du calcul des pistes passe sur le second, et la charge baisse (mesurée sur le FM-1 avec quatre pistes, des effets et un gros accord : de 72 % à 60 %). L'activer est bénéfique sans être indispensable : un seul cœur suffit déjà, mais le second laisse de la marge, pour que le son reste propre quand tout joue en même temps (quatre pistes, les deux INSERT, des sons lourds). C'est encore une option en essai (BETA) : en cas de souci, elle se désactive d'elle-même et tout continue.") +
 felucca("Menu", "Felucca's menu page describes the menu of the original firmware.",
         "La page du menu de Felucca décrit le menu du firmware d'origine."))
