# Catégories des 255 sons P600 (filtre PRESETS > LIST). B BASS, L LEAD, P PAD, U PLUCK, K KEYS, D DRUM, F FX, O OTHER.
# 1-100 : d'après le nom et les notes du manuel d'origine ; 101-200 : rubriques de la « Patch Collection 2022 » ;
# 201-255 : familles du guide (banques/guru/guru_extras.json). Sortie : la chaîne de 255 lettres pour category.c.
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
F100 = {  # n: lettre
 1:'K',2:'L',3:'P',4:'P',5:'F',6:'L',7:'L',8:'L',9:'P',10:'F',11:'K',12:'L',13:'P',14:'K',15:'K',16:'L',17:'K',18:'L',19:'K',20:'K',
 21:'K',22:'L',23:'P',24:'K',25:'U',26:'U',27:'L',28:'B',29:'P',30:'F',31:'K',32:'L',33:'P',34:'L',35:'K',36:'U',37:'L',38:'B',39:'F',40:'L',
 41:'K',42:'L',43:'P',44:'L',45:'K',46:'L',47:'P',48:'L',49:'U',50:'F',51:'K',52:'L',53:'P',54:'P',55:'U',56:'U',57:'K',58:'B',59:'U',60:'F',
 61:'K',62:'L',63:'B',64:'F',65:'F',66:'F',67:'L',68:'B',69:'K',70:'U',71:'K',72:'L',73:'L',74:'K',75:'U',76:'P',77:'L',78:'L',79:'U',80:'F',
 81:'K',82:'K',83:'P',84:'F',85:'U',86:'L',87:'P',88:'L',89:'D',90:'F',91:'K',92:'B',93:'U',94:'K',95:'P',96:'F',97:'L',98:'L',99:'F',100:'F'}
# 101-200 : rubriques de la collection 2022 (10 sons chacune), avec quelques sons classés à part
GROUPS = ['K', 'P', 'L', 'L', 'B', None, 'F', 'U', 'U', 'P']   # piano, pad 1, lead, brass, bass, natural, effect, stab, bell, pad 2
NATURAL = {151:'L',152:'K',153:'L',154:'K',155:'L',156:'D',157:'K',158:'K',159:'L',160:'L'}   # oboe, orgue, trompette, épinette, ...
SPECIAL = {127:'P',   # PW Pad (rubrique lead) : une nappe
           163:'P',   # Vox Humana : nappe de voix
           170:'D'}   # Simmons Toms
FAM = {'Bass':'B','Chord':'U','FX':'F','Keys':'K','Lead':'L','Pad':'P','Percussion':'D','Pluck':'U','Polysynth':'P','Bells':'U'}
SEQ = {229:'B', 230:'U', 239:'F', 247:'U', 253:'U'}   # « Sequence » : ACID SEQ 1 basse, PHASE 3 / ARP PULSE / DIGI RAIN pincés, S&H BLEEPS bruitage
gx = json.load(open(os.path.join(H, '..', 'banques', 'guru', 'guru_extras.json')))
cat = {}
for n in range(1, 101): cat[n] = F100[n]
for n in range(101, 201):
    g = GROUPS[(n - 101) // 10]
    cat[n] = SPECIAL.get(n) or (NATURAL[n] if g is None else g)
for i, x in enumerate(gx):
    n = 201 + i
    cat[n] = SEQ.get(n) or FAM[x['fam'][0]]
assert len(cat) == 255 and all(c in 'BLPUKDFO' for c in cat.values())
s = ''.join(cat[n] for n in range(1, 256))
print(s)
