# 13 · Sending and getting back sounds with a computer
CH("import", "Sending sounds from a computer, and getting them back", "Envoyer des sons depuis un ordinateur, et les récupérer",
 P2("The <b>Guru-600 Sound Sender</b> page (<a href='https://guru-600.com/envoi-sons.html'>guru-600.com/envoi-sons.html</a>) sends Prophet-600 sounds to the FM-1 and brings them back to the computer. The sounds stay in the FM-1 after power-off.",
    "La page <b>Guru-600 Sound Sender</b> (<a href='https://guru-600.com/envoi-sons.html'>guru-600.com/envoi-sons.html</a>) envoie des sons Prophet-600 au FM-1 et les rapatrie sur l'ordinateur. Les sons restent dans le FM-1 après extinction.") +
 '<div class="split">' + T('<img src="img/envoi_en.png" style="width:360px" alt="">', '<img src="img/envoi_fr.png" style="width:360px" alt="">', "figure") + '<div>' +
 H4("What it accepts", "Ce qu'elle accepte") +
 LI([("A <b>.syx</b> file of Prophet-600 sounds: an original Sequential program dump, or a GliGli firmware patch file.",
      "Un fichier <b>.syx</b> de sons Prophet-600 : un dump de programmes Sequential d'origine, ou un fichier de patchs du firmware GliGli."),
     ("One sound or a whole bank of 100 in the same file.", "Un seul son ou une banque entière de 100 dans le même fichier."),
     ("Any other file: No Prophet-600 sound in this file.", "Tout autre fichier : Aucun son Prophet-600 dans ce fichier.")]) +
 '</div></div>' +
 H3("Sending, step by step", "Envoyer, pas à pas") +
 STEPS([("Connect the FM-1 to the computer with a USB <b>data</b> cable and switch it on. Close the other applications that use MIDI.",
         "Branchez le FM-1 à l'ordinateur avec un câble USB <b>de données</b> et allumez-le. Fermez les autres applications qui utilisent le MIDI."),
        ("Open the page in <b>a MIDI-compatible browser</b> (Chrome, Edge, Brave, Opera…) and press <b>Connect</b>; allow MIDI (SysEx) when the browser asks.",
         "Ouvrez la page dans <b>un navigateur compatible MIDI</b> (Chrome, Edge, Brave, Opera…) et cliquez sur <b>Connecter</b> ; autorisez le MIDI (SysEx) quand le navigateur le demande."),
        ("Open the .syx file.",
         "Ouvrez le fichier .syx."),
        ("For each sound, type its place (1 to 255, as numbered in PRESETS) and press <b>Send</b>. Or type a first place and press <b>Send all</b>: the sounds go into consecutive places from there.",
         "Pour chaque son, tapez sa place (de 1 à 255, selon la numérotation de PRESETS) et cliquez sur <b>Envoyer</b>. Ou tapez une première place et cliquez sur <b>Tout envoyer</b> : les sons se suivent à partir de là."),
        ("The sounds are now in the PRESETS list.",
         "Les sons sont désormais dans la liste PRESETS.")]) +
 LI([("A sent sound replaces the built-in sound of its place until ORIG or RESET SOUNDS brings it back.",
      "Un son envoyé remplace le son intégré de sa place jusqu'à ce que ORIG ou RESET SOUNDS le rétablisse."),
     ("<b>55 sounds at most</b> in total, whether sent or saved on the FM-1, whatever their places. Beyond that: P600: NO FREE PLACE on the FM-1.",
      "<b>55 sons au maximum</b> en tout, envoyés ou enregistrés sur le FM-1, quelle que soit leur place. Au-delà : P600: NO FREE PLACE sur le FM-1."),
     ("Sending to a place that already holds a sound of yours replaces it without counting as an extra sound.",
      "Un son envoyé vers une place qui contient déjà l'un de vos sons remplace celui-ci, sans compter un son de plus."),
     ("An imported sound's name begins with its place number.", "Le nom d'un son importé commence par son numéro de place."),
     ("A sent sound is kept like a sound saved on SAVE › PLACE (chapter {ch:keep}): it plays POLY (or UNI if its unison is on), dry (no effect send) and with VINTAGE at 24.",
      "Un son envoyé est gardé comme un son enregistré sur SAVE › PLACE (chapitre {ch:keep}) : il joue en POLY (ou en UNI si son unisson est actif), sec (sans envoi d'effet) et avec VINTAGE à 24."),
     ("Any SysEx utility can also send a .syx file to the FM-1 by USB. A sound sent that way, with no place named, goes to the first place from 201 that holds none of your sounds, replacing a built-in Guru-600 sound there.",
      "N'importe quel utilitaire SysEx peut aussi envoyer un fichier .syx au FM-1 par USB. Un son envoyé ainsi, sans place indiquée, va dans la première place à partir de 201 qui ne contient aucun de vos sons, à la place d'un son intégré du Guru-600."),
     ("USB only: neither the MIDI socket (TRS) nor the Mac application receives sounds (chapter {ch:app}).",
      "USB seulement : ni la prise MIDI (TRS) ni l'application Mac ne reçoivent de sons (chapitre {ch:app})."),
     ("Send with the sequencer stopped.",
      "Envoyez les sons séquenceur arrêté.")]) +
 H3("Getting sounds back from the FM-1", "Récupérer des sons du FM-1") +
 P2("In the <b>GET SOUNDS BACK</b> box of the same page, once connected:", "Dans le cadre <b>RÉCUPÉRER DES SONS</b> de la même page, une fois connecté :") +
 LI([("<b>Get this place</b>: one sound, from the place you type.", "<b>Récupérer cette place</b> : un son, celui de la place indiquée."),
     ("<b>Get the saved and imported sounds</b>: all your sounds (No saved or imported sound on the FM-1 when there is none).", "<b>Récupérer les sons enregistrés et importés</b> : tous vos sons (Aucun son enregistré ou importé sur le FM-1 s'il n'y en a pas)."),
     ("<b>Get all 255</b>: the whole bank.", "<b>Tout récupérer (255)</b> : toute la banque.")]) +
 P2("The sounds arrive in a .syx file in your Downloads folder, in the Prophet-600's format (Sequential's). Send it back to the FM-1, keep it as a backup, share it or load it into a real Prophet-600. An unmodified factory sound comes back identical to Sequential's original; finer Guru-600 settings are rounded to the nearest Prophet-600 value. Send a real Prophet-600 only places 1 to 100: place 101 lands on its program 01, and so does place 201.",
    "Les sons arrivent dans un fichier .syx, dans le dossier Téléchargements, au format du Prophet-600 (celui de Sequential). Renvoyez-le au FM-1, gardez-le en sauvegarde, partagez-le ou chargez-le dans un vrai Prophet-600. Un son d'usine non modifié revient identique à l'original de Sequential ; les réglages plus fins du Guru-600 sont arrondis à la valeur la plus proche du Prophet-600. N'envoyez à un vrai Prophet-600 que les places 1 à 100 : la place 101 arrive sur son programme 01, la place 201 aussi.") +
 BOX("note", ("Only what a Prophet-600 sound can hold travels this way. WHEEL travels as the LFO's INITIAL AMOUNT; VEL>FLT, VINTAGE, DETUNE, the LFO's volume destination and the effects do not; the LFO's shape becomes triangle or square, and the glide is rounded. Names do not travel: sent back, a sound is named P600 and a number. To keep everything, use USER places or projects, and the BACKUP page of the Guru-600 editor (chapter {ch:editor}).",
              "Seul ce que peut contenir un son de Prophet-600 voyage ainsi. WHEEL voyage comme INITIAL AMOUNT du LFO ; VEL>FLT, VINTAGE, DETUNE, la destination volume du LFO et les effets, non ; la forme du LFO devient triangle ou carré, et le glide est arrondi. Les noms ne voyagent pas : renvoyé, un son s'appelle P600 suivi d'un numéro. Pour tout conserver, utilisez les emplacements USER ou les projets, et la page BACKUP de l'éditeur Guru-600 (chapitre {ch:editor}).")) +
 H3("Restoring the original sounds from the computer", "Rétablir les sons d'origine depuis l'ordinateur") +
 P2("In the RESET box, <b>Restore the original sounds</b> erases every sent or saved sound, after confirmation, and brings back the 255 built-in sounds. Same as RESET SOUNDS on the FM-1 (chapter {ch:reset}).",
    "Dans le cadre RÉINITIALISATION, <b>Restaurer les sons d'origine</b> oublie tous les sons envoyés ou enregistrés, après confirmation, et rétablit les 255 sons intégrés. Identique à RESET SOUNDS sur le FM-1 (chapitre {ch:reset}).") +
 H3("If it does not work", "Si cela ne fonctionne pas") +
 table([("The page says", "La page affiche"), ("What to do", "Que faire")], [
   [("This browser has no Web MIDI.", "Ce navigateur ne prend pas en charge Web MIDI."), ("Use a MIDI-compatible browser: Chrome, Edge, Brave, Opera…", "Utilisez un navigateur compatible MIDI : Chrome, Edge, Brave, Opera…")],
   [("MIDI (SysEx) access was not allowed.", "L'accès MIDI (SysEx) n'a pas été autorisé."), ("Allow MIDI in the site settings (the icon to the left of the address bar) and press Connect again.", "Autorisez le MIDI dans les paramètres du site (l'icône à gauche de la barre d'adresse) et cliquez de nouveau sur Connecter.")],
   [("No MIDI output found.", "Aucune sortie MIDI trouvée."), ("Check the cable (a data cable) and that the FM-1 is on.", "Vérifiez le câble (un câble de données) et assurez-vous que le FM-1 est allumé.")],
   [("The FM-1 does not answer.", "Le FM-1 ne répond pas."), ("Check that it is running the Guru-600 and is connected by USB, then press Connect again.", "Vérifiez qu'il utilise bien le Guru-600 et qu'il est branché en USB, puis cliquez de nouveau sur Connecter.")]]))
