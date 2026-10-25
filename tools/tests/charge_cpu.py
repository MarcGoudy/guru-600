"""Charge processeur du P600 dans fm1-emu (firmware de test test-cpu.fwsc : la page INFO ouverte après le démarrage).
Un clavier MIDI virtuel choisit un son (Program Change) et tient 6 notes ; une capture de l'écran à 15 s.
    venv/bin/python p600/tests/charge_cpu.py PROGRAMME NOM   (PROGRAMME -1 : aucune note)"""
import subprocess, sys, time, mido, os
from PIL import Image
D = os.path.expanduser("~/Documents/FM-1/fm1-emu/fm1-emu-0.2.0-macos-arm64")
FW = os.path.expanduser("~/Documents/FM-1/Firmwares/test-cpu.fwsc")
prog, name = int(sys.argv[1]), sys.argv[2]
out = mido.open_output("Guru Test", virtual=True)
time.sleep(0.5)
t0 = time.time()
emu = subprocess.Popen([D + "/fm1-live", "--fwsc", FW, "--midi", "Guru Test", "--shot", "15000"], stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, cwd=D)
time.sleep(4.8)
if prog >= 0:
    out.send(mido.Message("program_change", program=prog, channel=0))
    time.sleep(0.4)
    for n in (48, 52, 55, 60, 64, 67):
        out.send(mido.Message("note_on", note=n, velocity=100, channel=0))
log, _ = emu.communicate(timeout=60)
print(name, "|", [l for l in log.splitlines() if "panel.ppm" in l][0][-60:], "| %.1f s" % (time.time() - t0))
Image.open(D + "/work/panel.ppm").crop((370, 40, 850, 520)).save(os.path.expanduser("~/Documents/FM-1/fm1-emu/anim/cpu_%s.png" % name))
