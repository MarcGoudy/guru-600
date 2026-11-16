#!/bin/zsh
# Guru-600 Editor pour Windows (16/11/2026, Marc) : « Guru-600 Editor.exe » (icône Guru-600) ouvre l'éditeur rangé à côté de lui
# (editor\index.html) dans une fenêtre à part d'Edge (ou Chrome, Brave) : hors ligne, sans dépendre du navigateur.
#   make_editor_windows.sh  ->  p600/windows/editor/build/Guru-600 Editor  et  Partage/Guru-600-Editor-Windows.zip
set -e
F=~/Documents/FM-1; W=${0:A:h}; S=$F/Partage/site-installation; T=~/.rustup/toolchains/stable-aarch64-apple-darwin/bin
V=$(sed -n 's/^#define GURU_VERSION "\(.*\)".*/\1/p' $F/Felucca/firmware/src/guru_version.h)
sed -i '' "s/^version = .*/version = \"$V\"/" $W/Cargo.toml
sed -i '' "s/FILEVERSION .*/FILEVERSION ${V//./,},0/; s/PRODUCTVERSION .*/PRODUCTVERSION ${V//./,},0/; s/\"FileVersion\", \".*\"/\"FileVersion\", \"$V\"/; s/\"ProductVersion\", \".*\"/\"ProductVersion\", \"$V\"/" $W/editor.rc
(cd $W && x86_64-w64-mingw32-windres -c 1252 editor.rc -O coff -o editor-res.o)
(cd $W && CARGO_TARGET_X86_64_PC_WINDOWS_GNU_LINKER=x86_64-w64-mingw32-gcc RUSTC=$T/rustc \
  CARGO_TARGET_X86_64_PC_WINDOWS_GNU_RUSTFLAGS="-C link-arg=$W/editor-res.o" $T/cargo build -q --release --target x86_64-pc-windows-gnu)
O="$W/build/Guru-600 Editor"; rm -rf $W/build; mkdir -p "$O"
cp $W/target/x86_64-pc-windows-gnu/release/guru600-editor.exe "$O/Guru-600 Editor.exe"
ditto $S/editor "$O/editor"; ditto $S/guide "$O/guide"; cp $F/Partage/"Guru-600 Editor - Guide.pdf" "$O/"
find "$O" -name .DS_Store -delete
rm -f $F/Partage/Guru-600-Editor-Windows.zip; (cd $W/build && zip -qr -X $F/Partage/Guru-600-Editor-Windows.zip "Guru-600 Editor")
echo "Guru-600 Editor $V pour Windows : $F/Partage/Guru-600-Editor-Windows.zip"
