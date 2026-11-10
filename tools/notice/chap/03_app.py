# 3 · The Guru-600 application on a Mac
APPKEYS = [("A W S E D F T G Y H U J K O L P ; '", "the keys, from C4 (A) up to F5 (')", "les touches, du C4 (A) au F5 (')"),
           ("← / →", "OCT− / OCT+", "OCT− / OCT+"), ("Space", "PLAY", "PLAY"), ("R", "REC", "REC"),
           ("1 2 3 4 5", "FX, SCL, ENV, LFO, EDIT", "FX, SCL, ENV, LFO, EDIT"),
           ("6 7 8 9 0", "GLO, HOME, SAVE, ARP, SEQ", "GLO, HOME, SAVE, ARP, SEQ"),
           ("[ / ]", "turn SELECT", "tourner SELECT"), ("- / =", "turn PRESETS", "tourner PRESETS"),
           (", / .", "turn ALGORITHM", "tourner ALGORITHM"), ("Esc", "quit (the memory is kept)", "quitter (la mémoire est gardée)")]
CH("app", "The Guru-600 application on a Mac", "L'application Guru-600 sur Mac",
 P2("<b>Guru-600.app</b> runs the Guru-600 firmware in an FM-1 emulator on the Mac. Everything in this guide works in it: "
    "explore the Guru-600 before installing it, prepare sounds, learn the pages or play without the device.",
    "<b>Guru-600.app</b> fait tourner le firmware Guru-600 dans un émulateur du FM-1 sur le Mac. Tout ce que décrit cette "
    "notice y fonctionne : découvrez le Guru-600 avant de l'installer, préparez des sons, apprenez les pages ou jouez sans "
    "l'appareil.") +
 BOX("note", ("It needs a Mac with Apple silicon (M1 or later).",
              "Il faut un Mac à puce Apple (M1 ou plus récent).")) +
 H3("Installing and opening it", "L'installer et l'ouvrir") +
 STEPS([("Unzip <b>Guru-600-Mac.zip</b>.",
         "Décompressez <b>Guru-600-Mac.zip</b>."),
        ("Double-click <b>Guru-600.app</b>. The first time, the Mac blocks it: open System Settings › Privacy & Security and click <b>Open Anyway</b>.",
         "Double-cliquez sur <b>Guru-600.app</b>. La première fois, le Mac la bloque : ouvrez Réglages Système › Confidentialité et sécurité et cliquez sur <b>Ouvrir quand même</b>.")]) +
 H3("Playing with the mouse", "Jouer à la souris") +
 LI([("<b>Buttons and keys</b>: click. Hold the mouse button down to hold them; drag across the keys for a glissando.",
      "<b>Boutons et touches</b> : cliquez. Gardez le bouton de la souris enfoncé pour les maintenir ; glissez sur les touches pour un glissando."),
     ("<b>Knobs</b> (SELECT, PRESETS, ALGORITHM, KNOB 1 to 4, MASTER): drag up or down on them, or scroll over them with the wheel or the trackpad. Up turns clockwise.",
      "<b>Boutons rotatifs</b> (SELECT, PRESETS, ALGORITHM, KNOB 1 à 4, MASTER) : glissez dessus vers le haut ou le bas, ou faites défiler avec la molette ou le trackpad au-dessus d'eux. Vers le haut revient à tourner vers la droite."),
     ("<b>Double tap</b>: two quick clicks on the same button.", "<b>Double appui</b> : deux clics rapides sur le même bouton."),
     ("<b>Quick screens</b> (chapter {ch:layers}): hold the button for more than 1 s, then let go: the quick screen stays "
      "open, and you can click its keys and knobs. Click the button again to close it.",
      "<b>Écrans rapides</b> (chapitre {ch:layers}) : maintenez le bouton plus de 1 s et relâchez : l'écran rapide reste "
      "ouvert, et vous pouvez cliquer sur ses touches et ses boutons. Cliquez de nouveau sur le bouton pour le fermer."),
     ("<b>Two controls at once</b> (GLO + PLAY, OCT− + OCT+…): hold one with the computer keyboard and click the other.",
      "<b>Deux commandes à la fois</b> (GLO + PLAY, OCT− + OCT+…) : maintenez l'une avec le clavier de l'ordinateur et cliquez sur l'autre.")]) +
 H3("Playing with the computer keyboard", "Jouer au clavier de l'ordinateur") +
 table([("Mac key", "Touche du Mac"), ("FM-1", "FM-1")], [[f"<b>{e(a)}</b>", (b, c)] for a, b, c in APPKEYS]) +
 P2("KNOB 1 to 4 and MASTER can only be turned with the mouse. The letters refer to key positions on a QWERTY keyboard; on an AZERTY keyboard, use the keys in the same positions.",
    "KNOB 1 à 4 et MASTER se tournent à la souris uniquement. Les lettres suivent la position des touches d'un clavier QWERTY ; sur un clavier AZERTY, ce sont les touches situées aux mêmes endroits.") +
 H3("A MIDI keyboard", "Un clavier MIDI") +
 P2("Every MIDI keyboard or controller connected to the Mac <b>before you open the application</b> plays it. If you connect one later, quit the application and open it again. Its mod wheel and knobs work as described in chapter {ch:midi}.",
    "Tout clavier ou contrôleur MIDI branché au Mac <b>avant d'ouvrir l'application</b> la fait jouer. S'il est branché après, quittez l'application et rouvrez-la. Sa molette et ses boutons rotatifs fonctionnent comme décrit au chapitre {ch:midi}.") +
 H3("The menus", "Les menus") +
 LI([("<b>Backup</b> › <b>Export Backup…</b>: saves the application's whole memory in a file. <b>Import Backup…</b>: replaces that memory with a file's, from the application or from a FM-1; the application starts again (below).",
      "<b>Sauvegarde</b> › <b>Exporter une sauvegarde…</b> : enregistre toute la mémoire de l'application dans un fichier. <b>Importer une sauvegarde…</b> : remplace cette mémoire par celle d'un fichier, venu de l'application ou d'un FM-1 ; l'application redémarre (ci-dessous)."),
     ("<b>Audio</b> › <b>Latency</b>: <b>20 ms (fastest)</b>: instant response, but the sound may crackle if other applications are running. <b>50 ms (safest)</b>: no crackling, a slight delay. <b>35 ms</b>: in between.",
      "<b>Audio</b> › <b>Latency</b> (latence) : <b>20 ms (fastest)</b> : réponse immédiate, mais le son peut craquer si d'autres applications sont ouvertes. <b>50 ms (safest)</b> : aucun craquement, un léger retard. <b>35 ms</b> : entre les deux."),
     ("If the window's title shows less than 1.00x, close other applications or choose a higher latency.",
      "Si le titre de la fenêtre affiche moins de 1.00x, fermez d'autres applications ou choisissez une latence plus élevée."),
     ("<b>Window</b>: the usual macOS commands to place and size the window.",
      "<b>Fenêtre</b> : les commandes habituelles de macOS pour placer et dimensionner la fenêtre."),
     ("<b>Help</b> (Aide, Hilfe…) › <b>Guru-600 User Guide</b> opens this guide in your browser, in the Mac's language.",
      "<b>Aide</b> › <b>Notice d'utilisation du Guru-600</b> ouvre cette notice dans votre navigateur, dans la langue du Mac.")]) +
 H3("Its memory", "Sa mémoire") +
 P2("The application keeps your sounds, your projects and your settings. Quit with <b>Esc</b> or the red button to keep them. To back them up: <b>Backup › Export Backup…</b>. To start fresh, delete the file <b>~/Library/Application Support/Guru-600/flash.bin</b> with the application closed.",
    "L'application conserve vos sons, vos projets et vos réglages. Quittez avec <b>Échap</b> ou le bouton rouge pour les garder. Pour les sauvegarder : <b>Sauvegarde › Exporter une sauvegarde…</b>. Pour repartir de zéro, supprimez le fichier <b>~/Library/Application Support/Guru-600/flash.bin</b>, application fermée.") +
 H3("From the application to the FM-1, and back", "De l'application au FM-1, et inversement") +
 H4("From the application to the FM-1", "De l'application au FM-1") +
 STEPS([("In the application: <b>Backup \u203a Export Backup\u2026</b>, and choose where to save the file.",
         "Dans l'application : <b>Sauvegarde › Exporter une sauvegarde…</b>, et choisissez où enregistrer le fichier."),
        ("Connect the FM-1, open the Guru-600 editor (link on the installation page), and on its BACKUP page choose that file and click <b>RESTORE IT ON THE FM-1</b>.",
         "Branchez le FM-1, ouvrez l'éditeur Guru-600 (lien sur la page d'installation) et, sur sa page BACKUP, choisissez ce fichier et cliquez sur <b>RESTORE IT ON THE FM-1</b>.")]) +
 H4("From the FM-1 to the application", "Du FM-1 à l'application") +
 STEPS([("In the Guru-600 editor, on the BACKUP page, click <b>SAVE A BACKUP TO THIS COMPUTER</b>.",
         "Dans l'éditeur Guru-600, sur la page BACKUP, cliquez sur <b>SAVE A BACKUP TO THIS COMPUTER</b>."),
        ("In the application: <b>Backup \u203a Import Backup\u2026</b>, and choose that file. The application starts again with the FM-1's memory.",
         "Dans l'application : <b>Sauvegarde › Importer une sauvegarde…</b>, et choisissez ce fichier. L'application redémarre avec la mémoire du FM-1.")]) +
 LI([("Everything goes across: the music, the projects, the USER sounds, the P600 places, the samples and their slices, the FM6 voice bank and the settings. What the other machine held is replaced.",
      "Tout passe : la musique, les projets, les sons USER, les places P600, les échantillons et leurs découpes, la banque de voix FM6 et les réglages. Ce que contenait l'autre machine est remplacé."),
     ("The application saves the current music by itself, at most a little over a minute after your last change. To be sure of it, save it in a project before exporting (chapter {ch:song}).",
      "L'application enregistre la musique en cours d'elle-même, au plus un peu plus d'une minute après votre dernier changement. Pour en être sûr, rangez-la dans un projet avant d'exporter (chapitre {ch:song}).")]) +
 H3("With the Guru-600 editor", "Avec l'éditeur Guru-600") +
 P2("Open the application, then the Guru-600 editor (chapter {ch:editor}): the editor connects to the application as to an FM-1, and you hear everything you do in it. The Sound Sender page sends sounds to the application the same way. Their MIDI port is named <b>Guru-600</b>.",
    "Ouvrez l'application, puis l'éditeur Guru-600 (chapitre {ch:editor}) : l'éditeur se connecte à l'application comme à un FM-1, et vous entendez tout ce que vous y faites. La page d'envoi des sons envoie de même des sons à l'application. Leur port MIDI s'appelle <b>Guru-600</b>.") +
 H3("What the application cannot do", "Ce que l'application ne sait pas faire") +
 LI([("Work with the Felucca web editor: use the Guru-600 editor.",
      "Fonctionner avec l'éditeur web Felucca : utilisez l'éditeur Guru-600."),
     ("Send audio to other applications.", "Envoyer de l'audio vers d'autres applications.")]) +
 BOX("tip", ("<b>RESET GURU-600</b> (chapter {ch:reset}) also works in the application.",
             "<b>RESET GURU-600</b> (chapitre {ch:reset}) fonctionne aussi dans l'application.")))
