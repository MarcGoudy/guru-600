# 5 · The synthesizer, in plain words (from the first guide)
CH("basics", "The synthesizer, in plain words", "Le synthétiseur expliqué simplement",

 P2("A synthesizer builds a sound in a few stages, always in the same order.",
    "Un synthétiseur fabrique un son en quelques étapes, toujours dans le même ordre.") +
 '<div class="chain">' + ''.join(f'<span style="--c:{c}">{T(a, b)}</span>' for a, b, c in
    [("Oscillators", "Oscillateurs", FAM["osc"]), ("Mixer", "Mixeur", FAM["osc"]), ("Filter", "Filtre", FAM["flt"]),
     ("Amplifier", "Amplificateur", FAM["env"]), ("Effects", "Effets", "#9a9486")]) + '</div>' +
 H3("1. The oscillators: the raw sound", "1. Les oscillateurs : le son brut", FAM["osc"]) +
 P2("An oscillator vibrates and makes a steady tone, like a string being bowed without stopping. Its <b>shape</b> "
    "(waveform) gives it its color:", "Un oscillateur vibre et produit un son continu, comme une corde frottée sans interruption. "
    "Sa <b>forme d'onde</b> lui donne sa couleur :") +
 LI([("<b>SAW</b> (sawtooth): bright and buzzy, rich in harmonics — brass, strings, leads.",
      "<b>SAW</b> (dent de scie) : brillante et nasillarde, riche en harmoniques — cuivres, cordes, leads."),
     ("<b>TRI</b> (triangle): soft and round, close to a flute.", "<b>TRI</b> (triangle) : douce et ronde, proche d'une flûte."),
     ("<b>PLS</b> (pulse): hollow and woody. Its <b>pulse width</b> changes its character: a square wave (50 %) sounds like a "
      "clarinet; a narrow pulse sounds thin and nasal. Moving the width slowly creates the shimmer of string ensembles.",
      "<b>PLS</b> (impulsion) : creuse et boisée. Sa <b>largeur d'impulsion</b> change son caractère : carrée (50 %), elle "
      "évoque la clarinette ; étroite, elle devient fine et nasale. La faire bouger lentement donne le scintillement des "
      "ensembles de cordes.")]) +
 P2("The Guru-600, like the Prophet-600, has two oscillators per voice, <b>A</b> and <b>B</b>. Each can use several shapes at once. "
    "Tuning them apart (an octave, a fifth, or just slightly) makes the sound fuller. <b>SYNC</b> forces A to restart with each cycle of B: "
    "a hard, biting sound, very '80s.",
    "Le Guru-600, comme le Prophet-600, a deux oscillateurs par voix, <b>A</b> et <b>B</b>. Chacun peut combiner plusieurs formes d'onde. "
    "Les accorder différemment (une octave, une quinte, ou juste un peu) épaissit le son. La <b>SYNC</b> oblige A à "
    "redémarrer avec B : un son dur et mordant, très années 80.") +
 H3("2. The mixer", "2. Le mixeur", FAM["osc"]) +
 P2("The <b>MIXER</b> sets the balance between oscillator A and oscillator B.", "Le <b>MIXER</b> règle l'équilibre entre "
    "l'oscillateur A et l'oscillateur B.") +
 H3("3. The filter: the tone control", "3. Le filtre : le réglage de timbre", FAM["flt"]) +
 P2("The filter removes the high frequencies, like a very powerful treble knob. <b>CUTOFF</b> sets how bright the sound is: "
    "turned down, it is muffled; turned up, it is bright. <b>RESONANCE</b> boosts the frequencies right at the cutoff: the "
    "sound becomes nasal, then whistles. With resonance very high, the filter whistles on its own.",
    "Le filtre retire les aigus, comme un réglage de tonalité très puissant. <b>CUTOFF</b> (coupure) règle la brillance : "
    "bas, le son est étouffé ; haut, il est brillant. La <b>RESONANCE</b> renforce les fréquences proches de la coupure : le "
    "son devient nasal, puis siffle. Poussé très haut, le filtre siffle tout seul.") +
 H3("4. The envelopes: how the sound evolves", "4. Les enveloppes : comment le son évolue", FAM["env"]) +
 P2("An envelope describes what happens from the moment you press a key until after you release it, in four steps:",
    "Une enveloppe décrit ce qui se passe entre le moment où vous appuyez sur une touche et celui où le son s'arrête, en "
    "quatre étapes :") +
 LI([("<b>ATTACK</b>: how fast the sound appears (a piano: instant; strings: slow).",
      "<b>ATTACK</b> (attaque) : la vitesse d'apparition du son (un piano : immédiate ; des cordes : lente)."),
     ("<b>DECAY</b>: how fast it then drops.", "<b>DECAY</b> (déclin) : la vitesse à laquelle il redescend ensuite."),
     ("<b>SUSTAIN</b>: the level it holds while you keep the key down.", "<b>SUSTAIN</b> (maintien) : le niveau gardé tant "
      "que la touche reste enfoncée."),
     ("<b>RELEASE</b>: how long it takes to die away once you let go.", "<b>RELEASE</b> (relâchement) : le temps qu'il met à "
      "s'éteindre une fois la touche relâchée.")]) +
 P2("The Guru-600, like the Prophet-600, has two: the <b>AMPLIFIER</b> envelope shapes the volume; the <b>FILTER ENVELOPE</b> opens and closes "
    "the filter — the 'wah' of a brass attack, the 'pluck' of a clavinet.",
    "Le Guru-600, comme le Prophet-600, en a deux : l'enveloppe d'<b>AMPLIFIER</b> façonne le volume, la <b>FILTER ENVELOPE</b> ouvre et ferme "
    "le filtre — le « wah » d'une attaque de cuivre, le « pincé » d'un clavinet.") +
 H3("5. The LFO: movement", "5. Le LFO : le mouvement", FAM["lfo"]) +
 P2("The LFO (low-frequency oscillator) is a slow, inaudible wave that moves another setting up and down: the pitch "
    "(<b>vibrato</b>), the filter (<b>wah-wah</b>), the pulse width (shimmer) or the volume (<b>tremolo</b>).",
    "Le LFO (oscillateur basse fréquence) est une onde lente, inaudible, qui fait bouger un autre réglage : la hauteur "
    "(<b>vibrato</b>), le filtre (<b>wah-wah</b>), la largeur d'impulsion (scintillement) ou le volume (<b>trémolo</b>).") +
 H3("6. Poly-Mod: the Prophet's signature", "6. La Poly-Mod : la signature du Prophet", FAM["pm"]) +
 P2("<b>POLY-MOD</b> lets the filter envelope or oscillator B shape oscillator A's pitch or the filter, inside each voice. "
    "Small amounts add bite; larger amounts make bells, metallic sounds, sweeps and sound effects that ordinary "
    "synthesizers cannot produce.",
    "La <b>POLY-MOD</b> permet à l'enveloppe du filtre ou à l'oscillateur B de modeler la hauteur de l'oscillateur A ou le "
    "filtre, dans chaque voix. Une faible dose ajoute du mordant ; une forte dose donne des cloches, des sons métalliques, des balayages "
    "et des effets qu'un synthétiseur ordinaire ne sait pas faire.") +
 H3("7. Voices, unison and glide", "7. Voix, unisson et glide", FAM["vce"]) +
 P2("Six <b>voices</b> mean six notes at once. <b>UNISON</b> stacks all the voices on one note for a huge single-note "
    "sound (basses, leads). <b>GLIDE</b> slides from one note to the next instead of jumping.",
    "Six <b>voix</b>, c'est six notes en même temps. L'<b>UNISON</b> empile toutes les voix sur une seule note pour un son "
    "énorme (basses, leads). Le <b>GLIDE</b> fait glisser d'une note à l'autre au lieu de sauter.") +
 H3("8. Effects", "8. Les effets", "#9a9486") +
 LI([("<b>REV</b> (reverb): the sound of a room or a hall around the instrument.", "<b>REV</b> (réverbération) : le son "
      "d'une pièce ou d'une salle autour de l'instrument."),
     ("<b>DLY</b> (delay): echoes that repeat the sound.", "<b>DLY</b> (delay) : des échos qui répètent le son."),
     ("<b>CHO</b> (chorus): a slightly doubled, wider sound.", "<b>CHO</b> (chorus) : un son légèrement doublé, plus large."),
     ("<b>DST</b> (distortion): saturates the sound, from warm to aggressive.", "<b>DST</b> (distorsion) : sature le son, "
      "du chaud à l'agressif.")]) +
 BOX("tip", ("Chapter {ch:p600} shows where each of these controls is on the Guru-600, page by page.", "Le chapitre {ch:p600} montre où se trouve chacune de ces commandes sur le Guru-600, page par page.")))
