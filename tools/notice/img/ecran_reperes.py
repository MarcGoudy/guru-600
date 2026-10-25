from PIL import Image, ImageDraw, ImageFont
src=Image.open("shots/scr_parts.png").convert("RGB")
S=2; P=44
im=Image.new("RGB",(480*S+2*P,480*S+2*P),src.getpixel((1,1)))
im.paste(src.resize((480*S,480*S),Image.LANCZOS),(P,P))
d=ImageDraw.Draw(im)
f=ImageFont.truetype("fonts/InterTight.ttf",26); 
try: f.set_variation_by_axes([800])
except Exception: pass
B=[(1,24,-6),(2,56,-6),(3,84,-6),(4,250,-6),(5,372,-6),(6,452,-6),(7,121,58),(8,240,168),(9,240,410),(10,150,486),(11,428,486)]
for n,x,y in B:
    cx,cy=P+x*S,P+y*S; r=19
    d.ellipse((cx-r-2,cy-r-2,cx+r+2,cy+r+2),fill=(255,255,255)); d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(255,80,70))
    d.text((cx,cy+1),str(n),font=f,fill=(255,255,255),anchor="mm")
im.save("img/ecran_reperes.png")
