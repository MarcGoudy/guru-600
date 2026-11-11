//! The FM-1 front panel, drawn after M-VAVE's official photos of the FM-1 (cuvave.com, the
//! front views of its six colours): MASTER / SELECT / PRESETS / ALGORITHM top left with OCT- /
//! OCT+ under them, the screen in the middle, KNOB1-4 and two rows of six buttons on the right,
//! and the 27 silicone keys (F3..G5) across the bottom.
//!
//! Guru-600: the knobs, buttons, keys, their words and the colours are the photos', at the
//! photos' scale (K1: the photo's LCD is 153 of its pixels for 240); the screen is shown larger
//! than on the FM-1, 1.625 times its size, to be read easily, and the layout around it is Marc
//! Massé's (his retouched capture of 11 November 2026: places in points, in the body). The
//! including crate sets `PANEL_SCALE`: 1 (the browser, the plugin, Windows), 2 draws everything
//! twice as fine (the Mac's window, shown at half size: sharp on a Retina screen). The words on
//! the buttons and keys are masks made by tools/panel_labels.py.

use std::sync::atomic::{AtomicUsize, Ordering};

pub const S: usize = crate::PANEL_SCALE;
const SF: f32 = S as f32;
/// Panel pixels (at scale 1) per photo unit: the photo's LCD is 240 pixels in 153.
const K1: f32 = 240.0 / 153.0;
/// The room around the body, points.
const M1: f32 = 22.0;
const M: f32 = M1 * SF;
/// The body, points.
const BODY_W: f32 = 1411.0;
const BODY_H: f32 = 856.0;
/// The LCD: 240 pixels shown 1.625 times (390 points), its top left corner in the body.
pub const LCD_ZOOM: f32 = 1.625;
const LCD_PT: f32 = 240.0 * LCD_ZOOM;
const LCD_AT: (f32, f32) = (337.0, 39.0);
/// The black glass round it: margins left / right, top, bottom (points).
const BZ_SIDE: f32 = 19.5;
const BZ_TOP: f32 = 19.5;
const BZ_BOTTOM: f32 = 24.5;

pub const W: usize = ((BODY_W + 2.0 * M1) * SF + 0.5) as usize;
pub const H: usize = ((BODY_H + 2.0 * M1) * SF + 0.5) as usize;
pub const LCD_X: usize = ((M1 + LCD_AT.0) * SF + 0.5) as usize;
pub const LCD_Y: usize = ((M1 + LCD_AT.1) * SF + 0.5) as usize;
/// The LCD's side on the panel, pixels.
pub const LCD_N: usize = (LCD_PT * SF + 0.5) as usize;

pub const ROOM: u32 = 0x18191b;
pub const AMBER: u32 = 0xf2a33a;

/// A place in the body (points) to panel pixels.
const fn at(v: f32) -> f32 {
    M + v * SF
}
/// Points to panel pixels.
const fn p1(v: f32) -> f32 {
    v * SF
}
/// Photo units to panel pixels (the size of everything but the screen).
const fn cs(v: f32) -> f32 {
    v * K1 * SF
}
const fn ks(v: f32) -> f32 {
    cs(v)
}
const fn kvs(v: f32) -> f32 {
    cs(v)
}

// ---------------------------------------------------------------- colours --

/// One of the FM-1's six colours, as M-VAVE sells them (cuvave.com/product?id=fm-1), each
/// measured on its front photo (Purple: on Marc Massé's corrected photo, Purple.psd).
pub struct Colour {
    /// M-VAVE's name for it
    pub name: &'static str,
    /// the aluminium body
    body: u32,
    /// the silicone trays, around the keys
    tray: u32,
    /// the silicone keys
    key: u32,
    /// the silicone buttons
    btn: u32,
    /// the words printed on the body
    silk: u32,
    /// the words on the buttons and keys
    ink: u32,
    /// the line on each key
    line: u32,
}

pub const COLOURS: [Colour; 6] = [
    Colour { name: "Black", body: 0x4e4f4e, tray: 0x333434, key: 0x2c2d2b, btn: 0x282828, silk: 0xd9dada, ink: 0xf4f4f4, line: 0x6f7070 },
    Colour { name: "Purple", body: 0xd596ba, tray: 0x88618d, key: 0x815984, btn: 0x8b638f, silk: 0xfde9f3, ink: 0x221422, line: 0x302332 },
    Colour { name: "Orange", body: 0xc3724d, tray: 0x91584b, key: 0x824b3f, btn: 0x855042, silk: 0xfff3ea, ink: 0x321f18, line: 0x2e2420 },
    Colour { name: "Black-Green", body: 0x4c4b4e, tray: 0x76d0c3, key: 0x6ecabc, btn: 0x7ad2c5, silk: 0xeae9ec, ink: 0x0b2b2b, line: 0x1a333c },
    Colour { name: "Cool Gray", body: 0xe3d9cf, tray: 0x404448, key: 0x3a3c3d, btn: 0x45494a, silk: 0x2e2722, ink: 0x2a2e2f, line: 0x303435 },
    Colour { name: "White-Blue", body: 0xf1ede7, tray: 0x547393, key: 0x466481, btn: 0x587592, silk: 0x3d4a66, ink: 0x1c2d36, line: 0x222f3a },
];

static COLOUR: AtomicUsize = AtomicUsize::new(0);

/// Draw in colour `i` (COLOURS) from now on; the base must be made again.
pub fn set_colour(i: usize) {
    COLOUR.store(i.min(COLOURS.len() - 1), Ordering::Relaxed);
}

pub fn colour() -> usize {
    COLOUR.load(Ordering::Relaxed)
}

fn col() -> &'static Colour {
    &COLOURS[colour()]
}

// ---------------------------------------------------------------- layout --

/// What a point on the panel is.
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Ctl {
    /// An encoder: index into `ENCS`.
    Enc(usize),
    /// The MASTER pot (SARADC ch 4).
    Pot,
    /// A button: its matrix key id (0..13).
    Btn(u8),
    /// A note key: its matrix key id (14..40).
    Key(u8),
}

/// Knob radius, units.
const KNOB_R: f32 = 19.0;
/// The knobs' places (points): the left columns and rows, the right row.
const LCOL: [f32; 2] = [75.5, 225.2];
const LROW: [f32; 2] = [128.8, 280.8];
const RCOL: [f32; 4] = [832.8, 994.9, 1157.0, 1319.1];

/// Encoders: (label, matrix encoder, centre x, centre y, radius).
pub const ENCS: [(&str, u8, f32, f32, f32); 7] = [
    ("SELECT", 0, at(LCOL[1]), at(LROW[0]), cs(KNOB_R)),
    ("PRESETS", 6, at(LCOL[0]), at(LROW[1]), cs(KNOB_R)),
    ("ALGORITHM", 1, at(LCOL[1]), at(LROW[1]), cs(KNOB_R)),
    ("KNOB1", 2, at(RCOL[0]), at(LROW[0]), cs(KNOB_R)),
    ("KNOB2", 3, at(RCOL[1]), at(LROW[0]), cs(KNOB_R)),
    ("KNOB3", 4, at(RCOL[2]), at(LROW[0]), cs(KNOB_R)),
    ("KNOB4", 5, at(RCOL[3]), at(LROW[0]), cs(KNOB_R)),
];
pub const POT: (f32, f32, f32) = (at(LCOL[0]), at(LROW[0]), cs(KNOB_R));

/// The first button's centre (FX) and the OCT buttons' (points); the photo's pitches.
const FX_AT: (f32, f32) = (851.8, 288.8);
const OCT_AT: [(f32, f32); 2] = [(113.2, 399.5), (214.8, 399.5)];
/// The first lower key's centre x and the lower keys' top (points).
const KEY0_X: f32 = 108.8;
const KEYS_Y: f32 = 644.3;

/// Buttons: (label, matrix id, x, y, w, h) in panel pixels.
pub fn buttons() -> Vec<(&'static str, u8, f32, f32, f32, f32)> {
    // (a little larger than the photo's 59.5 x 34.5 and 48 x 46: Marc Massé's choice)
    let (ow, oh) = (cs(61.5), cs(37.0));
    let mut v = vec![
        ("OCT-", 0, at(OCT_AT[0].0) - ow / 2.0, at(OCT_AT[0].1) - oh / 2.0, ow, oh),
        ("OCT+", 1, at(OCT_AT[1].0) - ow / 2.0, at(OCT_AT[1].1) - oh / 2.0, ow, oh),
    ];
    let rows: [[(&str, u8); 6]; 2] = [
        [("FX", 2), ("SEL", 3), ("ENV", 4), ("LFO", 5), ("EDIT", 6), ("GLO", 7)],
        [("HOME", 8), ("SAVE", 9), ("ARP", 10), ("SEQ", 11), ("PLAY/STOP", 12), ("REC", 13)],
    ];
    let (bw, bh) = (cs(51.0), cs(49.0));
    for (r, row) in rows.iter().enumerate() {
        for (i, (name, id)) in row.iter().enumerate() {
            let (cx, cy) = (at(FX_AT.0) + cs(56.6) * i as f32, at(FX_AT.1) + cs(57.0) * r as f32);
            v.push((*name, *id, cx - bw / 2.0, cy - bh / 2.0, bw, bh));
        }
    }
    v
}

/// The words under the upper keys' lines (none on the last one).
const KEY_WORDS: [&str; 11] = ["OP1", "OP2", "OP3", "OP4", "OP5", "OP6", "PIT", "GLO.", "MONO", "POLY", ""];

/// Photo units of the key area (the photo's x from the first lower key's centre, 71; its y from
/// the lower keys' top, 411) to panel pixels.
const fn kx(u: f32) -> f32 {
    at(KEY0_X) + (u - 71.0) * K1 * SF
}
const fn ky(u: f32) -> f32 {
    at(KEYS_Y) + (u - 411.0) * K1 * SF
}

/// Note keys: (matrix id, x, y, w, h, upper row) in panel pixels.
pub fn keys() -> Vec<(u8, f32, f32, f32, f32, bool)> {
    let mut v = Vec::new();
    // F3..G5: the lower keys are F G A B C D E F G A B C D E F G
    let lower = [0u8, 2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19, 21, 23, 24, 26];
    for (i, n) in lower.iter().enumerate() {
        let cx = 71.0 + 50.5 * i as f32;
        v.push((14 + n, kx(cx - 23.0), ky(411.0), ks(46.0), kvs(87.0), false));
    }
    // an upper key sits over the gap after lower key i
    let upper = [(1u8, 0usize), (3, 1), (5, 2), (8, 4), (10, 5), (13, 7), (15, 8), (17, 9), (20, 11), (22, 12), (25, 14)];
    for (n, after) in upper {
        let cx = 71.0 + 50.5 * (after as f32 + 0.5);
        v.push((14 + n, kx(cx - 23.0), ky(324.0), ks(46.0), kvs(84.0), true));
    }
    v
}

pub fn hit(x: f32, y: f32) -> Option<Ctl> {
    let grip = 6.0 * SF;
    for (i, (_, _, cx, cy, r)) in ENCS.iter().enumerate() {
        if (x - cx).powi(2) + (y - cy).powi(2) <= (r + grip).powi(2) {
            return Some(Ctl::Enc(i));
        }
    }
    if (x - POT.0).powi(2) + (y - POT.1).powi(2) <= (POT.2 + grip).powi(2) {
        return Some(Ctl::Pot);
    }
    let inside = |px: f32, py: f32, w: f32, h: f32| x >= px && x < px + w && y >= py && y < py + h;
    for (_, id, px, py, w, h) in buttons() {
        if inside(px, py, w, h) {
            return Some(Ctl::Btn(id));
        }
    }
    for (id, px, py, w, h, _) in keys() {
        if inside(px, py, w, h) {
            return Some(Ctl::Key(id));
        }
    }
    None
}

// ---------------------------------------------------------------- drawing --

pub fn mix(a: u32, b: u32, t: f32) -> u32 {
    let t = t.clamp(0.0, 1.0);
    let ch = |s: u32| -> u32 {
        let x = ((a >> s) & 255) as f32;
        let y = ((b >> s) & 255) as f32;
        ((x + (y - x) * t).round() as u32) << s
    };
    ch(16) | ch(8) | ch(0)
}

/// Darker (t > 0) or lighter (t < 0).
fn shade(c: u32, t: f32) -> u32 {
    if t >= 0.0 { mix(c, 0x000000, t) } else { mix(c, 0xffffff, -t) }
}

thread_local! {
    /// The width of the canvas being drawn (each panel's `base` / `draw` sets its own).
    static CANVAS_W: std::cell::Cell<usize> = const { std::cell::Cell::new(W) };
}

/// Draw on canvases `w` pixels wide from now on (the SMK-37 panel's is wider).
pub fn canvas(w: usize) {
    CANVAS_W.with(|c| c.set(w));
}

pub fn put(buf: &mut [u32], x: i32, y: i32, c: u32, a: f32) {
    let w = CANVAS_W.with(|c| c.get());
    if x >= 0 && y >= 0 && (x as usize) < w && (y as usize) < buf.len() / w && a > 0.0 {
        let p = &mut buf[y as usize * w + x as usize];
        *p = mix(*p, c, a);
    }
}

/// Rounded rectangle with a vertical gradient, anti-aliased edges.
pub fn rrect(buf: &mut [u32], x: f32, y: f32, w: f32, h: f32, r: f32, top: u32, bot: u32) {
    shape(buf, x, y, w, h, r, 1.0, 1.0, |_, fy| mix(top, bot, (fy - y) / h));
}

/// A rounded rectangle whose edge fades over `soft` pixels (a shadow when large), at opacity
/// `alpha`, coloured by `f(x, y)`.
fn shape(buf: &mut [u32], x: f32, y: f32, w: f32, h: f32, r: f32, soft: f32, alpha: f32, f: impl Fn(f32, f32) -> u32) {
    let r = r.min(w / 2.0).min(h / 2.0);
    let pad = soft.ceil() + 1.0;
    for py in (y - pad).floor() as i32..=(y + h + pad).ceil() as i32 {
        for px in (x - pad).floor() as i32..=(x + w + pad).ceil() as i32 {
            let (fx, fy) = (px as f32 + 0.5, py as f32 + 0.5);
            let qx = (fx - (x + w / 2.0)).abs() - (w / 2.0 - r);
            let qy = (fy - (y + h / 2.0)).abs() - (h / 2.0 - r);
            let d = (qx.max(0.0).powi(2) + qy.max(0.0).powi(2)).sqrt() + qx.max(qy).min(0.0) - r;
            let a = (0.5 - d / soft).clamp(0.0, 1.0);
            if a > 0.0 {
                put(buf, px, py, f(fx, fy), a * alpha);
            }
        }
    }
}

pub fn disc(buf: &mut [u32], cx: f32, cy: f32, r: f32, f: impl Fn(f32, f32) -> u32) {
    for py in (cy - r - 1.0) as i32..=(cy + r + 1.0) as i32 {
        for px in (cx - r - 1.0) as i32..=(cx + r + 1.0) as i32 {
            let (dx, dy) = (px as f32 + 0.5 - cx, py as f32 + 0.5 - cy);
            let d = (dx * dx + dy * dy).sqrt();
            let a = (r - d + 0.5).clamp(0.0, 1.0);
            if a > 0.0 {
                put(buf, px, py, f(dx, dy), a);
            }
        }
    }
}

/// A soft round shadow.
fn soft_disc(buf: &mut [u32], cx: f32, cy: f32, r: f32, soft: f32, c: u32, alpha: f32) {
    for py in (cy - r - soft - 1.0) as i32..=(cy + r + soft + 1.0) as i32 {
        for px in (cx - r - soft - 1.0) as i32..=(cx + r + soft + 1.0) as i32 {
            let (dx, dy) = (px as f32 + 0.5 - cx, py as f32 + 0.5 - cy);
            let d = (dx * dx + dy * dy).sqrt() - r;
            let a = (0.5 - d / soft).clamp(0.0, 1.0);
            if a > 0.0 {
                put(buf, px, py, c, a * a * alpha);
            }
        }
    }
}

/// 5x7 glyphs, one byte per column, bit 0 at the top.
fn glyph(c: char) -> [u8; 5] {
    match c {
        '0' => [0x3E, 0x51, 0x49, 0x45, 0x3E], '1' => [0x00, 0x42, 0x7F, 0x40, 0x00],
        '2' => [0x42, 0x61, 0x51, 0x49, 0x46], '3' => [0x21, 0x41, 0x45, 0x4B, 0x31],
        '4' => [0x18, 0x14, 0x12, 0x7F, 0x10], '5' => [0x27, 0x45, 0x45, 0x45, 0x39],
        '6' => [0x3C, 0x4A, 0x49, 0x49, 0x30], '7' => [0x01, 0x71, 0x09, 0x05, 0x03],
        '8' => [0x36, 0x49, 0x49, 0x49, 0x36], '9' => [0x06, 0x49, 0x49, 0x29, 0x1E],
        'A' => [0x7E, 0x11, 0x11, 0x11, 0x7E], 'B' => [0x7F, 0x49, 0x49, 0x49, 0x36],
        'C' => [0x3E, 0x41, 0x41, 0x41, 0x22], 'D' => [0x7F, 0x41, 0x41, 0x22, 0x1C],
        'E' => [0x7F, 0x49, 0x49, 0x49, 0x41], 'F' => [0x7F, 0x09, 0x09, 0x09, 0x01],
        'G' => [0x3E, 0x41, 0x49, 0x49, 0x7A], 'H' => [0x7F, 0x08, 0x08, 0x08, 0x7F],
        'I' => [0x00, 0x41, 0x7F, 0x41, 0x00], 'J' => [0x20, 0x40, 0x41, 0x3F, 0x01],
        'K' => [0x7F, 0x08, 0x14, 0x22, 0x41], 'L' => [0x7F, 0x40, 0x40, 0x40, 0x40],
        'M' => [0x7F, 0x02, 0x0C, 0x02, 0x7F], 'N' => [0x7F, 0x04, 0x08, 0x10, 0x7F],
        'O' => [0x3E, 0x41, 0x41, 0x41, 0x3E], 'P' => [0x7F, 0x09, 0x09, 0x09, 0x06],
        'Q' => [0x3E, 0x41, 0x51, 0x21, 0x5E], 'R' => [0x7F, 0x09, 0x19, 0x29, 0x46],
        'S' => [0x46, 0x49, 0x49, 0x49, 0x31], 'T' => [0x01, 0x01, 0x7F, 0x01, 0x01],
        'U' => [0x3F, 0x40, 0x40, 0x40, 0x3F], 'V' => [0x1F, 0x20, 0x40, 0x20, 0x1F],
        'W' => [0x3F, 0x40, 0x38, 0x40, 0x3F], 'X' => [0x63, 0x14, 0x08, 0x14, 0x63],
        'Y' => [0x07, 0x08, 0x70, 0x08, 0x07], 'Z' => [0x61, 0x51, 0x49, 0x45, 0x43],
        '+' => [0x08, 0x08, 0x3E, 0x08, 0x08], '-' => [0x08, 0x08, 0x08, 0x08, 0x08],
        '/' => [0x20, 0x10, 0x08, 0x04, 0x02], '.' => [0x00, 0x60, 0x60, 0x00, 0x00],
        '<' => [0x08, 0x14, 0x22, 0x41, 0x00], '>' => [0x00, 0x41, 0x22, 0x14, 0x08],
        _ => [0; 5],
    }
}

/// Text centred on cx, `scale` pixels per font dot.
pub fn text(buf: &mut [u32], cx: f32, y: f32, s: &str, scale: usize, color: u32) {
    let adv = 6 * scale;
    let x0 = cx as i32 - (s.len() * adv) as i32 / 2 + scale as i32 / 2;
    for (i, c) in s.chars().enumerate() {
        for (gx, col) in glyph(c.to_ascii_uppercase()).iter().enumerate() {
            for gy in 0..7 {
                if col >> gy & 1 != 0 {
                    for sy in 0..scale {
                        for sx in 0..scale {
                            let px = x0 + (i * adv + gx * scale + sx) as i32;
                            let py = y as i32 + (gy * scale + sy) as i32;
                            put(buf, px, py, color, 1.0);
                        }
                    }
                }
            }
        }
    }
}

/// The FM-1's silkscreen: its dot font, letters 10 units high, the inked dots centred on cx.
fn silk(buf: &mut [u32], cx: f32, top: f32, s: &str, color: u32) {
    let (dw, dh) = (cs(1.23), cs(1.43));
    // the columns that carry ink (a glyph's blank side columns would put the word off centre)
    let cols: Vec<usize> = s.chars().enumerate()
        .flat_map(|(i, c)| glyph(c).into_iter().enumerate().filter(|(_, g)| *g != 0).map(move |(gx, _)| i * 6 + gx))
        .collect();
    let (first, last) = (*cols.iter().min().unwrap_or(&0) as f32, *cols.iter().max().unwrap_or(&0) as f32);
    let x0 = cx - (first + last + 1.0) * dw / 2.0;
    for (i, c) in s.chars().enumerate() {
        for (gx, col) in glyph(c).iter().enumerate() {
            for gy in 0..7 {
                if col >> gy & 1 != 0 {
                    let (x, y) = (x0 + (i * 6 + gx) as f32 * dw, top + gy as f32 * dh);
                    // (a thin stroke: each dot a little smaller than its place)
                    shape(buf, x + dw * 0.06, y + dh * 0.06, dw * 0.88, dh * 0.88, 0.0, 1.0, 0.95, |_, _| color);
                }
            }
        }
    }
}

/// The word masks (tools/panel_labels.py): (scale, word, width, height, alpha).
fn masks() -> &'static Vec<(u8, &'static str, usize, usize, &'static [u8])> {
    static M: std::sync::OnceLock<Vec<(u8, &'static str, usize, usize, &'static [u8])>> = std::sync::OnceLock::new();
    M.get_or_init(|| {
        let b: &'static [u8] = include_bytes!("panel_labels.bin");
        let mut v = Vec::new();
        let mut i = 0;
        while i + 2 <= b.len() {
            let (s, n) = (b[i], b[i + 1] as usize);
            let word = std::str::from_utf8(&b[i + 2..i + 2 + n]).unwrap_or("");
            let o = i + 2 + n;
            let (w, h) = (u16::from_le_bytes([b[o], b[o + 1]]) as usize, u16::from_le_bytes([b[o + 2], b[o + 3]]) as usize);
            v.push((s, word, w, h, &b[o + 4..o + 4 + w * h]));
            i = o + 4 + w * h;
        }
        v
    })
}

/// A word on a button or key, centred on (cx, cy).
fn word(buf: &mut [u32], cx: f32, cy: f32, w: &str, color: u32) {
    if let Some((_, _, mw, mh, a)) = masks().iter().find(|m| m.0 as usize == S && m.1 == w) {
        let (x0, y0) = ((cx - *mw as f32 / 2.0).round() as i32, (cy - *mh as f32 / 2.0).round() as i32);
        for y in 0..*mh {
            for x in 0..*mw {
                let v = a[y * mw + x];
                if v > 0 {
                    put(buf, x0 + x as i32, y0 + y as i32, color, v as f32 / 255.0);
                }
            }
        }
    }
}

/// The parts that never change: body, trays, screen, printed words.
pub fn base() -> Vec<u32> {
    canvas(W);
    let c = col();
    let mut b = vec![ROOM; W * H];
    let (bx, by, bw, bh) = (M, M, p1(BODY_W), p1(BODY_H));
    let br = p1(56.0);
    // the body: its shadow on the table, its edge, its face
    shape(&mut b, bx, by + p1(8.0), bw, bh, br, p1(20.0), 0.55, |_, _| 0x000000);
    rrect(&mut b, bx, by, bw, bh, br, shade(c.body, 0.10), shade(c.body, 0.30));
    let (top, bot) = (shade(c.body, -0.035), shade(c.body, 0.035));
    shape(&mut b, bx + p1(2.0), by + p1(1.5), bw - p1(4.0), bh - p1(6.0), br - p1(2.0), 1.0, 1.0, |_, fy| mix(top, bot, (fy - by) / bh));
    // a thin light along the top edge
    shape(&mut b, bx + br, by + p1(0.8), bw - 2.0 * br, p1(1.2), 0.0, 1.0, 0.25, |_, _| 0xffffff);
    // the screen: a black glass with a soft rim
    let (sx, sy) = (at(LCD_AT.0 - BZ_SIDE), at(LCD_AT.1 - BZ_TOP));
    let (sw, sh, sr) = (p1(LCD_PT + 2.0 * BZ_SIDE), p1(LCD_PT + BZ_TOP + BZ_BOTTOM), p1(28.0));
    shape(&mut b, sx, sy + p1(2.5), sw, sh, sr, p1(6.0), 0.35, |_, _| 0x000000);
    rrect(&mut b, sx, sy, sw, sh, sr, 0x2a2a2c, 0x1a1a1b);
    rrect(&mut b, sx + p1(2.0), sy + p1(2.0), sw - p1(4.0), sh - p1(4.0), sr - p1(2.0), 0x0f0f10, 0x0b0b0c);
    // the silicone trays: OCT, the buttons, the keys, sunk in the body
    let (fx, fy) = (at(FX_AT.0), at(FX_AT.1));
    let trays = [
        (at((OCT_AT[0].0 + OCT_AT[1].0) / 2.0) - cs(69.0), at(OCT_AT[0].1) - cs(23.5), cs(138.0), cs(47.0), cs(9.0)),
        (fx - cs(38.5), fy - cs(34.0), cs(355.0), cs(125.0), cs(14.0)),
        (kx(38.0), ky(311.0), ks(826.0), kvs(197.0), ks(26.0)),
    ];
    for (x, y, w, h, r) in trays {
        shape(&mut b, x - p1(1.2), y - p1(1.2), w + p1(2.4), h + p1(2.4), r + p1(1.2), 1.0, 0.45, |_, _| shade(c.body, 0.45));
        rrect(&mut b, x, y, w, h, r, shade(c.tray, 0.04), shade(c.tray, -0.02));
    }
    // the little dots: between the button rows, and between the key groups
    disc(&mut b, fx + cs(141.0), fy + cs(28.5), cs(2.2), |_, _| shade(c.tray, 0.8));
    for x in [249.0, 401.0, 603.0, 753.0] {
        disc(&mut b, kx(x), ky(408.0), ks(2.2), |_, _| shade(c.tray, 0.8));
    }
    // the knobs' words, centred over their knobs
    let mut knobs = vec![("MASTER", POT.0, POT.1)];
    knobs.extend(ENCS.iter().map(|e| (e.0, e.2, e.3)));
    for (n, x, y) in knobs {
        silk(&mut b, x, y - cs(44.0), n, c.silk);
    }
    // the knobs' shadows (they stay put when the knobs turn)
    for (x, y, r) in ENCS.iter().map(|e| (e.2, e.3, e.4)).chain([POT]) {
        soft_disc(&mut b, x + cs(2.5), y + cs(4.0), r, cs(5.0), 0x000000, 0.5);
    }
    b
}

/// A knob, seen a little from above as on the photos: its knurled skirt (whose fine ridges turn
/// with it), its flat matt top with a soft chamfer; `pointer` draws MASTER's white mark.
pub fn knob(buf: &mut [u32], cx: f32, cy: f32, r: f32, angle: f32, pointer: bool) {
    // the skirt: fine vertical ridges catching the light from the upper left
    disc(buf, cx + r * 0.02, cy + r * 0.04, r, |dx, dy| {
        let d = (dx * dx + dy * dy).sqrt() / r;
        let a = dy.atan2(dx) - angle;
        let ridge = ((a * 30.0).sin() * 0.5 + 0.5).powi(2);
        let light = ((-dx * 0.6 - dy * 0.8) / r).clamp(-1.0, 1.0) * 0.5 + 0.5;
        let rim = ((d - 0.86) / 0.14).clamp(0.0, 1.0);
        shade(mix(0x0c0c0d, 0x8c8e93, ridge * (0.12 + 0.6 * light) * (1.0 - 0.5 * rim)), 0.0)
    });
    // the top
    let (tx, ty, tr) = (cx - r * 0.05, cy - r * 0.08, r * 0.84);
    disc(buf, tx, ty, tr, |dx, dy| {
        let d = (dx * dx + dy * dy).sqrt() / tr;
        let light = ((-dx * 0.6 - dy * 0.8) / tr).clamp(-1.0, 1.0) * 0.5 + 0.5;
        if d > 0.9 {
            mix(0x161618, 0x55575c, light * light)
        } else {
            mix(0x121214, 0x26272a, light * 0.7 + (1.0 - d) * 0.15)
        }
    });
    if pointer {
        // a short white bar near the edge of the top
        let (s, c) = angle.sin_cos();
        let (from, to, half) = (tr * 0.5, tr * 0.84, tr * 0.11);
        let steps = ((to - from) / 0.5).ceil() as i32;
        for t in 0..=steps {
            let d = from + (to - from) * t as f32 / steps as f32;
            disc(buf, tx + s * d, ty - c * d, half, |_, _| 0xf4f4f0);
        }
    }
}

pub struct State<'a> {
    pub lcd: &'a [u16],
    pub enc_clicks: &'a [i32; 7],
    pub pot: u16,
    pub down: &'a [bool; 41],
    pub leds: &'a [f32; 41],
    #[allow(dead_code)]
    pub turning: &'a [u32; 8],
}

/// LED on-fraction -> brightness as the eye sees it, 0..1. A lit LED is on 1 tick in 11 (the scan's
/// columns); Felucca also lights LEDs far less: the glow of MENU > LEDS (DIM HI ~1/30 of lit, DIM LO
/// ~1/60), the drum grid's mid level (~1/8), a breath (up to ~60 %). The eye is logarithmic (a glow of
/// 1/30 reads well under lit but plainly on), so the level is too: lit 1, ~1/8 0.6, DIM HI ~0.33,
/// DIM LO ~0.2, under 1/200 dark.
fn bright(f: f32) -> f32 {
    let r = f * 11.0;
    if r < 0.005 { 0.0 } else { (1.0 + r.log10() / 2.3).clamp(0.0, 1.0) }
}

/// The colour of a lit LED's light.
const LIT: u32 = 0xfffaf0;

/// A silicone key: its shadow, its side, its face (sunk when held).
fn rubber(buf: &mut [u32], x: f32, y: f32, w: f32, h: f32, r: f32, face: u32, tray: u32, down: bool) {
    let sink = if down { ks(1.6) } else { 0.0 };
    shape(buf, x, y + ks(2.5), w, h, r, ks(3.0), if down { 0.35 } else { 0.6 }, |_, _| shade(tray, 0.45));
    rrect(buf, x, y + sink, w, h, r, shade(face, 0.10), shade(face, 0.30));
    let (fx, fy, fw, fh) = (x + ks(1.6), y + sink + ks(1.0), w - ks(3.2), h - ks(4.2));
    let (top, bot) = if down { (shade(face, 0.10), shade(face, 0.06)) } else { (shade(face, -0.05), shade(face, 0.02)) };
    rrect(buf, fx, fy, fw, fh, r - ks(1.6), top, bot);
}

/// A silicone button, as on the photos: a groove round its foot, a shadow on the tray, its flank
/// showing below, a flat top. Returns the top's centre.
fn pad(buf: &mut [u32], x: f32, y: f32, w: f32, h: f32, r: f32, face: u32, tray: u32, down: bool) -> (f32, f32) {
    let sink = if down { cs(1.4) } else { 0.0 };
    shape(buf, x - cs(1.5), y - cs(1.2), w + cs(3.0), h + cs(3.4), r + cs(1.5), 1.0, 0.8, |_, _| shade(tray, 0.5));
    shape(buf, x + cs(0.8), y + cs(2.2), w, h, r, cs(3.5), if down { 0.25 } else { 0.45 }, |_, _| 0x000000);
    rrect(buf, x, y + sink * 0.5, w, h - sink * 0.5, r, shade(face, 0.14), shade(face, 0.34));
    let (fx, fy, fw, fh) = (x + cs(1.3), y + sink + cs(0.6), w - cs(2.6), h - cs(4.4));
    let (top, bot) = if down { (shade(face, 0.07), shade(face, 0.05)) } else { (shade(face, -0.035), shade(face, 0.01)) };
    rrect(buf, fx, fy, fw, fh, r * 0.85, top, bot);
    (fx + fw / 2.0, fy + fh / 2.0)
}

/// For each of the LCD's LCD_N panel pixels across: the LCD pixel before it and the weight of the
/// next one ("sharp bilinear": each LCD pixel stays flat, only its edge is blended over about one
/// panel pixel, so the zoom need not be a whole number).
fn lcd_taps() -> &'static Vec<(usize, f32)> {
    static T: std::sync::OnceLock<Vec<(usize, f32)>> = std::sync::OnceLock::new();
    T.get_or_init(|| {
        let z = LCD_N as f32 / 240.0;
        (0..LCD_N)
            .map(|o| {
                let s = (o as f32 + 0.5) / z - 0.5;
                let i = s.floor().clamp(0.0, 239.0);
                let f = ((s - i - 0.5) * z + 0.5).clamp(0.0, 1.0);
                (i as usize, if i as usize >= 239 { 0.0 } else { f })
            })
            .collect()
    })
}

/// The LCD (240 x 240 RGB565) on its glass, LCD_N panel pixels square.
fn lcd(buf: &mut [u32], fb: &[u16]) {
    let rgb = |p: u16| -> [f32; 3] {
        let p = p as u32;
        [((p >> 11) * 255 / 31) as f32, (((p >> 5) & 63) * 255 / 63) as f32, ((p & 31) * 255 / 31) as f32]
    };
    let taps = lcd_taps();
    // the rows first (each LCD row blended across), then down (in a buffer kept from frame to frame)
    thread_local! {
        static ROWS: std::cell::RefCell<Vec<[f32; 3]>> = std::cell::RefCell::new(vec![[0f32; 3]; 240 * LCD_N]);
    }
    ROWS.with(|r| lcd_rows(buf, fb, &rgb, taps, &mut r.borrow_mut()));
}

fn lcd_rows(buf: &mut [u32], fb: &[u16], rgb: &impl Fn(u16) -> [f32; 3], taps: &[(usize, f32)], rows: &mut [[f32; 3]]) {
    for y in 0..240 {
        for (ox, &(i, f)) in taps.iter().enumerate() {
            let (a, b) = (rgb(fb[y * 240 + i]), rgb(fb[y * 240 + (i + 1).min(239)]));
            rows[y * LCD_N + ox] = [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f];
        }
    }
    for (oy, &(j, f)) in taps.iter().enumerate() {
        let o = (LCD_Y + oy) * W + LCD_X;
        let (r0, r1) = (j * LCD_N, (j + 1).min(239) * LCD_N);
        for ox in 0..LCD_N {
            let (a, b) = (rows[r0 + ox], rows[r1 + ox]);
            let ch = |k: usize| (a[k] + (b[k] - a[k]) * f).round().clamp(0.0, 255.0) as u32;
            buf[o + ox] = ch(0) << 16 | ch(1) << 8 | ch(2);
        }
    }
}

pub fn draw(buf: &mut [u32], base: &[u32], st: &State) {
    canvas(W);
    buf.copy_from_slice(base);
    let c = col();
    lcd(buf, st.lcd);
    // knobs: encoders turn 18 degrees a click; the pot sweeps 270 degrees
    for (i, (_, _, cx, cy, r)) in ENCS.iter().enumerate() {
        knob(buf, *cx, *cy, *r, (st.enc_clicks[i] as f32 * 18.0).to_radians(), false);
    }
    let pa = (-135.0 + 270.0 * st.pot as f32 / 1023.0).to_radians();
    knob(buf, POT.0, POT.1, POT.2, pa, true);
    // buttons: held ones sink; a lit one's word shines white, as the FM-1's do
    for (name, id, x, y, w, h) in buttons() {
        let down = st.down[id as usize];
        let led = bright(st.leds[id as usize]);
        let (cx, cy) = pad(buf, x, y, w, h, cs(11.0), c.btn, c.tray, down);
        // the LED behind the word: a soft light on the top, the word lit through
        if led > 0.0 {
            shape(buf, cx - cs(18.0), cy - cs(8.0), cs(36.0), cs(16.0), cs(8.0), cs(7.0), 0.28 * led * led, |_, _| LIT);
        }
        let ink = mix(c.ink, 0xffffff, led);
        if let Some((a, b)) = name.split_once('/') {
            word(buf, cx, cy - cs(6.5), a, ink);
            shape(buf, cx - cs(14.5), cy - cs(0.65), cs(29.0), cs(1.3), 0.0, 1.0, 1.0, |_, _| ink);
            word(buf, cx, cy + cs(6.5), b, ink);
        } else {
            word(buf, cx, cy, name, ink);
        }
    }
    // keys: held ones sink; the line on a lit key glows
    let mut upper = 0;
    for (id, x, y, w, h, up) in keys() {
        let down = st.down[id as usize];
        let led = bright(st.leds[id as usize]);
        rubber(buf, x, y, w, h, w / 2.0, c.key, c.tray, down);
        let sink = if down { ks(1.6) } else { 0.0 };
        let cx = x + w / 2.0;
        let line = mix(c.line, LIT, led);
        let lw = ks(5.5);
        let label = if up { KEY_WORDS[upper] } else { "" };
        let (ly, lh) = if label.is_empty() { (y + h / 2.0 - kvs(22.5), kvs(45.0)) } else { (y + kvs(20.0), kvs(24.0)) };
        if led > 0.0 {
            shape(buf, cx - lw / 2.0 - ks(2.0), ly + sink - ks(2.0), lw + ks(4.0), lh + ks(4.0), lw, ks(4.0), 0.6 * led * led, |_, _| LIT);
        }
        rrect(buf, cx - lw / 2.0, ly + sink, lw, lh, lw / 2.0, line, line);
        if !label.is_empty() {
            word(buf, cx, y + kvs(57.0) + sink, label, c.ink);
        }
        if up {
            upper += 1;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Every knob, button and key answers a click in its middle, and the LCD fits its screen.
    #[test]
    fn every_control_is_hit_in_its_middle() {
        for (i, (_, _, cx, cy, _)) in ENCS.iter().enumerate() {
            assert_eq!(hit(*cx, *cy), Some(Ctl::Enc(i)));
        }
        assert_eq!(hit(POT.0, POT.1), Some(Ctl::Pot));
        for (_, id, x, y, w, h) in buttons() {
            assert_eq!(hit(x + w / 2.0, y + h / 2.0), Some(Ctl::Btn(id)));
        }
        let ks = keys();
        assert_eq!(ks.len(), 27);
        for (id, x, y, w, h, _) in ks {
            assert_eq!(hit(x + w / 2.0, y + h / 2.0), Some(Ctl::Key(id)));
        }
        assert!(LCD_X + LCD_N < W && LCD_Y + LCD_N < H);
        for i in 0..COLOURS.len() {
            set_colour(i);
            assert_eq!(base().len(), W * H);
        }
        set_colour(0);
    }

    /// Felucca's LED levels (hal/fm1_input.h) each show: lit > the drum grid's mid > the glow of
    /// MENU > LEDS DIM HI > DIM LO > off.
    #[test]
    fn led_levels_are_told_apart() {
        let lit = 1.0 / 11.0;
        let (mid, hi, lo) = (bright(lit / 8.0 + lit / 30.0), bright(lit / 30.0), bright(lit / 60.0));
        assert_eq!(bright(lit), 1.0);
        assert!(mid > hi + 0.15 && hi > lo + 0.08 && lo > 0.1, "{mid} {hi} {lo}");
        assert_eq!(bright(0.0), 0.0);
    }
}
