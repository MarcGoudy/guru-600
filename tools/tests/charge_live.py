"""En temps réel, fenêtre ouverte : le firmware de test (page INFO), un son choisi en Program Change, 6 notes tenues,
une capture d'écran pendant l'accord.   venv/bin/python p600/tests/charge_live.py PROG NOM [SECONDES]"""
import subprocess, sys, time, mido, os
D = os.path.expanduser("~/Documents/FM-1/fm1-emu/fm1-emu-0.2.0-macos-arm64")
FW = os.path.expanduser("~/Documents/FM-1/Firmwares/test-cpu.fwsc")
prog, name = int(sys.argv[1]), sys.argv[2]
hold = float(sys.argv[3]) if len(sys.argv) > 3 else 4
out = mido.open_output("Guru Test", virtual=True)
time.sleep(0.5)
emu = subprocess.Popen([D + "/fm1-live", "--fwsc", FW, "--midi", "Guru Test"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, cwd=D)
time.sleep(9)
out.send(mido.Message("program_change", program=prog, channel=0))
time.sleep(0.5)
for n in (55, 59, 62, 65, 69, 72):
    out.send(mido.Message("note_on", note=n, velocity=100, channel=0))
time.sleep(hold)
subprocess.run(["screencapture", "-x", os.path.expanduser("~/Documents/FM-1/fm1-emu/anim/live_%s.png" % name)])
for n in (55, 59, 62, 65, 69, 72):
    out.send(mido.Message("note_off", note=n, channel=0))
time.sleep(0.5)
emu.terminate()
