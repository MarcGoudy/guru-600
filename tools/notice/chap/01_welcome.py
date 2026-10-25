# 1 · What the Guru-600 brings (the opening page)
CH("welcome", "What the Guru-600 brings", "Ce que le Guru-600 apporte",
 P2("The Guru-600 turns the M-VAVE FM-1 into an emulator of the <b>Sequential Circuits Prophet-600</b> (1982), one of the very "
    "first synthesizers with MIDI. It is a firmware: it replaces the FM-1's original firmware and can be removed at any time.",
    "Le Guru-600 transforme le M-VAVE FM-1 en émulateur du <b>Prophet-600 de Sequential Circuits</b> (1982), l'un des tout "
    "premiers synthétiseurs MIDI. C'est un firmware : il remplace celui d'origine du FM-1 et peut être retiré à tout moment.") +
 H3("What it adds", "Ce qu'il ajoute") +
 LI([("<b>A P600 sound engine</b> built like the original: two oscillators per voice with sync, a 24 dB filter with its own envelope, "
      "Poly-Mod, an LFO, unison and six voices (chapter {ch:p600}).",
      "<b>Un moteur sonore P600</b> construit comme l'original : deux oscillateurs par voix avec synchronisation, un filtre 24 dB avec son "
      "enveloppe, la Poly-Mod, un LFO, l'unisson et six voix (chapitre {ch:p600})."),
     ("<b>255 sounds</b>: the Prophet-600's 100 factory programs under their real names, 100 free sounds from the Prophet-600 "
      "community, and 55 sounds made for the Guru-600. With the 71 sounds of Felucca's other engines, the list holds 326 sounds, plus 32 USER slots for yours (chapter {ch:sounds}).",
      "<b>255 sons</b> : les 100 programmes d'usine du Prophet-600 sous leurs vrais noms, 100 sons libres de la communauté du "
      "Prophet-600 et 55 sons créés pour le Guru-600. Avec les 71 sons des autres moteurs de Felucca, la liste compte 326 sons, plus 32 emplacements USER pour les vôtres (chapitre {ch:sounds})."),
     ("<b>MORPH and MUTATE</b>: gradually turn one sound into another, or create a variation of a sound in one gesture (chapter {ch:morph}).",
      "<b>MORPH et MUTATE</b> : transformer progressivement un son en un autre, ou créer une variante d'un son en un geste (chapitre {ch:morph})."),
     ("<b>55 places of your own</b> for P600 sounds, in addition to the 32 USER places, with the original sound always one gesture away (chapter {ch:keep}).",
      "<b>55 places à vous</b> pour les sons P600, en plus des 32 emplacements USER, et le son d'origine toujours à portée d'un geste (chapitre {ch:keep})."),
     ("<b>Sounds sent from a computer</b>: original Prophet-600 files (.syx) go into the FM-1 and come back out in the "
      "Prophet-600's own format (chapter {ch:import}).",
      "<b>Des sons envoyés depuis un ordinateur</b> : les fichiers d'origine du Prophet-600 (.syx) entrent dans le FM-1 et en "
      "ressortent au format du Prophet-600 (chapitre {ch:import})."),
     ("<b>A chord memory</b>: play a chord once, and one finger then plays it in any key (chapter {ch:chords}).",
      "<b>Une mémoire d'accords</b> : jouez un accord une fois, un seul doigt le rejoue ensuite dans n'importe quelle tonalité (chapitre {ch:chords})."),
     ("<b>A MIDI map that follows the GliGli firmware's</b>: a setup made for a real Prophet-600 controls the Guru-600 as is (chapter {ch:midi}).",
      "<b>Une table MIDI qui suit celle du firmware GliGli</b> : un réglage prévu pour un vrai Prophet-600 pilote le Guru-600 tel quel (chapitre {ch:midi})."),
     ("<b>A new look</b>: Prophet-600-style pages, a screen that draws the sound in 3D in real time, a colored message band and an animated start screen (chapter {ch:screen}).",
      "<b>Un nouveau visage</b> : des pages à l'image du Prophet-600, un écran qui dessine le son en 3D en temps réel, un bandeau de messages coloré et un écran de démarrage animé (chapitre {ch:screen})."),
     ("<b>Easier navigation</b>: a double tap on a page button goes back one page, and a quick screen held 1 s stays open (chapters {ch:controls} and {ch:layers}).",
      "<b>Une navigation plus simple</b> : deux appuis rapides sur un bouton de page ramènent à la page précédente, et un écran rapide maintenu 1 s reste ouvert (chapitres {ch:controls} et {ch:layers})."),
     ("<b>Two resets</b>, clearly separated: one for the sounds only, one for the whole instrument (chapter {ch:reset}).",
      "<b>Deux réinitialisations</b>, bien distinctes : l'une pour les sons seuls, l'autre pour tout l'instrument (chapitre {ch:reset})."),
     ("<b>An application for Mac</b>: the whole Guru-600 on the computer screen, to explore it, prepare sounds, or play without the FM-1 (chapter {ch:app}).",
      "<b>Une application pour Mac</b> : tout le Guru-600 sur l'écran de l'ordinateur, pour le découvrir, préparer des sons ou jouer sans le FM-1 (chapitre {ch:app}).")]) +
 H3("What it keeps from Felucca", "Ce qu'il garde de Felucca") +
 P2("The Guru-600 is built on <b>Felucca</b>, a free firmware for the FM-1 by Leo Kuroshita. Everything Felucca does remains "
    "and works with the P600 engine: four tracks, thirteen other sound engines, a 64-step sequencer with automation, an "
    "arpeggiator, effects, scales and chords, songs and projects. Chapters {ch:tracks} to {ch:song} summarize them; the "
    "Felucca wiki gives the details.",
    "Le Guru-600 repose sur <b>Felucca</b>, un firmware libre pour le FM-1 écrit par Leo Kuroshita. Tout ce que fait Felucca "
    "demeure et fonctionne avec le moteur P600 : quatre pistes, treize autres moteurs sonores, un séquenceur de 64 pas avec "
    "automation, un arpégiateur, des effets, des gammes et des accords, des morceaux et des projets. Les chapitres "
    "{ch:tracks} à {ch:song} les résument ; le wiki de Felucca donne le détail.") +
 BOX("note", ("The Felucca wiki (" + wiki() + ") describes Felucca, the original firmware: a few details may differ in the Guru-600. It is in English.",
              "Le wiki de Felucca (" + wiki() + ") décrit Felucca, le firmware d'origine : quelques détails peuvent différer dans le Guru-600. Il est en anglais.")) +
 H3("Compared with the Prophet-600", "Face au Prophet-600") +
 P2("The Guru-600 is a digital imitation of an analog synthesizer. The 100 factory sounds use the original settings, "
    "read from Sequential's files. The envelopes, filter and LFO are calibrated on a measured Prophet-600. Each "
    "Prophet-600 sounded a little different from the next: expect the same character, not the same machine.",
    "Le Guru-600 est une imitation numérique d'un synthétiseur analogique. Les 100 sons d'usine reprennent les réglages "
    "d'origine, lus dans les fichiers de Sequential. Les enveloppes, le filtre et le LFO sont calibrés sur un Prophet-600 "
    "mesuré. Chaque Prophet-600 sonnait un peu différemment du suivant : attendez-vous au même caractère, pas à la même machine.") +
 P2("Beyond the original, on the P600 engine:", "Au-delà de l'original, sur le moteur P600 :") +
 LI([("An LFO with tempo sync and more shapes, a modulation matrix, velocity on the filter, stereo spread.",
      "Un LFO synchronisable au tempo avec plus de formes, une matrice de modulation, la vélocité sur le filtre, l'étalement stéréo."),
     ("Mono, legato and note priorities; VINTAGE drift; USB audio and MIDI.",
      "Mono, legato et priorités de notes ; la dérive VINTAGE ; audio et MIDI par USB.")]) +
 H3("How to read this guide", "Comment lire cette notice") +
 LI([("<b>New to synthesizers?</b> Read chapters {ch:first} (first steps) and {ch:basics} (the synthesizer in plain words), "
      "then {ch:controls} and {ch:screen}.",
      "<b>Vous débutez ?</b> Lisez les chapitres {ch:first} (premiers pas) et {ch:basics} (le synthétiseur expliqué "
      "simplement), puis {ch:controls} et {ch:screen}."),
     ("<b>You know synthesizers?</b> Go straight to the P600 engine ({ch:p600}), MORPH ({ch:morph}) and how to keep your sounds ({ch:keep}).",
      "<b>Vous connaissez les synthétiseurs ?</b> Allez directement au moteur P600 ({ch:p600}), à MORPH ({ch:morph}) et à l'enregistrement des sons ({ch:keep})."),
     ("<b>Something not working as expected?</b> Chapter {ch:faq} answers the usual questions and explains every message the screen can show.",
      "<b>Quelque chose ne marche pas comme prévu ?</b> Le chapitre {ch:faq} répond aux questions courantes et explique chaque message que l'écran peut afficher.")]) +
 H3("Conventions", "Conventions") +
 LI([("Words in <b>CAPITALS</b> are what you read on the FM-1's buttons and screen: <b>EDIT</b>, <b>CUTOFF</b>, <b>OCT+</b>.",
      "Les mots en <b>CAPITALES</b> sont ceux que vous lisez sur les boutons et l'écran du FM-1 : <b>EDIT</b>, <b>CUTOFF</b>, <b>OCT+</b>."),
     ("<b>KNOB 1</b> to <b>KNOB 4</b> are the four knobs at the top right, under the screen's four settings, from left to right.",
      "<b>KNOB 1</b> à <b>KNOB 4</b> sont les quatre boutons rotatifs en haut à droite, sous les quatre réglages de l'écran, de gauche à droite."),
     ("<b>MENU › SYSTEM › HELP</b> means: open the menu, go to the SYSTEM tab, choose the HELP row.",
      "<b>MENU › SYSTEM › HELP</b> signifie : ouvrez le menu, allez à l'onglet SYSTEM, choisissez la ligne HELP."),
     ("<b>Tap</b>: press and release right away. <b>Hold</b>: keep pressed. <b>Double tap</b>: two quick taps on the same button.",
      "<b>Appui</b> : appuyer et relâcher aussitôt. <b>Maintenir</b> : garder enfoncé. <b>Double appui</b> : deux appuis rapides sur le même bouton."),
     ("Notes use letter names: C D E F G A B; C4 is middle C.",
      "Les notes sont écrites à l'anglaise : C D E F G A B pour do ré mi fa sol la si ; C4 est le do du milieu.")]))
