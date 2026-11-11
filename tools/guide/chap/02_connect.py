# 02 · Opening the editor and connecting the FM-1
CH("connect", "Opening the editor", "Ouvrir l'éditeur",
 H3("Opening it", "L'ouvrir", EDC["sound"]) +
 LI([("<b>Online</b>: go to <b><a href='https://guru-600.com/editor/'>guru-600.com/editor/</a></b> with Chrome, Edge, Brave or Opera.",
      "<b>En ligne</b> : allez sur <b><a href='https://guru-600.com/editor/'>guru-600.com/editor/</a></b> avec Chrome, Edge, Brave ou Opera."),
     ("<b>Without internet</b>: in the <b>Guru-600 Editor</b> folder, open <b>editor › index.html</b> with one of these browsers (right-click › Open With). Keep the <b>editor</b> and <b>guide</b> folders side by side.",
      "<b>Sans internet</b> : dans le dossier <b>Guru-600 Editor</b>, ouvrez <b>editor › index.html</b> avec l'un de ces navigateurs (clic droit › Ouvrir avec). Gardez les dossiers <b>editor</b> et <b>guide</b> côte à côte.")]) +
 H3("Connecting the FM-1", "Brancher le FM-1", EDC["sound"]) +
 STEPS([("Connect the FM-1 to the computer with the USB cable and switch it on.",
         "Branchez le FM-1 à l'ordinateur avec le câble USB et allumez-le."),
        ("Click <b>CONNECT FM-1</b> at the top of the editor (or its LED).",
         "Cliquez sur <b>CONNECT FM-1</b> en haut de l'éditeur (ou sur son voyant)."),
        ("The first time, the browser asks to use your MIDI devices: click <b>Allow</b>.",
         "La première fois, le navigateur demande à utiliser vos appareils MIDI : cliquez sur <b>Autoriser</b>."),
        ("The LED lights green and the label says <b>FM-1 CONNECTED</b>. The editor reads the FM-1: the page shows its sounds and its music.",
         "Le voyant s'allume en vert et l'étiquette indique <b>FM-1 CONNECTED</b>. L'éditeur lit le FM-1 : la page affiche ses sons et sa musique.")]) +
 P2("Afterwards, the editor connects by itself when it opens and when you plug the FM-1 in. Unplugged, the LED goes out and the label comes back to CONNECT FM-1; the values stay on screen.",
    "Ensuite, l'éditeur se connecte tout seul à l'ouverture et quand vous branchez le FM-1. Débranché, le voyant s'éteint et l'étiquette revient à CONNECT FM-1 ; les valeurs restent affichées.") +
 H3("With the Guru-600 application on a Mac", "Avec l'application Guru-600 sur Mac", EDC["sound"]) +
 P2("Open <b>Guru-600.app</b>: the editor connects to it as to an FM-1, and you hear it on the Mac. Everything in this guide works with it, the FM-1 left aside.",
    "Ouvrez <b>Guru-600.app</b> : l'éditeur s'y connecte comme à un FM-1, et vous l'entendez sur le Mac. Tout ce que décrit ce guide fonctionne avec elle, sans le FM-1.") +
 H3("Without the FM-1", "Sans le FM-1", EDC["sound"]) +
 P2("Every page can be explored without the FM-1: it shows example values, and the knobs, switches and lists move. Nothing is kept: what needs the FM-1 (saving, loading, playing, sending) says <b>Connect the FM-1 first.</b>",
    "Chaque page peut être découverte sans le FM-1 : elle affiche des valeurs d'exemple, et les boutons, interrupteurs et listes bougent. Rien n'est gardé : ce qui demande le FM-1 (enregistrer, charger, jouer, envoyer) indique <b>Branchez d'abord le FM-1.</b>") +
 H3("If it does not connect", "Si la connexion ne se fait pas", EDC["sound"]) +
 QA([("This browser has no MIDI.", "Ce navigateur n'a pas le MIDI.",
      "Open the editor with Chrome, Edge, Brave or Opera.", "Ouvrez l'éditeur avec Chrome, Edge, Brave ou Opera."),
     ("MIDI access was refused.", "L'accès au MIDI a été refusé.",
      "Allow MIDI for this page in the browser's site settings (the icon at the left of the address bar), then reload the page.",
      "Autorisez le MIDI pour cette page dans les réglages du site du navigateur (l'icône à gauche de la barre d'adresse), puis rechargez la page."),
     ("No FM-1 found.", "Aucun FM-1 trouvé.",
      "Check that the FM-1 is on, that the cable carries data (try another one), and that no other program uses the FM-1 (another editor, a music program): close it and click CONNECT FM-1 again.",
      "Vérifiez que le FM-1 est allumé, que le câble transporte les données (essayez-en un autre), et qu'aucun autre programme n'utilise le FM-1 (un autre éditeur, un logiciel de musique) : fermez-le et cliquez de nouveau sur CONNECT FM-1."),
     ("This FM-1 needs the Guru-600 firmware.", "Ce FM-1 doit avoir le firmware Guru-600.",
      "The FM-1 runs another firmware: install the Guru-600 (see the Guru-600 user guide).",
      "Le FM-1 a un autre firmware : installez le Guru-600 (voir la notice du Guru-600)."),
     ("The FM-1 does not answer.", "Le FM-1 ne répond pas.",
      "Unplug the FM-1, plug it in again and wait for FM-1 CONNECTED.", "Débranchez le FM-1, rebranchez-le et attendez FM-1 CONNECTED.")]))
