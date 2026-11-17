#!/bin/zsh
# Guru-600 Editor pour Mac (16/11/2026, Marc) : une application avec l'icône Guru-600, qui garde l'éditeur et son guide
# dans ses Resources et les ouvre dans une fenêtre à part (launcher.zsh) : hors ligne, sans dépendre du navigateur.
#   make_editor_app.sh  ->  p600/mac/editor/build/Guru-600 Editor.app  et  Partage/Guru-600-Editor-Mac.zip
set -e
F=~/Documents/FM-1; H=${0:A:h}; S=$F/Partage/site-installation
V=$(sed -n 's/^#define GURU_VERSION "\(.*\)".*/\1/p' $F/Felucca/firmware/src/guru_version.h)
A="$H/build/Guru-600 Editor.app"; C="$A/Contents"
rm -rf $H/build; mkdir -p "$C/MacOS" "$C/Resources"
cp $H/launcher.zsh "$C/MacOS/Guru-600 Editor"; chmod +x "$C/MacOS/Guru-600 Editor"
ditto $S/editor "$C/Resources/editor"; ditto $S/guide "$C/Resources/guide"
cp $F/p600/icone/v2/editor.icns "$C/Resources/Guru600.icns"   # (16/11/2026 : l'icône EDITOR de Marc)
cat > "$C/Info.plist" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleName</key><string>Guru-600 Editor</string>
<key>CFBundleDisplayName</key><string>Guru-600 Editor</string>
<key>CFBundleIdentifier</key><string>fr.marcmasse.guru-600-editor</string>
<key>CFBundleExecutable</key><string>Guru-600 Editor</string>
<key>CFBundleIconFile</key><string>Guru600</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
<key>CFBundleShortVersionString</key><string>$V</string>
<key>CFBundleVersion</key><string>$V</string>
<key>LSMinimumSystemVersion</key><string>10.13</string>
<key>NSHighResolutionCapable</key><true/>
</dict></plist>
PL
find "$A" -name .DS_Store -delete
codesign --force --deep -s - "$A" 2>&1 | tail -1
rm -f $F/Partage/Guru-600-Editor-Mac.zip; (cd $H/build && ditto -c -k --keepParent "Guru-600 Editor.app" $F/Partage/Guru-600-Editor-Mac.zip)
echo "Guru-600 Editor $V pour Mac : $F/Partage/Guru-600-Editor-Mac.zip"
