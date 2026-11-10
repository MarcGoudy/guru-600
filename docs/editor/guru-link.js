// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the link to the FM-1 (Web MIDI, SysEx). Two kinds of frames:
//   Felucca's   F0 7D 46 4C cmd .. F7   (Felucca/web/EDITOR_PROTOCOL.md: INFO, GET, SET, DUMP, DESC, WATCH, TRACK...)
//   Guru-600's  F0 7D 47 36 cmd .. F7   (firmware editor.c ed_p6, eng_p600.c p600_sysex: the 255 places, MORPH)
// Every request gets one answer with the same header and cmd; while watched, the device pushes CHANGED (23),
// RELOAD (24), STEP_CHANGED (26) and TRACK_CHANGED (32).

const FL = [0x7D, 0x46, 0x4C], G6 = [0x7D, 0x47, 0x36];
const CMD = { INFO: 1, GET: 2, SET: 3, DUMP: 4, DESC: 5, WATCH: 22, CHANGED: 23, RELOAD: 24, PING: 25, STEP_CHANGED: 26,
  TRACK: 27, TRACK_CHANGED: 32 };
const P6 = { IMPORT: 1, RESET: 2, FORGET: 3, EXPORT: 4, LIST: 5, SAVE: 6, NAMES: 8, LOAD: 9, STATE: 10, MORPH: 11,
  MUTATE: 12, MSTATE: 13, BEAT: 14 };
const PUSH = new Set([CMD.CHANGED, CMD.RELOAD, CMD.STEP_CHANGED, CMD.TRACK_CHANGED]);

const v14enc = (v) => { const u = Math.max(-8192, Math.min(8191, Math.round(v))) + 8192; return [u & 0x7F, (u >> 7) & 0x7F]; };
const v14dec = (lo, hi) => (lo | (hi << 7)) - 8192;
const place2 = (d) => [d & 0x7F, d >> 7];
function str(a, i) { let s = ""; while (i < a.length && a[i]) s += String.fromCharCode(a[i++]); return [s, i + 1]; }

// one request at a time; the answer is the next frame with the same header and cmd (and, for GET / SET / DESC, the same
// scope and id; for the place commands, the same place)
class Link {
  constructor(input, output, onPush) {
    this.out = output; this.onPush = onPush; this.q = Promise.resolve(); this.wait = null; this.buf = [];
    input.onmidimessage = (e) => this.rx(e.data);
  }
  rx(data) {
    // a note the FM-1's keys play (seq.c key_on / key_off send it to MIDI OUT, on the track's channel): shown
    if (data.length === 3 && (data[0] & 0xE0) === 0x80 && this.onNote) {
      this.onNote(data[0] & 15, data[1], (data[0] & 0xF0) === 0x90 ? data[2] : 0); return;
    }
    for (const b of data) {
      if (b === 0xF0) { this.buf = [b]; continue; }
      if (!this.buf.length) continue;
      if (b >= 0xF8) continue;                          // realtime bytes inside SysEx
      this.buf.push(b);
      if (b === 0xF7) { const f = this.buf; this.buf = []; this.frame(f); }
      else if (this.buf.length > 4096) this.buf = [];
    }
  }
  frame(f) {
    const hdr = f.slice(1, 4), cmd = f[4], a = f.slice(5, -1);
    const fl = hdr.every((x, i) => x === FL[i]), g6 = hdr.every((x, i) => x === G6[i]);
    if (!fl && !g6) return;
    const w = this.wait;
    if (w && w.g6 === g6 && w.cmd === cmd && w.match(a)) { this.wait = null; clearTimeout(w.t); w.ok(a); return; }
    if (fl && PUSH.has(cmd)) this.onPush(cmd, a);
    if (g6 && cmd === P6.BEAT) this.onPush("beat", a);   // (Guru-600: the beat, firmware editor.c ed_p6_beat)
  }
  // a request: [header, cmd, args], match(a) the answer; resolves with the answer's args
  ask(g6, cmd, args = [], match = () => true, timeout = 600) {
    const run = () => new Promise((ok, ko) => {
      this.wait = { g6, cmd, match, ok, t: setTimeout(() => { this.wait = null; ko(new Error("timeout " + cmd)); }, timeout) };
      this.out.send([0xF0, ...(g6 ? G6 : FL), cmd, ...args, 0xF7]);
    });
    const p = this.q.then(run, run);
    this.q = p.catch(() => {});
    return p;
  }
  close() { if (this.wait) clearTimeout(this.wait.t); this.wait = null; }
}

// the device as the editor uses it
class Device {
  constructor(link) { this.link = link; }
  async info() {
    const a = await this.link.ask(false, CMD.INFO);
    let [version, i] = str(a, 0);
    const neng = a[i], pcount = a[i + 1], gcount = a[i + 2], nstep = a[i + 3], pe0 = a[i + 4];
    i += 5;
    const engines = [];
    for (let k = 0; k < neng; k++) { let s; [s, i] = str(a, i); engines.push(s); }
    const ntrk = a[i] || 1, tr = a.slice(i + 1);   // (Felucca's trailer: SONG, preferences, MOTION, then the backup's caps)
    const backupCaps = tr[0] === 16 && tr[1] === 0x55 && tr[2] === 1 && (tr[3] & 15) && tr[4] === 0x4d && tr[5] === 1 && tr[6] === 64 && tr[8] === 0x42 && tr[9] === 1 ? tr[10] & 3 : 0;
    return { version, neng, pcount, gcount, nstep, pe0, engines, ntrk, backupCaps };
  }
  async desc(id, scope = 0) {
    const a = await this.link.ask(false, CMD.DESC, [scope, id], (r) => r[0] === scope && r[1] === id);
    const d = { fmt: a[2], min: v14dec(a[3], a[4]), max: v14dec(a[5], a[6]), def: v14dec(a[7], a[8]), names: [] };
    let i = 9;
    [d.label, i] = str(a, i);
    [d.unit, i] = str(a, i);
    if (d.fmt === 8) for (let k = d.min; k <= d.max && i < a.length; k++) { let s; [s, i] = str(a, i); d.names.push(s); }
    return d;
  }
  async set(id, v, scope = 0) {
    const a = await this.link.ask(false, CMD.SET, [scope, id, ...v14enc(v)], (r) => r[0] === scope && r[1] === id);
    return v14dec(a[2], a[3]);
  }
  async dump(pcount) {
    const a = await this.link.ask(false, CMD.DUMP, [], () => true, 1000);
    const p = [], g = [];
    for (let k = 0; k < pcount; k++) p.push(v14dec(a[2 + 2 * k], a[3 + 2 * k]));
    for (let k = 2 + 2 * pcount; k + 1 < a.length; k += 2) g.push(v14dec(a[k], a[k + 1]));   // (the globals after)
    return { engine: a[0], p, g };
  }
  async watch(on) { return (await this.link.ask(false, CMD.WATCH, [on ? 1 : 0]))[0]; }
  ping() { return this.link.ask(false, CMD.PING); }
  async track(sel) {
    const a = await this.link.ask(false, CMD.TRACK, sel == null ? [] : [sel & 3]);
    const n = a[1], tracks = [];
    for (let k = 0; k < n; k++) {   // per track: engine, preset, level (v14: 2 bytes), mute, armed
      const o = 2 + 6 * k;
      tracks.push({ engine: a[o], preset: a[o + 1], level: v14dec(a[o + 2], a[o + 3]), mute: a[o + 4], armed: a[o + 5] });
    }
    return { sel: a[0], tracks };
  }
  // the sequencer (Felucca's STEP_GET / STEP_SET, MOTION; Guru-600's TOOL)
  async stepGet(i) {
    const a = await this.link.ask(false, 6, [i & 63], (r) => r[0] === (i & 63));
    return { n: a[1], notes: a.slice(2, 6), time: a[6], flags: a[7], vel: a[8], hit: a[9] | (a[11] & 1) << 7, acc: a[10] | (a[11] >> 1 & 1) << 7,
             chance: a[12] ?? 100, ratchet: a[13] || 1, nudge: (a[14] ?? 8) - 8, cond: a[15] || 0 };
  }
  async stepSet(i, s) {
    const args = [i & 63, Math.max(0, Math.min(4, s.n)), ...[0, 1, 2, 3].map((k) => (s.notes[k] | 0) & 127), s.time & 3, s.flags & 3, s.vel & 127,
      s.hit & 127, s.acc & 127, (s.hit >> 7 & 1) | (s.acc >> 7 & 1) << 1, Math.max(0, Math.min(100, s.chance)), Math.max(1, Math.min(4, s.ratchet)),
      Math.max(0, Math.min(15, s.nudge + 8)), Math.max(0, Math.min(11, s.cond))];
    return this.link.ask(false, 7, args, (r) => r[0] === (i & 63));
  }
  async motion(track) {   // every record: {on, max, list: [{step, id, v, lock}]}
    const a = await this.link.ask(false, 64, [track & 3, 8], (r) => r[0] === (track & 3), 1000);
    const n = a[3] | a[4] << 7, max = a[5] | a[6] << 7, list = [];
    for (let k = 0; k < n; k++) list.push({ step: a[7 + 4 * k], id: a[8 + 4 * k], v: v14dec(a[9 + 4 * k], a[10 + 4 * k]) });
    for (let k = 0; k < n; k++) list[k].lock = a[7 + 4 * n + k] === 1;
    return { on: !!a[2], max, list };
  }
  motionOp(track, op, args = []) { return this.link.ask(false, 64, [track & 3, op, ...args], (r) => r[0] === (track & 3)); }
  async tool(p, h = 0, st = 16, rot = 0) { return (await this.link.ask(true, 16, [p, h, st, rot], () => true, 1500))[1]; }
  // Guru-600: the places
  async state() { const a = await this.link.ask(true, P6.STATE); return { sel: a[0], engine: a[1], place: a[2] | a[3] << 7, kept: !!a[4] }; }
  async names(start, k) {
    const a = await this.link.ask(true, P6.NAMES, [...place2(start), k], (r) => (r[0] | r[1] << 7) === start, 1000);
    const out = [];
    let i = 3;
    for (let n = 0; n < a[2]; n++) { const kept = !!a[i++]; let s; [s, i] = str(a, i); out.push({ kept, name: s }); }
    return out;
  }
  async load(d) { return (await this.link.ask(true, P6.LOAD, place2(d), (r) => (r[0] | r[1] << 7) === d))[2]; }
  async save(d) { return (await this.link.ask(true, P6.SAVE, place2(d), (r) => (r[0] | r[1] << 7) === d, 2000))[2]; }
  async forget(d) { return (await this.link.ask(true, P6.FORGET, place2(d), (r) => (r[0] | r[1] << 7) === d))[2]; }
  async reset() { return (await this.link.ask(true, P6.RESET, [], () => true, 2000))[2]; }
  async rename(d, nm) { return (await this.link.ask(true, 7, [...place2(d), ...[...nm].map((c) => c.charCodeAt(0) & 127)], (r) => (r[0] | r[1] << 7) === d))[2]; }
  async importTo(d, body) { return (await this.link.ask(true, P6.IMPORT, [...place2(d), ...body], (r) => (r[0] | r[1] << 7) === d || (r[0] | r[1] << 7) === 255))[2]; }
  async exportOf(d) {   // -> {name, sci: [F0 01 02 nn .. F7]}
    const a = await this.link.ask(true, P6.EXPORT, place2(d), (r) => (r[0] | r[1] << 7) === d);
    let name = ""; for (let k = 2; k < 18 && a[k]; k++) name += String.fromCharCode(a[k]);
    return { name, sci: [0xF0, ...a.slice(18, 53), 0xF7] };
  }
  async morph(b, pos) { return (await this.link.ask(true, P6.MORPH, [...place2(b), pos], (r) => (r[0] | r[1] << 7) === b))[3]; }
  async mutate(amt) { return (await this.link.ask(true, P6.MUTATE, [amt]))[1]; }
  async morphState() { const a = await this.link.ask(true, P6.MSTATE); return { b: a[0] | a[1] << 7, pos: a[2], amt: a[3] }; }
}

// the SysEx messages of a .syx file that are Prophet-600 sounds: Sequential's (F0 01 02 nn .. 35 bytes) or GliGli's
// (F0 00 61 16 01 ..), as the send page reads them (p600/site/envoi-sons.src.html)
// the name a .syx carries (the editor's record F0 7D 47 36 07 00 00 name F7, after the program), or ""
function syxName(buf) {
  const d = new Uint8Array(buf);
  for (let i = 0; i + 7 < d.length; i++)
    if (d[i] === 0xF0 && d[i + 1] === 0x7D && d[i + 2] === 0x47 && d[i + 3] === 0x36 && d[i + 4] === 7) {
      let j = i + 7, t = ""; while (j < d.length && d[j] !== 0xF7) t += String.fromCharCode(d[j++]); return t;
    }
  return "";
}
function parseSyx(buf) {
  const d = new Uint8Array(buf), list = [];
  for (let i = 0; i < d.length; i++) {
    if (d[i] !== 0xF0) continue;
    let j = i + 1;
    while (j < d.length && d[j] !== 0xF7) j++;
    const m = [...d.slice(i + 1, j)];
    if ((m.length === 35 && m[0] === 0x01 && m[1] === 0x02) || (m.length > 9 && m[0] === 0x00 && m[1] === 0x61 && m[2] === 0x16 && m[3] === 0x01)) list.push(m);
    i = j;
  }
  return list;
}
