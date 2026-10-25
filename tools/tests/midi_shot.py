import subprocess, sys, time, mido, os
EMU = os.path.expanduser("~/Documents/FM-1/fm1-emu/fm1-emu-0.2.0-macos-arm64/fm1-live")
FW = os.path.expanduser("~/Documents/FM-1/Firmwares/guru-600.fwsc")
out = mido.open_output("Guru Test", virtual=True)
time.sleep(0.5)
emu = subprocess.Popen([EMU, "--fwsc", FW, "--midi", "Guru Test", "--shot", "13000"], stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, cwd=os.path.dirname(EMU))
time.sleep(10)
out.send(mido.Message("program_change", program=int(sys.argv[1]), channel=0))
time.sleep(0.3)
for n in (48, 52, 55, 60, 64, 67):
    out.send(mido.Message("note_on", note=n, velocity=100, channel=0))
log, _ = emu.communicate(timeout=60)
print(log[-600:])
