# 8 · The P600 engine, page by page
WAVES_EN = "OFF (silent), SAW, TRI, SAW+T, PLS, SAW+P, TRI+P, ALL (all three)"
WAVES_FR = "OFF (muet), SAW, TRI, SAW+T, PLS, SAW+P, TRI+P, ALL (les trois)"
TIME_EN, TIME_FR = "1 ms – 10 s", "1 ms – 10 s"


def p6page(n, fam, title, intro_en, intro_fr, rows, tips=None):
    t = f"{n}/11 · {title}"
    return (page(fam, f"shots/p6_edit{n}.png", t, t, intro_en, intro_fr, rows,
                 f"EDIT, page {n} of 11.", f"EDIT, page {n} sur 11.") +
            (LI(tips) if tips else ""))


CH("p600", "The P600 engine, page by page", "Le moteur P600, page par page",
 P2("A track whose engine is <b>P600</b> plays like a Prophet-600: per voice, two oscillators (A and B) whose waveforms can be combined, a mixer, a 24 dB low-pass filter with its own envelope and keyboard tracking, the Poly-Mod, then the amplifier and its envelope.",
    "Une piste dont le moteur est <b>P600</b> joue comme un Prophet-600 : par voix, deux oscillateurs (A et B) aux formes d'onde combinables, un mixeur, un filtre passe-bas 24 dB avec sa propre enveloppe et son suivi de clavier, la Poly-Mod, puis l'amplificateur et son enveloppe.") +
 '<div class="key">' + H3("Reaching the pages", "Atteindre les pages") +
 LI([("Choose a P600 track (ALGORITHM; track 1 at power-on) and press <b>EDIT</b>: page 1/11, POLY MOD. Press EDIT again for the next page, double tap for the previous one.",
      "Choisissez une piste P600 (ALGORITHM ; la piste 1 à l'allumage) et appuyez sur <b>EDIT</b> : la page 1/11, POLY MOD. Appuyez de nouveau sur EDIT pour la page suivante, double appui pour la page précédente."),
     ("EDIT reopens the page you left. The page name and number are at the bottom right of the screen: POLY MOD 1/11, OSC 2/11…",
      "EDIT rouvre la page que vous avez quittée. Le nom et le numéro de la page sont en bas à droite de l'écran : POLY MOD 1/11, OSC 2/11…"),
     ("KNOB 1 to 4 (top right) change the four settings, left to right. The amplifier envelope is on <b>ENV</b> and the LFO on <b>LFO</b> (chapter {ch:envlfo}).",
      "KNOB 1 à 4 (en haut à droite) modifient les quatre réglages, de gauche à droite. L'enveloppe d'amplitude est sur <b>ENV</b> et le LFO sur <b>LFO</b> (chapitre {ch:envlfo})."),
     ("A change affects the track's sound, not the saved sound: to keep it, see chapter {ch:keep}.",
      "Un changement modifie le son de la piste, pas le son rangé : pour le conserver, voyez le chapitre {ch:keep}.")]) + '</div>' +
 p6page(1, "pm", "POLY MOD", "In each voice, two sources modulate oscillator A's pitch and/or the filter.",
        "Dans chaque voix, deux sources modulent la hauteur de l'oscillateur A et/ou le filtre.",
        [("PM EN", "FILTER ENV: how much the filter envelope modulates the destination.", "FILTER ENV : quantité de modulation par l'enveloppe du filtre.", "0–100 %", "0–100 %"),
         ("PM B", "OSC B: how much oscillator B modulates the destination, at audio speed: metallic, bell-like sounds.", "OSC B : quantité de modulation par l'oscillateur B, à vitesse audio : sons métalliques, cloches.", "0–100 %", "0–100 %"),
         ("PM DS", "DEST: where the modulation goes: OFF, FRQ A (oscillator A's pitch), FILT (the filter), BOTH.", "DEST : la destination : OFF, FRQ A (hauteur de l'oscillateur A), FILT (le filtre), BOTH (les deux).", "4 choices", "4 choix")],
        [("<b>Nothing happens?</b> DEST is OFF, or both amounts are at 0 %.", "<b>Rien ne se passe ?</b> DEST est sur OFF, ou les deux quantités sont à 0 %."),
         ("FILTER ENV to FRQ A sweeps oscillator A's pitch at each note, up to five octaves: a sync sweep when SYNC is on (page 3), a zap or a drop otherwise.", "FILTER ENV vers FRQ A balaie la hauteur de l'oscillateur A à chaque note, jusqu'à cinq octaves : un balayage de synchro quand SYNC est activé (page 3), un « zap » ou une chute sinon."),
         ("OSC B modulates even when mixed out (MIXER at 0 %) or set to OFF (it then acts as a triangle): use it purely as a modulator.", "OSC B module même hors du mixage (MIXER à 0 %) ou sur OFF (il agit alors comme un triangle) : utilisez-le uniquement comme modulateur.")]) +
 p6page(2, "osc", "OSC", "The waveforms and pitches of oscillators A and B.", "Les formes d'onde et les hauteurs des oscillateurs A et B.",
        [("A WAV", "SHAPE A: oscillator A's waveforms: " + WAVES_EN + ".", "SHAPE A : formes d'onde de l'oscillateur A : " + WAVES_FR + ".", "8 choices", "8 choix"),
         ("A FRQ", "FREQ A: oscillator A's pitch in semitones. 24 plays the note as written, 12 an octave lower, 36 an octave higher.", "FREQ A : hauteur de l'oscillateur A en demi-tons. 24 joue la note telle quelle, 12 une octave plus bas, 36 une octave plus haut.", "0–63 st", "0–63 st"),
         ("B WAV", "SHAPE B: oscillator B's waveforms, the same eight choices.", "SHAPE B : formes d'onde de l'oscillateur B, les huit mêmes choix.", "8 choices", "8 choix"),
         ("B FRQ", "FREQ B: oscillator B's pitch, the same way.", "FREQ B : hauteur de l'oscillateur B, de la même façon.", "0–63 st", "0–63 st")],
        [("<b>No sound?</b> The oscillator you are listening to is set to OFF, or the MIXER (page 4) sends everything to an oscillator set to OFF.", "<b>Pas de son ?</b> L'oscillateur entendu est sur OFF, ou le MIXER (page 4) donne tout à un oscillateur sur OFF."),
         ("A fifth apart (A 24, B 31) or an octave apart (A 24, B 36): a fuller sound. Detune B slightly with B FINE (page 3) for the classic beating.", "À une quinte (A 24, B 31) ou une octave (A 24, B 36) : un son plus plein. Désaccordez légèrement B avec B FINE (page 3) pour le battement classique."),
         ("PLS (pulse) changes with the pulse width set on page 3.", "PLS (impulsion) varie selon la largeur d'impulsion réglée en page 3.")]) +
 p6page(3, "osc", "OSC 2", "Pulse widths, fine tuning and sync.", "Largeurs d'impulsion, accord fin et synchronisation.",
        [("A PW", "PW A: pulse width of A (heard when its shape includes PLS). 50 %: square, hollow; narrow: thin, nasal.", "PW A : largeur d'impulsion de A (audible quand sa forme contient PLS). 50 % : carré, creux ; étroit : fin, nasal.", "0–100 %", "0–100 %"),
         ("B PW", "PW B: pulse width of B.", "PW B : largeur d'impulsion de B.", "0–100 %", "0–100 %"),
         ("B FIN", "FINE B: raises B slightly, up to a semitone: a fuller, beating sound.", "FINE B : élève légèrement la hauteur de B, jusqu'à un demi-ton : un son plus épais, qui bat.", "0–127", "0–127"),
         ("SYNC", "A restarts with each cycle of B: a hard, biting tone, which changes when FREQ A moves.", "A redémarre à chaque cycle de B : un son dur et mordant, qui change quand FREQ A bouge.", "OFF / ON", "OFF / ON")],
        [("SYNC sounds best with A higher than B (FREQ A above FREQ B) and A in the mix. Sweep FREQ A, or let the Poly-Mod do it (page 1).", "La SYNC s'entend surtout avec A plus aigu que B (FREQ A au-dessus de FREQ B) et A dans le mixage. Balayez FREQ A, ou laissez la Poly-Mod le faire (page 1)."),
         ("The LFO can move the pulse widths (LFO DEST › SHP): the shimmer of string ensembles.", "Le LFO peut faire bouger les largeurs d'impulsion (LFO DEST › SHP) : le scintillement des ensembles de cordes.")]) +
 p6page(4, "osc", "MIXER", "The balance of the two oscillators, the glide and the voice mode.", "L'équilibre des deux oscillateurs, le glide et le mode de voix.",
        [("MIX", "MIXER: 0 % only A, 50 % both equally, 100 % only B.", "MIXER : 0 % seulement A, 50 % les deux à égalité, 100 % seulement B.", "0–100 %", "0–100 %"),
         ("GLD", "GLIDE: time to slide from one note to the next (0: no glide).", "GLIDE : temps de glissement d'une note à l'autre (0 : pas de glide).", TIME_EN, TIME_FR),
         ("VCE", "VOICES: POLY (up to six notes), MONO (one note, each note restarts the envelopes), LEG (legato: one note, the envelopes restart only after a gap), UNI (unison: all the voices on one note, huge).", "VOICES : POLY (jusqu'à six notes), MONO (une note, chaque note relance les enveloppes), LEG (legato : une note, les enveloppes ne repartent qu'après un silence), UNI (unisson : toutes les voix sur une note, énorme).", "4 modes", "4 modes")],
        [("In UNI, DETUNE (page 7) spreads the stacked voices; the track then plays one note at a time.", "En UNI, DETUNE (page 7) écarte les voix empilées ; la piste ne joue alors qu'une note à la fois."),
         ("The four tracks share the FM-1's eight voices: a P600 track takes six at most, fewer if the other tracks are playing many notes.", "Les quatre pistes se partagent les huit voix du FM-1 : une piste P600 en prend six au plus, moins si les autres pistes jouent beaucoup de notes.")]) +
 p6page(5, "flt", "FILTER", "The 24 dB low-pass filter.", "Le filtre passe-bas 24 dB.",
        [("CUT", "CUTOFF: the brightness. The same as KNOB 1 on HOME.", "CUTOFF : la brillance. La même chose que KNOB 1 sur HOME.", "30 Hz – 16 kHz", "30 Hz – 16 kHz"),
         ("RES", "RESONANCE: boosts the frequencies at the cutoff; past about 70 % the filter whistles on its own.", "RESONANCE : renforce les fréquences à la coupure ; au-delà d'environ 70 %, le filtre siffle tout seul.", "0–100 %", "0–100 %"),
         ("FENV", "ENV AMT: how much the filter envelope (page 6) opens the filter.", "ENV AMT : à quel point l'enveloppe du filtre (page 6) ouvre celui-ci.", "0–100 %", "0–100 %"),
         ("KBD", "KEYBOARD: higher notes open the filter: OFF, HALF, FULL (the filter follows the keyboard note for note).", "KEYBOARD : les notes aiguës ouvrent le filtre : OFF, HALF, FULL (le filtre suit le clavier note pour note).", "3 choices", "3 choix")],
        [("<b>The sound is dull or silent?</b> CUTOFF is very low and ENV AMT at 0 %: turn one of them up.", "<b>Le son est sourd ou muet ?</b> CUTOFF est très bas et ENV AMT à 0 % : ouvrez l'un des deux."),
         ("With RES very high and KBD FULL, the filter whistles in tune and can be played as a third oscillator, even with both oscillators OFF.", "Avec RES très élevée et KBD sur FULL, le filtre siffle juste et se joue comme un troisième oscillateur, même avec les deux oscillateurs sur OFF."),
         ("Playing harder can open the filter: VEL>FLT on page 7, with a MIDI keyboard or SELECT = VEL.", "Jouer plus fort peut ouvrir le filtre : VEL>FLT en page 7, avec un clavier MIDI ou SELECT = VEL.")]) +
 p6page(6, "env", "FLT ENV", "The filter's own envelope.", "L'enveloppe propre au filtre.",
        [("ATK", "ATTACK: time for the filter to open.", "ATTACK : temps d'ouverture du filtre.", TIME_EN, TIME_FR),
         ("DEC", "DECAY: time to fall back to the sustain level.", "DECAY : temps de redescente vers le niveau de maintien.", TIME_EN, TIME_FR),
         ("SUS", "SUSTAIN: the level held while the key is down.", "SUSTAIN : le niveau tenu tant que la touche est enfoncée.", "0–100 %", "0–100 %"),
         ("REL", "RELEASE: time to close after the key is released.", "RELEASE : temps de fermeture après le relâchement.", TIME_EN, TIME_FR)],
        [("With ENV AMT (page 5) at 0 %, the envelope does nothing to the filter. It still drives the Poly-Mod (page 1).", "Avec ENV AMT (page 5) à 0 %, l'enveloppe ne fait rien au filtre. Elle pilote toujours la Poly-Mod (page 1)."),
         ("Short ATTACK and DECAY, low SUSTAIN: the pluck of a clavinet or a bass. Slow ATTACK: brass that swells.", "ATTACK et DECAY courts, SUSTAIN bas : le pincé d'un clavinet ou d'une basse. ATTACK lente : des cuivres qui enflent.")]) +
 p6page(7, "ext", "EXTRAS", "Features the Prophet-600 did not have, set per sound.",
        "Ce que le Prophet-600 n'avait pas, réglé par chaque son.",
        [("VINTAGE", "Each voice drifts slightly, in pitch (up to ±20 cents) and in brightness, like an old analog synthesizer. 0 %: perfectly stable.", "Chaque voix dérive légèrement, en hauteur (jusqu'à ±20 cents) et en brillance, comme un vieux synthétiseur analogique. 0 % : parfaitement stable.", "0–100 %", "0–100 %"),
         ("WHEEL", "How much of the LFO the mod wheel controls. 0 %: the LFO always plays fully and the wheel does nothing. +100 %: no LFO until you push the wheel. Negative: the wheel takes the LFO away (chapter {ch:midi}).", "La part du LFO que commande la molette. 0 % : le LFO joue toujours en entier et la molette ne fait rien. +100 % : pas de LFO tant que vous ne poussez pas la molette. Négatif : la molette retire le LFO (chapitre {ch:midi}).", "−100 / +100 %", "−100 / +100 %"),
         ("VEL>FLT", "Playing harder opens the filter (negative: closes it). Requires velocity: a MIDI keyboard, or SELECT = VEL.", "Jouer plus fort ouvre le filtre (négatif : le ferme). Il faut une vélocité : un clavier MIDI, ou SELECT = VEL.", "−100 / +100 %", "−100 / +100 %"),
         ("DETUNE", "The spread of the voices in unison (VOICES = UNI).", "L'écart des voix en unisson (VOICES = UNI).", "0–127", "0–127")],
        [("WHEEL and VEL>FLT are slots 4 and 3 of the modulation matrix (LFO › MOD); loading a P600 sound resets them (MODW › DEPTH and VEL › CUT). Slots 1 and 2 are free for your own modulations; loading a sound clears them, and only a USER place or a project keeps them.", "WHEEL et VEL>FLT sont les emplacements 4 et 3 de la matrice de modulation (LFO › MOD) ; charger un son P600 les réinitialise (MODW › DEPTH et VEL › CUT). Les emplacements 1 et 2 sont libres pour vos propres modulations ; charger un son les efface, et seuls un emplacement USER ou un projet les gardent."),
         ("VINTAGE is not saved with a sound in a P600 place (chapter {ch:keep}): every P600 sound loads with VINTAGE at 24 (about 19 %). It is saved in USER places and projects.", "VINTAGE n'est pas enregistré avec un son dans une place P600 (chapitre {ch:keep}) : chaque son P600 se charge avec VINTAGE à 24 (environ 19 %). Il l'est dans les emplacements USER et les projets.")]) +
 p6page(8, "mph", "MORPH", "Gradually turn one sound into another, or create a variation (chapter {ch:morph}).",
        "Transformer progressivement un son en un autre, ou créer une variante (chapitre {ch:morph}).",
        [("SOUND A", "The starting sound: the track's P600 sound.", "Le son de départ : le son P600 de la piste.", "1–255", "1–255"),
         ("SOUND B", "The sound to reach.", "Le son à atteindre.", "1–255", "1–255"),
         ("MORPH", "Where you are between A and B.", "Où vous êtes entre A et B.", "0–100 %", "0–100 %"),
         ("MUTATE", "How far OCT+ (MUTATE) changes the sound.", "Jusqu'où OCT+ (MUTATE) modifie le son.", "1–100 %", "1–100 %")]) +
 p6page(9, "vce", "VOICE", "Felucca's voice page, common to every engine.", "La page de voix de Felucca, commune à tous les moteurs.",
        [("VOICES", "The voice mode, the same setting as on page 4.", "Le mode de voix, le même réglage qu'en page 4.", "4 modes", "4 modes"),
         ("GLIDE", "The glide time, the same as on page 4.", "Le temps de glide, le même qu'en page 4.", TIME_EN, TIME_FR),
         ("GLMOD", "How the glide is timed: RATE (a constant speed: a wide interval takes longer) or TIME (always the same time).", "Mode du glide : RATE (vitesse constante : un grand intervalle prend plus de temps) ou TIME (toujours le même temps).", "2 choices", "2 choix"),
         ("PRIO", "In MONO and LEG, which note sounds when you hold several: LAST, LOW or HIGH.", "En MONO et LEG, la note qui sonne quand vous en tenez plusieurs : LAST (la dernière), LOW (la plus grave) ou HIGH (la plus aiguë).", "3 choices", "3 choix")]) +
 p6page(10, "vce", "VOICE 2", "Voice allocation, unison detune, panning and mute.", "Attribution des voix, désaccord d'unisson, panoramique et sourdine.",
        [("ALLOC", "How notes take voices: ROT (in rotation, so a note's release keeps ringing) or REUSE (a repeated note takes its own voice back).", "Attribution des voix : ROT (à tour de rôle : la fin d'une note continue ainsi de sonner) ou REUSE (une note répétée reprend sa propre voix).", "2 choices", "2 choix"),
         ("DETUNE", "The unison detune, the same as on page 7.", "Le désaccord d'unisson, le même qu'en page 7.", "0–127", "0–127"),
         ("PAN", "The track's position, left / right.", "La position de la piste, gauche / droite.", "−100 / +100 %", "−100 / +100 %"),
         ("MUTE", "Silences the track (the same as MIXER › MUTE).", "Coupe le son de la piste (comme MIXER › MUTE).", "OFF / ON", "OFF / ON")]) +
 p6page(11, "vce", "VOICE 3", "The stereo spread of the voices.", "L'étalement stéréo des voix.",
        [("SPRD", "The voices alternate left and right of the track's PAN: chords open up in stereo.", "Les voix alternent à gauche et à droite du PAN de la piste : les accords s'ouvrent en stéréo.", "0–100 %", "0–100 %")]) +
 H3("What a P600 sound holds", "Ce que contient un son P600") +
 P2("Each of the 255 P600 sounds sets the pages above, plus the amplifier envelope (ENV), the LFO (rate, shape, destinations and amount) and the track's effect sends (FX). Loading a sound resets all of these, and also the INSERT, the MOD slots, ENV DEST, LFO 2 and the VOICE settings; VINTAGE goes back to 24. What stays unchanged: the track's level, pan and mute, the scale and the chord keys (SCL), the arpeggiator (ARP), the SLICER, and the sequence with its length and swing. Chapter {ch:panel} shows where each knob of the real Prophet-600 is on the Guru-600.",
    "Chacun des 255 sons P600 règle les pages ci-dessus, plus l'enveloppe d'amplitude (ENV), le LFO (vitesse, forme, destinations et quantité) et les envois d'effets de la piste (FX). Charger un son redéfinit tout cela, ainsi que l'INSERT, les emplacements de MOD, ENV DEST, LFO 2 et les réglages VOICE ; VINTAGE revient à 24. Ce qui reste tel quel : le niveau, le panoramique et la sourdine de la piste, la gamme et les accords (SCL), l'arpégiateur (ARP), le SLICER, et la séquence avec sa longueur et son swing. Le chapitre {ch:panel} montre où se trouve chaque bouton du vrai Prophet-600 sur le Guru-600.") +
 BOX("tip", ("To start from scratch: hold EDIT and press the CLEAN key (G5), then OCT+ to confirm CLEAN INIT SOUND?. You get the plain P600 voice: two sawtooths, no effects and no modulation (chapter {ch:layers}). The INIT key (F5) loads the engine's first sound instead.",
             "Pour partir d'une page blanche : maintenez EDIT et appuyez sur la touche CLEAN (G5), puis OCT+ pour répondre à CLEAN INIT SOUND?. Vous obtenez la voix P600 nue, deux dents de scie, sans effet ni modulation (chapitre {ch:layers}). La touche INIT (F5), elle, charge le premier son du moteur.")))
