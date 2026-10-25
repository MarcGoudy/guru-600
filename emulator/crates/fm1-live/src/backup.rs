//! Guru-600: the application's memory as a complete backup of the Felucca web editor (web/fm1backup.js: the same
//! JSON file, its "felucca-backup" objects), and back. Export: the objects read from the emulated flash as
//! editor_backup.c lists them (storage.c's commit records, the sample slots, the FM6 voice bank, the P600 places, SLICE's
//! records); the editor's Restore backup then puts them on a FM-1. Import: an editor backup (of a FM-1, or of this
//! application) written into the flash as the firmware itself would have saved it, before the machine starts again.
//! The flash map: Felucca's firmware/src/storage.c. No JSON dependency: the file's few fields, read and written here.

const ST_MAGIC: u32 = 0x554C_4546; // "FELU"
const SECTOR: usize = 4096;
const PAYLOAD_OFF: usize = 256;
const PAYLOAD_MAX: usize = SECTOR - PAYLOAD_OFF;
// storage.c's objects
const OBJ_SETTINGS: u32 = 0;
const OBJ_PROJECT0: u32 = 1;
const OBJ_UPRESET0: u32 = 5;
const OBJ_FM6BANK: u32 = 7;
const OBJ_UPFM6: u32 = 8;
const OBJ_AUTOSAVE: u32 = 9;
const OBJ_P600: u32 = 10;
const OBJ_FM6VB: u32 = 32;
// the user sample slots (eng_sample.c), SLICE's record in each one's last sector (slice_store.c)
const SMP_BASE: usize = 0xA0000;
const SMP_SIZE: usize = 0x14000;
const SMP_DATA: usize = 512;
const SMP_MAGIC: u32 = 0x504D_5346; // "FSMP"
const SLC_OFF: usize = SMP_SIZE - 0x1000;
const SLC_LEN: usize = 152;
const SLC_MAGIC: u32 = 0x314D_4C53; // "SLM1"
// the FM6 voice bank (fm6_vbank.c)
const FVB_HOME: usize = 0xE7000;
const FVB_INFO: usize = 224;
const FVB_LEN: usize = 3616;
const FVB_MAGIC: u32 = 0x5636_4D46; // "FM6V"

/// the settings' CALIBRATION (persist_t.panel: 16..48), and the firmware's PANEL_DEFAULT (panel.c): the application's own
const PANEL_AT: usize = 16;
const PANEL_DEFAULT: [u8; 32] = [53, 78, 65, 80, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 1, 0, 1, 6, 2, 3, 4, 5, 1, 1, 1, 1, 1, 1, 1];

/// the editor's object ids, in its order (fm1backup.js BACKUP_IDS), and those of older archives
const IDS: [u32; 16] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 32, 33, 34, 10, 11, 12];

fn crc32(b: &[u8]) -> u32 {
    let mut c = 0xFFFF_FFFFu32;
    for &x in b {
        c ^= x as u32;
        for _ in 0..8 {
            c = (c >> 1) ^ if c & 1 != 0 { 0xEDB8_8320 } else { 0 };
        }
    }
    !c
}
fn rd32(f: &[u8], at: usize) -> u32 { u32::from_le_bytes([f[at], f[at + 1], f[at + 2], f[at + 3]]) }
fn rd16(f: &[u8], at: usize) -> u32 { u16::from_le_bytes([f[at], f[at + 1]]) as u32 }

/// storage.c st_sector: copy A (0) / B (1) of an object
fn sector(obj: u32, copy: u32) -> usize {
    let c = copy as usize * SECTOR;
    match obj {
        OBJ_SETTINGS => 0xFC000 + c,
        OBJ_FM6BANK | OBJ_UPFM6 => if copy == 1 { 0xFE000 } else { 0x9F000 },
        OBJ_AUTOSAVE => 0xE5000 + c,
        OBJ_P600 => 0xD9000 + c,
        o if o >= OBJ_UPRESET0 => 0xDC000 + (o - OBJ_UPRESET0) as usize * 2 * SECTOR + c,
        o => 0x97000 + (o - OBJ_PROJECT0) as usize * 2 * SECTOR + c,
    }
}

/// storage.c st_head + st_body: a copy's (seq, payload), valid
fn copy_of(f: &[u8], obj: u32, copy: u32) -> Option<(u32, &[u8])> {
    let b = sector(obj, copy);
    let h = &f[b..b + 32];
    let len = rd32(h, 12) as usize;                 // (st_hdr_t: magic, type, slot, seq, len, crc, rsv[2], hcrc)
    if rd32(h, 0) != ST_MAGIC || rd16(h, 4) != obj || rd16(h, 6) != copy || len > PAYLOAD_MAX || rd32(h, 28) != crc32(&h[..28]) {
        return None;
    }
    let p = &f[b + PAYLOAD_OFF..b + PAYLOAD_OFF + len];
    (crc32(p) == rd32(h, 16)).then_some((rd32(h, 8), p))
}

/// storage.c st_current: the newest valid copy's payload (A on a tie)
fn load(f: &[u8], obj: u32) -> Option<Vec<u8>> {
    let (a, b) = (copy_of(f, obj, 0), copy_of(f, obj, 1));
    match (a, b) {
        (Some((sa, pa)), Some((sb, pb))) => Some(if sb != sa && sb.wrapping_sub(sa) < 0x8000_0000 { pb } else { pa }.to_vec()),
        (Some((_, p)), None) | (None, Some((_, p))) => Some(p.to_vec()),
        _ => None,
    }
}

/// a user slot's sample, header and data, as the editor's file holds it (and fm1backup.js checks it), or none
fn sample(f: &[u8], k: usize) -> Option<&[u8]> {
    let s = &f[SMP_BASE + k * SMP_SIZE..SMP_BASE + (k + 1) * SMP_SIZE];
    let len = rd32(s, 16) as usize;
    let count = s[6] as usize;
    if rd32(s, 0) != SMP_MAGIC || rd16(s, 4) != 1 || count == 0 || count > 16 || len == 0 || SMP_DATA + len > SMP_SIZE ||
        SMP_DATA + len > 81920 || crc32(&s[SMP_DATA..SMP_DATA + len]) != rd32(s, 20) {
        return None;
    }
    for z in 0..count {
        let o = 32 + z * 28;
        let (start, n, ls, le, rate) = (rd32(s, o) as usize, rd32(s, o + 4) as usize, rd32(s, o + 8), rd32(s, o + 12), rd32(s, o + 16));
        if n == 0 || start > len || n.div_ceil(2) > len - start || n > 163_840 || ls > le || le as usize >= n || rate == 0 ||
            rate > 262_144 || s[o + 24] > 88 || s[o + 25] > s[o + 26] {
            return None;
        }
    }
    Some(&s[..SMP_DATA + len])
}

/// the FM6 voice bank's payload (its header and voices) at 0xE7000, valid, or none
fn voice_bank(f: &[u8]) -> Option<&[u8]> {
    let h = &f[FVB_HOME..FVB_HOME + 32];
    let p = &f[FVB_HOME + FVB_INFO..FVB_HOME + FVB_INFO + FVB_LEN];
    (rd32(h, 0) == ST_MAGIC && rd16(h, 4) == OBJ_FM6VB && rd16(h, 6) == 0 && rd32(h, 12) as usize == FVB_LEN &&
        rd32(h, 28) == crc32(&h[..28]) && crc32(p) == rd32(h, 16) && rd32(p, 0) == FVB_MAGIC && rd16(p, 4) == 1 && rd16(p, 6) == 32)
        .then_some(p)
}

// ---- base64, the file's dates

const B64: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
fn b64(b: &[u8]) -> String {
    let mut s = String::with_capacity(b.len().div_ceil(3) * 4);
    for c in b.chunks(3) {
        let n = (c[0] as u32) << 16 | (*c.get(1).unwrap_or(&0) as u32) << 8 | *c.get(2).unwrap_or(&0) as u32;
        for i in 0..4 {
            s.push(if i <= c.len() { B64[(n >> (18 - 6 * i)) as usize & 63] as char } else { '=' });
        }
    }
    s
}
fn unb64(s: &str) -> Option<Vec<u8>> {
    let mut out = Vec::with_capacity(s.len() / 4 * 3);
    for c in s.as_bytes().chunks(4) {
        if c.len() != 4 {
            return None;
        }
        let mut n = 0u32;
        let mut pad = 0;
        for &x in c {
            n <<= 6;
            if x == b'=' {
                pad += 1;
            } else if pad > 0 {
                return None;
            } else {
                n |= B64.iter().position(|&y| y == x)? as u32;
            }
        }
        out.extend_from_slice(&n.to_be_bytes()[1..4 - pad]);
    }
    Some(out)
}
fn now_iso() -> String {
    let t = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map_or(0, |d| d.as_secs()) as i64;
    let (days, s) = (t.div_euclid(86_400), t.rem_euclid(86_400));
    // (days since 1970-01-01 -> the civil date: H. Hinnant's algorithm)
    let z = days + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z - era * 146_097;
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = doy - (153 * mp + 2) / 5 + 1;
    let m = if mp < 10 { mp + 3 } else { mp - 9 };
    let y = yoe + era * 400 + (m <= 2) as i64;
    format!("{y:04}-{m:02}-{d:02}T{:02}:{:02}:{:02}.000Z", s / 3600, s / 60 % 60, s % 60)
}

/// the application's memory -> the editor's backup file (JSON). The current music is the one the application saved
/// last (its autosave: what it starts with); none yet, the file has none and the editor keeps the FM-1's
pub fn export(f: &[u8]) -> String {
    let mut objs = Vec::new();
    for &id in &IDS {
        let bytes: Vec<u8> = match id {
            0 => load(f, OBJ_AUTOSAVE).unwrap_or_default(),
            1 => load(f, OBJ_SETTINGS).unwrap_or_default(),
            2..=5 => load(f, OBJ_PROJECT0 + id - 2).unwrap_or_default(),
            6 | 7 => load(f, OBJ_UPRESET0 + id - 6).unwrap_or_default(),
            8 => Vec::new(),                                           // (the retired FM6 bank: always empty)
            9 => load(f, OBJ_UPFM6).unwrap_or_default(),
            10 => load(f, OBJ_P600).unwrap_or_default(),
            11 => voice_bank(f).map(|p| p.to_vec()).unwrap_or_default(),
            12 => {
                let mut r = vec![0u8; 3 * SLC_LEN];
                for k in 0..3 {
                    if let Some(s) = sample(f, k) {
                        let at = SMP_BASE + k * SMP_SIZE + SLC_OFF;
                        if s.len() <= SLC_OFF && rd32(f, at) == SLC_MAGIC {
                            r[k * SLC_LEN..(k + 1) * SLC_LEN].copy_from_slice(&f[at..at + SLC_LEN]);
                        }
                    }
                }
                r
            }
            _ => sample(f, (id - 32) as usize).map(|s| s.to_vec()).unwrap_or_default(),
        };
        let crc = if bytes.is_empty() { 0 } else { crc32(&bytes) };
        objs.push(format!("{{\"id\":{id},\"size\":{},\"crc\":{crc},\"data\":\"{}\"}}", bytes.len(), b64(&bytes)));
    }
    format!("{{\"format\":\"felucca-backup\",\"version\":1,\"firmware\":\"Guru-600 application\",\"source\":\"guru-600-app\",\
             \"created\":\"{}\",\"objects\":[{}]}}\n", now_iso(), objs.join(","))
}

// ---- reading the file: a small JSON parser, enough for the editor's backups

#[derive(Debug)]
enum J {
    N(f64),
    S(String),
    A(Vec<J>),
    O(Vec<(String, J)>),
    Other,
}
struct P<'a> {
    s: &'a [u8],
    i: usize,
}
impl P<'_> {
    fn ws(&mut self) {
        while self.i < self.s.len() && self.s[self.i].is_ascii_whitespace() {
            self.i += 1;
        }
    }
    fn val(&mut self) -> Option<J> {
        self.ws();
        match *self.s.get(self.i)? {
            b'{' => {
                self.i += 1;
                let mut v = Vec::new();
                loop {
                    self.ws();
                    if self.s.get(self.i) == Some(&b'}') {
                        self.i += 1;
                        return Some(J::O(v));
                    }
                    let J::S(k) = self.val()? else { return None };
                    self.ws();
                    if self.s.get(self.i) != Some(&b':') {
                        return None;
                    }
                    self.i += 1;
                    v.push((k, self.val()?));
                    self.ws();
                    match self.s.get(self.i)? {
                        b',' => self.i += 1,
                        b'}' => {}
                        _ => return None,
                    }
                }
            }
            b'[' => {
                self.i += 1;
                let mut v = Vec::new();
                loop {
                    self.ws();
                    if self.s.get(self.i) == Some(&b']') {
                        self.i += 1;
                        return Some(J::A(v));
                    }
                    v.push(self.val()?);
                    self.ws();
                    match self.s.get(self.i)? {
                        b',' => self.i += 1,
                        b']' => {}
                        _ => return None,
                    }
                }
            }
            b'"' => {
                self.i += 1;
                let mut out = Vec::new();
                loop {
                    let c = *self.s.get(self.i)?;
                    self.i += 1;
                    match c {
                        b'"' => return String::from_utf8(out).ok().map(J::S),
                        b'\\' => {
                            let e = *self.s.get(self.i)?;
                            self.i += 1;
                            match e {
                                b'u' => {
                                    let h = std::str::from_utf8(self.s.get(self.i..self.i + 4)?).ok()?;
                                    self.i += 4;
                                    let ch = char::from_u32(u32::from_str_radix(h, 16).ok()?).unwrap_or('?');
                                    out.extend_from_slice(ch.to_string().as_bytes());
                                }
                                b'n' => out.push(b'\n'),
                                b't' => out.push(b'\t'),
                                b'r' => out.push(b'\r'),
                                b'b' => out.push(8),
                                b'f' => out.push(12),
                                x => out.push(x),
                            }
                        }
                        x => out.push(x),
                    }
                }
            }
            b't' | b'f' | b'n' => {
                while self.i < self.s.len() && self.s[self.i].is_ascii_alphabetic() {
                    self.i += 1;
                }
                Some(J::Other)
            }
            _ => {
                let st = self.i;
                while self.i < self.s.len() && matches!(self.s[self.i], b'-' | b'+' | b'.' | b'e' | b'E' | b'0'..=b'9') {
                    self.i += 1;
                }
                std::str::from_utf8(&self.s[st..self.i]).ok()?.parse().ok().map(J::N)
            }
        }
    }
}
fn field<'a>(o: &'a [(String, J)], k: &str) -> Option<&'a J> { o.iter().find(|(x, _)| x == k).map(|(_, v)| v) }
fn num(o: &[(String, J)], k: &str) -> Option<u64> {
    match field(o, k)? {
        J::N(n) if *n >= 0.0 && n.fract() == 0.0 => Some(*n as u64),
        _ => None,
    }
}

/// an editor backup file -> its objects (id, bytes), checked as fm1backup.js readBackup checks them
pub fn read(text: &str) -> Result<Vec<(u32, Vec<u8>)>, String> {
    let bad = || "Not a complete Felucca backup".to_string();
    let J::O(top) = (P { s: text.as_bytes(), i: 0 }).val().ok_or_else(bad)? else { return Err(bad()) };
    if !matches!(field(&top, "format"), Some(J::S(s)) if s == "felucca-backup") || num(&top, "version") != Some(1) {
        return Err(bad());
    }
    let Some(J::A(list)) = field(&top, "objects") else { return Err(bad()) };
    // the id lists of each firmware's archives (fm1backup.js idsOf)
    let v3: Vec<u32> = IDS.iter().copied().filter(|&i| !(10..32).contains(&i)).collect();
    let v2: Vec<u32> = v3.iter().copied().filter(|&i| i != 9).collect();
    let v1: Vec<u32> = v2.iter().copied().filter(|&i| i != 8).collect();
    let ids: Vec<u32> = [IDS.to_vec(), v3, v2, v1].into_iter().find(|l| l.len() == list.len()).ok_or_else(bad)?;
    let mut out = Vec::new();
    for (o, &want) in list.iter().zip(&ids) {
        let J::O(o) = o else { return Err(bad()) };
        let (id, size, crc) = (num(o, "id"), num(o, "size"), num(o, "crc"));
        let Some(J::S(data)) = field(o, "data") else { return Err("Invalid backup object".into()) };
        let (Some(id), Some(size), Some(crc)) = (id, size, crc) else { return Err("Invalid backup object".into()) };
        if id as u32 != want || size > if id >= 32 { 81_920 } else { PAYLOAD_MAX as u64 } {
            return Err("Invalid backup object".into());
        }
        let bytes = unb64(data).ok_or("Invalid backup object")?;
        if bytes.len() as u64 != size || (size > 0 && crc32(&bytes) as u64 != crc) || (size == 0 && crc != 0) {
            return Err("Backup checksum mismatch".into());
        }
        out.push((id as u32, bytes));
    }
    Ok(out)
}

/// the objects written into the flash f as the firmware saves them: each one's copy A (sequence 1), the sample
/// slots, the voice bank, the places, the slices; every other data sector of the map erased first (what the
/// backup does not hold is not there any more, as on a FM-1 restored). The firmware's area is left as it is
pub fn import(f: &mut [u8], objs: &[(u32, Vec<u8>)]) -> Result<(), String> {
    let get = |id: u32| objs.iter().find(|(i, _)| *i == id).map(|(_, b)| b.as_slice()).filter(|b| !b.is_empty());
    // (the settings keep the application's own CALIBRATION: a FM-1's buttons and knobs are not wired as the panel drawn here)
    let own_panel: Vec<u8> = load(f, OBJ_SETTINGS).filter(|p| p.len() >= PANEL_AT + 32).map_or(PANEL_DEFAULT.to_vec(), |p| p[PANEL_AT..PANEL_AT + 32].to_vec());
    for (id, b) in objs {
        if (*id < 32 && b.len() > PAYLOAD_MAX) || (*id == 11 && !b.is_empty() && b.len() != FVB_LEN) || (*id == 12 && !b.is_empty() && b.len() != 3 * SLC_LEN) {
            return Err("Invalid backup object".into());
        }
    }
    let mut erase = |at: usize, n: usize| f[at..at + n].fill(0xFF);
    erase(0x97000, 0x8000);                           // the projects
    erase(0x9F000, SECTOR);                           // the FM6 patches' copy A (B: 0xFE000)
    erase(0xFE000, SECTOR);
    erase(SMP_BASE, 3 * SMP_SIZE);                    // the sample slots (and the places, and the slices, in them)
    erase(0xDC000, 4 * SECTOR);                       // the user preset banks
    erase(0xE5000, 3 * SECTOR);                       // the autosave's pair, the voice bank
    erase(0xFC000, 2 * SECTOR);                       // the settings
    let put = |f: &mut [u8], obj: u32, p: &[u8]| {   // storage.c st_save_to: the payload, then its commit record
        let b = sector(obj, 0);
        let mut h = Vec::with_capacity(32);
        for v in [ST_MAGIC] { h.extend_from_slice(&v.to_le_bytes()); }
        h.extend_from_slice(&(obj as u16).to_le_bytes());
        h.extend_from_slice(&0u16.to_le_bytes());                  // slot: copy A
        for v in [1u32, p.len() as u32, crc32(p), 0xFFFF_FFFF, 0xFFFF_FFFF] { h.extend_from_slice(&v.to_le_bytes()); }
        let hc = crc32(&h);
        h.extend_from_slice(&hc.to_le_bytes());
        f[b..b + 32].copy_from_slice(&h);
        f[b + PAYLOAD_OFF..b + PAYLOAD_OFF + p.len()].copy_from_slice(p);
    };
    if let Some(p) = get(0) { put(f, OBJ_AUTOSAVE, p); }
    if let Some(p) = get(1) {
        let mut p = p.to_vec();
        if p.len() >= PANEL_AT + 32 {
            p[PANEL_AT..PANEL_AT + 32].copy_from_slice(&own_panel);
        }
        put(f, OBJ_SETTINGS, &p);
    }
    for k in 0..4 { if let Some(p) = get(2 + k) { put(f, OBJ_PROJECT0 + k, p); } }
    for k in 0..2 { if let Some(p) = get(6 + k) { put(f, OBJ_UPRESET0 + k, p); } }
    if let Some(p) = get(9) { put(f, OBJ_UPFM6, p); } else if let Some(p) = get(8) { put(f, OBJ_FM6BANK, p); }
    for k in 0..3 {
        if let Some(s) = get(32 + k as u32) {
            f[SMP_BASE + k * SMP_SIZE..SMP_BASE + k * SMP_SIZE + s.len()].copy_from_slice(s);
        }
    }
    if let Some(p) = get(10) { put(f, OBJ_P600, p); }
    if let Some(p) = get(11) {
        let mut h = Vec::with_capacity(32);
        h.extend_from_slice(&ST_MAGIC.to_le_bytes());
        h.extend_from_slice(&(OBJ_FM6VB as u16).to_le_bytes());
        h.extend_from_slice(&0u16.to_le_bytes());
        for v in [1u32, FVB_LEN as u32, crc32(p), 0xFFFF_FFFF, 0xFFFF_FFFF] { h.extend_from_slice(&v.to_le_bytes()); }
        let hc = crc32(&h);
        h.extend_from_slice(&hc.to_le_bytes());
        f[FVB_HOME..FVB_HOME + 32].copy_from_slice(&h);
        f[FVB_HOME + FVB_INFO..FVB_HOME + FVB_INFO + FVB_LEN].copy_from_slice(p);
    }
    if let Some(r) = get(12) {
        for k in 0..3 {
            let rec = &r[k * SLC_LEN..(k + 1) * SLC_LEN];
            let len = get(32 + k as u32).map_or(usize::MAX, |s| s.len());
            if rd32(rec, 0) == SLC_MAGIC && len <= SLC_OFF {
                let at = SMP_BASE + k * SMP_SIZE + SLC_OFF;
                f[at..at + SLC_LEN].copy_from_slice(rec);
            }
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    /// FM1_BK_FLASH=<flash.bin> FM1_BK_OUT=<file>: its export written there; FM1_BK_IN=<backup.json> FM1_BK_FLASH_OUT=<file>:
    /// that backup imported into the flash, written there (p600/tests/flash_capture.c reads both back with the firmware)
    #[test]
    fn files() {
        let Ok(path) = std::env::var("FM1_BK_FLASH") else { return };
        let mut f = std::fs::read(path).unwrap();
        if let Ok(out) = std::env::var("FM1_BK_OUT") {
            let j = export(&f);
            let objs = read(&j).unwrap();
            assert_eq!(objs.len(), 16);
            std::fs::write(out, j).unwrap();
        }
        if let (Ok(inp), Ok(out)) = (std::env::var("FM1_BK_IN"), std::env::var("FM1_BK_FLASH_OUT")) {
            let objs = read(&std::fs::read_to_string(inp).unwrap()).unwrap();
            import(&mut f, &objs).unwrap();
            std::fs::write(out, &f).unwrap();
            // and its export again: the same objects (but the current music and settings, none when the backup has none)
            let again = read(&export(&f)).unwrap();
            for ((ia, a), (ib, b)) in objs.iter().zip(&again) {
                assert_eq!(ia, ib);
                if *ia != 8 { assert_eq!(a, b, "object {ia}"); }
            }
        }
    }
    #[test]
    fn base64_round_trip() {
        for n in 0..10 {
            let b: Vec<u8> = (0..n).map(|i| (i * 37 + 5) as u8).collect();
            assert_eq!(unb64(&b64(&b)).unwrap(), b);
        }
    }
}
