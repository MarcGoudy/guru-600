# 10 · MORPH and MUTATE
CH("morph", "MORPH and MUTATE", "MORPH et MUTATE",
 '<div class="split">' + shot("shots/p6_edit8.png", "EDIT › MORPH, page 8 of 11, on a P600 track.", "EDIT › MORPH, page 8 sur 11, sur une piste P600.", 260) + '<div>' +
 P2("<b>MORPH</b> gradually turns one P600 sound into another with a single knob. <b>MUTATE</b> creates a variation of the current sound in one press, close to the original or far from it. Both are on the same page, on P600 tracks only.",
    "<b>MORPH</b> transforme progressivement un son P600 en un autre, avec un seul bouton rotatif. <b>MUTATE</b> crée une variante du son actuel en un appui, proche de l'original ou éloignée. Les deux sont sur la même page, sur les pistes P600 seulement.") +
 STEPS([("Select a P600 track and press <b>EDIT</b> until <b>MORPH 8/11</b> appears.", "Choisissez une piste P600 et appuyez sur <b>EDIT</b> jusqu'à <b>MORPH 8/11</b>.")]) +
 '</div></div>' +
 knobs([("KNOB 1", "SOUND A: the starting sound (the track's sound). Turn it to load the next or previous P600 sound (after 255 comes 1).", "SOUND A : le son de départ (le son de la piste). Tournez-le pour charger le son P600 suivant ou précédent (après 255 vient 1).", "1–255", "1–255"),
        ("KNOB 2", "SOUND B: the sound to reach, any of the 255 places (after 255 comes 1).", "SOUND B : le son à atteindre, n'importe laquelle des 255 places (après 255 vient 1).", "1–255", "1–255"),
        ("KNOB 3", "MORPH: 0 % is A, 100 % is B, everything in between is a mixture.", "MORPH : 0 % correspond à A, 100 % à B ; entre les deux, un mélange.", "0–100 %", "0–100 %"),
        ("KNOB 4", "MUTATE: how far a press of OCT+ moves the sound away (31 % when the page opens).", "MUTATE : jusqu'où un appui sur OCT+ éloigne le son (31 % à l'ouverture de la page).", "1–100 %", "1–100 %")]) +
 H3("Morphing, step by step", "Morpher, pas à pas") +
 STEPS([("Choose A with <b>KNOB 1</b> (or keep the track's sound) and B with <b>KNOB 2</b>. At 0 %, you hear A.",
         "Choisissez A avec <b>KNOB 1</b> (ou gardez le son de la piste) et B avec <b>KNOB 2</b>. À 0 %, vous entendez A."),
        ("Play and turn <b>KNOB 3</b> slowly: the sound moves from A toward B. Continuous settings glide; switches (VOICES, KBD, the LFO's shape…) change one by one, each at its own point between 20 and 80 %, and the waveforms, SYNC and the Poly-Mod destinations crossfade. At 100 % you have B completely, its effect sends included; settings B does not hold (INSERT, MOD slots 1–2, LFO 2, ENV DEST) go back to their defaults.",
         "Jouez et tournez <b>KNOB 3</b> lentement : le son va de A vers B. Les réglages continus glissent ; les commutateurs (VOICES, KBD, la forme du LFO…) changent un par un, chacun à son propre point entre 20 et 80 %, et les formes d'onde, SYNC et les destinations de la Poly-Mod passent en fondu. À 100 %, vous avez B en entier, envois d'effets compris ; les réglages que B ne contient pas (INSERT, emplacements de MOD 1 et 2, LFO 2, ENV DEST) reviennent à leurs valeurs d'origine."),
        ("Stop wherever you like: the sound you hear becomes the track's sound.",
         "Arrêtez-vous où vous voulez : le son entendu devient celui de la piste."),
        ("Back to 0 %: exactly A again.", "Retour à 0 % : exactement A.")]) +
 H3("What the six bars show", "Ce que montrent les six barres") +
 P2("The bars show six of the settings that travel: <b>CUT</b> (cutoff), <b>RES</b> (resonance), <b>ENV</b> (filter envelope amount), <b>MIX</b> (the mixer), <b>PW</b> (A's pulse width) and <b>PM</b> (POLY MOD's FILTER ENV amount). Each bar shows the current value; above 0 %, a white mark shows A and a colored mark B. The slider above shows the MORPH position.",
    "Six des réglages qui voyagent, en barres : <b>CUT</b> (coupure), <b>RES</b> (résonance), <b>ENV</b> (quantité d'enveloppe du filtre), <b>MIX</b> (le mixeur), <b>PW</b> (largeur d'impulsion de A) et <b>PM</b> (quantité FILTER ENV de POLY MOD). Chaque barre montre la valeur actuelle ; au-dessus de 0 %, un repère blanc indique A et un repère de couleur B. Le curseur au-dessus montre la position de MORPH.") +
 H3("Mutating, step by step", "Muter, pas à pas") +
 STEPS([("Set the amount with <b>KNOB 4</b>: low for a close variation, high for a very different sound.",
         "Réglez la quantité avec <b>KNOB 4</b> : faible, une variante proche ; forte, un son très différent."),
        ("Press <b>OCT+</b> (the <span class='k'>OCT+</span> MUTATE keycap, bottom left).",
         "Appuyez sur <b>OCT+</b> (la touche <span class='k'>OCT+</span> MUTATE, en bas à gauche)."),
        ("Press OCT+ again for another variation. Each press starts from the sound you hear.",
         "Appuyez de nouveau sur OCT+ pour une autre variante. Chaque appui part du son entendu."),
        ("Went one mutation too far? <b>Hold SAVE</b> for 1 s: the sound before the last mutation comes back.",
         "Une mutation de trop ? <b>Maintenez SAVE</b> 1 s : le son d'avant la dernière mutation revient.")]) +
 P2("MUTATE changes the waveforms and pitches, the mixer, the filter and its envelope, the pulse widths, the fine tuning and the sync, the Poly-Mod, the amplifier envelope and the LFO's speed, each by a random amount within what KNOB 4 allows. A mutation is never silent. After a mutation, MORPH goes back to 0 %: the mutated sound is the new A.",
    "MUTATE modifie les formes d'onde et les hauteurs, le mixeur, le filtre et son enveloppe, les largeurs d'impulsion, l'accord fin et la synchro, la Poly-Mod, l'enveloppe d'amplitude et la vitesse du LFO, chacun d'une quantité au hasard dans la limite permise par KNOB 4. Une mutation n'est jamais muette. Après une mutation, MORPH revient à 0 % : le son muté devient le nouveau A.") +
 H3("Keeping the result", "Garder le résultat") +
 P2("A morphed or mutated sound is not saved: the next sound you load replaces it. To keep it:",
    "Un son morphé ou muté n'est pas rangé : le prochain son chargé le remplace. Pour le conserver :") +
 LI([("<b>SAVE › PLACE</b>: in one of the 255 P600 places, replacing its sound (chapter {ch:keep}).",
      "<b>SAVE › PLACE</b> : dans l'une des 255 places P600, en remplaçant le son qui s'y trouve (chapitre {ch:keep})."),
     ("<b>SAVE › USER</b>: in one of the 32 USER places, with a name of your choice (chapter {ch:keep}).",
      "<b>SAVE › USER</b> : dans l'un des 32 emplacements USER, avec le nom de votre choix (chapitre {ch:keep})."),
     ("Or keep it in a project, with the music (chapter {ch:song}).", "Ou conservez-le dans un projet, avec la musique (chapitre {ch:song}).")]) +
 H3("Good to know", "Bon à savoir") +
 LI([("Turning KNOB 3 again replaces any setting changed by hand on another page in the meantime.",
      "Tourner de nouveau KNOB 3 remplace tout réglage changé à la main entre-temps sur une autre page."),
     ("Changing A with KNOB 1 keeps the MORPH position.",
      "Changer A avec KNOB 1 conserve la position de MORPH."),
     ("MORPH works on the selected track. Loading another sound on it, or selecting another track, sets MORPH back to 0 %, starting from the current sound.",
      "MORPH agit sur la piste choisie. Charger un autre son sur celle-ci, ou choisir une autre piste, remet MORPH à 0 %, à partir du son actuel."),
     ("A and B can be any P600 sounds, including those you saved or imported into the P600 places.",
      "A et B peuvent être n'importe quels sons P600, y compris ceux que vous avez enregistrés ou importés dans leurs places."),
     ("On this page, OCT+ always means MUTATE, and the octave does not change. Press OCT− twice to return to HOME.",
      "Sur cette page, OCT+ signifie toujours MUTATE, et l'octave ne change pas. Appuyez deux fois sur OCT− pour revenir à HOME."),
     ("PRESETS still changes the track's sound, through the whole list.",
      "PRESETS change toujours le son de la piste, dans toute la liste.")]))
