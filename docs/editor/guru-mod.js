// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the MOD page: the selected track's modulation matrix (4 slots; 3 and 4 are EXTRAS' VEL > FLT and
// WHEEL on a P600 track), the LFO's options (LFO 2 on the FM-1: SYNC TRIG POL; PHASE FADE; the LFO to the amp), the
// voice's (VOICE pages) and the envelope's (ENV DEST, ENV SYNC); ACTIVE lists what modulates the sound now.
"use strict";

Object.assign(P, { LPHASE: 11, LFADE: 12, LD_AMP: 16, ED_FLT: 5, ED_PIT: 6, ED_SHP: 7, GLMODE: 41, PRIO: 42, ALLOC: 43,
  LSYNC: 91, LTRIG: 92, LPOL: 93, ESYNC: 102 });
const N_MSRC = ["OFF", "LFO", "ENV", "VEL", "KEY", "RAND", "MODW", "AT", "EXPR", "S&H", "SLEW"];
const N_MDST = ["OFF", "PITCH", "CUT", "SHP", "AMP", "PAN", "DIST", "CHO", "DLY", "REV", "RATE", "VIB", "E1", "E2", "E3", "E4", "E5", "E6",
  "E7", "E8", "DEPTH", "VEL", "TIME"];
// E1..E8: the P600's own parameters (its EDIT 1 / EDIT 2 labels)
const E_NAMES = ["WAVE A", "FREQ A", "WAVE B", "FREQ B", "CUTOFF", "RESONANCE", "MIXER", "ENV AMOUNT"];
const N_MDST_P6 = N_MDST.map((n, i) => (i >= 12 && i <= 19 ? E_NAMES[i - 12] : n));
const N_LSYNC = ["OFF", "4BAR", "2BAR", "1/1", "1/2", "1/4", "1/8", "8T", "1/16", "16T", "1/32"];
const MS = [49, 52, 55, 58];   // slot k: SRC MS[k], DST MS[k] + 1, AMT MS[k] + 2
for (const b of MS) {
  D[b] = dsc(F.ENUM, 0, 10, 0); D[b].names = N_MSRC;
  D[b + 1] = dsc(F.ENUM, 0, 22, 0); D[b + 1].names = N_MDST_P6;
  if (!D[b + 2]) D[b + 2] = dsc(F.BIPCT, -64, 63, 0);   // (slots 3, 4: EXTRAS' VEL > FLT and WHEEL, as SOUND has them)
}
Object.assign(D, {
  [P.LSYNC]: dsc(F.ENUM, 0, 10, 0), [P.LTRIG]: dsc(F.ENUM, 0, 1, 0), [P.LPOL]: dsc(F.ENUM, 0, 1, 0), [P.LPHASE]: dsc(F.INT, 0, 127, 0),
  [P.LFADE]: dsc(F.TIME, 0, 127, 0), [P.LD_AMP]: dsc(F.PCT, 0, 127, 0), [P.GLMODE]: dsc(F.ENUM, 0, 1, 0), [P.PRIO]: dsc(F.ENUM, 0, 2, 0),
  [P.ALLOC]: dsc(F.ENUM, 0, 1, 0), [P.ESYNC]: dsc(F.ONOFF, 0, 1, 0), [P.ED_FLT]: dsc(F.BIPCT, -64, 63, 0), [P.ED_PIT]: dsc(F.BIPCT, -64, 63, 0),
  [P.ED_SHP]: dsc(F.BIPCT, -64, 63, 0),
});
D[P.LSYNC].names = N_LSYNC;
Object.assign(val, { 49: 1, 50: 1, 51: 16, 52: 2, 53: 5, 54: -26, 55: 3, 56: 2, 57: 33, 58: 6, 59: 20, 60: 63,
  [P.LSYNC]: 0, [P.LTRIG]: 0, [P.LPOL]: 0, [P.LPHASE]: 0, [P.LFADE]: 52, [P.LD_AMP]: 0, [P.GLMODE]: 0, [P.PRIO]: 0, [P.ALLOC]: 0, [P.ESYNC]: 0,
  [P.ED_FLT]: 0, [P.ED_PIT]: 0, [P.ED_SHP]: 0 });
METRICS.mx = { kn: 46, tlh: 0 }; METRICS.lfo2 = { kn: 54, tlh: 22 }; METRICS.vc2 = {}; METRICS.env2 = { kn: 54, tlh: 22 };

// a field with its arrows (◀ value ▶): a choice of many
function field(id, w = 130) {
  const box = h("div", "arrows fldw");
  const l = h("div", "arr l"), f = h("div", "field"), r = h("div", "arr r");
  f.style.width = w + "px"; box.append(l, f, r);
  ctl.push({ kind: "fld", id, el: f, l, r });
  return box;
}
const ctlMod = ctl.length;
// the MOD page uses its space as FX and ARP: square keys (VOICE's larger, its box is roomy), the groups centred, the
// LFO's rows and ENVELOPE's groups spread evenly
document.head.insertAdjacentHTML("beforeend", "<style>.chg.sq60 .btn.ch { width: 62px; height: 62px; min-width: 0; padding: 0; font-size: 16px; display: flex; align-items: center; justify-content: center; }.bd.vcb > .grp { justify-content: center; }#lfo2 .bd.stack { justify-content: space-evenly; padding-left: 0; }#lfo2 .bd.stack > .grp { align-items: center; padding-top: 0; flex: 0 0 auto; }#lfo2 .bd.stack > .grp.chg { justify-content: center; }#lfo2 .srow2 { justify-content: space-evenly; padding-left: 0; width: 100%; }#lfo2 .srow2 > .grp { align-items: center; padding-top: 0; }#env2 .bd { justify-content: space-evenly; }#env2 .bd > .grp { justify-content: center; padding-top: 0; }#env2 .bd > .grp:first-child { flex: none; padding: 0 34px; }#env2 .bd > .grp:last-child { flex: 1; }</style>");
(function buildMod() {
  const sec = (id, t, c, box) => { const e = makeSection({ id, t, c, box, groups: [] }); e.dataset.page = "mod"; e.style.setProperty("--onc", `var(--${c})`);
    return [e, e.querySelector(".bd")]; };
  let [, b] = sec("mx", "MOD MATRIX", "lfo", [12, 155, 900, 520]);
  b.classList.add("mxb");
  b.insertAdjacentHTML("beforeend", `<div class="mxr hd"><div></div><div>SOURCE</div><div></div><div>DESTINATION</div><div>AMOUNT</div><div></div></div>`);
  MS.forEach((m, k) => {
    const r = h("div", "mxr");
    const n = h("div", "", `<span class="n">${k + 1}</span>`);
    const a = h("div", ""); a.appendChild(field(m, 120));
    const ar = h("div", "to", "→");
    const d = h("div", ""); d.appendChild(field(m + 1, 150));
    const kn = h("div", "mxk"); const it = makeItem(K(m + 2, { bip: true }));   // (the value right of its knob: the row is low)
    const w = h("div", "kv"); w.append(it.querySelector(".knob"), it.querySelector(".v")); it.appendChild(w); kn.appendChild(it);
    const tag = h("div", "tag", k === 2 ? "EXTRAS · VEL &gt; FLT" : k === 3 ? "EXTRAS · WHEEL" : "");
    r.append(n, a, ar, d, kn, tag); b.appendChild(r);
  });
  [, b] = sec("lfo2", "LFO", "lfo", [908, 155, 1314, 520]);
  b.classList.add("stack");
  const sy = h("div", "grp chg"); sy.innerHTML = `<div class="gt">SYNC</div>`; sy.appendChild(field(P.LSYNC, 90));
  const row = h("div", "srow2"); row.append(choice("TRIG", P.LTRIG, ["NOTE", "FREE"], 2, "sq"), choice("POLARITY", P.LPOL, ["BI", "UNI"], 2, "sq"));
  b.appendChild(sy);
  const kn = h("div", "grp"); kn.innerHTML = `<div class="gt"></div>`; const its = h("div", "items");
  [[P.LPHASE, "PHASE"], [P.LFADE, "FADE"], [P.LD_AMP, "TO AMP"]].forEach(([id, t]) => its.appendChild(makeItem(K(id, { tl: t }))));
  kn.appendChild(its); b.append(row, kn);
  [, b] = sec("vc2", "VOICE", "vce", [12, 528, 900, 773]);
  b.classList.add("vcb");
  b.append(choice("MODE", P.VOICE, ["POLY", "MONO", "LEGATO", "UNISON"], 4, "sq60"), choice("GLIDE", P.GLMODE, ["RATE", "TIME"], 2, "sq60"),
    choice("PRIORITY", P.PRIO, ["LAST", "LOW", "HIGH"], 3, "sq60"), choice("VOICES", P.ALLOC, ["ROTATE", "REUSE"], 2, "sq60"));
  [, b] = sec("env2", "ENVELOPE", "env", [908, 528, 1314, 773]);
  const es = h("div", "grp chg"); es.innerHTML = `<div class="gt">SYNC</div>`; es.appendChild(makeItem(S(P.ESYNC, 0)));
  const ek = h("div", "grp"); ek.innerHTML = `<div class="gt"></div>`; const eits = h("div", "items");
  [[P.ED_FLT, "TO FILTER"], [P.ED_PIT, "TO PITCH"], [P.ED_SHP, "TO SHAPE"]].forEach(([id, t]) => eits.appendChild(makeItem(K(id, { tl: t, bip: true }))));
  ek.appendChild(eits); b.append(es, ek);
  const act = h("div", "sec"); act.id = "active"; act.dataset.page = "mod"; act.style.setProperty("--c", "var(--snd)");
  act.innerHTML = `<div class="ttl">ACTIVE</div><div id="actlist"></div>`;
  abs(act, 1322, 155, 1524, 773);
  for (const e of stage.querySelectorAll('[data-page="mod"]')) e.style.display = "none";
})();
ctl.slice(ctlMod).forEach(bindCtl);
// (VOICE MODE: 0 POLY 1 MONO 2 LEGATO 3 UNISON; the SOUND page's UNISON switch is the same parameter)
D[P.VOICE].names = ["POLY", "MONO", "LEGATO", "UNISON"];

// ACTIVE: the matrix's slots in use, the LFO's destinations, POLY-MOD's, ENV DEST's
const actList = document.getElementById("actlist");
function drawActive() {
  const rows = [];
  MS.forEach((m) => { if (val[m] && val[m + 1] && val[m + 2]) rows.push([N_MSRC[val[m]], N_MDST_P6[val[m + 1]], fmt(m + 2, val[m + 2])]); });
  [[P.LD_PIT, "FREQ A-B"], [P.LD_SHP, "PW A-B"], [P.LD_FLT, "FILTER"]].forEach(([id, t]) => { if (val[id]) rows.push(["LFO", t, fmt(id, val[id])]); });
  if (val[P.LD_AMP]) rows.push(["LFO", "AMP", fmt(P.LD_AMP, val[P.LD_AMP])]);
  if (val[P.PMDST] && (val[P.PMENV] || val[P.PMB])) rows.push(["POLY-MOD", ["", "FREQ A", "FILTER", "FREQ A + FILTER"][val[P.PMDST]], fmt(P.PMENV, val[P.PMENV])]);
  [[P.ED_FLT, "FILTER"], [P.ED_PIT, "PITCH"], [P.ED_SHP, "SHAPE"]].forEach(([id, t]) => { if (val[id]) rows.push(["ENV", t, fmt(id, val[id])]); });
  actList.innerHTML = rows.map(([a, b, v]) => `<div class="row arow"><div class="nm">${a} → ${b}</div><div class="av">${v}</div></div>`).join("") ||
    `<div class="hint">—</div>`;
}
const modRender = render;
render = function (only) { modRender(only); if (page === "mod") drawActive(); };
pageOpen.mod = () => { render(); if (dev) reloadValues().then(() => render()).catch((e) => console.warn(e)); };
render();
