"""Les 25 sons originaux du Guru-600 (places 226 à 250 de la banque) : réglages en unités lisibles (ms, Hz, %),
convertis en unités internes du moteur P600 avec les tables du firmware. Créés pour le Guru-600 (Marc Massé, 2026),
sous la licence du projet (GPL-3).
    python3 -I p600/originals.py Felucca/build/gen/felucca_tables.h p600/banques/guru/originals.json"""
import json, math, re, sys

src = open(sys.argv[1]).read()
def table(n):
    m = re.search(n + r'\[128\] = \{([^}]*)\}', src)
    return [int(x) for x in re.findall(r'\d+', m.group(1))]
TIME, LFO, CUT = table('TIME_MS_X10'), table('LFO_HZ_X100'), table('CUTOFF_HZ')
near = lambda tab, v: min(range(128), key=lambda i: abs(math.log(max(tab[i], 1e-6)) - math.log(max(v, 1e-6))))
ms = lambda v: 0 if v <= 1 else near(TIME, v * 10)          # milliseconds -> F_TIME
hz = lambda v: near(CUT, v)                                  # filter cutoff in Hz
lhz = lambda v: near(LFO, v * 100)                           # LFO rate in Hz
pc = lambda v: round(v * 127 / 100)                          # percent -> 0..127
SAW, TRI, PLS = 1, 2, 4

def snd(name, family, a=SAW, fa=0, b=SAW, fb=0, cut=2000, res=0, mix=50, fenv=0, amp=(1, 300, 100, 300),
        fe=(1, 300, 0, 300), pw=(50, 50), fine=0, sync=0, pm_env=0, pm_b=0, pm_dst=0, kbd=2, lfo=(5, 'tri'),
        lfod=(0, 0, 0), glide=0, unison=0, lfoamp=0, vel=0, detune=12, wheel=64, mono=False, about=('', '')):
    wave = {'sin': 0, 'tri': 1, 'saw': 2, 'sqr': 3, 'sh': 4}[lfo[1]]
    return dict(name=name, family=family, about=about,
                e=[a, 24 + fa, b, 24 + fb, hz(cut), pc(res), pc(mix), pc(fenv)],
                env=[ms(amp[0]), ms(amp[1]), pc(amp[2]), ms(amp[3])],
                x=dict(fenv=[ms(fe[0]), ms(fe[1]), pc(fe[2]), ms(fe[3])], pw=[pc(pw[0]), pc(pw[1])], fine=fine,
                       sync=sync, pm=[pc(pm_env), pc(pm_b), pm_dst], kbd=kbd, lfo=[lhz(lfo[0]), wave],
                       lfod=list(lfod), glide=ms(glide), unison=unison, lfoamp=lfoamp, vel=vel, detune=detune,
                       wheel=wheel), mono=mono)

FA, FL, BOTH = 1, 2, 3          # POLY-MOD destinations
S = [
 snd('GLASS BELLS', 'Bells', a=TRI, b=PLS, fb=19, fine=40, cut=9000, mix=10, amp=(1, 2500, 0, 2500), pm_b=55, pm_dst=FA,
     about=('Osc B modulates osc A at a non-harmonic ratio: clear, glassy bells. Play high.',
            "L'oscillateur B module l'oscillateur A à un rapport non harmonique : des cloches claires, de verre. Jouez dans l'aigu.")),
 snd('GONG', 'Bells', a=SAW, b=PLS, fb=7, fine=70, cut=4000, res=20, mix=20, fenv=40, amp=(1, 6000, 0, 6000),
     fe=(1, 4000, 0, 4000), pm_b=75, pm_env=30, pm_dst=FA,
     about=('A metallic hit that rings for seconds. Play low and let it die away.',
            'Un coup métallique qui résonne plusieurs secondes. Jouez dans le grave et laissez-le s\'éteindre.')),
 snd('SYNC SCREAM', 'Lead', a=SAW, fa=12, b=SAW, cut=6000, res=25, mix=0, fenv=30, sync=1, pm_env=80, pm_dst=FA,
     amp=(5, 500, 85, 300), fe=(5, 900, 20, 400), mono=True, glide=60,
     about=('Osc A synced to B, its pitch swept by the filter envelope through POLY-MOD: the classic sync scream.',
            "L'oscillateur A synchronisé sur B, sa hauteur balayée par l'enveloppe du filtre via la POLY-MOD : le cri de synchro classique.")),
 snd('WATER DROP', 'Percussion', mix=0, cut=300, res=92, fenv=70, amp=(1, 350, 0, 350), fe=(1, 120, 0, 120),
     about=('The self-oscillating filter dropping in pitch: a drop of water. Try different notes.',
            "Le filtre en auto-oscillation qui chute en hauteur : une goutte d'eau. Essayez plusieurs notes.")),
 snd('SYNTH TOM', 'Percussion', a=TRI, mix=0, cut=120, res=95, fenv=45, amp=(1, 500, 0, 400), fe=(1, 250, 0, 250),
     about=('An 80s electronic tom, from the filter alone. Play low to mid.',
            'Un tom électronique des années 80, fait avec le seul filtre. Jouez du grave au médium.')),
 snd('METAL PLATE', 'FX', a=PLS, b=PLS, fb=6, fine=30, pw=(30, 70), cut=3500, res=50, mix=40, fenv=20,
     amp=(1, 900, 0, 900), fe=(1, 300, 0, 300), pm_b=60, pm_dst=BOTH,
     about=('A struck metal sheet: osc B modulates both osc A and the filter.',
            "Une plaque de métal frappée : l'oscillateur B module à la fois l'oscillateur A et le filtre.")),
 snd('LASER ZAP', 'FX', a=SAW, mix=0, cut=8000, fenv=10, pm_env=100, pm_dst=FA, amp=(1, 250, 0, 200), fe=(1, 200, 0, 200),
     about=('A fast pitch fall from the filter envelope through POLY-MOD: laser shots.',
            "Une chute de hauteur très rapide, par l'enveloppe du filtre via la POLY-MOD : des tirs de laser.")),
 snd('SONAR PING', 'FX', mix=0, cut=1500, res=96, fenv=15, amp=(1, 3000, 0, 3000), fe=(1, 60, 0, 60),
     lfo=(0.4, 'sin'), lfod=(4, 0, 0), wheel=0,
     about=('A pure ping that fades slowly, with a slight drift: a submarine sonar.',
            "Un « ping » pur qui s'éteint lentement, avec une légère dérive : le sonar d'un sous-marin.")),
 snd('S&H BLEEPS', 'Sequence', a=PLS, b=SAW, fb=12, cut=800, res=80, mix=40, lfo=(7, 'sh'), lfod=(0, 0, 63), wheel=0,
     amp=(1, 300, 90, 200),
     about=('The LFO in Sample & Hold sets the filter at random: computer bleeps. Hold a note or a chord.',
            "Le LFO en échantillonneur-bloqueur règle le filtre au hasard : des bips d'ordinateur. Tenez une note ou un accord.")),
 snd('DRONE FIFTHS', 'Pad', a=SAW, b=SAW, fb=7, fine=10, cut=900, res=30, mix=50, fenv=15, amp=(3000, 3000, 100, 5000),
     fe=(5000, 5000, 60, 5000), lfo=(0.2, 'tri'), lfod=(0, 30, 0), wheel=0,
     about=('A slow drone in fifths that opens over several seconds. Hold one note.',
            'Un bourdon lent en quintes qui s\'ouvre en plusieurs secondes. Tenez une seule note.')),
 snd('SLOW SWEEP', 'Pad', a=PLS, b=PLS, fb=12, pw=(25, 40), cut=250, res=45, mix=50, fenv=70, amp=(1500, 2000, 100, 4000),
     fe=(4000, 6000, 30, 5000), lfo=(0.3, 'tri'), lfod=(0, 40, 0), wheel=0,
     about=('A dark pad whose filter rises slowly while the pulse widths shimmer.',
            "Une nappe sombre dont le filtre s'ouvre lentement pendant que les largeurs d'impulsion scintillent.")),
 snd('TRILL LEAD', 'Lead', a=SAW, b=PLS, fb=12, cut=3500, res=20, mix=30, lfo=(7, 'sqr'), lfod=(8, 0, 0), wheel=0,
     amp=(5, 300, 90, 200), mono=True,
     about=('A square LFO on the pitch makes a fast trill, as the Prophet-600 manual suggests.',
            "Un LFO carré sur la hauteur produit un trille rapide, comme le suggère le manuel du Prophet-600.")),
 snd('WOBBLE BASS', 'Bass', a=SAW, fa=-12, b=PLS, fb=-12, cut=400, res=60, mix=50, lfo=(3, 'tri'), lfod=(0, 0, 50),
     wheel=0, amp=(1, 300, 100, 150), mono=True,
     about=('A filter wobbled by the LFO at three beats a second. Turn LFO FREQUENCY to follow the tempo.',
            'Un filtre secoué par le LFO, trois fois par seconde. Réglez LFO FREQUENCY sur le tempo.')),
 snd('HARP PLUCK', 'Pluck', a=TRI, b=SAW, fb=12, cut=700, res=15, mix=35, fenv=55, amp=(1, 1200, 0, 900),
     fe=(1, 350, 0, 400), vel=30,
     about=('A bright pluck that rounds off as it fades, close to a harp. Velocity opens it.',
            "Un son pincé brillant qui s'arrondit en s'éteignant, proche d'une harpe. La vélocité l'ouvre."))
 ,snd('ROBOT VOICE', 'FX', a=SAW, b=TRI, fb=-5, fine=20, cut=900, res=85, mix=10, pm_b=55, pm_dst=FL,
     amp=(10, 400, 90, 200),
     about=('Osc B moves the resonant filter at audio rate: a talking robot. Play slow melodies.',
            "L'oscillateur B fait bouger le filtre résonant à vitesse audio : un robot qui parle. Jouez des mélodies lentes.")),
 snd('SIREN', 'FX', a=SAW, b=SAW, fb=0, fine=15, cut=4000, mix=50, lfo=(0.5, 'tri'), lfod=(60, 0, 0), wheel=0,
     glide=800, mono=True, amp=(10, 300, 100, 500),
     about=('A big pitch swing from the LFO, with glide: a siren. Hold one note.',
            'Un grand balancement de hauteur par le LFO, avec glide : une sirène. Tenez une note.')),
 snd('ARP PULSE', 'Sequence', a=PLS, b=PLS, fb=12, pw=(18, 30), cut=1200, res=40, mix=30, fenv=45,
     amp=(1, 220, 0, 150), fe=(1, 150, 0, 150),
     about=('A short, narrow pulse made for the arpeggiator and the sequencer.',
            "Une impulsion courte et étroite, faite pour l'arpégiateur et le séquenceur.")),
 snd('CLOCK TICK', 'Percussion', mix=0, cut=5000, res=94, fenv=20, amp=(1, 45, 0, 40), fe=(1, 30, 0, 30), kbd=2,
     about=('A tiny high tick, for rhythms in the sequencer.',
            'Un petit « tic » aigu, pour les rythmes du séquenceur.')),
 snd('BOWED METAL', 'Pad', a=TRI, b=PLS, fb=5, fine=45, cut=3000, res=25, mix=20, pm_b=45, pm_dst=FA,
     amp=(800, 2000, 85, 2500), lfo=(4.5, 'sin'), lfod=(3, 0, 0), wheel=0,
     about=('A bowed metal bar: inharmonic, slow to start, with a light vibrato.',
            "Une barre de métal frottée à l'archet : inharmonique, lente à démarrer, avec un léger vibrato.")),
 snd('CHIME PAD', 'Pad', a=TRI, b=TRI, fb=24, fine=25, cut=6000, mix=40, pm_b=35, pm_dst=FA, amp=(600, 3000, 60, 5000),
     about=('Soft bells that swell in and ring on: a bell pad.',
            'Des cloches douces qui gonflent et résonnent longtemps : une nappe de cloches.')),
 snd('UNISON MONSTER', 'Lead', a=SAW, fa=-12, b=SAW, fb=-12, fine=15, cut=1800, res=30, mix=50, fenv=25, unison=1,
     detune=110, glide=40, amp=(1, 400, 100, 300), fe=(1, 500, 30, 300), mono=True,
     about=('All six voices stacked and wide apart on one note: a huge bass-lead.',
            'Les six voix empilées et très désaccordées sur une seule note : une basse-lead énorme.')),
 snd('RAVE HOOVER', 'Lead', a=PLS, b=SAW, fb=-12, pw=(12, 50), cut=3000, res=10, mix=50, pm_env=25, pm_dst=FA, unison=1,
     detune=90, glide=120, lfo=(6, 'tri'), lfod=(0, 50, 0), wheel=0, amp=(1, 400, 100, 400), fe=(1, 600, 0, 600), mono=True,
     about=('A narrow pulse with a fast pulse-width LFO, unison and a pitch dip: the 90s rave sound.',
            "Une impulsion étroite avec un LFO rapide sur sa largeur, l'unisson et une petite plongée de hauteur : le son des raves des années 90.")),
 snd('DIGITAL RAIN', 'Sequence', a=TRI, b=PLS, fb=12, cut=2500, res=30, mix=30, lfo=(6, 'sh'), lfod=(30, 0, 0), wheel=0,
     amp=(1, 180, 0, 300),
     about=('Sample & Hold on the pitch: random notes at every LFO step. Hold a key.',
            "L'échantillonneur-bloqueur sur la hauteur : une note au hasard à chaque pas du LFO. Tenez une touche.")),
 snd('GATED PAD', 'Pad', a=SAW, b=SAW, fb=12, fine=8, cut=1500, res=20, mix=45, lfo=(8, 'sqr'), lfoamp=63, wheel=0,
     amp=(200, 2000, 100, 1500),
     about=('A pad chopped by a square LFO on the volume: a rhythmic gate.',
            'Une nappe hachée par un LFO carré sur le volume : un effet de porte rythmique.')),
 snd('RING BASS', 'Bass', a=SAW, fa=-12, b=TRI, fb=-5, fine=10, cut=1200, res=35, mix=15, pm_b=40, pm_dst=FA,
     fenv=30, amp=(1, 600, 70, 150), fe=(1, 300, 10, 200), mono=True,
     about=('Osc B modulates osc A at a low ratio: a grainy, metallic bass.',
            "L'oscillateur B module l'oscillateur A à un rapport grave : une basse granuleuse et métallique.")),
]
json.dump(S, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
print(len(S), 'sons ->', sys.argv[2])
