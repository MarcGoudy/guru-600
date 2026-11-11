"""Banque d'usine du Prophet-600 -> firmware/src/p600_bank.h (moteur P600 de Felucca).
Entrée : factory_bank.json (decode_factory.py). Les conversions suivent gligli p600fw common/import.c
quand il en donne une ; sinon ce sont des approximations, à régler à l'oreille.
    python3 make_bank.py factory_bank.json ../Felucca/firmware/src/p600_bank.h [banques/v2022_bank.json [banques/guru/guru_extras.json]]"""
import json, math, sys
# (10/11, Marc) les noms que la coupure à 11 caractères rendrait identiques à un autre : abrégés pour rester distincts
ABBR = {"Orchestral 1": "Orch. 1", "Orchestral 2": "Orch. 2", "Orchestral 3": "Orch. 3", "Space Oboe Chord": "Sp.Oboe Ch.",
        # the v2022 versions of factory sounds (Z80 Nbr.) take a 2, as the factory's keep their name
        "Club Organ": "ClubOrgan 2", "Chiffy Organ": "ChiffyOrg 2", "Harmonica": "Harmonica 2", "Pulse Mod I": "PulseModI 2"}

FACTORY_NAMES = json.load(open(__file__.rsplit("/", 1)[0] + "/factory_names.json"))   # le manuel CM600A, figure 11-0
Z80_ENV_CV = [0, 55, 86, 101, 111, 124, 135, 139, 143, 148, 154, 164, 176, 185, 191, 210]   # import.c z80EnvCV


def env_time(v):            # 4 bits -> F_TIME 0..127 (10^(4 i/127) ms, 1 ms .. 10 s)
    # mesuré sur un vrai Prophet-600 (prophet600.blogspot.com, « Envelope analysis ») : attaque 0, 35, 105, 185 ms
    # pour 0..3 et ~10 s pour 15. Ces mesures suivent la tension CEM3310 d'import.c : t = 35 ms * e^(0.0366 (cv - 55))
    if v == 0:
        return 0
    ms = 35 * math.exp(0.0366 * (Z80_ENV_CV[v] - 55))
    return max(0, min(127, round(127 * math.log10(ms) / 4)))


def cutoff(c):              # 7 bits -> CUT (30 Hz .. 16 kHz en 127 pas) : chez GliGli (import.c, synth.c computeTunedCVs,
    # tuner.c) la note du filtre est 0.625 c demi-tons au-dessus de C0 (16,35 Hz), suivi de clavier compris à part
    hz = 16.35 * 2 ** (0.625 * c / 12)
    return max(0, min(127, round(127 * math.log(hz / 30) / math.log(16000 / 30))))


# FENV : 15 = ~9,8 octaves chez GliGli (amt << 11 sur ~3120 pas de CV par octave) ; 127 ici = 9,06 octaves


def sus(v):
    return v * 127 // 15


def lfo_rate(v):            # 4 bits -> LFO ¼ .. 20 Hz (manuel CM600A, 7-8 : « about ¼ to 20 Hz ») -> l'indice de LFO_HZ
    hz = 0.25 * 80 ** (v / 15)
    return max(0, min(127, round(127 * math.log(hz / 0.05) / math.log(800))))


def wave(saw, tri, pulse):
    return saw | tri << 1 | pulse << 2


def convert(p):
    lfo_d = p["lfoAmt"] * p["lfoAmt"] * 63 // 961   # (amt / 31)^2 : le potentiomètre d'origine est très progressif
    # la molette (manuel 7-8) : elle s'ajoute à INITIAL AMOUNT sur les destinations choisies. Les destinations à fond,
    # et la part que la molette ouvre (matrice MODW -> DEPTH, AMT a : profondeur 1 - a/64 molette en bas)
    wheel = min(63, 64 * (63 - lfo_d) // 63)       # (AMT va jusqu à 63)
    preset = {
        "name": "%d %s" % (p["prog"] + 1, FACTORY_NAMES[p["prog"]][1]),   # la place, puis le nom du manuel (abrégé)
        "e": [wave(p["sawA"], p["triA"], p["pulseA"]), p["freqA"],
              wave(p["sawB"], p["triB"], p["pulseB"]), p["freqB"],
              cutoff(p["cutoff"]), p["reso"] * 2, p["mixer"] * 2, min(127, p["filEnvAmt"] * 137 // 15)],
        "env": [env_time(p["ampAtk"]), env_time(p["ampDec"]), sus(p["ampSus"]), env_time(p["ampRel"])],
    }
    ext = {
        "fenv": [env_time(p["filAtk"]), env_time(p["filDec"]), sus(p["filSus"]), env_time(p["filRel"])],
        "pw": [p["pwA"], p["pwB"]],
        "fine": p["fineB"],
        "sync": p["syncA"],
        "pm": [p["pmodFilEnv"] * 127 // 15, p["pmodOscB"], p["pmodFreqA"] | p["pmodFil"] << 1],
        "kbd": 2 if p["trackFull"] else 1 if p["trackHalf"] else 0,
        # RATE, WAVE (1 TRI, 3 SQR : lfoShape 1 = triangle, 0 = impulsion), PIT, SHP, FLT
        "lfo": [lfo_rate(p["lfoFreq"]), 1 if p["lfoShape"] else 3,
                63 if p["lfoPitch"] else 0, 63 if p["lfoPW"] else 0, 63 if p["lfoFil"] else 0],
        "glide": p["glide"] * 6,
        "unison": p["unison"],
        "lfoamp": 0, "vel": 0, "detune": 12, "wheel": wheel,
    }
    return preset, ext


def env_cv(raw):            # un temps GliGli (16 bits, la tension CEM3310 << 8) -> F_TIME, la même courbe que env_time
    cv = raw >> 8
    if cv == 0:
        return 0
    ms = max(1.0, 35 * math.exp(0.0366 * (cv - 55)))
    return max(0, min(127, round(127 * math.log10(ms) / 4)))


def lfo_gligli(raw):        # gligli lfo.c : speed = 16 * 65535 * e^-((65535 - raw) / 8000), demi-période 2^24, 2 kHz
    hz = 2000 * 16 * 65535 * math.exp(-(65535 - raw) / 8000) / 2 ** 25
    return max(0, min(127, round(127 * math.log(max(hz, 0.05) / 0.05) / math.log(800))))


GLIGLI_LFO_WAVE = {0: 3, 1: 1, 2: 4, 3: 0, 4: 4, 5: 2}   # impulsion SQR, triangle TRI, aléatoire S&H, sinus SIN, bruit S&H, scie SAW


def convert_gligli(p):      # un programme GliGli v8 (decode_gligli.py) -> le moteur P600, en entiers comme le firmware
    clamp = lambda v, a, b: max(a, min(b, int(v)))   # (eng_p600.c p6_from_gligli : les mêmes valeurs, octet pour octet)
    fb = (p["FreqB"] >> 2) + ((p["FreqBFine"] >> 7) - 256)          # B en 1/256 de demi-ton, l'accord fin compris
    fbi = fb >> 8
    va, vb = p["VolA"], p["VolB"]
    mix = 64 if va + vb == 0 else clamp(127 * vb // (va + vb), 0, 127)
    amt = lambda raw, k: clamp(int((raw - 32768) * k / (2048 * 15)), 0, 127)   # l'échelle 4 bits du Z80 (import.c << 11)
    amp = [env_cv(p["AmpAtt"]), env_cv(p["AmpDec"]), p["AmpSus"] * 127 // 65535, env_cv(p["AmpRel"])]
    fen = [env_cv(p["FilAtt"]), env_cv(p["FilDec"]), p["FilSus"] * 127 // 65535, env_cv(p["FilRel"])]
    if p.get("EnvRouting") == 2:            # l'amplitude suit l'enveloppe du filtre
        amp = list(fen)
    elif p.get("EnvRouting") == 3:          # porte : l'amplitude ouverte tant que la touche est tenue
        amp = [0, 0, 127, 0]
    tg = p["LFOTargets"]
    depth = (p["LFOAmt"] >> 8) * (p["LFOAmt"] >> 8) * 63 // 65025
    preset = {
        "name": ABBR.get(p["name"], p["name"])[:15],   # (ABBR: a name the cut would make another's)
        "e": [wave(p["ASaw"], p["ATri"], p["ASqr"]), clamp((p["FreqA"] + 512) >> 10, 0, 63),
              wave(p["BSaw"], p["BTri"], p["BSqr"]), clamp(fbi, 0, 63),
              cutoff(p["Cutoff"] >> 8), clamp((p["Resonance"] >> 10) * 2, 0, 127), mix, amt(p["FilEnvAmt"], 137)],
        "env": amp,
    }
    ext = {
        "fenv": fen, "pw": [p["APW"] >> 9, p["BPW"] >> 9], "fine": clamp((fb - (fbi << 8)) * 127 // 256, 0, 127),
        "sync": p["Sync"], "pm": [amt(p["PModFilEnv"], 127), p["PModOscB"] >> 9, p["PModFA"] | p["PModFil"] << 1],
        "kbd": min(2, p["TrackingShift"]),
        "lfo": [lfo_gligli(((p["LFOFreq"] >> 8) << 8) | 0x80), GLIGLI_LFO_WAVE.get(p["LFOShape"], 1),
                63 if tg & 1 else 0, 63 if tg & 8 else 0, 63 if tg & 2 else 0],
        "glide": clamp(((p["Glide"] - 0xC000) >> 10) * 6, 0, 127) if p["Glide"] > 0xC000 else 0,
        "unison": 1 if p["Unison"] else 0, "lfoamp": 127 if tg & 4 else 0, "wheel": min(63, 64 * (63 - depth) // 63),
        "vel": p["FilVelocity"] * 40 // 65535, "detune": clamp(p["UnisonDetune"] >> 9, 0, 127),
    }
    return preset, ext


def c_list(v):
    return "{" + ", ".join(str(x) for x in v) + "}"


def main(src, dst, gligli=None, extras=None):
    bank = json.load(open(src))
    out = ["/* SPDX-License-Identifier: GPL-3.0-only */",
           "/* The Prophet-600's 100 factory programs (Sequential Circuits' program dump, as gligli p600fw imports it),",
           " * converted by p600/make_bank.py: do not edit. P600_PRESETS the part preset_t holds, P600_EXT the rest",
           " * (eng_p600.c p600_preset). Dry, as the original: no sends */",
           "typedef struct {",
           "    uint8_t fenv[4], pw[2], fine, sync, pm[3], kbd, lfo[2];",
           "    int8_t lfod[3];",
           "    uint8_t glide, unison, lfoamp, vel, detune, wheel;",
           "} p600_ext_t;",
           "",
           "static const preset_t P600_PRESETS[] = {"]
    exts = []
    for p in bank:
        pr, ex = convert(p)
        out.append('    {"%s", %s, %s, 0, 0, FX(0, 0, 0, 0)},' % (pr["name"], c_list(pr["e"]), c_list(pr["env"])))
        exts.append(ex)
    if gligli:                              # la collection libre v2022 (GliGli / image-et-son, GPL v3), après l'usine
        out.append("    /* the v2022 Patch Collection 1 (image-et-son.com, GPL v3): Matrix12x, el-folie, Jpro600k, Andy W., imogen */")
        for p in json.load(open(gligli)):
            pr, ex = convert_gligli(p)
            nm = ("%d %s" % (len(exts) + 1, pr["name"])).replace("\\", "").replace('"', "'")[:15].upper()   # (11/11 : tous les noms en majuscules)
            out.append('    {"%s", %s, %s, 0, 0, FX(0, 0, 0, 0)},' % (nm, c_list(pr["e"]), c_list(pr["env"])))
            exts.append(ex)
    if extras:                              # Guru-600 : places 201 .. 255, des sons Surge XT adaptés (GPL-3) et des originaux
        out.append("    /* Guru-600's own (201 .. 255): Surge XT factory sounds adapted (GPL-3, Claes Johanson), then originals */")
        for x in json.load(open(extras)):
            nm = "%d %s" % (len(exts) + 1, x["name"])
            fx = x.get("fx", [0, 0, 0, 0])
            out.append('    {"%s", %s, %s, 0, %d, FX(%d, %d, %d, %d)},' % (nm, c_list(x["e"]), c_list(x["env"]), int(x["mono"]), *fx))
            ex = dict(x["x"]); ex["lfo"] = list(x["x"]["lfo"]) + list(x["x"]["lfod"])
            exts.append(ex)
    nfix = len(exts)
    out.append("    /* the free places (up to 255) a program received as SysEx can take (eng_p600.c p600_sysex): a plain voice */")
    for k in range(255 - nfix):                    # (a track's preset number is 8 bits: 255 programs in all)
        out.append('    {"EMPTY", {3, 24, 1, 24, 90, 0, 64, 40}, {0, 70, 100, 40}, 0, 0, FX(0, 0, 0, 0)},')
    out += ["};", "#define P600_NFIX %d   /* the fixed programs; IMPORT's follow */" % nfix, "",
            "static const p600_ext_t P600_EXT[] = {"]
    for x in exts:
        out.append("    {%s, %s, %d, %d, %s, %d, %s, %s, %d, %d, %d, %d, %d, %d}," % (
            c_list(x["fenv"]), c_list(x["pw"]), x["fine"], x["sync"], c_list(x["pm"]), x["kbd"],
            c_list(x["lfo"][:2]), c_list(x["lfo"][2:]), x["glide"], x["unison"], x["lfoamp"], x["vel"], x["detune"],
            x["wheel"]))
    out += ["};", '_Static_assert(NELEM(P600_EXT) == P600_NFIX, "p600_bank.h: one EXT per fixed program");', ""]
    # the conversions of an imported program (eng_p600.c p600_sysex), as tables: the firmware has no floats
    tab = lambda name, ctype, vals: ["static const %s %s[%d] = {" % (ctype, name, len(vals))] + [
        "    " + ", ".join(str(v) for v in vals[i:i + 16]) + "," for i in range(0, len(vals), 16)] + ["};"]
    out += ["/* SysEx import: an envelope time's CEM3310 voltage (GliGli's 16 bits >> 8) -> F_TIME; the Z80's 4-bit times",
            " * and LFO rates; a cutoff (the Z80's 7 bits, GliGli's 16 >> 8) -> CUT; GliGli's LFO rate (>> 8) -> P_LRATE */"]
    out += tab("P6_ENV_CV", "uint8_t", [env_cv(k << 8) for k in range(256)])
    out += tab("P6_Z80_ENV", "uint8_t", [env_time(v) for v in range(16)])
    out += tab("P6_Z80_LFO", "uint8_t", [lfo_rate(v) for v in range(16)])
    out += tab("P6_CUT8", "uint8_t", [cutoff(c) for c in range(256)])
    out += tab("P6_GLFO", "uint8_t", [lfo_gligli((k << 8) | 0x80) for k in range(256)])
    out.append("")
    open(dst, "w").write("\n".join(out))
    print(len(bank), "programmes ->", dst)


if __name__ == "__main__":
    main(*sys.argv[1:5])
