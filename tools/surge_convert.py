"""Sons de Surge XT (GPL-3, patches_factory) -> réglages du moteur P600 (unités internes du Guru-600).
Ne garde que les sons « analogiques » (oscillateurs Classic ou Sine, sans FM ni anneau, une seule scène).
La traduction est une adaptation : le Prophet-600 a deux oscillateurs, un filtre 24 dB et deux enveloppes.
    python3 -I p600/surge_convert.py DOSSIER_FXP Felucca/build/gen/felucca_tables.h p600/banques/guru/surge_candidates.json"""
import glob, json, math, os, re, sys

def table(src, n):
    m = re.search(n + r'\[128\] = \{([^}]*)\}', src)
    return [int(x) for x in re.findall(r'\d+', m.group(1))]

def near(tab, v):                                  # index of the table value nearest v (log scale)
    v = max(v, 1e-6)
    return min(range(128), key=lambda i: abs(math.log(max(tab[i], 1e-6)) - math.log(v)))

def clamp(v, lo, hi):
    return max(lo, min(hi, int(round(v))))

def read(path):
    d = open(path, 'rb').read()
    x = d[d.find(b'<?xml'):].decode('utf8', 'replace')
    p = {m.group(1): m.group(2) for m in re.finditer(r'<([a-z0-9_]+) type="\d+" value="([^"]+)"', x)}
    mods = {}
    for m in re.finditer(r'<(a_[a-z0-9_]+) type="\d+" value="[^"]+">((?:<modrouting[^>]*/>)+)</', x):
        mods[m.group(1)] = [(int(a), float(b)) for a, b in re.findall(r'source="(\d+)" depth="([-0-9.e]+)"', m.group(2))]
    meta = re.search(r'<meta name="([^"]*)" category="([^"]*)"[^>]*author="([^"]*)"', x)
    return p, mods, meta.groups() if meta else ('?', '?', '?')

def f(p, k, d=0.0):
    try:
        return float(p.get(k, d))
    except ValueError:
        return d

def main(folder, tables, out):
    src = open(tables).read()
    TIME, LFO, CUT = (table(src, n) for n in ('TIME_MS_X10', 'LFO_HZ_X100', 'CUTOFF_HZ'))
    tm = lambda log2s: 0 if log2s <= -7.9 else near(TIME, 10000 * 2 ** log2s)   # Surge: log2 seconds -> F_TIME index
    res = []
    for path in sorted(glob.glob(os.path.join(folder, '*', '*.fxp'))):
        p, mods, (name, cat, author) = read(path)
        act = [k for k in (1, 2, 3) if p.get(f'a_mute_o{k}') == '0']
        types = [p.get(f'a_osc{k}_type') for k in act]
        if not act or not all(t in ('0', '1') for t in types) or p.get('a_fm_switch', '0') != '0' or \
           p.get('scenemode', '0') != '0' or p.get('a_mute_ring12', '1') != '1' or p.get('a_mute_ring23', '1') != '1':
            continue
        if p.get('a_filter1_type') not in ('0', '1', '2', '3'):          # low-pass or none only
            continue
        osc = []
        for k in act[:2]:
            t = p.get(f'a_osc{k}_type')
            shape = f(p, f'a_osc{k}_param0')
            if t == '1':
                w = 2                                                       # sine -> TRI
            elif shape < -0.5:
                w = 4                                                       # PULSE
            elif shape < -0.1:
                w = 5                                                       # SAW+P
            else:
                w = 1                                                       # SAW
            semis = 12 * f(p, f'a_osc{k}_octave') + f(p, f'a_osc{k}_pitch')
            osc.append(dict(w=w, semis=semis, width=f(p, f'a_osc{k}_param1', 0.5), sync=f(p, f'a_osc{k}_param4'),
                            uni=f(p, f'a_osc{k}_param6', 1), det=f(p, f'a_osc{k}_param5'),
                            lvl=f(p, f'a_level_o{k}', 1)))
        a = osc[0]; b = osc[1] if len(osc) > 1 else dict(osc[0], semis=osc[0]['semis'])
        base = 12 * f(p, 'a_octave') + f(p, 'a_pitch')
        e = [0] * 8
        e[0] = a['w']; e[2] = b['w']
        e[1] = clamp(24 + base + a['semis'] + (a['sync'] if a['sync'] > 0.5 else 0), 0, 63)
        e[3] = clamp(24 + base + b['semis'], 0, 63)
        if len(osc) == 1:
            e[6] = 0                                                       # A only
        else:
            la, lb = a['lvl'], b['lvl']
            e[6] = clamp(127 * lb / max(la + lb, 1e-6), 0, 127)
        ftype = p.get('a_filter1_type')
        hz = 440 * 2 ** (f(p, 'a_filter1_cutoff') / 12) if ftype != '0' else 16000
        e[4] = near(CUT, hz)
        e[5] = clamp(f(p, 'a_filter1_resonance') * 120, 0, 120) if ftype != '0' else 0
        e[7] = clamp(abs(f(p, 'a_filter1_envmod')) / 108 * 127, 0, 127)
        env = [tm(f(p, 'a_env1_attack', -8)), tm(f(p, 'a_env1_decay', -8)),
               clamp(f(p, 'a_env1_sustain', 1) * 127, 0, 127), tm(f(p, 'a_env1_release', -8))]
        fenv = [tm(f(p, 'a_env2_attack', -8)), tm(f(p, 'a_env2_decay', -8)),
                clamp(f(p, 'a_env2_sustain', 1) * 127, 0, 127), tm(f(p, 'a_env2_release', -8))]
        kt = f(p, 'a_filter1_keytrack')
        uni = max(a['uni'], b['uni'])
        poly = p.get('a_polymode', '0')
        x = dict(fenv=fenv, pw=[clamp(64 + (a['width'] - 0.5) * 100, 8, 120), clamp(64 + (b['width'] - 0.5) * 100, 8, 120)],
                 fine=clamp(abs(b['semis'] - round(b['semis'])) * 127, 0, 127) if len(osc) > 1 else 0,
                 sync=int(a['sync'] > 0.5), pm=[0, 0, 0], kbd=0 if kt < 0.25 else 1 if kt < 0.75 else 2,
                 lfo=[near(LFO, 2 ** f(p, 'a_lfo0_rate', 0)), 1 if p.get('a_lfo0_shape', '1') in ('0', '1') else 3],
                 lfod=[0, 0, 0], glide=tm(f(p, 'a_portamento', -8)), unison=int(poly != '0' and uni > 1),
                 lfoamp=0, vel=0, detune=clamp(max(a['det'], b['det']) * 160, 0, 127), wheel=64)
        res.append(dict(file=os.path.relpath(path, folder), name=name, family=os.path.basename(os.path.dirname(path)),
                        author=author, e=e, env=env, x=x, mono=poly != '0'))
    json.dump(res, open(out, 'w'), indent=1, ensure_ascii=False)
    print(len(res), 'candidats ->', out)

if __name__ == '__main__':
    main(*sys.argv[1:4])
