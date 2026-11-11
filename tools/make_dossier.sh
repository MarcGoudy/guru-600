#!/bin/zsh
# Après une modification : met à jour l'app Guru-600, le zip, le site, le dossier de diffusion Guru-600 et sa copie sur 1To.
#   p600/make_dossier.sh        (le firmware doit être compilé : Felucca/build/felucca.fwsc)
set -e
F=~/Documents/FM-1; A=/Applications/Guru-600.app; R=$A/Contents/Resources; G=$F/Guru-600
FW=$F/Felucca/build/felucca.fwsc
V=$(sed -n 's/^VERSION = "\(.*\)".*/\1/p' $F/p600/site/make_site_guru.py)   # la version (1.0.1…)
# 1. l'app : firmware, notice
pkill -f "Guru-600.app/Contents/" || true
# l'émulateur (avec sa façade) est l'exécutable même de l'app : sans lanceur en shell, « Ouvrir quand même » le couvre
(cd $F/fm1-emu-src && cargo build --release -p fm1-live 2>&1 | tail -1)
cp $F/fm1-emu-src/target/release/fm1-live $A/Contents/MacOS/Guru-600; rm -f $R/Guru-600
cp $FW $F/Firmwares/guru-600.fwsc; cp $FW $F/Partage/guru-600.fwsc; cp $FW $R/guru-600.fwsc
rm -rf $R/Notice; mkdir -p $R/Notice; (cd $F/p600/notice && cp index.html $R/Notice/ && cp -R img shots fonts $R/Notice/)
codesign --force --deep -s - $A 2>&1 | tail -1
rm -f $F/Partage/Guru-600.zip; ditto -c -k --keepParent $A $F/Partage/Guru-600.zip
# l'installateur Mac (image disque) : le visiteur passe par lui, l'application téléchargée par le navigateur serait bloquée
zsh $F/p600/mac/make_dmg.sh https://guru-600.com/telecharger/Guru-600-Mac.zip $F/Partage > /dev/null
# 2. le site
~/Documents/FM-1/venv/bin/python $F/p600/site/make_site_guru.py $FW $F/Partage/site-installation
# 3. le dossier de diffusion
mkdir -p "$G/1 Firmware" "$G/2 Application Mac" "$G/3 Notice/Notice HTML" "$G/4 Site web" "$G/5 Sources" "$G/6 Licences" "$G/7 Éditeur"
rm -f "$G/1 Firmware/"guru-600-*.fwsc; cp $FW "$G/1 Firmware/guru-600-$V.fwsc"
rm -rf "$G/2 Application Mac/Guru-600.app"; ditto $A "$G/2 Application Mac/Guru-600.app"; cp $F/Partage/Guru-600.zip "$G/2 Application Mac/Guru-600-Mac.zip"; cp $F/Partage/Guru-600-Installer-Mac.dmg "$G/2 Application Mac/"
# l'application Windows, refaite ici (après l'application Mac, à laquelle make_windows.sh compare son firmware)
zsh $F/p600/windows/make_windows.sh > /dev/null
rm -rf "$G/2 Application Windows"; mkdir -p "$G/2 Application Windows"
ditto $F/p600/windows/build/Guru-600 "$G/2 Application Windows/Guru-600"; cp $F/Partage/Guru-600-Windows.zip "$G/2 Application Windows/"
cmp $FW "$G/2 Application Windows/Guru-600/guru-600.fwsc" || { echo "application Windows : firmware périmé (relancer p600/windows/make_windows.sh)"; exit 1; }
cp $F/Partage/"Guru-600 - User guide - Notice.pdf" "$G/3 Notice/"
rm -rf "$G/3 Notice/Notice HTML"; mkdir -p "$G/3 Notice/Notice HTML"; (cd $F/p600/notice && cp index.html "$G/3 Notice/Notice HTML/" && cp -R img shots fonts "$G/3 Notice/Notice HTML/")
rm -rf "$G/4 Site web"; ditto $F/Partage/site-installation "$G/4 Site web"
# l'éditeur web et son guide, côte à côte (son « ? » ouvre ../guide/), comme sur le site, avec le PDF du guide
E="$G/7 Éditeur/Guru-600 Editor"; rm -rf "$G/7 Éditeur"; mkdir -p "$E"
ditto $F/Partage/site-installation/editor "$E/editor"; ditto $F/Partage/site-installation/guide "$E/guide"
cp $F/Partage/"Guru-600 Editor - Guide.pdf" "$E/"
(cd "$G/7 Éditeur" && ditto -c -k --keepParent "Guru-600 Editor" "Guru-600-Editor.zip")
T=$(mktemp -d)
(cd $F/Felucca && git diff > "$G/5 Sources/guru-600-vs-felucca-63f88ec.patch" && mkdir -p $T/guru-600-firmware &&
 { git ls-files -co --exclude-standard | grep -v '^build/'; } | while read f; do [ -f "$f" ] && mkdir -p "$T/guru-600-firmware/$(dirname "$f")" && cp "$f" "$T/guru-600-firmware/$f"; done)
(cd $F/Felucca/firmware/engines && git ls-files | while read f; do mkdir -p "$T/guru-600-firmware/firmware/engines/$(dirname "$f")"; cp "$f" "$T/guru-600-firmware/firmware/engines/$f"; done)
mkdir -p $T/guru-600-tools; rsync -a --exclude 'build/' --exclude 'dbg/' --exclude 'wav*/' --exclude 'manuels/' --exclude 'American Uncial*' --exclude '*.wav' --exclude 'splash/' --exclude '__pycache__' --exclude 'windows/build/' --exclude '*.o' $F/p600/ $T/guru-600-tools/
(cd $F/fm1-emu-src && git diff > "$G/5 Sources/fm1-emu-guru-600.patch" && mkdir -p $T/fm1-emu-guru-600 && git ls-files -co --exclude-standard | grep -v '^target/' | while read f; do mkdir -p "$T/fm1-emu-guru-600/$(dirname "$f")"; cp "$f" "$T/fm1-emu-guru-600/$f"; done)
rm -f "$G/5 Sources/"*.zip
(cd $T && zip -qr "$G/5 Sources/guru-600-firmware-source.zip" guru-600-firmware && zip -qr "$G/5 Sources/guru-600-tools-source.zip" guru-600-tools && zip -qr "$G/5 Sources/fm1-emu-guru-600-source.zip" fm1-emu-guru-600)
rm -rf $T
# 4. la copie sur 1To, puis la vérification
if [ -d /Volumes/1To ]; then
  # (8, 9, 10 : seulement sur le 1To — firmwares officiels, annonces, sauvegardes du FM-1 — jamais effacés)
  rsync -a --delete --exclude "8 Firmwares officiels M-VAVE" --exclude "9 Diffusion" --exclude "10 Sauvegardes FM-1" "$G/" /Volumes/1To/Guru-600/
  diff -rq -x "8 Firmwares officiels M-VAVE" -x "9 Diffusion" -x "10 Sauvegardes FM-1" "$G" /Volumes/1To/Guru-600 && echo "1To : copie identique"
else
  echo "1To non monté : copie à refaire"
fi
cmp -s $FW "$G/1 Firmware/guru-600-$V.fwsc" && cmp -s $FW "$G/4 Site web/firmware/guru-600-$V.fwsc" && cmp -s $FW $R/guru-600.fwsc && echo "firmware identique partout"
