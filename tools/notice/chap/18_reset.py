# 18 · Resets, calibration and rescue
CH("reset", "Resets, calibration and rescue", "Réinitialisations, calibrage et secours",
 table([("", ""), ("RESET SOUNDS", "RESET SOUNDS"), ("RESET GURU-600", "RESET GURU-600")], [
   [("Erases", "Oublie"), ("Every P600 sound you saved in a place or sent from a computer", "Tous les sons P600 enregistrés dans une place ou envoyés depuis un ordinateur"), ("Everything: settings, USER sounds, projects, the current music, samples, P600 sounds, the FM6 bank, MIDI LEARN", "Tout : réglages, sons USER, projets, musique en cours, échantillons, sons P600, banque FM6, MIDI LEARN")],
   [("Keeps", "Conserve"), ("Everything else: USER sounds, projects, settings, the current music", "Tout le reste : sons USER, projets, réglages, musique en cours"), ("Only the calibration of the controls", "Seulement le calibrage des commandes")],
   [("Afterwards", "Ensuite"), ("The 255 built-in sounds are back", "Les 255 sons intégrés sont revenus"), ("The Guru-600 restarts fresh","Le Guru-600 redémarre comme neuf")]]) +
 H3("RESET SOUNDS: the original sounds back", "RESET SOUNDS : retour aux sons d'origine") +
 '<div class="split">' + shot("shots/menu_4.png", "MENU › SYSTEM.", "MENU › SYSTEM.", 220) + '<div>' +
 P2("Three ways, with the same result:", "Trois façons, pour le même résultat :") +
 STEPS([("<b>From the menu</b>: hold HOME, go to the SYSTEM tab with ALGORITHM, choose RESET SOUNDS with PRESETS and press OCT+. The band says SOUNDS RESET (or NO IMPORTED SOUND if there was none).",
         "<b>Par le menu</b> : maintenez HOME, allez à l'onglet SYSTEM avec ALGORITHM, choisissez RESET SOUNDS avec PRESETS et appuyez sur OCT+. Le bandeau indique SOUNDS RESET (ou NO IMPORTED SOUND s'il n'y en avait aucun)."),
        ("<b>At power-on</b>: hold SAVE while switching on. The screen asks RESET SOUNDS ?: OCT+ yes (DONE), OCT− no (CANCELLED). It waits until you answer.",
         "<b>À l'allumage</b> : maintenez SAVE en allumant le FM-1. L'écran demande RESET SOUNDS ? : OCT+ oui (DONE), OCT− non (CANCELLED). Il attend votre réponse."),
        ("<b>From a computer</b>: on the Sound Sender page, click Restore the original sounds (chapter {ch:import}).",
         "<b>Depuis un ordinateur</b> : sur la page d'envoi, Restaurer les sons d'origine (chapitre {ch:import}).")]) +
 '</div></div>' +
 BOX("warn", ("In the menu, RESET SOUNDS asks for no confirmation: OCT+ erases your P600 sounds immediately. To keep them, copy them to a computer first (chapter {ch:import}). To reset a single place, use ORIG on SAVE › PLACE instead (chapter {ch:keep}).",
              "Dans le menu, RESET SOUNDS ne pose pas de question : OCT+ oublie aussitôt vos sons P600. Pour les conserver, récupérez-les d'abord sur un ordinateur (chapitre {ch:import}). Pour oublier une seule place, utilisez plutôt ORIG sur SAVE › PLACE (chapitre {ch:keep}).")) +
 H3("RESET GURU-600: as good as new", "RESET GURU-600 : comme neuf") +
 STEPS([("Hold HOME, go to SYSTEM, choose <b>RESET GURU-600</b> and press OCT+.",
         "Maintenez HOME, allez à SYSTEM, choisissez <b>RESET GURU-600</b> et appuyez sur OCT+."),
        ("ARE YOU SURE? / ALL WILL BE ERASED: <b>OCT+</b> confirms, OCT− cancels.",
         "ARE YOU SURE? / ALL WILL BE ERASED : <b>OCT+</b> confirme, OCT− annule."),
        ("The Guru-600 restarts as new.",
         "Le Guru-600 redémarre comme neuf.")]) +
 P2("First back up what you want to keep (the BACKUP page of the Guru-600 editor, chapter {ch:editor}). The Mac application works the same way.",
    "Sauvegardez d'abord ce que vous voulez conserver (la page BACKUP de l'éditeur Guru-600, chapitre {ch:editor}). L'application Mac fonctionne de la même façon.") +
 H3("CALIBRATION: when a button or knob responds incorrectly", "CALIBRATION : quand un bouton répond mal") +
 P2("If a button acts like another one, or a knob turns the wrong way, teach the FM-1 its controls again:",
    "Si un bouton agit comme un autre, ou si un bouton rotatif tourne à l'envers, réapprenez ses commandes au FM-1 :") +
 STEPS([("MENU › SYSTEM › <b>CALIBRATION</b>, OCT+; or hold OCT− and OCT+ together while switching on.",
         "MENU › SYSTEM › <b>CALIBRATION</b>, OCT+ ; ou maintenez OCT− et OCT+ ensemble en allumant le FM-1."),
        ("HARDWARE CALIBRATION: let go of every button. At each PRESS, press the button named: the 14 buttons, in the order FX, SCL, ENV, LFO, EDIT, GLO, HOME, SAVE, ARP, SEQ, PLAY, REC, OCT−, OCT+.",
         "HARDWARE CALIBRATION : relâchez tous les boutons. À chaque PRESS, appuyez sur le bouton nommé : les 14 boutons, dans l'ordre FX, SCL, ENV, LFO, EDIT, GLO, HOME, SAVE, ARP, SEQ, PLAY, REC, OCT−, OCT+."),
        ("Then TURN RIGHT for each of the seven knobs (SELECT, ALGORITHM, PRESETS, KNOB 1 to 4): turn the knob named clockwise.",
         "Puis TURN RIGHT pour chacun des sept boutons rotatifs (SELECT, ALGORITHM, PRESETS, KNOB 1 à 4) : tournez le bouton nommé dans le sens des aiguilles d'une montre."),
        ("The calibration is saved (from the menu: when the menu closes). Pressing a keyboard key, or 30 s of inactivity, cancels it: SETUP CANCELLED, and the old settings remain.",
         "Le calibrage est enregistré (depuis le menu : à la fermeture de celui-ci). Un appui sur une touche du clavier, ou 30 s sans manipulation, annule l'opération : SETUP CANCELLED, et les anciens réglages restent.")]) +
 H3("If the FM-1 stops responding", "Si le FM-1 ne répond plus") +
 LI([("<b>Recovery mode on purpose</b>: hold OCT− and OCT+ for 5 s. During the countdown UPDATE MODE IN 3, 2, 1, let go to cancel (UPDATE CANCELLED). The FM-1 is then in recovery mode (a computer sees it as WL80UBOOT). To get out of it, see chapter {ch:install}.",
      "<b>Mode récupération volontaire</b> : maintenez OCT− et OCT+ pendant 5 s. Pendant le décompte UPDATE MODE IN 3, 2, 1, relâchez pour annuler (UPDATE CANCELLED). Le FM-1 est ensuite en mode récupération (un ordinateur le voit sous le nom WL80UBOOT). Pour en sortir, voyez le chapitre {ch:install}."),
     ("<b>FELUCCA CRASH</b> with numbers: a firmware error. The FM-1 restarts by itself after 4 s. If it happens again, note the numbers and reinstall.",
      "<b>FELUCCA CRASH</b> avec des chiffres : une erreur du firmware. Le FM-1 redémarre de lui-même au bout de 4 s. Si cela se reproduit, notez les chiffres et réinstallez."),
     ("<b>After two failed starts in a row</b>, the FM-1 goes into that same recovery mode by itself at the next start: see chapter {ch:install}.",
      "<b>Après deux démarrages ratés consécutifs</b>, le FM-1 passe de lui-même dans ce même mode récupération au démarrage suivant : voyez le chapitre {ch:install}."),
     ("<b>2ND CORE MISREAD: OFF</b>: the second core switched itself off; everything carries on as normal.",
      "<b>2ND CORE MISREAD: OFF</b> : le second cœur s'est désactivé de lui-même ; tout continue normalement."),
     ("<b>The sound freezes or a note hangs</b>: switch the FM-1 off and on again; your music comes back (RESTORE LAST).",
      "<b>Le son est figé ou une note reste accrochée</b> : éteignez et rallumez le FM-1 ; votre musique revient (RESTORE LAST).")]))
