"""Les traductions de l'éditeur qui débordent de leur bouton ou de leur cadre : chaque page dans chaque langue, ouverte
avec ?checkfit (guru-i18n.js marque data-over), dans Chrome sans fenêtre. Usage : check_fit.py [langues...]"""
import os, re, subprocess, sys, tempfile, shutil, html
ED = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "editeur", "index.html")
C = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAGES = ["sound", "seq", "song", "arp", "fx", "mod", "tracks", "projects", "samples", "backup", "settings"]
LANGS = sys.argv[1:] or ["fr", "de", "es", "it", "zh", "ja"]
for lg in LANGS:
    found = set()
    for pg in PAGES:
        prof = tempfile.mkdtemp()
        dom = subprocess.run([C, "--headless=new", f"--user-data-dir={prof}", "--window-size=1536,1024", "--virtual-time-budget=8000",
                              "--dump-dom", f"file://{ED}?tab={pg}&lang={lg}&checkfit"], capture_output=True, text=True).stdout
        shutil.rmtree(prof, ignore_errors=True)
        for m in re.finditer(r'<(\w+) class="([^"]*)"[^>]*data-over="1"[^>]*>(.*?)</\1>', dom, re.S):
            t = html.unescape(re.sub(r"<[^>]+>", " ", m.group(3))).strip()
            if t: found.add((pg, m.group(2).split()[0], re.sub(r"\s+", " ", t)[:60]))
    print(lg, len(found))
    for f in sorted(found): print("  ", *f, sep=" | ")
