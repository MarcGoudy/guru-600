# 12 · SAMPLES: your own samples in USR1 to USR3
CH("samples", "SAMPLES: your own samples", "SAMPLES : vos propres échantillons",
 P2("The FM-1 has three slots for your own samples: <b>USR1</b>, <b>USR2</b> and <b>USR3</b>. The SAMPLE, GRAIN and SLICE "
    "engines play them. The SAMPLES page fills them from sound files on the computer.",
    "Le FM-1 a trois emplacements pour vos propres échantillons : <b>USR1</b>, <b>USR2</b> et <b>USR3</b>. Les moteurs "
    "SAMPLE, GRAIN et SLICE les jouent. La page SAMPLES les remplit à partir de fichiers son de l'ordinateur.") +
 SHOT("samples", "The SAMPLES page: one column per slot.", "La page SAMPLES : une colonne par emplacement.") +
 H3("What a slot holds", "Ce que contient un emplacement", EDC["samples"]) +
 LI([("Up to 16 files, each one a <b>zone</b>: it plays from its <b>root note</b>, on the keys around it.",
      "Jusqu'à 16 fichiers, chacun une <b>zone</b> : il joue depuis sa <b>note de base</b>, sur les touches autour d'elle."),
     ("A name of 8 characters at most.", "Un nom de 8 caractères au plus."),
     ("USR1 and USR2: 79.5 KiB each, about 7 seconds of sound. USR3: 67.5 KiB, about 6 seconds (the Guru-600 keeps the P600 sounds you saved at the end of USR3).",
      "USR1 et USR2 : 79,5 Kio chacun, environ 7 secondes de son. USR3 : 67,5 Kio, environ 6 secondes (le Guru-600 garde à la fin de USR3 les sons P600 que vous avez enregistrés).")]) +
 P2("The top line of each column shows what the slot holds now on the FM-1: its name and number of zones (or EMPTY), and how full it is.",
    "La ligne du haut de chaque colonne montre ce que contient l'emplacement sur le FM-1 : son nom et son nombre de zones (ou EMPTY), et son remplissage.") +
 H3("Sending samples", "Envoyer des échantillons", EDC["samples"]) +
 STEPS([("Drop one or more sound files on the frame <b>DROP WAV FILES HERE</b> of the slot, or click <b>CHOOSE FILES</b>. WAV files are best; most other sound files the browser can play work too.",
         "Déposez un ou plusieurs fichiers son sur le cadre <b>DROP WAV FILES HERE</b> de l'emplacement, ou cliquez sur <b>CHOOSE FILES</b>. Les fichiers WAV conviennent le mieux ; la plupart des autres fichiers son que le navigateur sait lire marchent aussi."),
        ("Check the list: for each file, its root note, the keys it plays (from–to) and its length. Click <b>▶</b> to hear it as the FM-1 will store it; <b>✕</b> removes it.",
         "Vérifiez la liste : pour chaque fichier, sa note de base, les touches qu'il joue (de–à) et sa durée. Cliquez sur <b>▶</b> pour l'écouter tel que le FM-1 le gardera ; <b>✕</b> le retire."),
        ("Change a root note if needed: click it, type the note (<b>C4</b>, <b>F#3</b>, <b>Bb2</b>…) and press Enter. The keys of every zone follow.",
         "Changez une note de base si besoin : cliquez dessus, tapez la note (<b>C4</b>, <b>F#3</b>, <b>Bb2</b>…) et appuyez sur Entrée. Les touches de chaque zone suivent."),
        ("Check the <b>NAME</b> (it takes the first file's name), then click <b>SEND TO USR</b><i>n</i> and confirm.",
         "Vérifiez le <b>NAME</b> (il reprend le nom du premier fichier), puis cliquez sur <b>SEND TO USR</b><i>n</i> et confirmez."),
        ("The bar shows the progress, then the message <b>Sent to USR</b><i>n</i>. The top line shows the new contents.",
         "La barre montre l'avancement, puis le message <b>Envoyé dans USR</b><i>n</i>. La ligne du haut affiche le nouveau contenu.")]) +
 BOX("warn", ("Sending replaces everything the slot held. A sound that played that slot now plays the new samples.",
              "L'envoi remplace tout ce que contenait l'emplacement. Un son qui jouait cet emplacement joue désormais les nouveaux échantillons.")) +
 H3("Root notes and keys", "Notes de base et touches", EDC["samples"]) +
 LI([("A file named with a note, such as <b>piano_C4.wav</b> or <b>F#3.wav</b>, takes that note as its root (C4 = middle C). Any other file takes <b>C4</b>.",
      "Un fichier dont le nom contient une note, comme <b>piano_C4.wav</b> ou <b>F#3.wav</b>, prend cette note comme note de base (C4 = do du milieu). Tout autre fichier prend <b>C4</b>."),
     ("The keys are shared out between the zones: each one plays up to halfway to the next root. The lowest goes down to the bottom of the keyboard, the highest up to the top.",
      "Les touches sont réparties entre les zones : chacune joue jusqu'à mi-chemin de la note de base suivante. La plus grave descend jusqu'en bas du clavier, la plus aiguë monte jusqu'en haut."),
     ("Two files cannot share a root note: their notes turn red, the line under the list says TWO FILES ON ONE ROOT NOTE and SEND stays grey. Change one of them.",
      "Deux fichiers ne peuvent pas avoir la même note de base : leurs notes passent en rouge, la ligne sous la liste indique TWO FILES ON ONE ROOT NOTE et SEND reste gris. Changez l'une des deux.")]) +
 H3("Size", "Taille", EDC["samples"]) +
 P2("The line under the list shows the size of the files against the slot's room. The files are stored at 22,050 Hz, in mono. "
    "Over the slot's room, the line turns red (TOO LONG FOR THE SLOT) and SEND stays grey: remove a file, or shorten your files on the computer.",
    "La ligne sous la liste montre la taille des fichiers par rapport à la place de l'emplacement. Les fichiers sont gardés à 22 050 Hz, en mono. "
    "Au-delà de la place disponible, la ligne passe en rouge (TOO LONG FOR THE SLOT) et SEND reste gris : retirez un fichier, ou raccourcissez vos fichiers sur l'ordinateur.") +
 H3("Erasing a slot", "Effacer un emplacement", EDC["samples"]) +
 P2("Click <b>ERASE</b> and confirm. The slot becomes EMPTY; a sound that played it plays a plain sine wave, and the FM-1 shows NO SAMPLE.",
    "Cliquez sur <b>ERASE</b> et confirmez. L'emplacement devient EMPTY ; un son qui le jouait joue une simple sinusoïde, et le FM-1 affiche NO SAMPLE.") +
 H3("Playing your samples", "Jouer vos échantillons", EDC["samples"]) +
 P2("On the FM-1, choose the SAMPLE, GRAIN or SLICE engine for a track (on the TRACKS page, chapter {ch:tracks}, or on the device), then its sound USR1, USR2 or USR3.",
    "Sur le FM-1, choisissez le moteur SAMPLE, GRAIN ou SLICE pour une piste (sur la page TRACKS, chapitre {ch:tracks}, ou sur l'appareil), puis son son USR1, USR2 ou USR3.") +
 QA([("This file could not be read.", "Ce fichier n'a pas pu être lu.",
      "The browser cannot decode it. Save it as WAV on the computer and drop it again.",
      "Le navigateur ne sait pas le décoder. Enregistrez-le en WAV sur l'ordinateur et déposez-le de nouveau."),
     ("16 files at most: the others were left out.", "16 fichiers au plus : les autres ont été laissés de côté.",
      "A slot holds 16 zones. Use another slot for the rest.", "Un emplacement contient 16 zones. Utilisez un autre emplacement pour le reste."),
     ("SEND stays grey.", "SEND reste gris.",
      "It needs at least one file, a NAME, no root note twice and a size that fits; the FM-1 must be connected.",
      "Il faut au moins un fichier, un NAME, aucune note de base en double et une taille qui tient ; le FM-1 doit être branché."),
     ("The samples are not in the backup file.", "Les échantillons ne sont pas dans le fichier de sauvegarde.",
      "They are: SAMPLE USR1 to USR3 in the BACKUP list (chapter {ch:backup}). Keep your original files too.",
      "Si : SAMPLE USR1 à USR3 dans la liste de BACKUP (chapitre {ch:backup}). Gardez aussi vos fichiers d'origine.")]))
