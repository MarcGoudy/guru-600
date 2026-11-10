# 11 · PROJECTS: the four projects and the 32 USER sounds
CH("projects", "PROJECTS: projects and USER sounds", "PROJECTS : projets et sons USER",
 P2("The PROJECTS page keeps your music in the FM-1: four <b>projects</b>, A to D, and 32 <b>USER sounds</b>.",
    "La page PROJECTS garde votre musique dans le FM-1 : quatre <b>projets</b>, A à D, et 32 <b>sons USER</b>.") +
 SHOT("projects", "The PROJECTS page: the projects on the left, the USER sounds on the right.",
      "La page PROJECTS : les projets à gauche, les sons USER à droite.") +
 H3("The projects A to D", "Les projets A à D", EDC["projects"]) +
 P2("A project holds the whole music: the four tracks with their sounds, steps and automation, the mix and the song. "
    "Each slot shows SAVED or EMPTY. The SONG page plays its sections from these four slots (chapter {ch:song}).",
    "Un projet contient toute la musique : les quatre pistes avec leurs sons, leurs pas et leurs automations, le mixage et le morceau. "
    "Chaque emplacement indique SAVED ou EMPTY. La page SONG joue ses sections depuis ces quatre emplacements (chapitre {ch:song}).") +
 LI([("<b>SAVE</b>: saves the music as it is now in that slot. A slot already SAVED asks before it is replaced.",
      "<b>SAVE</b> : enregistre la musique telle qu'elle est dans cet emplacement. Un emplacement déjà SAVED demande confirmation avant d'être remplacé."),
     ("<b>LOAD</b>: replaces the music of the moment with that project, after a confirmation. Grey on an EMPTY slot.",
      "<b>LOAD</b> : remplace la musique du moment par ce projet, après confirmation. Gris sur un emplacement EMPTY.")]) +
 BOX("note", ("The music of the moment is kept by the FM-1 at power-off (RESTORE LAST, chapter {ch:settings}), but a project is the safe copy: save it before trying something new.",
              "La musique du moment est gardée par le FM-1 à l'extinction (RESTORE LAST, chapitre {ch:settings}), mais un projet en est la copie sûre : enregistrez-le avant d'essayer autre chose.")) +
 H3("The USER sounds", "Les sons USER", EDC["projects"]) +
 P2("A USER sound is one track's sound with its 16-step pattern, kept under a name, whatever its engine. "
    "The list shows the 32 places: number, engine and name; — is an empty place. Click a place to choose it.",
    "Un son USER est le son d'une piste avec son motif de 16 pas, gardé sous un nom, quel que soit son moteur. "
    "La liste montre les 32 places : numéro, moteur et nom ; — est une place vide. Cliquez sur une place pour la choisir.") +
 CTL([("STORE THE TRACK'S SOUND", "Keeps the sound of the selected track (TRACK 1 to 4, at the top) in the chosen place. Type its name (12 characters at most) and confirm. A place in use asks before it is replaced.",
       "Garde le son de la piste choisie (TRACK 1 à 4, en haut) dans la place choisie. Tapez son nom (12 caractères au plus) et confirmez. Une place occupée demande confirmation avant d'être remplacée."),
      ("LOAD", "Loads the chosen USER sound on the selected track. A double click on a place does the same. If the track's sound was changed and not saved, the editor asks first.",
       "Charge le son USER choisi sur la piste choisie. Un double clic sur une place fait de même. Si le son de la piste a été modifié sans être enregistré, l'éditeur demande d'abord."),
      ("ERASE", "Empties the chosen place, after a confirmation.", "Vide la place choisie, après confirmation.")]) +
 P2("For a P600 sound, SAVE TO THIS PLACE on the SOUND page (chapter {ch:sound}) keeps it among the 255 P600 places; a USER sound keeps it with its pattern, for any engine.",
    "Pour un son P600, SAVE TO THIS PLACE sur la page SOUND (chapitre {ch:sound}) le garde parmi les 255 places du P600 ; un son USER le garde avec son motif, quel que soit le moteur.") +
 QA([("The FM-1 could not save (stop the music first).", "Le FM-1 n'a pas pu enregistrer (arrêtez d'abord la musique).",
      "Click ■, then SAVE again.", "Cliquez sur ■, puis de nouveau sur SAVE."),
     ("Loaded the wrong project.", "Mauvais projet chargé.",
      "The music of the moment is replaced: if it was saved in a project, load that project again. Otherwise it is lost.",
      "La musique du moment est remplacée : si elle était enregistrée dans un projet, rechargez ce projet. Sinon, elle est perdue."),
     ("Do the projects leave the FM-1?", "Les projets peuvent-ils sortir du FM-1 ?",
      "Yes: a backup holds all four, with everything else (chapter {ch:backup}).",
      "Oui : une sauvegarde contient les quatre, avec tout le reste (chapitre {ch:backup}).")]))
