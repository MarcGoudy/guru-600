"""Captures d'écran de la notice, prises dans l'émulateur (fm1-live --shot) : chaque scène est une suite de gestes
sur le FM-1 émulé, après le démarrage. Usage : capture.py scenes.json [nom ...]  (sans nom : toutes les scènes).

Une scène : {"name": "edit_morph", "keys": ["EDIT", "wait 400", "EDIT", "K1 +3", "hold GLO 1300"], "crop": "screen"}
  - "EDIT", "OCTUP"... : un appui bref (120 ms) ; "hold X 1300" : maintenu 1300 ms, relâché ensuite ;
    "down X" / "up X" : appuyé / relâché (un calque gardé ouvert pendant la capture) ;
  - "K1 +3", "PRESETS -2", "ALGO +1", "SELECT +1" : un bouton rotatif, en crans ;
  - "C4" ou "n12" : une note (120 ms) ; "wait 400" : une pause (ms) ;
  - "crop": "screen" (l'écran seul, 480 x 480) ou "panel" (toute la façade).
Les captures vont dans shots/<name>.png."""
import json, os, subprocess, sys, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor

H = os.path.dirname(os.path.abspath(__file__))
EMU = os.path.expanduser("~/Documents/FM-1/fm1-emu-src/target/release/fm1-live")
FW = os.path.expanduser("~/Documents/FM-1/Felucca/build/felucca.fwsc")
T0 = 9000                                   # (the splash is over)
ENC = {"SELECT": 0, "ALGO": 1, "K1": 2, "K2": 3, "K3": 4, "K4": 5, "PRESETS": 6}


PRELUDE = ["hold FX 600", "hold GLO 600", "hold SCL 600", "hold EDIT 600", "hold SEQ 600", "hold REC 600", "wait 2600"]
# (each layer opened once: no "HOLD [X] QUICK" hint on the pictures; "prelude": false in a scene to keep it)


def keys(scene):                            # the gestures -> FM1_BENCH_KEYS, and the time of the picture
    t, ev = T0, []
    for g in (PRELUDE if scene.get("prelude", True) else []) + scene["keys"]:
        w = g.split()
        if w[0] == "wait":
            t += int(w[1])
        elif w[0] == "hold":
            ev += [f"{t}:{w[1]}", f"{t + int(w[2])}:{w[1]}^"]
            t += int(w[2]) + 250
        elif w[0] == "down":
            ev.append(f"{t}:{w[1]}")
            t += int(w[2]) if len(w) > 2 else 1300
        elif w[0] == "up":
            ev.append(f"{t}:{w[1]}^")
            t += 250
        elif w[0] in ENC:
            n = int(w[1])
            ev.append(f"{t}:e{ENC[w[0]]}:{n}")
            t += 150 + 40 * abs(n)
        else:
            ev += [f"{t}:{w[0]}", f"{t + 120}:{w[0]}^"]
            t += 450
    return ",".join(ev), t + scene.get("settle", 600)


def take(scene):
    k, t = keys(scene)
    d = tempfile.mkdtemp()
    try:
        os.mkdir(os.path.join(d, "work"))
        subprocess.run([EMU, "--fwsc", FW, "--shot", str(t)], cwd=d, env=dict(os.environ, FM1_BENCH_KEYS=k),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
        out = os.path.join(H, "shots", scene["name"] + ".png")
        subprocess.run(["sips", "-s", "format", "png", os.path.join(d, "work", "panel.ppm"), "--out", out],
                       stdout=subprocess.DEVNULL, check=True)
        if scene.get("crop", "screen") == "screen":
            subprocess.run(["sips", "-c", "480", "480", "--cropOffset", "42", "370", out, "--out", out],
                           stdout=subprocess.DEVNULL, check=True)
        return scene["name"], "ok"
    except Exception as x:
        return scene["name"], f"ERREUR {x}"
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    scenes = json.load(open(sys.argv[1]))
    want = set(sys.argv[2:])
    todo = [s for s in scenes if not want or s["name"] in want]
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        for name, r in ex.map(take, todo):
            print(name, r)
