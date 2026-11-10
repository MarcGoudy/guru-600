// SPDX-License-Identifier: GPL-3.0-only
// Copyright (C) 2026 Leo Kuroshita (@kurogedelic), Hügelton Instruments
// The user samples, as Felucca's editor builds them (Felucca/web/editor.html, checked byte for byte against tools/sampleio.py by
// web/test_web.mjs): copied unchanged, inside a scope of their own (SIO.*) for the Guru-600 editor.
const SIO = (() => {
"use strict";
const NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const noteName = (n) => NOTE_NAMES[n % 12] + (Math.floor(n / 12) - 1);   /* 60 = C4 */
/* a note token: a number or a note name (C4, F#3, Bb2) */
function parseNote(tok) {
  if (/^\d+$/.test(tok)) { const n = +tok; return n <= 127 ? n : null; }
  const m = /^([A-Ga-g])([#b]?)(-?\d)$/.exec(tok);
  if (!m) return null;
  const base = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 }[m[1].toUpperCase()];
  const n = base + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + (parseInt(m[3], 10) + 1) * 12;
  return n >= 0 && n <= 127 ? n : null;
}
/* "C4 E4 G4" -> [60, 64, 67]; null on a bad token or more than 4 notes */
function parseNotes(s) {
  const t = s.trim().split(/[\s,]+/).filter(Boolean);
  if (t.length > 4) return null;
  const out = t.map(parseNote);
  return out.includes(null) ? null : out;
}

const SMP = { SLOT_SIZE: 0x14000, DATA_OFF: 512, RATE: 22050, HDR_LEN: 32 + 16 * 28, MAX_ZONES: 16 };
SMP.MAX_DATA = SMP.SLOT_SIZE - SMP.DATA_OFF;

/* groups of up to 7 bytes, each preceded by their top bits */
function pack7(b) {
  const out = [];
  for (let i = 0; i < b.length; i += 7) {
    const g = Array.from(b.slice(i, i + 7));
    out.push(g.reduce((m, x, j) => m | (((x >> 7) & 1) << j), 0));
    for (const x of g) out.push(x & 0x7F);
  }
  return out;
}
function unpack7(a) {
  const out = [];
  for (let i = 0; i < a.length; i += 8) {
    const top = a[i];
    for (let j = 0; j < 7 && i + 1 + j < a.length; j++) out.push(a[i + 1 + j] | (((top >> j) & 1) << 7));
  }
  return Uint8Array.from(out);
}

const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
  return t;
})();
function crc32(b) { let c = 0xFFFFFFFF; for (let i = 0; i < b.length; i++) c = CRC_TABLE[(c ^ b[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }

const IMA_STEP = [7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88,
  97, 107, 118, 130, 143, 157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658,
  724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660,
  4026, 4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899, 15289, 16818,
  18500, 20350, 22385, 24623, 27086, 29794, 32767];
const IMA_IDX = [-1, -1, -1, -1, 2, 4, 6, 8];
/* IMA ADPCM, 4 bit, low nibble first, from predictor 0 / index 0 -> {data, pred, idx} (state at loopStart) */
function imaEncode(s, loopStart = 0) {
  let pred = 0, idx = 0, atLoop = [0, 0];
  const nib = new Uint8Array(s.length + (s.length & 1));
  for (let n = 0; n < s.length; n++) {
    if (n === loopStart) atLoop = [pred, idx];
    const step = IMA_STEP[idx];
    let diff = s[n] - pred, code = 0;
    if (diff < 0) { code = 8; diff = -diff; }
    let vd = step >> 3;
    if (diff >= step) { code |= 4; diff -= step; vd += step; }
    if (diff >= step >> 1) { code |= 2; diff -= step >> 1; vd += step >> 1; }
    if (diff >= step >> 2) { code |= 1; vd += step >> 2; }
    pred = Math.max(-32768, Math.min(32767, code & 8 ? pred - vd : pred + vd));
    idx = Math.max(0, Math.min(88, idx + IMA_IDX[code & 7]));
    nib[n] = code;
  }
  const out = new Uint8Array(nib.length >> 1);
  for (let k = 0; k < nib.length; k += 2) out[k >> 1] = nib[k] | (nib[k + 1] << 4);
  return { data: out, pred: atLoop[0], idx: atLoop[1] };
}

/* WAV: PCM 8/16/24/32 or float, any channel count, mixed to mono -> {sr, x} (gen_samples.read_any_wav) */
function parseWav(buf) {
  const d = new Uint8Array(buf), v = new DataView(d.buffer, d.byteOffset, d.byteLength);
  const id = (i) => String.fromCharCode(d[i], d[i + 1], d[i + 2], d[i + 3]);
  if (d.length < 12 || id(0) !== "RIFF" || id(8) !== "WAVE") throw new Error("not a WAV file");
  let i = 12, fmt = null, data = null;
  while (i + 8 <= d.length) {
    const cid = id(i), n = v.getUint32(i + 4, true);
    if (cid === "fmt ") {
      let tag = v.getUint16(i + 8, true);
      const ch = v.getUint16(i + 10, true), sr = v.getUint32(i + 12, true), bits = v.getUint16(i + 22, true);
      if (tag === 0xFFFE) tag = v.getUint16(i + 32, true);
      fmt = { tag, ch, sr, bits };
    } else if (cid === "data") {
      data = [i + 8, Math.min(d.length, i + 8 + n)];
      break;
    }
    i += 8 + n + (n & 1);
  }
  if (!fmt || !data) throw new Error("WAV without fmt/data");
  const { tag, ch, sr, bits } = fmt, bps = bits >> 3, frame = bps * ch;
  if (!(tag === 1 || tag === 3) || !bps || !ch) throw new Error("unsupported WAV format");
  const nfr = Math.floor((data[1] - data[0]) / frame), x = new Float64Array(nfr);
  for (let f = 0; f < nfr; f++) {
    let acc = 0;
    for (let c = 0; c < ch; c++) {
      const o = data[0] + f * frame + c * bps;
      let s;
      if (tag === 3) s = bps === 4 ? v.getFloat32(o, true) : v.getFloat64(o, true);
      else if (bps === 2) s = v.getInt16(o, true) / 32768;
      else if (bps === 3) s = (((d[o] | (d[o + 1] << 8) | (d[o + 2] << 16)) << 8) >> 8) / 8388608;
      else if (bps === 4) s = v.getInt32(o, true) / 2147483648;
      else s = (d[o] - 128) / 128;
      acc += s;
    }
    x[f] = acc / ch;
  }
  return { sr, x };
}

/* gen_samples.resample: moving average over the ratio, then linear interpolation */
function resample(x, sr, to) {
  if (sr === to) return Array.from(x);
  if (sr > to) {
    const k = Math.max(1, pyRound(sr / to));
    if (k > 1) {
      const y = new Array(x.length);
      for (let i = 0; i < x.length; i++) { let s = 0; for (let j = i; j < Math.min(x.length, i + k); j++) s += x[j]; y[i] = s / k; }
      x = y;
    }
  }
  const step = sr / to, out = [];
  let p = 0;
  while (p < x.length - 1) { const i = Math.floor(p), f = p - i; out.push(x[i] * (1 - f) + x[i + 1] * f); p += step; }
  return out;
}
function pyRound(v) { const f = Math.floor(v), r = v - f; return r > 0.5 ? f + 1 : r < 0.5 ? f : (f % 2 ? f + 1 : f); }

/* mono float -> int16, peak normalised to 30000 */
function normalize(x) {
  let pk = 1e-9;
  for (const v of x) pk = Math.max(pk, Math.abs(v));
  return Int16Array.from(x, (v) => Math.max(-32768, Math.min(32767, Math.trunc(v / pk * 30000))));
}

/* a trimmed sample: raw (mono float at SMP.RATE) from a to b, a fade of FADE samples at both cut ends
 * (no click where the sound was cut; none at the file's own start and end), normalised */
const FADE = 44;                                     /* 2 ms at 22050 Hz */
function takeSample(raw, a, b) {
  a = Math.max(0, Math.min(raw.length - 1, a | 0));
  b = Math.max(a + 1, Math.min(raw.length, b | 0));
  const x = Float64Array.from(raw.subarray ? raw.subarray(a, b) : raw.slice(a, b));
  const n = Math.min(FADE, x.length >> 1);
  for (let i = 0; i < n; i++) {
    const g = i / n;
    if (a > 0) x[i] *= g;
    if (b < raw.length) x[x.length - 1 - i] *= g;
  }
  return normalize(x);
}

/* a trimming view [v0, v1) of n samples: zoomed by factor (< 1 in) around the fraction at of the
 * view, then moved by pan views; at least 256 samples (~12 ms), inside [0, n) */
function zoomView(n, v0, v1, at, factor, pan) {
  const min = Math.min(n, 256);
  let span = Math.round(Math.max(min, Math.min(n, (v1 - v0) * factor)));
  let c = v0 + at * (v1 - v0) + pan * span;         /* the sample under the pointer stays under it */
  let a = Math.round(c - at * span);
  a = Math.max(0, Math.min(n - span, a));
  return [a, a + span];
}

/* where the sound is: the first and last sample above rel x the peak, with a 5 ms pre-roll and a
 * 20 ms tail; [0, length] for silence */
function autoTrim(raw, rel = 0.02) {
  let pk = 0;
  for (const v of raw) pk = Math.max(pk, Math.abs(v));
  if (!pk) return [0, raw.length];
  const th = pk * rel;
  let a = 0, b = raw.length - 1;
  while (a < raw.length && Math.abs(raw[a]) < th) a++;
  while (b > a && Math.abs(raw[b]) < th) b--;
  return [Math.max(0, a - Math.round(SMP.RATE * 0.005)), Math.min(raw.length, b + 1 + Math.round(SMP.RATE * 0.02))];
}

/* root from a file name like "piano_C4" or "F#3" (C4 = 60), else 60 (sampleio.note_from_name) */
function rootFromName(name) {
  const m = /(?<![A-Za-z])([A-G])([#b]?)(-?\d)(?!\d)/.exec(name);
  if (!m) return 60;
  const n = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 }[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + (parseInt(m[3], 10) + 1) * 12;
  return Math.max(0, Math.min(127, n));
}

/* zones: [{s: Int16Array (22050 Hz), root, lo?, hi?}] -> {hdr (480 B), data, zones} (sampleio.user_slot) */
function buildSlot(name, zonesIn) {
  const zones = [], parts = [];
  let len = 0;
  for (const z of zonesIn) {
    const e = imaEncode(z.s, 0);
    zones.push({ off: len, n: z.s.length, ls: 0, le: z.s.length - 1, root: z.root, lo: z.lo ?? null, hi: z.hi ?? null, pred: e.pred, idx: e.idx });
    parts.push(e.data);
    len += e.data.length;
  }
  const data = new Uint8Array(len);
  let o = 0;
  for (const p of parts) { data.set(p, o); o += p.length; }
  if (len > SMP.MAX_DATA) throw new Error(`too long: ${len} B (max ${SMP.MAX_DATA} B)`);
  if (!zones.length || zones.length > SMP.MAX_ZONES) throw new Error("1..16 files per slot");
  zones.sort((a, b) => a.root - b.root);
  zones.forEach((z, j) => {
    if (z.lo == null) {
      z.lo = j === 0 ? 0 : Math.floor((zones[j - 1].root + z.root) / 2) + 1;
      z.hi = j === zones.length - 1 ? 127 : Math.floor((z.root + zones[j + 1].root) / 2);
    }
  });
  const hdr = new Uint8Array(SMP.HDR_LEN), v = new DataView(hdr.buffer);
  v.setUint32(0, 0x504D5346, true);
  v.setUint16(4, 1, true);
  hdr[6] = zones.length;
  const nm = String(name).toUpperCase().replace(/[^\x20-\x7E]/g, "").slice(0, 8);
  for (let i = 0; i < nm.length; i++) hdr[8 + i] = nm.charCodeAt(i);
  v.setUint32(16, len, true);
  v.setUint32(20, crc32(data), true);
  const rate = pyRound(SMP.RATE / 44100 * 65536);
  zones.forEach((z, j) => {
    const b = 32 + j * 28;
    [z.off, z.n, z.ls, z.le, rate].forEach((x, k) => v.setUint32(b + k * 4, x >>> 0, true));
    v.setInt16(b + 20, z.root * 16, true);
    v.setInt16(b + 22, z.pred, true);
    hdr[b + 24] = z.idx; hdr[b + 25] = z.lo; hdr[b + 26] = z.hi; hdr[b + 27] = 0;
  });
  return { hdr, data, zones };
}

/* -------------------------------------------------------------- librarian --- */
/* A patch (library entry, user preset):
     {name, engine (index), engineName, p: [P_COUNT values by parameter id, null = unknown],
      pattern: 16 x [note 0..127 (0 rest), flags 1 accent | 2 slide | 4 tie] or null,
      grid: 16 x [lane hits 0..255, their accents] or null (a DRUM sound's 16 steps; then no pattern),
      tags: [], created, modified}

   Library / bank / single-patch file (JSON):
     {
       "format": "felucca-library", "version": 1,
       "kind": "library" | "bank" | "patch",
       "firmware": "FELUCCA 0.5 ...",          device version string when exported ("" if unknown)
       "pCount": 57, "pE0": 49,                 P_COUNT and the first engine parameter id
       "paramLabels": ["LVL", "ATK", ...],      one key per parameter id: the DESC label, "#2", "#3" appended to
                                                a repeated label (PIT, PIT#2), and "E0".."E7" for the engine
                                                parameters (their labels depend on the engine)
       "engines": ["ANALOG", ...],              engine names by index
       "exported": "2026-10-03T12:00:00.000Z",
       "patches": [{ "name", "engine", "engineName", "params": [pCount numbers or null],
                     "pattern": [[note, flags] x 16] or null, "grid": [[hits, accents] x 16] (when there is one),
                     "tags": [...], "created", "modified",
                     "slot": n (bank files only, 0-based) }]
     }
   Reading maps every parameter by its key, so a firmware with other ids (or more parameters) still gets
   the right values; parameters the file does not have are null (left at the engine default). Engines are
   matched by name. The old single-sound file ("felucca-patch" version 1, "Save to file") is read too. */
const SMP_RC = { 1: "size", 2: "header", 3: "data CRC", 4: "flash", 5: "zones" };
const kib = (n) => (n / 1024).toFixed(1);

/* auto key split, as in buildSlot (for the preview) */
function splitKeys(files) {
  const z = files.map((f, i) => ({ i, root: f.root })).sort((a, b) => a.root - b.root);
  const out = [];
  z.forEach((x, j) => {
    out[x.i] = [j === 0 ? 0 : Math.floor((z[j - 1].root + x.root) / 2) + 1, j === z.length - 1 ? 127 : Math.floor((x.root + z[j + 1].root) / 2)];
  });
  return out;
}
const draftBytes = (d) => d.files.reduce((a, f) => a + ((f.s.length + 1) >> 1), 0);

async function decodeFile(f) {
  const buf = await f.arrayBuffer();
  let x;
  try {
    const w = parseWav(buf);
    x = resample(w.x, w.sr, SMP.RATE);
  } catch (e) {                                     /* not a plain WAV: let the browser decode it */
    const Ctx = window.OfflineAudioContext || window.webkitOfflineAudioContext;
    const ab = await new Ctx(1, 1, SMP.RATE).decodeAudioData(buf.slice(0));
    x = new Float64Array(ab.length);
    for (let c = 0; c < ab.numberOfChannels; c++) { const d = ab.getChannelData(c); for (let i = 0; i < d.length; i++) x[i] += d[i] / ab.numberOfChannels; }
  }
  if (!x.length) throw new Error("no audio");
  const raw = Float64Array.from(x);                 /* kept for trimming: s is raw[a, b) (takeSample) */
  return { fname: f.name, raw, a: 0, b: raw.length, s: takeSample(raw, 0, raw.length),
           root: rootFromName(f.name.replace(/\.[^.]*$/, "")) };
}
return { SMP, buildSlot, decodeFile, splitKeys, draftBytes, kib, SMP_RC, noteName, parseNote, autoTrim, takeSample, pack7 };
})();
