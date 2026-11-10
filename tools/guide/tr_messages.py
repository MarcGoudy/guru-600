"""Les messages de l'éditeur cités dans les traductions du guide (titres des questions, citations en gras) : l'éditeur
les affiche dans la langue du lecteur (guru-tx.js) ; là où une traduction cite le message anglais, il est remplacé par
le sien. Usage : tr_messages.py tx.json (TX de l'éditeur, en JSON : chaque langue, chaque clé)."""
import json, re, sys, os
H = os.path.dirname(os.path.abspath(__file__))
TX = json.load(open(sys.argv[1]))
for l in ("de", "es", "it", "zh", "ja"):
    p = os.path.join(H, f"tr_{l}.json"); tr = json.load(open(p)); n = 0
    for k, en in TX["en"].items():
        mine = TX[l][k]
        en = en.replace("<br>", " ")
        parts = en.split("%s")
        # (%s: a letter or a number, A, 12; a detail after ": " at the end: the rest of the quote)
        pat = "".join(re.escape(x) + ("" if i == len(parts) - 1 else "([^<\"”»]+)" if i == len(parts) - 2 and not parts[-1] and x.endswith(": ") else "([A-Za-z0-9]+)")
                      for i, x in enumerate(parts))
        rx = re.compile(pat)
        rx_short = None
        if en.endswith(": %s"):                     # (quoted without its detail: "This file could not be read.")
            rx_short = re.compile(re.escape(en[:-4] + "."))
        for key, t in tr.items():
            def sub(m):
                out = mine.replace("<br>", " ")
                for g in m.groups():
                    out = out.replace("%s", g, 1)
                return out
            t2 = rx.sub(sub, t)
            if rx_short:
                t2 = rx_short.sub(mine.replace(": %s", "").replace("：%s", "").rstrip(" :") + ("" if l in ("zh", "ja") else "."), t2)
            if t2 != t:
                tr[key] = t2; n += 1
    json.dump(tr, open(p, "w"), ensure_ascii=False, indent=1)
    print(l, n, "citations")
