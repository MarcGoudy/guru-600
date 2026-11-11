//! Guru-600 on Windows: what the Mac's launcher (Contents/MacOS/Guru-600) and its dialogs (osascript) do there.
//!
//! Started with no arguments (a double-click on Guru-600.exe), the options the Mac's launcher gives are made here:
//! the firmware guru-600.fwsc next to the program, the flash memory kept in %APPDATA%\Guru-600\flash.bin, the
//! menus in the user's language (Help opens Notice\index.html next to the program). The file dialogs and the
//! messages are Windows' own (PowerShell's System.Windows.Forms, MessageBoxW).

use std::os::windows::process::CommandExt;
use std::path::PathBuf;
use std::process::Command;

/// the version shown in Help > About
pub const VERSION: &str = "1.0.1";

const CREATE_NO_WINDOW: u32 = 0x0800_0000;

#[link(name = "kernel32")]
extern "system" {
    fn GetUserDefaultLocaleName(name: *mut u16, len: i32) -> i32;
}
#[link(name = "user32")]
extern "system" {
    fn MessageBoxW(hwnd: *mut core::ffi::c_void, text: *const u16, caption: *const u16, kind: u32) -> i32;
}

fn wide(s: &str) -> Vec<u16> {
    s.encode_utf16().chain(std::iter::once(0)).collect()
}

/// the user's language: "fr", "de", "es", "it", or "en"
fn lang() -> String {
    let mut b = [0u16; 85];
    let n = unsafe { GetUserDefaultLocaleName(b.as_mut_ptr(), b.len() as i32) };
    let s = if n > 1 { String::from_utf16_lossy(&b[..n as usize - 1]) } else { String::new() };
    s.split('-').next().unwrap_or("").to_lowercase()
}

/// the menus' words, as the Mac's launcher has them: (Help, its item, Backup, Export, Import, About)
fn words() -> [&'static str; 6] {
    match lang().as_str() {
        "fr" => ["Aide", "Notice d'utilisation du Guru-600", "Sauvegarde", "Exporter une sauvegarde…", "Importer une sauvegarde…", "À propos du Guru-600"],
        "de" => ["Hilfe", "Guru-600 Bedienungsanleitung", "Backup", "Backup exportieren…", "Backup importieren…", "Über Guru-600"],
        "es" => ["Ayuda", "Manual de usuario del Guru-600", "Copia de seguridad", "Exportar copia de seguridad…", "Importar copia de seguridad…", "Acerca de Guru-600"],
        "it" => ["Aiuto", "Manuale d'uso del Guru-600", "Backup", "Esporta backup…", "Importa backup…", "Informazioni su Guru-600"],
        _ => ["Help", "Guru-600 User Guide", "Backup", "Export Backup…", "Import Backup…", "About Guru-600"],
    }
}

/// the About item's title (the Help menu's second item)
pub fn about_title() -> String {
    words()[5].to_string()
}

/// a double-click on Guru-600.exe: the Mac launcher's options, with the files next to the program
pub fn default_args() -> Option<Vec<String>> {
    let here: PathBuf = std::env::current_exe().ok()?.parent()?.to_path_buf();
    let fwsc = here.join("guru-600.fwsc");
    if !fwsc.exists() {
        return None;
    }
    let data = PathBuf::from(std::env::var_os("APPDATA")?).join("Guru-600");
    let _ = std::fs::create_dir_all(&data);
    let w = words();
    let s = |p: PathBuf| p.to_string_lossy().into_owned();
    Some(vec![
        "Guru-600".into(),
        "--fwsc".into(), s(fwsc),
        "--flash".into(), s(data.join("flash.bin")),
        "--help-menu".into(), w[0].into(), w[1].into(), s(here.join("Notice").join("index.html")),
        "--backup-menu".into(), w[2].into(), w[3].into(), w[4].into(),
    ])
}

/// the user guide (or any file) in its usual program
pub fn open(file: &str) {
    let _ = Command::new("explorer").arg(file).spawn();
}

/// Windows' own file dialog: where to save the backup (`save`), or which one to open
pub fn choose_file(save: bool) -> Option<String> {
    let dialog = if save {
        "$d=New-Object System.Windows.Forms.SaveFileDialog;$d.FileName='Guru-600 backup.json';$d.DefaultExt='json';"
    } else {
        "$d=New-Object System.Windows.Forms.OpenFileDialog;"
    };
    let script = format!(
        "[Console]::OutputEncoding=[Text.Encoding]::UTF8;Add-Type -AssemblyName System.Windows.Forms;{dialog}\
         $d.Filter='JSON (*.json)|*.json';$f=New-Object System.Windows.Forms.Form -Property @{{TopMost=$true}};\
         if($d.ShowDialog($f) -eq 'OK'){{[Console]::Out.Write($d.FileName)}}"
    );
    let out = Command::new("powershell")
        .args(["-NoProfile", "-STA", "-Command", &script])
        .creation_flags(CREATE_NO_WINDOW)
        .output()
        .ok()?;
    let p = String::from_utf8_lossy(&out.stdout).trim().to_string();
    (!p.is_empty()).then(|| if save && !p.to_lowercase().ends_with(".json") { format!("{p}.json") } else { p })
}

/// a message box (a backup that could not be read or written, or About)
pub fn message(title: &str, text: &str) {
    let (t, c) = (wide(text), wide(title));
    unsafe {
        MessageBoxW(core::ptr::null_mut(), t.as_ptr(), c.as_ptr(), 0x40 /* MB_ICONINFORMATION */);
    }
}

/// Help > About
pub fn about() {
    message(
        &about_title(),
        &format!("Guru-600\nA PROPHET-600 TRIBUTE\n\nby Marc Massé, v{VERSION}\nbased on Felucca by Leo Kuroshita\n\nhttps://marcgoudy.github.io/guru-600/"),
    );
}
