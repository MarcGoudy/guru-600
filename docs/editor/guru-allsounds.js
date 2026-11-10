// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the SOUNDS list holds every sound one can have (Marc, 10/11): the 255 Guru-600 sounds (P600) first, then
// each other engine's factory sounds of the FM-1 (a heading per engine, the device's order), then the USER sounds. The
// family chips filter them all, with the FM-1's own categories (firmware category.c PRESET_CAT). An FM-1 sound's number on a
// light grey-blue ground, numbered on from 256 (no headings: Marc, 10/11); orange stays for what you made (a USER sound).
// A sound of another engine plays on the selected track, which takes that engine (Felucca's PRESET 8; a USER sound: UP_LOAD 20).
"use strict";

const ENG_CAT = { 0: "LPBPBKLBULLP", 2: "LKPLUU", 3: "LBLLL", 4: "KKLL", 5: "PLBF", 6: "BLLUP", 7: "KKKKK", 8: "PFPP", 9: "UUUPUDDPU",
  10: "DDDD", 11: "FFFF", 12: "KUBLPUKU", 13: "DD" };                     // (firmware category.c: a letter per preset)
const CAT_FAM = { B: 0, L: 1, P: 2, U: 3, K: 4, D: 5, F: 6 };          // (FAMILIES' order; O OTHER: under ALL only)
const UP_CAT_FAM = [-1, 0, 1, 2, 3, 4, 5, 6, -1];                       // (a USER sound's category byte: CAT_*)
const ENG_DEF = { 0: ["SAW LEAD", "SOFT PAD", "SQR BASS", "PWM STR", "ACID", "SINE KEY", "RAVE", "SUB BASS", "PLUCK", "BRASS", "WIND", "STRINGS"],
  2: ["BRASS", "ORGAN", "STRING", "RESO", "BELL", "WIRE"], 3: ["PULSE LD", "WAVE BASS", "ARP 8BIT", "WAVE LEAD", "STEP LEAD"],
  4: ["PIANO", "PIANO", "FLUTE", "SAX"], 5: ["CHOIR AAH", "VOX LEAD", "WOW BASS", "WHISPER"], 6: ["FAT BASS", "ARP LEAD", "SYNC LEAD", "RING BELL", "CHIP CHOIR"],
  7: ["ORGAN 1", "ORGAN 2", "ORGAN 3", "ORGAN 4", "ORGAN 5"], 8: ["CLOUD PAD", "GLITCH", "FROZEN", "SHIMMER"],
  9: ["BELL TREE", "MARIMBA", "PLUCK", "BOWED METAL", "KALIMBA", "HAND DRUM", "TOMS", "DRONE STRING", "HARP"],
  10: ["DRUM KIT", "DEEP KIT", "TIGHT KIT", "PERC KIT"], 11: ["WIND", "RAIN", "ARCADE", "METAL"],
  12: ["TINE EP", "BELL", "FM BASS", "BRASS", "PAD", "MARIMBA", "ORGAN", "PLUCK"], 13: ["CHOP", "STUTTER"] };
const X_ENGS = ENG_ORDER.filter((e) => e !== 14);
let xRows = [], xHeads = [], xPick = null;                               // ({e, k} or {u}: the one chosen here last)
document.head.insertAdjacentHTML("beforeend", "<style>" +
  "#list .xh { font: 700 15px/1 'Barlow C'; color: #9fb3c8; letter-spacing: .04em; padding: 12px 6px 5px; }" +
  "#list .xh.hide { display: none; }" +
  "#list .row.fm1 .n { background: color-mix(in srgb, #7f9bb8 30%, #111); border-color: #9fb3c8; }" +
  "#list .row.on.fm1 .n { background: #b9c9da; border-color: #000; }" +   // (lit: the black number on a light grey-blue)
  "#list .row.user .nm { color: var(--kept); }" +
  "#list .row.on.user { --sel: var(--kept); }</style>");

function xBuild() {                                                       // the FM-1's sounds and the USER sounds, after P600's
  const list = document.getElementById("list");
  for (const e of [...xRows, ...xHeads]) e.remove();
  xRows = []; xHeads = [];
  const head = (t) => { const e = h("div", "xh", t); list.appendChild(e); xHeads.push(e); return e; };
  for (const e of X_ENGS) {
    const nm = (engPresets[e] && engPresets[e].length ? engPresets[e] : ENG_DEF[e]) || [];
    if (!nm.length) continue;
    const hd = null;                                                     // (no heading: the number's ground tells them apart)
    nm.forEach((n, k) => {
      const r = h("div", "row fm1"); r.innerHTML = `<div class="n">${256 + xRows.length}</div><div class="nm">${n}</div>`;
      r.dataset.e = e; r.dataset.k = k; r.dataset.fam = CAT_FAM[(ENG_CAT[e] || "")[k]] ?? -1; r.head = hd;
      r.addEventListener("pointerdown", () => xChoose({ e, k }, n));
      list.appendChild(r); xRows.push(r);
    });
  }
  const users = (typeof userList !== "undefined" ? userList : []).map((u, i) => ({ ...u, i })).filter((u) => u.used);
  if (users.length) {
    const hd = null;
    for (const u of users) {
      const r = h("div", "row user"); r.innerHTML = `<div class="n">U${u.i + 1}</div><div class="nm">${u.name}</div>`;
      r.dataset.u = u.i; r.dataset.fam = UP_CAT_FAM[u.cat || 0] ?? (u.engine === 10 || u.engine === 13 ? 5 : -1); r.head = hd;
      r.addEventListener("pointerdown", () => xChoose({ u: u.i }, u.name));
      list.appendChild(r); xRows.push(r);
    }
  }
  xShow();
}
function xShow() {                                                        // the filter, and the one the track plays lit
  const seen = new Set();
  for (const r of xRows) {
    const hide = family >= 0 && +r.dataset.fam !== family;
    r.classList.toggle("hide", hide);
    if (!hide) seen.add(r.head);
    const on = xPick && (r.dataset.u != null ? xPick.u === +r.dataset.u : xPick.e === +r.dataset.e && xPick.k === +r.dataset.k);
    r.classList.toggle("on", !!on && curEng !== 14);
  }
  for (const hd of xHeads) hd.classList.toggle("hide", !seen.has(hd));
  for (const id of ["b-save", "b-orig", "b-export"]) {                 // (P600's own: a Guru-600 sound's place only)
    const b = document.getElementById(id); if (b && curEng !== 14) b.classList.add("dis");
  }
}
async function xChoose(pick, name) {
  if (!dev) return toast(tx("offline"));
  if (dirty && curEng === 14 && !await uiConfirm(tx("lose"))) return;
  try {
    if (pick.u != null) await dev.link.ask(false, 20, [pick.u], (r) => r[0] === pick.u, 1500);   // UP_LOAD
    else await dev.link.ask(false, 8, [pick.e, pick.k], (r) => r[0] === pick.e);                 // PRESET
    xPick = pick; dirty = false;
    await reloadValues(); showSounds();
    toast(tx("kitdone", name, track + 1));
  } catch (e) { toast(tx("noreply")); }
}
async function xRead() {                                                  // the names from the FM-1 (each engine's, the USER sounds)
  if (!dev) return;
  if (dev.info && dev.info.engines) engNames = dev.info.engines;
  for (const e of X_ENGS) { try { await enginePresets(e); } catch (er) {} }
  try { if (typeof userRead === "function") await userRead(); } catch (er) {}
  try { const tr = await dev.track(), s = tr.tracks[tr.sel] || {};       // what the selected track plays now
    if (s.engine !== 14) xPick = { e: s.engine, k: s.preset }; } catch (er) {}
  xBuild();
}
const xShowSounds0 = showSounds;
showSounds = function (scroll) { xShowSounds0(scroll); xShow(); };
const xPageOpen0 = pageOpen.sound;
pageOpen.sound = () => { if (xPageOpen0) xPageOpen0(); if (dev) xRead(); };
let xReadDone = false;                                                    // (the FM-1's names read once connected)
const xReloadAll0 = reloadAll;
reloadAll = async function () { await xReloadAll0(); if (!xReadDone && dev) { xReadDone = true; xRead(); } };
xBuild();
{ const at = +new URLSearchParams(location.search).get("listat");   // (?listat=n: the list scrolled to its row n, for the guide's shot)
  if (at) setTimeout(() => { const r = [...document.querySelectorAll("#list .row")][at - 1]; if (r) r.parentElement.scrollTop = r.offsetTop - r.parentElement.offsetTop; }, 1500); }
// the computer's ↑ ↓ on the SOUND page: the sound before / after in SOUNDS (the shown ones: the family chosen), loaded as a
// click does (Marc, 10/11)
addEventListener("keydown", (e) => {
  if ((e.code !== "ArrowUp" && e.code !== "ArrowDown") || page !== "sound" || e.repeat || e.metaKey || e.ctrlKey || e.altKey ||
      (e.target.closest && e.target.closest("input, textarea, [contenteditable]")) || document.querySelector("#dlg.on")) return;
  const rows = [...document.querySelectorAll("#list .row")].filter((r) => !r.classList.contains("hide") && r.offsetParent);
  if (!rows.length) return;
  e.preventDefault();
  const at = rows.findIndex((r) => r.classList.contains("on"));
  const to = rows[at < 0 ? 0 : Math.max(0, Math.min(rows.length - 1, at + (e.code === "ArrowDown" ? 1 : -1)))];
  if (!to || to === rows[at]) return;
  to.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true }));
  to.scrollIntoView({ block: "nearest" });
});
