# 13 · BACKUP: the whole FM-1 in one file
CH("backup", "BACKUP: the whole FM-1 in one file", "BACKUP : tout le FM-1 dans un fichier",
 P2("The BACKUP page saves everything the FM-1 holds in one file on the computer, and puts it back: the music of the moment, "
    "the projects A to D, the 32 USER sounds, the three samples and their slices, the P600's places and the settings.",
    "La page BACKUP enregistre tout ce que contient le FM-1 dans un seul fichier sur l'ordinateur, et le remet en place : la "
    "musique du moment, les projets A à D, les 32 sons USER, les trois échantillons et leurs découpes, les places du P600 et "
    "les réglages.") +
 SHOT("backup", "The BACKUP page: the FM-1 on the left, a file on the right.",
      "La page BACKUP : le FM-1 à gauche, un fichier à droite.") +
 BOX("note", ("Make a backup before installing another firmware, before RESET ALL SOUNDS, and from time to time.",
              "Faites une sauvegarde avant d'installer un autre firmware, avant RESET ALL SOUNDS, et de temps en temps.")) +
 H3("ON THE FM-1: what it holds", "ON THE FM-1 : ce qu'il contient", EDC["backup"]) +
 P2("The list shows each part of the FM-1 and its size. A lit LED: the part holds something; EMPTY: nothing to save. "
    "TOTAL: the size of the whole.",
    "La liste montre chaque partie du FM-1 et sa taille. LED allumée : la partie contient quelque chose ; EMPTY : rien à "
    "enregistrer. TOTAL : la taille de l'ensemble.") +
 table([("Line", "Ligne"), ("What it is", "Ce que c'est")], [
     ["<b>CURRENT MUSIC</b>", ("The music as it is now: the four tracks, their sounds, steps and automation, the mix, the song.",
                               "La musique telle qu'elle est : les quatre pistes, leurs sons, pas et automations, le mixage, le morceau.")],
     ["<b>SETTINGS</b>", ("The settings of the MENU (chapter {ch:settings}).", "Les réglages du MENU (chapitre {ch:settings}).")],
     ["<b>PROJECT A … D</b>", ("The four saved projects (chapter {ch:projects}).", "Les quatre projets enregistrés (chapitre {ch:projects}).")],
     ["<b>USER SOUNDS 1–16, 17–32</b>", ("The 32 USER sounds.", "Les 32 sons USER.")],
     ["<b>USER SOUNDS' FM6 PATCHES</b>", ("The FM6 patches of the USER sounds made with the FM6 engine.",
                                          "Les patchs FM6 des sons USER faits avec le moteur FM6.")],
     ["<b>SAMPLE USR1 … USR3</b>", ("The three user samples (chapter {ch:samples}).", "Les trois échantillons de l'utilisateur (chapitre {ch:samples}).")],
     ["<b>P600 PLACES</b>", ("The P600 sounds you saved over the 255 places (SAVE TO THIS PLACE, chapter {ch:sound}).",
                             "Les sons P600 enregistrés sur les 255 places (SAVE TO THIS PLACE, chapitre {ch:sound}).")],
     ["<b>FM6 VOICE BANK</b>", ("The FM6 voice bank loaded in the FM-1.", "La banque de voix FM6 chargée dans le FM-1.")],
     ["<b>SLICE SLICES</b>", ("The slices you set by hand on each sample (the SLICE engine, MAN mode).",
                              "Les découpes réglées à la main sur chaque échantillon (moteur SLICE, mode MAN).")]]) +
 H3("Saving a backup", "Enregistrer une sauvegarde", EDC["backup"]) +
 STEPS([("Stop the music (■).", "Arrêtez la musique (■)."),
        ("Click <b>SAVE A BACKUP TO THIS COMPUTER</b>. The bar under the list shows the progress.",
         "Cliquez sur <b>SAVE A BACKUP TO THIS COMPUTER</b>. La barre sous la liste montre l'avancement."),
        ("The browser saves <b>Guru-600-backup-</b><i>year-month-day</i><b>.json</b> in its downloads folder. Keep it somewhere safe.",
         "Le navigateur enregistre <b>Guru-600-backup-</b><i>année-mois-jour</i><b>.json</b> dans son dossier de téléchargements. Rangez-le en lieu sûr.")]) +
 P2("The file is the same as the one saved by the Guru-600 application on the Mac and by the installer: each of them can put it back.",
    "Le fichier est le même que celui qu'enregistrent l'application Guru-600 sur Mac et l'installateur : chacun d'eux peut le remettre en place.") +
 H3("FROM A FILE: restoring a backup", "FROM A FILE : restaurer une sauvegarde", EDC["backup"]) +
 STEPS([("Drop the backup file on the frame <b>DROP A BACKUP FILE HERE</b>, or click <b>CHOOSE A FILE</b>.",
         "Déposez le fichier de sauvegarde sur le cadre <b>DROP A BACKUP FILE HERE</b>, ou cliquez sur <b>CHOOSE A FILE</b>."),
        ("Check the file: its name, its date and where it comes from appear above the frame, and what it holds below it. Nothing is sent yet.",
         "Vérifiez le fichier : son nom, sa date et sa provenance s'affichent au-dessus du cadre, et ce qu'il contient en dessous. Rien n'est encore envoyé."),
        ("Stop the music (■), then click <b>RESTORE IT ON THE FM-1</b> and confirm.",
         "Arrêtez la musique (■), puis cliquez sur <b>RESTORE IT ON THE FM-1</b> et confirmez."),
        ("Keep the FM-1 connected until the message <b>Backup restored</b>. The editor then reads the FM-1 again.",
         "Gardez le FM-1 branché jusqu'au message <b>Sauvegarde restaurée</b>. L'éditeur relit alors le FM-1.")]) +
 BOX("warn", ("Restoring replaces everything on the FM-1: its music, projects, USER sounds, samples and settings. Save a backup of the FM-1 first if you may want it back.",
              "La restauration remplace tout sur le FM-1 : sa musique, ses projets, ses sons USER, ses échantillons et ses réglages. Enregistrez d'abord une sauvegarde du FM-1 si vous pouvez en avoir besoin.")) +
 P2("The FM-1 keeps its own CALIBRATION (how its buttons and knobs are wired), whatever the file holds. A file saved by the Mac application before it saved any music or settings leaves the FM-1's own in place.",
    "Le FM-1 garde sa propre CALIBRATION (le câblage de ses boutons et de ses boutons rotatifs), quel que soit le fichier. Un fichier de l'application Mac enregistré avant qu'elle ait de la musique ou des réglages laisse ceux du FM-1 en place.") +
 H3("If it does not work", "Si ça ne marche pas", EDC["backup"]) +
 QA([("The buttons stay grey.", "Les boutons restent gris.",
      "Connect the FM-1 (chapter {ch:connect}). RESTORE also needs a file chosen. If the left column says THIS FIRMWARE CANNOT BE BACKED UP FROM HERE, install the Guru-600 firmware again.",
      "Branchez le FM-1 (chapitre {ch:connect}). RESTORE demande aussi un fichier choisi. Si la colonne de gauche indique THIS FIRMWARE CANNOT BE BACKED UP FROM HERE, réinstallez le firmware Guru-600."),
     ("Stop the music first.", "Arrêtez d'abord la musique.",
      "Click ■, then try again.", "Cliquez sur ■, puis recommencez."),
     ("Not a complete backup.", "Ce n'est pas une sauvegarde complète.",
      "The file is not a backup of the FM-1, or it was damaged. Choose another one.",
      "Le fichier n'est pas une sauvegarde du FM-1, ou il est abîmé. Choisissez-en un autre."),
     ("Backup stopped: The device changed during backup.", "Sauvegarde interrompue : The device changed during backup.",
      "Something changed on the FM-1 while it was being saved. Leave it alone, music stopped, and save again.",
      "Quelque chose a changé sur le FM-1 pendant l'enregistrement. N'y touchez pas, musique arrêtée, et recommencez."),
     ("The cable came out during a restore.", "Le câble s'est débranché pendant une restauration.",
      "Connect the FM-1 again and restore the same file once more: it puts everything back from the start.",
      "Rebranchez le FM-1 et restaurez de nouveau le même fichier : il remet tout en place depuis le début.")]))
