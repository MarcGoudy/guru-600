// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the SONG page. Up to 16 sections, in each the PROJECT slot each track plays (A..D, or "–": silent) and
// the section's repeats (1..16); PLAY SONG / STOP. Felucca's SONG (33, ops 4..7: sections) and PROJECT (9, op 2: a slot
// used or not).
"use strict";

const SLOT = ["A", "B", "C", "D", "–"], SLOTC = ["var(--osc)", "var(--lfo)", "var(--env)", "var(--pm)", "#6b675e"];
let song = { list: [[0, 0, 0, 0, 4], [1, 1, 0, 4, 2], [0, 2, 1, 1, 4], [3, 3, 4, 2, 1], [0, 0, 0, 0, 2], [1, 1, 1, 1, 8]],
             running: true, row: 2, left: 2 };   // the mockup's while no FM-1 is there
let songSel = 4, slotsUsed = [true, true, true, false];

(function buildSong() {
  const sec = h("div", "sec"); sec.id = "songsec"; sec.dataset.page = "song"; sec.style.setProperty("--c", "var(--snd)");
  sec.innerHTML = `<div class="ttl">SECTIONS</div><div class="bd"><div id="songtab"></div></div>`;
  abs(sec, 12, 155, 1314, 773);
  const col = h("div", "sec"); col.id = "songcol"; col.dataset.page = "song"; col.style.setProperty("--c", "var(--snd)");
  col.innerHTML = `<div class="ttl">SONG</div>` +
    `<div class="songtp"><div class="btn big" id="sg-play">▶ PLAY SONG</div><div class="btn big" id="sg-stop">■ STOP</div></div>` +
    `<div class="songst"><div id="sg-sec">SECTION – / –</div><div id="sg-rep">REPEAT – / –</div></div>` +
    `<div class="songops">${["ADD", "INSERT", "DELETE", "MOVE UP", "MOVE DOWN", "CLEAR SONG"].map((t, i) => `<div class="btn" data-op="${i}">${t}</div>`).join("")}</div>` +
    `<div class="songslots"><div class="gt">SLOTS</div><div class="sl">${SLOT.slice(0, 4).map((t, i) => `<span><b class="led" style="--trk:${SLOTC[i]}"></b>${t}</span>`).join("")}</div>` +   // (a slot lit: a pattern saved there)
    `<div class="hint">SAVE THEM IN PROJECTS</div></div>`;
  abs(col, 1322, 155, 1524, 773);
  for (const e of stage.querySelectorAll('[data-page="song"]')) e.style.display = "none";
})();

const songTab = document.getElementById("songtab");
function drawSong() {
  songTab.innerHTML = `<div class="sr hd"><div>#</div><div>TRACK 1</div><div>TRACK 2</div><div>TRACK 3</div><div>TRACK 4</div><div>REPEAT</div></div>`;
  for (let r = 0; r < 16; r++) {
    const s = song.list[r], e = h("div", "sr" + (s ? "" : " empty") + (song.running && r === song.row ? " play" : "") + (r === songSel ? " sel" : ""));
    e.dataset.r = r;
    let html = `<div><span class="n">${r + 1}</span></div>`;
    for (let t = 0; t < 4; t++) html += s ? `<div><span class="slot" data-t="${t}" style="--sc:${SLOTC[s[t]]}">${SLOT[s[t]]}</span></div>` : `<div><span class="slot">·</span></div>`;
    html += s ? `<div><span class="rep">×${s[4]}</span><span class="rb" data-d="1">▲</span><span class="rb" data-d="-1">▼</span></div>` : `<div><span class="rep dim">·</span></div>`;
    e.innerHTML = html;
    songTab.appendChild(e);
  }
  document.getElementById("sg-play").classList.toggle("on", song.running);
  document.getElementById("sg-sec").textContent = song.running ? `SECTION ${song.row + 1} / ${song.list.length}` : `SECTIONS ${song.list.length}`;
  document.getElementById("sg-rep").textContent = song.running && song.list[song.row] ? `REPEAT ${song.list[song.row][4] - song.left + 1} / ${song.list[song.row][4]}` : "";
  document.querySelectorAll("#songcol .led").forEach((l, i) => l.classList.toggle("on", slotsUsed[i]));
}
// a click: a slot A B C D – in turn, the repeats with the arrows, the row selected
songTab.addEventListener("pointerdown", (e) => {
  const row = e.target.closest(".sr"); if (!row || row.classList.contains("hd")) return;
  const r = +row.dataset.r, s = song.list[r];
  songSel = r;
  if (s && e.target.dataset.t != null) { s[+e.target.dataset.t] = (s[+e.target.dataset.t] + 1) % 5; songWrite(); }
  else if (s && e.target.dataset.d) { s[4] = Math.max(1, Math.min(16, s[4] + +e.target.dataset.d)); songWrite(); }
  drawSong();
});
document.querySelectorAll("#songcol .songops .btn").forEach((b) => b.addEventListener("click", async () => {
  const op = +b.dataset.op, L = song.list, r = songSel;
  if (op === 0 && L.length < 16) { L.push(L.length ? [...L[L.length - 1]] : [0, 0, 0, 0, 1]); songSel = L.length - 1; }
  else if (op === 1 && L.length < 16) { L.splice(Math.min(r, L.length), 0, [0, 0, 0, 0, 1]); }
  else if (op === 2 && L[r]) { L.splice(r, 1); songSel = Math.min(r, L.length - 1); }
  else if (op === 3 && r > 0 && L[r]) { [L[r - 1], L[r]] = [L[r], L[r - 1]]; songSel = r - 1; }
  else if (op === 4 && L[r + 1]) { [L[r + 1], L[r]] = [L[r], L[r + 1]]; songSel = r + 1; }
  else if (op === 5) { if (!L.length || !await uiConfirm(tx("songclr"))) return; song.list = []; songSel = 0; }
  else return;
  songWrite(); drawSong();
}));
document.getElementById("sg-play").addEventListener("pointerdown", () => songOp(6));
document.getElementById("sg-stop").addEventListener("pointerdown", () => songOp(7));

/* ------------------------------------------------------------------------------------ the FM-1 --- */
function songReply(a) {   // op, rc, count, running, section, remaining, count x (4 slots, repeat)
  const n = a[2], list = [];
  for (let k = 0; k < n; k++) list.push(a.slice(6 + 5 * k, 11 + 5 * k));
  song = { list, running: !!a[3], row: a[4], left: a[5] };
  return a[1];
}
const SONG_RC = { 1: "songbad", 2: "songbusy", 3: "songslot", 4: "songslot", 5: "songslot", 6: "songslot" };
let songBusy = null;
async function songWrite() {   // the sections as they are now (one write at a time, the last wins)
  if (!dev) return;
  const args = [5, song.list.length, ...song.list.flat()];
  songBusy = (songBusy || Promise.resolve()).then(async () => {
    const rc = songReply(await dev.link.ask(false, 33, args, (r) => r[0] === 5));
    if (rc) toast(tx(SONG_RC[rc] || "songbad", SLOT[rc - 3] || ""));
    drawSong();
  }).catch(() => toast(tx("noreply")));
}
async function songOp(op) {
  if (!dev) return toast(tx("offline"));
  try { const rc = songReply(await dev.link.ask(false, 33, [op], (r) => r[0] === op)); if (rc) toast(tx(SONG_RC[rc] || "songbad", SLOT[rc - 3] || "")); drawSong(); }
  catch (e) { toast(tx("noreply")); }
}
async function songRead() {
  if (!dev) return;
  songReply(await dev.link.ask(false, 33, [4], (r) => r[0] === 4));
  for (let k = 0; k < 4; k++) slotsUsed[k] = !!(await dev.link.ask(false, 9, [2, k], (r) => r[1] === k))[2];
  drawSong();
}
let songPoll = 0;
pageOpen.song = () => {
  drawSong();
  clearInterval(songPoll);
  if (dev) { songRead().catch((e) => console.warn(e)); songPoll = setInterval(() => {   // (the poll: quiet; a FM-1 that stops answering is the WATCH's to tell)
    if (page !== "song" || !dev) return clearInterval(songPoll);
    dev.link.ask(false, 33, [4], (r) => r[0] === 4).then((a) => { songReply(a); drawSong(); }).catch(() => {});
  }, 500); }
};

Object.assign(TX.en, { songclr: "Clear the whole song?", songbad: "The FM-1 refused these sections.", songbusy: "The FM-1 is busy: try again.",
  songslot: "Slot %s is empty: save a pattern in it (PROJECTS) first." });
Object.assign(TX.fr, { songclr: "Effacer tout le morceau ?", songbad: "Le FM-1 a refusé ces sections.", songbusy: "Le FM-1 est occupé : réessayez.",
  songslot: "L'emplacement %s est vide : enregistrez-y d'abord un motif (PROJECTS)." });
