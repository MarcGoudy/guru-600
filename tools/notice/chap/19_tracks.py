# 19 · Four tracks, the mixer and the tempo (Felucca)
CH("tracks", "Four tracks, the mixer and the tempo", "Quatre pistes, le mixeur et le tempo",
 P2("The FM-1 plays four tracks at once. Each has its own engine, sound, sequence and effect sends; the eight voices of the FM-1 are shared between them. <b>ALGORITHM</b> selects the track the keys, the knobs and PRESETS act on; its number is at the top left of the screen.",
    "Le FM-1 joue quatre pistes à la fois. Chacune a son propre moteur, son son, sa séquence et ses envois d'effets ; les huit voix du FM-1 sont partagées entre elles. <b>ALGORITHM</b> choisit la piste sur laquelle agissent les touches, les boutons rotatifs et PRESETS ; son numéro est en haut à gauche de l'écran.") +
 page("vce", "shots/pg_mixer.png", "HOME › MIXER", "HOME › MIXER", "The selected track's place in the mix. On HOME, press HOME.",
      "La place de la piste choisie dans le mixage. Sur HOME, appuyez sur HOME.",
      [("LEVEL", "The track's volume, in dB.", "Le volume de la piste, en dB.", "dB", "dB"),
       ("PAN", "Left / right.", "Gauche / droite.", "−100 / +100 %", "−100 / +100 %"),
       ("REV", "The track's reverb send.", "L'envoi de la piste vers la réverbération.", "0–100 %", "0–100 %"),
       ("MUTE", "Right: muted; left: unmuted.", "À droite : piste muette ; à gauche : le son revient.", "OFF / ON", "OFF / ON")],
      "The MIXER page.", "La page MIXER.") +
 page("vce", "shots/pg_clock.png", "HOME › CLOCK", "HOME › CLOCK", "The tempo and the clock. On MIXER, press HOME again.",
      "Le tempo et l'horloge. Sur MIXER, appuyez de nouveau sur HOME.",
      [("BPM", "The tempo, even with BPM LOCK.", "Le tempo, même avec BPM LOCK.", "40–240", "40–240"),
       ("SWG", "The swing of every track.", "Le swing de toutes les pistes.", "0–100 %", "0–100 %"),
       ("CLK", "Who sets the tempo: INT (the FM-1), USB or TRS (an external MIDI clock).", "Qui donne le tempo : INT (le FM-1), USB ou TRS (une horloge MIDI externe).", "3 choices", "3 choix")],
      "The CLOCK page.", "La page CLOCK.") +
 LI([("You can also mix in the GLO quick screen: levels on the knobs, solos, mutes and tap tempo (chapter {ch:layers}).",
      "Le mixage se règle aussi dans l'écran rapide GLO : niveaux sur les boutons rotatifs, solos, sourdines et tempo tapé (chapitre {ch:layers})."),
     ("A track's level, pan and mute stay unchanged when you change its sound.", "Le niveau, le panoramique et la sourdine d'une piste restent quand vous changez de son."),
     ("<b>A track is silent?</b> MUTE is ON (MIXER or GLO), its LEVEL is at its lowest, or another track is soloed.",
      "<b>Une piste est muette ?</b> MUTE est sur ON (MIXER ou GLO), son LEVEL est au plus bas, ou une autre piste est en solo."),
     ("<b>Notes are cut off?</b> The eight voices are shared: four tracks playing chords at once can run out of voices; the oldest notes stop first.",
      "<b>Des notes sont coupées ?</b> Les huit voix sont partagées : quatre pistes jouant des accords en même temps peuvent manquer de voix ; les notes les plus anciennes s'arrêtent d'abord.")]) +
 felucca("Features", "Felucca's features page describes the tracks, the mixer and the clock.",
         "La page des fonctions de Felucca décrit les pistes, le mixeur et l'horloge."))
