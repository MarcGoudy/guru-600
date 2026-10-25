"""Traductions de la notice : exporte les textes encore à traduire, langue par langue, en lots (tr_todo/xx_NN.json :
[{"en": …, "fr": …}]), puis (tr_export.py merge) range les lots traduits (tr_todo/xx_NN.out.json : {en: traduction})
dans tr_xx.json. Les textes d'abord produits par make_notice.py (strings.json)."""
import json, os, sys, glob
H = os.path.dirname(os.path.abspath(__file__))
LANGS = ("de", "es", "it", "zh", "ja")
D = os.path.join(H, "tr_todo")


def export(size=120):
    os.makedirs(D, exist_ok=True)
    for f in glob.glob(os.path.join(D, "*.json")):
        os.remove(f)
    strings = json.load(open(os.path.join(H, "strings.json")))
    for l in LANGS:
        tr = json.load(open(os.path.join(H, f"tr_{l}.json")))
        todo = [s for s in strings if s["en"] not in tr]
        for k in range(0, len(todo), size):
            json.dump(todo[k:k + size], open(os.path.join(D, f"{l}_{k // size:02d}.json"), "w"), ensure_ascii=False, indent=1)
        print(l, len(todo), "à traduire")


def merge():
    strings = {s["en"] for s in json.load(open(os.path.join(H, "strings.json")))}
    for l in LANGS:
        p = os.path.join(H, f"tr_{l}.json")
        tr = json.load(open(p))
        n = 0
        for f in sorted(glob.glob(os.path.join(D, f"{l}_*.out.json"))):
            for en, t in json.load(open(f)).items():
                if en in strings and isinstance(t, str) and t.strip():
                    tr[en] = t
                    n += 1
        json.dump(tr, open(p, "w"), ensure_ascii=False, indent=1)
        print(l, n, "rangés,", sum(1 for s in strings if s not in tr), "manquants")


if __name__ == "__main__":
    merge() if sys.argv[1:] == ["merge"] else export()
