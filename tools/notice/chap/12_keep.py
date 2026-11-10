# 12 · Keeping your sounds
NAMEKEYS = [("White keys", "Touches blanches", "Letters, by tapping the same key repeatedly (AB, CD, EF… as on an old phone); a tap within 0.8 s goes to the next letter of the key.", "Les lettres, en appuyant plusieurs fois sur la même touche (AB, CD, EF… comme sur un vieux téléphone) ; un appui dans les 0,8 s passe à la lettre suivante de la touche."),
            ("F#", "Fa#", "Cursor left.", "Curseur à gauche."), ("G#", "Sol#", "A space.", "Un espace."),
            ("A#", "La#", "Cursor right.", "Curseur à droite."), ("C#", "Do#", "Delete (held: repeats).", "Effacer (maintenu : répète)."),
            ("D#", "Ré#", "Letters ↔ numbers (123: 1 to 9, 0 and - . _ / # +).", "Lettres ↔ chiffres (123 : 1 à 9, 0 et - . _ / # +)."),
            ("KNOB 1", "KNOB 1", "Moves the cursor.", "Déplace le curseur."), ("KNOB 2", "KNOB 2", "Changes the character under the cursor.", "Change le caractère sous le curseur."),
            ("KNOB 3", "KNOB 3", "USER: the sound's family (BASS, LEAD…). PROJECT: a random name.", "USER : la famille du son (BASS, LEAD…). PROJECT : un nom au hasard."),
            ("OCT+", "OCT+", "Saves under that name.", "Enregistre, sous ce nom."), ("OCT−", "OCT−", "Cancels: nothing is saved.", "Annule : rien n'est écrit.")]
CH("keep", "Keeping your sounds", "Conserver vos sons",
 '<div class="key">' + P2("<b>The essentials.</b> Editing a sound does not change the saved sound: the next sound you load replaces your changes. To keep a sound, save it to one of two kinds of places:",
                          "<b>L'essentiel.</b> Modifier un son ne modifie pas le son rangé : le prochain son chargé remplace vos changements. Pour conserver un son, rangez-le à l'un de ces deux types d'endroits :") +
 table([("", ""), ("32 USER places", "32 emplacements USER"), ("255 P600 places", "255 places P600")], [
   [("What goes in", "Ce que vous y rangez"), ("Any sound, of any engine", "N'importe quel son, de n'importe quel moteur"), ("A P600 sound, replacing a built-in one (55 at most in total)", "Un son P600, à la place d'un son intégré (55 au plus en tout)")],
   [("Where", "Où"), ("SAVE › USER (U01 to U32); at the end of the PRESETS list", "SAVE › USER (U01 à U32) ; à la fin de la liste PRESETS"), ("SAVE › PLACE; in PRESETS, at that place's number (1 to 255)", "SAVE › PLACE ; dans PRESETS, au numéro de la place (1 à 255)")],
   [("Its name", "Son nom"), ("The one you type (12 characters)", "Celui que vous tapez (12 caractères)"), ("The sound's name, preceded by the new place's number: ORGAN I saved in place 30 becomes 30 ORGAN I. It cannot be changed on the FM-1", "Le nom du son, précédé du numéro de la nouvelle place : ORGAN I rangé dans la place 30 devient 30 ORGAN I. Il ne peut pas être changé sur le FM-1")],
   [("Kept after power-off", "Conservé après extinction"), ("Yes", "Oui"), ("Yes", "Oui")],
   [("Erased by", "Effacé par"), ("ERASE, or RESET GURU-600", "ERASE, ou RESET GURU-600"), ("ORIG, RESET SOUNDS, or RESET GURU-600", "ORIG, RESET SOUNDS, ou RESET GURU-600")]]) + '</div>' +
 BOX("warn", ("Save with the sequencer stopped. STOP TO SAVE: press PLAY to stop it, then save again.",
              "Enregistrez séquenceur arrêté. STOP TO SAVE : appuyez sur PLAY pour l'arrêter, puis enregistrez de nouveau.")) +
 H3("Saving to a USER place", "Enregistrer dans un emplacement USER") +
 '<div class="split">' + shot("shots/pg_save1.png", "SAVE › USER, page 1 of 6.", "SAVE › USER, page 1 sur 6.", 240) + '<div>' +
 STEPS([("Press <b>SAVE</b>: the USER page opens, with SAVE selected.",
         "Appuyez sur <b>SAVE</b> : la page USER s'ouvre, avec SAVE choisi."),
        ("Choose the place, U01 to U32, with <b>KNOB 1</b> or PRESETS. An empty place reads --.",
         "Choisissez l'emplacement, U01 à U32, avec <b>KNOB 1</b> ou PRESETS. Un emplacement vide affiche --."),
        ("Press <b>OCT+</b>. If the place is in use (OVERWRITE U05?): OCT+ to replace its sound, OCT− to keep it.",
         "Appuyez sur <b>OCT+</b>. Si l'emplacement est occupé (OVERWRITE U05?) : OCT+ pour remplacer le son, OCT− pour le conserver."),
        ("On the NAME screen, type a name if you like (table below), choose its family with KNOB 3, then press <b>OCT+</b>.",
         "Sur l'écran NAME, tapez un nom si vous le souhaitez (tableau ci-dessous), choisissez sa famille avec KNOB 3, puis appuyez sur <b>OCT+</b>.")]) +
 P2("The quickest save: <b>SAVE</b>, <b>OCT+</b>, <b>OCT+</b>.", "L'enregistrement le plus rapide : <b>SAVE</b>, <b>OCT+</b>, <b>OCT+</b>.") +
 '</div></div>' +
 table([("On the NAME screen", "Sur l'écran NAME"), ("", "")], [[T(f"<b>{a}</b>", f"<b>{b}</b>"), (c, d)] for a, b, c, d in NAMEKEYS]) +
 H4("Loading, renaming, erasing a USER sound", "Charger, renommer, effacer un son USER") +
 LI([("<b>Load</b>: turn PRESETS to the end of the list. Or on SAVE › USER: choose the place with KNOB 1, turn <b>KNOB 2</b> right (LOAD) and press OCT+.",
      "<b>Charger</b> : tournez PRESETS jusqu'à la fin de la liste. Ou sur SAVE › USER : choisissez l'emplacement avec KNOB 1, tournez <b>KNOB 2</b> à droite (LOAD) et appuyez sur OCT+."),
     ("<b>Rename</b>: on SAVE › USER, choose the place, tap <b>EDIT</b> and type the new name.",
      "<b>Renommer</b> : sur SAVE › USER, choisissez l'emplacement, appuyez sur <b>EDIT</b> et tapez le nouveau nom."),
     ("<b>Erase</b>: choose the place, turn <b>KNOB 3</b> right (ERASE), press OCT+, then OCT+ again to confirm.",
      "<b>Effacer</b> : choisissez l'emplacement, tournez <b>KNOB 3</b> à droite (ERASE), appuyez sur OCT+, puis de nouveau sur OCT+ pour confirmer."),
     ("To cancel: turn KNOB 2, 3 or 4 to the left, or press OCT− (a second press returns to HOME).",
      "Pour abandonner : tournez KNOB 2, 3 ou 4 vers la gauche, ou appuyez sur OCT− (un second appui ramène à HOME).")]) +
 H3("Saving a P600 sound to a place", "Enregistrer un son P600 dans une place") +
 '<div class="split">' + shot("shots/pg_save2.png", "SAVE › PLACE, page 2 of 6 (P600 tracks only).", "SAVE › PLACE, page 2 sur 6 (pistes P600 seulement).", 240) + '<div>' +
 STEPS([("On a P600 track, press <b>SAVE</b> twice: the <b>PLACE</b> page opens, on the sound's own place, with SAVE selected.",
         "Sur une piste P600, appuyez deux fois sur <b>SAVE</b> : la page <b>PLACE</b> s'ouvre, sur la place du son, avec SAVE choisi."),
        ("To save it elsewhere, choose another place, 1 to 255, with <b>KNOB 1</b>. A place in color already holds one of your sounds. Every place holds a sound: yours always replaces one. Do not use PRESETS here: it changes the track's sound, not the place.",
         "Pour l'enregistrer ailleurs, choisissez une autre place, de 1 à 255, avec <b>KNOB 1</b>. Une place en couleur contient déjà l'un de vos sons. Toutes les places contiennent un son : le vôtre en remplace toujours un. N'utilisez pas PRESETS ici : il change le son de la piste, pas la place."),
        ("Press <b>OCT+</b>, then <b>OCT+</b> again to confirm (SAVE IN PLACE 12?).",
         "Appuyez sur <b>OCT+</b>, puis de nouveau sur <b>OCT+</b> pour confirmer (SAVE IN PLACE 12?)."),
        ("The track now plays that place, and PRESETS finds your sound at that number.",
         "La piste joue désormais cette place, et PRESETS trouve votre son à ce numéro.")]) +
 '</div></div>' +
 LI([("Your sound replaces the built-in one <b>only while it is there</b>: the built-in sound is never lost and comes back with ORIG or RESET SOUNDS.",
      "Votre son remplace le son intégré <b>seulement tant qu'il est là</b> : le son intégré n'est jamais perdu et revient avec ORIG ou RESET SOUNDS."),
     ("<b>Saved with the sound</b>: the oscillators, the mixer, the filter and its envelope, the Poly-Mod, the amplifier envelope, the glide, UNI on or off (with its DETUNE), the LFO's rate, shape and destinations, WHEEL and VEL>FLT. <b>Not saved</b>: VINTAGE (back to 24 at each load), the effect sends (a kept sound plays dry, all sends at 0), the INSERT, MONO and LEG (a kept sound always plays POLY, or UNI if its unison was on), the LFO's PHS and FADE and the LFO 2 page, ENV DEST, MOD slots 1–2 and the VOICE pages. Use a USER place to keep everything.",
      "<b>Enregistrés avec le son</b> : les oscillateurs, le mixeur, le filtre et son enveloppe, la Poly-Mod, l'enveloppe d'amplitude, le glide, UNI actif ou non (avec son DETUNE), la vitesse, la forme et les destinations du LFO, WHEEL et VEL>FLT. <b>Non enregistrés</b> : VINTAGE (revient à 24 à chaque chargement), les envois d'effets (un son gardé joue sec, tous les envois à 0), l'INSERT, MONO et LEG (un son gardé joue toujours en POLY, ou en UNI si son unisson était actif), PHS et FADE du LFO et la page LFO 2, ENV DEST, les emplacements de MOD 1 et 2 et les pages VOICE. Utilisez un emplacement USER pour tout conserver."),
     ("The 55 places of your own are shared by the sounds you save here and the sounds sent from a computer (chapter {ch:import}). Beyond 55: P600 MEMORY FULL. Free up places with ORIG.",
      "Les 55 places à vous sont partagées entre les sons enregistrés ici et les sons envoyés depuis un ordinateur (chapitre {ch:import}). Au-delà de 55 : P600 MEMORY FULL. Libérez-en avec ORIG."),
     ("Wait 1.5 s after saving before switching off; the sound is written only while the sequencer is stopped. P600: NOT SAVED: the write failed; stop the sequencer and save the place again. If a USR3 sample sent by an older version of the firmware takes the storage area of the P600 sounds, they are kept only until power-off (no message): send a new sample to USR3, or erase it, from the SAMPLES page of the Guru-600 editor.",
      "Attendez 1,5 s après l'enregistrement avant d'éteindre ; le son n'est écrit que séquenceur arrêté. P600: NOT SAVED : l'écriture a échoué ; arrêtez le séquenceur et enregistrez de nouveau la place. Si un échantillon USR3 envoyé par une ancienne version du firmware occupe la zone de mémoire des sons P600, ceux-ci ne sont gardés que jusqu'à l'extinction (sans message) : envoyez un nouvel échantillon dans USR3, ou effacez-le, depuis la page SAMPLES de l'éditeur Guru-600."),
     ("NOT A P600 SOUND: the track's engine is not P600. Use SAVE › USER for it.",
      "NOT A P600 SOUND : le moteur de la piste n'est pas P600. Utilisez plutôt SAVE › USER.")]) +
 H4("Getting a place's original sound back", "Retrouver le son d'origine d'une place") +
 STEPS([("On SAVE › PLACE, choose the place with KNOB 1.", "Sur SAVE › PLACE, choisissez la place avec KNOB 1."),
        ("Turn <b>KNOB 3</b> right (ORIG) and press <b>OCT+</b> (ORIGINAL TO 12?).", "Tournez <b>KNOB 3</b> à droite (ORIG) et appuyez sur <b>OCT+</b> (ORIGINAL TO 12?)."),
        ("<b>OCT+</b> to confirm. ALREADY ORIGINAL: the place holds no sound of yours.", "<b>OCT+</b> pour confirmer. ALREADY ORIGINAL : la place ne contient aucun son à vous.")]) +
 H3("Undo, reload, forget", "Annuler, recharger, oublier") +
 LI([("<b>Back to the saved sound</b>: turn PRESETS one step away and back; the sound reloads as it was saved.",
      "<b>Revenir au son rangé</b> : tournez PRESETS d'un cran puis revenez ; le son se recharge tel qu'il est rangé."),
     ("<b>Undo a load</b>: hold SAVE for 1 s; hold again to redo. It undoes the track's last sound load (a quick run of PRESETS turns counts as one), MUTATE, pattern load or sequence edit.",
      "<b>Annuler un chargement</b> : maintenez SAVE 1 s ; maintenez de nouveau pour rétablir. Cela annule le dernier chargement de son de la piste (une série rapide de crans de PRESETS compte pour un seul), MUTATE, chargement de séquence ou modification de séquence."),
     ("<b>Clear all your P600 sounds at once</b>: RESET SOUNDS (chapter {ch:reset}). Your USER sounds are not affected.",
      "<b>Oublier d'un coup tous vos sons P600</b> : RESET SOUNDS (chapitre {ch:reset}). Vos sons USER ne sont pas touchés.")]) +
 BOX("tip", ("A project (SAVE › PROJECT) keeps the four tracks' sounds with the music, as they are (chapter {ch:song}).",
             "Un projet (SAVE › PROJECT) conserve les sons des quatre pistes avec la musique, tels qu'ils sont (chapitre {ch:song}).")))
