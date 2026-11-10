// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the SAMPLES page: the three user sample slots (USR1..USR3: the SAMPLE, GRAIN and SLICE engines play them).
// Files dropped or chosen (WAV, or anything the browser decodes), one zone per file on its root note, sent as Felucca's
// editor sends them (guru-sampleio.js: SMP_BEGIN 11, SMP_WRITE 12, SMP_END 13; SMP_ERASE 14; SMP_INFO 15).
"use strict";

let smpInfo = { slotKiB: 80, slots: [{ zones: 3, name: "VOX", kib: 41 }, { zones: 0, name: "", kib: 0 }, { zones: 1, name: "BREAK", kib: 52 }] };
const smpDraft = [0, 1, 2].map(() => ({ name: "", files: [] }));
// (the Guru-600 keeps its saved P600 places at the end of USR3: its sample data stops at 17 sectors, as the firmware's
// eng_sample.c SMP_SLOT_END; the FM-1 refuses more)
const smpMax = (k) => (k === 2 ? 17 * 4096 - SIO.SMP.DATA_OFF : SIO.SMP.MAX_DATA);
let smpBusy = false;

// the SAMPLES page uses its space: with no file yet the drop zone fills the slot (larger text and button), the hint
// under it; the buttons at the bottom level (ERASE had the SOUND page's margin)
document.head.insertAdjacentHTML("beforeend", "<style>.smpsec .sbtn { align-items: center; } .smpsec .sbtn .btn { height: 46px; font-size: 19px; } .smpsec .btn.red.er { margin-top: 0; }.smpsec.nofiles .drop { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 24px; gap: 6px; }.smpsec.nofiles .drop span { font-size: 16px; } .smpsec.nofiles .drop .btn { height: 48px; font-size: 20px; padding: 0 28px; margin-top: 8px; }.smpsec.nofiles .flist { flex: none; } .smpsec.nofiles .flist .hint { margin: 0; padding: 4px 10px 0; font-size: 15px; }</style>");
(function buildSamples() {
  for (let k = 0; k < 3; k++) {
    const e = h("div", "sec smpsec"); e.dataset.page = "samples"; e.dataset.k = k; e.style.setProperty("--c", "var(--env)"); e.style.setProperty("--onc", "var(--env)");
    e.innerHTML = `<div class="ttl">USR${k + 1}</div><div class="sbd">` +
      `<div class="sst"><div class="snm"></div><div class="sbar"><i></i></div><div class="skb"></div></div>` +
      `<div class="sname"><span>NAME</span><input maxlength="8" spellcheck="false" placeholder="NAME"></div>` +
      `<div class="drop">DROP WAV FILES HERE<br><span>OR</span><div class="btn choose">CHOOSE FILES</div><input type="file" multiple hidden accept=".wav,audio/*"></div>` +
      `<div class="flist"></div><div class="ssize"></div>` +
      `<div class="sprog"><i></i></div>` +
      `<div class="sbtn"><div class="btn up">SEND TO USR${k + 1}</div><div class="btn red er">ERASE</div></div></div>`;
    abs(e, 12 + k * 506, 155, 12 + k * 506 + 498, 773);
    e.style.display = "none";
  }
})();
const smpSecs = [...stage.querySelectorAll(".smpsec")];
function drawSamples() {
  smpSecs.forEach((e, k) => {
    const u = smpInfo.slots[k] || { zones: 0, name: "", kib: 0 }, d = smpDraft[k];
    e.querySelector(".snm").textContent = u.zones ? `${u.name || "—"} · ${u.zones} ZONE${u.zones > 1 ? "S" : ""}` : "EMPTY";
    const cap = Math.min(smpInfo.slotKiB * 1024, smpMax(k));
    e.querySelector(".sbar i").style.width = Math.min(100, u.kib * 1024 / cap * 100) + "%";
    e.querySelector(".skb").textContent = `${u.kib} / ${dec(SIO.kib(cap))} KiB`;
    const inp = e.querySelector(".sname input"); if (document.activeElement !== inp) inp.value = d.name;
    const keys = SIO.splitKeys(d.files), roots = d.files.map((f) => f.root), dup = roots.some((r, i) => roots.indexOf(r) !== i);
    e.querySelector(".flist").innerHTML = d.files.map((f, i) => `<div class="frow" data-i="${i}"><div class="fn">${f.fname}</div>` +
      `<input class="froot${roots.indexOf(f.root) !== i || roots.lastIndexOf(f.root) !== i ? " bad" : ""}" value="${SIO.noteName(f.root)}" spellcheck="false"><div class="fk">${SIO.noteName(keys[i][0])}–${SIO.noteName(keys[i][1])}</div>` +
      `<div class="fl">${(f.s.length / SIO.SMP.RATE).toFixed(2)} s</div><div class="btn fp">▶</div><div class="btn fx">✕</div></div>`).join("") ||
      `<div class="hint">ONE ZONE PER FILE, PLAYED FROM ITS ROOT NOTE · ${SIO.SMP.MAX_ZONES} FILES AT MOST</div>`;
    const bytes = SIO.draftBytes(d), big = bytes > smpMax(k);
    e.querySelector(".ssize").textContent = d.files.length ? `${dec(SIO.kib(bytes))} / ${dec(SIO.kib(smpMax(k)))} KiB${big ? " · TOO LONG FOR THE SLOT" : ""}${dup ? " · TWO FILES ON ONE ROOT NOTE" : ""}` : "";
    e.querySelector(".ssize").classList.toggle("bad", big || dup);
    e.querySelector(".up").classList.toggle("dis", smpBusy || !d.files.length || big || dup || !d.name);
    e.querySelector(".er").classList.toggle("dis", smpBusy || !u.zones);
    e.querySelector(".drop").classList.toggle("dis", smpBusy);
    e.classList.toggle("nofiles", !d.files.length);   // (no file yet: the drop zone takes the room the list will use)
  });
}
async function addFiles(k, list) {
  const d = smpDraft[k];
  for (const f of list) {
    try {
      const z = await SIO.decodeFile(f);
      if (d.files.length >= SIO.SMP.MAX_ZONES) { toast(tx("smpmax", SIO.SMP.MAX_ZONES)); break; }
      d.files.push(z);
      if (!d.name) d.name = f.name.replace(/\.[^.]*$/, "").replace(/[ _-]*[A-Ga-g][#b]?-?\d$/, "").toUpperCase().replace(/[^\x20-\x7E]/g, "").slice(0, 8);
    } catch (e) { toast(tx("smpdec", f.name)); }
  }
  drawSamples();
}
let pvCtx = null, pvSrc = null;
function preview(f) {   // the file as it will be stored (22050 Hz)
  try {
    if (pvSrc) pvSrc.stop();
    pvCtx = pvCtx || new AudioContext(); pvCtx.resume().catch(() => {});
    const buf = pvCtx.createBuffer(1, f.s.length, SIO.SMP.RATE), ch = buf.getChannelData(0);
    for (let i = 0; i < f.s.length; i++) ch[i] = f.s[i] / 32768;
    pvSrc = pvCtx.createBufferSource(); pvSrc.buffer = buf; pvSrc.connect(pvCtx.destination); pvSrc.start();
  } catch (e) {}
}
smpSecs.forEach((e, k) => {
  const d = smpDraft[k], fileIn = e.querySelector(".drop input"), drop = e.querySelector(".drop");
  e.querySelector(".choose").addEventListener("click", () => { if (!smpBusy) fileIn.click(); });
  fileIn.addEventListener("change", () => { addFiles(k, [...fileIn.files]); fileIn.value = ""; });
  drop.addEventListener("dragover", (ev) => { ev.preventDefault(); drop.classList.add("over"); });
  drop.addEventListener("dragleave", () => drop.classList.remove("over"));
  drop.addEventListener("drop", (ev) => { ev.preventDefault(); drop.classList.remove("over"); if (!smpBusy) addFiles(k, [...ev.dataTransfer.files]); });
  e.querySelector(".sname input").addEventListener("input", (ev) => {
    const v = ev.target.value.toUpperCase().replace(/[^\x20-\x7E]/g, "").slice(0, 8); if (v !== ev.target.value) ev.target.value = v; d.name = v; drawSamples();
  });
  e.querySelector(".flist").addEventListener("click", (ev) => {
    const r = ev.target.closest(".frow"); if (!r) return; const i = +r.dataset.i;
    if (ev.target.classList.contains("fp")) preview(d.files[i]);
    if (ev.target.classList.contains("fx") && !smpBusy) { d.files.splice(i, 1); drawSamples(); }
  });
  e.querySelector(".flist").addEventListener("change", (ev) => {
    if (!ev.target.classList.contains("froot")) return;
    const i = +ev.target.closest(".frow").dataset.i, n = SIO.parseNote(ev.target.value.trim().replace(/^[a-g]/, (c) => c.toUpperCase()).replace(/^([A-G])B/, "$1b").replace("♯", "#").replace("♭", "b"));
    if (n == null) { ev.target.classList.add("bad"); return; }
    d.files[i].root = n; drawSamples();
  });
  e.querySelector(".up").addEventListener("click", () => smpUpload(k));
  e.querySelector(".er").addEventListener("click", () => smpErase(k));
});

/* ------------------------------------------------------------------------------------ the FM-1 --- */
async function smpRead() {   // SMP_INFO: slots, slot KiB, per slot zones, name, KiB
  const a = await dev.link.ask(false, 15, [], () => true, 1500);
  let i = 2; const slots = [];
  for (let k = 0; k < a[0]; k++) { const zones = a[i++]; let name = ""; while (i < a.length && a[i]) name += String.fromCharCode(a[i++]); i++; slots.push({ zones, name, kib: a[i++] }); }
  smpInfo = { slotKiB: a[1], slots };
  drawSamples();
}
async function smpUpload(k) {
  const d = smpDraft[k];
  if (!dev) return toast(tx("offline"));
  let built;
  try { built = SIO.buildSlot(d.name, d.files.map((f) => ({ s: f.s, root: f.root }))); } catch (e) { return toast(tx("smpfail", e.message)); }
  if (!await uiConfirm(tx("smpup", k + 1))) return;
  const { hdr, data } = built, prog = smpSecs[k].querySelector(".sprog i");
  smpBusy = true; drawSamples();
  try {
    let a = await dev.link.ask(false, 11, [k], (r) => r[0] === k, 1500);
    if (a[1]) throw new Error("begin rc " + a[1]);
    for (let off = 0; off < data.length; off += 256) {
      const o = SIO.SMP.DATA_OFF + off;
      a = await dev.link.ask(false, 12, [k, o & 127, (o >> 7) & 127, (o >> 14) & 127, ...SIO.pack7(data.subarray(off, off + 256))], (r) => r[0] === k, 1500);
      if (a[4]) throw new Error(`write rc ${a[4]}`);
      prog.style.width = Math.min(100, (off + 256) / data.length * 100) + "%";
    }
    a = await dev.link.ask(false, 13, [k, ...SIO.pack7(hdr)], (r) => r[0] === k, 2500);
    if (a[1]) throw new Error(`end rc ${a[1]} (${SIO.SMP_RC[a[1]] || "?"})`);
    toast(tx("smpdone", k + 1)); d.files = []; d.name = "";
  } catch (e) { toast(tx("smpfail", e.message)); }
  finally { prog.style.width = "0"; smpBusy = false; try { await smpRead(); } catch (e) {} drawSamples(); }
}
async function smpErase(k) {
  if (!dev) return toast(tx("offline"));
  if (!await uiConfirm(tx("smperase", k + 1))) return;
  smpBusy = true; drawSamples();
  try { const a = await dev.link.ask(false, 14, [k], (r) => r[0] === k, 3000); if (a[1]) throw new Error("erase rc " + a[1]); toast(tx("smperased", k + 1)); }
  catch (e) { toast(tx("smpfail", e.message)); }
  finally { smpBusy = false; try { await smpRead(); } catch (e) {} drawSamples(); }
}
pageOpen.samples = () => { drawSamples(); if (dev) smpRead().catch((e) => console.warn(e)); };
Object.assign(TX.en, { smpmax: "%s files at most: the others were left out.", smpdec: "This file could not be read: %s", smpfail: "Sample not sent: %s",
  smpup: "Send these files to USR%s? What it holds now is replaced.", smpdone: "Sent to USR%s", smperase: "Erase USR%s?", smperased: "USR%s erased" });
Object.assign(TX.fr, { smpmax: "%s fichiers au plus : les autres ont été laissés de côté.", smpdec: "Ce fichier n'a pas pu être lu : %s", smpfail: "Échantillon non envoyé : %s",
  smpup: "Envoyer ces fichiers dans USR%s ? Ce qu'il contient est remplacé.", smpdone: "Envoyé dans USR%s", smperase: "Effacer USR%s ?", smperased: "USR%s effacé" });
