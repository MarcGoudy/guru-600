// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the ARP page: the selected track's arpeggiator, its scale (ROOT, SCALE, QUANTIZE, TRANSPOSE) and its
// chord keys (CHORD, VOICING). Track parameters, set as the others (SET); the KEY column shows the scale's notes.
"use strict";

Object.assign(P, { AMODE: 17, ARATE: 18, AOCT: 19, AGATE: 20, ASWING: 21, APROB: 22, AHOLD: 23, AORDER: 24, ROOT: 25, SCALE: 26, QUANT: 27,
  CHRD: 81, VOIC: 82 });
const N_AMODE = ["OFF", "UP", "DN", "UPDN", "RND", "ORD", "REPEAT", "DNUP", "UP+8", "CONV", "DIVG", "PINKY", "THUMB", "WALK", "CHORD"];
const N_ROOT = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const N_SCALE = ["CHR", "MAJ", "MIN", "DOR", "MIX", "PEN", "MPEN", "HARM", "PHRY", "LYD", "LOC", "MEL", "BLUES", "WHOLE", "DIMHW", "DIMWH"];
const N_QUANT = ["OFF", "SNAP", "WHITE", "SEQ", "SEQ+T"];
const N_CHRD = ["OFF", "DIA3", "DIA7", "MAJ", "MIN", "DOM7", "MAJ7", "MIN7", "SUS4", "POW", "MEM"];
const N_VOIC = ["CLOSE", "OPEN", "INV1", "INV2", "+OCT"];
// the notes of each scale (firmware seq.c SCALE_MASK): bit k = k semitones over ROOT
const SCALE_MASK = [0xFFF, 0xAB5, 0x5AD, 0x6AD, 0x6B5, 0x295, 0x4A9, 0x9AD, 0x5AB, 0xAD5, 0x56B, 0xAAD, 0x4E9, 0x555, 0x6DB, 0xB6D];
Object.assign(D, {
  [P.AMODE]: dsc(F.ENUM, 0, 14, 0), [P.ARATE]: dsc(F.ENUM, 0, 9, 2), [P.AOCT]: dsc(F.INT, 1, 4, 1), [P.AGATE]: dsc(F.PCT, 1, 127, 64),
  [P.ASWING]: dsc(F.PCT, 0, 100, 0), [P.APROB]: dsc(F.PCT, 0, 127, 127), [P.AHOLD]: dsc(F.ONOFF, 0, 1, 0), [P.AORDER]: dsc(F.ENUM, 0, 1, 0),
  [P.ROOT]: dsc(F.ENUM, 0, 11, 0), [P.SCALE]: dsc(F.ENUM, 0, 15, 0), [P.QUANT]: dsc(F.ENUM, 0, 4, 0), [P.CHRD]: dsc(F.ENUM, 0, 10, 0),
  [P.VOIC]: dsc(F.ENUM, 0, 4, 0),
});
D[P.ARATE].names = D[P.SDIV].names; D[P.ARATE].order = D[P.SDIV].order;   // (N_DIV: shown in the FM-1's order)
Object.assign(val, { [P.AMODE]: 1, [P.ARATE]: 2, [P.AOCT]: 2, [P.AGATE]: 64, [P.ASWING]: 0, [P.APROB]: 127, [P.AHOLD]: 1, [P.AORDER]: 0,
  [P.ROOT]: 0, [P.SCALE]: 2, [P.QUANT]: 1, [P.CHRD]: 1, [P.VOIC]: 0 });
for (const id of [P.AMODE, P.ARATE, P.AOCT, P.AGATE, P.ASWING, P.APROB, P.AHOLD, P.AORDER, P.ROOT, P.SCALE, P.QUANT, P.CHRD, P.VOIC]) notSound.add(id);
METRICS.arp = { kn: 60, tlh: 22 }; METRICS.scl = { kn: 54, tlh: 20 };

// a choice as buttons (cols across), each its value lit when chosen
function choice(title, id, names, cols, cls = "") {
  const g = h("div", "grp chg " + cls);
  g.innerHTML = `<div class="gt">${title}</div>`;
  const box = h("div", "chb"); box.style.gridTemplateColumns = `repeat(${cols}, auto)`;
  const order = D[id] && D[id].order;   // (the device's order of the values: params.c SLDIV_ORDER, DTIME_ORDER)
  (order || names.map((n, v) => v)).forEach((v) => { const b = h("div", "btn ch", names[v]); box.appendChild(b); ctl.push({ kind: "selb", id, v, el: b }); });
  g.appendChild(box);
  return g;
}
// the ARP page uses its space as FX: square keys, the groups centred, SCALE's and CHORD's rows over the whole height
document.head.insertAdjacentHTML("beforeend", "<style>.chg.sq .btn.ch { width: 52px; height: 52px; min-width: 0; padding: 0; font-size: 15px; display: flex; align-items: center; justify-content: center; }.chg.sq46 .btn.ch { width: 46px; height: 46px; min-width: 0; padding: 0; font-size: 14px; display: flex; align-items: center; justify-content: center; }#arp .grp { justify-content: center; padding-top: 0; }#scl .bd.stack, #chd .bd.stack { padding-left: 0; }#scl .bd.stack > *, #chd .bd.stack > * { flex: 1 1 auto; }#scl .grp.chg > .chb, #chd .grp.chg > .chb { flex: 1; justify-content: center; }#scl .srow2 { align-items: center; padding-top: 4px; padding-bottom: 4px; }#scl .srow2 > .grp.chg:first-child { flex: 1; }</style>");
const ctlArp = ctl.length;
(function buildArp() {
  const ar = makeSection({ id: "arp", t: "ARPEGGIATOR", c: "snd", box: [12, 155, 1314, 400], groups: [] });
  const bd = ar.querySelector(".bd");
  bd.appendChild(choice("MODE", P.AMODE, N_AMODE, 5, "sq46"));
  const kn = h("div", "grp"); kn.innerHTML = `<div class="gt"></div>`;
  const its = h("div", "items");
  [[P.ARATE, "RATE"], [P.AOCT, "OCT"], [P.AGATE, "GATE"], [P.ASWING, "SWING"], [P.APROB, "PROB"]].forEach(([id, t]) => its.appendChild(makeItem(K(id, { tl: t }))));
  kn.appendChild(its); bd.appendChild(kn);
  const hd = h("div", "grp chg"); hd.innerHTML = `<div class="gt">HOLD</div>`;
  hd.appendChild(makeItem(S(P.AHOLD, 0)));
  const od = choice("ORDER", P.AORDER, ["NOTE", "PLAY"], 2, "sq46");
  const g3 = h("div", "grp chg col2"); g3.append(hd, od); bd.appendChild(g3);

  const sc = makeSection({ id: "scl", t: "SCALE", c: "snd", box: [12, 408, 830, 773], groups: [] });
  const sb = sc.querySelector(".bd"); sb.classList.add("stack");
  sb.appendChild(choice("ROOT", P.ROOT, N_ROOT, 12, "root sq"));
  sb.appendChild(choice("SCALE", P.SCALE, N_SCALE, 8, "sq"));
  const row = h("div", "srow2"); row.appendChild(choice("QUANTIZE", P.QUANT, N_QUANT, 5, "sq"));
  const tr = h("div", "grp chg"); tr.innerHTML = `<div class="gt"></div>`; tr.appendChild(makeItem(K(P.TRANS, { tl: "TRANSPOSE" }))); row.appendChild(tr);
  sb.appendChild(row);

  const ch = makeSection({ id: "chd", t: "CHORD", c: "snd", box: [838, 408, 1314, 773], groups: [] });
  const cb = ch.querySelector(".bd"); cb.classList.add("stack");
  cb.appendChild(choice("CHORD", P.CHRD, N_CHRD, 6, "sq"));
  cb.appendChild(choice("VOICING", P.VOIC, N_VOIC, 5, "sq"));

  const key = h("div", "sec"); key.id = "keycol"; key.style.setProperty("--c", "var(--snd)");
  key.innerHTML = `<div class="ttl">KEY</div><div id="keyv"></div><div id="keyname"></div>`;
  abs(key, 1322, 155, 1524, 773);
  for (const e of [ar, sc, ch, key]) { e.dataset.page = "arp"; e.style.display = "none"; e.style.setProperty("--c", "var(--snd)"); }
})();
ctl.slice(ctlArp).forEach(bindCtl);

// KEY: an octave, B at the top, C at the bottom; the scale's notes lit, ROOT marked
const keyV = document.getElementById("keyv");
function drawKey() {
  const r = val[P.ROOT], m = SCALE_MASK[val[P.SCALE]] || 0xFFF;
  let html = "", n = 0;
  for (let k = 11; k >= 0; k--) {
    const on = (m >> ((k - r + 12) % 12)) & 1;
    n += on;
    html += `<div class="ky${[1, 3, 6, 8, 10].includes(k) ? " b" : ""}${on ? " on" : ""}${k === r ? " root" : ""}"><span>${N_ROOT[k]}</span></div>`;
  }
  keyV.innerHTML = html;
  document.getElementById("keyname").textContent = `${N_ROOT[r]} ${N_SCALE[val[P.SCALE]]} · ${n} NOTES`;
}
const arpRender = render;
render = function (only) { arpRender(only); if (page === "arp" && (only == null || +only === P.ROOT || +only === P.SCALE)) drawKey(); };
pageOpen.arp = () => { render(); if (dev) reloadValues().then(() => render()).catch((e) => console.warn(e)); };
render();
