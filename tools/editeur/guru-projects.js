// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the PROJECTS page: the four projects A..D (the four tracks, their steps, the song, the automation:
// Felucca's PROJECT, 9) and the 32 USER sounds (a sound and its 16-step pattern: UP_LIST 16, UP_STORE 19, UP_LOAD 20,
// UP_ERASE 21), these on the selected track.
"use strict";

let projUsed = [true, true, true, false], userList = Array.from({ length: 32 }, (_, i) => (i < 5 ? { used: true, engine: [14, 14, 0, 12, 10][i],
  name: ["MY BASS", "WARM PAD", "SAW LEAD", "E.PIANO", "BEAT 1"][i] } : { used: false, engine: 0, name: "" })), userSel = 0;

// the PROJECTS page uses its space: larger letters and buttons on the cards, the hint readable and centred, the
// buttons under USER SOUNDS level (ERASE had the SOUND page's margin)
document.head.insertAdjacentHTML("beforeend", "<style>#usersec #u-erase { margin-top: 0; }.ub { align-items: center; } .ub .btn { height: 46px; font-size: 19px; }.pj { gap: 22px; padding: 0 20px; } .pj .pl { font-size: 66px; width: 58px; } .pj .ps { font-size: 23px; }.pj .pb { gap: 10px; } .pj .btn { width: 104px; height: 48px; font-size: 20px; }.phint { font-size: 14px; text-align: center; padding: 6px 14px 12px; }.urow .nm { font-size: 17px; }</style>");
(function buildProjects() {
  const pr = h("div", "sec"); pr.id = "projsec"; pr.dataset.page = "projects"; pr.style.setProperty("--c", "var(--snd)");
  pr.innerHTML = `<div class="ttl">PROJECTS</div><div class="bd projbd">${["A", "B", "C", "D"].map((l, k) =>
    `<div class="pj" data-k="${k}" style="--sc:${SLOTC[k]}"><div class="pl">${l}</div><div class="ps"></div>` +
    `<div class="pb"><div class="btn psave">SAVE</div><div class="btn pload">LOAD</div></div></div>`).join("")}</div>` +
    `<div class="phint">A PROJECT HOLDS THE FOUR TRACKS: THEIR SOUNDS, STEPS AND AUTOMATION, THE MIX AND THE SONG.<br>THE SONG PLAYS ITS SECTIONS FROM THESE SLOTS.</div>`;
  abs(pr, 12, 155, 560, 773);
  const us = h("div", "sec"); us.id = "usersec"; us.dataset.page = "projects"; us.style.setProperty("--c", "var(--snd)");
  us.innerHTML = `<div class="ttl">USER SOUNDS</div><div class="bd userbd"><div id="userlist"></div>` +
    `<div class="ub"><div class="btn" id="u-store">STORE THE TRACK'S SOUND</div><div class="btn" id="u-load">LOAD</div><div class="btn red" id="u-erase">ERASE</div></div></div>`;
  abs(us, 568, 155, 1524, 773);
  for (const e of [pr, us]) e.style.display = "none";
})();
const userListEl = document.getElementById("userlist");
function drawProjects() {
  document.querySelectorAll("#projsec .pj").forEach((e, k) => {
    e.classList.toggle("used", projUsed[k]);
    e.querySelector(".ps").textContent = projUsed[k] ? "SAVED" : "EMPTY";
    e.querySelector(".pload").classList.toggle("dis", !projUsed[k]);
  });
  userListEl.innerHTML = userList.map((u, i) => `<div class="row urow${i === userSel ? " on" : ""}${u.used ? "" : " empty"}" data-i="${i}">` +
    `<div class="n">${i + 1}</div><div class="ue">${u.used ? engNames[u.engine] || "" : ""}</div><div class="nm">${u.used ? u.name : "—"}</div></div>`).join("");
  document.getElementById("u-load").classList.toggle("dis", !userList[userSel].used);
  document.getElementById("u-erase").classList.toggle("dis", !userList[userSel].used);
}
userListEl.addEventListener("pointerdown", (e) => { const r = e.target.closest(".urow"); if (!r) return; userSel = +r.dataset.i; drawProjects(); });
userListEl.addEventListener("dblclick", (e) => { const r = e.target.closest(".urow"); if (r && userList[+r.dataset.i].used) userLoad(); });
document.querySelectorAll("#projsec .pj").forEach((e, k) => {
  e.querySelector(".psave").addEventListener("click", async () => {
    if (!dev) return toast(tx("offline"));
    if (projUsed[k] && !await uiConfirm(tx("projover", "ABCD"[k]))) return;
    try { const a = await dev.link.ask(false, 9, [1, k], (r) => r[0] === 1 && r[1] === k, 4000); projUsed[k] = !!a[2]; drawProjects(); toast(tx("projsaved", "ABCD"[k])); }
    catch (er) { toast(tx("projfail")); }
  });
  e.querySelector(".pload").addEventListener("click", async () => {
    if (!dev) return toast(tx("offline"));
    if (!projUsed[k] || !await uiConfirm(tx("projload", "ABCD"[k]))) return;
    try { await dev.link.ask(false, 9, [0, k], (r) => r[0] === 0 && r[1] === k, 3000); dirty = false; await reloadAll(); toast(tx("projloaded", "ABCD"[k])); }
    catch (er) { toast(tx("noreply")); }
  });
});
document.getElementById("u-store").addEventListener("click", async () => {
  if (!dev) return toast(tx("offline"));
  const u = userList[userSel];
  if (u.used && !await uiConfirm(tx("userover", userSel + 1, u.name))) return;
  const nm = await uiPrompt(tx("username"), u.used ? u.name : "");
  if (nm == null) return;
  const name = String(nm).replace(/[^\x20-\x7E]/g, "").trim().toUpperCase().slice(0, 12);
  try { const a = await dev.link.ask(false, 19, [userSel, ...[...name].map((c) => c.charCodeAt(0) & 127), 0], (r) => r[0] === userSel, 3000);
    if (a[1]) return toast(tx("projfail")); await userRead(); toast(tx("userstored", userSel + 1)); }
  catch (er) { toast(tx("noreply")); }
});
async function userLoad() {
  if (!dev) return toast(tx("offline"));
  if (!userList[userSel].used) return;
  if (dirty && !await uiConfirm(tx("lose"))) return;
  try { await dev.link.ask(false, 20, [userSel], (r) => r[0] === userSel); dirty = false; await reloadValues(); toast(userList[userSel].name); }
  catch (er) { toast(tx("noreply")); }
}
document.getElementById("u-load").addEventListener("click", userLoad);
document.getElementById("u-erase").addEventListener("click", async () => {
  if (!dev) return toast(tx("offline"));
  const u = userList[userSel]; if (!u.used || !await uiConfirm(tx("usererase", userSel + 1, u.name))) return;
  try { await dev.link.ask(false, 21, [userSel], (r) => r[0] === userSel, 3000); await userRead(); } catch (er) { toast(tx("noreply")); }
});

/* ------------------------------------------------------------------------------------ the FM-1 --- */
async function userRead() {   // UP_LIST: start, count, total, per slot used, engine, name; (1.2) then the categories
  for (let s = 0; s < 32; s += 16) {
    const a = await dev.link.ask(false, 16, [s, 16], (r) => r[0] === s, 1500);
    let i = 3;
    for (let k = 0; k < a[1]; k++) {
      const used = !!a[i], engine = a[i + 1]; i += 2;
      let name = ""; while (i < a.length && a[i]) name += String.fromCharCode(a[i++]); i++;
      userList[s + k] = { used, engine, name };
    }
  }
  drawProjects();
}
async function projRead() {
  if (!dev) return;
  if (dev.info && dev.info.engines) engNames = dev.info.engines;
  for (let k = 0; k < 4; k++) projUsed[k] = !!(await dev.link.ask(false, 9, [2, k], (r) => r[0] === 2 && r[1] === k))[2];
  await userRead();
}
pageOpen.projects = () => { drawProjects(); if (dev) projRead().catch((e) => console.warn(e)); };
Object.assign(TX.en, { projover: "Project %s holds a saved project: replace it with the music as it is now?", projsaved: "Saved as project %s",
  projfail: "The FM-1 could not save (stop the music first).", projload: "Load project %s? The music as it is now is replaced.", projloaded: "Project %s loaded",
  userover: "USER %s holds %s: replace it?", username: "The sound's name (12 letters at most):", userstored: "Stored as USER %s", usererase: "Erase USER %s (%s)?" });
Object.assign(TX.fr, { projover: "Le projet %s contient déjà un projet : le remplacer par la musique telle qu'elle est ?", projsaved: "Enregistré comme projet %s",
  projfail: "Le FM-1 n'a pas pu enregistrer (arrêtez d'abord la musique).", projload: "Charger le projet %s ? La musique en cours est remplacée.", projloaded: "Projet %s chargé",
  userover: "USER %s contient %s : le remplacer ?", username: "Le nom du son (12 lettres au plus) :", userstored: "Enregistré comme USER %s", usererase: "Effacer USER %s (%s) ?" });
