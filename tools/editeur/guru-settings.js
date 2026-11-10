// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the SETTINGS page: the FM-1's MENU settings as the device describes them (Felucca's MENU_DESC 72:
// each one's id, kind, value, range, name, its values' names and its MENU tab; MENU_SET 73), grouped by tab as on the
// device; and the editor's own (its lighting, its messages' language: kept in this browser).
"use strict";

const N_CH = [...Array.from({ length: 16 }, (_, k) => String(k + 1)), "OMNI", "OFF"];
// (offline: the list as the firmware gives it; connected, the device's own replaces it)
let menuItems = [
  [0, 0, 10, "COLOR", 0, "GREY|GREEN|AMBER|ICE|VIOLET|ROSE|PAPER|HI-CON|NIGHT|MONO|P600"], [1, 0, 0, "STYLE", 0, "FLAT|LINE"],
  [2, 0, 0, "LARGE", 0, "OFF|ON"], [3, 0, 0, "ANIM", 0, "ON|OFF|IDLE"], [4, 0, 2, "LEDS", 0, "OFF|DIM LO|DIM HI|INV|INV LO|INV HI"],
  [5, 0, 1, "HOLD", 1, "0.3 s|0.4 s|0.5 s|0.6 s"], [6, 0, 0, "KNOB ACCEL", 1, "OFF|ON"], [7, 0, 0, "FX LATCH", 1, "OFF|ON"],
  [8, 0, 0, "BPM LOCK", 1, "OFF|ON"], [9, 0, 0, "SPEAKER EQ", 2, "FLAT|LOWCUT|BASS+"], [10, 0, 0, "USB LEVEL", 2, "MASTER|FIXED"],
  [12, 0, 0, "CLICK", 2, "OFF|REC|ON"], [13, 0, 1, "CLICK LEVEL", 2, "LOW|MID|HIGH"], [14, 0, 0, "COUNT-IN", 2, "OFF|1 BAR|2 BARS"],
  [15, 0, 0, "RESTORE LAST", 4, "ON|OFF"], [16, 0, 0, "SCALE LEDS", 1, "OFF|ON"], [17, 0, 0, "SCREEN OFF", 0, "NEVER|5 MIN|15 MIN|30 MIN|60 MIN"],
  [18, 0, 0, "SCOPE", 0, "OUT|MIX"], [19, 0, 0, "STEP PREVIEW", 1, "OFF|ON"], [20, 0, 0, "CHORD ENTRY", 1, "HOLD|ADD"],
  [21, 0, 0, "MIDI IN", 3, "CH1-4|SEL|CH5-8|CH9-12|CH13-16|TRACK"], [22, 1, 0, "TUNE", 2, "ct"], [24, 0, 0, "HELP", 4, "OFF|ON"],
  [25, 0, 0, "SELECT", 1, "BPM|PAGE|MODW|VEL"], [26, 0, 0, "T1 CHANNEL", 3, N_CH.join("|")], [27, 0, 1, "T2 CHANNEL", 3, N_CH.join("|")],
  [28, 0, 2, "T3 CHANNEL", 3, N_CH.join("|")], [29, 0, 3, "T4 CHANNEL", 3, N_CH.join("|")], [30, 0, 0, "AUTO SELECT", 3, "OFF|ON"],
  [31, 0, 0, "SCREEN WAKE", 3, "+MIDI|PANEL"], [32, 0, 0, "2ND CORE", 4, "OFF|ON (BETA)"],
].map(([id, kind, v, name, tab, n]) => ({ id, kind, v, lo: kind ? -50 : 0, hi: kind ? 50 : n.split("|").length - 1, name, tab,
  tabn: ["DISPLAY", "CONTROL", "AUDIO", "MIDI", "SYSTEM"][tab], names: n.split("|") }));
const SET_SECS = [["DISPLAY", "osc", 0], ["CONTROL", "lfo", 1], ["AUDIO", "fx", 2], ["MIDI", "vce", 3], ["SYSTEM", "pm", 4], ["EDITOR", "snd", 5]];
// three columns: DISPLAY over SYSTEM, CONTROL over EDITOR, AUDIO over MIDI (each as tall as its settings)
// (heights in proportion to their rows: the same pitch in the two boxes of a column; the rows spread over each box)
const SET_BOX = (k) => [[12, 155, 512, 559], [520, 155, 1016, 572], [1024, 155, 1524, 441], [1024, 449, 1524, 773], [12, 567, 512, 773], [520, 580, 1016, 773]][k];
document.head.insertAdjacentHTML("beforeend", "<style>.setsec .sbd { justify-content: space-evenly; gap: 0; }.setr .nm { font-size: 17px; } .setr .chs .btn.ch { height: 36px; font-size: 16px; } .setr .fldw .field { height: 36px; line-height: 32px; }.sethint { margin-top: 0; text-align: center; font-size: 14px; color: #8d8a82; }.setr { grid-template-columns: 120px 290px; justify-content: center; column-gap: 34px; } .setr .chs { width: 100%; } .setr .fldw { justify-self: stretch; display: flex; align-items: center; margin: 0 -24px; } .setr .fldw .field { flex: 1; width: auto; }</style>");

(function buildSettings() {
  SET_SECS.forEach(([t, c], k) => {
    const e = h("div", "sec setsec"); e.dataset.page = "settings"; e.dataset.k = k;
    e.style.setProperty("--c", `var(--${c})`); e.style.setProperty("--onc", `var(--${c})`);
    e.innerHTML = `<div class="ttl">${t}</div><div class="sbd"></div>`;
    abs(e, ...SET_BOX(k)); e.style.display = "none";
  });
})();
const setSecs = [...stage.querySelectorAll(".setsec")];
const LANG_NAMES = { auto: "AUTO", en: "ENGLISH", fr: "FRANÇAIS", de: "DEUTSCH", es: "ESPAÑOL", it: "ITALIANO", zh: "中文", ja: "日本語" };
const setLang = (() => { try { return localStorage.getItem("guru600-lang") || "auto"; } catch (e) { return "auto"; } })();
const short = (it) => it.kind === 0 && it.names.length <= 4 && it.names.join("").length <= 22;   // buttons; else a field
const valName = (it) => (it.kind ? (it.v > 0 ? "+" : "") + it.v + " " + it.names[0] : it.names[it.v - it.lo] || "?");
function setRow(it) {
  if (short(it)) return `<div class="setr" data-id="${it.id}"><div class="nm">${it.name}</div><div class="chs" style="grid-template-columns:repeat(${it.names.length}, 1fr)">` +
    it.names.map((n, i) => `<div class="btn ch${i + it.lo === it.v ? " on" : ""}" data-v="${i + it.lo}" >${n}</div>`).join("") + `</div></div>`;
  return `<div class="setr" data-id="${it.id}"><div class="nm">${it.name}</div><div class="arrows fldw"><div class="arr l"></div>` +
    `<div class="field">${valName(it)}</div><div class="arr r"></div></div></div>`;
}
function drawSettings() {
  const tune = menuItems.find((x) => x.id === 22);
  if (tune && val[1003] != null) tune.v = val[1003];   // (TUNE: the FX page's MASTER TUNE, the same value)
  setSecs.forEach((e, k) => {
    const b = e.querySelector(".sbd");
    if (k < 5) { b.innerHTML = (menuItems.filter((it) => it.tab === k).map(setRow).join("") || `<div class="hint">—</div>`) +
      (k === 4 ? `<div class="setr" data-ed="factory"><div class="nm">FACTORY</div><div class="btn red" id="b-factory">RESET GURU-600</div></div>` : ""); return; }   // (Guru-600 10/11: MENU > SYSTEM > RESET GURU-600)
    const flat = document.body.classList.contains("flat");
    b.innerHTML = `<div class="setr" data-ed="glow"><div class="nm">LIGHTING</div><div class="chs" style="grid-template-columns:repeat(2, 1fr)">` +
      `<div class="btn ch${flat ? "" : " on"}" data-v="1">LIT</div><div class="btn ch${flat ? " on" : ""}" data-v="0">FLAT</div></div></div>` +
      `<div class="setr" data-ed="lang"><div class="nm">LANGUAGE</div><div class="arrows fldw"><div class="arr l"></div>` +
      `<div class="field">${LANG_NAMES[setLang]}</div><div class="arr r"></div></div></div><div class="sethint">THE EDITOR'S OWN, KEPT IN THIS BROWSER. THE OTHERS ARE THE FM-1'S MENU: SAVED IN IT AT ONCE.</div>`;
  });
}
async function menuSet(it, v) {
  v = Math.max(it.lo, Math.min(it.hi, v));
  if (v === it.v) return;
  it.v = v; drawSettings();
  if (it.id === 22 && D[1003]) { val[1003] = v; render(1003); }   // (TUNE: the FX page's MASTER TUNE too)
  if (!dev) return;
  try {
    const a = await dev.link.ask(false, 73, [it.id, ...v14enc(v)], (r) => r[1] === it.id, 1500);
    it.v = v14dec(a[2], a[3]); drawSettings();
    if (a[0] === 1) toast(tx("setno")); else if (a[0] === 3) toast(tx("setram")); else if (a[0] === 4) toast(tx("setlater"));
  } catch (e) { toast(tx("noreply")); }
}
stage.addEventListener("pointerdown", (ev) => {
  const r = ev.target.closest(".setsec .setr"); if (!r) return;
  if (r.dataset.ed === "factory") { if (ev.target.closest("#b-factory")) factoryReset(); return; }
  if (r.dataset.ed === "glow") { const b = ev.target.closest(".ch"); if (b) { setGlow(b.dataset.v === "1"); drawSettings(); } return; }
  if (r.dataset.ed === "lang") {   // (AUTO and the seven; the page reloads in the one chosen)
    const k = ev.target.classList.contains("l") ? -1 : ev.target.classList.contains("r") ? 1 : 0; if (!k) return;
    const vs = Object.keys(LANG_NAMES), v = vs[(vs.indexOf(setLang) + k + vs.length) % vs.length];
    try { localStorage.setItem("guru600-lang", v); } catch (e) {}
    location.replace(location.pathname + "?tab=settings"); return;
  }
  const it = menuItems.find((x) => x.id === +r.dataset.id); if (!it) return;
  const b = ev.target.closest(".ch"); if (b) return menuSet(it, +b.dataset.v);
  const n = it.hi - it.lo + 1, step = (k) => (it.kind ? it.v + k : it.lo + ((it.v - it.lo + k + n) % n));
  if (ev.target.classList.contains("l")) menuSet(it, step(-1));
  if (ev.target.classList.contains("r")) menuSet(it, step(1));
});
stage.addEventListener("wheel", (ev) => {
  const f = ev.target.closest(".setsec .field"); if (!f) return;
  ev.preventDefault();
  const it = menuItems.find((x) => x.id === +f.closest(".setr").dataset.id), n = it.hi - it.lo + 1, k = ev.deltaY < 0 ? 1 : -1;
  menuSet(it, it.kind ? it.v + k : it.lo + ((it.v - it.lo + k + n) % n));
}, { passive: false });

/* ------------------------------------------------------------------------------------ the FM-1 --- */
async function menuRead() {
  const out = [];
  for (let k = 0; k < 64; k++) {
    const a = await dev.link.ask(false, 72, [k], (r) => r[0] === k, 1000);
    if (a[1] === 127) break;
    let i = 3;
    const rs = () => { let s = ""; while (i < a.length && a[i]) s += String.fromCharCode(a[i++]); i++; return s; };
    const it = { id: a[1], kind: a[2], v: v14dec(a[3], a[4]), lo: v14dec(a[5], a[6]), hi: v14dec(a[7], a[8]) }; i = 9;
    it.name = rs(); it.names = [];
    if (it.kind === 0) for (let j = it.lo; j <= it.hi; j++) it.names.push(rs()); else it.names.push(rs());
    it.tab = i < a.length ? a[i++] : 4; it.tabn = i < a.length ? rs() : "SYSTEM";
    if (it.tab > 4) it.tab = 4;   // (a tab newer than this page: with SYSTEM)
    out.push(it);
  }
  if (out.length) menuItems = out;
  drawSettings();
}
pageOpen.settings = () => { drawSettings(); if (dev) menuRead().catch((e) => console.warn(e)); };
Object.assign(TX.en, { setno: "This FM-1 does not have that setting.", setram: "Set, but the FM-1 could not keep it: it is lost at power-off.",
  setlater: "Set: the FM-1 keeps it once the music stops." });
Object.assign(TX.fr, { setno: "Ce FM-1 n'a pas ce réglage.", setram: "Réglé, mais le FM-1 n'a pas pu le garder : il sera perdu à l'extinction.",
  setlater: "Réglé : le FM-1 le garde dès que la musique s'arrête." });

// RESET GURU-600 (MENU > SYSTEM's, firmware editor.c P6 17): everything of the user's erased on the FM-1, asked twice
async function factoryReset() {
  if (!dev) return toast(tx("offline"));
  if (!await uiConfirm(tx("factory1")) || !await uiConfirm(tx("factory2"))) return;
  dev.link.out.send([0xF0, 0x7D, 0x47, 0x36, 17, 82, 69, 83, 69, 84, 0xF7]);   // (17 R E S E T: no answer, the FM-1 restarts)
  toast(tx("factorygo"));
}
