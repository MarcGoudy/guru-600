# 26 · The Prophet-600 panel ↔ the Guru-600
MAP2 = [("POLY-MOD › FILTER ENVELOPE, OSC B", "EDIT › POLY MOD (1/11) › PM EN, PM B"),
        ("POLY-MOD › FREQ A, FILTER (switches)", ("EDIT › POLY MOD (1/11) › PM DS: FRQ A, FILT, BOTH", "EDIT › POLY MOD (1/11) › PM DS : FRQ A, FILT, BOTH")),
        ("LFO › FREQUENCY, SHAPE", "LFO › RATE, WAVE"),
        ("LFO › INITIAL AMOUNT", ("EDIT › EXTRAS (7/11) › WHEEL (lower WHEEL = more LFO without the wheel)", "EDIT › EXTRAS (7/11) › WHEEL (WHEEL plus bas = plus de LFO sans la molette)")),
        ("LFO › FREQ, PW, FILTER (switches)", ("LFO › LFO DEST › PIT, SHP, FLT (0 or 100 %)", "LFO › LFO DEST › PIT, SHP, FLT (0 ou 100 %)")),
        ("OSC A › FREQUENCY, SAW / TRI / PULSE", "EDIT › OSC (2/11) › A FRQ, A WAV"),
        ("OSC A › PULSE WIDTH, SYNC", "EDIT › OSC 2 (3/11) › A PW, SYNC"),
        ("OSC B › FREQUENCY, SAW / TRI / PULSE", "EDIT › OSC (2/11) › B FRQ, B WAV"),
        ("OSC B › FINE, PULSE WIDTH", "EDIT › OSC 2 (3/11) › B FIN, B PW"),
        ("MIXER › OSC A / OSC B", ("EDIT › MIXER (4/11) › MIX (also HOME › KNOB 4)", "EDIT › MIXER (4/11) › MIX (aussi HOME › KNOB 4)")),
        ("GLIDE", "EDIT › MIXER (4/11) › GLD"),
        ("UNISON", "EDIT › MIXER (4/11) › VCE = UNI"),
        ("FILTER › CUTOFF, RESONANCE, ENVELOPE AMOUNT", ("EDIT › FILTER (5/11) › CUT, RES, FENV (also HOME › KNOB 1 to 3)", "EDIT › FILTER (5/11) › CUT, RES, FENV (aussi HOME › KNOB 1 à 3)")),
        ("FILTER › KEYBOARD HALF / FULL", "EDIT › FILTER (5/11) › KBD"),
        ("FILTER ENVELOPE › ATTACK, DECAY, SUSTAIN, RELEASE", "EDIT › FLT ENV (6/11)"),
        ("AMPLIFIER › ATTACK, DECAY, SUSTAIN, RELEASE", "ENV (1/2)"),
        ("MASTER VOLUME", "MASTER"), ("TUNE", "MENU › AUDIO › TUNE"),
        (("PROGRAM (the numeric keys)", "PROGRAM (les touches numériques)"), "PRESETS"), ("RECORD", "SAVE › PLACE"),
        (("Pitch wheel", "Molette de hauteur"), ("a MIDI keyboard's pitch wheel", "celle d'un clavier MIDI")),
        (("Mod wheel", "Molette de modulation"), ("a MIDI keyboard's mod wheel, or SELECT = MODW; its amount: EDIT › EXTRAS › WHEEL", "celle d'un clavier MIDI, ou SELECT = MODW ; son dosage : EDIT › EXTRAS › WHEEL"))]


CH("panel", "The Prophet-600 panel ↔ the Guru-600", "La façade du Prophet-600 ↔ le Guru-600",
 '<figure class="wide"><img src="img/facade.png" alt=""></figure>' +
 P2("Where each control of the Prophet-600's panel is on the Guru-600.",
    "Où se trouve chaque commande de la façade du Prophet-600 sur le Guru-600.") +
 table([("Prophet-600 panel", "Façade du Prophet-600"), ("Guru-600 on the FM-1", "Le Guru-600 sur le FM-1")], [[(e(a[0]), e(a[1])) if isinstance(a, tuple) else e(a), (e(b[0]), e(b[1])) if isinstance(b, tuple) else e(b)] for a, b in MAP2]) +
 P2("The same controls respond to the MIDI CC numbers of the GliGli firmware (chapter {ch:midi}).",
    "Les mêmes commandes répondent aux numéros de CC MIDI du firmware GliGli (chapitre {ch:midi})."))
