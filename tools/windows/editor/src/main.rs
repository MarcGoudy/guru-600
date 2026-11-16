// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 Editor for Windows (16/11/2026, Marc): opens the editor kept next to this program (editor\index.html), so it
// works without Internet and whatever the browser has kept or cleared, in a window of its own (--app: no address bar,
// no tabs), in a browser with MIDI: Edge (always on Windows 10 and 11), else Chrome, Brave.
#![windows_subsystem = "windows"]
use std::os::windows::process::CommandExt;
use std::path::PathBuf;
use std::process::Command;

const CREATE_NO_WINDOW: u32 = 0x0800_0000;

// file:///C:/Users/.../editor/index.html, with what is not a plain character percent-encoded (spaces, accents)
fn file_url(p: &PathBuf) -> String {
    let s = p.to_string_lossy().replace('\\', "/");
    let s = s.strip_prefix("//?/").unwrap_or(&s).to_string();
    let mut u = String::from("file:///");
    for b in s.bytes() {
        if b.is_ascii_alphanumeric() || b"/:-._~".contains(&b) { u.push(b as char) } else { u.push_str(&format!("%{:02X}", b)) }
    }
    u
}

// the browsers, where their installers put them
fn browsers() -> Vec<PathBuf> {
    let mut v = Vec::new();
    let roots: Vec<String> = ["ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA"].iter().filter_map(|k| std::env::var(k).ok()).collect();
    for rel in ["Microsoft\\Edge\\Application\\msedge.exe", "Google\\Chrome\\Application\\chrome.exe",
                "BraveSoftware\\Brave-Browser\\Application\\brave.exe"] {
        for r in &roots { v.push(PathBuf::from(r).join(rel)); }
    }
    v
}

#[link(name = "user32")]
extern "system" { fn MessageBoxW(h: *mut u8, text: *const u16, caption: *const u16, kind: u32) -> i32; }
fn wide(s: &str) -> Vec<u16> { s.encode_utf16().chain(std::iter::once(0)).collect() }

fn main() {
    let dir = std::env::current_exe().ok().and_then(|p| p.parent().map(|d| d.to_path_buf())).unwrap_or_default();
    let page = dir.join("editor").join("index.html");
    let arg = format!("--app={}", file_url(&page));
    for b in browsers() {
        if b.is_file() && Command::new(&b).arg(&arg).creation_flags(CREATE_NO_WINDOW).spawn().is_ok() { return; }
    }
    // (else: the App Paths of Windows, through start)
    for name in ["msedge", "chrome", "brave"] {
        if let Ok(st) = Command::new("cmd").args(["/C", "start", "", name, &arg]).creation_flags(CREATE_NO_WINDOW).status() {
            if st.success() { return; }
        }
    }
    let msg = "The Guru-600 editor needs a browser with MIDI: Edge, Chrome or Brave.\n\
               L'éditeur Guru-600 a besoin d'un navigateur avec le MIDI : Edge, Chrome ou Brave.";
    unsafe { MessageBoxW(std::ptr::null_mut(), wide(msg).as_ptr(), wide("Guru-600 Editor").as_ptr(), 0x30); }
}
