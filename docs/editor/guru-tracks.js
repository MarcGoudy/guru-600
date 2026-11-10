// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the TRACKS page: the four tracks side by side (their engine, their sound, LEVEL, PAN, the sends, MUTE,
// SOLO, armed), the selected one chosen here too. Felucca's TRACK (27), TRACK_MIX (28), TRACK_PARAM (31), SET of G_ENGSEL.
"use strict";

const G_ENGSEL = 20;
const TP_IDS = { level: 0, pan: 39, dist: 33, cho: 34, dly: 35, rev: 36 };
let mix = [0, 1, 2, 3].map((t) => ({ engine: [14, 14, 0, 10][t], preset: [0, 2, 0, 0][t], level: [104, 98, 90, 110][t], mute: t === 2,
  armed: t === 0, pan: [0, -20, 18, 0][t], dist: 0, cho: [30, 10, 0, 0][t], dly: [22, 0, 40, 0][t], rev: [45, 30, 20, 10][t] }));
let solo = -1, engNames = ["ANALOG", "-", "PHASE", "LOFI", "SAMPLE", "VOICE", "TRIO", "WHEEL", "GRAIN", "PHYS", "DRUM", "NOISE", "FM6", "SLICE", "P600"];
const ENG_ORDER = [14, 0, 12, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 10];   // the device's order (P600 first, as on the FM-1)
const ENGC = (e) => (e === 14 ? "var(--osc)" : e === 10 ? "var(--env)" : e === 12 ? "var(--pm)" : "var(--lfo)");

// DIST above PAN (the track's own distortion, not a send: as on the FX page), the sends in a row of three, ◀ the sound ▶
document.head.insertAdjacentHTML("beforeend", "<style>.strip .sends { grid-template-columns: repeat(3, 1fr); }.strip .mixr { justify-content: stretch; }.strip .mixr > .lcol, .strip .mixr > .fader { flex: 1 1 0; min-width: 0; }.strip .fv { width: 84px; text-align: center; }.strip .sk .v, .strip .pan .v { width: 60px; text-align: center; }.strip .lcol { display: flex; flex-direction: column; justify-content: space-evenly; align-items: center; height: 100%; }.strip .sndrow { display: flex; align-items: center; justify-content: center; gap: 10px; width: 100%; }.strip .sndrow .snd { min-width: 0; max-width: 250px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; text-align: center; }</style>");
(function buildTracks() {
  for (let t = 0; t < 4; t++) {
    const e = h("div", "sec strip"); e.dataset.page = "tracks"; e.dataset.t = t; e.style.setProperty("--c", "var(--snd)");
    e.innerHTML = `<div class="ttl">TRACK ${t + 1}</div><div class="sbd">` +
      `<div class="eng"><div class="arr l"></div><div class="field ef"></div><div class="arr r"></div></div>` +
      `<div class="sndrow"><div class="arr l"></div><div class="snd"></div><div class="arr r"></div></div>` +
      `<div class="sends">${["CHORUS", "DELAY", "REVERB"].map((n, k) => `<div class="sk" data-k="${["cho", "dly", "rev"][k]}"><div class="tl">${n}</div></div>`).join("")}</div>` +
      `<div class="mixr"><div class="lcol"><div class="sk" data-k="dist"><div class="tl">DIST</div></div><div class="pan" data-k="pan"><div class="tl">PAN</div></div></div>` +
      `<div class="fader"><div class="fdr"><i></i><b></b></div><div class="fv"></div></div></div>` +
      `<div class="ms"><div class="btn mute">MUTE</div><div class="btn solo">SOLO</div></div>` +
      `<div class="selrow"><b class="led arm"></b><div class="btn sel">SELECT</div></div></div>`;
    abs(e, 12 + t * 378, 155, 12 + t * 378 + 370, 773);
    e.querySelectorAll(".sk, .pan").forEach((k) => { const s = knobSvg(); s.classList.add("small"); k.appendChild(s); k.appendChild(h("div", "v")); });
    e.style.display = "none";
  }
})();
const strips = [...stage.querySelectorAll(".strip")];
const dbOf = (v) => (v <= 0 ? "OFF" : dec(((v - 112) / 2).toFixed(1)) + " dB");
function drawTracks() {
  strips.forEach((e, t) => {
    const m = mix[t];
    e.classList.toggle("selt", t === track); e.classList.toggle("muted", m.mute || (solo >= 0 && solo !== t));
    e.style.setProperty("--c", t === track ? "var(--trk)" : "var(--snd)");
    e.querySelector(".ef").textContent = engNames[m.engine] || "?";
    e.querySelector(".ef").style.setProperty("--c", ENGC(m.engine));
    e.querySelector(".snd").textContent = m.engine === 14 ? (t === track || m.preset < 127 ? placeLabel(t === track ? place : m.preset) : "")
      : ((engPresets[m.engine] || [])[m.preset] || "");
    for (const k of ["dist", "cho", "dly", "rev", "pan"]) {
      const box = e.querySelector(`[data-k="${k}"]`), v = m[k];
      drawKnob(box.querySelector("svg"), k === "pan" ? (v + 64) / 127 : v / 127, k === "pan");
      box.querySelector(".v").textContent = k === "pan" ? (v ? (v < 0 ? "L " : "R ") + Math.round(Math.abs(v) * 100 / 64) : "C") : Math.round(v * 100 / 127) + " %";
    }
    e.querySelector(".fdr b").style.bottom = (m.level / 127 * 100) + "%";
    e.querySelector(".fdr i").style.height = (m.level / 127 * 100) + "%";
    e.querySelector(".fv").textContent = dbOf(m.level);
    e.querySelector(".mute").classList.toggle("on", m.mute);
    e.querySelector(".solo").classList.toggle("on", solo === t);
    e.querySelector(".arm").classList.toggle("on", m.armed);
    e.querySelector(".sel").classList.toggle("on", t === track);
  });
}

/* ---------------------------------------------------------------------------------------- editing --- */
async function tParam(t, id, v) {   // any track's parameter (TRACK_PARAM); the selected track's also in val[]
  if (t === track && D[id]) { val[id] = v; render(id); }
  if (dev) try { await dev.link.ask(false, 31, [t, id, ...v14enc(v)], (r) => r[0] === t && r[1] === id); } catch (e) { toast(tx("noreply")); }
}
async function tMix(t) {
  const m = mix[t], mute = m.mute || (solo >= 0 && solo !== t);
  if (dev) try { await dev.link.ask(false, 28, [t, ...v14enc(m.level), mute ? 1 : 0], (r) => r[0] === t); } catch (e) { toast(tx("noreply")); }
}
strips.forEach((e, t) => {
  e.querySelectorAll(".sk, .pan").forEach((box) => {
    const k = box.dataset.k, svg = box.querySelector("svg"), [lo, hi] = k === "pan" ? [-64, 63] : [0, 127];
    knobDrag(svg, () => mix[t][k], (x) => { const v = Math.max(lo, Math.min(hi, Math.round(x))); if (v === mix[t][k]) return; mix[t][k] = v; drawTracks(); tParam(t, TP_IDS[k], v); }, hi - lo, k === "pan" ? 0 : 0);
  });
  const fdr = e.querySelector(".fdr");
  const at = (ev) => { const r = fdr.getBoundingClientRect(); mix[t].level = Math.round(Math.max(0, Math.min(1, 1 - (ev.clientY - r.top) / r.height)) * 127); drawTracks(); };
  fdr.addEventListener("pointerdown", (ev) => { fdr.setPointerCapture(ev.pointerId); at(ev); });
  fdr.addEventListener("pointermove", (ev) => { if (fdr.hasPointerCapture(ev.pointerId)) { at(ev); tMix(t); } });
  fdr.addEventListener("pointerup", () => tMix(t));
  fdr.addEventListener("dblclick", () => { mix[t].level = 104; drawTracks(); tMix(t); });
  e.querySelector(".mute").addEventListener("pointerdown", () => { mix[t].mute = !mix[t].mute; drawTracks(); tMix(t); });
  e.querySelector(".solo").addEventListener("pointerdown", () => { solo = solo === t ? -1 : t; drawTracks(); for (let k = 0; k < 4; k++) tMix(k); });
  e.querySelector(".sel").addEventListener("pointerdown", () => document.querySelector(`.trk[data-t="${t}"]`).dispatchEvent(new PointerEvent("pointerdown")));
  const step = async (d) => {   // the engine: the device's order; changed on the track selected for it, then back
    if (!dev) return toast(tx("offline"));
    if (!await uiConfirm(tx("engchg", t + 1))) return;
    const i = ENG_ORDER.indexOf(mix[t].engine), e2 = ENG_ORDER[(i + d + ENG_ORDER.length) % ENG_ORDER.length], was = track;
    try {
      if (t !== was) await dev.track(t);
      await dev.set(G_ENGSEL, e2, 1);
      if (t !== was) await dev.track(was);
      await tracksRead(); if (t === was) await reloadValues();
    } catch (er) { toast(tx("noreply")); }
  };
  // the sound: ◀ ▶ around its name (P600: the 255 places; another engine: its sounds), on that track, then back
  const sstep = async (d) => {
    if (!dev) return toast(tx("offline"));
    const m = mix[t], was = track;
    if (t === was && m.engine === 14 && dirty && !await uiConfirm(tx("lose"))) return;
    try {
      if (t !== was) await dev.track(t);
      if (m.engine === 14) { const st = await dev.state(); await dev.load((st.place + d + 255) % 255); }
      else {
        await enginePresets(m.engine);
        const n = (engPresets[m.engine] || []).length;
        if (n) await dev.link.ask(false, 8, [m.engine, (m.preset + d + n) % n], (r) => r[0] === m.engine);
      }
      if (t !== was) await dev.track(was);
      if (t === was) { dirty = false; await reloadValues(); }
      await tracksRead();
    } catch (er) { toast(tx("noreply")); }
  };
  e.querySelector(".sndrow .l").addEventListener("pointerdown", () => sstep(-1));
  e.querySelector(".sndrow .r").addEventListener("pointerdown", () => sstep(1));
  e.querySelector(".eng .l").addEventListener("pointerdown", () => step(-1));
  e.querySelector(".eng .r").addEventListener("pointerdown", () => step(1));
});

/* ------------------------------------------------------------------------------------ the FM-1 --- */
const engPresets = {};   // engine -> its preset names (Felucca's NAMES; P600's are the places)
async function enginePresets(e) {
  if (engPresets[e] || e === 14) return;
  const a = await dev.link.ask(false, 10, [e], (r) => r[0] === e, 1500);
  const out = []; let i = 2;   // (NAMES: engine, count, the count names, then the two EDIT pages' titles: not sounds)
  while (i < a.length && out.length < Math.min(127, a[1])) { let s = ""; while (i < a.length && a[i]) s += String.fromCharCode(a[i++]); i++; out.push(s); }
  engPresets[e] = out;
}
async function tracksRead() {
  if (!dev) return;
  if (dev.info && dev.info.engines) engNames = dev.info.engines;
  const tr = await dev.track();
  for (let t = 0; t < 4; t++) {
    const s = tr.tracks[t] || {}, m = mix[t];
    Object.assign(m, { engine: s.engine, preset: s.preset, level: s.level, armed: !!s.armed });
    if (solo < 0) m.mute = !!s.mute;
    for (const k of ["pan", "dist", "cho", "dly", "rev"]) {
      const a = await dev.link.ask(false, 31, [t, TP_IDS[k]], (r) => r[0] === t && r[1] === TP_IDS[k]);
      m[k] = v14dec(a[2], a[3]);
    }
  }
  for (const m of mix) try { await enginePresets(m.engine); } catch (e) {}
  track = tr.sel; showTrack();
  drawTracks();
}
pageOpen.tracks = () => { drawTracks(); if (dev) tracksRead().catch((e) => console.warn(e)); };
Object.assign(TX.en, { engchg: "Change the engine of track %s? Its sound is replaced by the new engine's first." });
Object.assign(TX.fr, { engchg: "Changer le moteur de la piste %s ? Son son est remplacé par le premier du nouveau moteur." });
