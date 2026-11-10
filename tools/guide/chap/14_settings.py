# 14 · SETTINGS: the FM-1's menu and the editor's own
# (the rows: the notice's, chapter "The menu, row by row": the same texts, so the same translations)

SET_ROWS = {
 'DISPLAY': [
  ('COLOR', 'GREY, GREEN, AMBER, ICE, VIOLET, ROSE, PAPER, HI-CON, NIGHT, MONO, <b>P600</b> (+ CUSTOM)', "The screen's palette. CUSTOM appears only when a palette was made in the Felucca web editor.", "La palette de l'écran. CUSTOM n'apparaît que si une palette a été créée dans l'éditeur web Felucca."),
  ('STYLE', '<b>FLAT</b>, LINE', 'FLAT: filled cards. LINE: dark areas separated by thin lines.', 'FLAT : cartes pleines. LINE : zones sombres séparées par des filets.'),
  ('LARGE', '<b>OFF</b>, ON', 'Larger names and values on the pages.', 'Noms et valeurs plus grands sur les pages.'),
  ('ANIM', 'OFF, <b>ON</b>, IDLE', 'OFF: no animation (values change at once, no light sweep at power-on). IDLE: like ON, and the lights animate after a minute of inactivity.', "OFF : aucune animation (les valeurs changent d'un coup, pas de balayage lumineux à l'allumage). IDLE : comme ON, et les voyants s'animent après une minute sans manipulation."),
  ('LEDS', 'OFF, DIM LO, <b>DIM HI</b>, INV, INV LO, INV HI', "The lights' style: DIM: unused lights glow faintly; OFF: they are dark; INV: the reverse (like the M-VAVE firmware).", "Le style des voyants : DIM : les voyants inutilisés luisent faiblement ; OFF : ils sont éteints ; INV : l'inverse (comme le firmware M-VAVE)."),
  ('SCREEN OFF', '<b>NEVER</b>, 5, 15, 30, 60 MIN', 'Turns the screen off after that much inactivity; the sound keeps playing.', "Éteint l'écran après ce délai sans manipulation ; le son continue."),
  ('SCOPE', '<b>OUT</b>, MIX', 'Where the visuals pick up the sound: after MASTER (OUT) or before (MIX).', 'Où les images captent le son : après MASTER (OUT) ou avant (MIX).'),
 ],
 'CONTROL': [
  ('HOLD', '0.3, <b>0.4</b>, 0.5, 0.6\u202fs', 'How long a quick-screen button is held before its screen opens.', "Durée de maintien d'un bouton d'écran rapide avant que l'écran s'ouvre."),
  ('KNOB ACCEL', '<b>OFF</b>, ON', 'A fast turn moves faster on long ranges.', 'Un tour rapide avance plus vite sur les grandes plages.'),
  ('FX LATCH', '<b>OFF</b>, ON', 'FX quick screen: keys switch effects on and off instead of working only while held.', 'Écran rapide FX : les touches allument et éteignent les effets au lieu de les maintenir.'),
  ('BPM LOCK', '<b>OFF</b>, ON', 'SELECT changes the tempo only with GLO held.', "SELECT ne change le tempo qu'avec GLO maintenu."),
  ('SCALE LEDS', '<b>OFF</b>, ON', 'The keys of the scale light up.', "Les touches de la gamme s'allument."),
  ('STEP PREVIEW', '<b>OFF</b>, ON', 'On SEQ › STEP, the step under the cursor sounds when you move to it (sequencer stopped).', "Sur SEQ › STEP, le pas sous le curseur sonne quand vous l'atteignez (séquenceur arrêté)."),
  ('CHORD ENTRY', '<b>HOLD</b>, ADD', 'Step recording: HOLD writes the keys held together; ADD adds or removes each key in the step.', 'Enregistrement pas à pas : HOLD écrit les touches tenues ensemble ; ADD ajoute ou retire chaque touche dans le pas.'),
  ('SELECT', '<b>BPM</b>, PAGE, MODW, VEL', "What SELECT does: the tempo, the pages, the mod wheel (also sent as MIDI CC 1), or the keys' velocity.", 'Ce que fait SELECT : le tempo, les pages, la molette de modulation (aussi envoyée en MIDI CC 1), ou la vélocité des touches.'),
 ],
 'AUDIO': [
  ('SPEAKER EQ', '<b>FLAT</b>, LOWCUT, BASS+', 'A tone correction for the small speaker; it also affects headphones and USB audio.', "Une correction de timbre pour le petit haut-parleur ; elle s'applique aussi au casque et l'audio USB."),
  ('USB LEVEL', '<b>MASTER</b>, FIXED', 'FIXED: the USB audio stays at full level regardless of MASTER.', "FIXED : l'audio USB reste à plein niveau quel que soit MASTER."),
  ('CLICK', '<b>OFF</b>, REC, ON', 'The metronome; REC: only while recording.', "Le métronome ; REC : seulement pendant l'enregistrement."),
  ('CLICK LEVEL', 'LOW, <b>MID</b>, HIGH', "The metronome's volume.", 'Le volume du métronome.'),
  ('COUNT-IN', '<b>OFF</b>, 1 BAR, 2 BARS', 'A count before recording starts.', "Un décompte avant le début de l'enregistrement."),
  ('TUNE', '−50 … <b>0</b> … +50 ct', 'The overall tuning, in cents. Kept with the project, not with the settings.', "L'accord général, en cents. Enregistré avec le projet, pas avec les réglages."),
 ],
 'MIDI': [
  ('MIDI IN', '<b>CH1-4</b>, SEL, CH5-8, CH9-12, CH13-16, TRACK', 'Which MIDI channels play which track: CH1-4 = channels 1 to 4 on tracks 1 to 4 (same for the other blocks); SEL = every channel on the selected track; TRACK = the channels set below. Kept with the project.', 'Quels canaux MIDI jouent quelle piste : CH1-4 = canaux 1 à 4 sur les pistes 1 à 4 (de même pour les autres blocs) ; SEL = tous les canaux sur la piste choisie ; TRACK = les canaux réglés ci-dessous. Enregistré avec le projet.'),
  ('T1 … T4 CHANNEL', '1 … 16, OMNI, OFF (<b>T1 = 1, T2 = 2, T3 = 3, T4 = 4</b>)', "Each track's channel, used only with MIDI IN = TRACK (grayed out otherwise). Kept with the project.", 'Le canal de chaque piste, utilisé seulement avec MIDI IN = TRACK (grisé sinon). Enregistré avec le projet.'),
  ('AUTO SELECT', '<b>OFF</b>, ON', 'A MIDI note for another track selects that track.', 'Une note MIDI destinée à une autre piste sélectionne cette piste.'),
  ('SCREEN WAKE', '<b>+MIDI</b>, PANEL', 'What wakes a dark screen: the panel and MIDI notes, or the panel only.', "Ce qui rallume l'écran : la façade et les notes MIDI, ou la façade seulement."),
 ],
 'SYSTEM': [
  ('RESTORE LAST', '<b>ON</b>, OFF', 'ON: the music and the sounds are kept when you switch off and come back at power-on. OFF: the FM-1 starts fresh each time.', "ON : la musique et les sons sont conservés à l'extinction et reviennent à l'allumage. OFF : le FM-1 démarre comme neuf à chaque fois."),
  ('HELP', '<b>OFF</b>, ON', 'Hints at the bottom of each page and quick screen of the FM-1.', 'Des astuces en bas de chaque page et de chaque écran rapide du FM-1.'),
  ('2ND CORE', '<b>OFF</b>, ON (BETA)', "Uses the chip's second core, starting at the next power-on (2ND CORE ON: RESTART). It switches itself off if it misbehaves.", 'Utilise le second cœur de la puce, au prochain allumage (2ND CORE ON: RESTART). Il se désactive de lui-même en cas de problème.'),
  ('FACTORY', 'RESET GURU-600', "Erases everything of yours on the FM-1 (projects, USER sounds, samples, P600 places, settings), after two confirmations; it restarts as new. Make a backup first (chapter {ch:backup}). As MENU › SYSTEM › RESET GURU-600.", "Efface tout ce qui est à vous sur le FM-1 (projets, sons USER, échantillons, places P600, réglages), après deux confirmations ; il redémarre comme neuf. Faites d'abord une sauvegarde (chapitre {ch:backup}). Comme MENU › SYSTEM › RESET GURU-600."),
 ],
}


def srows(tab):
    return table([("Setting", "Réglage"), ("Values (default in bold)", "Valeurs (réglage d'origine en gras)"), ("What it does", "Rôle")],
                 [[f"<b>{a}</b>", b, (c, d)] for a, b, c, d in SET_ROWS[tab]])


CH("settings", "SETTINGS: the FM-1's menu and the editor's own", "SETTINGS : le menu du FM-1 et les réglages de l'éditeur",
 P2("The SETTINGS page shows the settings of the FM-1's MENU, grouped by its tabs (DISPLAY, CONTROL, AUDIO, MIDI, SYSTEM), "
    "and the editor's own (EDITOR). The FM-1 describes its settings itself: the page always shows those of the firmware installed.",
    "La page SETTINGS présente les réglages du MENU du FM-1, groupés selon ses onglets (DISPLAY, CONTROL, AUDIO, MIDI, SYSTEM), "
    "et ceux de l'éditeur (EDITOR). Le FM-1 décrit lui-même ses réglages : la page montre toujours ceux du firmware installé.") +
 SHOT("settings", "The SETTINGS page.", "La page SETTINGS.") +
 H3("Changing a setting", "Changer un réglage", EDC["settings"]) +
 LI([("<b>Buttons</b>: click the value. The lit button is the current one.",
      "<b>Boutons</b> : cliquez sur la valeur. Le bouton allumé est la valeur actuelle."),
     ("<b>Field with arrows</b> (◀ value ▶): click ◀ or ▶, or scroll over the field. At the end of the list it starts again from the other end; TUNE stops at −50 and +50.",
      "<b>Champ à flèches</b> (◀ valeur ▶) : cliquez sur ◀ ou ▶, ou faites défiler au-dessus du champ. Au bout de la liste, il repart de l'autre bout ; TUNE s'arrête à −50 et +50."),
     ("The FM-1 applies it at once and keeps it: nothing else to do, no menu to close.",
      "Le FM-1 l'applique aussitôt et le garde : rien d'autre à faire, aucun menu à fermer."),
     ("MIDI IN, T1 … T4 CHANNEL and TUNE belong to the music: they are kept with the project (chapter {ch:projects}). TUNE is also the FX page's MASTER TUNE (chapter {ch:fx}).",
      "MIDI IN, T1 … T4 CHANNEL et TUNE appartiennent à la musique : ils sont enregistrés avec le projet (chapitre {ch:projects}). TUNE est aussi le MASTER TUNE de la page FX (chapitre {ch:fx}).")]) +
 QA([("Set: the FM-1 keeps it once the music stops.", "Réglé : le FM-1 le garde dès que la musique s'arrête.",
      "The setting applies now; the FM-1 saves it when you stop the music (■).",
      "Le réglage s'applique tout de suite ; le FM-1 l'enregistre quand vous arrêtez la musique (■)."),
     ("Set, but the FM-1 could not keep it.", "Réglé, mais le FM-1 n'a pas pu le garder.",
      "The setting applies, but it is lost at power-off. Change it again later; if the message comes back, make a backup (chapter {ch:backup}).",
      "Le réglage s'applique, mais il sera perdu à l'extinction. Changez-le de nouveau plus tard ; si le message revient, faites une sauvegarde (chapitre {ch:backup})."),
     ("This FM-1 does not have that setting.", "Ce FM-1 n'a pas ce réglage.",
      "The firmware installed is older than the editor. Reload the page with the FM-1 connected: the page then shows its own settings.",
      "Le firmware installé est plus ancien que l'éditeur. Rechargez la page, FM-1 branché : elle affiche alors ses propres réglages.")]) +
 P2("The rows that run something stay on the FM-1's menu: CALIBRATION, RESET SOUNDS, RESET GURU-600, INFO, ABOUT and LEARN CLEAR.",
    "Les lignes qui lancent une action restent dans le menu du FM-1 : CALIBRATION, RESET SOUNDS, RESET GURU-600, INFO, ABOUT et LEARN CLEAR.") +
 "".join(H3(t, t, EDC["settings"]) + srows(t) for t in ("DISPLAY", "CONTROL", "AUDIO", "MIDI", "SYSTEM")) +
 H3("EDITOR", "EDITOR", EDC["settings"]) +
 P2("The editor's own settings, kept by this browser on this computer.",
    "Les réglages de l'éditeur, gardés par ce navigateur sur cet ordinateur.") +
 table([("Setting", "Réglage"), ("Values", "Valeurs"), ("What it does", "Rôle")], [
     ["<b>LIGHTING</b>", "<b>LIT</b>, FLAT", ("LIT: the lights glow as on a lit panel. FLAT: plain colors. The same as the bulb button at the end of the tabs (chapter {ch:layout}).",
                                               "LIT : les voyants brillent comme sur une façade éclairée. FLAT : des couleurs unies. Comme le bouton ampoule au bout des onglets (chapitre {ch:layout}).")],
     ["<b>LANGUAGE</b>", "<b>AUTO</b>, ENGLISH, FRANÇAIS, DEUTSCH, ESPAÑOL, ITALIANO, 中文, 日本語",
      ("The editor's language: its pages, buttons and messages, the FM-1's menu (this page), the tooltips, and this guide when ? opens it. The names of the sound and sequencer settings stay in English, as on the FM-1's screen. AUTO: the browser's language (English if it is another one). Click ◀ or ▶: the page reloads in the language chosen. The screenshots of this guide show the editor in English.",
       "La langue de l'éditeur : ses pages, ses boutons et ses messages, le menu du FM-1 (cette page), les infobulles, et ce guide quand ? l'ouvre. Les noms des réglages du son et du séquenceur restent en anglais, comme sur l'écran du FM-1. AUTO : la langue du navigateur (l'anglais si c'en est une autre). Cliquez sur ◀ ou ▶ : la page se recharge dans la langue choisie. Les captures de ce guide montrent l'éditeur en anglais.")]]))
