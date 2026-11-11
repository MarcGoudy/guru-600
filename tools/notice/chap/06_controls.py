# 6 · The FM-1's controls and gestures
CTL2 = [("1", "MASTER", "Overall volume (speaker, headphones and USB audio, unless MENU › AUDIO › USB LEVEL = FIXED).", "Volume général (haut-parleur, casque et audio USB, sauf si MENU › AUDIO › USB LEVEL = FIXED)."),
        ("2", "SELECT", "The tempo by default. Can instead step through the pages, act as the mod wheel, or set the keys' velocity (MENU › CONTROL › SELECT).", "Le tempo, par défaut. Peut aussi faire défiler les pages, servir de molette de modulation ou régler la vélocité des touches (MENU › CONTROL › SELECT)."),
        ("3", "PRESETS", "Changes the selected track's sound. On some pages it moves the cursor or the row instead.", "Change le son de la piste choisie. Sur certaines pages, il déplace le curseur ou la ligne."),
        ("4", "ALGORITHM", "Selects the track, 1 to 4. In the menu: the tab.", "Choisit la piste, de 1 à 4. Dans le menu : l'onglet."),
        ("5", "OCT− / OCT+", "Octave down / up. On action pages, in dialogs and in the menu: back or cancel / confirm.", "Octave inférieure / supérieure. Sur les pages qui exécutent une action, dans les dialogues et dans le menu : retour ou annuler / confirmer."),
        ("6", "KNOB 1–4", "The four settings shown at the top of the screen.", "Les quatre réglages affichés en haut de l'écran."),
        ("7", "FX", "The effects pages. Held: the FX quick screen (performance effects).", "Les pages d'effets. Maintenu : l'écran rapide FX (effets de jeu)."),
        ("8", "SEL", "The scale and chord pages. Held: the SEL quick screen.", "Les pages de gamme et d'accords. Maintenu : l'écran rapide SEL."),
        ("9", "ENV", "The amplifier envelope pages.", "Les pages de l'enveloppe d'amplitude."),
        ("10", "LFO", "The LFO pages and the modulation matrix. Held while turning the knobs: MOMENTARY changes.", "Les pages du LFO et la matrice de modulation. Maintenu avec les boutons rotatifs : changements MOMENTARY."),
        ("11", "EDIT", "The sound engine's pages (for P600: its eleven pages). Held: the EDIT quick screen (engines).", "Les pages du moteur sonore (pour P600 : ses onze pages). Maintenu : l'écran rapide EDIT (moteurs)."),
        ("12", "GLO", "The song page. Held: the GLO quick screen (mutes, solos, levels, tap tempo, MIDI LEARN).", "La page du morceau. Maintenu : l'écran rapide GLO (sourdines, solos, niveaux, tempo tapé, MIDI LEARN)."),
        ("13", "HOME", "Back to HOME; on HOME: MIXER, then CLOCK. Held: the menu.", "Retour à HOME ; sur HOME : MIXER, puis CLOCK. Maintenu : le menu."),
        ("14", "SAVE", "The pages for saving and loading sounds and projects. Held: undo / redo.", "Les pages pour enregistrer et charger sons et projets. Maintenu : annuler / rétablir."),
        ("15", "ARP", "The arpeggiator pages.", "Les pages de l'arpégiateur."),
        ("16", "SEQ", "The sequencer pages. Held: the SEQ TOOLS quick screen.", "Les pages du séquenceur. Maintenu : l'écran rapide SEQ TOOLS."),
        ("17", "PLAY", "Starts / stops the sequencer.", "Lance / arrête le séquenceur."),
        ("18", "REC", "Arms recording on the selected track. Held: the REC quick screen.", "Arme l'enregistrement de la piste choisie. Maintenu : l'écran rapide REC."),
        ("19", ("KEYS", "TOUCHES"), "27 keys, F3 to G5: for playing; in a quick screen, shortcuts.", "27 touches, de F3 à G5 : jouer ; dans un écran rapide, des raccourcis."),
        ("20", ("SCREEN", "ÉCRAN"), "The page, its four settings, the track, the sound and the messages.", "La page, ses quatre réglages, la piste, le son et les messages.")]
GEST_FR = {"OCT− + OCT+ held 5 s": "OCT− + OCT+ maintenus 5 s", "OCT− + OCT+ held at power-on": "OCT− + OCT+ maintenus à l'allumage", "SAVE held at power-on": "SAVE maintenu à l'allumage", "GLO held + PLAY": "GLO maintenu + PLAY", "GLO held + SELECT": "GLO maintenu + SELECT", "GLO held + key D4": "GLO maintenu + touche D4", "LFO held + KNOB 1–4": "LFO maintenu + KNOB 1–4", "FX held + white key held + PRESETS": "FX maintenu + touche blanche maintenue + PRESETS", "Step held + KNOB 1–4": "Pas maintenu + KNOB 1–4", "SAVE held 1 s": "SAVE maintenu 1 s"}
COMBOS = [("OCT− + OCT+", "Back to the middle octave.", "Retour à l'octave du milieu."),
          ("OCT− + OCT+ held 5 s", "Recovery mode (WL80UBOOT, chapter {ch:install}). Let go before 5 s to cancel.", "Mode récupération (WL80UBOOT, chapitre {ch:install}). Relâchez avant 5 s pour annuler."),
          ("OCT− + OCT+ held at power-on", "Hardware calibration (chapter {ch:reset}).", "Calibrage du matériel (chapitre {ch:reset})."),
          ("SAVE held at power-on", "RESET SOUNDS ? (chapter {ch:reset}).", "RESET SOUNDS ? (chapitre {ch:reset})."),
          ("GLO held + PLAY", "RESTART: back to the start without stopping.", "RESTART : retour au début sans arrêter la lecture."),
          ("GLO held + SELECT", "The tempo, whatever SELECT is set to.", "Le tempo, quel que soit le réglage de SELECT."),
          ("GLO held + key D4", "MIDI LEARN on / off (chapter {ch:midi}).", "MIDI LEARN activé / désactivé (chapitre {ch:midi})."),
          ("LFO held + KNOB 1–4", "MOMENTARY: changes that last while LFO is held (chapter {ch:envlfo}).", "MOMENTARY : des changements qui durent tant que LFO est maintenu (chapitre {ch:envlfo})."),
          ("FX held + white key held + PRESETS", "Assigns another effect to that key (chapter {ch:layers}).", "Attribue un autre effet à cette touche (chapitre {ch:layers})."),
          ("Step held + KNOB 1–4", "A parameter lock on that step (chapter {ch:seq}).", "Un verrou de paramètre sur ce pas (chapitre {ch:seq})."),
          ("SAVE held 1 s", "Undo / redo the last load (sound, pattern) or sequence edit.", "Annuler / rétablir le dernier chargement (son, séquence) ou la dernière modification de séquence.")]
CH("controls", "The FM-1's controls and gestures", "Les commandes du FM-1 et les gestes",
 '<figure class="wide"><img src="img/facade_reperes.png" alt=""></figure>' +
 table([("No.", "N°"), ("Control", "Commande"), ("What it does", "Rôle")],
       [[a, f"<b>{b}</b>" if isinstance(b, str) else T(f"<b>{b[0]}</b>", f"<b>{b[1]}</b>"), (c, d)] for a, b, c, d in CTL2]) +
 P2("The <b>USB</b> socket, on the back, carries power, MIDI and audio, and receives the firmware and imported sounds. The MIDI socket (TRS) receives notes and controllers, but not sounds.",
    "La prise <b>USB</b>, à l'arrière, assure l'alimentation, le MIDI et l'audio, et reçoit le firmware et les sons importés. La prise MIDI (TRS) reçoit les notes et les contrôleurs, mais pas les sons.") +
 H3("Tap, hold, double tap", "Appui, maintien, double appui") +
 table([("Gesture", "Geste"), ("On a page button", "Sur un bouton de page")], [
   [("<b>Tap</b>", "<b>Appui</b>"), ("Acts when you let go. From another family: opens that family on the page you last viewed. Already in the family: the next page.", "Agit au relâchement. Depuis une autre famille : ouvre la famille sur la page vue en dernier. Déjà dans la famille : la page suivante.")],
   [("<b>Double tap</b>", "<b>Double appui</b>"), ("Two taps within a third of a second: one page back. On GLO (a single page) and REC: locks their quick screen open.", "Deux appuis en moins d'un tiers de seconde : une page en arrière. Sur GLO (une seule page) et REC : garde leur écran rapide ouvert.")],
   [("<b>Hold</b> (FX, SEL, EDIT, GLO, SEQ, REC)", "<b>Maintien</b> (FX, SEL, EDIT, GLO, SEQ, REC)"), ("After 0.4 s (MENU › CONTROL › HOLD): the quick screen, as long as you hold.", "Après 0,4 s (MENU › CONTROL › HOLD) : l'écran rapide, tant que vous maintenez.")],
   [("<b>Hold for more than 1 s</b> without touching anything else", "<b>Maintien de plus de 1 s</b>, sans rien toucher d'autre"), ("Let go: the quick screen stays open. A tap on its button closes it.", "Relâchez : l'écran rapide reste ouvert. Un appui sur son bouton le ferme.")],
   [("<b>HOME held 1 s</b>", "<b>HOME maintenu 1 s</b>"), ("Opens the menu (it stays open).", "Ouvre le menu (il reste ouvert).")],
   [("<b>SAVE held 1 s</b>", "<b>SAVE maintenu 1 s</b>"), ("Undo; held again: redo.", "Annuler ; maintenu de nouveau : rétablir.")]]) +
 LI([("To go forward several pages, leave a short pause between taps; two taps too close together count as a double tap.",
      "Pour avancer de plusieurs pages, laissez une courte pause entre les appuis ; deux appuis trop rapprochés comptent comme un double appui."),
     ("From the first page of a family, going back takes you to its last page; from the last page, going forward takes you to the first.",
      "Depuis la première page d'une famille, reculer mène à sa dernière page ; depuis la dernière, avancer mène à la première."),
     ("<b>SAVE</b> pressed from another family always opens <b>USER</b>, the page for saving a sound.",
      "<b>SAVE</b> pressé depuis une autre famille ouvre toujours <b>USER</b>, la page qui sert à ranger un son."),
     ("<b>HOME</b> pressed on HOME shows MIXER, then CLOCK, then HOME again. A double tap goes the other way.",
      "<b>HOME</b> pressé sur HOME montre MIXER, puis CLOCK, puis de nouveau HOME. Un double appui parcourt ce cycle dans l'autre sens."),
     ("To change page with SELECT: MENU › CONTROL › <b>SELECT = PAGE</b>. Turn right to go forward, left to go back. The tempo then moves to GLO + SELECT and HOME › CLOCK.",
      "Pour changer de page avec SELECT : MENU › CONTROL › <b>SELECT = PAGE</b>. Tournez à droite pour avancer, à gauche pour reculer. Le tempo passe alors à GLO + SELECT et à HOME › CLOCK.")]) +
 H3("OCT− and OCT+", "OCT− et OCT+") +
 P2("On ordinary pages they shift the keyboard by octaves (−3 to +3) as soon as pressed; their light is lit away from the middle octave. Elsewhere they act when you let go:",
    "Sur les pages ordinaires, ils déplacent le clavier par octaves (−3 à +3), dès l'appui ; leur voyant s'allume hors de l'octave du milieu. Ailleurs, ils agissent au relâchement :") +
 LI([("<b>Action pages</b> (save, load, erase, MORPH's MUTATE, LEARN…): <b>OCT+</b> performs the action; <b>OCT−</b> cancels it, and a second press returns to HOME (on PHRASES, SONG and AUTOMATION, OCT− goes straight to HOME). On these pages the octave does not change.",
      "<b>Pages qui exécutent une action</b> (enregistrer, charger, effacer, MUTATE de MORPH, LEARN…) : <b>OCT+</b> fait l'action ; <b>OCT−</b> l'abandonne, et un second appui ramène à HOME (sur PHRASES, SONG et AUTOMATION, OCT− ramène directement à HOME). Sur ces pages, l'octave ne change pas."),
     ("<b>Dialogs</b> (ERASE U01?, SAVE IN PLACE 5?…): <b>OCT+</b> = YES, <b>OCT−</b> = NO. Until you answer, only the keys respond (they play).",
      "<b>Dialogues</b> (ERASE U01?, SAVE IN PLACE 5?…) : <b>OCT+</b> = OUI, <b>OCT−</b> = NON. Tant que vous n'avez pas répondu, seules les touches répondent (elles jouent)."),
     ("<b>Quick screens</b> GLO, SEL, EDIT, SEQ and REC: <b>OCT−</b> undoes everything changed in the quick screen since it opened.",
      "<b>Écrans rapides</b> GLO, SEL, EDIT, SEQ et REC : <b>OCT−</b> annule tout ce que l'écran rapide a modifié depuis son ouverture."),
     ("<b>Menu</b>: moves the value one step down / up.", "<b>Menu</b> : diminue / augmente la valeur d'un cran."),
     ("A <b>breathing</b> OCT+ light means OCT+ would do something now.", "Un voyant OCT+ qui <b>respire</b> signifie qu'OCT+ ferait quelque chose maintenant.")]) +
 H3("The knobs", "Les boutons rotatifs") +
 LI([("<b>KNOB 1 to 4</b> change the four settings shown. On an action page, turn the action card's knob right to select the action, left to cancel it, then press OCT+.",
      "<b>KNOB 1 à 4</b> changent les quatre réglages affichés. Sur une page qui exécute une action, tournez le bouton de la carte de l'action à droite pour la choisir, à gauche pour l'abandonner, puis appuyez sur OCT+."),
     ("MENU › CONTROL › <b>KNOB ACCEL</b> ON: a fast turn on a setting with many values moves 2 to 8 times faster.",
      "MENU › CONTROL › <b>KNOB ACCEL</b> sur ON : un tour rapide sur un réglage à nombreuses valeurs avance 2 à 8 fois plus vite."),
     ("<b>ALGORITHM</b> selects tracks 1 to 4, one per step, without wrapping around. It does nothing while a quick screen is held.",
      "<b>ALGORITHM</b> choisit les pistes 1 à 4, une par cran, sans boucler. Il ne fait rien tant qu'un écran rapide est maintenu."),
     ("<b>PRESETS</b> changes the track's sound, except: on STEP, DETAIL, AUTOMATION, SONG, USER, PHRASES and PROJECT it moves the cursor, the row or the slot, like KNOB 1; on TOOLS and SLICES it does nothing. On SAVE › PLACE it changes the sound too: choose the place with KNOB 1 only.",
      "<b>PRESETS</b> change le son de la piste, sauf : sur STEP, DETAIL, AUTOMATION, SONG, USER, PHRASES et PROJECT, il déplace le curseur, la ligne ou l'emplacement, comme KNOB 1 ; sur TOOLS et SLICES, il ne fait rien. Sur SAVE › PLACE, il change aussi le son : choisissez la place avec KNOB 1 seulement."),
     ("<b>SELECT</b>: the tempo (40 to 240 BPM) by default. With MENU › CONTROL › <b>BPM LOCK</b> ON, SELECT no longer changes the tempo (BPM LOCKED): set it with GLO held, on HOME › CLOCK, or with GLO's TAP key.",
      "<b>SELECT</b> : le tempo (40 à 240 BPM) par défaut. Avec MENU › CONTROL › <b>BPM LOCK</b> sur ON, SELECT ne change plus le tempo (BPM LOCKED) : réglez-le avec GLO maintenu, sur HOME › CLOCK, ou avec la touche TAP de GLO.")]) +
 H3("The keys", "Les touches") +
 LI([("27 keys, from F3 to G5 at the middle octave. Without a MIDI keyboard they play at a fixed velocity of 100; MENU › CONTROL › SELECT = <b>VEL</b> lets SELECT set it (1 to 127); it goes back to 100 at each power-on.",
      "27 touches, de F3 à G5 à l'octave du milieu. Sans clavier MIDI, elles jouent à une vélocité fixe de 100 ; MENU › CONTROL › SELECT = <b>VEL</b> permet de la régler avec SELECT (1 à 127) ; elle revient à 100 à chaque allumage."),
     ("A MIDI sustain pedal (CC 64) works.",
      "Une pédale de maintien MIDI (CC 64) fonctionne."),
     ("A key pressed while a quick screen's button is held is a shortcut: silent, never recorded.",
      "Une touche pressée pendant que vous maintenez le bouton d'un écran rapide est un raccourci : muette, jamais enregistrée.")]) +
 H3("Every combination", "Toutes les combinaisons") +
 table([("Gesture", "Geste"), ("Effect", "Effet")], [[T(f"<b>{a}</b>", f"<b>{GEST_FR.get(a, a)}</b>"), (b, c)] for a, b, c in COMBOS]) +
 H3("The lights", "Les voyants") +
 LI([("<b>Lit</b>: in effect now. <b>Breathing</b> (slowly brighter and dimmer): available, you can press it. <b>Dark</b>: nothing available. MENU › DISPLAY › LEDS changes the style.",
      "<b>Allumé</b> : actif maintenant. <b>Qui respire</b> (s'éclaire et s'atténue lentement) : disponible, vous pouvez appuyer. <b>Éteint</b> : rien de disponible. MENU › DISPLAY › LEDS change le style."),
     ("While the sequencer plays, PLAY's own light goes dark and the green light is lit; during a count-in the green light flashes on each beat.",
      "Pendant que le séquenceur joue, le voyant de PLAY s'éteint et le voyant vert s'allume ; pendant un décompte, le voyant vert clignote à chaque temps."),
     ("REC is lit while a track is armed.", "REC est allumé tant qu'une piste est armée.")]) +
 felucca("Controls", "Felucca's controls page lists the buttons and gestures of the original firmware.",
         "La page des commandes de Felucca liste les boutons et gestes du firmware d'origine."))
