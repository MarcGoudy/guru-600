// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the SEQUENCER page (the selected track's 64 steps, its LEN DIV SWING GATE QUANTIZE TRANSPOSE, the
// tools, its automation). Felucca's STEP_GET / STEP_SET / MOTION, Guru-600's TOOL (firmware editor.c ed_p6).
"use strict";

/* -------------------------------------------------------------------------------- the parameters --- */
Object.assign(P, { TRANS: 28, SLEN: 29, SDIV: 30, SSWING: 31, SGATE: 32, SQNT: 94 });
Object.assign(D, {
  [P.SLEN]: dsc(F.INT, 1, 64, 16), [P.SDIV]: dsc(F.ENUM, 0, 9, 2), [P.SSWING]: dsc(F.PCT, 0, 100, 0), [P.SGATE]: dsc(F.PCT, 1, 127, 64),
  [P.SQNT]: dsc(F.ONOFF, 0, 1, 1), [P.TRANS]: dsc(F.INT, -24, 24, 0, "st"),
});
D[P.SDIV].names = ["1/4", "1/8", "1/16", "1/32", "8T", "16T", "1/2", "1/1", "2BAR", "4BAR"];
D[P.SDIV].order = [9, 8, 7, 6, 0, 1, 4, 2, 5, 3];   // (shown as on the FM-1: 4BAR 2BAR 1/1 1/2 1/4 1/8 8T 1/16 16T 1/32)
Object.assign(val, { [P.SLEN]: 16, [P.SDIV]: 2, [P.SSWING]: 50, [P.SGATE]: 95, [P.SQNT]: 1, [P.TRANS]: 0 });
for (const id of [P.TRANS, P.SLEN, P.SDIV, P.SSWING, P.SGATE, P.SQNT]) notSound.add(id);
METRICS.sq = { kn: 50, tlh: 20 };

// the names the automation list gives the parameters it holds
const PNAME = { [P.CUT]: "CUTOFF", [P.RES]: "RESONANCE", [P.FENV]: "ENV AMOUNT", [P.MIX]: "MIXER", [P.GLIDE]: "GLIDE", [P.AFRQ]: "FREQ A",
  [P.BFRQ]: "FREQ B", [P.APW]: "PW A", [P.BPW]: "PW B", [P.BFIN]: "FINE B", [P.PMENV]: "PM FIL ENV", [P.PMB]: "PM OSC B", [P.ATK]: "AMP ATTACK",
  [P.DEC]: "AMP DECAY", [P.SUS]: "AMP SUSTAIN", [P.REL]: "AMP RELEASE", [P.FATK]: "FLT ATTACK", [P.FDEC]: "FLT DECAY", [P.FSUS]: "FLT SUSTAIN",
  [P.FREL]: "FLT RELEASE", [P.LRATE]: "LFO FREQ", [P.VINT]: "VINTAGE", [P.WHEEL]: "WHEEL", [P.VEL]: "VEL > FLT", [P.DETUNE]: "DETUNE",
  [P.LEVEL]: "LEVEL", [P.PAN]: "PAN", [P.SPRD]: "SPREAD", [P.DIST]: "DIST", [P.CHOR]: "CHORUS", [P.DLY]: "DELAY", [P.REV]: "REVERB",
  [P.AWAV]: "WAVE A", [P.BWAV]: "WAVE B" };

/* ----------------------------------------------------------------------------------- the steps --- */
const NSTEP = 64, COND = ["", "1:2", "2:2", "1:3", "2:3", "3:3", "1:4", "2:4", "3:4", "4:4", "FILL", "!FILL"];
const TIME = { NOTE: 0, TIE: 1, REST: 2 };
const emptyStep = () => ({ n: 0, notes: [0, 0, 0, 0], time: 0, flags: 0, vel: 96, hit: 0, acc: 0, chance: 100, ratchet: 1, nudge: 0, cond: 0 });
let steps = Array.from({ length: NSTEP }, emptyStep);
// the mockup's sequence while no FM-1 is there
(() => {
  const bass = [48, 0, 55, 0, 52, 0, 55, 0, 53, 0, 52, 0, 55, 0, 55, 0];
  bass.forEach((n, i) => { if (n) Object.assign(steps[i], { n: 1, notes: [n, 0, 0, 0], vel: 70 + (i * 13) % 50 }); });
  Object.assign(steps[4], { n: 3, notes: [55, 59, 62, 0] });
  Object.assign(steps[8], { notes: [57, 0, 0, 0] }); steps[9].time = TIME.TIE;
  steps[11] = Object.assign(emptyStep(), { time: TIME.REST });
  steps[0].flags = 1; steps[8].flags = 1; steps[12].flags = 2;
  steps[5].chance = 75; steps[13].chance = 50; steps[7].ratchet = 2; steps[15].ratchet = 4;
  steps[2].nudge = 2; steps[10].nudge = -1; steps[3].cond = 1; steps[11].cond = 7;
})();
let seqPage = 0, playing = -1;                // the page of 16 shown; the step playing (-1: stopped)
let rollLo = 48;                               // the lowest note shown (C3); the roll shows ROWS

/* --------------------------------------------------------------------------------------- the page --- */
const SQ = { x0: 12, x1: 1314, seqY: [155, 300], stepsY: [308, 562], detY: [570, 773] };
function seqSection(id, title, box) {
  const e = h("div", "sec"); e.style.setProperty("--c", "var(--snd)"); e.id = id; e.dataset.page = "seq";
  e.appendChild(h("div", "ttl", title));
  const bd = h("div", "bd"); e.appendChild(bd);
  abs(e, ...box);
  return [e, bd];
}
const ctl0 = ctl.length;
(function buildSeq() {
  // SEQUENCE: six settings, the pages, the tools
  const sec = makeSection({ id: "sq", t: "SEQUENCE", c: "snd", box: [SQ.x0, SQ.seqY[0], SQ.x1, SQ.seqY[1]], groups: [
    { t: "", items: [K(P.SLEN, { tl: "LEN" }), K(P.SDIV, { tl: "DIV" }), K(P.SSWING, { tl: "SWING" }), K(P.SGATE, { tl: "GATE" }),
      S(P.SQNT, 0, { tl: "QUANTIZE" }), K(P.TRANS, { tl: "TRANSPOSE" })] }] });
  sec.dataset.page = "seq";
  sec.style.setProperty("--c", "var(--snd)");
  const bd = sec.querySelector(".bd");
  const gp = h("div", "grp sqgrp"); gp.innerHTML = `<div class="gt">STEPS</div><div class="pages"></div>`;
  ["1-16", "17-32", "33-48", "49-64"].forEach((t, i) => { const b = h("div", "btn pg" + (i ? "" : " on"), t); b.dataset.pg = i; gp.querySelector(".pages").appendChild(b); });
  const gt = h("div", "grp sqgrp"); gt.innerHTML = `<div class="gt">TOOLS</div><div class="tools"></div>`;
  [[0, "CLEAR"], [1, "REVERSE"], [2, "SHIFT ◀"], [3, "SHIFT ▶"], [4, "RANDOM"], [5, "COOK"], [7, "EUCLID"], [12, "DOUBLE"], [13, "HALF"]]
    .forEach(([p, t]) => { const b = h("div", "btn tool", t); b.dataset.tool = p; gt.querySelector(".tools").appendChild(b); });
  bd.append(gp, gt);

  // STEPS: the roll
  const [, sb] = seqSection("sqsteps", "STEPS", [SQ.x0, SQ.stepsY[0], SQ.x1, SQ.stepsY[1]]);
  sb.innerHTML = `<div id="rollkeys"></div><div id="roll"><div id="rollhead"></div><div id="rollgrid"><div id="rollph"></div><div id="rollnotes"></div></div></div>`;

  // DETAIL: seven lanes under the roll's columns
  const [, db] = seqSection("sqdet", "DETAIL", [SQ.x0, SQ.detY[0], SQ.x1, SQ.detY[1]]);
  const lanes = ["VELOCITY", "ACCENT", "SLIDE", "CHANCE", "RATCH", "NUDGE", "COND"];
  db.innerHTML = `<div id="detlabels">${lanes.map((l) => `<div>${l}</div>`).join("")}</div><div id="detgrid"></div>`;

  // AUTOMATION: the column of SOUNDS
  const au = h("div", "sec"); au.id = "auto"; au.dataset.page = "seq"; au.style.setProperty("--c", "var(--snd)");
  au.innerHTML = `<div class="ttl">AUTOMATION</div><div class="autoplay"><span>PLAY</span><div class="hsw" id="autoon"></div></div>` +
    `<div id="autolist"></div><div class="autobtn"><div class="btn" id="b-autodel">DELETE</div><div class="btn" id="b-autoclr">CLEAR ALL</div></div>`;
  abs(au, 1322, 308, 1524, 773);

  // SOUND: the selected track's sound, above AUTOMATION (its engine, then ◀ the sound ▶)
  const so = h("div", "sec"); so.id = "sqsound"; so.dataset.page = "seq"; so.style.setProperty("--c", "var(--snd)");
  so.innerHTML = `<div class="ttl">SOUND</div><div class="sqeng" id="sqeng"></div>` +
    `<div class="sqsnd"><div class="arr l" id="sqs-"></div><div class="field" id="sqsf"></div><div class="arr r" id="sqs+"></div></div>`;
  abs(so, 1322, 155, 1524, 300);
  for (const e of stage.querySelectorAll('[data-page="seq"]')) e.style.display = "none";
})();
ctl.slice(ctl0).forEach(bindCtl);
render();
layout();   // (the new sections placed, their knobs centred)

const rollKeys = document.getElementById("rollkeys"), rollHead = document.getElementById("rollhead"), rollGrid = document.getElementById("rollgrid");
const rollNotes = document.getElementById("rollnotes"), rollPh = document.getElementById("rollph"), detGrid = document.getElementById("detgrid");
const ROWS = 15;   // an octave and some (the wheel scrolls)
const black = (n) => [1, 3, 6, 8, 10].includes(n % 12);
const noteName = (n) => ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][n % 12] + (Math.floor(n / 12) - 1);

// the roll's background: a row per note (black keys darker), a column per step (a stronger line every 4)
function drawRollFrame() {
  rollKeys.replaceChildren(); rollHead.replaceChildren();
  for (let r = 0; r < ROWS; r++) {
    const n = rollLo + ROWS - 1 - r, k = h("div", "rk" + (black(n) ? " b" : ""));
    if (n % 12 === 0) k.dataset.c = noteName(n);
    rollKeys.appendChild(k);
  }
  for (let c = 0; c < 16; c++) {
    const i = seqPage * 16 + c, e = h("div", "rh" + (c % 4 === 0 ? " bar" : "") + (i >= val[P.SLEN] ? " out" : ""), String(i + 1));
    e.dataset.c = c; rollHead.appendChild(e);
  }
  const rows = [];
  for (let r = 0; r < ROWS; r++) { const n = rollLo + ROWS - 1 - r; rows.push(black(n) ? "#0d0d0d" : "#141414"); }
  rollGrid.style.setProperty("--rows", rows.map((c, r) => `${c} ${(r * 100 / ROWS).toFixed(3)}% ${((r + 1) * 100 / ROWS).toFixed(3)}%`).join(","));
}
// the notes: a bar per note of each step, a TIE carrying the bar on; REST marked
function drawRoll() {
  rollNotes.replaceChildren();
  const len = val[P.SLEN];
  for (let c = 0; c < 16; c++) {
    const i = seqPage * 16 + c, s = steps[i];
    if (i >= len) continue;
    if (s.time === TIME.REST) {   // (marked where it cuts a note: an empty step is a REST too on the FM-1)
      const p = i ? steps[i - 1] : null;
      if (p && ((p.time === TIME.NOTE && p.n) || p.time === TIME.TIE)) { const e = h("div", "rest", "REST"); e.style.left = (c * 100 / 16) + "%"; rollNotes.appendChild(e); }
      continue;
    }
    if (s.time === TIME.TIE) continue;
    if (!s.n) continue;
    let span = 1;
    while (c + span < 16 && seqPage * 16 + c + span < len && steps[i + span].time === TIME.TIE) span++;
    for (let k = 0; k < s.n; k++) {
      const n = s.notes[k], r = rollLo + ROWS - 1 - n;
      if (r < 0 || r >= ROWS) continue;
      const e = h("div", "nt" + (span > 1 ? " tie" : ""));
      e.style.left = `calc(${c * 100 / 16}% + 3px)`; e.style.width = `calc(${span * 100 / 16}% - 6px)`;
      e.style.top = `calc(${r * 100 / ROWS}% + 1.5px)`; e.style.height = `calc(${100 / ROWS}% - 3px)`;
      e.style.setProperty("--v", (0.45 + 0.55 * s.vel / 127).toFixed(2));
      if (span > 1 && k === 0) e.dataset.tie = "TIE";
      rollNotes.appendChild(e);
    }
  }
  seqPlayhead(playing);
}
function seqPlayhead(i) {
  playing = i;
  const c = i - seqPage * 16, on = i >= 0 && c >= 0 && c < 16;
  rollPh.style.display = on ? "" : "none";
  if (on) rollPh.style.left = (c * 100 / 16) + "%";
  for (const e of rollHead.children) e.classList.toggle("ph", on && +e.dataset.c === c);
  for (const e of detGrid.querySelectorAll(".dc")) e.classList.toggle("ph", on && +e.dataset.c === c);
}
// the details, column by column
function drawDetail() {
  detGrid.replaceChildren();
  const len = val[P.SLEN];
  for (let c = 0; c < 16; c++) {
    const i = seqPage * 16 + c, s = steps[i], col = h("div", "dc" + (i >= len ? " out" : "") + (c % 4 === 0 ? " bar" : ""));
    col.dataset.c = c;
    const on = s.time === TIME.NOTE && s.n;
    col.innerHTML = `<div class="ln vel${on ? "" : " nn"}" data-k="vel"><i style="height:${on ? Math.round(s.vel * 100 / 127) : 0}%"></i></div>` +
      `<div class="ln" data-k="acc"><b class="led${s.flags & 1 ? " on" : ""}"></b></div>` +
      `<div class="ln" data-k="sld"><b class="led${s.flags & 2 ? " on" : ""}"></b></div>` +
      `<div class="ln num" data-k="chance">${s.cond ? "" : s.chance}</div>` +
      `<div class="ln num" data-k="rat">×${s.ratchet}</div>` +
      `<div class="ln num" data-k="nud">${s.nudge > 0 ? "+" + s.nudge : s.nudge < 0 ? "−" + -s.nudge : "0"}</div>` +
      `<div class="ln num" data-k="cond">${COND[s.cond] || ""}</div>`;
    detGrid.appendChild(col);
  }
  seqPlayhead(playing);
}
function drawSeq() { drawRollFrame(); drawRoll(); drawDetail(); }

/* --------------------------------------------------------------------------------------- editing --- */
const writing = new Map();   // step -> its last write in flight (each step written as it is, in order)
function putStep(i, s) {
  steps[i] = s; drawRoll(); drawDetail();
  if (!dev) return;
  const w = (writing.get(i) || Promise.resolve()).then(() => dev.stepSet(i, s)).catch(() => toast(tx("noreply")));
  writing.set(i, w);
}
const copy = (s) => ({ ...s, notes: [...s.notes] });
// a click in the roll: the note there on or off (a chord: up to 4)
rollGrid.addEventListener("pointerdown", (e) => {
  const r = rollGrid.getBoundingClientRect(), c = Math.floor((e.clientX - r.left) / r.width * 16), row = Math.floor((e.clientY - r.top) / r.height * ROWS);
  const i = seqPage * 16 + c, n = rollLo + ROWS - 1 - row;
  if (c < 0 || c > 15 || row < 0 || row >= ROWS || i >= val[P.SLEN]) return;
  const s = copy(steps[i]);
  if (s.time !== TIME.NOTE) { s.time = TIME.NOTE; s.n = 0; }
  const k = s.notes.slice(0, s.n).indexOf(n);
  if (k >= 0) { s.notes.splice(k, 1); s.notes.push(0); s.n--; }
  else if (s.n < 4) { s.notes[s.n++] = n; }
  else return toast(tx("chord4"));
  putStep(i, s);
  if (k < 0 && dev) { dev.link.out.send([0x90 | track, n, s.vel || 96]); setTimeout(() => dev && dev.link.out.send([0x80 | track, n, 0]), 180); }
});
rollGrid.addEventListener("wheel", (e) => { e.preventDefault(); rollLo = Math.max(12, Math.min(96, rollLo + (e.deltaY < 0 ? 1 : -1))); drawRollFrame(); drawRoll(); }, { passive: false });
// a click on a step's number: NOTE, TIE, REST in turn
rollHead.addEventListener("pointerdown", (e) => {
  const c = e.target.dataset && e.target.dataset.c; if (c == null) return;
  const i = seqPage * 16 + +c; if (i >= val[P.SLEN]) return;
  const s = copy(steps[i]); s.time = (s.time + 1) % 3; putStep(i, s);
});
// the details: a drag up / down (VELOCITY, CHANCE, NUDGE), a click (ACCENT, SLIDE, RATCH, COND)
detGrid.addEventListener("pointerdown", (e) => {
  const ln = e.target.closest(".ln"), col = e.target.closest(".dc"); if (!ln || !col) return;
  const i = seqPage * 16 + +col.dataset.c, k = ln.dataset.k; if (i >= val[P.SLEN]) return;
  const s = copy(steps[i]);
  if (k === "acc") { s.flags ^= 1; return putStep(i, s); }
  if (k === "sld") { s.flags ^= 2; return putStep(i, s); }
  if (k === "rat") { s.ratchet = s.ratchet % 4 + 1; return putStep(i, s); }
  if (k === "cond") { s.cond = (s.cond + 1) % COND.length; if (s.cond) s.chance = 100; return putStep(i, s); }
  const span = { vel: [1, 127], chance: [0, 100], nud: [-8, 7] }[k]; if (!span) return;
  e.preventDefault(); ln.setPointerCapture(e.pointerId);
  const key = { vel: "vel", chance: "chance", nud: "nudge" }[k], v0 = s[key], y0 = e.clientY;
  const sc = () => stage.getBoundingClientRect().width / stage.offsetWidth;
  if (k === "vel") {   // VELOCITY: where it is clicked in the lane
    const r = ln.getBoundingClientRect(); s.vel = Math.max(1, Math.min(127, Math.round((1 - (e.clientY - r.top) / r.height) * 127)));
    if (!(s.time === TIME.NOTE && s.n)) return; putStep(i, s);
  }
  const mv = (ev) => {
    const d = Math.round((y0 - ev.clientY) / sc() * (span[1] - span[0]) / 120);
    const t = copy(steps[i]);
    t[key] = Math.max(span[0], Math.min(span[1], (k === "vel" ? s.vel : v0) + d));
    if (k === "chance") t.cond = 0;
    if (t[key] !== steps[i][key]) putStep(i, t);
  };
  const up = () => { ln.removeEventListener("pointermove", mv); ln.removeEventListener("pointerup", up); };
  ln.addEventListener("pointermove", mv); ln.addEventListener("pointerup", up);
});
// a double click on a detail's name: that row back to its usual value on every step of the sequence (Marc, 10/11)
document.getElementById("detlabels").addEventListener("dblclick", (e) => {
  const row = e.target.closest("#detlabels > div"); if (!row) return;
  const k = ["vel", "acc", "sld", "chance", "rat", "nud", "cond"][[...row.parentElement.children].indexOf(row)];
  const set = { vel: (t) => { t.vel = 96; }, acc: (t) => { t.flags &= ~1; }, sld: (t) => { t.flags &= ~2; }, chance: (t) => { t.chance = 100; },
    rat: (t) => { t.ratchet = 1; }, nud: (t) => { t.nudge = 0; }, cond: (t) => { t.cond = 0; } }[k];
  if (!set) return;
  for (let i = 0; i < val[P.SLEN]; i++) {
    const t = copy(steps[i]); set(t);
    if (JSON.stringify(t) !== JSON.stringify(steps[i])) putStep(i, t);
  }
  window.getSelection().removeAllRanges();
});
// the pages of 16
document.querySelectorAll("#sq .pg").forEach((b) => b.addEventListener("pointerdown", () => {
  seqPage = +b.dataset.pg; document.querySelectorAll("#sq .pg").forEach((o) => o.classList.toggle("on", o === b)); drawSeq();
}));
// the tools: the FM-1 does them (as SEQ TOOLS), then its steps are read again
let euclid = { hits: 5, steps: 16, rot: 0 };
document.querySelectorAll("#sq .tool").forEach((b) => b.addEventListener("click", async () => {
  if (!dev) return toast(tx("offline"));
  const p = +b.dataset.tool;
  if (p === 0 && !await uiConfirm(tx("seqclear"))) return;
  if (p === 7) {
    const a = await uiPrompt(tx("euclid"), `${euclid.hits} ${euclid.steps} ${euclid.rot}`);
    if (a == null) return;
    const [hh, ss, rr] = a.trim().split(/[\s,/]+/).map(Number);
    if (!(ss >= 1 && ss <= 64 && hh >= 0 && hh <= ss)) return toast(tx("euclidbad"));
    euclid = { hits: hh, steps: ss, rot: Math.max(0, Math.min(ss - 1, rr | 0)) };
  }
  try {
    const rc = await dev.tool(p, euclid.hits, euclid.steps, euclid.rot);
    if (rc === 2) return toast(tx("notools"));
    if (rc === 1) return toast(tx("toolnone"));
    await seqRead();
    toast(b.textContent);
  } catch (e) { toast(tx("noreply")); }
}));

/* ------------------------------------------------------------------------------------ automation --- */
let auto = { on: true, demo: true, list: [   // (offline: an example; connected, the FM-1's own, read at once)
  { step: 2, id: P.CUT, v: 81, lock: false }, { step: 6, id: P.RES, v: 38, lock: false }, { step: 8, id: P.FENV, v: 102, lock: false },
  { step: 11, id: P.MIX, v: 64, lock: false }, { step: 4, id: P.CUT, v: 51, lock: true }, { step: 12, id: P.GLIDE, v: 70, lock: true }] }, autoSel = 1;
const autoList = document.getElementById("autolist"), autoOn = document.getElementById("autoon");
function drawAuto() {
  autoOn.classList.toggle("on", auto.on);
  document.getElementById("b-autodel").classList.toggle("dis", !auto.list[autoSel]);   // (nothing to delete: grey)
  document.getElementById("b-autoclr").classList.toggle("dis", !auto.list.length);
  autoList.replaceChildren();
  if (!auto.list.length) autoList.appendChild(h("div", "ahint", tx("autoempty")));   // (an empty list explains itself)
  auto.list.forEach((m, k) => {
    const v = D[m.id] ? fmt(m.id, m.v) : String(m.v);
    const r = h("div", "row arow" + (k === autoSel ? " on" : "") + (m.lock ? " lock" : ""),
      `${m.lock ? '<svg class="lk" viewBox="0 0 12 14"><rect x="1" y="6" width="10" height="7.5" rx="1.5"/><path d="M3.5 6V4a2.5 2.5 0 0 1 5 0v2" fill="none" stroke-width="1.6"/></svg>' : ""}` +
      `<div class="n">${m.step + 1}</div><div class="nm">${PNAME[m.id] || "PARAM " + m.id}</div><div class="av">${v}</div>`);
    r.addEventListener("pointerdown", () => { autoSel = k; drawAuto(); });
    autoList.appendChild(r);
  });
}
autoOn.addEventListener("pointerdown", async () => {
  auto.on = !auto.on; drawAuto();
  if (dev) try { await dev.motionOp(track, 1, [auto.on ? 1 : 0]); } catch (e) { toast(tx("noreply")); }
});
document.getElementById("b-autodel").addEventListener("click", async () => {
  const m = auto.list[autoSel]; if (!m) return;
  if (dev) try { const r = await dev.motionOp(track, 4, [m.step & 63, m.id & 127]); if (r[1]) return toast(tx(r[1] === 3 ? "songbusy" : "noreply")); } catch (e) { return toast(tx("noreply")); }
  auto.list.splice(autoSel, 1); autoSel = Math.min(autoSel, auto.list.length - 1); drawAuto();
});
document.getElementById("b-autoclr").addEventListener("click", async () => {
  if (!auto.list.length || !await uiConfirm(tx("autoclr"))) return;
  if (dev) try { const r = await dev.motionOp(track, 2); if (r[1]) return toast(tx(r[1] === 3 ? "songbusy" : "noreply")); } catch (e) { return toast(tx("noreply")); }
  auto = { on: false, list: [] }; drawAuto();   // (the FM-1 turns PLAY off with it)
});

/* ------------------------------------------------------------------------------------ the FM-1 --- */
async function seqRead() {   // the selected track's LEN and the rest (DUMP), its 64 steps, its automation
  if (!dev) return;
  await reloadValues();
  for (let i = 0; i < NSTEP; i++) steps[i] = await dev.stepGet(i);
  {   // the roll shows the track's notes (the lowest at the bottom, when they fit)
    const ns = steps.flatMap((s) => (s.time === TIME.NOTE ? s.notes.slice(0, s.n) : [])).filter((n) => n > 0);
    if (ns.length) rollLo = Math.max(12, Math.min(96, Math.min(...ns) - 1, Math.max(...ns) - ROWS + 2));
  }
  try { const m = await dev.motion(track); auto = { on: m.on, list: m.list }; autoSel = 0; } catch (e) {}
  drawSeq(); drawAuto();
  await sqSoundRead();
}

/* ------------------------------------------------- the SOUND box (above AUTOMATION): the selected track's sound --- */
// a P600 track: its place (1..255, as SOUND's list); another engine: its presets (Felucca's PRESET 8, names: NAMES 10)
let sqEng = 14, sqPre = 0;
document.head.insertAdjacentHTML("beforeend", "<style>#sqsound > .ttl { color: #fff; border-bottom: 0; font-size: 26px; }" +
  ".sqeng { text-align: center; font: 600 17px/1 'Barlow C'; color: var(--c); padding: 2px 0 8px; }" +
  ".sqsnd { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 0 8px; }" +
  ".sqsnd .field { height: 34px; line-height: 30px; width: 136px; padding: 0 6px; font-size: 18px; color: var(--cream); overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }</style>");
document.getElementById("sqs-").addEventListener("pointerdown", () => sqSoundStep(-1));
document.getElementById("sqs+").addEventListener("pointerdown", () => sqSoundStep(1));
function sqSoundShow() {
  const f = document.getElementById("sqsf"), e = document.getElementById("sqeng");
  e.textContent = (typeof engNames !== "undefined" && engNames[sqEng]) || "";
  f.textContent = sqEng === 14 ? placeLabel(place) : ((engPresets[sqEng] || [])[sqPre]) || "";
  f.title = f.textContent;
}
async function sqSoundRead() {
  if (!dev) return sqSoundShow();
  try {
    const tr = await dev.track(), s = tr.tracks[tr.sel] || {};
    sqEng = s.engine; sqPre = s.preset;
    if (sqEng !== 14) await enginePresets(sqEng);
  } catch (e) {}
  sqSoundShow();
}
async function sqSoundStep(d) {
  if (!dev) return toast(tx("offline"));
  if (sqEng === 14) { await choose((place + d + 255) % 255); return sqSoundShow(); }
  const n = (engPresets[sqEng] || []).length;
  if (!n) return;
  sqPre = (sqPre + d + n) % n; sqSoundShow();
  try { await dev.link.ask(false, 8, [sqEng, sqPre], (r) => r[0] === sqEng); await reloadValues(); } catch (e) { toast(tx("noreply")); }
}
function seqStepChanged(i, t) {   // a step edited on the FM-1
  if (!dev || t !== track || page !== "seq") return;
  dev.stepGet(i).then((s) => { steps[i] = s; drawRoll(); drawDetail(); }).catch(() => {});
}
// DETAIL's columns under the roll's steps, whatever the width of the roll's note names (the solfège widens it: Marc, 10/11)
function alignDetail() {
  const L = document.getElementById("detlabels"), k = L.offsetWidth ? L.getBoundingClientRect().width / L.offsetWidth : 1;
  const d = (rollGrid.getBoundingClientRect().left - detGrid.getBoundingClientRect().left) / k;
  if (k && Math.abs(d) > 0.5) L.style.width = (parseFloat(getComputedStyle(L).width) + d) + "px";
}
pageOpen.seq = () => { if (dev && auto.demo) auto = { on: false, list: [] }; drawSeq(); drawAuto(); sqSoundShow(); requestAnimationFrame(alignDetail); if (dev) seqRead().catch((e) => console.warn(e)); };
const seqLen = ctl.find((c) => c.id === P.SLEN);
const seqRender = render;
render = function (only) { seqRender(only); if (page === "seq" && (only == null || +only === P.SLEN)) drawSeq(); };   // (LEN: the steps out of it dim)

Object.assign(TX.en, { chord4: "A step holds 4 notes at most.", seqclear: "Clear the steps of this track?", euclid: "EUCLID: hits, steps, rotation (e.g. 5 16 0)",
  euclidbad: "EUCLID: hits from 0 to the steps, steps from 1 to 64.", notools: "The tools need the Guru-600 firmware of the FM-1.", toolnone: "Nothing to do.",
  autoclr: "Clear all the automation of this track?" });
Object.assign(TX.fr, { chord4: "Un pas tient 4 notes au plus.", seqclear: "Effacer les pas de cette piste ?", euclid: "EUCLID : coups, pas, décalage (par exemple 5 16 0)",
  euclidbad: "EUCLID : des coups de 0 au nombre de pas, des pas de 1 à 64.", notools: "Les outils demandent le firmware Guru-600 du FM-1.", toolnone: "Rien à faire.",
  autoclr: "Effacer toute l'automation de cette piste ?" });
