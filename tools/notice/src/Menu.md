# Menu

Hold **HOME** for the menu, in five tabs: **DISPLAY** (COLOR, STYLE, LARGE, ANIM, LEDS, SCREEN OFF, SCOPE, HOME),
**CONTROL** (HOLD, KNOB ACCEL, FX LATCH, BPM LOCK, SCALE LEDS, STEP PREVIEW, CHORD ENTRY, SELECT), **AUDIO** (SPEAKER EQ,
USB LEVEL, CLICK, CLICK LEVEL, COUNT-IN, TUNE), **MIDI** (MIDI IN, T1–T4 CHANNEL, AUTO SELECT, SCREEN WAKE, LEARN CLEAR)
and **SYSTEM** (USB SERIAL,
RESTORE LAST, HELP, HARDWARE CALIBRATION, INFO, ABOUT).
ALGORITHM moves between the tabs and PRESETS through the rows of one; any of KNOB 1–4, or OCT+ / OCT−,
changes the value (OCT+ opens HARDWARE CALIBRATION, INFO and ABOUT); press HOME to close the menu. Every new
setting defaults to the earlier behaviour. The web editor's Settings tab reads and changes them too, saved the same
way as from the menu, in the same tabs.

- **COLOR:** the palette. GREY (grayscale, called MONO up to 1.0.1), GREEN, AMBER, ICE, VIOLET, ROSE,
  PAPER (light), HI-CON (high contrast), NIGHT (the 0.9 look: true black, green-tinted text) and MONO
  (black and white). 1.6: **CUSTOM** while one is stored: five colours (BG, SURF, TEXT, THEME, ACCENT) set in the
  [web editor](https://hugelton.github.io/Felucca/webapp/editor/) under Settings > Custom palette (a live preview on the
  FM-1); the rest of the colours are derived from them. Part of the settings, not of projects. Hard to read colours get
  a warning in the editor, nothing more; hold HOME for the menu and COLOR (the first row of DISPLAY) takes you back to a
  built-in palette
- **STYLE:** FLAT (filled cards) or LINE (areas divided by thin lines)
- **LARGE:** OFF or ON: on HOME and the value pages the four knob cards grow tall, marked K1–K4, with
  larger labels and values about twice the size; the graph below becomes a strip. Lists, the piano roll,
  the drum grid and the quick layers keep their layout with larger labels
- **ANIM:** ON, OFF or IDLE. OFF shows every change at once, without rolling digits, a gliding piano roll or
  the LED sweep at power-on. IDLE is ON plus a gentle LED animation after a minute without input: a soft light drifts
  over the keys and the buttons breathe; any key, button or knob ends it and does what it always does. It never runs
  while playing, with a track armed, in a layer, the menu or a dialog
- **LEDS:** OFF (no glow), DIM LO, DIM HI (default), INV (the idle LEDs lit, the active ones dark), INV LO or INV HI
  (INV with the lit LEDs at a steady low level, about 1/12 or 1/8 of full, for a dark room).
  What can be pressed breathes up to about 60 % of a lit LED, about 30 % with DIM LO
- **SCREEN OFF:** NEVER (default), 5 MIN, 15 MIN, 30 MIN or 60 MIN: after that long with no button, key or knob
  touched, the screen goes dark; the sound, the sequencer, MIDI and USB go on. The backlight stays on (on the FM-1
  its line also enables the buttons and keys). The next button, key or knob only turns the screen back on; a MIDI
  note turns it on too and plays (SCREEN WAKE)
- **SCOPE:** OUT (default) or MIX: what HOME's oscilloscope shows. OUT the sound after MASTER (the picture shrinks
  with the volume), MIX the mix before MASTER, the same size at any volume
- **HOME:** SCOPE (default), TRACKS or LEVELS: under HOME's four cards, the oscilloscope or the four tracks, a row
  each with its sound, its steps playing, MUTE and a meter. With TRACKS only the look changes; with LEVELS KNOB 1–4
  set the LEVEL of T1–T4 (the engine's main parameters are on EDIT)
- **HOLD:** how long a layer's button is held before its map shows
- **KNOB ACCEL:** OFF (one step per click) or ON: a fast, steady turn of a wide value moves 2 to 4 steps
  per click, up to 8 on values of more than 64 steps, the FX and GLO layers' knobs included; lists never
  jump. ON or OFF, every click of a fast turn counts
- **FX LATCH:** ON, FX + an effect key turns the effect on until pressed again, the knob macros stay
  where you leave them, and FX + OCT− turns everything off
- **BPM LOCK:** ON, SELECT no longer changes the tempo; hold GLO and turn SELECT, tap F4 in the GLO
  layer or use HOME > CLOCK instead
- **SCALE LEDS:** OFF or ON: the keys show the selected track's scale all the time (the root a little
  brighter); not on DRUM or SLICE tracks
- **STEP PREVIEW:** OFF (default) or ON: on SEQ > STEP with the transport stopped, moving the cursor plays the step
  it lands on once (its notes or hits, through the track's sound)
- **CHORD ENTRY:** HOLD (default) or ADD: how step recording writes. HOLD: the keys held together become the step,
  letting go moves on. ADD: each key adds its note to the step, up to 4 (a key whose note is there takes it out),
  and KNOB 1 moves on, so a chord goes in one finger at a time
- **SELECT:** BPM (default), PAGE, MODW or VEL. PAGE: turning SELECT steps the pages of the family shown, as a tap
  of its button does (left goes back). MODW: SELECT is the selected track's mod wheel (as MIDI CC1, sent out too).
  VEL: SELECT sets the velocity the keys play at (1–127). With any but BPM the tempo is GLO + SELECT, HOME > CLOCK or
  GLO's TAP
- **SPEAKER EQ:** FLAT, LOWCUT or BASS+, a tone setting for the built-in speaker (not a switch). It also
  shapes the headphone out and USB audio, so keep it on FLAT when recording. The firmware cannot turn
  the speaker off, but headphones in the jack do
- **USB LEVEL:** MASTER (the MASTER knob sets the USB audio level too) or FIXED (USB always at full
  level, MASTER sets only the speaker and headphones)
- **CLICK:** OFF (default), REC (while a track is armed) or ON: a click on every beat while playing, the
  bar's first beat higher. **CLICK LEVEL:** LOW, MID (default) or HIGH; MASTER sets it too
- **COUNT-IN:** OFF (default), 1 BAR or 2 BARS: with a track armed, PLAY counts in first (clicking even with
  CLICK OFF), and a note played in the last half beat lands on step 1. Not with an external clock
- **TUNE:** the global tuning, −50 to +50 cents. It is the project's, saved and loaded with it
- **MIDI IN:** CH1-4 (default), SEL, CH5-8, CH9-12, CH13-16 or TRACK (see MIDI above). The project's too
- **T1–T4 CHANNEL:** with MIDI IN TRACK, each track's channel: 1–16, OMNI (any channel no other track has) or OFF;
  1–4 until changed (dim while MIDI IN is something else). The project's too
- **AUTO SELECT:** OFF (default) or ON: a MIDI note into another track makes it the selected one
- **SCREEN WAKE:** +MIDI (default) or PANEL: whether MIDI notes keep the screen on and wake it (SCREEN OFF)
- **LEARN CLEAR:** how many CCs MIDI LEARN has set (NONE, 1 CC … 16 CC); OCT+ clears them all
- **USB SERIAL:** ON or OFF, applied when the menu closes (the FM-1 reconnects). OFF leaves out the
  serial console, a developer tool, so the FM-1 is a plain audio + MIDI device; this lets macOS 13–15
  see its USB audio input. MIDI, the editor and the installer work either way
- **RESTORE LAST:** ON (default) or OFF. ON, the FM-1 starts with the music you left (the header says
  RESTORED), kept in an autosave apart from the four projects; it is written when the music changed, the
  transport is stopped and nothing has been touched for 10 s, at most once a minute. OFF starts with the
  power-on sounds
- **HELP:** OFF (default) or ON: a short hint in the footer for about 2 s when a page opens, and under a quick
  layer's map while it shows
- **HARDWARE CALIBRATION**, **INFO** (the version, the USB link and the CPU load) and **ABOUT**
