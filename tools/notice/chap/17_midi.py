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
 H3("The mod wheel", "La molette de modulation") +
 P2("The appendix gives the mod wheel's role in each factory sound. The FM-1 has no mod wheel:",
    "L'annexe indique l'effet de la molette de modulation dans chaque son d'usine. Le FM-1 n'en a pas :") +
 LI([("use a MIDI keyboard's mod wheel (CC 1);", "utilisez la molette d'un clavier MIDI (CC 1) ;"),
     ("or set MENU › CONTROL › <b>SELECT = MODW</b>: SELECT becomes the mod wheel of the selected track (MODW 0 to 127 in the band). The tempo then moves to GLO + SELECT.",
      "ou réglez MENU › CONTROL › <b>SELECT = MODW</b> : SELECT devient la molette de la piste choisie (MODW 0 à 127 dans le bandeau). Le tempo passe alors à GLO + SELECT.")]) +
 P2("<b>WHEEL</b> on the EXTRAS page sets the wheel's effect (chapter {ch:p600}). The wheel does not spring back: at 0, it adds nothing.",
    "<b>WHEEL</b> sur la page EXTRAS dose l'action de la molette (chapitre {ch:p600}). La molette ne revient pas seule : à 0, elle n'ajoute rien.") +
 H3("Every P600 control on a MIDI CC", "Chaque commande P600 sur un CC MIDI") +
 P2("On a P600 track, each Guru-600 setting responds to a fixed MIDI CC, from a controller's knobs or from music software (Logic, Ableton…). The numbers are those of the GliGli firmware for the Prophet-600: a setup made for a real Prophet-600 works as is, except the glide, on CC 5 instead of 38. The CC is received on the track's channel (MENU › MIDI). A CC set with MIDI LEARN takes priority. While the track records, CC moves are recorded as automation.",
    "Sur une piste P600, chaque réglage du Guru-600 répond à un CC MIDI fixe, depuis les boutons d'un contrôleur ou un logiciel de musique (Logic, Ableton…). Les numéros sont ceux du firmware GliGli pour le Prophet-600 : un réglage prévu pour un vrai Prophet-600 fonctionne tel quel, sauf le glide, sur le CC 5 au lieu du 38. Le CC arrive sur le canal de la piste (MENU › MIDI). Un CC réglé avec MIDI LEARN est prioritaire. Pendant que la piste enregistre, les mouvements de CC sont enregistrés en automation.") +
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
     ("<b>Program Change</b>: the track loads a sound from its own engine: program 0 is the engine's first sound, 1 the second, and so on (on P600: programs 0 to 127 = sounds 1 to 128). A program beyond the engine's last sound is ignored; the engine does not change. P600 places 129 to 255 cannot be reached this way. On a DRUM track, the program picks the KIT; on FM6, programs past the eight sounds pick the voices B1 to B32 of the bank sent from the web editor.",
      "<b>Program Change</b> : la piste charge un son de son propre moteur : le programme 0 est le premier son du moteur, 1 le deuxième, etc. (sur P600 : programmes 0 à 127 = sons 1 à 128). Un programme au-delà du dernier son du moteur est ignoré ; le moteur ne change pas. Les places P600 129 à 255 ne sont pas accessibles ainsi. Sur une piste DRUM, le programme choisit le KIT ; sur FM6, les programmes au-delà des huit sons choisissent les voix B1 à B32 de la banque envoyée par l'éditeur web."),
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
 H3("Tempo and clock", "Tempo et horloge") +
 P2("On HOME › CLOCK, <b>CLK</b> chooses who sets the tempo: INT (the FM-1), USB or TRS (an external MIDI clock sets the tempo and starts the sequencer). With an external clock, TAP and RESTART respond with CLK IS EXT (chapter {ch:tracks}).",
    "Sur HOME › CLOCK, <b>CLK</b> choisit qui donne le tempo : INT (le FM-1), USB ou TRS (une horloge MIDI externe donne le tempo et lance le séquenceur). Avec une horloge externe, TAP et RESTART répondent CLK IS EXT (chapitre {ch:tracks}).") +
 felucca("Features", "Felucca's features page describes its MIDI, MIDI LEARN and clock.",
         "La page des fonctions de Felucca décrit sa gestion du MIDI, MIDI LEARN et l'horloge."))
