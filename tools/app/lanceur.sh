#!/bin/sh
# Guru-600 : le lanceur de l'application (Contents/MacOS/Guru-600). Il remplace son propre processus par l'émulateur
# fm1-emu (Contents/Resources/Guru-600) et le firmware Felucca + P600 : le Dock montre donc l'icône et le nom de
# l'application pendant l'utilisation. La mémoire flash du FM-1 émulé (sons enregistrés, importés, projets) est gardée
# entre deux lancements dans ~/Library/Application Support/Guru-600/flash.bin. Le menu Aide ouvre la notice ; le menu
# Sauvegarde exporte cette mémoire en sauvegarde de l'éditeur web Felucca, ou en importe une (fm1-live, backup.rs).
R="$(cd "$(dirname "$0")/../Resources" && pwd)"
D="$HOME/Library/Application Support/Guru-600"
mkdir -p "$D"
xattr -d com.apple.quarantine "$R/Guru-600" 2>/dev/null
case "$(defaults read -g AppleLocale 2>/dev/null)" in
    fr*) MT="Aide";  MI="Notice d'utilisation du Guru-600"; BT="Sauvegarde"; BE="Exporter une sauvegarde…"; BI="Importer une sauvegarde…"; WT="Fenêtre"; AT="À propos du Guru-600" ;;
    de*) MT="Hilfe"; MI="Guru-600 Bedienungsanleitung"; BT="Backup"; BE="Backup exportieren…"; BI="Backup importieren…"; WT="Fenster"; AT="Über Guru-600" ;;
    es*) MT="Ayuda"; MI="Manual de usuario del Guru-600"; BT="Copia de seguridad"; BE="Exportar copia de seguridad…"; BI="Importar copia de seguridad…"; WT="Ventana"; AT="Acerca de Guru-600" ;;
    it*) MT="Aiuto"; MI="Manuale d'uso del Guru-600"; BT="Backup"; BE="Esporta backup…"; BI="Importa backup…"; WT="Finestra"; AT="Informazioni su Guru-600" ;;
    *)   MT="Help";  MI="Guru-600 User Guide"; BT="Backup"; BE="Export Backup…"; BI="Import Backup…"; WT="Window"; AT="About Guru-600" ;;
esac
exec "$R/Guru-600" --fwsc "$R/guru-600.fwsc" --flash "$D/flash.bin" --help-menu "$MT" "$MI" "$R/Notice/index.html" \
    --backup-menu "$BT" "$BE" "$BI" --window-menu "$WT" \
    --about "$AT" "guru-600" "A PROPHET-600 TRIBUTE" "by Marc Massé, v1.0" "based on Felucca by Leo Kuroshita" \
    "$R/Notice/fonts/MonRong.ttf" "$R/Notice/fonts/InterTight.ttf"
