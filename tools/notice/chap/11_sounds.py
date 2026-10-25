# 11 · The sounds: finding a sound
CH("sounds", "The sounds: finding a sound", "Les sons : trouver un son",
 P2("Turn <b>PRESETS</b> on HOME or on any sound page to load the next sound on the selected track. The list holds every engine's sounds, P600 first.",
    "Tournez <b>PRESETS</b> sur HOME ou sur n'importe quelle page de son pour charger le son suivant sur la piste choisie. La liste contient les sons de tous les moteurs, P600 en premier.") +
 P2("In all: 326 sounds supplied, 32 USER slots to fill with your sounds, from any engine, and 55 places for your P600 sounds (chapter {ch:keep}).",
    "En tout : 326 sons fournis, 32 emplacements USER à remplir avec vos sons, de n'importe quel moteur, et 55 places pour vos sons P600 (chapitre {ch:keep}).") +
 table([("Numbers", "Numéros"), ("What", "Quoi")], [
   ["1–100", ("The Prophet-600 factory sounds, the 100 programs Sequential Circuits shipped with it in 1982, with their original names.", "Les sons d'usine du Prophet-600, les 100 programmes installés par Sequential Circuits en 1982, sous leurs noms d'origine.")],
   ["101–200", ("The free v2022 collection: 100 sounds made by Prophet-600 owners for the GliGli firmware and shared under the GPL license.", "La collection libre v2022 : 100 sons créés par des propriétaires de Prophet-600 pour le firmware GliGli et partagés sous licence GPL.")],
   ["201–255", ("The Guru-600's own sounds: 30 adapted from the free synthesizer Surge XT (sounds by Claes Johanson, GPL-3) and 25 originals: bells, gong, sync scream, filter percussion, sound effects, random sequences, slow pads.", "Les sons propres au Guru-600 : 30 adaptés du synthétiseur libre Surge XT (sons de Claes Johanson, GPL-3) et 25 originaux : cloches, gong, cri de synchro, percussions au filtre, bruitages, séquences aléatoires, nappes lentes.")],
   [("then", "puis"), ("The other engines' sounds: ANALOG, FM6, PHASE, LOFI, SAMPLE, VOICE, TRIO, WHEEL, GRAIN, PHYS, NOISE, SLICE, DRUM (chapter {ch:engines}): 71 sounds.", "Les sons des autres moteurs : ANALOG, FM6, PHASE, LOFI, SAMPLE, VOICE, TRIO, WHEEL, GRAIN, PHYS, NOISE, SLICE, DRUM (chapitre {ch:engines}) : 71 sons.")],
   [("last", "enfin"), ("Your USER sounds, the ones you saved (chapter {ch:keep}).", "Vos sons USER, ceux que vous avez rangés (chapitre {ch:keep}).")]]) +
 LI([("The list wraps around: after the last sound comes sound 1, and before sound 1 the last one.",
      "La liste boucle : après le dernier son vient le son 1, et avant le son 1, le dernier."),
     ("Long names are shortened on the screen; the full names are in the appendix.",
      "Les noms longs sont abrégés à l'écran ; les noms complets sont en annexe."),
     ("Loading a sound never touches the track's sequence, even while it plays.",
      "Charger un son ne touche jamais la séquence de la piste, même pendant qu'elle joue."),
     ("Went too far? <b>Hold SAVE</b> for 1 s: your previous sound comes back, with its changes. Only the last load comes back: a quick run of turns counts as one.",
      "Vous avez tourné trop loin ? <b>Maintenez SAVE</b> 1 s : le son que vous aviez revient, avec ses changements. Seul le dernier chargement revient : une série rapide de crans compte pour un seul.")]) +
 H3("SAVE › PRESETS: browse, favorites, families", "SAVE › PRESETS : parcourir, favoris, familles") +
 '<div class="split">' + shot("shots/pg_save3.png", "SAVE › PRESETS, page 3 of 6.", "SAVE › PRESETS, page 3 sur 6.", 240) + '<div>' +
 P2("Press <b>SAVE</b> repeatedly until <b>PRESETS</b> appears (page 3 on a P600 track, page 2 on other tracks).",
    "Appuyez sur <b>SAVE</b> jusqu'à <b>PRESETS</b> (page 3 sur une piste P600, page 2 sur les autres).") +
 knobs([("KNOB 1", "No.: the sound, and its number in the list (1/326…). Same as PRESETS.", "No. : le son, et son numéro dans la liste (1/326…). Même rôle que PRESETS.", "list", "liste"),
        ("KNOB 2", "ENG: jump to the next or previous engine's first sound.", "ENG : saute au premier son du moteur suivant ou précédent.", "14 engines", "14 moteurs"),
        ("KNOB 3", "FAV: turn right to mark the sound as a favorite, left to unmark it.", "FAV : à droite, marque le son comme favori ; à gauche, le retire.", "OFF / ON", "OFF / ON"),
        ("KNOB 4", "LIST: which sounds PRESETS steps through: ALL, FAV (your favorites), or one family: BASS, LEAD, PAD, PLUCK (plucked sounds and bells), KEYS, DRUM, FX, OTHER.", "LIST : les sons que parcourt PRESETS : ALL (tous), FAV (vos favoris), ou une famille : BASS, LEAD, PAD, PLUCK (sons pincés et cloches), KEYS, DRUM, FX, OTHER.", "10 lists", "10 listes")]) +
 '</div></div>' +
 BOX("key", ("<b>LIST applies everywhere.</b> When it is not ALL, PRESETS on HOME and on every page steps only through that family or your favorites. If PRESETS seems to skip sounds, come back here and set LIST to ALL. NO FAVORITES or NO SOUNDS IN LIST means the chosen list is empty.",
             "<b>LIST reste en vigueur partout.</b> Quand elle n'est pas sur ALL, PRESETS sur HOME et sur toutes les pages ne parcourt que cette famille ou vos favoris. Si PRESETS semble sauter des sons, revenez ici et remettez LIST sur ALL. NO FAVORITES ou NO SOUNDS IN LIST signifie que la liste choisie est vide.")) +
 P2("Every P600 sound belongs to one family. A USER sound takes the family you give it when you name it (chapter {ch:keep}).",
    "Chaque son P600 appartient à une famille. Un son USER prend la famille que vous lui donnez en le nommant (chapitre {ch:keep}).") +
 H3("The Prophet-600 sounds and the mod wheel", "Les sons du Prophet-600 et la molette") +
 P2("For sounds 1 to 100, the appendix gives the Prophet-600 manual's notes: what the mod wheel adds and how to play each sound. The FM-1 has no wheel: use a MIDI keyboard's, or set MENU › CONTROL › SELECT = MODW (chapter {ch:midi}).",
    "Pour les sons 1 à 100, l'annexe reprend les notes du manuel du Prophet-600 : ce qu'ajoute la molette de modulation et comment jouer chaque son. Le FM-1 n'a pas de molette : utilisez celle d'un clavier MIDI, ou réglez MENU › CONTROL › SELECT = MODW (chapitre {ch:midi}).") +
 BOX("note", ("The complete list of the 255 P600 sounds, with their families, authors and notes, is in the <b>appendix</b>, at the end of this guide.",
              "La liste complète des 255 sons P600, avec leurs familles, leurs auteurs et leurs notes, est en <b>annexe</b>, à la fin de cette notice.")))
