#!/bin/zsh
# Guru-600 pour Windows : compile l'émulateur fm1-live pour Windows x86-64 depuis le Mac (rustup + mingw-w64),
# avec l'icône et la fiche de version (guru-600.rc), puis assemble le dossier « Guru-600 » et Partage/Guru-600-Windows.zip :
#   Guru-600.exe        double-clic : il trouve guru-600.fwsc à côté de lui, garde la mémoire dans %APPDATA%\Guru-600
#   guru-600.fwsc       le firmware (celui de Felucca/build, comme l'application Mac)
#   Notice\             la notice (menu Aide)
#   Licences\           les licences
#   LISEZMOI.txt / README.txt
# Prérequis (une fois) : brew install mingw-w64 rustup ; rustup toolchain install stable --target x86_64-pc-windows-gnu
set -e
F=~/Documents/FM-1
W=$F/p600/windows
E=$F/fm1-emu-src
R=/Applications/Guru-600.app/Contents/Resources
V=$(sed -n 's/^VERSION = "\(.*\)".*/\1/p' $F/p600/site/make_site_guru.py)
T=~/.rustup/toolchains/stable-aarch64-apple-darwin/bin

grep -q "VERSION: &str = \"$V\"" $E/crates/fm1-live/src/win.rs || { echo "win.rs VERSION != $V"; exit 1; }
sed -i '' "s/FILEVERSION .*/FILEVERSION ${V//./,},0/; s/PRODUCTVERSION .*/PRODUCTVERSION ${V//./,},0/; s/\"FileVersion\", \".*\"/\"FileVersion\", \"$V\"/; s/\"ProductVersion\", \".*\"/\"ProductVersion\", \"$V\"/" $W/guru-600.rc
(cd $W && x86_64-w64-mingw32-windres -c 1252 guru-600.rc -O coff -o guru-600-res.o)

cd $E
CARGO_TARGET_X86_64_PC_WINDOWS_GNU_LINKER=x86_64-w64-mingw32-gcc RUSTC=$T/rustc \
CARGO_TARGET_X86_64_PC_WINDOWS_GNU_RUSTFLAGS="-C link-arg=$W/guru-600-res.o" \
    $T/cargo build --release -p fm1-live --target x86_64-pc-windows-gnu

O=$W/build/Guru-600
rm -rf $W/build; mkdir -p $O
cp $E/target/x86_64-pc-windows-gnu/release/fm1-live.exe $O/Guru-600.exe
cp $F/Felucca/build/felucca.fwsc $O/guru-600.fwsc
cp -R $R/Notice $O/Notice
cp -R $R/Licences $O/Licences
cp $W/LISEZMOI.txt $W/README.txt $O/
find $O -name .DS_Store -delete
cmp $O/guru-600.fwsc $R/guru-600.fwsc || { echo "firmware différent de l'application Mac"; exit 1; }

mkdir -p $F/Partage
rm -f $F/Partage/Guru-600-Windows.zip
(cd $W/build && zip -qr -X $F/Partage/Guru-600-Windows.zip Guru-600)
ls -la $O $F/Partage/Guru-600-Windows.zip
echo "Guru-600 $V pour Windows : $F/Partage/Guru-600-Windows.zip"
