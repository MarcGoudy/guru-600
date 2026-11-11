#!/bin/zsh
# L'image disque Mac du Guru-600 (dmgbuild) : une fenêtre avec le fond dmg/fond@2x.png (les trois étapes) et
# l'installateur « Installer Guru-600 » (document script, icône Guru-600, sans extension) dans le cadre.
#   make_dmg.sh [adresse du zip de l'application] [dossier de sortie]
set -e
H=${0:A:h}; URL=${1:-https://guru-600.com/telecharger/Guru-600-Mac.zip}; OUT=${2:-$HOME/Documents/FM-1/Partage}
ICNS="$HOME/Documents/FM-1/Guru-600/2 Application Mac/Guru-600.app/Contents/Resources/applet.icns"
T=$(mktemp -d)
sed "s#https://guru-600.com/telecharger/Guru-600-Mac.zip#$URL#" $H/installer.applescript > $T/i.applescript
# l'installateur : un lanceur de trois lignes (ce qu'on voit), le programme dans Scripts/installer.scpt,
# l'icône, et la description illustrée (le bas de la fenêtre de l'Éditeur de script)
B="$T/Installer Guru-600.scptd"; osacompile -o "$B" $H/lanceur.applescript
osacompile -o "$B/Contents/Resources/Scripts/installer.scpt" $T/i.applescript
cp "$ICNS" "$B/Contents/Resources/guru600.icns"
# la fenêtre de l'Éditeur de script : la partie code repliée, seulement la description (réglages de Marc)
/usr/libexec/PlistBuddy -c "Add :WindowState dict" -c "Add :WindowState:name string ScriptWindowState" \
  -c "Add :WindowState:positionOfDivider real 0" -c "Add :WindowState:dividerCollapsed bool false" \
  -c "Add :WindowState:bundleDividerCollapsed bool true" -c "Add :WindowState:eventLogLevel integer 2" \
  -c "Add :WindowState:selectedTab string description" \
  -c "Add :WindowState:savedFrame string '150 140 680 760 0 0 1710 1073 '" "$B/Contents/Info.plist" >/dev/null
# la description (le bas de la fenêtre) : une seule image, dmg/description@2x.png (logo + la procédure en 7 langues),
# dessinée depuis dmg/description-image.html ; 640 x 640 points
R="$B/Contents/Resources/description.rtfd"; rm -rf "$R"; mkdir -p "$R"; sips -s dpiWidth 144 -s dpiHeight 144 $H/dmg/description@2x.png --out "$R/description.png" >/dev/null   # (144 ppp : 640 x 640 points, net en Retina)
printf '%s' '{\rtf1\ansi\ansicpg1252\cocoartf2908
{\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
\pard\qc\partightenfactor0
\f0\fs24 {{\NeXTGraphic description.png \width12800 \height12800 \appleattachmentpadding0 \appleembedtype0 \appleaqc
}'"$(printf '\xac')"'}}' > "$R/TXT.rtf"
osascript -l JavaScript -e "ObjC.import('AppKit'); \$.NSWorkspace.sharedWorkspace.setIconForFileOptions(\$.NSImage.alloc.initWithContentsOfFile('$ICNS'), '$B', 0)" >/dev/null
sips -z 420 660 $H/dmg/fond@2x.png --out $T/f1.png >/dev/null; sips -s dpiWidth 144 -s dpiHeight 144 $H/dmg/fond@2x.png --out $T/f2.png >/dev/null
tiffutil -cathidpicheck $T/f1.png $T/f2.png -out $T/fond.tiff >/dev/null 2>&1
rm -f "$OUT/Guru-600-Installer-Mac.dmg"
$HOME/Documents/FM-1/venv/bin/dmgbuild -s $H/dmg/reglages.py -D installer="$B" -D icns="$ICNS" -D fond=$T/fond.tiff "Guru-600" "$OUT/Guru-600-Installer-Mac.dmg" >/dev/null
rm -rf $T; echo "$OUT/Guru-600-Installer-Mac.dmg"
