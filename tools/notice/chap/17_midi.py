# 17 · The mod wheel, MIDI and MIDI LEARN
CH("midi", "The mod wheel, MIDI and MIDI LEARN", "La molette, le MIDI et MIDI LEARN",
 H3("Playing from a MIDI keyboard", "Jouer depuis un clavier MIDI") +
 LI([("Connect it by USB or to the MIDI socket (TRS). It plays the tracks as set in MENU › MIDI › MIDI IN: by default channels 1 to 4 play tracks 1 to 4 (chapter {ch:menu}).",
      "Branchez-le en USB ou sur la prise MIDI (TRS). Il joue les pistes selon MENU › MIDI › MIDI IN : par défaut, les canaux 1 à 4 jouent les pistes 1 à 4 (chapitre {ch:menu})."),
     ("To play the selected track whatever the keyboard's channel: MIDI IN = <b>SEL</b>.", "Pour jouer la piste choisie quel que soit le canal du clavier : MIDI IN = <b>SEL</b>."),
     ("The keyboard's velocity, mod wheel (CC 1), aftertouch, expression pedal (CC 11) and sustain pedal (CC 64) all work. The pitch wheel bends the notes by ±2 semitones (a keyboard can change that range with RPN 0). Aftertouch and the expression pedal act only through the modulation matrix (LFO › MOD, sources AT and EXPR).",
      "La vélocité du clavier, sa molette de modulation (CC 1), l'aftertouch, la pédale d'expression (CC 11) et la pédale de maintien (CC 64) fonctionnent. La molette de hauteur infléchit les notes de ±2 demi-tons (un clavier peut changer cette plage par le RPN 0). L'aftertouch et la pédale d'expression n'agissent qu'à travers la matrice de modulation (LFO › MOD, sources AT et EXPR)."),
     ("<b>Nothing plays?</b> The keyboard is sending on a channel that MIDI IN does not use (set MIDI IN = SEL to check), or the track is muted.",
      "<b>Rien ne joue ?</b> Le clavier émet sur un canal que MIDI IN n'utilise pas (réglez MIDI IN = SEL pour vérifier), ou la piste est coupée.")]) +
 H3("A controller's knobs: MIDI KNOBS", "Les boutons d'un contrôleur : MIDI KNOBS") +
 P2("With MENU › MIDI › <b>MIDI KNOBS</b> ON (the default), the knobs of a MIDI keyboard or controller control the Guru-600 with no setup. The four knob banks of an Arturia KeyStep 37 mk2 work as they come out of the box; any other keyboard or controller does the same by sending the CC numbers below.",
    "Avec MENU › MIDI › <b>MIDI KNOBS</b> sur ON (le réglage d'usine), les boutons d'un clavier ou d'un contrôleur MIDI pilotent le Guru-600 sans aucun réglage. Les quatre banques de boutons d'un Arturia KeyStep 37 mk2 fonctionnent telles qu'elles sortent de la boîte ; tout autre clavier ou contrôleur fait de même en envoyant les numéros de CC ci-dessous.") +
 table([("Bank", "Banque"), ("CC (knobs 1 to 4)", "CC (boutons 1 à 4)"), ("What they control", "Ce qu'ils pilotent")],
       [["<b>A</b>", "16 \u00b7 17 \u00b7 18 \u00b7 19", ("The FM-1's <b>KNOB 1 to 4</b>, on the page shown", "Les <b>KNOB 1 à 4</b> du FM-1, sur la page affichée")],
        ["<b>B</b>", "74 \u00b7 71 \u00b7 76 \u00b7 77", ("Cutoff, resonance, LFO rate, LFO amount (P600)", "Coupure, résonance, vitesse du LFO, quantité de LFO (P600)")],
        ["<b>C</b>", "73 \u00b7 75 \u00b7 97 \u00b7 72", ("Attack, decay, sustain, release", "Attaque, decay, sustain, release")],
        ["<b>D</b>", "80 \u00b7 81 \u00b7 82 \u00b7 83", ("The <b>LEVEL</b> of tracks 1 to 4: a mixer", "Le <b>LEVEL</b> des pistes 1 à 4 : une table de mixage")]], "knobs") +
 LI([("<b>Bank A</b> turns the FM-1's four knobs as your hand would, on whatever page is shown. At the end of its travel (0 or 127), the controller's knob also takes the FM-1's knob to its end.",
      "<b>La banque A</b> tourne les quatre boutons du FM-1 comme votre main, sur la page affichée. Au bout de sa course (0 ou 127), le bouton du contrôleur amène aussi celui du FM-1 au bout de la sienne."),
     ("<b>Banks B and C</b> act on the track the keyboard's channel plays (MENU › MIDI › MIDI IN; by default, channel 1 plays track 1).",
      "<b>Les banques B et C</b> agissent sur la piste que joue le canal du clavier (MENU › MIDI › MIDI IN ; par défaut, le canal 1 joue la piste 1)."),
     ("<b>Bank D</b> is a mixer: each knob sets its own track's volume, with nothing to select first. Fully left, the track is silent; fully right, it is at full volume. You see it on the MIXER page (HOME, then HOME again).",
      "<b>La banque D</b> est une table de mixage : chaque bouton règle le volume de sa propre piste, sans rien sélectionner. Tout à gauche, la piste est muette ; tout à droite, elle est au maximum. On le voit sur la page MIXER (HOME, puis de nouveau HOME)."),
     ("A controller does not know the FM-1's settings: the first time you move one of its knobs, the setting jumps to the knob's position.",
      "Un contrôleur ne connaît pas les réglages du FM-1 : la première fois que vous bougez l'un de ses boutons, le réglage saute à la position du bouton."),
     ("The KeyStep's screen does not show these functions: print the KeyStep sheet (KeyStep-Guru-600.pdf, on guru-600.com) and keep it next to it.",
      "L'écran du KeyStep n'affiche pas ces fonctions : imprimez la fiche KeyStep (KeyStep-Guru-600.pdf, sur guru-600.com) et gardez-la à côté."),
     ("<b>A track has gone quiet?</b> A bank D knob turned to the left lowered its volume, and it stays there even with the controller unplugged. Turn that knob to the right, or raise LEVEL on the MIXER page.",
      "<b>Une piste est devenue muette ?</b> Un bouton de la banque D tourné vers la gauche a baissé son volume, et il le reste même contrôleur débranché. Tournez ce bouton vers la droite, ou remontez LEVEL sur la page MIXER.")]) +
 H3("The mod wheel", "La molette de modulation") +
 P2("The appendix gives the mod wheel's role in each factory sound. The FM-1 has no mod wheel:",
    "L'annexe indique l'effet de la molette de modulation dans chaque son d'usine. Le FM-1 n'en a pas :") +
 LI([("use a MIDI keyboard's mod wheel (CC 1);", "utilisez la molette d'un clavier MIDI (CC 1) ;"),
     ("or set MENU › CONTROL › <b>SELECT = MODW</b>: SELECT becomes the mod wheel of the selected track (MODW 0 to 127 in the band). The tempo then moves to GLO + SELECT.",
      "ou réglez MENU › CONTROL › <b>SELECT = MODW</b> : SELECT devient la molette de la piste choisie (MODW 0 à 127 dans le bandeau). Le tempo passe alors à GLO + SELECT.")]) +
 P2("<b>WHEEL</b> on the EXTRAS page sets the wheel's effect (chapter {ch:p600}). The wheel does not spring back: at 0, it adds nothing.",
    "<b>WHEEL</b> sur la page EXTRAS dose l'action de la molette (chapitre {ch:p600}). La molette ne revient pas seule : à 0, elle n'ajoute rien.") +
 H3("Every P600 control on a MIDI CC", "Chaque commande P600 sur un CC MIDI") +
 P2("On a P600 track, each Guru-600 setting responds to a fixed MIDI CC, from a controller's knobs or from music software (Logic, Ableton…). The numbers are those of the GliGli firmware for the Prophet-600: a setup made for a real Prophet-600 works as is, except the glide, on CC 5 instead of 38. The CC is received on the track's channel (MENU › MIDI). A CC set with MIDI LEARN takes priority. While the track records, CC moves are recorded as automation. With MIDI KNOBS ON (the default), CC 16 to 19 turn the FM-1's knobs instead (above): set MIDI KNOBS to OFF to use them on the oscillators.",
    "Sur une piste P600, chaque réglage du Guru-600 répond à un CC MIDI fixe, depuis les boutons d'un contrôleur ou un logiciel de musique (Logic, Ableton…). Les numéros sont ceux du firmware GliGli pour le Prophet-600 : un réglage prévu pour un vrai Prophet-600 fonctionne tel quel, sauf le glide, sur le CC 5 au lieu du 38. Le CC arrive sur le canal de la piste (MENU › MIDI). Un CC réglé avec MIDI LEARN est prioritaire. Pendant que la piste enregistre, les mouvements de CC sont enregistrés en automation. Avec MIDI KNOBS sur ON (le réglage d'usine), les CC 16 à 19 tournent plutôt les boutons du FM-1 (ci-dessus) : réglez MIDI KNOBS sur OFF pour les utiliser sur les oscillateurs.") +
 table([("CC", "CC"), ("Control", "Commande"), ("Values", "Valeurs")], [["1", '<b>MOD WHEEL</b>', ("0 to 127", "0 à 127")],
       ["5", '<b>GLIDE</b>', ("0 to 127", "0 à 127")],
       ["7", '<b>VOLUME</b>', ("0 to 127", "0 à 127")],
       ["16", '<b>OSC A FREQUENCY</b>', ("0 to 127", "0 à 127")],
       ["17", '<b>OSC A LEVEL (MIXER)</b>', ("127 = only A", "127 = seulement A")],
       ["18", '<b>OSC A PULSE WIDTH</b>', ("0 to 127", "0 à 127")],
       ["19", '<b>OSC B FREQUENCY</b>', ("0 to 127", "0 à 127")],
       ["20", '<b>OSC B LEVEL (MIXER)</b>', ("127 = only B", "127 = seulement B")],
       ["21", '<b>OSC B PULSE WIDTH</b>', ("0 to 127", "0 à 127")],
       ["22", '<b>OSC B FINE</b>', ("0 to 127", "0 à 127")],
       ["23 / 74", '<b>FILTER CUTOFF</b>', ("0 to 127", "0 à 127")],
       ["24 / 71", '<b>RESONANCE</b>', ("0 to 127", "0 à 127")],
       ["25", '<b>FILTER ENVELOPE AMOUNT</b>', ("0 to 127", "0 à 127")],
       ["26 \u00b7 27 \u00b7 28 \u00b7 29", '<b>FILTER ENVELOPE RELEASE · SUSTAIN · DECAY · ATTACK</b>', ("0 to 127", "0 à 127")],
       ["30 \u00b7 31 \u00b7 32 \u00b7 33", '<b>AMPLIFIER RELEASE · SUSTAIN · DECAY · ATTACK</b>', ("0 to 127", "0 à 127")],
       ["34", '<b>POLY-MOD FIL ENV</b>', ("0 to 127", "0 à 127")],
       ["35", '<b>POLY-MOD OSC B</b>', ("0 to 127", "0 à 127")],
       ["36", '<b>LFO FREQUENCY</b>', ("0 to 127", "0 à 127")],
       ["37", '<b>LFO INITIAL AMOUNT</b>', ("0 to 127", "0 à 127")],
       ["40", '<b>VEL > FLT (EXTRAS)</b>', ("0 to 127", "0 à 127")],
       ["44", '<b>DETUNE (UNISON)</b>', ("0 to 127", "0 à 127")],
       ["48 \u00b7 49 \u00b7 50", '<b>OSC A SAW · TRI · PULSE</b>', ("64 to 127 = on", "64 à 127 = activé")],
       ["51 \u00b7 52 \u00b7 53", '<b>OSC B SAW · TRI · PULSE</b>', ("64 to 127 = on", "64 à 127 = activé")],
       ["54", '<b>SYNC</b>', ("64 to 127 = on", "64 à 127 = activé")],
       ["55 \u00b7 56", '<b>POLY-MOD › FREQ A · FILTER</b>', ("64 to 127 = on", "64 à 127 = activé")],
       ["57", '<b>LFO SHAPE</b>', ("0 to 63 triangle, 64 to 127 square", "0 à 63 triangle, 64 à 127 carré")],
       ["60", '<b>FILTER KEYBOARD</b>', ("0 to 42 OFF, 43 to 85 HALF, 86 to 127 FULL", "0 à 42 OFF, 43 à 85 HALF, 86 à 127 FULL")],
       ["66", '<b>UNISON</b>', ("64 to 127 = on", "64 à 127 = activé")],
       ["113 \u00b7 114 \u00b7 115", '<b>LFO › FREQ A-B · PW A-B · FILTER</b>', ("64 to 127 = on", "64 à 127 = activé")],
       ["116", '<b>VINTAGE (EXTRAS)</b>', ("0 to 127", "0 à 127")]], "knobs") +
 H3("For every engine", "Pour tous les moteurs") +
 LI([("These CCs act on every track, whatever its engine: 5 GLIDE, 7 LEVEL, 10 PAN, 71 resonance, 72 release, 73 attack, 74 brightness, 75 decay, 91 reverb send, 93 chorus send, 94 delay send.",
      "Ces CC agissent sur toutes les pistes, quel que soit leur moteur : 5 GLIDE, 7 LEVEL, 10 PAN, 71 résonance, 72 release, 73 attack, 74 brillance, 75 decay, 91 envoi de réverbération, 93 envoi de chorus, 94 envoi de delay."),
     ("<b>Program Change</b>: the track loads a sound from its own engine: program 0 is the engine's first sound, 1 the second, and so on (on P600: programs 0 to 127 = sounds 1 to 128). A program beyond the engine's last sound is ignored; the engine does not change. P600 places 129 to 255 cannot be reached this way. On a DRUM track, the program picks the KIT; on FM6, programs past the eight sounds pick the voices B1 to B32 of the bank sent from the Felucca web editor.",
      "<b>Program Change</b> : la piste charge un son de son propre moteur : le programme 0 est le premier son du moteur, 1 le deuxième, etc. (sur P600 : programmes 0 à 127 = sons 1 à 128). Un programme au-delà du dernier son du moteur est ignoré ; le moteur ne change pas. Les places P600 129 à 255 ne sont pas accessibles ainsi. Sur une piste DRUM, le programme choisit le KIT ; sur FM6, les programmes au-delà des huit sons choisissent les voix B1 à B32 de la banque envoyée par l'éditeur web Felucca."),
     ("The FM-1's own keys send their notes over USB MIDI, on the selected track's channel: they can play software on the computer.",
      "Les touches du FM-1 envoient leurs notes en MIDI USB, sur le canal de la piste choisie : elles peuvent jouer un logiciel sur l'ordinateur."),
     ("<b>USB audio</b>: connected to a computer, the FM-1 is also an audio input for recording its output, metronome excluded.",
      "<b>Audio USB</b> : branché à un ordinateur, le FM-1 est aussi une entrée audio pour enregistrer sa sortie, sans le métronome.")]) +
 H3("MIDI LEARN: your own CC on any knob", "MIDI LEARN : votre propre CC sur n'importe quel bouton") +
 STEPS([("Hold <b>GLO</b> and press key <b>D4</b> (LEARN): the band says MIDI LEARN ON. Let go of GLO.",
         "Maintenez <b>GLO</b> et appuyez sur la touche <b>D4</b> (LEARN) : le bandeau indique MIDI LEARN ON. Relâchez GLO."),
        ("Turn the knob you want to control, on any page (HOME, a sound page, MIXER, GLO's levels): the bottom line shows the setting, for example T2 CUT: SEND A CC (before any knob: LEARN: TURN A KNOB; once learned: T2 CUT = CC74).",
         "Tournez le bouton rotatif à piloter, sur n'importe quelle page (HOME, une page de son, MIXER, les niveaux de GLO) : la ligne du bas indique le réglage, par exemple T2 CUT: SEND A CC (avant tout bouton : LEARN: TURN A KNOB ; une fois appris : T2 CUT = CC74)."),
        ("Move a knob of your MIDI controller: CC74 -> T2 CUT. That CC now controls that setting, on that track.",
         "Bougez un bouton de votre contrôleur MIDI : CC74 -> T2 CUT. Ce CC pilote désormais ce réglage, sur cette piste."),
        ("Repeat for other knobs, then press <b>OCT+</b> (or GLO + D4 again): LEARN DONE.",
         "Recommencez pour d'autres boutons, puis appuyez sur <b>OCT+</b> (ou de nouveau GLO + D4) : LEARN DONE.")]) +
 LI([("One CC controls one setting, and one setting responds to one CC: learning again replaces both. 16 assignments at most (LEARN FULL).",
      "Un CC pilote un réglage, et un réglage répond à un CC : réapprendre remplace les deux. 16 attributions au plus (LEARN FULL)."),
     ("While learning, <b>OCT−</b> removes the CC of the setting just turned (T2 CUT CC CLEARED).", "Pendant l'apprentissage, <b>OCT−</b> retire le CC du réglage que vous venez de tourner (T2 CUT CC CLEARED)."),
     ("CC NOT LEARNABLE: CCs 0, 1, 6, 11, 32, 38, 64, 96 to 101 and 120 to 127 cannot be learned.",
      "CC NOT LEARNABLE : les CC 0, 1, 6, 11, 32, 38, 64, 96 à 101 et 120 à 127 ne peuvent pas être appris."),
     ("The assignments are kept after power-off. MENU › MIDI › LEARN CLEAR clears them all.", "Les attributions sont conservées après extinction. MENU › MIDI › LEARN CLEAR les oublie toutes.")]) +
 H3('A screen reader, for blind and visually impaired players', "Un lecteur d'écran, pour les musiciens aveugles et malvoyants") +
 LI([("At the request of a visually impaired player, the Guru-600 can speak its screen. Connect the FM-1 to a computer by USB and open <a href='https://github.com/charlesvestal/fm1-reader'>FM-1 Screen Reader</a>, by Charles Vestal: it says the page, its four cards, each knob you turn and the messages, or hands them to the computer's own screen reader.",
      "À la demande d'un musicien malvoyant, le Guru-600 peut dire son écran. Branchez le FM-1 à un ordinateur en USB et ouvrez <a href='https://github.com/charlesvestal/fm1-reader'>FM-1 Screen Reader</a>, de Charles Vestal : il dit la page, ses quatre cartes, chaque bouton que vous tournez et les messages, ou les confie au lecteur d'écran de l'ordinateur."),
     ('Nothing is sent while no reader is listening: music software on the same USB port sees nothing, and the screen does not change.',
      "Rien n'est envoyé tant qu'aucun lecteur n'écoute : un logiciel de musique sur le même port USB ne voit rien, et l'écran ne change pas."),
     ('It also says the octave when you press OCT− or OCT+, PLAY and STOP, and REC ON or OFF on the selected track. The Guru-600 gives it its own words, so it says “filter envelope” for FENV and “resonance” for RES.',
      "Il dit aussi l'octave quand vous appuyez sur OCT− ou OCT+, PLAY et STOP, et REC ON ou OFF sur la piste choisie. Le Guru-600 lui fournit ses propres mots : il dit « filter envelope » pour FENV et « resonance » pour RES.")]) +
 H3("Tempo and clock", "Tempo et horloge") +
 P2("On HOME › CLOCK, <b>CLK</b> chooses who sets the tempo: INT (the FM-1), USB or TRS (an external MIDI clock sets the tempo and starts the sequencer). With an external clock, TAP and RESTART respond with CLK IS EXT (chapter {ch:tracks}).",
    "Sur HOME › CLOCK, <b>CLK</b> choisit qui donne le tempo : INT (le FM-1), USB ou TRS (une horloge MIDI externe donne le tempo et lance le séquenceur). Avec une horloge externe, TAP et RESTART répondent CLK IS EXT (chapitre {ch:tracks}).") +
 felucca("Features", "Felucca's features page describes its MIDI, MIDI LEARN and clock.",
         "La page des fonctions de Felucca décrit sa gestion du MIDI, MIDI LEARN et l'horloge."))
