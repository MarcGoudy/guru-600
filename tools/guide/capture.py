"""Captures du guide : l'éditeur (p600/editeur) hors connexion, ses valeurs de démonstration, à 1536 x 1024 (la taille de
sa maquette : une page = un pixel par point), dans Chrome sans fenêtre et un profil neuf à chaque prise (sans lui, une
page restée en mémoire d'une prise précédente peut s'afficher). Usage : capture.py [nom ...] (sans nom : toutes).
Une prise : nom, onglet, recadrage (x0, y0, x1, y1 en points de la page ; None : toute la page)."""
import os, subprocess, sys, tempfile, shutil
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
ED = os.path.join(os.path.dirname(H), "editeur", "index.html")
C = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SHOTS = [("cover", "sound", None), ("sound", "sound", None), ("header", "sound", (0, 0, 1536, 150)),
         ("keyboard", "sound", (0, 776, 1536, 1024)), ("morph", "sound", (0, 650, 1320, 780)),
         ("sounds", "sound&listat=254", (1316, 150, 1536, 780)), ("seq", "seq", None), ("song", "song", None), ("arp", "arp", None),
         ("fx", "fx", None), ("mod", "mod", None), ("tracks", "tracks", None), ("projects", "projects", None),
         ("samples", "samples", None), ("backup", "backup", None), ("settings", "settings", None)]
want = set(a for a in sys.argv[1:] if len(a) > 2)
LANGS = [a for a in sys.argv[1:] if len(a) == 2] or ["en", "fr", "de", "es", "it", "zh", "ja"]   # (shots/xx/: one series per language)
for name, tab, crop in SHOTS:
  for lg in LANGS:
    if want and name not in want:
        continue
    prof = tempfile.mkdtemp()
    os.makedirs(os.path.join(H, "shots", lg), exist_ok=True)
    out = os.path.join(H, "shots", lg, name + ".png")
    subprocess.run([C, "--headless=new", f"--user-data-dir={prof}", "--window-size=1536,1024", "--hide-scrollbars",
                    "--virtual-time-budget=6000", f"--screenshot={out}", f"file://{ED}?tab={tab}&lang={lg}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    shutil.rmtree(prof, ignore_errors=True)
    im = Image.open(out)
    if crop:
        im = im.crop(crop)
    im.convert("RGB").save(out[:-4] + ".jpg", quality=88, optimize=True)   # (JPEG: the PDF stays light)
    os.remove(out)
    print(lg, name, im.size)
