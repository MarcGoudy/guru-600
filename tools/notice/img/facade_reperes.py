# La façade annotée (chapitre des commandes) : la façade de l'émulateur (shots/facade_rep_new.png, scenes_facade.json),
# 20 repères numérotés. Coordonnées dans une façade de 1280 px de large.
from PIL import Image, ImageDraw, ImageFont
src = Image.open("shots/facade_rep_new.png").convert("RGB")
W = 1280; H = round(src.height * W / src.width)
im = src.resize((W, H), Image.LANCZOS)
d = ImageDraw.Draw(im)
f = ImageFont.truetype("fonts/InterTight.ttf", 20)
try: f.set_variation_by_axes([800])
except Exception: pass
k = 1280 / 728
B = [(1, 48, 76), (2, 124, 76), (3, 48, 152), (4, 124, 152), (5, 118, 209), (6, 590, 75),
     (7, 436, 154), (8, 481, 154), (9, 525, 154), (10, 569, 154), (11, 614, 154), (12, 658, 154),
     (13, 436, 198), (14, 481, 198), (15, 525, 198), (16, 569, 198), (17, 614, 198), (18, 658, 198),
     (19, 340, 368), (20, 277, 140)]
for n, x, y in B:
    cx, cy = (x + 13) * k, (y - (25 if 7 <= n <= 18 else 13)) * k if n not in (19, 20) else y * k
    if n in (19, 20): cx = x * k
    r = 15
    d.ellipse((cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2), fill=(255, 255, 255))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 80, 70))
    d.text((cx, cy + 1), str(n), font=f, fill=(255, 255, 255), anchor="mm")
im.save("img/facade_reperes.png")
