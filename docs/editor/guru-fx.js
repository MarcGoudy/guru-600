// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the FX page. The track's INSERT, SLICER and sends; the buses all tracks share (DELAY, CHORUS, REVERB:
// globals) and MASTER (TUNE, the song's GROOVE). Track parameters and globals (ids 1000 + G_*), set as the others.
"use strict";

Object.assign(P, { SLCR: 45, SLPAT: 46, SLRATE: 47, SLDEPTH: 48, ITYPE: 96, IA: 97, IB: 98, IC: 99, IMIX: 100,
  JTYPE: 103, JA: 104, JB: 105, JC: 106, JMIX: 107 });   // (INSERT 2, Guru-600 10/11: the firmware's P_JTYPE .. P_JMIX)
const G = (id) => 1000 + id;
const GV = { SWING: G(1), TUNE: G(3), DTIME: G(4), DFDBK: G(5), DCOLOR: G(6), DMIX: G(7), RSIZE: G(8), RDAMP: G(9), CRATE: G(10), CDEPTH: G(11), RTYPE: G(24) };
const N_ITYPE = ["OFF", "SOFT", "HARD", "FOLD", "FUZZ", "CRUSH", "PHASR", "FLANG", "CHOR"];
const N_DTIME = ["1/4", "1/8", "1/16", "1/32", "8T", "16T", "1/2", "1/1", "2BAR", "4BAR", "1/8D", "1/16D", "1/4D"];
const N_IBITS = Array.from({ length: 16 }, (_, k) => String(k + 1));
const N_IRATE = ["689", "919", "1.1k", "1.4k", "1.8k", "2.2k", "2.8k", "3.7k", "4.4k", "5.5k", "7.4k", "8.8k", "11k", "15k", "22k", "44k"];
Object.assign(D, {
  [P.ITYPE]: dsc(F.ENUM, 0, 8, 0), [P.IMIX]: dsc(F.PCT, 0, 127, 127), [P.JTYPE]: dsc(F.ENUM, 0, 8, 0), [P.JMIX]: dsc(F.PCT, 0, 127, 127),
  [P.SLCR]: dsc(F.ENUM, 0, 2, 0), [P.SLPAT]: dsc(F.INT, 1, 16, 1), [P.SLRATE]: dsc(F.ENUM, 0, 5, 1), [P.SLDEPTH]: dsc(F.PCT, 0, 127, 127),
  [GV.DTIME]: dsc(F.ENUM, 0, 12, 1), [GV.DFDBK]: dsc(F.PCT, 0, 120, 60), [GV.DCOLOR]: dsc(F.PCT, 0, 127, 70), [GV.DMIX]: dsc(F.PCT, 0, 127, 90),
  [GV.RSIZE]: dsc(F.PCT, 0, 127, 90), [GV.RDAMP]: dsc(F.PCT, 0, 127, 60), [GV.CRATE]: dsc(F.LFOHZ, 0, 127, 40), [GV.CDEPTH]: dsc(F.PCT, 0, 127, 60),
  [GV.RTYPE]: dsc(F.ENUM, 0, 2, 2), [GV.TUNE]: dsc(F.INT, -50, 50, 0, "ct"), [GV.SWING]: dsc(F.PCT, 0, 100, 0),
});
D[GV.DFDBK].fmt = F.INT; D[GV.DFDBK].unit = "%";   // (0..120: the value is the %)
D[P.SLRATE].order = [0, 3, 1, 4, 2, 5];                            // (as on the FM-1, params.c: 1/8 8T 1/16 16T 1/32 32T)
D[GV.DTIME].order = [9, 8, 7, 6, 12, 0, 10, 1, 11, 4, 2, 5, 3];    // (4BAR 2BAR 1/1 1/2 1/4D 1/4 1/8D 1/8 1/16D 8T 1/16 16T 1/32)
// the insert's three values as its TYPE names them (firmware params.c INS_DESC: 0..127 each)
const INS = [
  [["DRIVE", F.PCT], ["TONE", F.CUTOFF], ["LEVEL", F.DB]],
  [["BITS", F.ENUM, N_IBITS], ["RATE", F.ENUM, N_IRATE, "Hz"], ["LPF", F.CUTOFF]],
  [["RATE", F.LFOHZ], ["DEPTH", F.PCT], ["FDBK", F.PCT]]];
function insDescs() {
  for (const [ty, ids] of [[P.ITYPE, [P.IA, P.IB, P.IC]], [P.JTYPE, [P.JA, P.JB, P.JC]]]) {
  const t = val[ty], set = INS[t < 5 ? 0 : t === 5 ? 1 : 2];
  ids.forEach((id, k) => {
    const [label, fmt0, names, unit] = set[k];
    D[id] = { fmt: names ? F.ENUM16 : fmt0, min: 0, max: 127, def: 64, unit: unit || "", names: names || null };
    const c = ctl.find((x) => x.id === id); if (c && c.tlEl) c.tlEl.textContent = label;
  });
  }
}
F.ENUM16 = 101;   // (a name for each 16th of 0..127: BITS, RATE of CRUSH)
for (const id of [P.ITYPE, P.IMIX, P.SLCR, P.SLPAT, P.SLRATE, P.SLDEPTH, P.IA, P.IB, P.IC, P.JTYPE, P.JA, P.JB, P.JC, P.JMIX, ...Object.values(GV)]) notSound.add(id);
Object.assign(val, { [P.ITYPE]: 3, [P.IA]: 64, [P.IB]: 80, [P.IC]: 96, [P.IMIX]: 127, [P.JTYPE]: 0, [P.JA]: 64, [P.JB]: 96, [P.JC]: 96, [P.JMIX]: 127, [P.SLCR]: 1, [P.SLPAT]: 5, [P.SLRATE]: 1, [P.SLDEPTH]: 127,
  [GV.DTIME]: 1, [GV.DFDBK]: 60, [GV.DCOLOR]: 70, [GV.DMIX]: 90, [GV.RSIZE]: 90, [GV.RDAMP]: 60, [GV.CRATE]: 40, [GV.CDEPTH]: 60,
  [GV.RTYPE]: 2, [GV.TUNE]: 0, [GV.SWING]: 0 });
insDescs();
const fxFmt = fmt;
fmt = function (id, v) {   // (BITS, CRUSH's RATE: the 16th of the range named)
  const d = D[id];
  if (d && d.fmt === F.ENUM16) return d.names[Math.min(15, v >> 3)] + (d.unit ? " " + d.unit : "");
  return fxFmt(id, v);
};

METRICS.fxi = { kn: 56, tlh: 22 }; METRICS.fxsl = { kn: 56, tlh: 22 }; METRICS.fxd = { kn: 56, tlh: 22 };
METRICS.fxdl = { kn: 54, tlh: 22 }; METRICS.fxc = { kn: 54, tlh: 22 }; METRICS.fxr = { kn: 54, tlh: 22 }; METRICS.fxm = { kn: 74, tlh: 26 };
const ctlFx = ctl.length;
let insSel = 0, insShow = () => {}, insGrid = [];   // (which INSERT the box shows: 0 the first, 1 the second; the TYPE grid)
function insLight() {   // the grid: the chosen INSERT's type lit, the other's dimmer, each with its number; OFF: the chosen one's
  const t1 = val[P.ITYPE] | 0, t2 = val[P.JTYPE] | 0, mine = insSel ? t2 : t1, other = insSel ? t1 : t2;
  for (const c of insGrid) {
    const n = (c.v && c.v === t1 ? "1" : "") + (c.v && c.v === t2 ? "2" : "");
    const dim = !!c.v && c.v === other && c.v !== mine;
    c.el.classList.toggle("on", c.v === mine || dim);
    c.el.classList.toggle("dimon", dim);   // (Marc, 10/11: the other INSERT's, less bright)
    if (n) c.el.dataset.ins = n.split("").join(" "); else delete c.el.dataset.ins;
  }
}
document.head.insertAdjacentHTML("beforeend", "<style>.grp.distg { position: relative; } .grp.distg::after { content: ''; position: absolute; right: -2px; top: var(--cut, 0); bottom: 0; border-right: 2px solid var(--fx); }" +
  "#fxi .grp.insgrid { border-left: 0; }" +   // (INSERT 1 / 2 open onto the TYPE grid: Marc, 10/11)
  ".grp.distg { justify-content: stretch; padding-top: 0; padding-bottom: 0; } .grp.distg > .distk { flex: 1 1 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }" +
  ".inspick { flex: 1 1 0; justify-content: center; border-bottom: 1.5px solid var(--fx); align-self: stretch; display: flex; flex-direction: column; align-items: center; }" +   // (a blue line: DIST apart from INSERT 1 / 2)
  ".chg .btn.ch.on.dimon { filter: brightness(.72); } .chg .btn.ch.on[data-ins]:not(.dimon) { filter: brightness(1.2); }" +   // (the chosen
                                                         // INSERT's type brighter, the other's dimmer: Marc, 10/11)   // (the other INSERT's: the same light, weaker)
  ".chg .btn.ch[data-ins] { position: relative; } .chg .btn.ch[data-ins]::after { content: attr(data-ins); position: absolute; right: 3px; top: 1px; font: 700 11px/1 'Barlow C'; }" +
  ".inspick .gt { margin-bottom: 6px; } .inspick .ipb { display: flex; gap: 6px; } .inspick .btn { width: 40px; height: 34px; min-width: 0; padding: 0; display: flex; align-items: center; justify-content: center; }</style>");
(function buildFx() {
  const sec = (id, t, box) => { const e = makeSection({ id, t, c: "fx", box, groups: [] }); e.dataset.page = "fx"; e.style.setProperty("--onc", "var(--fx)");
    return [e, e.querySelector(".bd")]; };   // (--onc: what is chosen lit in the page's blue)
  const knobs = (list) => { const g = h("div", "grp"); g.innerHTML = `<div class="gt"></div>`; const its = h("div", "items");
    list.forEach(([id, t]) => { const it = makeItem(K(id, { tl: t })); its.appendChild(it); const c = ctl[ctl.length - 1]; c.tlEl = it.querySelector(".tl"); }); g.appendChild(its); return g; };
  const grid2x2 = (g) => { g.classList.add("k2x2"); return g; };   // (INSERT's four knobs, two by two)
  const spread = (g) => { g.classList.add("spread"); return g; };   // (the knobs over the width left)
  const lab = (t, x, y) => { const e = h("div", "fxlab", t); e.dataset.page = "fx"; abs(e, x, y, x + 300, y + 18); };
  lab("TRACK 1", 14, 153); lab("ALL TRACKS", 14, 463);
  // (the sound's path, left to right: DIST, the INSERT, the SLICER, the sends; below, the buses in the sends' order)
  let [, b] = sec("fxi", "INSERT", [12, 172, 662, 455]);
  {   // DIST, then INSERT 1 or 2 (the two buttons under DIST choose which is shown: both always play, 1 then 2)
    const dist = knobs([[P.DIST, "DIST"]]);
    const pick = h("div", "inspick"); pick.innerHTML = `<div class="gt">INSERT</div><div class="ipb"><div class="btn ch on" data-k="0">1</div><div class="btn ch" data-k="1">2</div></div>`;
    const dk = h("div", "distk"); dk.append(...dist.children); dist.append(pick, dk);   // (INSERT 1 / 2 at the top, by the TYPE
                                                                                       //  grid; DIST under the blue rule: Marc, 10/11)
    // one TYPE grid for both (Marc, 10/11: both types lit together, a 1 / 2 in the corner); a click sets the INSERT chosen
    const c0 = ctl.length, grid = choice("TYPE", P.ITYPE, N_ITYPE, 3, "sq");
    insGrid = ctl.slice(c0).filter((c) => c.kind === "selb");
    grid.addEventListener("pointerdown", (e) => {
      const btn = e.target.closest(".btn"); if (!btn || !insSel) return;
      const c = insGrid.find((x) => x.el === btn); if (!c) return;
      e.preventDefault(); e.stopPropagation(); setVal(P.JTYPE, c.v);
    }, true);
    const one = [grid2x2(knobs([[P.IA, "DRIVE"], [P.IB, "TONE"], [P.IC, "LEVEL"], [P.IMIX, "MIX"]]))];
    const two = [grid2x2(knobs([[P.JA, "DRIVE"], [P.JB, "TONE"], [P.JC, "LEVEL"], [P.JMIX, "MIX"]]))];
    b.append(dist, grid, ...one, ...two);
    dist.classList.add("distg"); grid.classList.add("insgrid");
    const cut = () => dist.style.setProperty("--cut", (pick.offsetTop + pick.offsetHeight) + "px");   // (DIST's line: from the blue rule down)
    requestAnimationFrame(cut); new ResizeObserver(cut).observe(dist);
    insShow = (k) => {
      insSel = k;
      for (const e of one) e.style.display = k ? "none" : "";
      for (const e of two) e.style.display = k ? "" : "none";
      pick.querySelectorAll(".btn").forEach((x) => x.classList.toggle("on", +x.dataset.k === k));
      insLight();
    };
    pick.querySelectorAll(".btn").forEach((x) => x.addEventListener("pointerdown", () => insShow(+x.dataset.k)));
    insShow(0);
  }
  [, b] = sec("fxsl", "SLICER", [670, 172, 1072, 455]);
  b.classList.add("stack");
  const r1 = h("div", "srow2"); r1.append(choice("MODE", P.SLCR, ["OFF", "GATE", "STUT"], 3, "sq"), knobs([[P.SLPAT, "PATTERN"], [P.SLDEPTH, "DEPTH"]]));
  b.append(r1, choice("RATE", P.SLRATE, ["1/8", "1/16", "1/32", "8T", "16T", "32T"], 6, "sq"));
  [, b] = sec("fxd", "SENDS", [1080, 172, 1314, 455]);
  b.append(knobs([[P.CHOR, "CHORUS"], [P.DLY, "DELAY"], [P.REV, "REVERB"]]));
  [, b] = sec("fxdl", "DELAY", [252, 482, 940, 773]);
  b.append(choice("TIME", GV.DTIME, N_DTIME, 7, "sq"), spread(knobs([[GV.DFDBK, "FEEDBACK"], [GV.DCOLOR, "COLOR"], [GV.DMIX, "MIX"]])));
  [, b] = sec("fxc", "CHORUS", [12, 482, 244, 773]);
  b.classList.add("stack");
  b.append(knobs([[GV.CRATE, "RATE"]]), knobs([[GV.CDEPTH, "DEPTH"]]));
  [, b] = sec("fxr", "REVERB", [948, 482, 1314, 773]);
  b.classList.add("stack");
  b.append(choice("TYPE", GV.RTYPE, ["ROOM", "SPRING", "HALL"], 3, "sq"), knobs([[GV.RSIZE, "SIZE"], [GV.RDAMP, "DAMP"]]));
  const [m, mb] = sec("fxm", "MASTER", [1322, 172, 1524, 773]);
  mb.classList.add("stack");
  mb.append(knobs([[GV.TUNE, "TUNE"]]), knobs([[GV.SWING, "GROOVE"]]));
  m.insertAdjacentHTML("beforeend", `<div class="fxhint">TUNE: ALL TRACKS · GROOVE: THE SONG'S SWING</div>`);
  for (const e of stage.querySelectorAll('[data-page="fx"]')) e.style.display = "none";
})();
ctl.slice(ctlFx).forEach(bindCtl);
// the TRACK n heading follows the track; the insert's knobs their TYPE
const fxRender = render;
render = function (only) {
  const ty = only == null || +only === P.ITYPE || +only === P.JTYPE;
  if (ty) insDescs();
  fxRender(only);
  if (ty) for (const id of [P.IA, P.IB, P.IC, P.JA, P.JB, P.JC]) fxRender(id);
  insLight();
  const l = stage.querySelector('.fxlab'); if (l) l.textContent = "TRACK " + (track + 1);
  fxSendsShow();
};
// DELAY, CHORUS, REVERB are heard on the track only through its send: at 0 % the box is dimmed and says so (its knobs
// still work: the other tracks may send to it)
document.head.insertAdjacentHTML("beforeend", "<style>#fxdl > .ttl, #fxc > .ttl, #fxr > .ttl { position: relative; }" +
  ".sendhint { position: absolute; right: 10px; top: 0; font: 600 16px/34px 'Barlow C'; color: var(--cream); display: none; }" +
  ".sec.nosend .sendhint { display: block; }" +
  ".sec.nosend > .bd { opacity: .38; }</style>");
// the FX page uses its space: every group centred in its box, the rows and stacks spread evenly (Marc, 10/11)
document.head.insertAdjacentHTML("beforeend", "<style>.sec[data-page=fx] .grp { justify-content: center; padding-top: 0; }.sec[data-page=fx] .bd.stack { justify-content: space-evenly; padding-left: 0; }.sec[data-page=fx] .bd.stack > .grp, .sec[data-page=fx] .srow2 > .grp { align-items: center; padding-top: 0; flex: 0 0 auto; }.sec[data-page=fx] .srow2 { display: flex; justify-content: space-evenly; align-items: center; width: 100%; }.sec[data-page=fx] .chb { justify-content: center; }</style>");
// the choices of the FX page as square keys (INSERT TYPE in a 3 x 3 grid)
document.head.insertAdjacentHTML("beforeend", "<style>#fxi > .bd > .grp { flex: 1; } .grp.k2x2 > .items { display: grid; grid-template-columns: repeat(2, auto); gap: 6px 26px; justify-content: center; }</style>");
document.head.insertAdjacentHTML("beforeend", "<style>.grp.spread { flex: 1; } .grp.spread > .items { justify-content: space-evenly; width: 100%; }</style>");
document.head.insertAdjacentHTML("beforeend", "<style>.chg.sq .btn.ch { width: 52px; height: 52px; min-width: 0; padding: 0; font-size: 15px; display: flex; align-items: center; justify-content: center; }</style>");
const FX_SENDS = [["fxdl", P.DLY], ["fxc", P.CHOR], ["fxr", P.REV]];
for (const [id] of FX_SENDS) document.querySelector(`#${id} > .ttl`).insertAdjacentHTML("beforeend", `<span class="sendhint"></span>`);
function fxSendsShow() {
  for (const [id, p] of FX_SENDS) {
    const e = document.getElementById(id), off = !val[p];
    e.classList.toggle("nosend", off);
    if (off) e.querySelector(".sendhint").textContent = "TRACK " + (track + 1) + " · SEND 0 %";
  }
}
pageOpen.fx = () => { render(); if (dev) reloadValues().then(() => render()).catch((e) => console.warn(e)); };
render();
