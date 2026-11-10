// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: its own questions (a confirmation, a text to type) in the panel's style, instead of the browser's
// windows ("localhost indique..."). uiConfirm(text) -> true / false; uiPrompt(text, value) -> the text typed, or null.
// Enter: OK; Escape or a click outside: cancel. The buttons' words in the editor's language (lang, guru-i18n.js's list).
"use strict";

const DLG_W = { en: ["OK", "CANCEL"], fr: ["OK", "ANNULER"], de: ["OK", "ABBRECHEN"], es: ["ACEPTAR", "CANCELAR"],
  it: ["OK", "ANNULLA"], zh: ["确定", "取消"], ja: ["OK", "キャンセル"] };
document.head.insertAdjacentHTML("beforeend", "<style>" +
  "#dlg { position: fixed; inset: 0; z-index: 2000; display: none; align-items: center; justify-content: center; background: rgba(0,0,0,.62); }" +
  "#dlg.on { display: flex; }" +
  "#dlg .box { width: min(520px, 86vw); background: #0b0b0b; border: 2px solid var(--cream, #EDEBE6); border-radius: 10px; padding: 22px 24px 20px;" +
  " box-shadow: 0 10px 40px rgba(0,0,0,.8); color: #EDEBE6; font: 600 19px/1.35 'Barlow C', sans-serif; }" +
  "#dlg .msg { white-space: pre-line; margin-bottom: 18px; }" +
  "#dlg input { width: 100%; box-sizing: border-box; height: 42px; margin-bottom: 18px; padding: 0 12px; background: #000; color: #fff;" +
  " border: 2px solid #8f8b80; border-radius: 6px; font: 600 20px 'Barlow C', sans-serif; outline: none; }" +
  "#dlg input:focus { border-color: var(--cream, #EDEBE6); }" +
  "#dlg .bts { display: flex; justify-content: flex-end; gap: 12px; }" +
  "#dlg .btn { min-width: 120px; height: 44px; font-size: 19px; }" +
  "#dlg .ok { border-color: var(--cream, #EDEBE6); }</style>");
const dlgEl = document.createElement("div"); dlgEl.id = "dlg";
dlgEl.innerHTML = `<div class="box"><div class="msg"></div><input spellcheck="false"><div class="bts"><div class="btn no"></div><div class="btn ok"></div></div></div>`;
document.body.appendChild(dlgEl);
function uiAsk(text, value) {                             // value null: a confirmation; a string: a text to type
  const L = DLG_W[typeof lang !== "undefined" && DLG_W[lang] ? lang : "en"];
  const inp = dlgEl.querySelector("input"), ok = dlgEl.querySelector(".ok"), no = dlgEl.querySelector(".no");
  dlgEl.querySelector(".msg").textContent = text;
  ok.textContent = L[0]; no.textContent = L[1];
  inp.style.display = value == null ? "none" : ""; inp.value = value == null ? "" : value;
  dlgEl.classList.add("on");
  if (value != null) setTimeout(() => { inp.focus(); inp.select(); }, 0);
  return new Promise((done) => {
    const end = (r) => { dlgEl.classList.remove("on"); removeEventListener("keydown", key, true); ok.onclick = no.onclick = dlgEl.onpointerdown = null; done(r); };
    const yes = () => end(value == null ? true : inp.value);
    const nay = () => end(value == null ? false : null);
    const key = (e) => { if (e.key === "Enter") { e.preventDefault(); e.stopPropagation(); yes(); } else if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); nay(); }
      else if (value == null) e.stopPropagation(); };          // (the computer keys do not play while it is open)
    addEventListener("keydown", key, true);
    ok.onclick = yes; no.onclick = nay;
    dlgEl.onpointerdown = (e) => { if (e.target === dlgEl) nay(); };
  });
}
const uiConfirm = (text) => uiAsk(text, null);
const uiPrompt = (text, value) => uiAsk(text, value == null ? "" : String(value));
