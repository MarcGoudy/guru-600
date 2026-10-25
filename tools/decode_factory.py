"""Décode la banque d'usine du Prophet-600 (dump SysEx SCI, 100 x 37 octets).
Format : F0 01 02 <n°> 32 quartets (16 octets, poids faible d'abord) F7.
Champs de bits dans l'ordre de gligli p600fw common/import.c (struct z80Patch_t, LSB d'abord)."""
import json, sys

FIELDS = [("pwA",7),("pmodFilEnv",4),("lfoFreq",4),("pmodOscB",7),("lfoAmt",5),("freqB",6),
          ("freqA",6),("fineB",7),("mixer",6),("cutoff",7),("reso",6),("filEnvAmt",4),
          ("filRel",4),("filSus",4),("filDec",4),("filAtk",4),("ampRel",4),("ampSus",4),
          ("ampDec",4),("ampAtk",4),("glide",4),("pwB",7),
          ("pulseA",1),("pulseB",1),("trackFull",1),("trackHalf",1),("lfoShape",1),("lfoPitch",1),
          ("lfoPW",1),("lfoFil",1),("sawA",1),("triA",1),("syncA",1),("sawB",1),("triB",1),
          ("pmodFreqA",1),("pmodFil",1),("unison",1)]

def decode(path):
    d = open(path, "rb").read()
    out, i = [], 0
    while (s := d.find(b"\xf0", i)) >= 0:
        e = d.find(b"\xf7", s)
        m = d[s + 1:e]
        i = e + 1
        assert m[0] == 1 and m[1] == 2 and len(m) == 35, m.hex()
        raw = bytes((m[k*2+3] & 15) | ((m[k*2+4] & 15) << 4) for k in range(16))
        bits = int.from_bytes(raw, "little")
        p, pos = {"prog": m[2]}, 0
        for name, w in FIELDS:
            p[name] = (bits >> pos) & ((1 << w) - 1)
            pos += w
        out.append(p)
    return out

if __name__ == "__main__":
    bank = decode(sys.argv[1])
    json.dump(bank, open(sys.argv[2], "w"), indent=1)
    print(len(bank), "programmes ;", sum(w for _, w in FIELDS), "bits")
    for p in bank[:6]:
        print(p)
