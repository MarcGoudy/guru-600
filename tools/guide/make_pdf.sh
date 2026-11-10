#!/bin/zsh
# PDF du guide de l'éditeur : la couverture commune, puis les sept langues
cd "${0:A:h}"
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
T=$(mktemp -d)
~/Documents/FM-1/venv/bin/python make_guide.py || exit 1
for l in en fr de es it zh ja; do
  "$C" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=$T/$l.pdf "file://$PWD/index.html?lang=$l&part=lang" 2>/dev/null
done
"$C" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=$T/cover.pdf "file://$PWD/index.html?lang=en&part=cover" 2>/dev/null
OUT="${G6_OUT:-$HOME/Documents/FM-1/Partage/Guru-600 Editor - Guide.pdf}"   # (G6_OUT: a draft elsewhere)
~/Documents/FM-1/venv/bin/python - "$T" "$OUT" <<'PY'
import sys, os, pypdf
from pypdf.generic import NameObject, ArrayObject, DictionaryObject, NumberObject, NullObject
t, out = sys.argv[1], sys.argv[2]
w = pypdf.PdfWriter()
start = {}
for n in ("cover", "en", "fr", "de", "es", "it", "zh", "ja"):
    r = pypdf.PdfReader(f"{t}/{n}.pdf"); start[n] = len(w.pages); print(n, len(r.pages))
    w.append(r)
for pg in w.pages:                       # the links to https://guru-600.lang/xx (the cover's, the contents' appendix):
  for a in pg.get("/Annots", []):        # to that part's first page
    a = a.get_object()
    uri = a.get("/A", {}).get("/URI", "")
    if "guru-600.lang/" in uri:
        n = uri.rsplit("/", 1)[1]
        a[NameObject("/A")] = DictionaryObject({NameObject("/S"): NameObject("/GoTo"),
              NameObject("/D"): ArrayObject([w.pages[start[n]].indirect_reference, NameObject("/Fit")])})
for n, title in (("en", "English"), ("fr", "Français"), ("de", "Deutsch"), ("es", "Español"), ("it", "Italiano"), ("zh", "中文"), ("ja", "日本語")):
    w.add_outline_item(title, start[n])
import json, re                          # the contents' pages: where each chapter starts, in each language, from
parts = ["cover", "en", "fr", "de", "es", "it", "zh", "ja", "end"]   # the part's own named destinations (#s1 .. #sN,
pages = {}                                                 # Chrome's): any script, no text search. The next pass prints
NCH = json.load(open("chapters.json"))["n"]
for l in ("en", "fr", "de", "es", "it", "zh", "ja"):     # them (make_notice.py toc_pg)
    r = pypdf.PdfReader(f"{t}/{l}.pdf")
    nd = r.named_destinations
    idx = {pg.indirect_reference.idnum: i for i, pg in enumerate(r.pages)}
    found = []
    for k in range(1, NCH + 1):
        d = nd.get("/s%d" % k) or nd.get("s%d" % k)
        pi = idx.get(d.page.idnum) if d is not None and hasattr(d.page, "idnum") else (d.page if d is not None and isinstance(d.page, int) else None)
        found.append(start[l] + pi + 1 if pi is not None else "")
    pages[l] = found
old = json.load(open("toc_pages.json")) if os.path.exists("toc_pages.json") else {}
json.dump(pages, open("toc_pages.json", "w"))
print("sommaire", "stable" if old == pages else "mis à jour", pages["en"])
for l in ("en", "fr", "de", "es", "it", "zh", "ja"):    # every link to a chapter (#s1 .. #sN: the same names in
    for i in range(start[l], (start[parts[parts.index(l) + 1]] if parts[parts.index(l) + 1] in start else len(w.pages))):   # each language): to that language's own page
        for an in w.pages[i].get("/Annots", []):
            an = an.get_object()
            d = an.get("/Dest")
            m = re.fullmatch(r"/?s(\d+)", str(d)) if d is not None else None
            if m and int(m.group(1)) <= len(pages[l]) and pages[l][int(m.group(1)) - 1]:
                an[NameObject("/Dest")] = ArrayObject([w.pages[pages[l][int(m.group(1)) - 1] - 1].indirect_reference,
                                                       NameObject("/Fit")])
n = len(w.pages)                         # the folios: a number at the foot of every page but the cover, printed by
import subprocess                         # Chrome on blank A4 pages and laid over them
html = ['<!doctype html><meta charset="utf-8"><style>@page{size:A4;margin:0}body{margin:0}'
        '.p{height:297mm;position:relative;break-after:page}'
        '.n{position:absolute;bottom:7mm;width:100%;text-align:center;font:9pt "Inter Tight",Helvetica,sans-serif;color:#8a8478}'
        '</style>']
html += ['<div class="p"><div class="n">%s</div></div>' % (i + 1 if i else "") for i in range(n)]
open(f"{t}/num.html", "w").write("".join(html))
subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu",
                "--no-pdf-header-footer", f"--print-to-pdf={t}/num.pdf", f"file://{t}/num.html"],
               stderr=subprocess.DEVNULL, check=True)
num = pypdf.PdfReader(f"{t}/num.pdf")
assert len(num.pages) == n, (len(num.pages), n)
for i in range(1, n):
    w.pages[i].merge_page(num.pages[i])
w.write(out); print("total", n)
PY
[ -z "$G6_PASS2" ] && G6_PASS2=1 exec zsh "$0"    # (a second pass: the contents with the pages just found)
[ -z "$G6_OUT" ] && cp "$OUT" ~/Desktop/
