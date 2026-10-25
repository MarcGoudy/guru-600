# 2 · Installing the Guru-600 on an FM-1
CH("install", "Installing the Guru-600 on an FM-1", "Installer le Guru-600 sur un FM-1",
 BOX("warn", ("The Guru-600 1.0 is a first release, installed at your own risk: the author accepts no responsibility if your FM-1 is "
              "damaged or misbehaves. The Guru-600 replaces the official M-VAVE firmware, which you can put back at any time.",
              "Le Guru-600 1.0 est une première version, installée à vos risques : l'auteur décline toute responsabilité si votre FM-1 "
              "est endommagé ou fonctionne mal. Le Guru-600 remplace le firmware officiel de M-VAVE, que vous pouvez remettre à tout moment.")) +
 H3("What you need", "Ce qu'il vous faut") +
 LI([("The FM-1.",
      "Le FM-1."),
     ("A USB <b>data</b> cable, plugged directly into the computer.",
      "Un câble USB <b>de données</b>, branché directement sur l'ordinateur."),
     ("A Mac, a PC or a Linux computer.",
      "Un Mac, un PC ou un ordinateur Linux."),
     ("A MIDI-compatible browser: Chrome, Edge, Brave, Opera…",
      "Un navigateur compatible MIDI : Chrome, Edge, Brave, Opera…"),
     ("The Guru-600 installation page: <a href='https://marcgoudy.github.io/guru-600/'>marcgoudy.github.io/guru-600</a>.",
      "La page d'installation du Guru-600 : <a href='https://marcgoudy.github.io/guru-600/'>marcgoudy.github.io/guru-600</a>.")]) +
 H3("Installing, step by step", "Installer, pas à pas") +
 STEPS([("Switch the FM-1 on and connect it to the computer with the USB data cable.",
         "Allumez le FM-1 et branchez-le à l'ordinateur avec le câble USB de données."),
        ("Close every application that uses MIDI (music software, another browser tab with an editor).",
         "Fermez toutes les applications qui utilisent le MIDI (logiciel de musique, autre onglet avec un éditeur)."),
        ("Open the installation page and press <b>Install</b>. When the browser asks for MIDI (SysEx) access, allow it.",
         "Ouvrez la page d'installation et cliquez sur <b>Installer</b>. Quand le navigateur demande l'accès MIDI (SysEx), autorisez-le."),
        ("Do not unplug the cable and do not close the page during the installation.",
         "Ne débranchez pas le câble et ne fermez pas la page pendant l'installation."),
        ("The FM-1 restarts.",
         "Le FM-1 redémarre.")]) +
 H3("If the installation stops", "Si l'installation s'arrête") +
 table([("The page says", "La page affiche"), ("What to do", "Que faire")], [
   [("This browser cannot do it.", "Ce navigateur ne peut pas le faire."), ("Open the page in a MIDI-compatible browser: Chrome, Edge, Brave, Opera…", "Ouvrez la page dans un navigateur compatible MIDI : Chrome, Edge, Brave, Opera…")],
   [("MIDI (SysEx) access was not allowed.", "L'accès MIDI (SysEx) n'a pas été autorisé."), ("Click the icon to the left of the address bar, allow MIDI for the site, then press Install again.", "Cliquez sur l'icône à gauche de la barre d'adresse, autorisez le MIDI pour le site, puis cliquez de nouveau sur Installer.")],
   [("FM-1 not found.", "FM-1 introuvable."), ("Check the cable (a data cable), switch the FM-1 on, close the other applications that use MIDI, and press Install again.", "Vérifiez le câble (un câble de données), allumez le FM-1, fermez les autres applications qui utilisent le MIDI, puis cliquez de nouveau sur Installer.")],
   [("The connected device is not an FM-1.", "L'appareil branché n'est pas un FM-1."), ("Unplug the other MIDI devices and try again.", "Débranchez les autres appareils MIDI et recommencez.")],
   [("The USB connection was lost. / Stopped.", "La connexion USB a été perdue. / Arrêté."), ("Replug the cable and press Install again.", "Rebranchez le câble et cliquez de nouveau sur Installer.")],
   [("The FM-1 in update mode was not found.", "Le FM-1 en mode mise à jour est introuvable."), ("Replug the USB cable and press Install again.", "Rebranchez le câble USB et cliquez de nouveau sur Installer.")],
   [("The FM-1 did not come back.", "Le FM-1 n'est pas revenu."), ("Switch it off and on again.", "Éteignez-le puis rallumez-le.")],
   [("The file to install is damaged.", "Le fichier à installer est endommagé."), ("Reload the page and start again.", "Rechargez la page et recommencez.")]]) +
 P2("If the FM-1 runs a firmware from another author that the installation page does not find, first put back the official M-VAVE firmware with M-VAVE's updater, then install the Guru-600.",
    "Si le FM-1 utilise un firmware d'un autre auteur que la page d'installation ne trouve pas, remettez d'abord le firmware officiel avec l'outil de mise à jour de M-VAVE, puis installez le Guru-600.") +
 P2("If the FM-1 no longer starts and the computer sees a USB device named <b>WL80UBOOT</b>: try another USB data cable, close the other applications that use MIDI and run the installation again. If the FM-1 stays in this mode, recover it with the FM-1 Transporter (link on the installation page).",
    "Si le FM-1 ne démarre plus et que l'ordinateur voit un périphérique USB nommé <b>WL80UBOOT</b> : essayez un autre câble USB de données, fermez les autres applications qui utilisent le MIDI et relancez l'installation. Si le FM-1 reste dans ce mode, récupérez-le avec le FM-1 Transporter (lien sur la page d'installation).") +
 H3("Updating the Guru-600", "Mettre à jour le Guru-600") +
 P2("A new version installs the same way, from the installation page. First back up with the Felucca web editor.",
    "Une nouvelle version s'installe de la même façon, depuis la page d'installation. Sauvegardez d'abord avec l'éditeur web Felucca.") +
 H3("Switching to another firmware, then coming back", "Passer à un autre firmware, puis revenir") +
 STEPS([("In the Felucca web editor (link on the installation page), click <b>Save backup</b>: a file is saved to the computer.",
         "Dans l'éditeur web Felucca (lien sur la page d'installation), cliquez sur <b>Save backup</b> : un fichier est enregistré sur l'ordinateur."),
        ("Install the other firmware with its own tool. For the official M-VAVE firmware: M-VAVE's updater, on M-VAVE's site.",
         "Installez l'autre firmware avec son propre outil. Pour le firmware officiel : l'outil de mise à jour de M-VAVE, sur le site de M-VAVE."),
        ("To come back, install the Guru-600 from the installation page, then in the Felucca web editor click <b>Restore backup</b> and choose the file.",
         "Pour revenir, installez le Guru-600 depuis la page d'installation, puis, dans l'éditeur web Felucca, cliquez sur <b>Restore backup</b> et choisissez le fichier.")]) +
 P2("The FM-1 comes back exactly as you left it: the current music, the projects, the USER sounds, the P600 sounds kept in the places, the samples and their slices, the FM6 voice bank and the settings.",
    "Le FM-1 revient exactement tel que vous l'aviez laissé : la musique en cours, les projets, les sons USER, les sons P600 rangés dans les places, les échantillons et leurs découpes, la banque de voix FM6 et les réglages.") +
 felucca("Installation", "The Felucca installation guide also explains the Transporter and the recovery tools.",
         "Le guide d'installation de Felucca explique aussi le Transporter et les outils de récupération."))
