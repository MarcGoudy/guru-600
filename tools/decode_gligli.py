"""Décode un dump SysEx de patchs du firmware GliGli (Prophet-600 modernisé, gligli p600fw / image-et-son) :
F0 00 61 16 01 <données brouillées 5 -> 4 : n° de programme puis le preset tel que storage.c l'écrit> F7.
Lecture selon storage.c preset_loadCurrent (versions 1, 2, 7, 8). Sortie : JSON des paramètres bruts (16 bits)."""
import json, struct, sys

CP = ["FreqA", "VolA", "APW", "FreqB", "VolB", "BPW", "FreqBFine", "Cutoff", "Resonance", "FilEnvAmt", "FilRel", "FilSus",
      "FilDec", "FilAtt", "AmpRel", "AmpSus", "AmpDec", "AmpAtt", "PModFilEnv", "PModOscB", "LFOFreq", "LFOAmt", "Glide",
      "AmpVelocity", "FilVelocity", "ModDelay", "VibFreq", "VibAmt", "UnisonDetune", "SeqArpClock"]
SP1 = ["ASaw", "ATri", "ASqr", "BSaw", "BTri", "BSqr", "Sync", "PModFA", "PModFil", "LFOShape"]
SP2 = ["LFOTargets", "TrackingShift", "FilEnvShape", "FilEnvSlow", "AmpEnvShape", "AmpEnvSlow", "Unison",
       "AssignerPriority", "BenderSemitones", "BenderTarget", "ModWheelRange", "ChromaticPitch"]


def descramble(body):                      # midi.c sysexDescrambleBuffer : 5 octets 7 bits -> 4 octets
    out = bytearray()
    for i in range(0, len(body), 5):
        ch = body[i:i + 5]
        b = ch[4] if len(ch) > 4 else 0
        for k in range(min(4, len(ch))):
            out.append(ch[k] | (((b >> k) & 1) << 7))
    return bytes(out)


def parse(msg):
    assert msg[:4] == b"\x00\x61\x16\x01", msg[:4].hex()
    raw = descramble(msg[4:])
    num, buf, pos = raw[0], raw[1:] + bytes(256), 0   # (les octets nuls de la fin ne sont pas toujours envoyés)

    def rd(fmt):
        nonlocal pos
        v = struct.unpack_from("<" + fmt, buf, pos)
        pos += struct.calcsize(fmt)
        return v[0]
    p = {"prog": num, "magic": hex(rd("I")), "version": rd("B")}
    for n in CP[:25]:
        p[n] = rd("H")
    for n in SP1:
        p[n] = rd("B")
    p["LFOShiftLegacy"] = rd("B")
    for n in SP2:
        p[n] = rd("B")
    if p["version"] >= 2:
        for n in CP[25:30]:
            p[n] = rd("H")
        p["ModwheelTarget"], p["VibTarget"] = rd("B"), rd("B")
        p["voicePattern"] = [rd("B") for _ in range(6)]
    if p["version"] >= 7:
        p["tuning"] = [rd("H") for _ in range(12)]
    if p["version"] >= 8:
        p["PWMBug"], p["Spread"], p["External"] = rd("B"), rd("H"), rd("H")
        p["EnvRouting"], p["Assign"], p["LFOSync"] = rd("B"), rd("B"), rd("B")
        p["name"] = bytes(rd("B") for _ in range(16)).split(b"\0")[0].decode("latin-1").strip()
    return p


def decode(path):
    d = open(path, "rb").read()
    out, i = [], 0
    while (s := d.find(b"\xf0", i)) >= 0:
        e = d.find(b"\xf7", s)
        out.append(parse(d[s + 1:e]))
        i = e + 1
    return out


if __name__ == "__main__":
    bank = decode(sys.argv[1])
    json.dump(bank, open(sys.argv[2], "w"), indent=1)
    print(len(bank), "programmes")
    for p in bank[:3] + bank[19:20] + bank[24:25]:
        print({k: p[k] for k in ("prog", "magic", "version", "name", "FreqA", "FreqB", "Cutoff", "Resonance", "FilEnvAmt",
                                 "ASaw", "ASqr", "BSaw", "Unison", "LFOFreq", "LFOAmt", "LFOShape", "LFOTargets")})
