#!/bin/zsh
# La fiche KeyStep à imprimer (A4 paysage) : p600/keystep/make_fiche.sh -> KeyStep-Guru-600.pdf (+ aperçu PNG)
set -e
H=${0:A:h}; F=~/Documents/FM-1
V=$(sed -n 's/^#define GURU_VERSION "\(.*\)".*/\1/p' $F/Felucca/firmware/src/guru_version.h)
sed "s/__VERSION__/$V/" $H/fiche.html > $H/.fiche-v.html
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; P=$(mktemp -d)
"$C" --headless=new --user-data-dir=$P --no-pdf-header-footer --print-to-pdf=$H/KeyStep-Guru-600.pdf "file://$H/.fiche-v.html" 2>/dev/null
"$C" --headless=new --user-data-dir=$P --window-size=1123,794 --hide-scrollbars --screenshot=$H/apercu.png "file://$H/.fiche-v.html" 2>/dev/null
rm -rf $P $H/.fiche-v.html
echo "KeyStep-Guru-600.pdf ($V)"
