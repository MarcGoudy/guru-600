// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: what the panel does. Every control works on its own (the values here); with an FM-1 connected
// (guru-link.js) each change goes to it and its changes come back.
"use strict";

let curEng = 14, curPre = 0;          // the selected track's engine and preset (the sounds' list: guru-allsounds.js)
/* ------------------------------------------------------------------------------------- the values --- */
const clampD = (id, v) => Math.max(D[id].min, Math.min(D[id].max, Math.round(v)));
let dev = null;                        // the connected FM-1 (guru-link.js Device), or null
const sending = new Map();             // id -> {v: the value to send, busy}
function setVal(id, v, from = "user") {
  v = clampD(id, v);
  if (val[id] === v) return;
  val[id] = v;
  render(id);
  if (from === "user") { if (!notSound.has(+id)) dirty = true; send(id); }
}
function send(id) {   // (ids from 1000: the globals, G_* = id - 1000)
  if (!dev) return;
  const s = sending.get(id) || { busy: false };
  s.v = val[id]; sending.set(id, s);
  if (s.busy) return;
  s.busy = true;
  (async () => {
    while (true) {
      const v = s.v;
      try { const got = await (id >= 1000 ? dev.set(id - 1000, v, 1) : dev.set(id, v)); if (s.v === v && got !== v) { val[id] = got; render(id); } } catch (e) { console.warn(e); }
      if (s.v === v) break;
    }
    s.busy = false;
  })();
}
let dirty = false;                     // the sound changed since it was loaded or saved
const notSound = new Set();            // parameters that are not the sound's (the sequencer's, the globals): no "unsaved" 

const keysEl = document.getElementById("keys");

/* ---------------------------------------------------------------------------------------- knobs --- */
// drag up / down (Shift: finer), the wheel, a double click: the default
function knobDrag(el, get, put, span, def) {
  let y0 = 0, v0 = 0, acc = 0;
  el.addEventListener("pointerdown", (e) => {
    e.preventDefault(); el.setPointerCapture(e.pointerId); y0 = e.clientY; v0 = get(); acc = 0; 
  });
  el.addEventListener("pointermove", (e) => {
    if (!el.hasPointerCapture(e.pointerId)) return;
    const s = stage.getBoundingClientRect().width / stage.offsetWidth;   // the stage's scale
    const dy = (y0 - e.clientY) / s, k = e.shiftKey ? 0.15 : 1;
    acc = dy * k * span / 180;
    put(v0 + acc);
  });
  el.addEventListener("wheel", (e) => { e.preventDefault(); put(get() + (e.deltaY < 0 ? 1 : -1) * Math.max(1, Math.round(span / 64))); }, { passive: false });
  el.addEventListener("dblclick", () => { put(def); });
}
function bindCtl(c) {   // (a page made later binds its own: guru-seq.js ...)
  const d = D[c.id];
  if (c.kind === "knob") {
    if (c.inv) knobDrag(c.svg, () => d.max - val[c.id], (x) => setVal(c.id, d.max - x), d.max - d.min, d.max - d.def);
    else if (d.order) {   // (values shown in the device's order, longest note first: params.c DIV_ORDER ...)
      const n = d.max - d.min;
      knobDrag(c.svg, () => d.order.indexOf(val[c.id] - d.min), (x) => setVal(c.id, d.min + d.order[Math.max(0, Math.min(n, Math.round(x)))]),
        n, d.order.indexOf(d.def - d.min));
    } else knobDrag(c.svg, () => val[c.id], (x) => setVal(c.id, x), d.max - d.min, d.def);
  } else if (c.kind === "sw") {
    c.el.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      const v = val[c.id];
      setVal(c.id, c.lfo ? (v ? 0 : 63) : c.bit ? v ^ c.bit : (v ? 0 : 1));
    });
  } else if (c.kind === "radio") {
    c.el.addEventListener("pointerdown", (e) => { e.preventDefault(); setVal(c.id, c.v); });
  } else if (c.kind === "shape") {
    c.el.addEventListener("pointerdown", (e) => { e.preventDefault(); setVal(c.id, val[c.id] === 3 ? 1 : 3); });   // TRI 1, SQR 3
  } else if (c.kind === "unison") {
    c.el.addEventListener("pointerdown", (e) => { e.preventDefault(); setVal(c.id, val[c.id] === 3 ? 0 : 3); });   // UNI 3, POLY 0
  } else if (c.kind === "selb") {
    c.el.addEventListener("pointerdown", (e) => { e.preventDefault(); setVal(c.id, c.v); });
  } else if (c.kind === "fld") {   // the field's arrows: one step (round the list)
    const step = (k) => { const n = d.max - d.min + 1; setVal(c.id, d.min + ((val[c.id] - d.min + k + n) % n)); };
    c.l.addEventListener("pointerdown", (e) => { e.preventDefault(); step(-1); });
    c.r.addEventListener("pointerdown", (e) => { e.preventDefault(); step(1); });
    c.el.addEventListener("wheel", (e) => { e.preventDefault(); step(e.deltaY < 0 ? 1 : -1); }, { passive: false });
  }
}
ctl.forEach(bindCtl);

/* ---------------------------------------------------------------------------------------- BPM --- */
const G_BPM = 0;
let bpm = 120;
const bpmEl = document.getElementById("bpm");
function showBpm() { bpmEl.textContent = bpm; }
function setBpm(v, from = "user") {
  v = Math.max(40, Math.min(240, Math.round(v)));
  if (v === bpm) return;
  bpm = v; showBpm();
  if (from === "user" && dev) dev.set(G_BPM, v, 1).catch((e) => console.warn(e));
}
knobDrag(bpmEl, () => bpm, (x) => setBpm(x), 200, 120);
for (const [id, d] of [["bpm+", 1], ["bpm-", -1]]) {   // the arrows: a step a click, held: faster and faster
  const el = document.getElementById(id);
  let t = 0;
  const stop = () => clearTimeout(t);
  el.addEventListener("pointerdown", (e) => {
    e.preventDefault(); setBpm(bpm + d);
    let wait = 400;
    const again = () => { setBpm(bpm + d); wait = Math.max(40, wait * 0.8); t = setTimeout(again, wait); };
    t = setTimeout(again, wait);
  });
  el.addEventListener("pointerup", stop); el.addEventListener("pointerleave", stop); el.addEventListener("pointercancel", stop);
}

/* the beat: the BPM box flashes on each beat, more on the first; the flash fades in most of a beat */
let lastBeat = -1;
function showBeat(playing, b) {
  if (!playing) { lastBeat = -1; bpmEl.classList.remove("b", "b1"); return; }
  if (b === lastBeat) return;
  lastBeat = b;
  bpmEl.style.setProperty("--bt", Math.min(0.45, 0.8 * 60 / bpm) + "s");
  bpmEl.classList.remove("b", "b1"); void bpmEl.offsetWidth;   // (the animation from its start again)
  bpmEl.classList.add(b === 0 ? "b1" : "b");
}

/* -------------------------------------------------------------------------------------- MORPH --- */
let morph = { b: 11, pos: 40, amt: 40 };       // B: place 12; MUTATE's amount 1..127
let morphShown = null, morphGlide = 0;          // the thumb gliding to a position read on the FM-1 (pollMorph)
const slider = document.getElementById("slider");
function showMorph(at) {                       // at: where the thumb is drawn (pollMorph: it glides from there)
  if (at == null) { if (morphGlide) cancelAnimationFrame(morphGlide); morphGlide = 0; morphShown = null; }
  setMorph((at ?? morph.pos) / 100);
  if (at != null) document.getElementById("mpos").textContent = morph.pos + " %";
  document.getElementById("fb").textContent = placeLabel(morph.b);
  document.getElementById("mamt").textContent = Math.round(morph.amt * 100 / 127) + " %";
  drawKnob(document.getElementById("mknob"), (morph.amt - 1) / 126);
}
let morphBusy = false, morphWant = null, morphTouch = 0, morphPolling = false;
async function sendMorph() {
  if (!dev) return;
  morphTouch = Date.now();
  morphWant = morph.pos;
  if (morphBusy) return;
  morphBusy = true;
  while (morphWant != null) { const p = morphWant; morphWant = null; try { await dev.morph(morph.b, p); } catch (e) { console.warn(e); } }
  morphBusy = false;
}
slider.addEventListener("pointerdown", (e) => { slider.setPointerCapture(e.pointerId); moveMorph(e); });
slider.addEventListener("pointermove", (e) => { if (slider.hasPointerCapture(e.pointerId)) moveMorph(e); });
function moveMorph(e) {
  const r = slider.getBoundingClientRect(), pos = Math.round(Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * 100);
  if (pos === morph.pos) return;
  morph.pos = pos; showMorph(); dirty = true; sendMorph();
}
knobDrag(document.getElementById("mknob"), () => morph.amt, (x) => { morphTouch = Date.now(); morph.amt = Math.max(1, Math.min(127, Math.round(x))); showMorph(); }, 126, 40);
// MORPH turned on the FM-1 (KNOB1..4 of EDIT > MORPH): read back continuously, except while the editor's own MORPH
// controls are in use; when the mix moved, the knobs are read again (the morphed sound's values)
async function pollMorph() {
  if (!dev || morphPolling || morphBusy || morphWant != null || Date.now() - morphTouch < 1500) return;
  morphPolling = true;
  try {
    const m = await dev.morphState();
    if (morphBusy || morphWant != null || Date.now() - morphTouch < 1500) return;
    const amt = m.amt || morph.amt, moved = m.pos !== morph.pos || m.b !== morph.b;
    if (!moved && amt === morph.amt) return;
    const from = morphShown ?? morph.pos;
    morph.b = m.b; morph.pos = m.pos; morph.amt = amt;
    if (!moved) return showMorph();
    showMorph(from);                             // (B and the amount at once; the thumb glides)
    glideMorph(from); dirty = morph.pos > 0; morphReloadSoon();
  } catch (e) {} finally { morphPolling = false; }
}
// the thumb glides to the position read (no jump from one reading to the next)
function glideMorph(from) {
  morphShown = from;
  if (morphGlide) return;
  const step = () => {
    const d = morph.pos - morphShown;
    morphShown = Math.abs(d) < 0.3 ? morph.pos : morphShown + d * 0.35;
    setMorph(morphShown / 100);
    document.getElementById("mpos").textContent = morph.pos + " %";
    morphGlide = morphShown === morph.pos ? 0 : requestAnimationFrame(step);
  };
  morphGlide = requestAnimationFrame(step);
}
// the morphed sound's knobs: read again at most every 80 ms, and only the ones that changed are painted again
let morphReload = 0;
function morphReloadSoon() {
  if (morphReload) return;
  morphReload = setTimeout(async () => {
    try {
      if (dev) {
        const d = await dev.dump(dev.info.pcount);
        for (const id in D) {
          if (d.p[id] == null) continue;
          const v = clampD(id, d.p[id]);
          if (v !== val[id]) { val[id] = v; render(id); }
        }
      }
    } catch (e) {}
    morphReload = 0;
  }, 80);
}
// SOUND B: another B, the rail where it was (the sound mixed again at that place)
document.getElementById("fb-").addEventListener("click", () => { morph.b = (morph.b + 254) % 255; showMorph(); if (morph.pos) { dirty = true; sendMorph(); } });
document.getElementById("fb+").addEventListener("click", () => { morph.b = (morph.b + 1) % 255; showMorph(); if (morph.pos) { dirty = true; sendMorph(); } });
document.getElementById("b-mutate").addEventListener("click", async () => {
  if (!dev) return toast(tx("offline"));
  try { await dev.mutate(morph.amt); morph.pos = 0; showMorph(); dirty = true; await reloadValues(); } catch (e) { toast(tx("noreply")); }
});

/* ------------------------------------------------------------------------------------- the sounds --- */
const names = SOUND_NAMES.map((n) => ({ name: n, kept: false }));
while (names.length < 255) names.push({ name: "SOUND " + (names.length + 1), kept: false });
names[2].kept = true;
let place = 0, family = -1;
const bare = (s) => String(s || "").replace(/^\d+\s*/, "");   // "12 BRASS I" -> "BRASS I"
const placeLabel = (i) => (i + 1) + " " + (names[i] ? bare(names[i].name) : "");
const rows = [...document.querySelectorAll("#list .row")];
function showSounds(scroll) {
  rows.forEach((r, i) => {
    r.classList.toggle("on", i === place && curEng === 14);
    r.classList.toggle("kept", names[i].kept);
    r.classList.toggle("hide", family >= 0 && +FAMILY_OF[i] !== family);
    r.querySelector(".nm").textContent = bare(names[i].name);
  });
  document.getElementById("fa").textContent = placeLabel(place);
  document.getElementById("b-orig").classList.toggle("dis", !names[place].kept);
  if (scroll) rows[place].scrollIntoView({ block: "nearest" });
  showMorph();
}
document.querySelectorAll("#chips .chip").forEach((c) => c.addEventListener("pointerdown", () => {
  family = +c.dataset.f;
  document.querySelectorAll("#chips .chip").forEach((o) => o.classList.toggle("on", o === c));
  showSounds();
}));
rows.forEach((r, i) => r.addEventListener("pointerdown", () => choose(i)));
async function choose(i) {
  if (dirty && dev && i !== place && !await uiConfirm(tx("lose"))) return;
  place = i; dirty = false; showSounds(true);
  if (dev) { try { await dev.load(i); await reloadValues(); } catch (e) { toast(tx("noreply")); } }
}
// MORPH's SOUND A: another A at the same place of the rail (the firmware's mph_set takes the sound loaded as A and
// mixes it with B there again); no question: MORPH is for trying sounds
async function chooseA(i) {
  place = i; showSounds(true);
  if (!dev) return;
  try {
    await dev.load(i);
    if (morph.pos) await dev.morph(morph.b, morph.pos);
    dirty = morph.pos > 0;
    await reloadValues();
  } catch (e) { toast(tx("noreply")); }
}
document.getElementById("fa-").addEventListener("click", () => chooseA((place + 254) % 255));
document.getElementById("fa+").addEventListener("click", () => chooseA((place + 1) % 255));

/* ---------------------------------------------------------------------------------- the keyboard --- */
let octave = 0;                        // OCT- / OCT+: -2 .. +2 (the lowest key C3 at 0)
const BASE = 48;
const held = new Map();                // a pointer or a computer key -> the note it holds
// DRUM and SLICE map the FM-1's keys their own way (firmware drum_keys: 29 + key, slice_keys: 60 + key; the others 53 + key):
// the same key here as there, its note shifted (Marc, 10/11: the octave was off on these sounds)
const KEY_SHIFT = { 10: 24, 13: -7 };
const keyShift = () => KEY_SHIFT[curEng] || 0;
const sentNote = new Map();             // a key's note -> [channel, note] sent (its note-off the same, whatever changed meanwhile)
function noteOn(n) {
  const k = keysEl.querySelector(`[data-n="${n - BASE - 12 * octave}"]`); if (k) k.classList.add("dn");
  const s = [track, (n - keyShift()) & 127]; sentNote.set(n, s);
  if (dev) dev.link.out.send([0x90 | s[0], s[1], 100]);
}
function noteOff(n) {
  const k = keysEl.querySelector(`[data-n="${n - BASE - 12 * octave}"]`); if (k) k.classList.remove("dn");
  const s = sentNote.get(n) || [track, (n - keyShift()) & 127]; sentNote.delete(n);
  if (dev) dev.link.out.send([0x80 | s[0], s[1], 0]);
}
function keysDrawn() {   // (index.html drawKeys, after a resize): the keys still held lit again
  for (const n of [...held.values(), ...far]) { const k = keysEl.querySelector(`[data-n="${n - BASE - 12 * octave}"]`); if (k) k.classList.add("dn"); }
}
// the notes played on the FM-1's keys (its MIDI OUT, the selected track's channel): lit as if held here
const far = new Set();
function farNote(ch, n, vel) {
  if (ch !== track) return;
  n += keyShift();
  if (vel) far.add(n); else far.delete(n);
  const k = keysEl.querySelector(`[data-n="${n - BASE - 12 * octave}"]`);
  if (k && ![...held.values()].includes(n)) k.classList.toggle("dn", !!vel);
}
function farClear() {   // (another track, another octave, the FM-1 gone: the lit notes no longer stand)
  for (const n of far) { const k = keysEl.querySelector(`[data-n="${n - BASE - 12 * octave}"]`); if (k && ![...held.values()].includes(n)) k.classList.remove("dn"); }
  far.clear();
}
const keyAt = (e) => { const t = document.elementFromPoint(e.clientX, e.clientY); return t && t.dataset && t.dataset.n != null && keysEl.contains(t) ? +t.dataset.n : null; };
keysEl.addEventListener("pointerdown", (e) => {
  const k = keyAt(e); if (k == null) return;
  e.preventDefault(); keysEl.setPointerCapture(e.pointerId);
  const n = BASE + 12 * octave + k; held.set("p" + e.pointerId, n); noteOn(n);
});
keysEl.addEventListener("pointermove", (e) => {   // a glide over the keys
  const id = "p" + e.pointerId; if (!held.has(id)) return;
  const k = keyAt(e); if (k == null) return;
  const n = BASE + 12 * octave + k; if (n === held.get(id)) return;
  noteOff(held.get(id)); held.set(id, n); noteOn(n);
});
const release = (e) => { const id = "p" + e.pointerId; if (held.has(id)) { noteOff(held.get(id)); held.delete(id); } };
keysEl.addEventListener("pointerup", release);
keysEl.addEventListener("pointercancel", release);
// the computer's keys: A W S E D F T G Y H U J K O L P ; (QWERTY places: the same keys on an AZERTY keyboard by their code)
const KEYCODES = ["KeyA", "KeyW", "KeyS", "KeyE", "KeyD", "KeyF", "KeyT", "KeyG", "KeyY", "KeyH", "KeyU", "KeyJ", "KeyK", "KeyO", "KeyL", "KeyP", "Semicolon"];
addEventListener("keydown", (e) => {
  if (e.repeat || e.metaKey || e.ctrlKey || e.altKey || e.target.closest("input, textarea, [contenteditable]")) return;
  const i = KEYCODES.indexOf(e.code);
  if (e.code === "ArrowLeft") { e.preventDefault(); return setOct(octave - 1); }   // (← →: OCT − / OCT +; Z X no more: Marc, 10/11)
  if (e.code === "ArrowRight") { e.preventDefault(); return setOct(octave + 1); }
  if (i < 0 || held.has(e.code)) return;
  const n = BASE + 12 * (octave + 1) + i; held.set(e.code, n); noteOn(n);
});
addEventListener("keyup", (e) => { if (held.has(e.code)) { noteOff(held.get(e.code)); held.delete(e.code); } });
addEventListener("blur", () => { for (const n of held.values()) noteOff(n); held.clear(); });
function setOct(o) {
  o = Math.max(-2, Math.min(2, o));
  if (o === octave) return;
  for (const n of held.values()) noteOff(n); held.clear();
  const keep = [...far]; farClear();
  octave = o;
  for (const n of keep) farNote(track, n, 1);
  document.getElementById("oct-").classList.toggle("on", o < 0);
  document.getElementById("oct+").classList.toggle("on", o > 0);
}
document.getElementById("oct-").addEventListener("click", () => setOct(octave - 1));
document.getElementById("oct+").addEventListener("click", () => setOct(octave + 1));
// PITCH springs back to the middle; MOD stays
function wheel(id, spring, put) {
  const el = document.getElementById(id), ind = el.querySelector(".ind");
  let f = spring ? 0.5 : 0;
  const show = () => { ind.style.top = ((1 - f) * (el.clientHeight - 12) + 2) + "px"; };
  const at = (e) => { const r = el.getBoundingClientRect(); f = Math.max(0, Math.min(1, 1 - (e.clientY - r.top) / r.height)); show(); put(f); };
  let anim = 0, down = false;
  el.addEventListener("pointerdown", (e) => { cancelAnimationFrame(anim); down = true; el.setPointerCapture(e.pointerId); at(e); });
  el.addEventListener("pointermove", (e) => { if (down && el.hasPointerCapture(e.pointerId)) at(e); });
  // PITCH let go: back to the middle on a spring (a damped swing, 0.3 s, a little past the middle and back); the
  // sound follows it but never crosses the middle (the note does not wobble), and ends exactly there
  const let_go = () => {   // (the button up, or the gesture lost: out of the window, another app, a cancel)
    if (!down) return;
    down = false;
    if (!spring) return;
    const f0 = f - 0.5, t0 = performance.now();
    const step = (now) => {
      const t = (now - t0) / 1000;
      if (t >= 0.3 || !f0) { f = 0.5; show(); put(0.5); return; }
      const x = f0 * Math.exp(-t / 0.07) * Math.cos(2 * Math.PI * 4.5 * t);
      f = 0.5 + x; show();
      put(0.5 + (Math.sign(x) === Math.sign(f0) ? x : 0));
      anim = requestAnimationFrame(step);
    };
    anim = requestAnimationFrame(step);
  };
  for (const ev of ["pointerup", "pointercancel", "lostpointercapture"]) el.addEventListener(ev, let_go);
  addEventListener("pointerup", let_go); addEventListener("blur", let_go);
  new ResizeObserver(show).observe(el);
  show();
}
wheel("pitch", true, (f) => { const b = Math.round(f * 16383); if (dev) dev.link.out.send([0xE0 | track, b & 127, b >> 7]); });
wheel("modw", false, (f) => { if (dev) dev.link.out.send([0xB0 | track, 1, Math.round(f * 127)]); });

/* ------------------------------------------------------------------------------------ the tracks --- */
let track = 0;
function showTrack() { document.querySelectorAll(".trk").forEach((t) => t.classList.toggle("on", +t.dataset.t === track)); }
document.querySelectorAll(".trk").forEach((t) => t.addEventListener("pointerdown", async () => {
  const k = +t.dataset.t; if (k === track) return;
  for (const n of held.values()) noteOff(n); held.clear(); farClear();
  track = k; showTrack();
  if (dev) { try { await dev.track(k); await reloadAll(); reopenPage(); } catch (e) { toast(tx("noreply")); } }
}));
// the page shown read again for the track now selected (SEQUENCER: its steps; ARP, FX, MOD: its values)
function reopenPage() { if (dev && page !== "sound" && pageOpen[page]) pageOpen[page](); }

/* -------------------------------------------------------- full screen: F11, Alt+Enter, the logo, its button --- */
addEventListener("keydown", (e) => {
  if (e.code === "F11" || (e.code === "Enter" && e.altKey)) { e.preventDefault(); fullscreen(); }
});
document.getElementById("logo").addEventListener("dblclick", fullscreen);
document.getElementById("t-full").addEventListener("click", fullscreen);
// the bulb: the lit look or the flat one (remembered by this browser)
const glowEl = document.getElementById("t-glow");
function setGlow(on) {
  document.body.classList.toggle("flat", !on); glowEl.classList.toggle("on", on);
  try { localStorage.setItem("guru600-flat", on ? "0" : "1"); } catch (e) {}
}
glowEl.addEventListener("click", () => setGlow(document.body.classList.contains("flat")));
try { if (localStorage.getItem("guru600-flat") === "1") setGlow(false); } catch (e) {}
// the guide (p600/notice, next to the editor: here and on the site), in the page's language
// ?: the editor's guide (../guide, beside the editor), in the messages' language (the guide's seven), at the
// chapter of the page shown (GUIDE_CH: guru-guide-ch.js, written by guide/make_guide.py)
document.getElementById("t-help").addEventListener("click", () => {
  const l = lang;
  const ch = typeof GUIDE_CH === "object" ? GUIDE_CH[page] || GUIDE_CH.layout : 0;
  window.open("../guide/index.html?lang=" + l + (ch ? "#s" + ch : ""), "guru600-guide");
});
function fullscreen() { if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen().catch(() => {}); }

/* ---------------------------------------------------------------------------------- messages --- */
const TX = {
  en: { offline: "Connect the FM-1 first.", noreply: "The FM-1 does not answer.", lose: "The changes to this sound are not saved. Load another sound anyway?",
        nomidi: "This browser has no MIDI: use Chrome, Edge, Brave, Opera…", denied: "MIDI access was refused.", nodevice: "No FM-1 found: connect it by USB, with the Guru-600 firmware.",
        oldfw: "This FM-1 needs the Guru-600 firmware.", connected: "FM-1 connected", disconnected: "FM-1 disconnected",
        save: "Save the current sound in place %s? The sound there now is replaced.", saved: "Saved in place %s", full: "The memory of the places is full (55 sounds).",
        notp6: "This track does not play a P600 sound.", orig: "Bring back the original sound of place %s?", origdone: "Original sound back",
        reset: "Bring back the 255 original sounds? Every sound you saved or imported is erased.", resetdone: "The 255 original sounds are back",
        imp: "Put this sound in place %s? The sound there now is replaced.", impnone: "No Prophet-600 sound in this file.", impdone: "Imported in place %s",
        unsavedexp: "The changes to this sound are not saved: the file will hold the sound as saved in place %s. Export anyway?",
        other: "Track %s plays a sound of the FM-1 (%s).<br>This panel sets the Guru-600 sounds (1 to 255): choose one in the list to set it here." },
  fr: { offline: "Branchez d'abord le FM-1.", noreply: "Le FM-1 ne répond pas.", lose: "Les modifications de ce son ne sont pas enregistrées. Charger quand même un autre son ?",
        nomidi: "Ce navigateur n'a pas le MIDI : utilisez un navigateur compatible MIDI, Chrome, Edge, Brave, Opera…", denied: "L'accès au MIDI a été refusé.",
        nodevice: "Aucun FM-1 trouvé : branchez-le en USB, avec le firmware Guru-600.", oldfw: "Ce FM-1 doit avoir le firmware Guru-600.",
        connected: "FM-1 branché", disconnected: "FM-1 débranché",
        save: "Enregistrer le son actuel à la place %s ? Le son qui s'y trouve est remplacé.", saved: "Enregistré à la place %s", full: "La mémoire des places est pleine (55 sons).",
        notp6: "Cette piste ne joue pas un son P600.", orig: "Rétablir le son d'origine de la place %s ?", origdone: "Son d'origine rétabli",
        reset: "Rétablir les 255 sons d'origine ? Tous les sons enregistrés ou importés sont effacés.", resetdone: "Les 255 sons d'origine sont rétablis",
        imp: "Mettre ce son à la place %s ? Le son qui s'y trouve est remplacé.", impnone: "Aucun son de Prophet-600 dans ce fichier.", impdone: "Importé à la place %s",
        unsavedexp: "Les modifications de ce son ne sont pas enregistrées : le fichier contiendra le son tel qu'il est enregistré à la place %s. Exporter quand même ?",
        other: "La piste %s joue un son du FM-1 (%s).<br>Cette façade règle les sons Guru-600 (1 à 255) : choisissez-en un dans la liste pour le régler ici." },
};
const tx = (k, ...a) => { let s = (TX[lang] || TX.en)[k] || TX.en[k] || k; for (const x of a) s = s.replace("%s", x); return s; };
let toastT = 0;
function toast(s) {
  const e = document.querySelector("#toast span"); e.textContent = s; e.classList.add("on");
  clearTimeout(toastT); toastT = setTimeout(() => e.classList.remove("on"), 2600);
}

showTrack(); showBpm(); showSounds();

/* ===================================================================================== the FM-1 === */
async function reloadValues() {   // the selected track's values (DUMP) and its place (STATE)
  const st = await dev.state();
  if (curEng !== st.engine) farClear();   // (the keys lit with the other engine's shift)
  curEng = st.engine;
  track = st.sel; showTrack();
  const d = await dev.dump(dev.info.pcount);
  for (const id in D) if (d.p[id] != null) val[id] = clampD(id, d.p[id]);
  const g = d.g || [];
  if (g[G_BPM] != null) { bpm = g[G_BPM]; showBpm(); }
  for (const id in D) if (id >= 1000 && g[id - 1000] != null) val[id] = clampD(id, g[id - 1000]);
  const p6 = st.engine === dev.p600;
  stage.classList.toggle("other", !p6);
  if (!p6) document.getElementById("notice").innerHTML = `<div class="nbox">${tx("other", st.sel + 1, dev.info.engines[st.engine] || "?")}</div>`;
  if (p6) place = st.place;
  render(); showSounds(true);
}
async function reloadNames() {
  for (let s = 0; s < 255; s += 16) {
    const got = await dev.names(s, Math.min(16, 255 - s));
    got.forEach((x, i) => { names[s + i] = x; });
  }
  showSounds();
}
async function reloadAll() {
  await reloadValues();
  try { const m = await dev.morphState(); morph.b = m.b; morph.pos = m.pos; morph.amt = m.amt || 40; } catch (e) {}
  showMorph();
}

/* ---------------------------------------------------------------------------- connect, the pushes --- */
const ledEl = document.getElementById("led"), connEl = document.getElementById("conn");
function showConn(on) {
  ledEl.classList.toggle("off", !on);
  connEl.textContent = on ? "FM-1 CONNECTED" : "CONNECT FM-1";
}
let access = null, pinger = 0, morphPoller = 0;
let quietTries = 0;
async function connect(quiet = false) {   // quiet: at the opening, nothing said when no FM-1 is there
  if (dev) return;
  if (!navigator.requestMIDIAccess) return quiet ? undefined : toast(tx("nomidi"));
  try { if (!access) { access = await navigator.requestMIDIAccess({ sysex: true }); access.onstatechange = onMidiState; } }
  catch (e) { return toast(tx("denied")); }
  const isF = (p) => /felucca|fm-?1|guru/i.test(p.name || "") && p.state !== "disconnected";
  const input = [...access.inputs.values()].find(isF), output = [...access.outputs.values()].find(isF);
  if (!input || !output) return quiet ? undefined : toast(tx("nodevice"));
  const link = new Link(input, output, onPush);
  link.onNote = farNote;
  const d = new Device(link);
  try {
    d.info = await d.info();
    d.p600 = d.info.engines.indexOf("P600");
    if (d.p600 < 0 || d.info.pe0 !== PE0) { link.close(); return toast(tx("oldfw")); }
    await d.state();                                   // (a firmware without the Guru-600 frames does not answer)
  } catch (e) {
    link.close();
    // (quiet, no answer: an FM-1 still starting, or the Guru-600 application booting: asked again, 30 s at most)
    if (quiet && /timeout/.test(e.message) && ++quietTries < 15) return void setTimeout(() => connect(true), 2000);
    return quiet ? undefined : toast(/timeout/.test(e.message) ? tx("oldfw") : tx("noreply"));
  }
  quietTries = 0;
  dev = d;
  try {
    await dev.watch(true);
    await reloadNames();
    await reloadAll();
    const tr = await dev.track(); track = tr.sel; showTrack();
  } catch (e) { console.warn(e); }
  dirty = false;
  showConn(true); toast(tx("connected"));
  if (page !== "sound" && pageOpen[page]) pageOpen[page]();   // (the page shown read from the FM-1 now)
  pinger = setInterval(() => { if (dev) dev.watch(true).catch(() => lost()); }, 1000);   // (WATCH lasts 3 s without a request: asked
                                                                                         // again each second, it never lapses)
  morphPoller = setInterval(pollMorph, 30);     // (an MSTATE answer takes 1-2 ms on the FM-1)
}
function lost() {
  if (!dev) return;
  dev.link.close(); dev = null; clearInterval(pinger); clearInterval(morphPoller); farClear();
  stage.classList.remove("other"); showConn(false); showBeat(0, 0); showTransport(0, 0); toast(tx("disconnected"));
}
function onMidiState(e) {   // unplugged: disconnected; plugged in: connected
  if (dev && e.port.state === "disconnected" && e.port === dev.link.out) lost();
  else if (!dev && e.port.state === "connected" && /felucca|fm-?1|guru/i.test(e.port.name || "")) { quietTries = 0; setTimeout(() => connect(true), 300); }
}
connEl.addEventListener("click", () => connect());
ledEl.addEventListener("click", () => connect());
// at the opening: connected at once when MIDI was allowed before and an FM-1 is there
if (navigator.permissions) navigator.permissions.query({ name: "midi", sysex: true }).then((p) => { if (p.state === "granted") connect(true); }).catch(() => {});

// what the FM-1 says by itself: a value turned on it (23), another sound or track (24), the beat (Guru-600)
let reloading = 0;
function onPush(kind, a) {
  if (kind === CMD.CHANGED) {
    const scope = a[0], id = a[1], v = v14dec(a[2], a[3]);
    if (scope === 1 && id === G_BPM) { bpm = v; showBpm(); return; }
    if (scope === 0 && D[id] && !(sending.get(id) || {}).busy) { val[id] = clampD(id, v); render(id); dirty = true; }
    if (scope === 1 && D[1000 + id] && !(sending.get(1000 + id) || {}).busy) { val[1000 + id] = clampD(1000 + id, v); render(1000 + id); }
  } else if (kind === CMD.STEP_CHANGED) {   // a step edited on the FM-1 (its index, its track)
    if (typeof seqStepChanged === "function") seqStepChanged(a[0], a.length > 1 ? a[1] : track);
  } else if (kind === CMD.RELOAD) {
    clearTimeout(reloading); reloading = setTimeout(() => { reloadAll().then(reopenPage).catch((e) => console.warn(e)); reloadNamesOf(place); }, 60);
  } else if (kind === "beat") {   // playing, beat, armed, the step the track plays
    showBeat(a[0], a[1]); showTransport(a[0], a[2]);
    if (typeof seqPlayhead === "function") seqPlayhead(a[0] ? a[3] : -1);
  }
}
async function reloadNamesOf(i) {
  if (!dev) return;
  try { const s = Math.max(0, i - 1), got = await dev.names(s, 3); got.forEach((x, k) => { if (s + k < 255) names[s + k] = x; }); showSounds(); } catch (e) {}
}

/* ------------------------------------------------------------------------- PLAY STOP REC, the beat --- */
function showTransport(playing, armed) {
  document.getElementById("t-play").classList.toggle("on", !!playing);
  document.getElementById("t-rec").classList.toggle("on", !!((armed >> track) & 1));
}
async function transport(op) {
  if (!dev) return toast(tx("offline"));
  try { const a = await dev.link.ask(true, 15, [op]); showTransport(a[0], a[1]); } catch (e) { toast(tx("noreply")); }
}
document.getElementById("t-play").addEventListener("pointerdown", () => transport(1));
document.getElementById("t-stop").addEventListener("pointerdown", () => transport(2));
document.getElementById("t-rec").addEventListener("pointerdown", () => transport(3));

/* ---------------------------------------------------------------- SAVE, ORIGINAL, EXPORT, IMPORT, RESET --- */
document.getElementById("b-save").addEventListener("click", async () => {
  if (!dev) return toast(tx("offline"));
  if (!await uiConfirm(tx("save", place + 1))) return;
  try {
    const rc = await dev.save(place);
    if (rc === 1) return toast(tx("full"));
    if (rc === 2) return toast(tx("notp6"));
    dirty = false; await reloadNamesOf(place); toast(tx("saved", place + 1));
  } catch (e) { toast(tx("noreply")); }
});
document.getElementById("b-orig").addEventListener("click", async () => {
  if (!dev) return toast(tx("offline"));
  if (!names[place].kept || !await uiConfirm(tx("orig", place + 1))) return;
  try { await dev.forget(place); await dev.load(place); dirty = false; await reloadNamesOf(place); await reloadValues(); toast(tx("origdone")); }
  catch (e) { toast(tx("noreply")); }
});
// a sound's name as the FM-1 shows it: capitals, letters, digits and a few signs, 11 at most (the place number goes first)
const soundName = (t) => String(t || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase().replace(/[^ -~]/g, "").trim().slice(0, 11).trim();
async function renamePlace(i) {                     // RENAME (a right click on a sound of the list): a place holding your sound
  if (!dev) return toast(tx("offline"));
  if (!names[i].kept) return toast(tx("renfactory", i + 1));
  const ask = await uiPrompt(tx("rename", i + 1), bare(names[i].name));
  if (ask == null) return;
  const sn = soundName(ask); if (!sn) return;
  try { const rc = await dev.rename(i, sn); if (rc) return toast(tx(rc === 1 ? "full" : "renfactory", i + 1));
    await reloadNamesOf(i); toast(tx("renamed", i + 1)); }
  catch (e) { toast(tx("noreply")); }
}
rows.forEach((r, i) => r.addEventListener("contextmenu", (e) => { e.preventDefault(); renamePlace(i); }));
document.getElementById("b-export").addEventListener("click", async () => {
  if (!dev) return toast(tx("offline"));
  if (dirty && !await uiConfirm(tx("unsavedexp", place + 1))) return;
  try {
    const x = await dev.exportOf(place);
    const ask = await uiPrompt(tx("expname"), bare(x.name) || "P600");   // (the name kept in the file: re-imported with it)
    if (ask == null) return;
    const sn = soundName(ask) || "P600";
    const nm = String(place + 1).padStart(3, "0") + " " + sn.replace(/[\\/:*?"<>|]/g, "-") + ".syx";
    const rec = [0xF0, 0x7D, 0x47, 0x36, 7, 0, 0, ...[...sn].map((c) => c.charCodeAt(0)), 0xF7];
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([new Uint8Array([...x.sci, ...rec])], { type: "application/octet-stream" }));
    a.download = nm; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  } catch (e) { toast(tx("noreply")); }
});
const fileIn = Object.assign(document.createElement("input"), { type: "file", accept: ".syx,.mid,application/octet-stream" });
fileIn.addEventListener("change", async () => {
  const f = fileIn.files[0]; fileIn.value = "";
  if (!f || !dev) return;
  const buf = await f.arrayBuffer(), list = parseSyx(buf);
  if (!list.length) return toast(tx("impnone"));
  if (!await uiConfirm(tx("imp", place + 1))) return;
  try {
    const rc = await dev.importTo(place, list[0]);
    if (rc === 1) return toast(tx("full"));
    // its name: the file's record, else the file's name without its place number ("007 POWERSYNTH.syx")
    const sn = soundName(syxName(buf) || f.name.replace(/\.[^.]*$/, "").replace(/^\d+\s+/, ""));
    if (sn) await dev.rename(place, sn);
    await dev.load(place); dirty = false; await reloadNamesOf(place); await reloadValues(); toast(tx("impdone", place + 1));
  } catch (e) { toast(tx("noreply")); }
});
document.getElementById("b-import").addEventListener("click", () => { if (!dev) return toast(tx("offline")); fileIn.click(); });
document.getElementById("b-reset").addEventListener("click", async () => {
  if (!dev) return toast(tx("offline"));
  if (!await uiConfirm(tx("reset"))) return;
  try { await dev.reset(); await reloadNames(); await dev.load(place); dirty = false; await reloadValues(); toast(tx("resetdone")); }
  catch (e) { toast(tx("noreply")); }
});

/* ------------------------------------------------------------------------------------- the pages --- */
// one page shown at a time between the tabs and the keyboard; the header, the tabs and the keyboard never move
const pageOpen = {};     // name -> its function when shown (each page's file)
let page = "sound";
function showPage(name) {
  if (!document.querySelector(`[data-page="${name}"]`)) return;   // (a tab not made yet)
  page = name;
  for (const e of stage.querySelectorAll("[data-page]")) e.style.display = e.dataset.page === name ? "" : "none";
  for (const t of document.querySelectorAll(".tab")) t.classList.toggle("on", t.dataset.tab === name);
  layout();   // (its sections' contents centred now that they are shown)
  if (pageOpen[name]) pageOpen[name]();
  for (const t of document.querySelectorAll(".tab")) t.classList.toggle("later", !document.querySelector(`[data-page="${t.dataset.tab}"]`));
}
document.querySelectorAll(".tab").forEach((t) => t.addEventListener("pointerdown", () => showPage(t.dataset.tab)));
