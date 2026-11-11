// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the BACKUP page: the whole FM-1 (the music, A..D, the USER sounds, the samples, the P600's places,
// the settings) in one file on this computer, and back. Felucca's archive (guru-backupio.js: BACKUP_LIST 65, GET 66,
// PUT 67; the samples by SMP 11..14), the file the Mac application and the installer save too.
"use strict";

const BK_NAMES = { 0: "CURRENT MUSIC", 1: "SETTINGS", 2: "PROJECT A", 3: "PROJECT B", 4: "PROJECT C", 5: "PROJECT D",
  6: "USER SOUNDS 1–16", 7: "USER SOUNDS 17–32", 8: "FM6 PATCH BANK (OLD)", 9: "USER SOUNDS' FM6 PATCHES", 10: "P600 PLACES",
  11: "FM6 VOICE BANK", 12: "SLICE SLICES", 32: "SAMPLE USR1", 33: "SAMPLE USR2", 34: "SAMPLE USR3" };
const BK_GROUPS = [["MUSIC", [0, 2, 3, 4, 5]], ["SOUNDS", [6, 7, 9, 10, 11, 8]], ["SAMPLES", [32, 33, 34, 12]], ["SETTINGS", [1]]];
const BK_DEMO = { 0: 3000, 1: 600, 2: 3200, 3: 3200, 4: 3200, 6: 3840, 10: 3600, 12: 96, 32: 42000, 34: 79000 };   // (offline)
let bkDev = BK.BACKUP_IDS.map((id) => ({ id, size: BK_DEMO[id] || 0 })),
  bkFile = null, bkBusy = false, bkFileName = "";

// the BACKUP page uses its space: the FM-1's list over the whole height, the drop zone filling FROM A FILE while no
// file is chosen (the hint under it)
document.head.insertAdjacentHTML("beforeend", "<style>.bksec .bklist { display: block; overflow-y: auto; }.bkgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px 16px; align-content: start; }.bkg { display: flex; flex-direction: column; gap: 6px; }.bkgt { display: flex; justify-content: space-between; align-items: baseline; font: 700 18px/1 'Barlow C'; color: var(--c); padding: 0 4px 5px; border-bottom: 1.5px solid color-mix(in srgb, var(--c) 45%, transparent); }.bkgt span { font-weight: 600; font-size: 15px; color: #b5b1a6; }.bksec .bkrow { height: 32px; font-size: 17px; }#bkfile.nofile .drop { flex: 1; flex-direction: column; font-size: 24px; gap: 8px; }#bkfile.nofile .drop span { font-size: 16px; } #bkfile.nofile .drop .btn { height: 48px; font-size: 20px; padding: 0 28px; }#bkfile.nofile .bklist { flex: none; display: block; } #bkfile.nofile .bklist .hint { text-align: center; font-size: 15px; }.bkhd { font-size: 17px; } .bksec .sbtn .btn { height: 46px; font-size: 19px; }</style>");
(function buildBackup() {
  const col = (id, t, x0, x1, inner) => { const e = h("div", "sec bksec"); e.id = id; e.dataset.page = "backup"; e.style.setProperty("--c", "var(--snd)");
    e.innerHTML = `<div class="ttl">${t}</div><div class="sbd">${inner}</div>`; abs(e, x0, 155, x1, 773); e.style.display = "none"; return e; };
  col("bkdev", "ON THE FM-1", 12, 764, `<div class="bkhd"></div><div class="bklist"></div><div class="bktot"></div>` +
    `<div class="sprog"><i></i></div><div class="sbtn"><div class="btn" id="bk-save">SAVE A BACKUP TO THIS COMPUTER</div></div>`);
  col("bkfile", "FROM A FILE", 772, 1524, `<div class="bkhd"></div>` +
    `<div class="drop">DROP A BACKUP FILE HERE<span>OR</span><div class="btn choose">CHOOSE A FILE</div><input type="file" hidden accept=".json,application/json"></div>` +
    `<div class="bklist"></div><div class="bktot"></div>` +
    `<div class="sprog"><i></i></div><div class="sbtn"><div class="btn red" id="bk-restore">RESTORE IT ON THE FM-1</div></div>`);
})();
const bkSecs = { dev: document.getElementById("bkdev"), file: document.getElementById("bkfile") };
const bkKiB = (n) => (n ? dec((n / 1024).toFixed(n < 10240 ? 1 : 0)) + " KiB" : "EMPTY");
function bkRows(list) {   // grouped by family: MUSIC, SOUNDS, SAMPLES, SETTINGS (two by two), each with its total
  const by = {}; list.forEach((o) => { by[o.id] = o; });
  const known = new Set(BK_GROUPS.flatMap((g) => g[1]));
  const row = (o) => `<div class="row bkrow${o.size ? "" : " empty"}"><b class="led${o.size ? " on" : ""}"></b>` +
    `<div class="nm">${BK_NAMES[o.id] || "OBJECT " + o.id}</div><div class="sz">${bkKiB(o.size)}</div></div>`;
  return `<div class="bkgrid">` + BK_GROUPS.map(([t, ids], gi) => {
    const os = ids.map((i) => by[i]).filter((o) => o && (o.id !== 8 || o.size));
    if (gi === BK_GROUPS.length - 1) os.push(...list.filter((o) => !known.has(o.id)));   // (an unknown object: last)
    if (!os.length) return "";
    const tot = os.reduce((a, o) => a + o.size, 0);
    return `<div class="bkg"><div class="bkgt">${t}<span>${tot ? bkKiB(tot) : ""}</span></div>${os.map(row).join("")}</div>`;
  }).join("") + `</div>`;
}
function drawBackup() {
  const caps = dev ? dev.info && dev.info.backupCaps || 0 : 3, d = bkSecs.dev, f = bkSecs.file;
  d.querySelector(".bkhd").textContent = !dev ? "CONNECT THE FM-1 TO SAVE IT" : caps & 1 ? "SAVED AS IT IS NOW, IN ONE FILE"
    : "THIS FIRMWARE CANNOT BE BACKED UP FROM HERE";
  d.querySelector(".bklist").innerHTML = bkRows(bkDev);
  d.querySelector(".bktot").textContent = "TOTAL " + bkKiB(bkDev.reduce((n, o) => n + o.size, 0));
  document.getElementById("bk-save").classList.toggle("dis", bkBusy || !dev || !(caps & 1));
  f.querySelector(".bkhd").innerHTML = bkFile ? `<b>${bkFileName.replace(/[<&]/g, "")}</b> · ${(bkFile.created || "").slice(0, 10)} · ${bkFile.source === "guru-600-app" ? "THE MAC APPLICATION" : String(bkFile.firmware || "").replace(/[<&]/g, "")}`
    : "A FILE SAVED HERE, BY THE MAC APPLICATION OR THE INSTALLER";
  f.querySelector(".drop").classList.toggle("dis", bkBusy);
  f.querySelector(".bklist").innerHTML = bkFile ? bkRows(bkFile.objects) : `<div class="hint">WHAT THE FILE HOLDS SHOWS HERE BEFORE IT IS RESTORED</div>`;
  f.classList.toggle("nofile", !bkFile);   // (no file yet: the drop zone takes the room its list will use)
  f.querySelector(".bktot").textContent = bkFile ? "TOTAL " + bkKiB(bkFile.objects.reduce((n, o) => n + o.size, 0)) : "";
  document.getElementById("bk-restore").classList.toggle("dis", bkBusy || !bkFile || !dev || !(caps & 2));
}

/* ------------------------------------------------------------------------------------ the FM-1 --- */
// Felucca's request(): [cmd, args] -> the reply's bytes; each command's reply named as its editor matches it
function bkRequest([cmd, args], opt = {}) {
  const match = cmd === 66 ? (a) => a[0] === args[0] && a.slice(2, 7).every((v, i) => v === args[i + 1])
    : cmd === 67 ? (a) => a[0] === args[0] && a[1] === args[1] : cmd >= 11 && cmd <= 14 ? (a) => a[0] === args[0] : () => true;
  const go = (n) => dev.link.ask(false, cmd, args, match, opt.timeout || 1200).catch((e) => (n > 0 ? go(n - 1) : Promise.reject(e)));
  return go(opt.retries || 0);
}
async function bkRead() { bkDev = BK.bkManifest(await bkRequest([65, []], { timeout: 3000 })); drawBackup(); }
const bkProg = (sec) => (done, total) => { sec.querySelector(".sprog i").style.width = Math.round(done / Math.max(1, total) * 100) + "%"; };
function bkSaveFile(obj) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(obj, null, 1)], { type: "application/json" }));
  a.download = `Guru-600-backup-${new Date().toISOString().slice(0, 10)}.json`;
  document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
async function bkWork(sec, job) {
  if (!dev) return toast(tx("offline"));
  if (document.getElementById("t-play").classList.contains("on")) return toast(tx("bkstop"));
  bkBusy = true; drawBackup();
  try { await job(); }
  catch (e) { toast(tx("bkfail", e.message)); }
  finally { bkBusy = false; sec.querySelector(".sprog i").style.width = "0"; try { await bkRead(); } catch (e) {} drawBackup(); }
}
document.getElementById("bk-save").addEventListener("click", () => bkWork(bkSecs.dev, async () => {
  const file = await BK.captureBackup(bkRequest, dev.info.version, bkProg(bkSecs.dev));
  bkSaveFile(file); toast(tx("bkdone"));
}));
document.getElementById("bk-restore").addEventListener("click", async () => {
  if (!bkFile || !await uiConfirm(tx("bkconfirm"))) return;
  bkWork(bkSecs.file, async () => {
    await BK.restoreBackup(bkRequest, bkFile, bkProg(bkSecs.file));
    dirty = false; await reloadAll(); toast(tx("bkrestored"));
  });
});
(() => {
  const f = bkSecs.file, drop = f.querySelector(".drop"), inp = drop.querySelector("input");
  const take = async (file) => {
    if (!file || bkBusy) return;
    try { bkFile = BK.readBackup(await file.text()); bkFileName = file.name; } catch (e) { bkFile = null; toast(tx("bkbad", e.message)); }
    drawBackup();
  };
  drop.querySelector(".choose").addEventListener("click", () => inp.click());
  inp.addEventListener("change", () => { take(inp.files[0]); inp.value = ""; });
  drop.addEventListener("dragover", (ev) => { ev.preventDefault(); drop.classList.add("over"); });
  drop.addEventListener("dragleave", () => drop.classList.remove("over"));
  drop.addEventListener("drop", (ev) => { ev.preventDefault(); drop.classList.remove("over"); take(ev.dataTransfer.files[0]); });
})();
pageOpen.backup = () => { drawBackup(); if (dev && dev.info && dev.info.backupCaps & 1) bkRead().catch((e) => console.warn(e)); };
Object.assign(TX.en, { bkstop: "Stop the music first.", bkfail: "Backup stopped: %s", bkdone: "Backup saved", bkbad: "Not a complete backup: %s",
  bkconfirm: "Restore this backup on the FM-1? Its music, projects, USER sounds, samples and settings are replaced. Keep it connected.",
  bkrestored: "Backup restored" });
Object.assign(TX.fr, { bkstop: "Arrêtez d'abord la musique.", bkfail: "Sauvegarde interrompue : %s", bkdone: "Sauvegarde enregistrée",
  bkbad: "Ce n'est pas une sauvegarde complète : %s",
  bkconfirm: "Restaurer cette sauvegarde sur le FM-1 ? Sa musique, ses projets, ses sons USER, ses échantillons et ses réglages sont remplacés. Gardez-le branché.",
  bkrestored: "Sauvegarde restaurée" });

// (Guru-600 1.0.2) depuis la fenêtre de mise à jour : la même sauvegarde que le bouton de la page, vrai si elle a réussi
window.majSauvegarder = async () => {
  let fait = false;
  showPage("backup");
  await bkWork(bkSecs.dev, async () => {
    const file = await BK.captureBackup(bkRequest, dev.info.version, bkProg(bkSecs.dev));
    bkSaveFile(file); toast(tx("bkdone")); fait = true;
  });
  return fait;
};
