"""La page d'installation du Guru-600 (d'après Felucca/web/make_site.py) et la page d'envoi des sons, en cinq langues.
    venv/bin/python p600/site/make_site_guru.py ../Felucca/build/felucca.fwsc ../Partage/site-installation
Les textes : strings_en.json (anglais) et strings_tr.json (fr, de, es, it)."""
import json, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "Felucca" / "web"))
import make_site                                             # noqa: E402

LANGS = ["en", "fr", "de", "es", "it"]
NAMES = {"en": "EN", "fr": "FR", "de": "DE", "es": "ES", "it": "IT"}
VERSION = "1.0"


def texts(group):
    en = json.load(open(HERE / "strings_en.json"))[group]
    tr = json.load(open(HERE / "strings_tr.json"))
    out = {"en": en}
    for l in LANGS[1:]:
        out[l] = {k: tr[l][group].get(k, v) for k, v in en.items()}
    return out


LANG_JS = ('<nav class="langs">' + "".join(f'<button data-l="{l}">{NAMES[l]}</button>' for l in LANGS) + '</nav>')
LANG_CSS = (".langs{float:right;display:flex;gap:4px}.langs button{font:600 12px sans-serif;padding:3px 7px;"
            "border:1px solid currentColor;background:none;color:inherit;opacity:.5;cursor:pointer}"
            ".langs button.on{opacity:1}"
            "@font-face{font-family:'Mong Rong';src:url(MonRong.ttf)}"
            ".logo{font-family:'Mong Rong',serif;font-weight:normal;font-size:56px;line-height:1;margin:0 0 4px}"
            ".trib{font:800 12px sans-serif;letter-spacing:.12em;color:#d65440;margin:0 0 24px}")
PICK = ('let lang=(function(){try{const s=localStorage.getItem("g6lang");if(s)return s}catch(e){}'
        'const n=(navigator.language||"en").slice(0,2);return ' + json.dumps(LANGS) + '.includes(n)?n:"en"})();')


def installer(out):
    inst = out / "webapp" / "installer" / "index.html"
    h = inst.read_text(encoding="utf-8")
    T = texts("installer")
    h = h.replace('<html lang="ja">', '<html lang="en">', 1).replace("<title>Felucca</title>", "<title>Guru-600</title>", 1)
    h = h.replace("</style>", LANG_CSS + "</style>", 1)
    h = h.replace('  <button class="lang" id="lang"></button>\n  <h1>Felucca</h1>',
                  '  ' + LANG_JS + '\n  <h1 class="logo">guru-600</h1>\n  <p class="trib">A PROPHET-600 TRIBUTE</p>\n'
                  '  <p><b data-t="title"></b></p>', 1)
    h = h.replace('  <p><a href="../editor/" style="color:inherit" data-t="editor"></a></p>',
                  '  <p><a href="../../envoi-sons.html" style="color:inherit" data-t="send"></a></p>\n'
                  '  <p class="small"><a href="../editor/" style="color:inherit" data-t="editor"></a></p>\n'
                  '  <p class="small" style="border:1px solid currentColor;border-radius:8px;padding:8px 12px">'
                  '<span data-t="feedback"></span> <a href="https://github.com/MarcGoudy/guru-600" style="color:inherit">'
                  'github.com/MarcGoudy/guru-600</a></p>', 1)   # (a bug, an idea: the project's GitHub)
    h = h.replace('  <p class="small">Felucca by Leo Kuroshita', '  <p class="small"><span data-t="credit"></span><br>Felucca by Leo Kuroshita', 1)
    i, j = h.index("const TEXT = {"), h.index("\n};", h.index("const TEXT = {")) + 3
    h = h[:i] + "const TEXT = " + json.dumps(T, ensure_ascii=False, indent=1) + ";" + h[j:]
    a = 'let lang = (navigator.language || "en").toLowerCase().startsWith("ja") ? "ja" : "en";'
    assert a in h
    h = h.replace(a, PICK, 1)
    h = h.replace('  $("lang").textContent = t("other");',
                  '  document.querySelectorAll(".langs button").forEach((b) => b.classList.toggle("on", b.dataset.l === lang));', 1)
    h = h.replace('$("lang").addEventListener("click", () => { lang = lang === "ja" ? "en" : "ja"; applyLang(); });',
                  'document.querySelectorAll(".langs button").forEach((b) => b.addEventListener("click", () => { lang = b.dataset.l; '
                  'try { localStorage.setItem("g6lang", lang); } catch (e) {} applyLang(); }));', 1)
    h = h.replace("say(`Felucca ${meta.version}`);", "say(`Guru-600 ${meta.version}`);", 1)
    h = h.replace('<details style="margin-top:24px">', '<details style="display:none">', 1)   # (Guru-600: no return to V15 here: M-VAVE's own updater, the guide)
    h = h.replace("`Felucca-backup-", "`Guru-600-backup-", 1)
    assert "Felucca 1.0" not in h and '"ja"' not in h, "installer: some text left untouched"
    inst.write_text(h, encoding="utf-8")
    shutil.copy(HERE / "MonRong.ttf", inst.parent / "MonRong.ttf")
    shutil.copy(HERE / "MonRong-licence.txt", inst.parent / "MonRong-licence.txt")


def sender(out):
    h = (HERE / "envoi-sons.src.html").read_text(encoding="utf-8").replace("Guru 600", "Guru-600")
    T = texts("sender")
    i, j = h.index("const T = {"), h.index("\n};", h.index("const T = {")) + 3
    h = h[:i] + "const T = " + json.dumps(T, ensure_ascii=False, indent=1) + ";" + h[j:]
    h = h.replace('<div class="lang"><button id="lang">Français</button></div>', LANG_JS, 1)
    h = h.replace("<h1>GURU<span>~</span>600</h1>", '<h1 class="logo">guru-600</h1>', 1)
    h = h.replace("</style>", LANG_CSS.replace("url(MonRong.ttf)", "url(webapp/installer/MonRong.ttf)") + "</style>", 1)
    a = 'let lang = (navigator.language || "en").startsWith("fr") ? "fr" : "en", out = null, sounds = [];'
    assert a in h
    h = h.replace(a, PICK + " let out = null, sounds = [];", 1)
    h = h.replace('  $("lang").textContent = lang === "fr" ? "English" : "Français";',
                  '  document.querySelectorAll(".langs button").forEach((b) => b.classList.toggle("on", b.dataset.l === lang));', 1)
    h = h.replace('$("lang").onclick = () => { lang = lang === "fr" ? "en" : "fr"; try { localStorage.setItem("g6lang", lang); } catch (e) {} tr(); };',
                  'document.querySelectorAll(".langs button").forEach((b) => { b.onclick = () => { lang = b.dataset.l; '
                  'try { localStorage.setItem("g6lang", lang); } catch (e) {} tr(); }; });', 1)
    h = h.replace('try { const l = localStorage.getItem("g6lang"); if (l) lang = l; } catch (e) {}\n', "", 1)
    assert '$("lang")' not in h, "sender: the old language button is still used"
    (out / "envoi-sons.html").write_text(h, encoding="utf-8")


def main(pkg, out):
    out = Path(out)
    make_site.main(pkg, VERSION, str(out))
    fw = out / "firmware"
    for f in fw.glob("*.fwsc"):
        if f.name != f"felucca-{VERSION}.fwsc":
            f.unlink()
    (fw / f"felucca-{VERSION}.fwsc").rename(fw / f"guru-600-{VERSION}.fwsc")
    inst = out / "webapp" / "installer" / "index.html"
    h = inst.read_text(encoding="utf-8").replace(f"firmware/felucca-{VERSION}.fwsc", f"firmware/guru-600-{VERSION}.fwsc")
    inst.write_text(h, encoding="utf-8")
    installer(out)
    sender(out)
    (out / "index.html").write_text('<!doctype html><meta charset="utf-8"><title>Guru-600</title>'
                                    '<meta http-equiv="refresh" content="0; url=webapp/installer/">'
                                    '<a href="webapp/installer/">Guru-600 installer</a>\n', encoding="utf-8")
    print("site Guru-600:", out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
